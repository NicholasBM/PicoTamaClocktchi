# Bunny animation test file
from machine import I2C, Pin
from gui.ssd1306 import SSD1306_I2C
from fixed_icon import Animate, Icon, Button
from time import sleep

print("Starting Bunny Animation Test...")

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

# Create bunny animation
print("Loading bunny animation...")
# Note: The files are named bunny_1.pbm, bunny_2.pbm, etc., but the Animate class
# will automatically find files that start with the base name 'bunny_'
# Bunny images are 32x32 pixels
bunny_animation = Animate(filename=BITMAP_PATH + 'bunny_', width=32, height=32, x=80, y=22)
bunny_animation.speed = 'slow'
bunny_animation.loop(no=2)  # Play twice
bunny_animation.set = False

# Load fox walking frames for the "look" animation
print("Loading fox walking animation frames...")
fox_walk1 = Icon(BITMAP_PATH + 'fox_walk1.pbm', width=48, height=48, name="fox_walk1")
fox_walk2 = Icon(BITMAP_PATH + 'fox_walk2.pbm', width=48, height=48, name="fox_walk2")
fox_walk3 = Icon(BITMAP_PATH + 'fox_walk3.pbm', width=48, height=48, name="fox_walk3")
fox_walk4 = Icon(BITMAP_PATH + 'fox_walk4.pbm', width=48, height=48, name="fox_walk4")

# Right-facing frames
fox_walk1r = Icon(BITMAP_PATH + 'fox_walk1r.pbm', width=48, height=48, name="fox_walk1r")
fox_walk2r = Icon(BITMAP_PATH + 'fox_walk2r.pbm', width=48, height=48, name="fox_walk2r")
fox_walk3r = Icon(BITMAP_PATH + 'fox_walk3r.pbm', width=48, height=48, name="fox_walk3r")
fox_walk4r = Icon(BITMAP_PATH + 'fox_walk4r.pbm', width=48, height=48, name="fox_walk4r")

# Store frames in lists for easy access
fox_frames_left = [fox_walk1, fox_walk2, fox_walk3, fox_walk4]
fox_frames_right = [fox_walk1r, fox_walk2r, fox_walk3r, fox_walk4r]

# Setup buttons
print("Setting up buttons...")
button_a = Button(2)  # Left
button_b = Button(3)  # Center/Action
button_x = Button(4)  # Right

# Variables for animation
fox_position = 0  # 0=left, 1=center, 2=right
fox_x_position = 0  # Start at left
walking_active = False
walking_direction = 1  # 0=left, 1=right
movement_counter = 0  # Counter for animation frames
frame_index = 0  # Current animation frame index
bunny_active = False
bunny_done = False

def clear_screen():
    """Clear the entire screen"""
    oled.fill(0)

def draw_instructions():
    """Draw instructions at the bottom of the screen"""
    oled.fill_rect(0, 48, 128, 16, 0)  # Clear instruction area
    oled.text("A:Fox Left B:Bunny X:Fox Right", 0, 56)

def start_bunny_animation():
    """Start the bunny animation"""
    global bunny_active, bunny_done
    
    if not bunny_active and fox_position == 0:  # Only start if fox is on left
        bunny_active = True
        bunny_done = False
        bunny_animation.set = True
        print("Starting bunny animation")

def update_bunny_animation():
    """Update the bunny animation"""
    global bunny_active, bunny_done
    
    if bunny_active:
        # Animate the bunny
        bunny_animation.animate(oled)
        
        # Check if animation is done
        if bunny_animation.done:
            bunny_active = False
            bunny_animation.set = False
            # Reset animation state to prevent getting stuck
            bunny_animation.__current_frame = 0
            bunny_done = True
            print("Bunny animation completed")

def start_walking_animation(direction):
    """Start the fox walking animation
    direction: 0=left, 1=right"""
    global walking_active, walking_direction, fox_x_position, movement_counter, frame_index
    
    if not walking_active:
        walking_active = True
        walking_direction = direction
        
        # Set starting position based on current fox position
        if fox_position == 0:  # Left
            fox_x_position = 0
        elif fox_position == 1:  # Center
            fox_x_position = 48
        else:  # Right
            fox_x_position = 80
            
        frame_index = 0  # Reset animation frame
        movement_counter = 0  # Reset movement counter
        
        print(f"Starting walking animation: direction={'left' if direction==0 else 'right'}, from position {fox_position}")

