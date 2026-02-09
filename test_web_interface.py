# Quick test script for web interface
# Run this on your computer (not the Pico) to test the web interface

import requests
import time

# Replace with your Pico's IP address
PICO_IP = "192.168.1.100"  # Change this!
PORT = 8082

BASE_URL = f"http://{PICO_IP}:{PORT}"

def test_connection():
    """Test if we can connect to the Pico"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        if response.status_code == 200:
            print("✅ Connection successful!")
            return True
        else:
            print(f"❌ Connection failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_status():
    """Test the status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print("\n📊 Pet Status:")
            print(f"  Name: {data['name']}")
            print(f"  Type: {data['type']}")
            print(f"  Health: {data['health']}/10")
            print(f"  Happiness: {data['happiness']}/10")
            print(f"  Sleepiness: {data['sleepiness']}/10")
            print(f"  Age: {data['age']} days")
            print(f"  Sleeping: {data['sleeping']}")
            print(f"  God Mode: {data['god_mode']}")
            return True
        else:
            print(f"❌ Status request failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status request failed: {e}")
        return False

def test_display():
    """Test the display endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/display", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"\n🖥️  Display Data:")
            print(f"  Width: {data['width']}")
            print(f"  Height: {data['height']}")
            print(f"  Pixels: {len(data['pixels'])} bytes")
            return True
        else:
            print(f"❌ Display request failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Display request failed: {e}")
        return False

def test_button(button):
    """Test sending a button press"""
    try:
        response = requests.post(f"{BASE_URL}/button/{button}", timeout=2)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Button {button} pressed: {data}")
            return True
        else:
            print(f"❌ Button request failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Button request failed: {e}")
        return False

def main():
    print("=" * 50)
    print("PicoTamachibi Web Interface Test")
    print("=" * 50)
    print(f"\nTesting connection to {BASE_URL}")
    print("Make sure your Pico is in Web Mode!\n")
    
    # Test connection
    if not test_connection():
        print("\n⚠️  Could not connect to Pico.")
        print("Make sure:")
        print("  1. Pico is in Web Mode")
        print("  2. You're on the same WiFi network")
        print("  3. PICO_IP is set correctly in this script")
        return
    
    # Test status
    time.sleep(0.5)
    test_status()
    
    # Test display
    time.sleep(0.5)
    test_display()
    
    # Test buttons
    print("\n🎮 Testing Buttons:")
    print("(Watch your Pico screen for button presses)")
    time.sleep(1)
    
    for button in ['A', 'B', 'X']:
        print(f"\nTesting button {button}...")
        test_button(button)
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("✅ All tests complete!")
    print("=" * 50)
    print(f"\nOpen in browser: {BASE_URL}")

if __name__ == "__main__":
    main()
