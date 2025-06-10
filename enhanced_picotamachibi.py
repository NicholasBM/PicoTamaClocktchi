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

# load icons with corrected paths
print("Loading icons...")
food = Icon(BITMAP_PATH + 'food.pbm', width=16, height=16, name="food")
lightbulb = Icon(BITMAP_PATH + 'lightbulb.pbm', width=16, height=16, name="lightbulb")
game = Icon(BITMAP_PATH + 'game.pbm', width=16, height=16, name="game")
firstaid = Icon(BITMAP_PATH + 'firstaid.pbm', width=16, height=16, name="firstaid")
toilet = Icon(BITMAP_PATH + 'toilet.pbm', width=16, height=16, name="toilet")
heart = Icon(BITMAP_PATH + 'heart.pbm', width=16, height=16, name="heart")
call = Icon(BITMAP_PATH + 'call.pbm', width=16, height=16, name="call")
bubble = Icon(BITMAP_PATH + 'bubble.pbm', width=16, height=16, name="bubble")  # Added bubble icon for reflections
# Load background and ground layers
mountain = Icon(BITMAP_PATH + 'mountain.pbm', width=128, height=10, name="mountain")  # Background mountain
grass = Icon(BITMAP_PATH + 'grass1.pbm', width=32, height=8, name="grass")  # Ground layer

# Set Animations with corrected paths
print("Setting up animations...")
poopy = Animate(x=96, y=40, width=16, height=16, filename=BITMAP_PATH + 'poop')  # Moved up from y=48 to y=40

# Create baby animations for different positions
baby_left = Animate(x=0, y=9, width=48, height=48, animation_type="bounce", filename=BITMAP_PATH + 'baby_bounce')
baby_center = Animate(x=48, y=9, width=48, height=48, animation_type="bounce", filename=BITMAP_PATH + 'baby_bounce')
baby_right = Animate(x=80, y=9, width=48, height=48, animation_type="bounce", filename=BITMAP_PATH + 'baby_bounce')

# Set the default baby to center position
baby = baby_center

# Create eat animations for different positions
eat_left = Animate(x=0, y=9, width=48, height=48, filename=BITMAP_PATH + 'eat')
eat_center = Animate(x=48, y=9, width=48, height=48, filename=BITMAP_PATH + 'eat')
eat_right = Animate(x=80, y=9, width=48, height=48, filename=BITMAP_PATH + 'eat')

# Default eat animation (will be set based on fox position)
eat = eat_center

# Create sleep animations for different positions (moved down by 3px)
babyzzz_left = Animate(x=0, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'baby_zzz')
babyzzz_center = Animate(x=48, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'baby_zzz')
babyzzz_right = Animate(x=80, y=12, width=48, height=48, animation_type="loop", filename=BITMAP_PATH + 'baby_zzz')

# Default sleep animation (will be set based on fox position)
babyzzz = babyzzz_center

death = Animate(x=48, y=8, animation_type='bounce', filename=BITMAP_PATH + "skull")  # Moved up from y=16 to y=8

# Create potty animations for different positions
go_potty_left = Animate(filename=BITMAP_PATH + "potty", animation_type='bounce', x=0, y=9, width=48, height=48)
go_potty_center = Animate(filename=BITMAP_PATH + "potty", animation_type='bounce', x=48, y=9, width=48, height=48)
go_potty_right = Animate(filename=BITMAP_PATH + "potty", animation_type='bounce', x=80, y=9, width=48, height=48)

# Default potty animation (will be set based on fox position)
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

# Butterfly animations for different positions
butterfly_left = Animate(filename=BITMAP_PATH + 'butterfyl', width=48, height=48, x=0, y=8)
butterfly_center = Animate(filename=BITMAP_PATH + 'butterfyl', width=48, height=48, x=48, y=8)
butterfly_right = Animate(filename=BITMAP_PATH + 'butterfyl', width=48, height=48, x=80, y=8)

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

