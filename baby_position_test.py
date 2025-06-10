# Baby position test file
from machine import I2C, Pin
from gui.ssd1306 import SSD1306_I2C
from fixed_icon import Animate, Icon, Button
from time import sleep

print("Starting Baby Position Test...")

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

# Load fox walking frames
print("Loading fox walking animation frames...")
try:
    # Left-facing frames
    fox_walk1 = Icon(BITMAP_PATH + 'fox_walk1.pbm', width=48, height=48, name="fox_walk1")
    fox_walk2 = Icon(BITMAP_PATH + 'fox_walk2.pbm', width=48, height=48, name="fox_walk2")
    fox_walk3 = Icon(BITMAP_PATH + 'fox_walk3.pbm', width=48, height=48, name="fox_walk3")
    fox_walk4 = Icon(BITMAP_PATH + 'fox_walk4.pbm', width=48, height=48, name="fox_walk4")

    # Right-facing frames
    fox_walk1r = Icon(BITMAP_PATH + 'fox_walk1r.pbm', width=48, height=48, name="fox_walk1r")
    fox_walk2r = Icon(BITMAP_PATH + 'fox_walk2r.pbm', width=48, height=48, name="fox_walk2r")
    fox_walk3r = Icon(BITMAP_PATH + 'fox_walk3r.pbm', width=48, height=48, name="fox_walk3r")
    fox_walk4r = Icon(BITMAP_PATH + 'fox_walk4r.pbm', width=48, height=48, name="fox_walk4r")

    # Store frames in lists
    fox_frames_left = [fox_walk1, fox_walk2, fox_walk3, fox_walk4]
    fox_frames_right = [fox_walk1r, fox_walk2r, fox_walk3r, fox_walk4r]
    print("Successfully loaded all fox frames")
except Exception as e:
    print(f"Error loading fox images: {e}")
    # Fall back to using a single frame if there's an error
    try:
        # Try to load just the first frame
        fox_walk1 = Icon(BITMAP_PATH + 'fox_walk1.pbm', width=48, height=48, name="fox_walk1")
        fox_frames_left = [fox_walk1, fox_walk1, fox_walk1, fox_walk1]
        fox_frames_right = [fox_walk1, fox_walk1, fox_walk1, fox_walk1]
        print("Falling back to single frame animation")
    except Exception as e2:
        print(f"Critical error loading fox images: {e2}")
        # Create empty placeholder if even that fails
        fox_frames_left = []
        fox_frames_right = []

# Create baby animations for different positions
print("Loading baby animations...")
baby_left = Animate(x=0, y=8, width=48, height=48, animation_type="bounce", filename=BITMAP_PATH + 'baby_bounce')
baby_center = Animate(x=48, y=8, width=48, height=48, animation_type="bounce", filename=BITMAP_PATH + 'baby_bounce')
baby_right = Animate(x=80, y=8, width=48, height=48, animation_type="bounce", filename=BITMAP_PATH + 'baby_bounce')

# Set the default baby to center position
baby = baby_center

# Setup buttons
print("Setting up buttons...")
button_a = Button(2)  # Left
button_b = Button(3)  # Center/Action
button_x = Button(4)  # Right

# Variables for animation
walking_active = False
walking_direction = 0  # 0=left, 1=right
fox_x_position = 48  # Start at center
fox_position = 1  # 0=left, 1=center, 2=right
movement_counter = 0  # Counter for animation frames
frame_index = 0  # Current animation frame index

def clear_screen():
    """Clear the entire screen"""
    oled.fill(0)

def draw_instructions():
    """Draw instructions at the bottom of the screen"""
    oled.fill_rect(0, 48, 128, 16, 0)  # Clear instruction area
    oled.text("A:Left B:Reset X:Right", 0, 56)

def start_walking(direction):
    """Start the fox walking animation
    direction: 0=left, 1=right"""
    global walking_active, walking_direction, fox_x_position, movement_counter, frame_index
    
    if not walking_active:
        walking_active = True
        walking_direction = direction
        fox_x_position = 48  # Always start from center
        movement_counter = 0
        frame_index = 0  # Reset animation frame
        
        # Hide baby during walking
        baby.set = False
        
        print(f"Starting walking animation: direction={'left' if direction==0 else 'right'}")

