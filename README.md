# PicoTamaClocktchi 🦊

A virtual pet Tamagotchi-style game for Raspberry Pi Pico W with OLED display. Take care of your digital pet fox or grayhound with feeding, playing, and cleaning!

## Features

### Core Gameplay
- **Virtual Pet Care** - Feed, play with, and clean up after your pet
- **Multiple Pet Types** - Choose between Fox and Grayhound
- **Health System** - Monitor health, happiness, and sleepiness stats
- **Day/Night Cycle** - Pet sleeps and wakes up naturally
- **Hide & Seek Game** - Play interactive games with your pet
- **Animations** - Walking, eating, sleeping, playing with butterflies, and more
- **Random Events** - Birds, bunnies, squirrels, and weather effects

### Settings & Customization
- **Pet Naming** - Give your pet a custom name
- **Starting Age** - Set your pet's initial age (0-999 days)
- **God Mode** - Prevent pet death for holidays or extended absences
- **RTC Time Setting** - Configure real-time clock for accurate aging

### Web Remote Control 🌐
Control your pet from any device on your network!

- **Browser Interface** - Access from phone, tablet, or computer
- **Remote Actions** - Feed, sleep/wake, and clean from anywhere
- **Live Stats** - View health, happiness, sleepiness, and age in real-time
- **Activity Monitor** - See what your pet is currently doing
- **Auto-refresh** - Updates every 2 seconds automatically

To use Web Mode:
1. Press A+X buttons together for 5 seconds to open network menu
2. Select "Web Remote" option
3. Connect to WiFi (if not already connected)
4. Open browser to the displayed IP address on port 8082
5. Control your pet remotely!

## Hardware Requirements

- Raspberry Pi Pico W (or Pico 2 W)
- SSD1306 OLED Display (128x64, I2C)
- 3 Push Buttons (A, B, X)
- Breadboard and jumper wires

### Wiring
- **I2C Display**: SDA to GPIO0, SCL to GPIO1
- **Buttons**: Connect to appropriate GPIO pins with pull-down resistors

## Installation

1. Flash MicroPython to your Pico W
2. Copy all files to the Pico:
   - `enhanced_picotamachibi.py` - Main game file
   - `settings.py` - Settings menu
   - `web_mode.py` - Web remote control module
   - `web_interface_simple.py` - Web server
   - `wifi_config.py` - WiFi configuration
   - `fixed_icon.py` - Animation engine
   - `gui/` folder - All bitmap graphics
3. Configure WiFi credentials in `wifi_config.py`
4. Run `enhanced_picotamachibi.py` or set as `main.py`

## First Time Setup

On first boot, you'll be guided through:
1. Setting the current time
2. Naming your pet
3. Choosing pet type (Fox or Grayhound)
4. Setting starting age (optional)
5. Enabling god mode (optional)

## Controls

### Button Layout
- **A Button** - Cycle through menu icons
- **B Button** - Select/confirm action
- **X Button** - Cancel/back

### Menu Icons
- 🍖 **Food** - Feed your pet
- 💡 **Light** - Put pet to sleep or wake up
- 🎮 **Game** - Play hide & seek
- ⏰ **Clock** - Open settings menu
- 🚽 **Toilet** - Clean up poop
- ❤️ **Heart** - Check stats and show affection
- 📞 **Call** - Respond to alerts

### Special Combinations
- **A+X (hold 5 sec)** - Open network menu for web remote

## God Mode

God mode prevents your pet from dying, perfect for:
- Going on vacation
- Extended periods away from the device
- Testing features without worry
- Keeping your pet safe during holidays

When enabled:
- Pet cannot die from low stats
- Stats won't drop below 1
- All other gameplay remains normal

Enable in Settings menu (Clock icon) or during initial setup.

## Web Remote Features

The web interface provides:
- **Feed Button** - Give your pet food remotely
- **Sleep/Wake Toggle** - Control sleep state (button changes based on state)
- **Clean Button** - Clean up poop (shows "Already clean!" if not needed)
- **Live Stats Display** - Health, Happiness, Sleepiness, Age
- **Activity Bar** - Shows current animation/state
- **Alert Display** - See warnings and messages
- **Auto-update** - Refreshes every 2 seconds

Access at: `http://[PICO_IP]:8082`

## Performance

- **Debug Mode** - Set `DEBUG_MODE = False` in main file to disable console logging
- **Memory Efficient** - Web mode uses lazy loading to save boot memory
- **Optimized** - Runs smoothly on Pico W with ~450KB free memory

## Pet Stats

- **Health** (0-10) - Affected by cleanliness and feeding
- **Happiness** (0-10) - Increased by playing and care
- **Sleepiness** (0-10) - Decreases over time, restored by sleep

Keep all stats above 3 to avoid alerts. If two stats reach 0, your pet will die (unless god mode is enabled).

## Credits

Created for Raspberry Pi Pico W with love for virtual pets! 🐾

## License

Open source - feel free to modify and share!