# Default butterfly (will be set based on fox position)
butterfly = butterfly_center

# Bunny animation (only shows on right side when fox is on left)
bunny_animation = Animate(filename=BITMAP_PATH + 'bunny_', width=32, height=32, x=80, y=22)
bunny_animation.speed = 'slow'
bunny_animation.loop(no=2)  # Play twice
bunny_animation.set = False

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

# Store frames in lists for easy access
fox_frames_left = [fox_walk1, fox_walk2, fox_walk3, fox_walk4]
fox_frames_right = [fox_walk1r, fox_walk2r, fox_walk3r, fox_walk4r]

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

# Game Variables
TIREDNESS = 7200 # seconds (2 hours)
POOP_MIN = 1200 # seconds (20 minutes)
POOP_MAX = 7200 # seconds (2 hours)
SLEEP_DURATION = 12 * 60 * 60 # 12 hours in seconds
HUNGER_CHECK_INTERVAL = 3600 # 1 hour in seconds
QUICK_NAP_DURATION = 120 # 2 minutes in seconds
# Thresholds for alerts
CRITICAL_THRESHOLD = 3  # When stats are below this, trigger alert
DEATH_THRESHOLD = 1     # When all stats are at or below this, trigger death

# Helper function to cap stats at maximum value
def cap_stat(value, max_value=10):
    """Cap a stat value at the specified maximum"""
    return min(value, max_value)


def tired():
    gamestate.states["sleepiness"] -= 1
    if gamestate.states["sleepiness"] < 0:
        gamestate.states["sleepiness"] = 0
    tiredness.start(TIREDNESS * 1000)  # Every 2 hours
    
def wakeup():
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
            
        go_potty.loop(no=1)
        baby.set = False
        go_potty.set = True
        print(f"poop time at position {gamestate.states['fox_position']}")
    
def clear():
    """ Clear the screen """
    oled.fill_rect(0,0,128,64,0)

def draw_mountain(display):
    """ Draw mountain across the screen below the time bar """
    display.blit(mountain.image, 0, 16)  # Position just below the time bar

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
    toolbar.additem(firstaid)
    toolbar.additem(toilet)
    toolbar.additem(heart)
    toolbar.additem(call)
    return toolbar

def do_toolbar_stuff():
    global babyzzz  # Move global declaration to the beginning of the function
    
    if tb.selected_item == "food":
        global eat  # Add global declaration for eat
        
        # Wake up if sleeping
        force_wake_up()
        
        gamestate.states["feeding_time"] = True
        baby.set = False
        
        # Reset last feed time to track hunger
        gamestate.states["last_feed_time"] = time()
        gamestate.states["is_hungry"] = False
        gamestate.states["hunger_alert_shown"] = False
        
        # Select the appropriate eat animation based on fox position
        if gamestate.states["fox_position"] == 0:  # Left
            eat = eat_left
        elif gamestate.states["fox_position"] == 1:  # Center
            eat = eat_center
        else:  # Right
            eat = eat_right
            
        eat.set = True
            
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
        # Sleeping
        if not gamestate.states["sleeping"]:
            # Force end any active animations
            if gamestate.states["butterfly_active"]:
                gamestate.states["butterfly_active"] = False
                butterfly.set = False
                butterfly.__current_frame = 0
                
            if gamestate.states["walking_active"]:
                gamestate.states["walking_active"] = False
                
            if gamestate.states["quick_nap_active"]:
                gamestate.states["quick_nap_active"] = False
                
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
            baby.set = False
            
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
            
            gamestate.states["sleeping"] = False
            babyzzz.set = False
            baby.set = True
            sleep_time.message = "Morning"
            sleep_time.popup(oled)
            clear()
            
            # Schedule next poop event after waking up
            poop_event.start(randint(POOP_MIN * 1000, POOP_MAX * 1000))
            
        print("lightbulb")
    if tb.selected_item == "firstaid":
        # Wake up if sleeping
        force_wake_up()
        
        firstaid.message = "Vitamins"
        firstaid.popup(oled)
        gamestate.states["health"] = cap_stat(gamestate.states["health"] + 2)
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
        start_auto_hide_seek()

    if tb.selected_item == "call":
        # Call for help - reset alert and improve stats slightly
        call_animate.set = False
        gamestate.states["alert"] = False
        gamestate.states["health"] = cap_stat(gamestate.states["health"] + 2)
        gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 2)
        gamestate.states["sleepiness"] = cap_stat(gamestate.states["sleepiness"] + 2)
        
        # Display the reason for the alert
        if gamestate.states["alert_reason"]:
            heart_status.message = f"Alert: {gamestate.states['alert_reason']}"
            heart_status.popup(oled)
            gamestate.states["alert_reason"] = ""  # Reset the alert reason
        else:
            # Show the last random message if available, otherwise show "No Alert Active"
            if gamestate.states["last_random_message"]:
                heart_status.message = gamestate.states["last_random_message"]
            else:
                heart_status.message = "No Alert Active"
            heart_status.popup(oled)
        
        clear()
        
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
            
        # Always start walking animation after call function
        # This gives the fox a chance to walk around after being called
        # Choose appropriate direction based on current position
        if gamestate.states["fox_position"] == 0:  # Left edge
            direction = 1  # Move right
        elif gamestate.states["fox_position"] == 2:  # Right edge
            direction = 0  # Move left
        else:  # Center
            direction = randint(0, 1)  # Random direction
        
        # Wake up if sleeping
        force_wake_up()
        
        start_walking_animation(direction)

