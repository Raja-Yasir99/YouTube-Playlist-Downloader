# Troubleshooting Guide 🔧

## App Not Starting

### Issue: Import Errors
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port Already in Use
**Solution:**
Change the port in `app.py` or set environment variable:
```bash
set PORT=8080
python app.py
```

### Issue: eventlet Not Found
**Solution:**
The app will automatically use threading mode. For better performance:
```bash
pip install eventlet
```

## App Not Working in Browser

### Issue: Blank Page
**Check:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify Flask is running: `http://localhost:5000`
4. Check terminal for Python errors

### Issue: Socket.IO Not Connecting
**Solution:**
1. Check browser console for WebSocket errors
2. Verify firewall isn't blocking port 5000
3. Try refreshing the page
4. Check if eventlet/threading is working

### Issue: Downloads Not Starting
**Check:**
1. Verify YouTube URL is correct
2. Check browser console for API errors
3. Verify yt-dlp is installed: `pip install yt-dlp`
4. Check terminal for download errors

### Issue: Service Worker Errors
**Solution:**
Service worker is optional. Errors are non-critical and won't affect functionality.

## Common Errors

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install Flask flask-socketio python-socketio
```

### "Connection refused" or "Can't connect"
- Make sure Flask app is running
- Check if port 5000 is available
- Try a different port

### "Download failed" or "Error downloading"
- Check internet connection
- Verify playlist URL is valid
- Ensure playlist is public
- Update yt-dlp: `pip install --upgrade yt-dlp`

## Performance Issues

### App is Slow
1. Clear browser cache
2. Check internet speed
3. Close other browser tabs
4. Restart the Flask app

### Downloads are Slow
- This is normal for large playlists
- Check your internet speed
- YouTube may throttle downloads

## Still Having Issues?

1. Check the terminal output for errors
2. Open browser console (F12) and check for errors
3. Verify all dependencies are installed
4. Try restarting the app
5. Clear browser cache and cookies





