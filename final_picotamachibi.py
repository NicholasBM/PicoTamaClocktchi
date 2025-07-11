# final_picotamachibi.py - Final version with all features integrated
# This version includes all test features: birds, bunny, baby position, and walking

# Import the enhanced version as the base
from enhanced_picotamachibi import *

# Import the LogManager for better error handling
from LogManager import LogManager, check_animation_health, log_system_state, safe_execute

# Create a log manager instance
logger = LogManager()
logger.log("Final PicoTamachibi with all features started")

# Log initial system state
log_system_state(logger, gamestate, baby, babyzzz)

# Check animation health
check_animation_health(logger, gamestate, baby, babyzzz)

# Override the main game loop with enhanced version
print("Starting enhanced main game loop with all features...")

# Main Game Loop with all features integrated
while True:
    try:
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
                
        # Update animation refresh timer and check if refresh is needed
        gamestate.states["animation_refresh_timer"] += 1
        frames_since_refresh = gamestate.states["animation_refresh_timer"]
        seconds_since_refresh = frames_since_refresh * 0.05  # 0.05 seconds per frame
        
        # Check if it's time to refresh animations (every 30 minutes)
        if seconds_since_refresh >= ANIMATION_REFRESH_INTERVAL:
            refresh_animations()
            logger.log("Animation refresh performed")
        
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
        
        # Update display with error handling
        try:
            oled.show()
        except OSError as e:
            logger.error(f"Display error: {e}")
            # Wait a bit longer to allow I2C bus to recover
            sleep(0.2)
        
        # Periodically log system state (every ~5 minutes)
        if randint(0, 6000) == 0:  # ~5 minutes at 0.05s per frame
            log_system_state(logger, gamestate, baby, babyzzz)
            check_animation_health(logger, gamestate, baby, babyzzz)
            
        # Flush logs periodically
        if randint(0, 1000) == 0:  # ~50 seconds at 0.05s per frame
            logger.flush()
        
        sleep(0.05)
        
    except Exception as e:
        # Log any exceptions in the main loop
        logger.error(f"Exception in main loop: {e}")
        
        # Try to recover by clearing screen and continuing
        try:
            oled.fill(0)
            oled.text("Error occurred", 10, 20)
            oled.text("Recovering...", 10, 35)
            oled.show()
        except:
            pass
            
        # Force garbage collection
        gc.collect()
        
        # Wait a bit before continuing
        sleep(1)
