# Settings module for PicoTamachibi
# Handles time setup, pet naming, and pet selection

from machine import I2C, Pin, RTC
from gui.ssd1306 import SSD1306_I2C
from fixed_icon import Button
from time import sleep, time
import os

class Settings:
    def __init__(self, i2c, oled):
        """Initialize settings with the given I2C and OLED display"""
        self.i2c = i2c
        self.oled = oled
        self.button_a = Button(2)  # Left
        self.button_b = Button(3)  # Center/Action
        self.button_x = Button(4)  # Right
        
        # Settings variables
        self.hour = 12
        self.minute = 0
        self.am_pm = "AM"
        self.pet_name = "    "  # Start with 4 spaces
        self.pet_type = "Fox"  # Fox or Grayhound
        
        # Settings state
        self.current_page = 0  # 0=time, 1=name, 2=pet type, 3=confirm
        self.current_field = 0  # Field index within current page
        self.settings_complete = False
        self.hold_timer = 0  # Timer for button holds
        
        # Character selection for naming
        self.available_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
        self.char_index = 0
        self.name_position = 0
        self.max_name_length = 4  # Limit to 4 letters
        
        # Load settings if they exist
        self.load_settings()
        
        # Ensure pet name is exactly 4 characters
        if len(self.pet_name) != 4:
            self.pet_name = self.pet_name[:4].ljust(4)
    
    def clear_screen(self):
        """Clear the entire screen"""
        self.oled.fill(0)
    
    def show_screen(self):
        """Update the display - call this once after all drawing is complete"""
        self.oled.show()
        sleep(0.05)  # Small delay to reduce flickering
    
    def draw_header(self, title):
        """Draw a header with the given title"""
        self.oled.fill_rect(0, 0, 128, 16, 1)  # White background
        self.oled.text(title, 5, 4, 0)  # Black text
        self.oled.hline(0, 16, 128, 1)  # Horizontal line
    
    def draw_footer(self, left_text, center_text, right_text):
        """Draw footer with button labels"""
        self.oled.hline(0, 54, 128, 1)  # Horizontal line
        self.oled.text(left_text, 0, 56, 1)  # A button
        
        # Center the center text
        center_x = 64 - (len(center_text) * 4) // 2
        self.oled.text(center_text, center_x, 56, 1)  # B button
        
        # Right-align the right text
        right_x = 128 - len(right_text) * 8
        self.oled.text(right_text, right_x, 56, 1)  # X button
    
    def draw_progress(self):
        """Draw progress indicator"""
        total_pages = 4  # Time, Name, Pet Type, Confirm
        
        # Draw small dots for each page
        for i in range(total_pages):
            if i == self.current_page:
                # Current page - filled circle
                self.oled.fill_rect(56 + i*8, 46, 4, 4, 1)
            else:
                # Other pages - empty circle
                self.oled.rect(56 + i*8, 46, 4, 4, 1)
    
    def draw_time_setup(self):
        """Draw the time setup page"""
        self.clear_screen()
        self.draw_header("Set Time")
        
        # Draw time fields
        hour_str = f"{self.hour:2d}"
        minute_str = f"{self.minute:02d}"
        
        # Draw time in large format
        self.oled.text(hour_str, 40, 25, 1)
        self.oled.text(":", 56, 25, 1)
        self.oled.text(minute_str, 64, 25, 1)
        self.oled.text(self.am_pm, 88, 25, 1)
        
        # Highlight current field
        if self.current_field == 0:  # Hour
            self.oled.rect(38, 23, 16, 12, 1)
        elif self.current_field == 1:  # Minute
            self.oled.rect(62, 23, 16, 12, 1)
        else:  # AM/PM
            self.oled.rect(86, 23, 16, 12, 1)
        
        self.draw_progress()
        
        # Update footer based on current field
        if self.current_field == 2:  # AM/PM field
            self.draw_footer("Next", "Change", "Back")
        else:
            self.draw_footer("Next", "Change", "Back")
            
        self.show_screen()
    
    def draw_name_setup(self):
        """Draw the pet naming page"""
        self.clear_screen()
        self.draw_header("Name Your Pet")
        
        # Calculate center position for the name
        name_x = 64 - (self.max_name_length * 4)
        
        # Draw name boxes (4 characters)
        for i in range(self.max_name_length):
            # Draw box for each character position
            box_x = name_x + (i * 8)
            if i == self.name_position:
                # Highlight current position
                self.oled.fill_rect(box_x, 25, 8, 12, 1)
                # Draw character in inverse color if it exists
                if i < len(self.pet_name) and self.pet_name[i] != ' ':
                    self.oled.text(self.pet_name[i], box_x, 27, 0)
            else:
                # Draw character normally
                if i < len(self.pet_name) and self.pet_name[i] != ' ':
                    self.oled.text(self.pet_name[i], box_x, 27, 1)
                else:
                    # Draw underscore for empty positions
                    self.oled.hline(box_x, 35, 8, 1)
        
        # Draw current character being selected
        self.oled.text("Select:", 30, 40, 1)
        self.oled.fill_rect(70, 38, 10, 12, 1)  # Highlight box
        self.oled.text(self.available_chars[self.char_index], 72, 40, 0)  # Inverse text
        
        # Draw instructions
        self.oled.text("A:Next B:Select", 20, 48, 1)
        
        self.draw_progress()
        self.draw_footer("Cycle", "Select", "Back")
        self.show_screen()
    
    def draw_pet_setup(self):
        """Draw the pet type selection page"""
        self.clear_screen()
        self.draw_header("Select Pet Type")
        
        # Draw pet options
        self.oled.text("Fox", 30, 25, 1)
        self.oled.text("Grayhound", 30, 35, 1)
        
        # Highlight current selection
        if self.pet_type == "Fox":
            self.oled.fill_rect(20, 25, 8, 8, 1)
            self.oled.text("*", 20, 25, 0)
        else:
            self.oled.fill_rect(20, 35, 8, 8, 1)
            self.oled.text("*", 20, 35, 0)
        
        self.draw_progress()
        self.draw_footer("Next", "Select", "Back")
        self.show_screen()
    
    def draw_confirm_page(self):
        """Draw the confirmation page"""
        self.clear_screen()
        self.draw_header("Confirm Settings")
        
        # Format time for display
        hour_str = f"{self.hour:2d}"
        minute_str = f"{self.minute:02d}"
        time_str = f"{hour_str}:{minute_str} {self.am_pm}"
        
        # Draw settings summary
        self.oled.text("Time: " + time_str, 10, 20, 1)
        self.oled.text("Name: " + self.pet_name.strip(), 10, 30, 1)
        self.oled.text("Pet: " + self.pet_type, 10, 40, 1)
        
        self.draw_progress()
        self.draw_footer("Back", "Confirm", "Cancel")
        self.show_screen()
    
    def handle_time_input(self):
        """Handle input for time setup page"""
        if self.button_a.is_pressed:
            # Next field
            self.current_field = (self.current_field + 1) % 3
            
            # If we're on the AM/PM field and press Next again, go to next page
            if self.current_field == 0 and self.button_a.is_pressed:
                self.current_page += 1
                self.name_position = 0
                self.char_index = 0
                
            sleep(0.2)  # Debounce
        
        elif self.button_b.is_pressed:
            # Change value of current field
            if self.current_field == 0:  # Hour
                self.hour = (self.hour % 12) + 1  # 1-12
            elif self.current_field == 1:  # Minute
                self.minute = (self.minute + 1) % 60  # 0-59
            else:  # AM/PM
                self.am_pm = "PM" if self.am_pm == "AM" else "AM"
            sleep(0.2)  # Debounce
        
        elif self.button_x.is_pressed:
            # Back - go to previous field or do nothing if at first field
            if self.current_field > 0:
                self.current_field -= 1
            sleep(0.2)  # Debounce
    
    def handle_name_input(self):
        """Handle input for name setup page"""
        if self.button_a.is_pressed:
            # Cycle through characters
            self.char_index = (self.char_index + 1) % len(self.available_chars)
            sleep(0.1)  # Shorter debounce for faster character cycling
        
        elif self.button_b.is_pressed:
            # Select current character and move to next position
            # Update the character at the current position
            name_list = list(self.pet_name)
            name_list[self.name_position] = self.available_chars[self.char_index]
            self.pet_name = ''.join(name_list)
            
            # Move to next position or next page if done
            if self.name_position < self.max_name_length - 1:
                self.name_position += 1
                self.char_index = 0  # Reset character selection
            else:
                # All characters selected, move to next page
                self.current_page += 1
                self.current_field = 0
            
            sleep(0.2)  # Debounce
        
        elif self.button_x.is_pressed:
            # Back - go to previous position or previous page
            if self.name_position > 0:
                self.name_position -= 1
            else:
                # At first position, go back to time page
                self.current_page -= 1
                self.current_field = 2  # Set to AM/PM field on time page
            
            sleep(0.2)  # Debounce
    
    def handle_pet_input(self):
        """Handle input for pet type selection page"""
        if self.button_a.is_pressed:
            # Next page
            self.current_page += 1
            sleep(0.2)  # Debounce
        
        elif self.button_b.is_pressed:
            # Toggle pet type
            self.pet_type = "Grayhound" if self.pet_type == "Fox" else "Fox"
            sleep(0.2)  # Debounce
        
        elif self.button_x.is_pressed:
            # Back - go to previous page
            self.current_page -= 1
            self.name_position = self.max_name_length - 1  # Go to last character of name
            sleep(0.2)  # Debounce
    
    def handle_confirm_input(self):
        """Handle input for confirmation page"""
        if self.button_a.is_pressed:
            # Back - go to previous page
            self.current_page -= 1
            sleep(0.2)  # Debounce
        
        elif self.button_b.is_pressed:
            # Start hold timer for confirmation
            if self.hold_timer == 0:
                self.hold_timer = time()
            
            # Check if button has been held long enough (1 second)
            if time() - self.hold_timer >= 1:
                # Confirm settings
                self.apply_settings()
                self.save_settings()
                self.settings_complete = True
                self.hold_timer = 0
        
        elif self.button_x.is_pressed:
            # Cancel - reset to first page
            self.current_page = 0
            self.current_field = 0
            sleep(0.2)  # Debounce
        
        else:
            # Button released, reset hold timer
            self.hold_timer = 0
    
    def apply_settings(self):
        """Apply the settings to the system"""
        # Set the RTC time
        rtc = RTC()
        
        # Convert 12-hour to 24-hour format
        hour_24 = self.hour
        if self.am_pm == "PM" and self.hour < 12:
            hour_24 += 12
        elif self.am_pm == "AM" and self.hour == 12:
            hour_24 = 0
        
        # Get current date components (year, month, day)
        current_datetime = rtc.datetime()
        year = current_datetime[0]
        month = current_datetime[1]
        day = current_datetime[2]
        
        # Set new time while keeping the date
        rtc.datetime((year, month, day, 0, hour_24, self.minute, 0, 0))
        
        # Clean up pet name (remove trailing spaces)
        self.pet_name = self.pet_name.strip()
    
    def save_settings(self):
        """Save settings to a file"""
        try:
            with open('pet_settings.txt', 'w') as f:
                f.write(f"name={self.pet_name.strip()}\n")
                f.write(f"type={self.pet_type}\n")
                f.write(f"setup_complete=True\n")
        except:
            print("Error saving settings")
    
    def load_settings(self):
        """Load settings from file if it exists"""
        try:
            # Check if settings file exists
            try:
                os.stat('pet_settings.txt')
                file_exists = True
            except:
                file_exists = False
            
            if file_exists:
                with open('pet_settings.txt', 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            if key == 'name':
                                self.pet_name = value.ljust(4)[:4]  # Ensure exactly 4 chars
                            elif key == 'type':
                                self.pet_type = value
        except:
            print("Error loading settings")
    
    def is_first_boot(self):
        """Check if this is the first boot"""
        try:
            # Check if settings file exists
            try:
                os.stat('pet_settings.txt')
                file_exists = True
            except:
                file_exists = False
            
            if file_exists:
                with open('pet_settings.txt', 'r') as f:
                    for line in f:
                        if line.startswith('setup_complete=True'):
                            return False
            return True
        except:
            return True
    
    def run(self):
        """Run the settings interface"""
        self.settings_complete = False
        
        # Initialize name to 4 spaces
        self.pet_name = "    "
        self.name_position = 0
        self.char_index = 0
        
        while not self.settings_complete:
            # Draw current page
            if self.current_page == 0:
                self.draw_time_setup()
                self.handle_time_input()
                
                # Move to next page if A is pressed on AM/PM field
                if self.button_a.is_pressed and self.current_field == 2:
                    self.current_page += 1
                    self.current_field = 0
                    sleep(0.2)  # Debounce
            
            elif self.current_page == 1:
                self.draw_name_setup()
                self.handle_name_input()
            
            elif self.current_page == 2:
                self.draw_pet_setup()
                self.handle_pet_input()
            
            elif self.current_page == 3:
                self.draw_confirm_page()
                self.handle_confirm_input()
                
                # Draw hold progress if button is being held
                if self.hold_timer > 0:
                    elapsed = time() - self.hold_timer
                    if elapsed < 1:  # Less than 1 second
                        # Draw progress bar
                        progress = int(elapsed * 100)
                        bar_width = int(progress * 0.64)  # Scale to 64 pixels (half screen)
                        self.oled.fill_rect(32, 50, bar_width, 2, 1)
                        self.show_screen()
            
            sleep(0.05)
        
        # Show completion message
        self.clear_screen()
        self.draw_header("Settings Saved")
        self.oled.text("Welcome", 40, 25, 1)
        self.oled.text(self.pet_name.strip() + "!", 40, 35, 1)
        self.show_screen()
        sleep(2)
        
        return {
            'name': self.pet_name.strip(),
            'type': self.pet_type
        }

def run_settings(i2c, oled):
    """Run the settings interface and return the settings"""
    settings = Settings(i2c, oled)
    return settings.run()

def check_first_boot(i2c, oled):
    """Check if this is the first boot and run settings if needed"""
    settings = Settings(i2c, oled)
    if settings.is_first_boot():
        return settings.run()
    return None
