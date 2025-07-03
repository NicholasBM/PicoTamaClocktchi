# main.py - Runs automatically on Raspberry Pi Pico boot
import time

print("Starting PicoTamachibi...")
print("Initializing system...")

# Small delay to ensure all hardware is ready
time.sleep(1)

try:
    print("Loading final PicoTamachibi with all improvements...")
    
    # Try to import the final version with all improvements
    import final_picotamachibi
    
    print("Final PicoTamachibi loaded successfully!")
    
except Exception as e:
    error_msg = f"Error loading final PicoTamachibi: {e}"
    print(error_msg)
    
    print("Attempting to load enhanced version as fallback...")
    
    try:
        # Try to import the enhanced version as fallback
        import enhanced_picotamachibi
        
        print("Enhanced PicoTamachibi loaded successfully as fallback!")
        
    except Exception as e2:
        error_msg = f"Error loading enhanced PicoTamachibi: {e2}"
        print(error_msg)
        
        print("Failed to load PicoTamachibi. Please check your installation.")
        
        # Flash an error pattern on the Pico's built-in LED if available
        try:
            from machine import Pin
            led = Pin(25, Pin.OUT)  # Pico's built-in LED
            
            # Flash SOS pattern
            for _ in range(3):
                for _ in range(3):  # Short flashes (S)
                    led.value(1)
                    time.sleep(0.2)
                    led.value(0)
                    time.sleep(0.2)
                time.sleep(0.4)
                
                for _ in range(3):  # Long flashes (O)
                    led.value(1)
                    time.sleep(0.6)
                    led.value(0)
                    time.sleep(0.2)
                time.sleep(0.4)
                
                for _ in range(3):  # Short flashes (S)
                    led.value(1)
                    time.sleep(0.2)
                    led.value(0)
                    time.sleep(0.2)
                time.sleep(1)
        except Exception as e3:
            print(f"LED error indication failed: {e3}")