def update_walking():
    """Update the fox walking animation"""
    global walking_active, fox_x_position, movement_counter, frame_index, fox_position
    
    if walking_active:
        # AGGRESSIVE CLEARING - Clear the entire screen except instructions
        oled.fill_rect(0, 0, 128, 48, 0)
        
        # Update position based on direction
        if walking_direction == 0:  # Walking left
            fox_x_position -= 3  # Move left by 3 pixels (slower)
            print(f"MOVING LEFT: {fox_x_position}")
            
            if fox_x_position <= 0:  # Reached left edge
                fox_position = 0  # Update position state
                end_walking()
                print("Reached left edge")
                return
                
            # Use left-facing frames
            frames = fox_frames_left
            
        else:  # Walking right
            fox_x_position += 3  # Move right by 3 pixels (slower)
            print(f"MOVING RIGHT: {fox_x_position}")
            
            if fox_x_position >= 80:  # Reached right edge
                fox_position = 2  # Update position state
                end_walking()
                print("Reached right edge")
                return
                
            # Use right-facing frames
            frames = fox_frames_right
        
        # Draw position indicator at top of screen
        oled.fill_rect(fox_x_position + 24, 0, 5, 5, 1)  # Small white dot above fox
        
        # Increment movement counter
        movement_counter += 1
        
        # Cycle to next animation frame every few steps
        if movement_counter % 3 == 0:  # Change frame every 3 position updates
            frame_index = (frame_index + 1) % 4
        
        # Draw the current frame at the current position
        oled.blit(frames[frame_index].image, fox_x_position, 9)
        
        # Print position and frame for debugging
        print(f"Fox position: {fox_x_position}, Frame: {frame_index}, Position state: {fox_position}")

def end_walking():
    """End the fox walking animation"""
    global walking_active, baby
    
    walking_active = False
    
    # Update baby position based on fox position
    if fox_position == 0:  # Left
        # Use the left-positioned baby animation
        baby = baby_left
        oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
        oled.text("Moved to left!", 0, 0)
    elif fox_position == 1:  # Center
        # Use the center-positioned baby animation
        baby = baby_center
        oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
        oled.text("Reset to center", 0, 0)
    else:  # Right
        # Use the right-positioned baby animation
        baby = baby_right
        oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
        oled.text("Moved to right!", 0, 0)
    
    # Show baby again
    baby.set = True
    
    # Print position based on which baby animation is active
    if baby == baby_left:
        print("Baby position set to left")
    elif baby == baby_center:
        print("Baby position set to center")
    else:  # baby == baby_right
        print("Baby position set to right")

# Set up all baby animations
baby_left.loop(no=-1)  # Loop infinitely
baby_left.speed = 'very slow'

baby_center.loop(no=-1)  # Loop infinitely
baby_center.speed = 'very slow'

baby_right.loop(no=-1)  # Loop infinitely
baby_right.speed = 'very slow'

# Start with center baby active
baby = baby_center
baby.set = True

# Main loop
print("Starting main loop...")
clear_screen()
draw_instructions()

while True:
    # Handle button presses
    if button_a.is_pressed:
        if not walking_active:
            start_walking(0)  # Start walking left
    
    if button_x.is_pressed:
        if not walking_active:
            start_walking(1)  # Start walking right
    
    if button_b.is_pressed:
        # Reset position
        if not walking_active:
            clear_screen()
            fox_position = 1  # Center
            # Use the center-positioned baby animation
            baby = baby_center
            baby.set = True
            
            oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
            oled.text("Reset to center", 0, 0)
            draw_instructions()
    
    # Update walking animation
    update_walking()
    
    # Draw baby animation if active
    if baby.set and not walking_active:
        # Animate the baby (position is now handled by using different baby animations)
        baby.animate(oled)
        
        # Debug output based on which baby animation is active
        if baby == baby_left:
            print(f"Animating baby at left position, fox_position={fox_position}")
        elif baby == baby_center:
            print(f"Animating baby at center position, fox_position={fox_position}")
        else:  # baby == baby_right
            print(f"Animating baby at right position, fox_position={fox_position}")
    
    # Draw instructions
    draw_instructions()
    
    # Update display
    oled.show()
    
    # Short delay
    sleep(0.05)
