import os
import sys
from yt_dlp import YoutubeDL

def download_playlist(playlist_url):
    """
    Downloads all videos from a YouTube playlist.
    
    Args:
        playlist_url (str): The URL of the YouTube playlist
    """
    # Create downloads directory if it doesn't exist
    download_path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'best',  # Best available quality (single file, no FFmpeg required)
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Output template
        'noplaylist': False,  # Download playlist
        'quiet': False,  # Show progress
        'no_warnings': False,
        'progress_hooks': [progress_hook],
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            print(f"\n📥 Starting download of playlist...")
            print(f"📁 Videos will be saved to: {download_path}\n")
            ydl.download([playlist_url])
            print(f"\n✅ Playlist download completed!")
            print(f"📂 Check the 'downloads' folder for your videos.")
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error occurred: {error_msg}")
        
        if 'ffmpeg' in error_msg.lower():
            print("\n💡 Note: This script downloads the best available quality.")
            print("   For maximum quality, install FFmpeg, but current downloads")
            print("   should still be high quality.\n")
        
        print("Please make sure:")
        print("1. The playlist URL is correct")
        print("2. You have an internet connection")
        print("3. The playlist is public or you have access to it")
        sys.exit(1)

def progress_hook(d):
    """Callback function to show download progress"""
    if d['status'] == 'downloading':
        try:
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            filename = d.get('filename', 'Unknown')
            print(f"Downloading: {os.path.basename(filename)} - {percent} at {speed}")
        except:
            pass
    elif d['status'] == 'finished':
        print(f"✅ Finished: {os.path.basename(d.get('filename', 'Unknown'))}\n")

def main():
    """Main function to get user input and start download"""
    print("=" * 60)
    print("🎵 YouTube Playlist Downloader")
    print("=" * 60)
    print("\nEnter the YouTube playlist URL below.")
    print("Example: https://www.youtube.com/playlist?list=PLxxxxx")
    print("Or: https://www.youtube.com/watch?v=xxxxx&list=PLxxxxx\n")
    
    playlist_url = input("Playlist URL: ").strip()
    
    if not playlist_url:
        print("❌ No URL provided. Exiting...")
        sys.exit(1)
    
    if 'youtube.com' not in playlist_url and 'youtu.be' not in playlist_url:
        print("❌ Invalid YouTube URL. Please enter a valid YouTube playlist URL.")
        sys.exit(1)
    
    download_playlist(playlist_url)

if __name__ == "__main__":
    main()
