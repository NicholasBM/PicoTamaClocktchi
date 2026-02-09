# Web Mode Troubleshooting

## Error: "Web Mode Error"

This usually means one of these issues:

### 1. Missing File (Most Common)
**Problem:** `web_interface.py` is not uploaded to your Pico

**Solution:**
1. Open Thonny or your file manager
2. Upload `web_interface.py` to the root of your Pico
3. Verify it's there (should see it in the file list)
4. Try web mode again

**How to verify:**
```python
# In REPL:
import os
print(os.listdir())
# Should see 'web_interface.py' in the list
```

### 2. Memory Issue
**Problem:** Not enough RAM to load the web server

**Solution:**
1. Restart your Pico (fresh memory)
2. Try web mode immediately after boot
3. If still fails, try this in REPL:
```python
import gc
gc.collect()
print(f"Free memory: {gc.mem_free()} bytes")
# Should have at least 50,000 bytes free
```

### 3. Port Already in Use
**Problem:** Port 8082 is already bound

**Solution:**
1. Restart your Pico
2. Make sure you're not running web mode twice

### 4. Import Error
**Problem:** Syntax error in web_interface.py

**Solution:**
1. Re-download `web_interface.py` from the files I created
2. Upload it again (might have been corrupted)
3. Check for any error messages in the console

## Quick Diagnostic Steps

### Step 1: Check File Exists
```python
import os
'web_interface.py' in os.listdir()
# Should return True
```

### Step 2: Try Manual Import
```python
from web_interface import WebInterface
# If this fails, you'll see the actual error
```

### Step 3: Check Memory
```python
import gc
gc.collect()
print(f"Free: {gc.mem_free()}")
# Need at least 50KB free
```

### Step 4: Check Console Output
Look at the console/REPL for detailed error messages. The code now prints:
- Full exception traceback
- Specific error message
- Import errors vs runtime errors

## Common Error Messages

### "Missing File! Upload: web_interface.py"
- **Cause:** File not on Pico
- **Fix:** Upload `web_interface.py`

### "Web Server Failed to start"
- **Cause:** Port binding failed
- **Fix:** Restart Pico, try again

### "WiFi Failed!"
- **Cause:** Can't connect to WiFi
- **Fix:** Check `wifi_config.py` credentials

### "MemoryError"
- **Cause:** Not enough RAM
- **Fix:** Restart Pico, run `gc.collect()`

## Testing Web Interface Manually

Try this in REPL to see the exact error:

```python
# 1. Import the module
from web_interface import WebInterface

# 2. Get references to oled and gamestate
# (These should already exist if game is running)
print(f"OLED: {oled}")
print(f"GameState: {gamestate}")

# 3. Create instance
web = WebInterface(oled, gamestate)

# 4. Try to start server
result = web.start(port=8082)
print(f"Started: {result}")

# If you get here, it worked!
# Check the IP:
import network
wlan = network.WLAN(network.STA_IF)
print(f"IP: {wlan.ifconfig()[0]}")
```

## Files Checklist

Make sure these files are on your Pico:
- ✅ `enhanced_picotamachibi.py` (updated version)
- ✅ `web_interface.py` (NEW - must upload!)
- ✅ `wifi_config.py` (with correct WiFi credentials)
- ✅ `main.py`
- ✅ `settings.py`
- ✅ All other existing files

## Still Not Working?

1. **Check the console output** - It will show the actual error
2. **Try the manual test above** - This will pinpoint the issue
3. **Restart fresh** - Power cycle the Pico
4. **Check memory** - Make sure you have enough free RAM
5. **Re-upload web_interface.py** - File might be corrupted

## What Should Happen When It Works

1. Press Call icon → Network Menu
2. Select "Web Remote"
3. WiFi connects (shows IP)
4. Screen shows:
   ```
   WEB MODE ACTIVE
   ----------------
   Open browser to:
   http://192.168.1.100:8082
   Press X to stop
   ```
5. Open that URL in browser
6. See the web interface!

## Getting More Info

To see detailed error messages, connect to the Pico via USB and watch the console output when you try to start web mode. The error will be printed there with full details.
