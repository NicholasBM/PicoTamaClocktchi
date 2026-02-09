# PicoTamachibi Web Interface Guide

## What It Does
The web interface lets you view and control your PicoTamachibi pet from any device with a web browser on your local network (phone, tablet, computer).

## Features
- **Live Display**: See the OLED screen in real-time in your browser
- **Stats Dashboard**: View health, happiness, sleepiness, and age
- **Remote Control**: Press A, B, X buttons from your browser
- **Auto-Refresh**: Updates every second automatically

## How to Use

### 1. Start Web Mode
1. Press the **Call** icon (📞) in the toolbar to open Network Menu
2. Use **A button** to navigate to "Web Remote"
3. Press **B button** to select
4. Wait for WiFi to connect (uses your existing WiFi config)
5. The screen will show the IP address, like: `http://192.168.1.100:8082`

### 2. Open in Browser
1. On any device connected to the same WiFi network
2. Open a web browser (Chrome, Safari, Firefox, etc.)
3. Type the address shown on the Pico screen
4. Example: `http://192.168.1.100:8082`

### 3. Control Your Pet
- Click the **A**, **B**, **X** buttons on the web page
- They work exactly like the physical buttons
- The display updates every second
- Stats update in real-time

### 4. Stop Web Mode
- Press the **X button** on the physical Pico
- Or just close the browser and restart the Pico

## Technical Details

### Ports Used
- **8080**: Pet visit communication (existing)
- **8081**: Pet discovery (existing)
- **8082**: Web interface (NEW)

### Network Requirements
- Pico and browser device must be on same WiFi network
- No internet connection required (local only)
- Works with your existing `wifi_config.py` settings

### Performance
- Web server runs alongside the game
- Non-blocking design - won't slow down animations
- Handles one browser connection at a time
- Updates display buffer every second

### Browser Compatibility
- ✅ Chrome/Edge (recommended)
- ✅ Safari (iOS/macOS)
- ✅ Firefox
- ✅ Mobile browsers

## Troubleshooting

### Can't Connect to Web Interface
1. Check Pico is showing "WEB MODE ACTIVE"
2. Verify you're on the same WiFi network
3. Try typing the full IP address with port: `http://192.168.1.100:8082`
4. Check your router isn't blocking local connections

### Display Not Updating
1. Refresh the browser page
2. Check the "Status" indicator shows "Connected"
3. Try a different browser

### Buttons Not Working
1. Make sure web mode is still active on Pico
2. Check browser console for errors (F12)
3. Try clicking the button again

### Pico Freezes
1. Press X button to exit web mode
2. Restart the Pico if needed
3. Web mode uses more memory - this is normal

## Files Added
- `web_interface.py` - Web server module
- `WEB_INTERFACE_GUIDE.md` - This guide

## Files Modified
- `enhanced_picotamachibi.py` - Added web mode integration

## Security Note
⚠️ The web interface is designed for LOCAL network use only. Do not expose it to the internet without proper security measures (authentication, HTTPS, etc.).

## Future Enhancements (Ideas)
- [ ] Multiple simultaneous connections
- [ ] Pet history graphs
- [ ] Screenshot/save display
- [ ] Custom button macros
- [ ] Dark/light theme toggle
- [ ] Mobile-optimized layout
- [ ] WebSocket for faster updates

## Credits
Built on top of the existing PicoTamachibi networking system by reusing WiFi connection and socket handling code.
