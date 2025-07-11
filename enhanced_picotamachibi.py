# from icons import food_icon
from machine import I2C, Pin, RTC
from gui.ssd1306 import *
from fixed_icon import Animate, Icon, Toolbar, Button, Event, GameState
from time import sleep, time
import framebuf
from random import randint

print("Starting Enhanced PicoTamachibi with advanced features...")

# Define pins
sda = Pin(0)
scl = Pin(1)
id = 0

# Initialize I2C
print("Initializing I2C...")
i2c = I2C(id=id, sda=sda, scl=scl)
print(f"I2C scan results: {i2c.scan()}")

# Initialize OLED display
print("Initializing OLED display...")
oled = SSD1306_I2C(width=128, height=64, i2c=i2c)
oled.init_display()
print(f"oled: {oled}")

# Define bitmap path
BITMAP_PATH = "gui/bitmaps/"

# Load settings if they exist
print("Loading settings...")
pet_settings = None
pet_type = 'Fox'  # Always default to Fox first

try:
    with open('pet_settings.txt', 'r') as f:
        pet_settings = {}
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                pet_settings[key] = value
    
    # Only change pet type if explicitly set in settings
    if pet_settings and 'type' in pet_settings:
        pet_type = pet_settings['type']
        print(f"Settings loaded: {pet_settings} - Using {pet_type} pet type")
    else:
        pet_type = 'Fox'
        print(f"Settings loaded: {pet_settings} - Using default Fox pet type")
except:
    print("No settings file found or error loading settings - Using default Fox pet type")
    pet_settings = {'type': 'Fox'}  # Default to Fox if no settings

print(f"Pet type: {pet_type}")

# load icons with corrected paths
print("Loading icons...")
food = Icon(BITMAP_PATH + 'food.pbm', width=16, height=16, name="food")
lightbulb = Icon(BITMAP_PATH + 'lightbulb.pbm', width=16, height=16, name="lightbulb")
game = Icon(BITMAP_PATH + 'game.pbm', width=16, height=16, name="game")
clock = Icon(BITMAP_PATH + 'clock.pbm', width=16, height=16, name="clock")  # Replaced firstaid with clock
toilet = Icon(BITMAP_PATH + 'toilet.pbm', width=16, height=16, name="toilet")
heart = Icon(BITMAP_PATH + 'heart.pbm', width=16, height=16, name="heart")
call = Icon(BITMAP_PATH + 'call.pbm', width=16, height=16, name="call")
bubble = Icon(BITMAP_PATH + 'bubble.pbm', width=16, height=16, name="bubble")  # Added bubble icon for reflections
# Load background and ground layers
mountain = Icon(BITMAP_PATH + 'mountain.pbm', width=128, height=10, name="mountain")  # Background mountain
trees = Icon(BITMAP_PATH + 'trees.pbm', width=128, height=10, name="trees")  # Background trees for area 1
tree2 = Icon(BITMAP_PATH + 'tree2.pbm', width=10, height=50, name="tree2")  # Tree for new area
grass = Icon(BITMAP_PATH + 'grass1.pbm', width=32, height=8, name="grass")  # Ground layer

# Squirrel animation (running up the tree)
squirrel_animation = Animate(x=128 - 10 - 20, y=6, width=10, height=50, 
                            animation_type="default", filename=BITMAP_PATH + 'tree')
squirrel_animation.speed = 'slow'  # Set animation speed to slow
squirrel_animation.set = False  # Initially hidden

# Set Animations with corrected paths
print("Setting up animations...")
poopy = Animate(x=96, y=40, width=16, height=16, filename=BITMAP_PATH + 'poop')  # Moved up from y=48 to y=40

# Create Fox animations for different positions
fox_baby_left = Animate(x=0, y=9, width=48, height=48, animation_type="bouncing", filename=BITMAP_PATH + 'baby_bounce')
fox_baby_center = Animate(x=48, y=9, width=48, height=48, animation_type="bouncing", filename=BITMAP_PATH + 'baby_bounce')
fox_baby_right = Animate(x=80, y=9, width=48, height=48, animation_type="bouncing", filename=BITMAP_PATH + 'baby_bounce')

# Create Grayhound animations for different positions
grayhound_baby_left = Animate(x=0, y=9, width=48, height=48, animation_type="bouncing", filename=BITMAP_PATH + 'Grayhound/grayhoundbounce')
grayhound_baby_center = Animate(x=48, y=9, width=48, height=48, animation_type="bouncing", filename=BITMAP_PATH + 'Grayhound/grayhoundbounce')
grayhound_baby_right = Animate(x=80, y=9, width=48, height=48, animation_type="bouncing", filename=BITMAP_PATH + 'Grayhound/grayhoundbounce')

# Set the default baby animations based on pet type
print(f"Setting up baby animations for pet type: {pet_type}")
if pet_type == "Fox":
    baby_left = fox_baby_left
    baby_center = fox_baby_center
    baby_right = fox_baby_right
    print("Using Fox animations")
else:  # Grayhound
    baby_left = grayhound_baby_left
    baby_center = grayhound_baby_center
    baby_right = grayhound_baby_right
    print("Using Grayhound animations")

# Set the default baby to center position
baby = baby_center
print(f"Default baby set to center position: {baby}")

# Create Fox eat animations for different positions
fox_eat_left = Animate(x=0, y=9, width=48, height=48, filename=BITMAP_PATH + 'eat')
fox_eat_center = Animate(x=48, y=9, width=48, height=48, filename=BITMAP_PATH + 'eat')
fox_eat_right = Animate(x=80, y=9, width=48, height=48, filename=BITMAP_PATH + 'eat')

# Create Grayhound eat animations for different positions
grayhound_eat_left = Animate(x=0, y=9, width=48, height=48, filename=BITMAP_PATH + 'Grayhound/grayhoundeat')
grayhound_eat_center = Animate(x=48, y=9, width=48, height=48, filename=BITMAP_PATH + 'Grayhound/grayhoundeat')
grayhound_eat_right = Animate(x=80, y=9, width=48, height=48, filename=BITMAP_PATH + 'Grayhound/grayhoundeat')

# Set eat animations based on pet type
if pet_type == "Fox":
    eat_left = fox_eat_left
    eat_center = fox_eat_center
    eat_right = fox_eat_right
else:  # Grayhound
    eat_left = grayhound_eat_left
    eat_center = grayhound_eat_center
    eat_right = grayhound_eat_right

# Default eat animation (will be set based on position)
eat = eat_center

# Create Fox sleep animations for different positions (moved down by 3px)
fox_babyzzz_left = Animate(x=0, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'baby_zzz')
fox_babyzzz_center = Animate(x=48, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'baby_zzz')
fox_babyzzz_right = Animate(x=80, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'baby_zzz')

# Create Grayhound sleep animations for different positions - using correct filenames without grayhound prefix
# Note: The actual files are named sleeping1.pbm, sleeping2.pbm, etc.
grayhound_babyzzz_left = Animate(x=0, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'Grayhound/sleeping')
grayhound_babyzzz_center = Animate(x=48, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'Grayhound/sleeping')
grayhound_babyzzz_right = Animate(x=80, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'Grayhound/sleeping')

# Set sleep animations based on pet type
if pet_type == "Fox":
    babyzzz_left = fox_babyzzz_left
    babyzzz_center = fox_babyzzz_center
    babyzzz_right = fox_babyzzz_right
else:  # Grayhound
    babyzzz_left = grayhound_babyzzz_left
    babyzzz_center = grayhound_babyzzz_center
    babyzzz_right = grayhound_babyzzz_right

# Default sleep animation (will be set based on position)
babyzzz = babyzzz_center

death = Animate(x=48, y=8, animation_type='bounce', filename=BITMAP_PATH + "skull")  # Moved up from y=16 to y=8

# Create Fox potty animations for different positions
fox_potty_left = Animate(filename=BITMAP_PATH + "potty", animation_type='bounce', x=0, y=9, width=48, height=48)
fox_potty_center = Animate(filename=BITMAP_PATH + "potty", animation_type='bounce', x=48, y=9, width=48, height=48)
fox_potty_right = Animate(filename=BITMAP_PATH + "potty", animation_type='bounce', x=80, y=9, width=48, height=48)

# Create Grayhound potty animations for different positions
grayhound_potty_left = Animate(filename=BITMAP_PATH + "Grayhound/grayhoundpotty", animation_type='bounce', x=0, y=9, width=48, height=48)
grayhound_potty_center = Animate(filename=BITMAP_PATH + "Grayhound/grayhoundpotty", animation_type='bounce', x=48, y=9, width=48, height=48)
grayhound_potty_right = Animate(filename=BITMAP_PATH + "Grayhound/grayhoundpotty", animation_type='bounce', x=80, y=9, width=48, height=48)

# Set potty animations based on pet type
if pet_type == "Fox":
    go_potty_left = fox_potty_left
    go_potty_center = fox_potty_center
    go_potty_right = fox_potty_right
else:  # Grayhound
    go_potty_left = grayhound_potty_left
    go_potty_center = grayhound_potty_center
    go_potty_right = grayhound_potty_right

# Default potty animation (will be set based on position)
go_potty = go_potty_center
# New animation for call alert - using existing call_animate files
call_animate = Animate(filename=BITMAP_PATH + 'call_animate', width=16, height=16, x=108, y=0)
call_animate.speed = 'very slow'
call_animate.set = False

# Ears animation for hide and seek game
# Start with middle position (will be updated based on game)
# Using full 48x48 image size and positioning so ears peek above grass
ears_left = Animate(filename=BITMAP_PATH + 'ears', width=48, height=48, x=0, y=8)
ears_middle = Animate(filename=BITMAP_PATH + 'ears', width=48, height=48, x=40, y=8)
ears_right = Animate(filename=BITMAP_PATH + 'ears', width=48, height=48, x=80, y=8)

# Love heart animation for after game
love = Animate(filename=BITMAP_PATH + 'love', width=48, height=48, x=40, y=8)
love.set = False

# Fox butterfly animations for different positions
fox_butterfly_left = Animate(filename=BITMAP_PATH + 'butterfyl', width=48, height=48, x=0, y=8)
fox_butterfly_center = Animate(filename=BITMAP_PATH + 'butterfyl', width=48, height=48, x=48, y=8)
fox_butterfly_right = Animate(filename=BITMAP_PATH + 'butterfyl', width=48, height=48, x=80, y=8)

# Grayhound butterfly animations for different positions
grayhound_butterfly_left = Animate(filename=BITMAP_PATH + 'Grayhound/grayhoundbutterfyl', width=48, height=48, x=0, y=8)
grayhound_butterfly_center = Animate(filename=BITMAP_PATH + 'Grayhound/grayhoundbutterfyl', width=48, height=48, x=48, y=8)
grayhound_butterfly_right = Animate(filename=BITMAP_PATH + 'Grayhound/grayhoundbutterfyl', width=48, height=48, x=80, y=8)

# Set butterfly animations based on pet type
if pet_type == "Fox":
    butterfly_left = fox_butterfly_left
    butterfly_center = fox_butterfly_center
    butterfly_right = fox_butterfly_right
else:  # Grayhound
    butterfly_left = grayhound_butterfly_left
    butterfly_center = grayhound_butterfly_center
    butterfly_right = grayhound_butterfly_right

# Set up butterfly animations to play twice
butterfly_left.speed = 'very slow'
butterfly_left.loop(no=2)  # Play twice
butterfly_left.set = False

butterfly_center.speed = 'very slow'
butterfly_center.loop(no=2)  # Play twice
butterfly_center.set = False

butterfly_right.speed = 'very slow'
butterfly_right.loop(no=2)  # Play twice
butterfly_right.set = False

# Default butterfly (will be set based on position)
butterfly = butterfly_center

# Bunny animation (only shows on right side when fox is on left)
bunny_animation = Animate(filename=BITMAP_PATH + 'bunny_', width=32, height=32, x=80, y=24)
bunny_animation.speed = 'slow'
bunny_animation.loop(no=2)  # Play twice
bunny_animation.set = False

# Bird animation frames
print("Loading bird animation frames...")
bird_frames = []
for i in range(1, 5):  # Load 4 frames
    bird_frame = Icon(BITMAP_PATH + f'bird_{i}.pbm', width=8, height=8, name=f"bird_{i}")
    bird_frames.append(bird_frame)

# Load individual fox walking frames
print("Loading fox walking animation frames...")
# Left-facing frames (original)
fox_walk1 = Icon(BITMAP_PATH + 'fox_walk1.pbm', width=48, height=48, name="fox_walk1")
fox_walk2 = Icon(BITMAP_PATH + 'fox_walk2.pbm', width=48, height=48, name="fox_walk2")
fox_walk3 = Icon(BITMAP_PATH + 'fox_walk3.pbm', width=48, height=48, name="fox_walk3")
fox_walk4 = Icon(BITMAP_PATH + 'fox_walk4.pbm', width=48, height=48, name="fox_walk4")

# Right-facing frames (new)
fox_walk1r = Icon(BITMAP_PATH + 'fox_walk1r.pbm', width=48, height=48, name="fox_walk1r")
fox_walk2r = Icon(BITMAP_PATH + 'fox_walk2r.pbm', width=48, height=48, name="fox_walk2r")
fox_walk3r = Icon(BITMAP_PATH + 'fox_walk3r.pbm', width=48, height=48, name="fox_walk3r")
fox_walk4r = Icon(BITMAP_PATH + 'fox_walk4r.pbm', width=48, height=48, name="fox_walk4r")

# Load individual grayhound walking frames
print("Loading grayhound walking animation frames...")
# Left-facing frames - positioned 4px higher (y=15 instead of y=19)
grayhound_walk1 = Icon(BITMAP_PATH + 'Grayhound/walking1left.pbm', width=48, height=48, y=15, name="grayhound_walk1")
grayhound_walk2 = Icon(BITMAP_PATH + 'Grayhound/walking2left.pbm', width=48, height=48, y=15, name="grayhound_walk2")
grayhound_walk3 = Icon(BITMAP_PATH + 'Grayhound/walking3left.pbm', width=48, height=48, y=15, name="grayhound_walk3")

# Right-facing frames - positioned 4px higher (y=15 instead of y=19)
grayhound_walk1r = Icon(BITMAP_PATH + 'Grayhound/walking1.pbm', width=48, height=48, y=15, name="grayhound_walk1r")
grayhound_walk2r = Icon(BITMAP_PATH + 'Grayhound/walking2.pbm', width=48, height=48, y=15, name="grayhound_walk2r")
grayhound_walk3r = Icon(BITMAP_PATH + 'Grayhound/walking3.pbm', width=48, height=48, y=15, name="grayhound_walk3r")

# Store frames in lists for easy access based on pet type
if pet_type == "Fox":
    # Fox has 4 frames
    frames_left = [fox_walk1, fox_walk2, fox_walk3, fox_walk4]
    frames_right = [fox_walk1r, fox_walk2r, fox_walk3r, fox_walk4r]
else:  # Grayhound
    # Grayhound has 3 frames, repeat the last one to match Fox's 4 frames
    frames_left = [grayhound_walk1, grayhound_walk2, grayhound_walk3, grayhound_walk3]
    frames_right = [grayhound_walk1r, grayhound_walk2r, grayhound_walk3r, grayhound_walk3r]

# Use the appropriate frames based on pet type
fox_frames_left = frames_left
fox_frames_right = frames_right

