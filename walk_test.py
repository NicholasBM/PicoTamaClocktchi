# Simple test file for fox walking animation
from machine import I2C, Pin
from gui.ssd1306 import SSD1306_I2C
from fixed_icon import Animate, Icon, Button
from time import sleep

print("Starting Fox Walking Animation Test...")

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

# Load individual fox walking frames
print("Loading fox walking animation frames...")
fox_walk1 = Icon(BITMAP_PATH + 'fox_walk1.pbm', width=48, height=48, name="fox_walk1")
fox_walk2 = Icon(BITMAP_PATH + 'fox_walk2.pbm', width=48, height=48, name="fox_walk2")
fox_walk3 = Icon(BITMAP_PATH + 'fox_walk3.pbm', width=48, height=48, name="fox_walk3")
fox_walk4 = Icon(BITMAP_PATH + 'fox_walk4.pbm', width=48, height=48, name="fox_walk4")

# Store frames in a list for easy access
fox_frames = [fox_walk1, fox_walk2, fox_walk3, fox_walk4]

# Setup buttons
print("Setting up buttons...")
button_a = Button(2)  # Left
button_b = Button(3)  # Center/Action
button_x = Button(4)  # Right

# Variables for animation
walking_active = False
walking_direction = 0  # 0=left, 1=right
fox_x_position = 40  # Start at center
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
        fox_x_position = 40  # Always start from center
        movement_counter = 0
        frame_index = 0  # Reset animation frame
        
        print(f"Starting walking animation: direction={'left' if direction==0 else 'right'}")

def update_walking():
    """Update the fox walking animation"""
    global walking_active, fox_x_position, movement_counter, frame_index
    
    if walking_active:
        # AGGRESSIVE CLEARING - Clear the entire screen except instructions
        oled.fill_rect(0, 0, 128, 48, 0)
        
        # Update position based on direction
        if walking_direction == 0:  # Walking left
            fox_x_position -= 5  # Move left by 5 pixels (more noticeable)
            print(f"MOVING LEFT: {fox_x_position}")
            
            if fox_x_position <= 0:  # Reached left edge
                end_walking()
                print("Reached left edge")
                return
        else:  # Walking right
            fox_x_position += 5  # Move right by 5 pixels (more noticeable)
            print(f"MOVING RIGHT: {fox_x_position}")
            
            if fox_x_position >= 80:  # Reached right edge
                end_walking()
                print("Reached right edge")
                return
        
        # Draw position indicator at top of screen
        oled.fill_rect(fox_x_position + 24, 0, 5, 5, 1)  # Small white dot above fox
        
        # Cycle to next animation frame every few steps
        if movement_counter % 3 == 0:  # Change frame every 3 position updates
            frame_index = (frame_index + 1) % 4
        
        # Draw the current frame at the current position
        oled.blit(fox_frames[frame_index].image, fox_x_position, 9)  # Moved up by 10 pixels
        
        # Increment movement counter
        movement_counter += 1
        
        # Print position and frame for debugging
        print(f"Fox position: {fox_x_position}, Frame: {frame_index}")

def end_walking():
    """End the fox walking animation"""
    global walking_active
    
    walking_active = False
    
    # Show message about new position
    if walking_direction == 0:  # Left
        oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
        oled.text("Moved to left!", 0, 0)
    else:  # Right
        oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
        oled.text("Moved to right!", 0, 0)

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
            fox_x_position = 40
            frame_index = 0  # Reset to first frame
            
            # Draw the fox at the center position
            oled.blit(fox_frames[frame_index].image, fox_x_position, 9)  # Moved up by 10 pixels
            
            oled.fill_rect(0, 0, 128, 16, 0)  # Clear message area
            oled.text("Reset to center", 0, 0)
            draw_instructions()
    
    # Update walking animation
    update_walking()
    
    # Draw instructions
    draw_instructions()
    
    # Update display
    oled.show()
    
    # Short delay
    sleep(0.05)