def unhealthy_environment():
    # Decrease health by 0.7 points per hour (instead of 1 point per 2 hours)
    gamestate.states["health"] -= 0.7
    
    # Check if health is at half and show alert if not already shown
    if gamestate.states["health"] <= 5 and not gamestate.states["poop_alert_shown"]:
        gamestate.states["alert"] = True
        call_animate.set = True
        gamestate.states["alert_reason"] = "Why you no clean?"
        gamestate.states["poop_alert_shown"] = True
    
    # When health reaches half, also decrease happiness
    if gamestate.states["health"] <= 5:
        gamestate.states["happiness"] -= 0.7
    
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
    
    # Check death condition - all stats critically low
    if (gamestate.states["health"] <= DEATH_THRESHOLD and 
        gamestate.states["happiness"] <= DEATH_THRESHOLD and 
        gamestate.states["sleepiness"] <= DEATH_THRESHOLD):
        # If pet wasn't already dead, reset birth time
        if not death.set:
            gamestate.states["pet_birth_time"] = time()  # Reset age counter when pet dies
        death.set = True
    elif gamestate.states["health"] > 0:
        death.set = False

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
    score_event.message = f"U:{gamestate.states['player_score']} F:{gamestate.states['fox_score']}"
    score_event.popup(oled)
    clear()

def end_hide_seek_game():
    """End the hide and seek game and show the final result"""
    gamestate.states["hide_seek_active"] = False
    
    # Determine winner
    if gamestate.states["player_score"] > gamestate.states["fox_score"]:
        playtime.message = "You win!"
        
        # Update last play time
        gamestate.states["last_play_time"] = time()
        
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
    """Start the bunny animation - only shows on right side when fox is on left"""
    # Only start if fox is on left and no other animations are active
    if (gamestate.states["fox_position"] == 0 and  # Fox must be on left
        not gamestate.states["bunny_active"] and
        not gamestate.states["butterfly_active"] and
        not gamestate.states["walking_active"] and
        not gamestate.states["sleeping"] and
        not gamestate.states["quick_nap_active"]):
        
        # Set bunny animation active
        gamestate.states["bunny_active"] = True
        gamestate.states["last_bunny_time"] = time()
        
        # Hide regular baby animation temporarily
        baby.set = False
        
        # Set up bunny animation
        bunny_animation.set = True
        
        print("Starting bunny animation")

