# Main entry point for Enhanced PicoTamachibi
# This file automatically runs on device startup

import time
from machine import Pin

def show_startup_info():
    """Show device startup information"""
    print("\n" + "="*40)
    print("🐾 ENHANCED PICO TAMACHIBI 🐾")
    print("="*40)
    print("Device: Raspberry Pi Pico W")
    print("Features:")
    print("- Virtual pet care")
    print("- Wireless pet visits")
    print("- Network discovery")
    print("- OLED display")
    print("- Interactive games")
    print("="*40)

def main():
    """Main entry point"""
    try:
        # Show startup information
        show_startup_info()
        
        # Small delay for system to stabilize
        print("Initializing Enhanced PicoTamachibi...")
        time.sleep(2)
        
        # Import and run the enhanced game
        print("🚀 Starting Enhanced PicoTamachibi...")
        
        # Import the enhanced game (this will start the main game loop)
        import enhanced_picotamachibi
        
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted by user")
        print("Goodbye!")
        
    except ImportError as e:
        print(f"\n💥 Failed to import enhanced_picotamachibi: {e}")
        print("Make sure enhanced_picotamachibi.py is on the device")
        print("Also ensure all required files are present:")
        print("- fixed_icon.py")
        print("- settings.py") 
        print("- wifi_config.py")
        print("- gui/ directory with all bitmap files")
        
        # Flash onboard LED to indicate error
        try:
            led = Pin("LED", Pin.OUT)
            for _ in range(10):
                led.on()
                time.sleep(0.5)
                led.off()
                time.sleep(0.5)
        except:
            pass
        
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Check that all required files are present")
        print("Restarting in 10 seconds...")
        time.sleep(10)
        
        # Try to restart
        try:
            import machine
            machine.reset()
        except:
            print("Manual restart required")

if __name__ == "__main__":
    main()