# Variables to track fox position and animation during walking
fox_x_position = 48  # Start at center
fox_frame_index = 0  # Current animation frame index
fox_movement_counter = 0  # Counter to control animation speed

# We'll create the left walking animation by inverting the right one when needed
# Set up ears animations
ears_left.loop(no=1)
ears_middle.loop(no=1)
ears_right.loop(no=1)
ears_left.speed = 'slow'
ears_middle.speed = 'slow'
ears_right.speed = 'slow'
ears_left.set = False
ears_middle.set = False
ears_right.set = False

# Random event messages
random_events = [
    "Found a bug!",
    "Danced a bit.",
    "Chased a leaf.",
    "Tail moved?",
    "Heard a noise!",
    "Buried stuff.",
    "Sniffed wind.",
    "Rolled in mud.",
    "Saw a squirrel.",
    "Did a spin!",
    "Saw a bunny!"
]

# Reflection messages based on pet state
reflections = {
    "health_low": ["Not feeling great...", "Need medicine?", "Bit sick..."],
    "health_good": ["Feeling strong!", "So healthy!", "Top shape!"],
    "happiness_low": ["Bit sad today.", "Miss playing...", "Need fun..."],
    "happiness_good": ["So happy!", "Life's good!", "Feeling joy!"],
    "sleepiness_low": ["So tired...", "Need nap...", "Eyes heavy..."],
    "sleepiness_good": ["Wide awake!", "Full energy!", "Not tired!"],
    "general": ["Just thinking.", "Nice day.", "Hmm..."]
}

# Time-of-day messages
time_messages = {
    "morning": ["Hi sun!", "Let's run!", "Morn' world!"],
    "afternoon": ["Snack time?", "Good day!", "Zoom soon?"],
    "evening": ["Sun's low.", "Wind's nice.", "Getting dark."],
    "night": ["Stars out.", "Let's rest.", "Den time."]
}

# Track last time a time-of-day message was shown
last_time_message = 0  # Store as hour (0-23)

# Set the game state
print("Setting up game state...")
gamestate = GameState()

# Append states to the states dictionary
gamestate.states["pet_type"] = pet_type  # Store the pet type in game state
gamestate.states["sleeping"] = False      # Baby is not sleeping
gamestate.states["feeding_time"] = False  # Baby is not eating
gamestate.states["cancel"] = False
gamestate.states["unwell"] = False
gamestate.states["health"] = 10
gamestate.states["happiness"] = 10
gamestate.states["sleepiness"] = 10
gamestate.states["tired"] = False
gamestate.states["alert"] = False         # New state for call alert
gamestate.states["pet_birth_time"] = time()  # Track when the pet was born
gamestate.states["show_toolbar"] = True   # Whether to show toolbar (True) or clock (False)
gamestate.states["toolbar_timer"] = 0     # Timer for toolbar visibility (in frames)
gamestate.states["alert_reason"] = ""     # Track the reason for the alert
# Hide and seek game states
gamestate.states["hide_seek_active"] = False  # Whether the hide and seek game is active
gamestate.states["player_score"] = 0      # Player's score in hide and seek
gamestate.states["fox_score"] = 0         # Fox's score in hide and seek
gamestate.states["ear_position"] = 1      # Current ear position (0=left, 1=middle, 2=right)
gamestate.states["cancel_count"] = 0      # Counter for cancel button presses during game
gamestate.states["ear_pause_timer"] = 0   # Timer for pausing ears animation

# New animation states
gamestate.states["fox_position"] = 1      # Fox position: 0=left, 1=center, 2=right
gamestate.states["butterfly_active"] = False  # Whether butterfly animation is active
gamestate.states["walking_active"] = False    # Whether walking animation is active
gamestate.states["walking_direction"] = 0     # 0=left, 1=right
gamestate.states["just_cleaned"] = False      # Flag for tracking cleaning for testing
gamestate.states["cleaning_timer"] = 0        # Timer for animations after cleaning
gamestate.states["bunny_active"] = False      # Whether bunny animation is active
gamestate.states["last_bunny_time"] = time()  # Track last time bunny appeared
gamestate.states["last_random_message"] = ""  # Track the last random event message
gamestate.states["display_inverted"] = False  # Track if display is inverted (for night mode)

# Area transition states
gamestate.states["current_area"] = 0      # 0 = original area, 1 = new area

# Rain effect states
gamestate.states["rain_active"] = False        # Whether rain effect is active
gamestate.states["rain_drops"] = []            # List of rain drops [x, y]
gamestate.states["rain_timer"] = 0             # Timer for rain duration (in frames)
gamestate.states["rain_intensity"] = 10        # Number of raindrops on screen at once (reduced from 15 to 10)
gamestate.states["last_rain_time"] = time()    # Track last time rain appeared
gamestate.states["rain_random_timer"] = 0      # Random timer for next rain activation

# Squirrel animation state variables
gamestate.states["squirrel_initial_timer"] = 0      # Timer for initial activation (5 seconds)
gamestate.states["squirrel_active"] = False         # Whether squirrel animation is currently playing
gamestate.states["squirrel_activated"] = False      # Whether squirrel has been activated initially
gamestate.states["squirrel_last_time"] = time()     # Track last time squirrel animation played
gamestate.states["squirrel_random_timer"] = 0       # Random timer for next activation

# Protected animation states
gamestate.states["eating_protected"] = False  # Whether eating animation is protected from interruptions
gamestate.states["potty_protected"] = False   # Whether potty animation is protected from interruptions
gamestate.states["eating_frame_counter"] = 0  # Safety counter for eating animation
gamestate.states["potty_frame_counter"] = 0   # Safety counter for potty animation

# Bird animation states
gamestate.states["birds_active"] = False      # Whether birds are currently flying
gamestate.states["last_birds_time"] = time()  # Track last time birds appeared
gamestate.states["bird_positions"] = []       # List of bird positions [x, y, direction]
gamestate.states["bird_frame"] = 0            # Current animation frame for birds
gamestate.states["bird_frame_counter"] = 0    # Counter for bird animation timing
gamestate.states["birds_message_shown"] = False  # Whether the "Birds!" message has been shown for current appearance

# Daily care tracking
gamestate.states["last_daily_care_check"] = time()  # Track when we last checked daily care
gamestate.states["fed_today"] = False      # Whether fox was fed today
gamestate.states["played_today"] = False   # Whether fox was played with today
gamestate.states["slept_today"] = False    # Whether fox slept today
gamestate.states["poop_start_time"] = time()  # Track when poop appeared
gamestate.states["death_cause"] = ""       # Track cause of death
gamestate.states["death_screen_shown"] = False  # Whether death screen has been shown
gamestate.states["death_animation_shown"] = False  # Whether skull animation has been shown
gamestate.states["death_timer"] = 0  # Timer for skull animation
gamestate.states["death_combo_timer"] = 0  # Timer for death testing button combination
gamestate.states["death_combo_warning_shown"] = False  # Whether warning has been shown

# Auto hide and seek game states
gamestate.states["auto_hide_seek_active"] = False  # Whether auto hide and seek is active
gamestate.states["auto_hide_seek_position"] = 0    # Current position in sequence (0=left, 1=center, 2=right)
gamestate.states["auto_hide_seek_timer"] = 0       # Timer for showing each position
gamestate.states["last_auto_hide_seek"] = time()   # Track last time auto hide and seek was played

# New stat tracking variables
gamestate.states["last_play_time"] = time()   # Track last time played with
gamestate.states["last_feed_time"] = time()   # Track last time fed
gamestate.states["total_sleep_time"] = 0      # Track total sleep time in current cycle
gamestate.states["last_wake_time"] = time()   # Track time since last waking
gamestate.states["last_quick_nap_time"] = time() # Track time since last quick nap
gamestate.states["is_hungry"] = False         # Track if fox is hungry
gamestate.states["hunger_alert_shown"] = False # Track if hunger alert was shown
gamestate.states["poop_alert_shown"] = False  # Track if poop alert was shown
gamestate.states["quick_nap_active"] = False  # Track if quick nap is active

# Animation refresh states
gamestate.states["last_animation_refresh"] = time()  # Track last time animations were refreshed
gamestate.states["animation_refresh_timer"] = 0      # Timer for animation refresh (in frames)

# Memory management states
gamestate.states["last_gc_time"] = time()           # Track last time garbage collection was run
gamestate.states["last_memory_check"] = time()      # Track last time memory was checked
gamestate.states["lowest_memory"] = 0               # Track lowest memory seen (will be set after first check)
gamestate.states["last_deep_refresh"] = time()      # Track last time deep refresh was performed
gamestate.states["last_blank_check"] = time()       # Track last time blank screen check was performed

# Game Variables
TIREDNESS = 7200 # seconds (2 hours)
POOP_MIN = 1200 # seconds (20 minutes)
POOP_MAX = 7200 # seconds (2 hours)
SLEEP_DURATION = 12 * 60 * 60 # 12 hours in seconds
HUNGER_CHECK_INTERVAL = 7200 # 1 hour in seconds
QUICK_NAP_DURATION = 120 # 2 minutes in seconds
ANIMATION_REFRESH_INTERVAL = 1800 # 30 minutes in seconds

# Memory management constants
GC_INTERVAL = 300  # Run garbage collection every 5 minutes (in seconds)
MEMORY_CHECK_INTERVAL = 600  # Check memory every 10 minutes (in seconds)
MEMORY_WARNING_THRESHOLD = 10000  # Bytes of free memory that trigger warning
DEEP_REFRESH_INTERVAL = 3600  # Deep refresh every 1 hour (in seconds) - reduced from 2 hours
BLANK_SCREEN_CHECK_INTERVAL = 120  # Check for blank screen every 2 minutes (in seconds) - reduced from 5 minutes
ANIMATION_REFRESH_INTERVAL = 900  # Regular refresh every 15 minutes (in seconds) - reduced from 30 minutes
GC_INTERVAL = 300  # Run garbage collection every 5 minutes (in seconds)
MEMORY_CHECK_INTERVAL = 600  # Check memory every 10 minutes (in seconds)
MEMORY_WARNING_THRESHOLD = 10000  # Bytes of free memory that trigger warning
DEEP_REFRESH_INTERVAL = 7200  # Deep refresh every 2 hours (in seconds)
BLANK_SCREEN_CHECK_INTERVAL = 300  # Check for blank screen every 5 minutes (in seconds)

# Thresholds for alerts
CRITICAL_THRESHOLD = 3  # When stats are below this, trigger alert
DEATH_THRESHOLD = 1     # When all stats are at or below this, trigger death

# Helper function to cap stats at maximum value
def cap_stat(value, max_value=10):
    """Cap a stat value at the specified maximum"""
    return min(value, max_value)


def tired():
    gamestate.states["sleepiness"] -= 0.14
    if gamestate.states["sleepiness"] < 0:
        gamestate.states["sleepiness"] = 0
    tiredness.start(TIREDNESS * 1000)  # Every 2 hours
    
def wakeup():
    global baby, babyzzz
    
    # Update sleep tracking variables
    # Restore brightness and disable night mode
    oled.contrast(255)  # Set brightness to 100%
    oled.invert(False)  # Disable inversion
    gamestate.states["display_inverted"] = False
    
    gamestate.states["last_wake_time"] = time()
    gamestate.states["total_sleep_time"] = 0  # Reset sleep time counter
    
    # Reset quick nap tracking
    gamestate.states["quick_nap_active"] = False
    
    # Improve stats
    gamestate.states["sleepiness"] = 10
    gamestate.states["sleeping"] = False
    gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 2)
    gamestate.states["health"] = cap_stat(gamestate.states["health"] + 2)
    
    # IMPORTANT: Explicitly disable ALL sleep animations
    babyzzz_left.set = False
    babyzzz_center.set = False
    babyzzz_right.set = False
    babyzzz.set = False
    
    # Restore the correct baby animation based on position
    if gamestate.states["fox_position"] == 0:  # Left
        baby = baby_left
    elif gamestate.states["fox_position"] == 1:  # Center
        baby = baby_center
    else:  # Right
        baby = baby_right
        
    baby.set = True
    
    # Trigger rain immediately after waking up
    start_rain_effect(force=True)
    
    print(f"Waking up at position {gamestate.states['fox_position']}")
    global baby
    
    # Update sleep tracking variables
    gamestate.states["last_wake_time"] = time()
    gamestate.states["total_sleep_time"] = 0  # Reset sleep time counter
    
    # Reset quick nap tracking
    gamestate.states["quick_nap_active"] = False
    
    # Improve stats
    gamestate.states["sleepiness"] = 10
    gamestate.states["sleeping"] = False
    gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 2)
    gamestate.states["health"] = cap_stat(gamestate.states["health"] + 2)
    
    babyzzz.set = False
    
    # Restore the correct baby animation based on position
    if gamestate.states["fox_position"] == 0:  # Left
        baby = baby_left
    elif gamestate.states["fox_position"] == 1:  # Center
        baby = baby_center
    else:  # Right
        baby = baby_right
        
    baby.set = True
    
    # Trigger rain immediately after waking up
    start_rain_effect(force=True)
    
    print(f"Waking up at position {gamestate.states['fox_position']}")

def quick_nap():
    """Start a quick 2-minute nap"""
    global baby, babyzzz
    
    # Only allow quick naps if not already sleeping and not recently woken up
    current_time = time()
    time_since_waking = current_time - gamestate.states["last_wake_time"]
    time_since_last_nap = current_time - gamestate.states["last_quick_nap_time"]
    
    # Only nap if awake for at least 1 hour and no nap in the last hour
    if (not gamestate.states["sleeping"] and 
        time_since_waking > 3600 and  # 1 hour in seconds
        time_since_last_nap > 3600):  # 1 hour in seconds
        
        gamestate.states["quick_nap_active"] = True
        gamestate.states["last_quick_nap_time"] = current_time
        
        # Hide baby animation
        baby.set = False
        
        # Select the appropriate sleep animation based on fox position
        if gamestate.states["fox_position"] == 0:  # Left
            babyzzz = babyzzz_left
        elif gamestate.states["fox_position"] == 1:  # Center
            babyzzz = babyzzz_center
        else:  # Right
            babyzzz = babyzzz_right
            
        # Set up sleep animation
        babyzzz.loop(no=-1)  # Loop infinitely
        babyzzz.set = True
        
        # Show quick nap message
        sleep_time.message = "Quick nap..."
        sleep_time.popup(oled)
        clear()
        
        # Schedule wakeup
        quick_nap_event.start(QUICK_NAP_DURATION * 1000)  # 2 minutes in milliseconds
        
        # Improve sleepiness slightly
        gamestate.states["sleepiness"] = cap_stat(gamestate.states["sleepiness"] + 1)
        
        print("Starting quick nap")

def force_wake_up():
    """Force the fox to wake up from sleep"""
    global baby
    
    if gamestate.states["sleeping"]:
        # Track total sleep time
        current_time = time()
        sleep_start_time = gamestate.states["last_wake_time"]
        sleep_duration = current_time - sleep_start_time
        gamestate.states["total_sleep_time"] += sleep_duration
        
        gamestate.states["sleeping"] = False
        
        # Turn off ALL sleep animations explicitly
        babyzzz_left.set = False
        babyzzz_center.set = False
        babyzzz_right.set = False
        
        # Restore the correct baby animation based on position
        if gamestate.states["fox_position"] == 0:  # Left
            baby = baby_left
        elif gamestate.states["fox_position"] == 1:  # Center
            baby = baby_center
        else:  # Right
            baby = baby_right
            
        baby.set = True
        
        # Schedule next poop event after waking up
        poop_event.start(randint(POOP_MIN * 1000, POOP_MAX * 1000))
        
        print("Fox woken up")