def update_bunny_animation():
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
            
            # Determine target position based on starting position
            if gamestate.states["fox_position"] == 2:  # Started from right
                # Walking to center
                if fox_x_position <= 48:  # Reached center
                    gamestate.states["fox_position"] = 1  # Update position to center
                    end_walking_animation()
                    return
            else:  # Started from center
                # Walking to left
                if fox_x_position <= 0:  # Reached left edge
                    gamestate.states["fox_position"] = 0  # Update position to left
                    end_walking_animation()
                    return
                
            # Use left-facing frames
            frames = fox_frames_left
            
        else:  # Walking right
            fox_x_position += 3  # Move right by 3 pixels (slower)
            print(f"MOVING RIGHT: {fox_x_position}")
            
            # Determine target position based on starting position
            if gamestate.states["fox_position"] == 0:  # Started from left
                # Walking to center
                if fox_x_position >= 48:  # Reached center
                    gamestate.states["fox_position"] = 1  # Update position to center
                    end_walking_animation()
                    return
            else:  # Started from center
                # Walking to right
                if fox_x_position >= 80:  # Reached right edge
                    gamestate.states["fox_position"] = 2  # Update position to right
                    end_walking_animation()
                    return
                
            # Use right-facing frames
            frames = fox_frames_right
        
        # Position indicator removed
        
        # Increment movement counter
        fox_movement_counter += 1
        
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
    # Only start if no other animations are active
    if (not gamestate.states["sleeping"] and 
        not gamestate.states["butterfly_active"] and 
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
    
    # Clear the screen
    clear()

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

def trigger_reflection():
    """Trigger a reflection based on pet state with a small chance"""
    # Less frequent than random events (1 in 1500 frames, about once every ~75 seconds at 0.05s per frame)
    # Don't trigger during bunny animation to prevent interference
    if not gamestate.states["bunny_active"] and randint(0, 1499) == 0:
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
            gamestate.states["health"] -= 0.25
            gamestate.states["happiness"] -= 0.25
            
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
        return  # Skip regular animations when bunny is active
    
    # Handle butterfly animation if active
    if gamestate.states["butterfly_active"]:
        update_butterfly_animation()
        return  # Skip regular animations when butterfly is active
    
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
        time_since_last_hide_seek > 300 and  # At least 5 minutes since last auto hide and seek
        randint(0, 5999) == 0):
        start_auto_hide_seek()
    
    if gamestate.states["feeding_time"]:
        babyzzz.set = False
        baby.set = False
        eat.set = True
        # Only animate once per frame
        eat.animate(oled)
        
        # Check if animation is done
        if eat.done:
            gamestate.states["feeding_time"] = False
            energy_increase.message = "ENERGY + 2"
            energy_increase.popup(oled)
            gamestate.states["health"] = cap_stat(gamestate.states["health"] + 2)
            gamestate.states["happiness"] = cap_stat(gamestate.states["happiness"] + 2)
            
            clear()
            eat.set = False
            baby.set = True
        
    if gamestate.states["sleeping"]:
        babyzzz.set = True
        babyzzz.animate(oled)
            
    if go_potty.set:
        go_potty.animate(oled)

    if go_potty.done:
        go_potty.set = False
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
firstaid = Event(name="First Aid", sprite=firstaid, value=0)
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
# Set up all baby animations
baby_left.loop(no=-1)  # Loop infinitely
baby_left.speed = 'very slow'

baby_center.loop(no=-1)  # Loop infinitely
baby_center.speed = 'very slow'

baby_right.loop(no=-1)  # Loop infinitely
baby_right.speed = 'very slow'

# Set the default baby (center) as active
baby.set = True

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

print("Starting main game loop...")
# Main Game Loop
while True:
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
    
    # Draw mountain background first (bottom layer)
    draw_mountain(oled)
    
    # Update animations (middle layer)
    update_gamestate()
    
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
    
    oled.show()
    sleep(0.05)
