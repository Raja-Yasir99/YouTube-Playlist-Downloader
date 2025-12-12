import os
import json
import threading
import time
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_socketio import SocketIO, emit
from yt_dlp import YoutubeDL
import uuid
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year cache for static files

# Try to use eventlet, fallback to threading if not available
try:
    import eventlet
    async_mode = 'eventlet'
except ImportError:
    async_mode = 'threading'
    print("⚠️  eventlet not found, using threading mode. Install eventlet for better performance: pip install eventlet")

socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode, logger=False, engineio_logger=False, ping_timeout=60, ping_interval=25)

# Store download progress
download_progress = {}

# Throttle progress updates to reduce overhead
_last_progress_time = {}

def progress_hook(d, download_id):
    """Callback function to show download progress"""
    if d['status'] == 'downloading':
        try:
            # Throttle updates to every 0.5 seconds
            current_time = time.time()
            if download_id in _last_progress_time:
                if current_time - _last_progress_time[download_id] < 0.5:
                    return
            _last_progress_time[download_id] = current_time
            
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            filename = d.get('filename', 'Unknown')
            
            progress_data = {
                'status': 'downloading',
                'percent': percent,
                'speed': speed,
                'filename': os.path.basename(filename),
            }
            
            download_progress[download_id] = progress_data
            socketio.emit('progress', progress_data, room=download_id)
        except Exception as e:
            print(f"Error in progress hook: {e}")
    elif d['status'] == 'finished':
        filename = d.get('filename', 'Unknown')
        file_basename = os.path.basename(filename)
        progress_data = {
            'status': 'finished',
            'filename': file_basename,
            'message': f'✅ Finished: {file_basename}'
        }
        download_progress[download_id] = progress_data
        socketio.emit('progress', progress_data, room=download_id)
        # Also send a status update
        socketio.emit('status', {
            'status': 'progress',
            'message': f'✅ Video downloaded: {file_basename}'
        }, room=download_id)

def download_playlist_thread(playlist_url, download_id):
    """Download playlist in a separate thread"""
    try:
        # Give client time to join the room
        time.sleep(0.5)
        
        download_path = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        # Send initial status
        socketio.emit('status', {'status': 'starting', 'message': 'Initializing download...'}, room=download_id)
        time.sleep(0.2)  # Small delay to ensure message is sent
        
        # Create progress hook with download_id
        def progress_callback(d):
            progress_hook(d, download_id)
        
        ydl_opts = {
            # Prioritize MP4 format for maximum compatibility
            # Try best MP4 first, then fallback to best quality
            'format': 'best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'noplaylist': False,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [progress_callback],
            # Performance optimizations
            'extract_flat': False,
            'skip_download': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': True,  # Continue on errors
            'no_check_certificate': True,  # Faster connection
            'prefer_insecure': False,
            'socket_timeout': 30,  # Timeout for connections
        }
        
        socketio.emit('status', {'status': 'starting', 'message': 'Connecting to YouTube...'}, room=download_id)
        time.sleep(0.2)
        
        socketio.emit('status', {'status': 'starting', 'message': 'Starting download process...'}, room=download_id)
        time.sleep(0.2)
        
        # Track download progress
        downloaded_count = 0
        total_videos = 0
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                # Get playlist info first to show total count
                try:
                    info = ydl.extract_info(playlist_url, download=False)
                    if 'entries' in info:
                        total_videos = len([e for e in info['entries'] if e])
                        socketio.emit('status', {
                            'status': 'starting', 
                            'message': f'Found {total_videos} videos. Starting downloads...'
                        }, room=download_id)
                except:
                    pass
                
                # Now download
                ydl.download([playlist_url])
                
                # Count downloaded files
                if os.path.exists(download_path):
                    downloaded_count = len([f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f))])
        
        except Exception as download_error:
            error_msg = str(download_error)
            socketio.emit('status', {
                'status': 'error',
                'message': f'❌ Download error: {error_msg}'
            }, room=download_id)
            return
        
        # Send completion status
        completion_msg = f'✅ Playlist download completed! {downloaded_count} video(s) downloaded.'
        socketio.emit('status', {
            'status': 'completed',
            'message': completion_msg,
            'download_path': download_path,
            'downloaded_count': downloaded_count,
            'total_videos': total_videos
        }, room=download_id)
        
    except Exception as e:
        error_msg = str(e)
        socketio.emit('status', {
            'status': 'error',
            'message': f'❌ Error: {error_msg}'
        }, room=download_id)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    """Start playlist download"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        playlist_url = data.get('url', '').strip()
        
        if not playlist_url:
            return jsonify({'error': 'No URL provided'}), 400
        
        if 'youtube.com' not in playlist_url and 'youtu.be' not in playlist_url:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        # Generate unique download ID
        download_id = str(uuid.uuid4())
        
        # Start download in background thread immediately
        thread = threading.Thread(target=download_playlist_thread, args=(playlist_url, download_id))
        thread.daemon = True
        thread.start()
        
        # Return immediately - don't wait for download to start
        return jsonify({
            'download_id': download_id, 
            'message': 'Download request received',
            'status': 'processing'
        })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/downloads')
def list_downloads():
    """List all downloaded files - optimized with caching headers"""
    download_path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_path):
        response = jsonify({'files': []})
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    
    files = []
    try:
        for filename in os.listdir(download_path):
            filepath = os.path.join(download_path, filename)
            if os.path.isfile(filepath):
                files.append({
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'path': f'/downloads/{filename}'
                })
        # Sort by name for consistency
        files.sort(key=lambda x: x['name'])
    except Exception as e:
        print(f"Error listing files: {e}")
    
    response = jsonify({'files': files})
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/downloads/<filename>')
def download_file(filename):
    """Serve downloaded files with proper headers"""
    download_path = os.path.join(os.getcwd(), "downloads")
    filepath = os.path.join(download_path, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_from_directory(
        download_path, 
        filename, 
        as_attachment=True,
        mimetype='application/octet-stream'
    )

@app.route('/static/sw.js')
def service_worker():
    """Serve service worker with correct MIME type"""
    return send_file('static/sw.js', mimetype='application/javascript')

@app.route('/static/manifest.json')
def manifest():
    """Serve manifest with correct MIME type"""
    return send_file('static/manifest.json', mimetype='application/manifest+json')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to server'})

@socketio.on('join')
def handle_join(data):
    """Join a download room"""
    from flask_socketio import join_room
    download_id = data.get('download_id')
    if download_id:
        join_room(download_id)
        # Send confirmation with current status if available
        if download_id in download_progress:
            emit('progress', download_progress[download_id], room=download_id)
        else:
            emit('status', {'status': 'starting', 'message': 'Connected. Preparing download...'}, room=download_id)
        emit('joined', {'message': f'Joined room {download_id}'})

if __name__ == '__main__':
    # Create downloads directory if it doesn't exist
    download_path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # Create icons directory if it doesn't exist
    icons_path = os.path.join(os.getcwd(), "static", "icons")
    if not os.path.exists(icons_path):
        os.makedirs(icons_path)
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("🚀 Starting YouTube Playlist Downloader Web App...")
    print("📱 Open your browser and go to: http://localhost:{}".format(port))
    print("✨ PWA-ready for App Store deployment!")
    
    socketio.run(app, debug=debug, host='0.0.0.0', port=port, use_reloader=False)