def end_quick_nap():
    """End a quick nap"""
    global baby
    
    gamestate.states["quick_nap_active"] = False
    
    # Hide sleep animation
    babyzzz.set = False
    
    # Restore the correct baby animation based on position
    if gamestate.states["fox_position"] == 0:  # Left
        baby = baby_left
    elif gamestate.states["fox_position"] == 1:  # Center
        baby = baby_center
    else:  # Right
        baby = baby_right
        
    baby.set = True
    
    # Show wakeup message
    sleep_time.message = "Refreshed!"
    sleep_time.popup(oled)
    clear()
    
    print("Quick nap ended")
    
def poop_check():
    global go_potty
    
    if not gamestate.states["sleeping"]:
        # Select the appropriate potty animation based on fox position
        if gamestate.states["fox_position"] == 0:  # Left
            go_potty = go_potty_left
        elif gamestate.states["fox_position"] == 1:  # Center
            go_potty = go_potty_center
        else:  # Right
            go_potty = go_potty_right
        
        # Set up potty animation with protection
        go_potty.loop(no=1)  # Ensure it only loops once
        baby.set = False
        go_potty.set = True
        gamestate.states["potty_protected"] = True  # Protect the animation
        gamestate.states["potty_frame_counter"] = 0  # Reset safety counter
        
        print(f"poop time at position {gamestate.states['fox_position']}")
    
def clear():
    """ Clear the screen """
    oled.fill_rect(0,0,128,64,0)

def draw_mountain(display):
    """ Draw mountain or trees across the screen below the time bar based on current area """
    if gamestate.states["current_area"] == 0:
        # Draw mountain background in area 0
        display.blit(mountain.image, 0, 16)  # Position just below the time bar
    else:
        # Draw trees background in area 1
        display.blit(trees.image, 0, 16)  # Same position as mountain
        
        # Draw tree in area 1 (behind fox)
        display.blit(tree2.image, 128 - 10 - 20, 6)  # 128 (screen width) - 10 (tree width) - 20 (margin)

def draw_grass(display):
    """ Draw grass across the bottom of the screen """
    # Draw grass 4 times to cover 128 pixel width (32 × 4 = 128)
    for i in range(4):
        display.blit(grass.image, i * 32, 57)  # 57 = 64 - 7 (moved down by 1px)

def draw_clock_and_age(display):
    """ Draw the clock and pet age at the top of the screen """
    # Clear the top area
    display.fill_rect(0, 0, 128, 16, 0)
    
    # Get current time for London (using RTC)
    rtc = RTC()
    current_time = rtc.datetime()
    hour = current_time[4]
    minute = current_time[5]
    
    # Initialize display_inverted state if not present
    if "display_inverted" not in gamestate.states:
        gamestate.states["display_inverted"] = False
    
    # Note: Night mode is now controlled only by the lightbulb function
    # and is not automatically toggled based on time
    
    # Convert to 12-hour format with AM/PM
    am_pm = "AM" if hour < 12 else "PM"
    hour_12 = hour % 12
    if hour_12 == 0:
        hour_12 = 12
    time_str = f"{hour_12:d}:{minute:02d}{am_pm}"
    
    # Calculate pet age in days
    current_seconds = time()
    age_seconds = current_seconds - gamestate.states["pet_birth_time"]
    age_days = age_seconds / (24 * 60 * 60)  # Convert seconds to days
    
    # Round to nearest half day
    age_days_rounded = round(age_days * 2) / 2
    
    # Draw time on left side
    display.text(f"{time_str}", 0, 4)
    
    # Draw age closer to time (at x=60 instead of x=70)
    display.text(f"Age:{age_days_rounded:.1f}d", 60, 4)

def build_toolbar():
    print("building toolbar")
    toolbar = Toolbar()
    toolbar.spacer = 2
    toolbar.additem(food)    
    toolbar.additem(lightbulb)
    toolbar.additem(game)
    toolbar.additem(clock)  # Clock icon for settings
    toolbar.additem(toilet)
    toolbar.additem(heart)
    toolbar.additem(call)
    return toolbar

def do_toolbar_stuff():
    global babyzzz  # Move global declaration to the beginning of the function
    
    if tb.selected_item == "food":
        
        if gamestate.states["fox_position"] == 0:  # Left
            eat = eat_left
        elif gamestate.states["fox_position"] == 1:  # Center
            eat = eat_center
        else:  # Right
            eat = eat_right
        
        # IMPORTANT: Reset animation state to ensure it plays properly
        eat._Animate__current_frame = 0
        eat._Animate__done = False
        
        # Set up eating animation with protection
        eat.loop(no=1)  # Ensure it only loops once
        eat.set = True
        gamestate.states["eating_protected"] = True  # Protect the animation
        gamestate.states["eating_frame_counter"] = 0  # Reset safety counter
        
        # Show a message to confirm feeding is happening
        heart_status.message = "Feeding..."
        heart_status.popup(oled)
        clear()
                
        # Wake up if sleeping
        force_wake_up()
        
        gamestate.states["feeding_time"] = True
        baby.set = False
        
        # Reset last feed time to track hunger
        gamestate.states["last_feed_time"] = time()
        gamestate.states["is_hungry"] = False
        gamestate.states["hunger_alert_shown"] = False
        gamestate.states["fed_today"] = True  # Mark as fed today for daily care tracking
        
        # Select the appropriate eat animation based on fox position
        if gamestate.states["fox_position"] == 0:  # Left
            eat = eat_left
        elif gamestate.states["fox_position"] == 1:  # Center
            eat = eat_center
        else:  # Right
            eat = eat_right
        
        # Set up eating animation with protection
        eat.loop(no=1)  # Ensure it only loops once
        eat.set = True
        gamestate.states["eating_protected"] = True  # Protect the animation
        gamestate.states["eating_frame_counter"] = 0  # Reset safety counter
            
    if tb.selected_item == "game":
        # Wake up if sleeping
        force_wake_up()
        
        print("Starting hide and seek game")
        # Start hide and seek game
        gamestate.states["hide_seek_active"] = True
        gamestate.states["player_score"] = 0
        gamestate.states["fox_score"] = 0
        gamestate.states["cancel_count"] = 0
        
        # Hide regular baby animation
        baby.set = False
        babyzzz.set = False
        
        # Show game start message
        playtime.message = "Hide & Seek!"
        playtime.popup(oled)
        clear()
        
        # Initialize ear position randomly
        set_random_ear_position()
    if tb.selected_item == "toilet":
        # Wake up if sleeping
        force_wake_up()
        
        toilet.message = "Cleaning..."
        toilet.popup(oled)
        poopy.set = False
        baby.set = True
        clear()
        baby.animate(oled)
        poop_event.start(randint(POOP_MIN * 1000, POOP_MAX * 1000))
        
        # Set cleaning flag and timer for testing animations
        gamestate.states["just_cleaned"] = True
        gamestate.states["cleaning_timer"] = 200  # 10 seconds (200 frames at 0.05s per frame)
    if tb.selected_item == "lightbulb":
        if not gamestate.states["sleeping"]:
            # Force end any active animations
            if gamestate.states["butterfly_active"]:
                gamestate.states["butterfly_active"] = False
                butterfly.set = False
                butterfly._Animate__current_frame = 0
                
            if gamestate.states["walking_active"]:
                gamestate.states["walking_active"] = False
                
            if gamestate.states["quick_nap_active"]:
                gamestate.states["quick_nap_active"] = False
                
            # IMPORTANT: Explicitly disable ALL baby animations
            baby_left.set = False
            baby_center.set = False
            baby_right.set = False
            baby.set = False
            
            # Check if fox has already slept for 6 hours in this cycle
            current_time = time()
            remaining_sleep = SLEEP_DURATION
            
            if gamestate.states["total_sleep_time"] >= 6 * 3600:  # 6 hours in seconds
                # Already slept for 6 hours, only allow 6 more
                remaining_sleep = 6 * 3600  # 6 hours in seconds
                sleep_time.message = "Short Sleep"
            else:
                sleep_time.message = "Night Night"
            
            gamestate.states["sleeping"] = True

            # Enable night mode and reduce brightness
            oled.contrast(128)  # Set brightness to 50%
            oled.invert(True)  # Enable inversion
            gamestate.states["display_inverted"] = True
            
            # Select the appropriate sleep animation based on fox position
            if gamestate.states["fox_position"] == 0:  # Left
                babyzzz = babyzzz_left
            elif gamestate.states["fox_position"] == 1:  # Center
                babyzzz = babyzzz_center
            else:  # Right
                babyzzz = babyzzz_right
            
            # Explicitly set to loop infinitely and reset animation state
            babyzzz.loop(no=-1)  # Set to loop infinitely
            babyzzz.set = True
            
            sleep_time.popup(oled)
            clear()
            sleep_time.start(remaining_sleep * 1000)  # Sleep for remaining time
            
            # Cancel any pending poop events during sleep
            poop_event.done = True
            
        else:
            # Track total sleep time
            current_time = time()
            sleep_start_time = gamestate.states["last_wake_time"]
            sleep_duration = current_time - sleep_start_time
            gamestate.states["total_sleep_time"] += sleep_duration
            
            # Call wakeup function to ensure consistent behavior and trigger rain
            wakeup()
            
            # Show morning message
            sleep_time.message = "Morning"
            sleep_time.popup(oled)
            clear()
            
            # Mark as having slept today if slept for at least 30 minutes
            if sleep_duration > 30 * 60:  # 30 minutes in seconds
                gamestate.states["slept_today"] = True
                print("Fox has slept today")
            
            # Schedule next poop event after waking up
            poop_event.start(randint(POOP_MIN * 1000, POOP_MAX * 1000))        # Sleeping
        
    if tb.selected_item == "clock":
        # Wake up if sleeping
        force_wake_up()
        
        # Import settings module
        import settings
        
        # Run settings interface
        pet_settings = settings.run_settings(i2c, oled)
        
        # Apply settings if returned
        if pet_settings:
            # Update pet type if it was changed
            if 'type' in pet_settings and pet_settings['type'] != gamestate.states["pet_type"]:
                print(f"Pet type changed from {gamestate.states['pet_type']} to {pet_settings['type']}")
                
                # Save the new pet type to the game state
                gamestate.states["pet_type"] = pet_settings['type']
                
                # Apply the pet type change immediately
                apply_pet_type_change(pet_settings['type'])
                
                heart_status.message = f"Pet type changed to {pet_settings['type']}"
                heart_status.popup(oled)
                clear()
                
            if 'name' in pet_settings:
                # Show welcome message with pet name
                heart_status.message = f"Hello {pet_settings['name']}!"
                heart_status.popup(oled)
                clear()
    if tb.selected_item == "heart":
        # Wake up if sleeping
        force_wake_up()
        
        # Enhanced heart option to display status information
        heart_status.message = f"HP: {gamestate.states['health']}/10"
        heart_status.popup(oled)
        heart_status.message = f"HAP: {gamestate.states['happiness']}/10"
        heart_status.popup(oled)
        heart_status.message = f"SLP: {gamestate.states['sleepiness']}/10"
        heart_status.popup(oled)
        clear()
        # Still increase happiness as in the original
        gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 2)
        
        # Always trigger auto hide and seek after checking stats (for testing)

    if tb.selected_item == "call":
        # Call for help - reset alert and improve stats slightly
        call_animate.set = False
        gamestate.states["alert"] = False
        gamestate.states["health"] = cap_stat(gamestate.states["health"] + 2)
        gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 2)
        gamestate.states["sleepiness"] = cap_stat(gamestate.states["sleepiness"] + 2)
        
        # Initialize call_cycle if it doesn't exist
        if "call_cycle" not in gamestate.states:
            gamestate.states["call_cycle"] = 0
        
        # Determine direction based on call cycle
        if gamestate.states["call_cycle"] < 3:
            # First three cycles: move right
            direction = 1  # Right
        else:
            # After three cycles: move left
            direction = 0  # Left
        
        # Show the last random message if available, otherwise show "No Alert Active"
        if gamestate.states["alert_reason"]:
            heart_status.message = f"Alert: {gamestate.states['alert_reason']}"
            heart_status.popup(oled)
            gamestate.states["alert_reason"] = ""  # Reset the alert reason
        elif gamestate.states["last_random_message"]:
            heart_status.message = gamestate.states["last_random_message"]
            heart_status.popup(oled)
        else:
            heart_status.message = "No Alert Active"
            heart_status.popup(oled)
        
        clear()
        
        # Update cycle counter
        gamestate.states["call_cycle"] = (gamestate.states["call_cycle"] + 1) % 6
        
        # Force end any active animations
        if gamestate.states["butterfly_active"]:
            gamestate.states["butterfly_active"] = False
            butterfly.set = False
            butterfly.__current_frame = 0
            
        if gamestate.states["walking_active"]:
            gamestate.states["walking_active"] = False
            
        if gamestate.states["quick_nap_active"]:
            gamestate.states["quick_nap_active"] = False
            babyzzz.set = False
        
        # Wake up if sleeping
        force_wake_up()
        
        start_walking_animation(direction)

def unhealthy_environment():
    # Decrease health by 0.7 points per hour (instead of 1 point per 2 hours)
    gamestate.states["health"] -= 0.1
    
    # Check if health is at half and show alert if not already shown
    if gamestate.states["health"] <= 5 and not gamestate.states["poop_alert_shown"]:
        gamestate.states["alert"] = True
        call_animate.set = True
        gamestate.states["alert_reason"] = "Why you no clean?"
        gamestate.states["poop_alert_shown"] = True
    
    # When health reaches half, also decrease happiness
    if gamestate.states["health"] <= 5:
        gamestate.states["happiness"] -= 0.1
    
    print("Unhealthy Environment")
    
    # Cap at 0
    if gamestate.states["health"] <= 0:
        gamestate.states["health"] = 0
    if gamestate.states["happiness"] < 0:
        gamestate.states["happiness"] = 0
        
    gamestate.states["unwell"] = False
    
    # Restart the timer for another hour (3600 seconds)
    decrease_health.start(3600 * 1000)

def check_alerts():
    # Check if any stat is critically low
    health_critical = gamestate.states["health"] <= CRITICAL_THRESHOLD
    happiness_critical = gamestate.states["happiness"] <= CRITICAL_THRESHOLD
    sleepiness_critical = gamestate.states["sleepiness"] <= CRITICAL_THRESHOLD
    
    # Set alert if any stat is critically low
    if health_critical or happiness_critical or sleepiness_critical:
        gamestate.states["alert"] = True
        call_animate.set = True
        
        # Set the alert reason based on which stat is low
        gamestate.states["alert_reason"] = ""
        if health_critical:
            gamestate.states["alert_reason"] = "Low Health"
        if happiness_critical:
            if gamestate.states["alert_reason"]:
                gamestate.states["alert_reason"] += " & Low Happiness"
            else:
                gamestate.states["alert_reason"] = "Low Happiness"
        if sleepiness_critical:
            if gamestate.states["alert_reason"]:
                gamestate.states["alert_reason"] += " & Low Sleep"
            else:
                gamestate.states["alert_reason"] = "Low Sleep"
    else:
        gamestate.states["alert"] = False
        call_animate.set = False
    
    # Check death condition - any two stats at 0
    if ((gamestate.states["health"] <= 0 and gamestate.states["happiness"] <= 0) or
        (gamestate.states["health"] <= 0 and gamestate.states["sleepiness"] <= 0) or
        (gamestate.states["happiness"] <= 0 and gamestate.states["sleepiness"] <= 0)):
        
        # Set death cause based on which stats are at 0
        if gamestate.states["health"] <= 0 and gamestate.states["happiness"] <= 0:
            gamestate.states["death_cause"] = "Sick and unhappy"
        elif gamestate.states["health"] <= 0 and gamestate.states["sleepiness"] <= 0:
            gamestate.states["death_cause"] = "Sick and exhausted"
        elif gamestate.states["happiness"] <= 0 and gamestate.states["sleepiness"] <= 0:
            gamestate.states["death_cause"] = "Unhappy and exhausted"
            
        # Trigger death if not already dead
        if not death.set:
            death.set = True
            gamestate.states["death_screen_shown"] = False

