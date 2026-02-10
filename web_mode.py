# Web Mode Module - Only loaded when web mode is activated
# This keeps the main file small and saves memory

from time import sleep, time
from random import randint

# Global web interface instance
web_interface = None

def start_web_mode(oled, gamestate, connect_wifi_improved):
    """Start web interface mode - serve web page for remote control"""
    global web_interface
    
    # Connect to WiFi first
    if not connect_wifi_improved():
        oled.fill(0)
        oled.text("WiFi Failed!", 25, 25)
        oled.show()
        sleep(2)
        return False
    
    # Import web interface module (use simple version for memory efficiency)
    try:
        from web_interface_simple import WebInterface
        
        # Create web interface instance
        web_interface = WebInterface(oled, gamestate)
        
        # Start the web server
        if web_interface.start(port=8082):
            gamestate.states["web_mode_active"] = True
            
            # Get IP address
            ip = gamestate.states.get("network_ip", "Unknown")
            ip_parts = ip.split('.')
            
            # Show success message
            oled.fill(0)
            oled.text("WEB MODE ACTIVE", 10, 5)
            oled.text("-" * 16, 0, 15)
            oled.text("Open browser to:", 5, 25)
            oled.text(f"http://{ip_parts[2]}.{ip_parts[3]}:8082", 5, 35)
            oled.text("Press X to stop", 10, 50)
            oled.show()
            
            print(f"Web interface started at http://{ip}:8082")
            return True
        else:
            oled.fill(0)
            oled.text("Web Server", 25, 20)
            oled.text("Failed!", 35, 35)
            oled.show()
            sleep(2)
            return False
            
    except Exception as e:
        print(f"Error starting web mode: {e}")
        oled.fill(0)
        oled.text("Web Mode Error", 15, 25)
        oled.show()
        sleep(2)
        return False

def stop_web_mode(oled, gamestate):
    """Stop web interface mode"""
    global web_interface
    
    if web_interface:
        web_interface.stop()
        web_interface = None
    
    gamestate.states["web_mode_active"] = False
    
    oled.fill(0)
    oled.text("Web Mode", 30, 20)
    oled.text("Stopped", 35, 35)
    oled.show()
    sleep(1)
    
    print("Web mode stopped")

def update_web_mode(oled, gamestate, button_x, baby, baby_left, baby_center, baby_right,
                    eat_left, eat_center, eat_right, babyzzz_left, babyzzz_center, babyzzz_right,
                    poopy, poop_event, POOP_MIN, POOP_MAX, force_wake_up, butterfly):
    """Update web mode - handle incoming requests"""
    global web_interface
    
    if not gamestate.states.get("web_mode_active", False):
        return
    
    # Handle web requests (non-blocking)
    if web_interface:
        web_interface.handle_request()
    
    # Check for X button to exit
    if button_x.is_pressed:
        stop_web_mode(oled, gamestate)
        return
    
    # Check for web actions and execute them
    if gamestate.states.get("web_action_feed", False):
        gamestate.states["web_action_feed"] = False
        # Simulate food button press
        if not gamestate.states.get("sleeping", False):
            # Select the appropriate eat animation based on fox position
            if gamestate.states["fox_position"] == 0:  # Left
                eat = eat_left
            elif gamestate.states["fox_position"] == 1:  # Center
                eat = eat_center
            else:  # Right
                eat = eat_right
            
            # Set up eating animation
            eat._Animate__current_frame = 0
            eat._Animate__done = False
            eat.loop(no=1)
            eat.set = True
            gamestate.states["eating_protected"] = True
            gamestate.states["eating_frame_counter"] = 0
            
            # Wake up if sleeping
            if gamestate.states.get("sleeping", False):
                force_wake_up()
            
            gamestate.states["feeding_time"] = True
            baby.set = False
            
            # Reset last feed time
            gamestate.states["last_feed_time"] = time()
            gamestate.states["is_hungry"] = False
            gamestate.states["hunger_alert_shown"] = False
            gamestate.states["fed_today"] = True
            
            print("Web: Fed pet")
    
    if gamestate.states.get("web_action_sleep", False):
        gamestate.states["web_action_sleep"] = False
        
        # Toggle sleep state
        if gamestate.states.get("sleeping", False):
            # Wake up - restore brightness to lowest and disable night mode
            oled.contrast(1)  # Set brightness to lowest
            oled.invert(False)  # Disable inversion
            gamestate.states["display_inverted"] = False
            
            # Call the wakeup function
            force_wake_up()
            print("Web: Woke up pet")
        else:
            # Put to sleep
            # Force end any active animations
            if gamestate.states.get("butterfly_active", False):
                gamestate.states["butterfly_active"] = False
                butterfly.set = False
                
            if gamestate.states.get("walking_active", False):
                gamestate.states["walking_active"] = False
                
            if gamestate.states.get("quick_nap_active", False):
                gamestate.states["quick_nap_active"] = False
            
            # Disable all baby animations
            baby_left.set = False
            baby_center.set = False
            baby_right.set = False
            baby.set = False
            
            gamestate.states["sleeping"] = True
            
            # Enable night mode
            oled.contrast(1)  # Set brightness to lowest
            oled.invert(True)
            gamestate.states["display_inverted"] = True
            
            # Select appropriate sleep animation
            if gamestate.states["fox_position"] == 0:
                babyzzz = babyzzz_left
            elif gamestate.states["fox_position"] == 1:
                babyzzz = babyzzz_center
            else:
                babyzzz = babyzzz_right
            
            babyzzz.loop(no=-1)
            babyzzz.set = True
            
            print("Web: Put pet to sleep")
    
    if gamestate.states.get("web_action_clean", False):
        gamestate.states["web_action_clean"] = False
        
        # Check if there's poop to clean
        if poopy.set:
            # Clean up poop
            poopy.set = False
            baby.set = True
            
            # Wake up if sleeping
            if gamestate.states.get("sleeping", False):
                force_wake_up()
            
            # Schedule next poop
            poop_event.start(randint(POOP_MIN * 1000, POOP_MAX * 1000))
            
            # Set cleaning flag
            gamestate.states["just_cleaned"] = True
            gamestate.states["cleaning_timer"] = 200
            
            print("Web: Cleaned up poop")
        else:
            # No poop to clean
            print("Web: No poop to clean")
            # Set a flag so the web interface can show "Already clean"
            gamestate.states["web_clean_result"] = "Already clean!"