def update_walking_animation():
    """Update the fox walking animation"""
    global walking_active, fox_x_position, movement_counter, frame_index, fox_position
    
    if walking_active:
        # Clear the animation area
        oled.fill_rect(0, 0, 128, 48, 0)
        
        # Update position based on direction
        if walking_direction == 0:  # Walking left
            fox_x_position -= 3  # Move left by 3 pixels
            print(f"MOVING LEFT: {fox_x_position}")
            
            # Determine target position based on starting position
            if fox_position == 2:  # Started from right
                # Walking to center
                if fox_x_position <= 48:  # Reached center
                    fox_position = 1  # Update position to center
                    end_walking_animation()
                    return
            else:  # Started from center
                # Walking to left
                if fox_x_position <= 0:  # Reached left edge
                    fox_position = 0  # Update position to left
                    end_walking_animation()
                    return
                
            # Use left-facing frames
            frames = fox_frames_left
            
        else:  # Walking right
            fox_x_position += 3  # Move right by 3 pixels
            print(f"MOVING RIGHT: {fox_x_position}")
            
            # Determine target position based on starting position
            if fox_position == 0:  # Started from left
                # Walking to center
                if fox_x_position >= 48:  # Reached center
                    fox_position = 1  # Update position to center
                    end_walking_animation()
                    return
            else:  # Started from center
                # Walking to right
                if fox_x_position >= 80:  # Reached right edge
                    fox_position = 2  # Update position to right
                    end_walking_animation()
                    return
                
            # Use right-facing frames
            frames = fox_frames_right
        
        # Position indicator removed
        
        # Increment movement counter
        movement_counter += 1
        
        # Cycle to next animation frame every few steps
        if movement_counter % 3 == 0:  # Change frame every 3 position updates
            frame_index = (frame_index + 1) % 4
        
        # Draw the current frame at the current position
        oled.blit(frames[frame_index].image, fox_x_position, 9)
        
        # Print position and frame for debugging
        print(f"Fox position: {fox_x_position}, Frame: {frame_index}, Position state: {fox_position}")

def end_walking_animation():
    """End the fox walking animation"""
    global walking_active
    walking_active = False
    
    # Show position message
    if fox_position == 0:
        oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
        oled.text("Fox on left", 0, 0)
    elif fox_position == 1:
        oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
        oled.text("Fox in center", 0, 0)
    else:
        oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
        oled.text("Fox on right", 0, 0)
    
    print(f"Walking animation ended at position {fox_position}")

# Main loop
print("Starting main loop...")
clear_screen()
draw_instructions()

# Start with fox on left
fox_position = 0
fox_x_position = 0

# Draw initial fox position
oled.blit(fox_frames_left[0].image, fox_x_position, 9)
oled.text("Fox on left", 0, 0)
oled.show()

while True:
    # Handle button presses
    if button_a.is_pressed:
        if not walking_active and not bunny_active:
            if fox_position != 0:  # If not already on left
                start_walking_animation(0)  # Start walking left
    
    if button_x.is_pressed:
        if not walking_active and not bunny_active:
            if fox_position != 2:  # If not already on right
                start_walking_animation(1)  # Start walking right
    
    if button_b.is_pressed:
        if not walking_active and not bunny_active:
            start_bunny_animation()
    
    # Check if bunny animation is done and fox needs to walk back to center
    if bunny_done and fox_position == 0 and not walking_active:
        bunny_done = False
        sleep(1)  # Wait a second before walking back
        start_walking_animation(1)  # Walk right to center
    
    # Update animations
    if walking_active:
        update_walking_animation()
    elif bunny_active:
        update_bunny_animation()
    else:
        # Draw the fox in its current position when not animating
        oled.fill_rect(0, 9, 128, 48, 0)  # Clear animation area
        if fox_position == 0:
            oled.blit(fox_frames_left[0].image, 0, 9)
        elif fox_position == 1:
            oled.blit(fox_frames_left[0].image, 48, 9)
        else:
            oled.blit(fox_frames_right[0].image, 80, 9)
    
    # Draw instructions
    draw_instructions()
    
    # Update display
    oled.show()
    
    # Short delay
    sleep(0.05)