# Hide and seek game functions
def set_random_ear_position():
    """Set a random position for the ears animation"""
    # Randomly choose position (0=left, 1=middle, 2=right)
    gamestate.states["ear_position"] = randint(0, 2)
    # Reset the ear pause timer
    gamestate.states["ear_pause_timer"] = 20  # 1 second pause (20 frames at 0.05s per frame)
    print(f"Ears set to position {gamestate.states['ear_position']}")

def check_player_guess(position):
    """Check if the player's guess matches the ear position"""
    # Store current position for comparison
    current_position = gamestate.states["ear_position"]
    
    # Compare player's guess with current position
    correct = position == current_position
    
    # Update scores based on guess
    if correct:
        # Player guessed correctly
        gamestate.states["player_score"] += 1
        playtime.message = "You found me!"
    else:
        # Player guessed incorrectly
        gamestate.states["fox_score"] += 1
        playtime.message = f"Wrong spot! It was {['left', 'middle', 'right'][current_position]}"
    
    # Show result
    playtime.popup(oled)
    clear()
    
    # Show current score with more detail
    display_game_score()
    
    # Check if game is over
    if gamestate.states["player_score"] >= 3 or gamestate.states["fox_score"] >= 3:
        end_hide_seek_game()
    else:
        # Reset animation states before changing position
        ears_left.set = False
        ears_middle.set = False
        ears_right.set = False
        
        # Continue game with new position
        set_random_ear_position()

def display_game_score():
    """Display the current hide and seek game score"""
    score_event = Event(name="Game Score", sprite=game)
    # Use shorter text to prevent truncation
    # Use different letters based on pet type
    pet_letter = "F" if gamestate.states["pet_type"] == "Fox" else "G"
    score_event.message = f"U:{gamestate.states['player_score']} {pet_letter}:{gamestate.states['fox_score']}"
    score_event.popup(oled)
    clear()

def end_hide_seek_game():
    """End the hide and seek game and show the final result"""
    gamestate.states["hide_seek_active"] = False
    
    # Determine winner
    if gamestate.states["player_score"] > gamestate.states["fox_score"]:
        # Show different win messages based on pet type
        if gamestate.states["pet_type"] == "Fox":
            playtime.message = "You Win Wren!"
        else:
            playtime.message = "You Win Hugo!"
        
        # Update last play time
        gamestate.states["last_play_time"] = time()
        gamestate.states["played_today"] = True  # Mark as played today for daily care tracking
        
        # Reward player with happiness - cap at 8 if poop exists, otherwise cap at 10
        if poopy.set:
            # Cap at 8 if poop exists
            gamestate.states["happiness"] = min(8, gamestate.states["happiness"] + 3)
            playtime.message = "You win! Clean me!"
        else:
            # Cap at 10 if no poop
            gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 3)
    else:
        playtime.message = "Fox wins!"
        
        # Update last play time
        gamestate.states["last_play_time"] = time()
        
        # Still give some happiness for playing
        if poopy.set:
            # Cap at 8 if poop exists
            gamestate.states["happiness"] = min(8, gamestate.states["happiness"] + 1)
        else:
            # Cap at 10 if no poop
            gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 1)
    
    playtime.popup(oled)
    clear()
    
    # Reset game state
    ears_left.set = False
    ears_middle.set = False
    ears_right.set = False
    
    # Show love heart animation - fox likes being played with
    love.set = True
    
    # Clear screen
    oled.fill_rect(0, 0, 128, 64, 0)
    
    # Use animate method instead of directly accessing image
    # This ensures the animation is properly loaded
    love.animate(oled)
    oled.show()
    sleep(1)  # Show heart for 1 second
    
    # Add +2 health and happiness
    gamestate.states["health"] = cap_stat(gamestate.states["health"] + 2)
    gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 2)
    
    # Show baby again
    love.set = False
    # Reset animation frame to prevent artifacts
    love.__current_frame = 0
    
    # AGGRESSIVE CLEARING - Clear the entire screen again
    oled.fill_rect(0, 0, 128, 64, 0)
    
    # Restore the correct baby animation based on position
    if gamestate.states["fox_position"] == 0:  # Left
        baby = baby_left
    elif gamestate.states["fox_position"] == 1:  # Center
        baby = baby_center
    else:  # Right
        baby = baby_right
        
    baby.set = True

def start_butterfly_animation():
    """Start the butterfly animation"""
    global butterfly
    
    # Don't start animation if fox is sleeping
    if gamestate.states["sleeping"]:
        return
    
    if not gamestate.states["butterfly_active"] and not gamestate.states["walking_active"]:
        # Select the appropriate butterfly animation based on fox position
        if gamestate.states["fox_position"] == 0:  # Left
            butterfly = butterfly_left
        elif gamestate.states["fox_position"] == 1:  # Center
            butterfly = butterfly_center
        else:  # Right
            butterfly = butterfly_right
            
        gamestate.states["butterfly_active"] = True
        butterfly.set = True
        # Hide regular baby animation temporarily
        baby.set = False
        
        print(f"Starting butterfly animation at position {gamestate.states['fox_position']}")

def start_bunny_animation():
    # Start the bunny animation - only shows on right side when fox is on left in Area 0
    # Don't start animation if fox is sleeping
    if gamestate.states["sleeping"]:
        return
        
    # Don't start animation if fox is in Area 1
    if gamestate.states["current_area"] == 1:
        return
        
    # Only start if fox is on left and no other animations are active
    if (gamestate.states["fox_position"] == 0 and  # Fox must be on left
        not gamestate.states["bunny_active"] and
        not gamestate.states["butterfly_active"] and
        not gamestate.states["walking_active"] and
        not gamestate.states["quick_nap_active"]):
        
        # Set bunny animation active
        gamestate.states["bunny_active"] = True
        gamestate.states["last_bunny_time"] = time()
        
        # IMPORTANT: Reset bunny animation state to ensure it plays properly
        bunny_animation._Animate__current_frame = 0
        bunny_animation._Animate__done = False
        
        # Don't hide the fox animation - allow both to play together
        # baby.set = False  # This line is removed to keep fox visible
        
        # Set up bunny animation
        bunny_animation.loop(no=1)  # IMPORTANT: Ensure it only loops once
        bunny_animation.set = True
        
        print("Starting bunny animation with fox bouncing")
    """Start the bunny animation - only shows on right side when fox is on left in Area 0"""
    # Don't start animation if fox is sleeping
    if gamestate.states["sleeping"]:
        return
        
    # Don't start animation if fox is in Area 1
    if gamestate.states["current_area"] == 1:
        return
        
    # Only start if fox is on left and no other animations are active
    if (gamestate.states["fox_position"] == 0 and  # Fox must be on left
        not gamestate.states["bunny_active"] and
        not gamestate.states["butterfly_active"] and
        not gamestate.states["walking_active"] and
        not gamestate.states["quick_nap_active"]):
        
        # Set bunny animation active
        gamestate.states["bunny_active"] = True
        gamestate.states["last_bunny_time"] = time()
        
        # Don't hide the fox animation - allow both to play together
        # baby.set = False  # This line is removed to keep fox visible
        
        # Set up bunny animation
        bunny_animation.set = True
        
        print("Starting bunny animation with fox bouncing")

def update_bunny_animation():
    # Update the bunny animation
    if gamestate.states["bunny_active"]:
        # IMPORTANT: Check if bunny animation has been active for too long
        current_time = time()
        time_since_start = current_time - gamestate.states["last_bunny_time"]
        
        # If bunny animation has been active for more than 30 seconds, force end it
        if time_since_start > 30:
            print("Bunny animation has been active for too long - force ending")
            gamestate.states["bunny_active"] = False
            bunny_animation.set = False
            bunny_animation._Animate__current_frame = 0
            bunny_animation._Animate__done = False
            return
        
        # Animate the bunny
        bunny_animation.animate(oled)
        
        # Check if animation is done
        if bunny_animation.done:
            # End bunny animation
            gamestate.states["bunny_active"] = False
            bunny_animation.set = False
            # Reset animation state to prevent getting stuck
            bunny_animation._Animate__current_frame = 0
            bunny_animation._Animate__done = False
            
            # Make fox walk back to center to look
            if gamestate.states["fox_position"] == 0:  # If fox is on left
                # Start walking to center
                start_walking_animation(1)  # 1 = right direction
            
            print("Bunny animation completed")
            
        # Safety check - if animation has been active for too long, force end it
        # This prevents getting stuck in an infinite loop
        if randint(0, 50) == 0:  # Increased chance to end animation if it gets stuck (1 in 50)
            gamestate.states["bunny_active"] = False
            bunny_animation.set = False
            bunny_animation._Animate__current_frame = 0
            bunny_animation._Animate__done = False
            baby.set = True
            print("Bunny animation force-ended")
    """Update the bunny animation"""
    if gamestate.states["bunny_active"]:
        # Animate the bunny
        bunny_animation.animate(oled)
        
        # Check if animation is done
        if bunny_animation.done:
            # End bunny animation
            gamestate.states["bunny_active"] = False
            bunny_animation.set = False
            # Reset animation state to prevent getting stuck
            bunny_animation.__current_frame = 0
            
            # Make fox walk back to center to look
            if gamestate.states["fox_position"] == 0:  # If fox is on left
                # Start walking to center
                start_walking_animation(1)  # 1 = right direction
            
            print("Bunny animation completed")
            
        # Safety check - if animation has been active for too long, force end it
        # This prevents getting stuck in an infinite loop
        if randint(0, 100) == 0:  # Small random chance to end animation if it gets stuck
            gamestate.states["bunny_active"] = False
            bunny_animation.set = False
            bunny_animation.__current_frame = 0
            baby.set = True
            print("Bunny animation force-ended")

def update_butterfly_animation():
    """Update the butterfly animation"""
    if gamestate.states["butterfly_active"]:
        butterfly.animate(oled)
        
        # Check if animation is done
        if butterfly.done:
            gamestate.states["butterfly_active"] = False
            butterfly.set = False
            # Reset animation state to prevent getting stuck
            butterfly.__current_frame = 0
            # Show baby again
            baby.set = True
            print("Butterfly animation completed")
            
        # Safety check - if animation has been active for too long, force end it
        # This prevents getting stuck in an infinite loop
        if randint(0, 100) == 0:  # Small random chance to end animation if it gets stuck
            gamestate.states["butterfly_active"] = False
            butterfly.set = False
            butterfly.__current_frame = 0
            baby.set = True
            print("Butterfly animation force-ended")

def start_walking_animation(direction):
    """Start the fox walking animation
    direction: 0=left, 1=right"""
    global fox_x_position, fox_frame_index, fox_movement_counter
    
    # Don't start walking animation if fox is sleeping
    if gamestate.states["sleeping"]:
        print("Fox is sleeping - not starting walking animation")
        return
        
    if not gamestate.states["walking_active"] and not gamestate.states["butterfly_active"]:
        gamestate.states["walking_active"] = True
        gamestate.states["walking_direction"] = direction
        
        # Hide regular baby animation temporarily
        baby.set = False
        
        # Set starting position based on current fox position
        if gamestate.states["fox_position"] == 0:  # Left
            fox_x_position = 0
        elif gamestate.states["fox_position"] == 1:  # Center
            fox_x_position = 48
        else:  # Right
            fox_x_position = 80
            
        fox_frame_index = 0  # Reset animation frame
        fox_movement_counter = 0  # Reset movement counter
        
        print(f"Starting walking animation: direction={'left' if direction==0 else 'right'}, from position {gamestate.states['fox_position']}")
def update_walking_animation():
    """Update the fox walking animation"""
    global fox_x_position, fox_frame_index, fox_movement_counter
    
    if gamestate.states["walking_active"]:
        # AGGRESSIVE CLEARING - Clear the entire screen except toolbar/clock area
        oled.fill_rect(0, 16, 128, 48, 0)  # Clear all the way to the bottom
        
        # Update position based on direction
        if gamestate.states["walking_direction"] == 0:  # Walking left
            fox_x_position -= 3  # Move left by 3 pixels (slower)
            print(f"MOVING LEFT: {fox_x_position}")
            
            # IMPORTANT: Check for area transitions FIRST, before bounds checking
            # Handle area transition from Area 1 left to Area 0 right
            if gamestate.states["current_area"] == 1 and gamestate.states["fox_position"] == 0 and fox_x_position < -40:
                # Transition from area 1 left to area 0 right
                gamestate.states["current_area"] = 0
                gamestate.states["fox_position"] = 2  # Right position in area 0
                fox_x_position = 80
                
                # Reset squirrel state when leaving Area 1
                gamestate.states["squirrel_activated"] = False
                gamestate.states["squirrel_active"] = False
                gamestate.states["squirrel_initial_timer"] = 0
                squirrel_animation.set = False
                
                end_walking_animation()
                return
            
            # Handle position changes within the same area
            elif gamestate.states["fox_position"] == 2:  # Started from right
                # Walking to center
                if fox_x_position <= 48:  # Reached center
                    gamestate.states["fox_position"] = 1  # Update position to center
                    end_walking_animation()
                    return
            elif gamestate.states["fox_position"] == 1:  # Started from center
                # Walking to left
                if fox_x_position <= 0:  # Reached left edge
                    gamestate.states["fox_position"] = 0  # Update position to left
                    end_walking_animation()
                    return
            
            # Only apply bounds checking if we're not transitioning between areas
            # and we're already at the leftmost position in the current area
            if gamestate.states["fox_position"] == 0 and fox_x_position < -40 and gamestate.states["current_area"] == 0:
                fox_x_position = -40
                # End walking animation when reaching the edge
                end_walking_animation()
                return
                
            # Use left-facing frames
            frames = fox_frames_left
            
        else:  # Walking right
            fox_x_position += 3  # Move right by 3 pixels (slower)
            print(f"MOVING RIGHT: {fox_x_position}")
            
            # IMPORTANT: Check for area transitions FIRST, before bounds checking
            # Handle area transition from Area 0 right to Area 1 left
            if gamestate.states["current_area"] == 0 and gamestate.states["fox_position"] == 2 and fox_x_position > 120:
                # Transition from area 0 right to area 1 left
                gamestate.states["current_area"] = 1
                gamestate.states["fox_position"] = 0  # Left position in area 1
                fox_x_position = 0
                end_walking_animation()
                return
            
            # Handle position changes within the same area
            elif gamestate.states["fox_position"] == 0:  # Started from left
                # Walking to center
                if fox_x_position >= 48:  # Reached center
                    gamestate.states["fox_position"] = 1  # Update position to center
                    end_walking_animation()
                    return
            elif gamestate.states["fox_position"] == 1:  # Started from center
                # Walking to right
                if fox_x_position >= 80:  # Reached right edge
                    gamestate.states["fox_position"] = 2  # Update position to right
                    end_walking_animation()
                    return
            
            # Only apply bounds checking if we're not transitioning between areas
            # and we're already at the rightmost position in the current area
            if gamestate.states["fox_position"] == 2 and fox_x_position > 120 and gamestate.states["current_area"] == 1:
                fox_x_position = 120
                # End walking animation when reaching the edge
                end_walking_animation()
                return
                
            # Use right-facing frames
            frames = fox_frames_right
        
        # Position indicator removed
        
        # Increment movement counter
        fox_movement_counter += 1
        
        # Add safety counter to prevent infinite walking
        # If the fox has been walking for too long (500 frames = 25 seconds), force end the animation
        if fox_movement_counter > 500:
            print("Walking animation has been active for too long - force ending")
            end_walking_animation()
            return
        
        # Cycle to next animation frame every few steps
        # Use a movement counter to slow down the animation
        if fox_movement_counter % 3 == 0:  # Change frame every 3 position updates
            fox_frame_index = (fox_frame_index + 1) % 4
            print(f"FRAME CHANGED to {fox_frame_index}")
        
        # Get the current frame based on direction
        current_frame = frames[fox_frame_index]
        print(f"Using frame {fox_frame_index}: {current_frame.name}")
        
        # Draw the current frame at the current position
        oled.blit(current_frame.image, fox_x_position, 19)
        
        # Print position and frame for debugging
        print(f"Fox position: {fox_x_position}, Frame: {fox_frame_index}, Counter: {fox_movement_counter}")
