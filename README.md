# YouTube Playlist Downloader 🎵

A **stunning, high-performance** Progressive Web App (PWA) for downloading complete YouTube playlists in high quality. Built with Flask and featuring a **vibrant, colorful UI** with real-time progress updates. **Ready for App Store deployment!**

## Features ✨

- 🎥 **Complete Playlist Downloads** - Download entire YouTube playlists with a single click
- 🎨 **Vibrant Modern UI** - Beautiful gradient-based design with smooth animations
- ⚡ **Lightning Fast** - Optimized for performance with caching, debouncing, and requestAnimationFrame
- 📊 **Real-time Progress** - Live progress updates using WebSocket technology
- 📁 **Download Management** - View and download all your downloaded files
- 🚀 **High Quality** - Downloads videos in the best available quality
- 📱 **PWA Ready** - Installable as a native app on iOS, Android, and desktop
- 🏪 **App Store Ready** - Fully configured for App Store and Play Store deployment
- 🎯 **Mobile Optimized** - Perfect touch interactions and responsive design

## Installation 🛠️

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download

If you have this project, you're all set! Otherwise, download or clone the repository.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage 📖

1. **Start the Application**
   - Run `python app.py` in your terminal
   - Open your browser to `http://localhost:5000`

2. **Download a Playlist**
   - Paste a YouTube playlist URL in the input field
   - Click "Download Playlist" button
   - Watch the real-time progress as videos download

3. **Access Downloads**
   - All downloaded videos are saved in the `downloads/` folder
   - You can view and download files directly from the web interface

## Supported URL Formats

- `https://www.youtube.com/playlist?list=PLxxxxx`
- `https://www.youtube.com/watch?v=xxxxx&list=PLxxxxx`
- Any YouTube playlist URL

## Project Structure 📂

```
Playlist/
├── app.py                 # Flask backend application
├── playlist.py            # Original CLI script (legacy)
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── app.js        # Frontend JavaScript
└── downloads/            # Downloaded videos (created automatically)
```

## Performance Optimizations ⚡

- **RequestAnimationFrame** for smooth UI updates
- **Debouncing & Throttling** to reduce API calls
- **Caching** for downloads list and static assets
- **Service Worker** for offline support and faster loads
- **Optimized Socket.IO** with efficient transport
- **Lazy loading** and code splitting ready
- **CSS optimizations** with will-change hints

## App Store Deployment 🏪

### PWA Configuration

The app is fully configured as a Progressive Web App (PWA):

1. **Icons Setup**:
   - Create a 512x512 PNG icon
   - Save as `static/icons/icon-base.png`
   - Run `python create_icons.py` to generate all sizes
   - Or use online tools (see `static/icons/README.md`)

2. **iOS App Store**:
   - Use tools like [PWABuilder](https://www.pwabuilder.com/) to convert PWA to iOS app
   - Or use [Capacitor](https://capacitorjs.com/) for native iOS wrapper
   - The app includes all required meta tags for iOS

3. **Android Play Store**:
   - Use [PWABuilder](https://www.pwabuilder.com/) or [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap)
   - Or use [Capacitor](https://capacitorjs.com/) for native Android wrapper
   - All PWA features are configured

4. **Windows Store**:
   - Use [PWABuilder](https://www.pwabuilder.com/) for Windows app package
   - Or use [Electron](https://www.electronjs.org/) wrapper

### Testing PWA

1. Open the app in Chrome/Edge
2. Click the install button in the address bar
3. Or go to Settings > Install App
4. The app will appear as a standalone app

## Deployment 🚀

### Local Development

Simply run:
```bash
python app.py
```

### Production Deployment

For production, you may want to use a production WSGI server:

#### Using Gunicorn

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -k eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

#### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t playlist-downloader .
docker run -p 5000:5000 playlist-downloader
```

### Environment Variables

You can customize the application by setting environment variables:

- `PORT` - Port to run the server on (default: 5000)
- `HOST` - Host to bind to (default: 0.0.0.0)

## Troubleshooting 🔧

### Port Already in Use

If port 5000 is already in use, you can change it in `app.py`:

```python
socketio.run(app, debug=True, host='0.0.0.0', port=8080)  # Change 5000 to 8080
```

### FFmpeg Not Installed

The application works without FFmpeg, but for maximum quality, install FFmpeg:

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### Download Errors

If you encounter download errors:

1. Check your internet connection
2. Verify the playlist URL is correct
3. Ensure the playlist is public or you have access
4. Check that yt-dlp is up to date: `pip install --upgrade yt-dlp`

## Technologies Used 🛠️

- **Backend**: Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time Communication**: Socket.IO
- **Video Download**: yt-dlp
- **Icons**: Font Awesome

## License 📄

This project is open source and available for personal use.

## Contributing 🤝

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Support 💬

If you encounter any issues or have questions, please open an issue on the repository.

---

**Enjoy downloading your favorite playlists! 🎉**
