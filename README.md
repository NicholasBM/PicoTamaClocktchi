🐣 Enhanced PicoTamaCloktchi Setup Guide
This is an advanced Tamagotchi-style project based on [Kevin McAleer’s PicoTamachibi](https://github.com/kevinmcaleer/picotamachibi), expanded with additional features and animations. It runs on the Raspberry Pi Pico 2 or Pico 2 W, using MicroPython.

🧰 What You’ll Need
A Raspberry Pi Pico 2 or 2 W (with header pins is ideal).

Thonny IDE installed on your PC or Mac.

A USB cable to connect the Pico.

Either:

A breadboard and jumper wires for manual setup, or

[Kevin’s custom PCB](https://themakernotes.com/products/picotamachibi-pcb?srsltid=AfmBOop6EiiqPC5S398azA3Lg6otOlD-RYbR-lJekOnkOX_rMfZDtfr_) for easier assembly.

Kevin’s wiring guide is available [here](https://www.kevsrobots.com/blog/picotamachibi2.html). He has released two versions, so make sure you follow the guide that matches your build.

🔌 Setting Up MicroPython
Hold the BOOTSEL button on your Pico and connect it to your computer via USB.

The Pico will appear as a USB drive.

Download the MicroPython UF2 file from the [official Raspberry Pi site](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).

Drag and drop the UF2 file onto the Pico’s drive.

Unplug and replug the Pico. Open Thonny IDE.

In Thonny, go to Tools > Options > Interpreter and select the correct port and "MicroPython (Raspberry Pi Pico)".

📂 Uploading the Project Files
Download all the files from this repository (including test scripts and animation assets).

Open Thonny and connect to your Pico.

Shift + select all the files in the Thonny file browser, right-click, and choose Upload to /.

Locate enhanced_puicomachibi.py, right-click it, and choose Run.

You should now see your enhanced PicoTamaCloktchi running!

🧪 Extras Included
LCD test scripts

Legacy animation assets (useful for customizing or expanding behavior)


# PicoTamachibi Enhancements

This document outlines the enhancements made to the original PicoTamachibi code, transforming it into a more feature-rich and engaging virtual pet experience.

## Core System Improvements

### File Structure and Organization
- Added a dedicated bitmap path system (`BITMAP_PATH = "gui/bitmaps/"`) for better file organization
- Improved file loading with proper path handling for all resources
- Added more detailed console logging throughout the code

### Performance and Stability
- Added safety checks to prevent animations from getting stuck in infinite loops
- Implemented more aggressive screen clearing to prevent visual artifacts
- Added proper state management for all animations and game states
- Improved error handling throughout the code

### User Interface
- Added a clock and age display that shows when toolbar is hidden
- Implemented automatic toolbar hiding after 6 seconds of inactivity
- Added visual background elements (mountains and grass)
- Improved positioning of elements on screen for better visual appeal
- Added animated call icon for alerts

## Pet Mechanics

### Enhanced Stats System
- Implemented stat capping to prevent values exceeding maximum (10)
- Added more nuanced health and happiness decreases based on conditions
- Created critical thresholds for alerts (3) and death (1)
- Added hunger system that affects health and happiness
- Implemented more realistic poop timing (20 minutes to 2 hours)

### Time-Based Features
- Added real-time clock integration using RTC
- Implemented pet age tracking in days (with half-day precision)
- Added time-of-day messages (morning, afternoon, evening, night)
- Created time-based random events and reflections

### Sleep System
- Enhanced sleep mechanics with proper animation transitions
- Added sleep cycle tracking (12-hour maximum sleep duration)
- Implemented quick naps (2-minute duration) that occur randomly
- Added sleep time tracking to limit total sleep per cycle

### Feeding System
- Improved feeding mechanics with position-aware animations
- Added hunger tracking and alerts when pet hasn't been fed
- Implemented last feed time tracking
- Added more realistic energy increases from feeding

## Animation and Visual Enhancements

### Position System
- Added three distinct positions for the fox (left, center, right)
- Implemented position-specific animations for all actions
- Created smooth walking animations between positions
- Added proper animation frame cycling for walking

### New Animations
- Added butterfly animation that appears randomly
- Implemented bunny animation that appears when fox is on left
- Created hide and seek animations with ears peeking out
- Added love heart animation after games
- Implemented walking animations with proper directional frames

### Animation Quality
- Improved animation speeds for better visual appeal
- Added animation loops with proper completion detection
- Implemented animation state tracking to prevent conflicts
- Added animation transitions between states

## Interactive Features

### Hide and Seek Game
- Added interactive hide and seek game with scoring system
- Implemented random ear positions for gameplay
- Added game messages and score display
- Created game completion rewards based on outcome

### Auto Hide and Seek
- Implemented automatic hide and seek sequences that play randomly
- Added messages during auto hide and seek ("Can you see me?", "I'm hiding...", "Peekaboo!")
- Created proper animation sequences with transitions

### Personality Features
- Added random event messages that appear periodically
- Implemented pet reflections based on current stats
- Created a system to store and recall the last random message
- Added call button functionality to display alerts or last random message

### Alert System
- Implemented visual and text alerts for critical conditions
- Added specific alert reasons based on pet state
- Created alert indicators with animated call icon
- Implemented alert resolution through call button

## Technical Advancements

### State Management
- Expanded game state tracking with many new state variables
- Added proper state transitions between animations and activities
- Implemented state-based conditional behaviors
- Created state tracking for long-term pet care metrics

### Button Handling
- Improved button responsiveness and feedback
- Added context-sensitive button actions based on current state
- Implemented multi-press detection for game cancellation
- Created button-triggered position changes

### Animation Engine
- Enhanced animation loading and unloading
- Added support for position-specific animations
- Implemented animation speed controls
- Created animation completion detection and callbacks

## New Features

### Walking System
- Added fox walking animations in both directions
- Implemented smooth position transitions
- Created frame-based animation cycling
- Added walking triggers from various actions

### Random Events
- Implemented random butterfly appearances
- Added random bunny animations when fox is on left
- Created random quick naps during the day
- Implemented random auto hide and seek sequences

### Environmental Elements
- Added mountain background below time bar
- Implemented grass layer at bottom of screen
- Created layered drawing system for visual depth
- Added proper z-ordering of visual elements





### Environmental Elements
- Added mountain background below time bar
- Implemented grass layer at bottom of screen
- Created layered drawing system for visual depth
- Added proper z-ordering of visual elements