def start_auto_hide_seek():
    """Start the automatic hide and seek animation sequence"""
    # Don't start animation if fox is sleeping
    if gamestate.states["sleeping"]:
        return
        
    # Only start if no other animations are active
    if (not gamestate.states["butterfly_active"] and 
        not gamestate.states["walking_active"] and
        not gamestate.states["quick_nap_active"] and
        not gamestate.states["hide_seek_active"]):
        
        gamestate.states["auto_hide_seek_active"] = True
        gamestate.states["auto_hide_seek_position"] = 0  # Start with left position
        gamestate.states["auto_hide_seek_timer"] = 80  # Show each position for 4 seconds (80 frames)
        gamestate.states["auto_hide_seek_pause"] = 0  # No initial pause
        gamestate.states["last_auto_hide_seek"] = time()
        
        # Hide regular animations
        baby.set = False
        
        # Show game start message
        playtime.message = "Hide & Seek!"
        playtime.popup(oled)
        clear()
        
        # Show ears at first position (left)
        ears_left.set = True
        ears_middle.set = False
        ears_right.set = False
        
        # Show initial message
        playtime.message = "Can you see me?"
        playtime.popup(oled)
        clear()
        
        print("Starting auto hide and seek sequence")

def update_auto_hide_seek():
    """Update the automatic hide and seek animation"""
    if gamestate.states["auto_hide_seek_active"]:
        # Update timer
        if gamestate.states["auto_hide_seek_timer"] > 0:
            gamestate.states["auto_hide_seek_timer"] -= 1
            
            # Show "Can you see me?" message when timer is at 70 (shortly after position is shown)
            if gamestate.states["auto_hide_seek_timer"] == 70:
                playtime.message = "Can you see me?"
                playtime.popup(oled)
                clear()
        else:
            # Move to next position
            gamestate.states["auto_hide_seek_position"] += 1
            
            # Check if we've shown all positions
            if gamestate.states["auto_hide_seek_position"] > 2:
                # End the animation sequence
                end_auto_hide_seek()
                return
                
            # Hide all ears first to prevent overlap
            ears_left.set = False
            ears_middle.set = False
            ears_right.set = False
            
            # Show "I'm hiding..." message during transition
            playtime.message = "I'm hiding..."
            playtime.popup(oled)
            clear()
            
            # Set a brief pause before showing the next ears
            gamestate.states["auto_hide_seek_pause"] = 20  # 1 second pause (20 frames)
            gamestate.states["auto_hide_seek_timer"] = 80  # Reset timer to 4 seconds
            return
            
        # Check if we're in the pause between positions
        if gamestate.states.get("auto_hide_seek_pause", 0) > 0:
            gamestate.states["auto_hide_seek_pause"] -= 1
            if gamestate.states["auto_hide_seek_pause"] == 0:
                # Pause is over, show the ears for the current position
                if gamestate.states["auto_hide_seek_position"] == 0:  # Left
                    ears_left.set = True
                    ears_middle.set = False
                    ears_right.set = False
                elif gamestate.states["auto_hide_seek_position"] == 1:  # Center
                    ears_left.set = False
                    ears_middle.set = True
                    ears_right.set = False
                else:  # Right
                    ears_left.set = False
                    ears_middle.set = False
                    ears_right.set = True
                    
                # Show "Peekaboo!" message when appearing in new position
                playtime.message = "Peekaboo!"
                playtime.popup(oled)
                clear()
            return
            
        # Animate the appropriate ears
        if gamestate.states["auto_hide_seek_position"] == 0:  # Left
            ears_left.animate(oled)
        elif gamestate.states["auto_hide_seek_position"] == 1:  # Center
            ears_middle.animate(oled)
        else:  # Right
            ears_right.animate(oled)

def end_auto_hide_seek():
    """End the automatic hide and seek animation sequence"""
    global baby
    
    gamestate.states["auto_hide_seek_active"] = False
    
    # Hide all ear animations
    ears_left.set = False
    ears_middle.set = False
    ears_right.set = False
    
    # Reset animation frames to prevent artifacts
    ears_left.__current_frame = 0
    ears_middle.__current_frame = 0
    ears_right.__current_frame = 0
    
    # AGGRESSIVE CLEARING - Clear the entire screen area where ears might be
    oled.fill_rect(0, 8, 128, 48, 0)  # Clear from y=8 to y=56
    
    # Return fox to center position
    gamestate.states["fox_position"] = 1
    baby = baby_center
    baby.set = True
    
    print("Auto hide and seek sequence completed")

def end_walking_animation():
    """End the fox walking animation"""
    global baby
    gamestate.states["walking_active"] = False
    
    # Update baby position based on fox position without showing messages
    if gamestate.states["fox_position"] == 0:  # Left
        # Use the left-positioned baby animation
        baby = baby_left
    elif gamestate.states["fox_position"] == 1:  # Center
        # Use the center-positioned baby animation
        baby = baby_center
    else:  # Right
        # Use the right-positioned baby animation
        baby = baby_right
    
    # Show baby again
    baby.set = True
    
    # Start squirrel timer when entering Area 1 (without showing message)
    if gamestate.states["current_area"] == 1 and not gamestate.states["squirrel_activated"]:
        # Set timer for 5 seconds (100 frames at 0.05s per frame)
        gamestate.states["squirrel_initial_timer"] = 100
    
    # Start rain when fox is in center or right position of Area 1
    if gamestate.states["current_area"] == 1 and gamestate.states["fox_position"] >= 1:
        start_rain_effect()
    
    # Clear the screen
    clear()

def start_rain_effect(force=False):
    """Start the rain effect, with option to force regardless of time"""
    if not gamestate.states["rain_active"]:
        # Allow rain in any area (removed Area 1 restriction)
        
        # Check if enough time has passed since last rain (15 minutes) or if forced
        current_time = time()
        time_since_last_rain = current_time - gamestate.states["last_rain_time"]
        
        if force or time_since_last_rain > 15 * 60:  # 15 minutes in seconds
            # Initialize rain state
            gamestate.states["rain_active"] = True
            gamestate.states["rain_drops"] = []
            gamestate.states["last_rain_time"] = current_time
            
            # Create initial raindrops with random x positions
            for _ in range(gamestate.states["rain_intensity"]):
                x = randint(0, 127)  # Random x position across screen width
                y = randint(0, 30)   # Random starting height
                gamestate.states["rain_drops"].append([x, y])
            
            # Set timer for 60 seconds (1200 frames at 0.05s per frame)
            gamestate.states["rain_timer"] = 1200
            
            # Show message
            heart_status.message = "It's raining!"
            heart_status.popup(oled)
            clear()
            
            # Set a random timer for next rain activation (between 15-30 minutes)
            gamestate.states["rain_random_timer"] = randint(15 * 60 * 20, 30 * 60 * 20)  # 15-30 minutes at 0.05s per frame

def update_rain_effect(display):
    """Update and draw the rain effect - single drops like in area_test.py"""
    if not gamestate.states["rain_active"]:
        return
        
    # Update timer
    gamestate.states["rain_timer"] -= 1
    if gamestate.states["rain_timer"] <= 0:
        # End rain effect when timer expires
        gamestate.states["rain_active"] = False
        gamestate.states["rain_drops"] = []
        return
    
    # Clear the rain area (from top of screen to grass level)
    # This ensures previous rain pixels don't leave traces
    # We only clear the area above the background elements (y=16 to y=56)
    display.fill_rect(0, 16, 128, 41, 0)  # Clear from y=16 to y=56
    
    # Redraw background elements that were cleared
    draw_mountain(display)
    
    # Update raindrop positions
    new_drops = []
    for drop in gamestate.states["rain_drops"]:
        x, y = drop
        
        # Move drop down by 2-4 pixels (random speed)
        y += randint(2, 4)
        
        # If drop hits ground (grass level at y=57), create a new drop at the top
        if y >= 57:
            # Create new drop at top
            new_x = randint(0, 127)
            new_drops.append([new_x, 0])
        else:
            # Keep existing drop
            new_drops.append([x, y])
    
    # Update rain drops list
    gamestate.states["rain_drops"] = new_drops
    
    # Draw raindrops as single pixels (not strings)
    for drop in gamestate.states["rain_drops"]:
        x, y = drop
        # Draw just a single pixel for each raindrop
        display.pixel(x, y, 1)  # Draw white pixel

def start_squirrel_animation():
    """Start the squirrel animation"""
    if not gamestate.states["squirrel_active"]:
        # Set animation active
        gamestate.states["squirrel_active"] = True
        gamestate.states["squirrel_activated"] = True
        gamestate.states["squirrel_last_time"] = time()
        
        # Reset animation and make visible
        squirrel_animation._Animate__current_frame = 0
        squirrel_animation.set = True
        
        # Show message
        heart_status.message = "Look, a squirrel!"
        heart_status.popup(oled)
        clear()

def update_squirrel_timers():
    """Update squirrel animation timers"""
    current_time = time()
    
    # Only process when in Area 1
    if gamestate.states["current_area"] != 1:
        return
        
    # Initial activation timer (5 seconds after entering Area 1)
    if not gamestate.states["squirrel_activated"]:
        if gamestate.states["squirrel_initial_timer"] > 0:
            gamestate.states["squirrel_initial_timer"] -= 1
            if gamestate.states["squirrel_initial_timer"] <= 0:
                start_squirrel_animation()
    else:
        # Random activation (not more than once per minute)
        time_since_last = current_time - gamestate.states["squirrel_last_time"]
        if time_since_last > 60:  # At least 60 seconds since last activation
            if gamestate.states["squirrel_random_timer"] > 0:
                gamestate.states["squirrel_random_timer"] -= 1
                if gamestate.states["squirrel_random_timer"] <= 0:
                    start_squirrel_animation()
            else:
                # Set a new random timer (between 10-30 seconds)
                gamestate.states["squirrel_random_timer"] = randint(200, 600)  # 10-30 seconds at 0.05s per frame

def update_cleaning_timer():
    """Update the timer for animations after cleaning"""
    if gamestate.states["just_cleaned"]:
        if gamestate.states["cleaning_timer"] > 0:
            gamestate.states["cleaning_timer"] -= 1
            
            # Start butterfly animation 5 seconds after cleaning
            if gamestate.states["cleaning_timer"] == 100:  # 5 seconds (100 frames at 0.05s per frame)
                start_butterfly_animation()
                
            # Reset the cleaning flag when timer expires
            if gamestate.states["cleaning_timer"] == 0:
                gamestate.states["just_cleaned"] = False

def update_hide_seek_game():
    """Update the hide and seek game state"""
    # Hide regular animations
    baby.set = False
    babyzzz.set = False
    eat.set = False
    
    # Update ear animations based on position but don't draw them yet
    # We'll draw them after the grass to make them appear within the grass
    if gamestate.states["ear_position"] == 0:  # Left
        ears_left.set = True
        ears_middle.set = False
        ears_right.set = False
    elif gamestate.states["ear_position"] == 1:  # Middle
        ears_left.set = False
        ears_middle.set = True
        ears_right.set = False
    else:  # Right
        ears_left.set = False
        ears_middle.set = False
        ears_right.set = True
    
    # Handle ear pause timer
    if gamestate.states["ear_pause_timer"] > 0:
        gamestate.states["ear_pause_timer"] -= 1
        if gamestate.states["ear_pause_timer"] == 0:
            # After pause, move to a new position
            set_random_ear_position()

def draw_ears(display):
    """Draw the ears animations after the grass is drawn"""
    if not gamestate.states["hide_seek_active"]:
        return
        
    # Animate the appropriate ears based on position
    if gamestate.states["ear_position"] == 0:  # Left
        if ears_left.set:
            ears_left.animate(display)
    elif gamestate.states["ear_position"] == 1:  # Middle
        if ears_middle.set:
            ears_middle.animate(display)
    else:  # Right
        if ears_right.set:
            ears_right.animate(display)

def trigger_random_event():
    """Trigger a random event with a small chance"""
    # Don't trigger during sleep
    if gamestate.states["sleeping"]:
        return
        
    # Small chance of random event (1 in 1000 frames, about once every ~50 seconds at 0.05s per frame)
    # Don't trigger during bunny animation to prevent interference
    if not gamestate.states["bunny_active"] and randint(0, 999) == 0:
        event_message = random_events[randint(0, len(random_events) - 1)]
        # Store the message for later use
        gamestate.states["last_random_message"] = event_message
        
        random_event = Event(name="Random", sprite=game)
        random_event.message = event_message
        random_event.popup(oled)
        clear()
        print(f"Random event: {event_message}")

def start_birds_animation():
    """Start the birds flying animation"""
    global baby_left, baby_center, baby_right
    
    # Don't start animation if fox is sleeping
    if gamestate.states["sleeping"]:
        return
    
    # Only start if no other animations are active
    if (not gamestate.states["birds_active"] and 
        not gamestate.states["bunny_active"] and
        not gamestate.states["butterfly_active"] and
        not gamestate.states["walking_active"] and
        not gamestate.states["hide_seek_active"] and
        not gamestate.states["auto_hide_seek_active"]):
        
        # Set birds animation active
        gamestate.states["birds_active"] = True
        gamestate.states["last_birds_time"] = time()
        gamestate.states["bird_frame"] = 0
        gamestate.states["bird_frame_counter"] = 0
        
        # Speed up fox animation to show excitement
        baby_left.speed = 'normal'
        baby_center.speed = 'normal'
        baby_right.speed = 'normal'
        print("Fox is excited - animation speed increased!")
        
        # Create 1-3 birds with random positions and directions
        num_birds = randint(1, 3)
        gamestate.states["bird_positions"] = []
        
        for i in range(num_birds):
            # Random starting position
            if randint(0, 1) == 0:
                # Start from left
                x = -8
                direction = 1  # Moving right
            else:
                # Start from right
                x = 128
                direction = 0  # Moving left
                
            # Random height in sky area (top portion of screen)
            y = randint(17, 30)
            
            # Add bird [x, y, direction, speed]
            speed = randint(1, 3)  # Random speed
            gamestate.states["bird_positions"].append([x, y, direction, speed])
        
        print(f"Starting birds animation with {num_birds} birds")

