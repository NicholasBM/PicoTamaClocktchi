# Quick Start - Web Interface

## 🚀 5-Minute Setup

### Step 1: Upload Files
Upload these files to your Pico:
- ✅ `web_interface.py` (NEW)
- ✅ `enhanced_picotamachibi.py` (UPDATED)

### Step 2: Start Web Mode
1. Press **Call icon** (📞) on your pet
2. Navigate to **"Web Remote"**
3. Press **B** to select
4. Wait for connection...

### Step 3: Get IP Address
Screen will show:
```
WEB MODE ACTIVE
----------------
Open browser to:
http://192.168.1.100:8082
Press X to stop
```

### Step 4: Open Browser
On your phone/computer:
1. Open any browser
2. Type the address from Step 3
3. Bookmark it for easy access!

### Step 5: Control Your Pet
- Click **A**, **B**, **X** buttons
- Watch stats update live
- See the display in real-time

## 📱 What You'll See

```
┌─────────────────────────────┐
│  🐾 PicoTamachibi Remote 🐾 │
│                             │
│  [Live OLED Display Here]   │
│                             │
│  Health: 8/10               │
│  Happiness: 9/10            │
│  Sleepiness: 7/10           │
│  Age: 2.5d                  │
│                             │
│  [A]  [B]  [X]              │
│                             │
│  Status: Connected          │
└─────────────────────────────┘
```

## 🎮 Button Functions

| Button | Function |
|--------|----------|
| **A** | Left / Navigate |
| **B** | Select / Action |
| **X** | Right / Cancel |

Same as physical buttons!

## 🛑 Stop Web Mode

Press **X button** on the physical Pico

## ⚠️ Troubleshooting

**Can't connect?**
- Check you're on same WiFi
- Try typing full address with `:8082`
- Restart web mode

**Display not updating?**
- Refresh browser page
- Check "Status" shows "Connected"

**Buttons not working?**
- Make sure web mode still active
- Try clicking again

## 💡 Pro Tips

1. **Bookmark the page** - Quick access next time
2. **Works on phones** - Control from anywhere in house
3. **Multiple devices** - Open on phone AND computer
4. **Leave it running** - Check on pet anytime
5. **Battery saver** - Turn off Pico screen, use web instead

## 📊 What Gets Updated

Every second:
- ✅ Display image
- ✅ Health stat
- ✅ Happiness stat
- ✅ Sleepiness stat
- ✅ Age
- ✅ Connection status

## 🔒 Security

✅ Safe on home WiFi
❌ Don't expose to internet
✅ Local network only

## 🎯 Use Cases

- **Monitor from couch** - Check pet without getting up
- **Kids can help** - Let them feed from their tablet
- **Remote care** - Control from another room
- **Screenshots** - Take photos of the display
- **Show friends** - Demo your pet on big screen

## 📞 Need Help?

1. Read `WEB_INTERFACE_GUIDE.md`
2. Run `test_web_interface.py` on computer
3. Check Pico console for errors

---

**That's it! Enjoy your web-enabled PicoTamachibi! 🐾**