def update_birds_animation():
    """Update the birds flying animation"""
    if gamestate.states["birds_active"]:
        # Update bird animation frame counter
        gamestate.states["bird_frame_counter"] += 1
        
        # Change animation frame every 5 frames (0.25 seconds)
        if gamestate.states["bird_frame_counter"] % 5 == 0:
            gamestate.states["bird_frame"] = (gamestate.states["bird_frame"] + 1) % 4
        
        # Get current animation frame
        current_frame = bird_frames[gamestate.states["bird_frame"]]
        
        # Update bird positions
        birds_still_visible = False
        for bird in gamestate.states["bird_positions"]:
            x, y, direction, speed = bird
            
            # Update position based on direction
            if direction == 1:  # Moving right
                bird[0] += speed
                # Check if still on screen
                if bird[0] < 128:
                    birds_still_visible = True
            else:  # Moving left
                bird[0] -= speed
                # Check if still on screen
                if bird[0] > -8:
                    birds_still_visible = True
            
            # Draw bird if on screen
            if -8 < bird[0] < 128:
                oled.blit(current_frame.image, bird[0], bird[1])
        
        # Show "Birds!" message only once when birds first appear
        if not gamestate.states["birds_message_shown"] and baby.set:
            heart_status.message = "Birds!"
            heart_status.popup(oled)
            clear()
            gamestate.states["birds_message_shown"] = True
        
        # End animation if all birds have left the screen
        if not birds_still_visible:
            gamestate.states["birds_active"] = False
            gamestate.states["bird_positions"] = []
            gamestate.states["birds_message_shown"] = False  # Reset for next time
            
            # Return fox animation speed to very slow
            baby_left.speed = 'very slow'
            baby_center.speed = 'very slow'
            baby_right.speed = 'very slow'
            
            print("Birds animation completed - all birds left screen, fox calms down")

def trigger_reflection():
    """Trigger a reflection based on pet state with a small chance"""
    # Don't trigger during sleep
    if gamestate.states["sleeping"]:
        return
        
    # Less frequent than random events (1 in 1500 frames, about once every ~75 seconds at 0.05s per frame)
    # Don't trigger during bunny animation or birds animation to prevent interference
    if (not gamestate.states["bunny_active"] and 
        not gamestate.states["birds_active"] and 
        randint(0, 1499) == 0):
        # Determine which type of reflection based on pet state
        reflection_type = "general"
        
        if gamestate.states["health"] <= 5:
            reflection_type = "health_low"
        elif gamestate.states["health"] >= 8:
            reflection_type = "health_good"
        elif gamestate.states["happiness"] <= 5:
            reflection_type = "happiness_low"
        elif gamestate.states["happiness"] >= 8:
            reflection_type = "happiness_good"
        elif gamestate.states["sleepiness"] <= 5:
            reflection_type = "sleepiness_low"
        elif gamestate.states["sleepiness"] >= 8:
            reflection_type = "sleepiness_good"
            
        # Get a random message from the appropriate category
        messages = reflections[reflection_type]
        message = messages[randint(0, len(messages) - 1)]
        
        # Display the reflection
        reflection_event = Event(name="Thought", sprite=bubble)
        reflection_event.message = message
        reflection_event.popup(oled)
        clear()
        print(f"Reflection: {message}")

def hunger_check():
    """Check if the fox is hungry and apply effects"""
    # Check if it's been more than 6 hours since last feeding
    current_time = time()
    time_since_feeding = current_time - gamestate.states["last_feed_time"]
    
    if time_since_feeding > 6 * 3600:  # 6 hours in seconds
        # Fox is hungry
        if not gamestate.states["is_hungry"]:
            gamestate.states["is_hungry"] = True
            
            # Show hunger alert if not already shown
            if not gamestate.states["hunger_alert_shown"]:
                gamestate.states["alert"] = True
                call_animate.set = True
                gamestate.states["alert_reason"] = "Me Hungry"
                gamestate.states["hunger_alert_shown"] = True
        
        # Decrease health and happiness by 0.25 points per hour if environment is clean
        if not poopy.set:
            gamestate.states["health"] -= 0.035
            gamestate.states["happiness"] -= 0.035
            
            # Cap at 0
            if gamestate.states["health"] < 0:
                gamestate.states["health"] = 0
            if gamestate.states["happiness"] < 0:
                gamestate.states["happiness"] = 0
    else:
        # Reset hunger state
        gamestate.states["is_hungry"] = False
        gamestate.states["hunger_alert_shown"] = False
    
    # Schedule next hunger check
    hunger_event.start(HUNGER_CHECK_INTERVAL * 1000)  # Check every hour

def check_daily_care():
    """Check if daily care requirements are met and apply consequences if not"""
    current_time = time()
    time_since_check = current_time - gamestate.states["last_daily_care_check"]
    
    # Check once per hour
    if time_since_check > 3600:
        gamestate.states["last_daily_care_check"] = current_time
        
        # Get current hour to detect day change
        rtc = RTC()
        current_hour = rtc.datetime()[4]
        
        # Reset at midnight
        if current_hour == 0:
            reset_daily_care()
            return
            
        # Check if 24 hours have passed since last feed
        time_since_feeding = current_time - gamestate.states["last_feed_time"]
        if time_since_feeding > 24 * 3600 and not gamestate.states["fed_today"]:
            # Decrease health and happiness if not fed today
            gamestate.states["health"] -= 0.3
            gamestate.states["happiness"] -= 0.3
            gamestate.states["alert"] = True
            call_animate.set = True
            gamestate.states["alert_reason"] = "Need food!"
            
        # Check if 24 hours have passed since last play
        time_since_play = current_time - gamestate.states["last_play_time"]
        if time_since_play > 24 * 3600 and not gamestate.states["played_today"]:
            # Decrease happiness if not played with today
            gamestate.states["happiness"] -= 0.4
            gamestate.states["alert"] = True
            call_animate.set = True
            gamestate.states["alert_reason"] = "Play with me!"
            
        # Check if fox hasn't slept today
        if not gamestate.states["slept_today"]:
            # Decrease sleepiness if not slept today
            gamestate.states["sleepiness"] -= 0.3
            gamestate.states["alert"] = True
            call_animate.set = True
            gamestate.states["alert_reason"] = "Need sleep!"
        
        # Cap stats at 0
        if gamestate.states["health"] < 0:
            gamestate.states["health"] = 0
        if gamestate.states["happiness"] < 0:
            gamestate.states["happiness"] = 0
        if gamestate.states["sleepiness"] < 0:
            gamestate.states["sleepiness"] = 0

def reset_daily_care():
    """Reset daily care flags at midnight"""
    gamestate.states["fed_today"] = False
    gamestate.states["played_today"] = False
    gamestate.states["slept_today"] = False
    gamestate.states["last_daily_care_check"] = time()
    print("Daily care requirements reset")

def update_poop_effects():
    """Update effects of poop on health and happiness"""
    if poopy.set:
        current_time = time()
        poop_time = gamestate.states.get("poop_start_time", current_time)
        poop_duration = current_time - poop_time
        
        # After 2 hours, start decreasing health
        if poop_duration > 2 * 3600:
            # Decrease health every hour after 2 hours
            hours_since_threshold = (poop_duration - 2 * 3600) / 3600
            health_penalty = min(5, int(hours_since_threshold))
            
            # Apply penalties
            if gamestate.states["health"] > health_penalty:
                gamestate.states["health"] = gamestate.states["health"] - health_penalty
                
            # Also affect happiness after 4 hours
            if poop_duration > 4 * 3600:
                happiness_penalty = min(5, int((poop_duration - 4 * 3600) / 3600))
                if gamestate.states["happiness"] > happiness_penalty:
                    gamestate.states["happiness"] = gamestate.states["happiness"] - happiness_penalty
            
            # Set alert if penalties are being applied
            gamestate.states["alert"] = True
            call_animate.set = True
            gamestate.states["alert_reason"] = "Clean me!"

def show_game_over_screen():
    """Display game over screen with stats"""
    # Clear the screen
    oled.fill(0)
    
    # Calculate pet age in days
    current_seconds = time()
    age_seconds = current_seconds - gamestate.states["pet_birth_time"]
    age_days = age_seconds / (24 * 60 * 60)  # Convert seconds to days
    age_days_rounded = round(age_days * 2) / 2  # Round to nearest half day
    
    # Try to get pet name from settings
    pet_name = "Fox"  # Default name
    try:
        import settings
        saved_settings = load_settings()
        if saved_settings and 'name' in saved_settings:
            pet_name = saved_settings['name']
    except:
        pass  # Use default name if settings can't be loaded
    
    # Display game over text
    oled.text("GAME OVER", 30, 5)
    oled.text(f"RIP {pet_name}", 30, 20)
    oled.text(f"Age: {age_days_rounded:.1f} days", 15, 30)
    
    # Display cause of death (may need to split long text)
    cause = gamestate.states["death_cause"]
    if len(cause) > 16:  # If cause is too long for one line
        # Find a space to split at
        split_point = 16
        while split_point > 0 and cause[split_point-1] != ' ':
            split_point -= 1
        if split_point == 0:  # No space found, just split at max length
            split_point = 16
            
        oled.text(f"Cause: {cause[:split_point]}", 5, 40)
        oled.text(f"{cause[split_point:].strip()}", 5, 50)
    else:
        oled.text(f"Cause: {cause}", 5, 40)
    
    # Show restart instruction
    oled.text("Press B to restart", 5, 55)
    
    # Update display
    oled.show()

def load_settings():
    """Load settings from file"""
    try:
        settings_dict = {}
        with open('pet_settings.txt', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    settings_dict[key] = value
        return settings_dict
    except:
        print("Error loading settings")
        return None

def restart_game():
    """Restart the game with a new pet after showing settings screen"""
    global baby
    
    # Clear the screen
    oled.fill(0)
    oled.text("Starting New Pet", 10, 20)
    oled.text("Please wait...", 15, 35)
    oled.show()
    sleep(1)
    
    # Run the settings interface to get new pet name and type
    try:
        import settings
        # Force settings to run (not just check first boot)
        pet_settings = settings.run_settings(i2c, oled)
        
        # Apply settings if returned
        if pet_settings:
            print(f"New pet settings: {pet_settings}")
    except Exception as e:
        print(f"Error running settings: {e}")
    
    # Reset all stats
    gamestate.states["health"] = 10
    gamestate.states["happiness"] = 10
    gamestate.states["sleepiness"] = 10
    gamestate.states["pet_birth_time"] = time()
    gamestate.states["death_cause"] = ""
    
    # Reset animations
    death.set = False
    poopy.set = False
    
    # Reset position to center
    gamestate.states["fox_position"] = 1
    baby = baby_center
    baby.set = True
    
    # Reset daily care tracking
    gamestate.states["fed_today"] = False
    gamestate.states["played_today"] = False
    gamestate.states["slept_today"] = False
    gamestate.states["last_daily_care_check"] = time()
    
    # Reset other states
    gamestate.states["sleeping"] = False
    gamestate.states["feeding_time"] = False
    gamestate.states["alert"] = False
    call_animate.set = False
    
    # Schedule initial events
    poop_event.start(randint(POOP_MIN * 1000, POOP_MAX * 1000))
    tiredness.start(TIREDNESS * 1000)
    hunger_event.start(HUNGER_CHECK_INTERVAL * 1000)
    
    # Show welcome message with pet name
    try:
        saved_settings = load_settings()
        if saved_settings and 'name' in saved_settings:
            pet_name = saved_settings['name']
            heart_status.message = f"Hello {pet_name}!"
            heart_status.popup(oled)
    except:
        heart_status.message = "New fox born!"
        heart_status.popup(oled)
    
    clear()

def apply_pet_type_change(new_pet_type):
    """Apply pet type change immediately by updating all animations"""
    global baby, baby_left, baby_center, baby_right
    global eat, eat_left, eat_center, eat_right
    global babyzzz, babyzzz_left, babyzzz_center, babyzzz_right
    global go_potty, go_potty_left, go_potty_center, go_potty_right
    global butterfly, butterfly_left, butterfly_center, butterfly_right
    global fox_frames_left, fox_frames_right, frames_left, frames_right
    
    print(f"Applying pet type change to {new_pet_type}")
    
    # Update animations based on pet type
    if new_pet_type == "Fox":
        # Set baby animations
        baby_left = fox_baby_left
        baby_center = fox_baby_center
        baby_right = fox_baby_right
        
        # Set eat animations
        eat_left = fox_eat_left
        eat_center = fox_eat_center
        eat_right = fox_eat_right
        
        # Set sleep animations
        babyzzz_left = fox_babyzzz_left
        babyzzz_center = fox_babyzzz_center
        babyzzz_right = fox_babyzzz_right
        
        # Set potty animations
        go_potty_left = fox_potty_left
        go_potty_center = fox_potty_center
        go_potty_right = fox_potty_right
        
        # Set butterfly animations
        butterfly_left = fox_butterfly_left
        butterfly_center = fox_butterfly_center
        butterfly_right = fox_butterfly_right
        
        # Set walking frames
        frames_left = [fox_walk1, fox_walk2, fox_walk3, fox_walk4]
        frames_right = [fox_walk1r, fox_walk2r, fox_walk3r, fox_walk4r]
        
    else:  # Grayhound
        # Set baby animations
        baby_left = grayhound_baby_left
        baby_center = grayhound_baby_center
        baby_right = grayhound_baby_right
        
        # Set eat animations
        eat_left = grayhound_eat_left
        eat_center = grayhound_eat_center
        eat_right = grayhound_eat_right
        
        # Set sleep animations
        babyzzz_left = grayhound_babyzzz_left
        babyzzz_center = grayhound_babyzzz_center
        babyzzz_right = grayhound_babyzzz_right
        
        # Set potty animations
        go_potty_left = grayhound_potty_left
        go_potty_center = grayhound_potty_center
        go_potty_right = grayhound_potty_right
        
        # Set butterfly animations
        butterfly_left = grayhound_butterfly_left
        butterfly_center = grayhound_butterfly_center
        butterfly_right = grayhound_butterfly_right
        
        # Set walking frames - Grayhound has 3 frames, repeat the last one to match Fox's 4 frames
        frames_left = [grayhound_walk1, grayhound_walk2, grayhound_walk3, grayhound_walk3]
        frames_right = [grayhound_walk1r, grayhound_walk2r, grayhound_walk3r, grayhound_walk3r]
    
    # Update the walking frames
    fox_frames_left = frames_left
    fox_frames_right = frames_right
    
    # Update the current animations based on position
    if gamestate.states["fox_position"] == 0:  # Left
        baby = baby_left
        eat = eat_left
        babyzzz = babyzzz_left
        go_potty = go_potty_left
        butterfly = butterfly_left
    elif gamestate.states["fox_position"] == 1:  # Center
        baby = baby_center
        eat = eat_center
        babyzzz = babyzzz_center
        go_potty = go_potty_center
        butterfly = butterfly_center
    else:  # Right
        baby = baby_right
        eat = eat_right
        babyzzz = babyzzz_right
        go_potty = go_potty_right
        butterfly = butterfly_right
    
    print(f"Pet type changed to {new_pet_type}")

def unload_unused_animations():
    """Unload animations that aren't currently visible to free memory"""
    # Only keep the currently visible animations loaded
    if not gamestate.states["butterfly_active"]:
        butterfly_left.unload()
        butterfly_center.unload()
        butterfly_right.unload()
    
    if not gamestate.states["bunny_active"]:
        bunny_animation.unload()
    
    if not gamestate.states["birds_active"]:
        # Clear bird positions list to free memory
        gamestate.states["bird_positions"] = []
    
    # Force garbage collection after unloading
    import gc
    gc.collect()
    print(f"Unused animations unloaded, free memory: {gc.mem_free()}")

def check_for_blank_screen():
    global babyzzz, babyzzz_left, babyzzz_center, babyzzz_right
    global baby, baby_left, baby_center, baby_right
    
    # Check if the screen appears to be blank and fix if needed
    # Sample more points across the screen to better detect blank screens
    sample_points = [
        (24, 24),   # Left area
        (64, 24),   # Center area
        (100, 24),  # Right area
        (64, 40),   # Bottom center
        (32, 32),   # Additional points
        (96, 32),
        (48, 48),
        (80, 48)
    ]
    
    # Count how many points have pixels set
    active_pixels = 0
    for x, y in sample_points:
        if oled.pixel(x, y) == 1:
            active_pixels += 1
    
    # If very few pixels are set, screen might be blank
    if active_pixels <= 1:  # Allow for 1 stray pixel
        print("WARNING: Possible blank screen detected")
        
        # Force a complete screen redraw
        oled.fill(0)  # Clear the screen
        
        # Check if any animation should be active
        if gamestate.states["sleeping"]:
            # In sleep mode, ensure sleep animation is active
            if not babyzzz.set:
                print("Sleep animation should be active but isn't - fixing")
                
                # Explicitly disable all baby animations
                baby_left.set = False
                baby_center.set = False
                baby_right.set = False
                baby.set = False
                
                # Set the correct sleep animation based on position
                current_position = gamestate.states.get("fox_position", 1)  # Default to center if not found
                
                if current_position == 0:  # Left
                    babyzzz = babyzzz_left
                elif current_position == 1:  # Center
                    babyzzz = babyzzz_center
                else:  # Right
                    babyzzz = babyzzz_right
                
                babyzzz.loop(no=-1)  # Set to loop infinitely
                babyzzz.set = True
                
                # Show message about the fix
                heart_status.message = "Fixed sleep animation"
                heart_status.popup(oled)
                clear()
        else:
            # Not sleeping - check if any animation is active
            butterfly_active = gamestate.states.get("butterfly_active", False)
            bunny_active = gamestate.states.get("bunny_active", False)
            
            if not baby.set and not butterfly_active and not bunny_active:
                print("No animations active when they should be - fixing")
                
                # Force a deep refresh
                deep_refresh_animations()
                
                # Show message about the fix
                heart_status.message = "Fixed blank screen"
                heart_status.popup(oled)
                clear()
                
        return True  # Screen was blank
    
    return False  # Screen has content
def deep_refresh_animations():
    """Perform a complete reset of all animation states and redraw everything"""
    global baby, babyzzz, butterfly, bunny_animation, eat, go_potty
    
    print("Performing deep animation refresh")
    
    # Force garbage collection first
    import gc
    gc.collect()
    
    # Reset all animation objects
    baby_left._Animate__current_frame = 0
    baby_center._Animate__current_frame = 0
    baby_right._Animate__current_frame = 0
    babyzzz_left._Animate__current_frame = 0
    babyzzz_center._Animate__current_frame = 0
    babyzzz_right._Animate__current_frame = 0
    butterfly_left._Animate__current_frame = 0
    butterfly_center._Animate__current_frame = 0
    butterfly_right._Animate__current_frame = 0
    bunny_animation._Animate__current_frame = 0
    eat_left._Animate__current_frame = 0
    eat_center._Animate__current_frame = 0
    eat_right._Animate__current_frame = 0
    go_potty_left._Animate__current_frame = 0
    go_potty_center._Animate__current_frame = 0
    go_potty_right._Animate__current_frame = 0
    
    # Reset all animation states
    for anim in [baby_left, baby_center, baby_right, 
                babyzzz_left, babyzzz_center, babyzzz_right,
                butterfly_left, butterfly_center, butterfly_right,
                bunny_animation, eat_left, eat_center, eat_right,
                go_potty_left, go_potty_center, go_potty_right]:
        anim.set = False
        anim._Animate__done = False
    
    # Reset animation state flags
    gamestate.states["butterfly_active"] = False
    gamestate.states["walking_active"] = False
    gamestate.states["bunny_active"] = False
    gamestate.states["birds_active"] = False
    gamestate.states["hide_seek_active"] = False
    gamestate.states["auto_hide_seek_active"] = False
    gamestate.states["feeding_time"] = False
    
    # Clear the screen completely
    oled.fill(0)
    
    # Restore the correct animation based on current state
    if gamestate.states["sleeping"]:
        # In sleep mode, ensure only sleep animation is active
        if gamestate.states["fox_position"] == 0:  # Left
            babyzzz = babyzzz_left
        elif gamestate.states["fox_position"] == 1:  # Center
            babyzzz = babyzzz_center
        else:  # Right
            babyzzz = babyzzz_right
            
        babyzzz.loop(no=-1)  # Set to loop infinitely
        babyzzz.set = True
    else:
        # Not sleeping - restore main bounce animation
        if gamestate.states["fox_position"] == 0:  # Left
            baby = baby_left
        elif gamestate.states["fox_position"] == 1:  # Center
            baby = baby_center
        else:  # Right
            baby = baby_right
            
        baby._Animate__loop_count = -1  # Set to bounce infinitely
        baby._Animate__bouncing = True  # Set bouncing flag
        baby.set = True
    
    # Update the last refresh times
    gamestate.states["last_animation_refresh"] = time()
    gamestate.states["last_deep_refresh"] = time()
    gamestate.states["animation_refresh_timer"] = 0
    
    # Force garbage collection after reset
    gc.collect()
    
    # Show message about the deep refresh
    heart_status.message = "System refreshed"
    heart_status.popup(oled)
    clear()
    
    print(f"Deep animation refresh completed, free memory: {gc.mem_free()}")

def refresh_animations():
    """Refresh animations to ensure they don't get stuck or disappear
    
    This function serves as a workaround for animation issues:
    1. When in sleep mode, ensures only sleep animation is active
    2. When not in sleep mode, ensures the main bounce animation is running
       if no other animations are active
    3. Resets any stuck animations that might be causing blank screens
    """
    global baby, babyzzz
    
    # Check if pet is sleeping
    if gamestate.states["sleeping"]:
        # In sleep mode, ensure only sleep animation is active
        baby.set = False
        
        # Make sure the correct sleep animation is active based on position
        if gamestate.states["fox_position"] == 0:  # Left
            babyzzz = babyzzz_left
        elif gamestate.states["fox_position"] == 1:  # Center
            babyzzz = babyzzz_center
        else:  # Right
            babyzzz = babyzzz_right
            
        # Ensure sleep animation is active and looping
        babyzzz.loop(no=-1)  # Set to loop infinitely
        babyzzz.set = True
        
        # Reset any other animations that might be active
        gamestate.states["butterfly_active"] = False
        butterfly.set = False
        gamestate.states["walking_active"] = False
        gamestate.states["bunny_active"] = False
        bunny_animation.set = False
        gamestate.states["birds_active"] = False
        gamestate.states["bird_positions"] = []
        
        print("Animation refresh: Sleep mode - ensured only sleep animation is active")
    else:
        # Not sleeping - check if any animation is running
        no_animation_active = (
            not gamestate.states["butterfly_active"] and
            not gamestate.states["walking_active"] and
            not gamestate.states["bunny_active"] and
            not gamestate.states["birds_active"] and
            not gamestate.states["hide_seek_active"] and
            not gamestate.states["auto_hide_seek_active"] and
            not gamestate.states["feeding_time"] and
            not go_potty.set
        )
        
        # If no animation is running, ensure the main bounce animation is active
        if no_animation_active and not baby.set:
            # Reset all animations
            babyzzz.set = False
            butterfly.set = False
            bunny_animation.set = False
            
            # Set the correct baby animation based on position
            if gamestate.states["fox_position"] == 0:  # Left
                baby = baby_left
            elif gamestate.states["fox_position"] == 1:  # Center
                baby = baby_center
            else:  # Right
                baby = baby_right
                
            # Ensure baby animation is active and bouncing
            baby._Animate__loop_count = -1  # Set to bounce infinitely
            baby._Animate__bouncing = True  # Set bouncing flag
            baby.set = True
            
            print("Animation refresh: Restored main bounce animation")
        
        # Add validation that something is actually visible
        if not (baby.set or babyzzz.set or butterfly.set or bunny_animation.set or 
                go_potty.set or gamestate.states["birds_active"]):
            # Nothing is visible! Force baby to show
            print("WARNING: No animations visible during refresh, forcing baby animation")
            
            # Set the correct baby animation based on position
            if gamestate.states["fox_position"] == 0:  # Left
                baby = baby_left
            elif gamestate.states["fox_position"] == 1:  # Center
                baby = baby_center
            else:  # Right
                baby = baby_right
                
            baby.set = True
    
    # Update the last refresh time
    gamestate.states["last_animation_refresh"] = time()
    
    # Reset the animation refresh timer
    gamestate.states["animation_refresh_timer"] = 0
    
    # Show a message about the refresh (only occasionally)
    if randint(0, 3) == 0:  # 25% chance to show message
        heart_status.message = "Animation refreshed"
        heart_status.popup(oled)
        clear()

def check_time_of_day():
    """Check the time of day and trigger appropriate behavior"""
    global last_time_message
    
    # Don't trigger during bunny animation to prevent interference
    if gamestate.states["bunny_active"]:
        return
    
    # Get current hour from RTC
    rtc = RTC()
    current_time = rtc.datetime()
    hour = current_time[4]
    
    # Only show a new message if the hour has changed and we're switching to a new time period
    # or if the toolbar is shown (user interaction)
    if hour != last_time_message and gamestate.states["show_toolbar"]:
        time_period = ""
        if 5 <= hour < 12:
            time_period = "morning"
        elif 12 <= hour < 17:
            time_period = "afternoon"
        elif 17 <= hour < 22:
            time_period = "evening"
        else:  # 22-5
            time_period = "night"
            
        # Only show message if time period has changed
        if time_period:
            messages = time_messages[time_period]
            message = messages[randint(0, len(messages) - 1)]
            
            # Display the time-based message
            time_event = Event(name="Time", sprite=call)
            time_event.message = message
            time_event.popup(oled)
            clear()
            print(f"Time message: {message}")
            
            # Update last message time
            last_time_message = hour

def update_gamestate():
    print(gamestate)
    
    # Check for alerts and death conditions
    check_alerts()
    
    # Handle hide and seek game if active
    if gamestate.states["hide_seek_active"]:
        update_hide_seek_game()
        return  # Skip regular animations when game is active
    
    # Handle auto hide and seek animation if active
    if gamestate.states["auto_hide_seek_active"]:
        update_auto_hide_seek()
        return  # Skip regular animations when auto hide and seek is active
    
    # Handle bunny animation if active
    if gamestate.states["bunny_active"]:
        update_bunny_animation()
        # No return statement, so fox animation will continue
    
    # Handle butterfly animation if active
    if gamestate.states["butterfly_active"]:
        update_butterfly_animation()
        return  # Skip regular animations when butterfly is active
    
    # Handle birds animation if active
    if gamestate.states["birds_active"]:
        update_birds_animation()
        # No return statement, so fox animation will continue
        
    # Handle walking animation if active
    if gamestate.states["walking_active"]:
        update_walking_animation()
        return  # Skip regular animations when walking is active
    
    # Update cleaning timer for testing animations
    update_cleaning_timer()
    
    # Check for bunny animation when fox is on the left
    if gamestate.states["fox_position"] == 0:  # Left position
        # 1 in 4 chance to show bunny (1 in 1000 frames, checked only when fox is on left)
        current_time = time()
        time_since_last_bunny = current_time - gamestate.states["last_bunny_time"]
        
        # Only try to show bunny if it's been at least 30 seconds since last appearance
        if (time_since_last_bunny > 30 and  # 30 seconds minimum between appearances
            not gamestate.states["just_cleaned"] and 
            not gamestate.states["butterfly_active"] and 
            not gamestate.states["walking_active"] and
            not gamestate.states["bunny_active"] and
            randint(0, 999) < 250):  # 1 in 4 chance (250/1000)
            start_bunny_animation()
    
    # Set up random butterfly and walking animations (every few minutes)
    # 1 in 2000 chance per frame (about once every ~1.7 minutes at 0.05s per frame)
    if not gamestate.states["just_cleaned"] and not gamestate.states["bunny_active"] and randint(0, 1999) == 0:
        start_butterfly_animation()
    
    # 1 in 3000 chance per frame (about once every ~2.5 minutes at 0.05s per frame)
    if not gamestate.states["just_cleaned"] and not gamestate.states["butterfly_active"] and not gamestate.states["bunny_active"] and randint(0, 2999) == 0:
        direction = randint(0, 1)  # Random direction
        start_walking_animation(direction)
        
    # Random quick naps (1 in 5000 chance per frame, about once every ~4.2 minutes at 0.05s per frame)
    # But only if not already sleeping, not in other animations, and not recently woken up
    if (not gamestate.states["sleeping"] and 
        not gamestate.states["butterfly_active"] and 
        not gamestate.states["walking_active"] and
        not gamestate.states["quick_nap_active"] and
        randint(0, 4999) == 0):
        quick_nap()
        
    # Random birds flying by (1 in 4000 chance per frame, about once every ~3.3 minutes at 0.05s per frame)
    # But only if no other animations are active
    current_time = time()
    time_since_last_birds = current_time - gamestate.states["last_birds_time"]
    if (not gamestate.states["sleeping"] and 
        not gamestate.states["butterfly_active"] and 
        not gamestate.states["walking_active"] and
        not gamestate.states["quick_nap_active"] and
        not gamestate.states["hide_seek_active"] and
        not gamestate.states["auto_hide_seek_active"] and
        not gamestate.states["birds_active"] and
        time_since_last_birds > 180 and  # At least 3 minutes since last birds
        randint(0, 3999) == 0):
        start_birds_animation()
    
    # Random auto hide and seek (1 in 6000 chance per frame, about once every ~5 minutes at 0.05s per frame)
    # But only if no other animations are active
    current_time = time()
    time_since_last_hide_seek = current_time - gamestate.states["last_auto_hide_seek"]
    if (not gamestate.states["sleeping"] and 
        not gamestate.states["butterfly_active"] and 
        not gamestate.states["walking_active"] and
        not gamestate.states["quick_nap_active"] and
        not gamestate.states["hide_seek_active"] and
        not gamestate.states["auto_hide_seek_active"] and
        not gamestate.states["birds_active"] and
        time_since_last_hide_seek > 300 and  # At least 5 minutes since last auto hide and seek
        randint(0, 5999) == 0):
        start_auto_hide_seek()
    
    if gamestate.states["feeding_time"]:
        # IMPORTANT: Explicitly disable ALL sleep animations
        babyzzz_left.set = False
        babyzzz_center.set = False
        babyzzz_right.set = False
        
        start_birds_animation()
        babyzzz.set = False
        baby.set = False
        eat.set = True
        
        # Increment safety counter for eating animation
        if gamestate.states["eating_protected"]:
            gamestate.states["eating_frame_counter"] += 1
            
            # Force end animation if it's been active for too long (200 frames = 10 seconds)
            if gamestate.states["eating_frame_counter"] > 200:
                eat.done = True
                print("Eating animation force-ended due to timeout")
        
        # Only animate once per frame
        eat.animate(oled)
        
        # Check if animation is done
    if eat.done:
        gamestate.states["feeding_time"] = False
        gamestate.states["eating_protected"] = False  # Reset protection flag
        gamestate.states["eating_frame_counter"] = 0  # Reset safety counter
        
        energy_increase.message = "ENERGY + 2"
        energy_increase.popup(oled)
        gamestate.states["health"] = cap_stat(gamestate.states["health"] + 2)
        gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 2)
        
        clear()
        eat.set = False
        baby.set = True
        
        # Start birds animation after feeding to test bird functionality
        start_birds_animation()
        
    if gamestate.states["sleeping"]:
        babyzzz.set = True
        babyzzz.animate(oled)
            
    if go_potty.set:
        # Increment safety counter for potty animation
        if gamestate.states["potty_protected"]:
            gamestate.states["potty_frame_counter"] += 1
            
            # Force end animation if it's been active for too long (200 frames = 10 seconds)
            if gamestate.states["potty_frame_counter"] > 200:
                go_potty.done = True
                print("Potty animation force-ended due to timeout")
        
        go_potty.animate(oled)

    if go_potty.done:
        go_potty.set = False
        gamestate.states["potty_protected"] = False  # Reset protection flag
        gamestate.states["potty_frame_counter"] = 0  # Reset safety counter
        poopy.set = True
        baby.set = True
        
    if baby.set:
        baby.animate(oled)

    if poopy.set:
        poopy.animate(oled)
        # Check for the poop and if there is poop, decrease the health every 2 hours
        if not gamestate.states["unwell"]:
            gamestate.states["unwell"] = True    
            decrease_health.start(TIREDNESS * 1000)  # 2 hours in milliseconds
        
    if death.set:
        death.animate(oled)
    
    if not gamestate.states["tired"]:
        gamestate.states["tired"] = True
        tiredness.start(TIREDNESS * 1000)  # Every 2 hours
    if gamestate.states["sleepiness"] == 0:
        if not go_potty.set:
            baby.set = False
            babyzzz.set = True
            babyzzz.animate(oled)
            
    # Animate call icon if alert is active
    if gamestate.states["alert"] and call_animate.set:
        call_animate.animate(oled)

print("Building toolbar...")
tb = build_toolbar()

# Setup buttons
print("Setting up buttons...")
button_a = Button(2)
button_b = Button(3)
button_x = Button(4)

# Set toolbar index
index = 0

# Set the toolbar
tb.select(index, oled)

# Set up Events
print("Setting up events...")
energy_increase = Event(name="Increase Energy", sprite=heart, value=1)
clock_settings = Event(name="Settings", sprite=clock, value=0)
toilet = Event(name="Toilet", sprite=toilet, value=0)
poop_event = Event(name="poop time", sprite=toilet, callback=poop_check)
poop_event.start(randint(POOP_MIN * 1000, POOP_MAX * 1000))
sleep_time = Event(name="sleep time", sprite=lightbulb, value=1, callback=wakeup)
decrease_health = Event(name="decrease health", callback=unhealthy_environment)
tiredness = Event(name="tiredness", callback=tired)
hunger_event = Event(name="hunger check", sprite=food, callback=hunger_check)
hunger_event.start(HUNGER_CHECK_INTERVAL * 1000)  # Check hunger every hour
quick_nap_event = Event(name="quick nap", sprite=lightbulb, callback=end_quick_nap)
playtime = Event(name="Game", sprite=game)
# New event for status display
heart_status = Event(name="Status", sprite=heart)

print("Setting up animations...")
# Set up all baby animations with bounce effect
# Set loop count and bouncing flag directly for infinite bouncing
baby_left._Animate__loop_count = -1  # Set to bounce infinitely
baby_left._Animate__bouncing = True  # Set bouncing flag
baby_left.speed = 'very slow'

baby_center._Animate__loop_count = -1  # Set to bounce infinitely
baby_center._Animate__bouncing = True  # Set bouncing flag
baby_center.speed = 'very slow'

baby_right._Animate__loop_count = -1  # Set to bounce infinitely
baby_right._Animate__bouncing = True  # Set bouncing flag
baby_right.speed = 'very slow'

# Set up Grayhound animations with bounce effect
# Set loop count and bouncing flag directly for infinite bouncing
grayhound_baby_left._Animate__loop_count = -1  # Set to bounce infinitely
grayhound_baby_left._Animate__bouncing = True  # Set bouncing flag
grayhound_baby_left.speed = 'very slow'

grayhound_baby_center._Animate__loop_count = -1  # Set to bounce infinitely
grayhound_baby_center._Animate__bouncing = True  # Set bouncing flag
grayhound_baby_center.speed = 'very slow'

grayhound_baby_right._Animate__loop_count = -1  # Set to bounce infinitely
grayhound_baby_right._Animate__bouncing = True  # Set bouncing flag
grayhound_baby_right.speed = 'very slow'

# Print debug info
print("Baby animations set up with bounce effect")
print(f"Animation type: {baby_center.animation_type}")
# Add more detailed debug info
print("Adding debug frame counter to track animation")

# Add debug frame counter to main loop
debug_counter = 0
debug_last_frame = 0

# Set the default baby (center) as active
print("Setting baby.set to True to make animation visible")
baby.set = True
print(f"Baby animation active: {baby.set}")

poopy.bounce()
poopy.speed = 'slow'  # Set poop animation to slow speed
eat.loop(no=1)  # Set eat animation to loop only once
eat.speed = 'slow'  # Set eating animation to slow speed
go_potty.speed = 'slow'  # Set potty animation to slow speed
death.loop(no=-1)
death.speed='very slow'

# Set all sleep animations to very slow
babyzzz_left.speed = 'very slow'
babyzzz_center.speed = 'very slow'
babyzzz_right.speed = 'very slow'

call_animate.loop(no=-1)  # Make call animation loop infinitely
poopy.set = False

# Constants for toolbar timer
TOOLBAR_DISPLAY_TIME = 120  # 6 seconds (120 frames at 0.05s per frame)

# Check for first boot and run settings if needed
print("Checking for first boot...")
try:
    import settings
    pet_settings = settings.check_first_boot(i2c, oled)
    if pet_settings:
        print(f"First boot setup completed: {pet_settings}")
        # Apply settings if returned
        if 'name' in pet_settings:
            # Show welcome message with pet name
            heart_status.message = f"Hello {pet_settings['name']}!"
            heart_status.popup(oled)
            clear()
except Exception as e:
    print(f"Error during first boot check: {e}")

print("Starting main game loop...")
# Main Game Loop
while True:
    # Check for death state FIRST, before any other processing
    if death.set:
        # Clear any other animations or states
        baby.set = False
        babyzzz.set = False
        eat.set = False
        poopy.set = False
        go_potty.set = False
        butterfly.set = False
        bunny_animation.set = False
        call_animate.set = False
        
        # Check which death phase we're in
        if not gamestate.states.get("death_animation_shown", False):
            # Phase 1: Show only the skull animation
            oled.fill(0)  # Clear screen
            death.animate(oled)
            
            # Track how long we've shown the skull
            if not gamestate.states.get("death_timer", 0):
                gamestate.states["death_timer"] = 60  # Show skull for 3 seconds (60 frames)
            else:
                gamestate.states["death_timer"] -= 1
                
            # After timer expires or button press, move to stats screen
            if gamestate.states["death_timer"] <= 0 or button_a.is_pressed or button_b.is_pressed or button_x.is_pressed:
                gamestate.states["death_animation_shown"] = True
                gamestate.states["death_screen_shown"] = False
                
            oled.show()
            sleep(0.05)
            continue
        
        elif not gamestate.states.get("death_screen_shown", False):
            # Phase 2: Show the game over screen with stats
            oled.fill(0)  # Clear screen
            show_game_over_screen()
            gamestate.states["death_screen_shown"] = True
            
            oled.show()
            sleep(0.05)
            continue
        
        else:
            # Phase 3: Continue showing stats screen and check for restart
            oled.fill(0)  # Clear screen
            show_game_over_screen()
            
            # Check for restart button
            if button_b.is_pressed:
                sleep(0.2)  # Debounce
                restart_game()
        
        # Skip ALL other game logic
        oled.show()
        sleep(0.05)
        continue
    
    # Reset death flags when not dead
    gamestate.states["death_screen_shown"] = False
    gamestate.states["death_animation_shown"] = False
    gamestate.states["death_timer"] = 0
    
    # Secret button combination for testing death
    if button_a.is_pressed and button_x.is_pressed:
        # Start or continue tracking hold time
        current_time = time()
        
        # Initialize hold timer if not already set
        if not gamestate.states.get("death_combo_timer", 0):
            gamestate.states["death_combo_timer"] = current_time
            gamestate.states["death_combo_warning_shown"] = False
        
        # Calculate how long buttons have been held
        hold_duration = current_time - gamestate.states["death_combo_timer"]
        
        # Show warning after 2 seconds
        if hold_duration > 2 and not gamestate.states.get("death_combo_warning_shown", False):
            heart_status.message = "Testing death..."
            heart_status.popup(oled)
            clear()
            gamestate.states["death_combo_warning_shown"] = True
        
        # Trigger death after 5 seconds
        if hold_duration > 5:
            # Reset the timer
            gamestate.states["death_combo_timer"] = 0
            gamestate.states["death_combo_warning_shown"] = False
            
            # Set death cause for testing
            gamestate.states["death_cause"] = "Testing death"
            
            # Trigger death
            death.set = True
            gamestate.states["death_screen_shown"] = False
            
            # Show message
            oled.fill(0)
            oled.text("Death triggered", 10, 20)
            oled.text("for testing", 20, 35)
            oled.show()
            sleep(1)
    else:
        # Reset the timer if buttons are released
        gamestate.states["death_combo_timer"] = 0
        gamestate.states["death_combo_warning_shown"] = False
    
    key = ' '

    # Handle button presses for hide and seek game
    if gamestate.states["hide_seek_active"]:
        if button_a.is_pressed:
            # Left position guess
            gamestate.states["cancel_count"] = 0  # Reset cancel counter
            check_player_guess(0)  # 0 = left position
        
        elif button_b.is_pressed:
            # Middle position guess
            gamestate.states["cancel_count"] = 0  # Reset cancel counter
            check_player_guess(1)  # 1 = middle position
        
        elif button_x.is_pressed:
            # Either right position guess or cancel
            gamestate.states["cancel_count"] += 1
            if gamestate.states["cancel_count"] >= 3:
                # Exit game after 3 consecutive X presses
                playtime.message = "Game Cancelled"
                playtime.popup(oled)
                clear()
                end_hide_seek_game()
            else:
                # Right position guess
                check_player_guess(2)  # 2 = right position
    else:
        # Regular button handling
        if button_a.is_pressed or button_b.is_pressed or button_x.is_pressed:
            # Show toolbar when any button is pressed
            gamestate.states["show_toolbar"] = True
            gamestate.states["toolbar_timer"] = TOOLBAR_DISPLAY_TIME
        
        if not gamestate.states["cancel"]:
            tb.unselect(index, oled)
            
        if button_a.is_pressed:
            index += 1
            if index == 7:
                index = 0
            gamestate.states["cancel"] = False
            
        if button_x.is_pressed:
            gamestate.states["cancel"] = True
            index = -1
        
        if not gamestate.states["cancel"]:
            tb.select(index, oled)

        if button_b.is_pressed:
            do_toolbar_stuff()
    
    # Update toolbar timer
    if gamestate.states["toolbar_timer"] > 0:
        gamestate.states["toolbar_timer"] -= 1
        if gamestate.states["toolbar_timer"] == 0:
            gamestate.states["show_toolbar"] = False
    
    # Check for personality features
    trigger_random_event()
    trigger_reflection()
    check_time_of_day()
    
    # Check daily care requirements and poop effects
    check_daily_care()
    update_poop_effects()
    
    # Draw mountain background first (bottom layer)
    draw_mountain(oled)
    
    # Draw rain effect if active (should appear in front of background but behind fox)
    if gamestate.states["rain_active"]:
        update_rain_effect(oled)
    
    # Update squirrel timers and animation
    update_squirrel_timers()
    
    # Draw squirrel animation if active
    if gamestate.states["squirrel_active"]:
        squirrel_animation.animate(oled)
        # Check if animation is done
        if squirrel_animation.done:
            gamestate.states["squirrel_active"] = False
            squirrel_animation.set = False
            
    # Memory management - run garbage collection periodically
    current_time = time()
    if current_time - gamestate.states["last_gc_time"] > GC_INTERVAL:
        import gc
        gc.collect()
        gamestate.states["last_gc_time"] = current_time
        print(f"Periodic garbage collection performed, free memory: {gc.mem_free()}")
    
    # Memory usage tracking
    if current_time - gamestate.states["last_memory_check"] > MEMORY_CHECK_INTERVAL:
        import gc
        free_mem = gc.mem_free()
        gamestate.states["last_memory_check"] = current_time
        
        # Initialize lowest memory if not set
        if gamestate.states["lowest_memory"] == 0:
            gamestate.states["lowest_memory"] = free_mem
        
        # Track lowest memory seen
        if free_mem < gamestate.states["lowest_memory"]:
            gamestate.states["lowest_memory"] = free_mem
            print(f"New lowest memory: {free_mem} bytes")
        
        # Warning if memory is low
        if free_mem < MEMORY_WARNING_THRESHOLD:
            print(f"WARNING: Low memory: {free_mem} bytes")
            # Force more aggressive cleanup
            unload_unused_animations()
    
    # Check for blank screen periodically
    if current_time - gamestate.states["last_blank_check"] > BLANK_SCREEN_CHECK_INTERVAL:
        gamestate.states["last_blank_check"] = current_time
        check_for_blank_screen()
    
    # Deep refresh check
    if current_time - gamestate.states["last_deep_refresh"] > DEEP_REFRESH_INTERVAL:
        deep_refresh_animations()
    
    # Update animation refresh timer and check if refresh is needed
    gamestate.states["animation_refresh_timer"] += 1
    frames_since_refresh = gamestate.states["animation_refresh_timer"]
    seconds_since_refresh = frames_since_refresh * 0.05  # 0.05 seconds per frame
    
    # Check if it's time to refresh animations (every 30 minutes)
    if seconds_since_refresh >= ANIMATION_REFRESH_INTERVAL:
        refresh_animations()
    
    # Update animations (middle layer)
    update_gamestate()
    
    # Animation debugging removed
    
    # Draw the grass layer (top layer)
    draw_grass(oled)
    
    # Draw ears after grass but before toolbar/clock
    # This makes the ears appear to be sticking out from within the grass
    draw_ears(oled)
    
    # Draw either toolbar or clock based on state
    if gamestate.states["show_toolbar"]:
        # Draw toolbar
        tb.show(oled)
    else:
        # Draw clock and age
        draw_clock_and_age(oled)
    
    # Update display with error handling
    try:
        oled.show()
    except OSError as e:
        print(f"Display error: {e}")
        # Wait a bit longer to allow I2C bus to recover
        sleep(0.2)
    
    sleep(0.05)
