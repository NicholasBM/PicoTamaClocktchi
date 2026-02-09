# Diagnostic script for web mode issues
# Run this on your Pico to see what's wrong

print("=" * 40)
print("Web Mode Diagnostic")
print("=" * 40)

# Test 1: Check files exist
print("\n1. Checking files...")
import os
files = os.listdir()
has_simple = 'web_interface_simple.py' in files
has_full = 'web_interface.py' in files

print(f"   web_interface_simple.py: {'✓' if has_simple else '✗'}")
print(f"   web_interface.py: {'✓' if has_full else '✗'}")

if not has_simple and not has_full:
    print("\n   ERROR: No web interface files found!")
    print("   Upload web_interface_simple.py to your Pico")

# Test 2: Check memory
print("\n2. Checking memory...")
import gc
gc.collect()
free_mem = gc.mem_free()
print(f"   Free memory: {free_mem} bytes")
if free_mem < 50000:
    print("   WARNING: Low memory! Restart Pico")
else:
    print("   ✓ Memory OK")

# Test 3: Try importing
print("\n3. Testing import...")
try:
    if has_simple:
        from web_interface_simple import WebInterface
        print("   ✓ web_interface_simple imported OK")
    elif has_full:
        from web_interface import WebInterface
        print("   ✓ web_interface imported OK")
    else:
        print("   ✗ No web interface to import")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    import sys
    sys.print_exception(e)

# Test 4: Check socket
print("\n4. Testing socket...")
try:
    import socket
    print("   ✓ socket module OK")
except Exception as e:
    print(f"   ✗ socket module failed: {e}")

# Test 5: Check network
print("\n5. Checking network...")
try:
    import network
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f"   ✓ Connected to WiFi")
        print(f"   IP: {ip}")
    else:
        print("   ✗ Not connected to WiFi")
        print("   Run connect_wifi_improved() first")
except Exception as e:
    print(f"   ✗ Network check failed: {e}")

# Test 6: Try creating web interface
print("\n6. Testing WebInterface creation...")
try:
    # Need oled and gamestate - check if they exist
    try:
        print(f"   oled exists: {oled is not None}")
        print(f"   gamestate exists: {gamestate is not None}")
        
        if has_simple:
            from web_interface_simple import WebInterface
        elif has_full:
            from web_interface import WebInterface
        
        web = WebInterface(oled, gamestate)
        print("   ✓ WebInterface created OK")
        
        # Try starting (will fail if port in use, but that's OK)
        result = web.start(port=8082)
        if result:
            print("   ✓ Server started OK!")
            print(f"   Try: http://{wlan.ifconfig()[0]}:8082")
            web.stop()
        else:
            print("   ✗ Server failed to start")
            
    except NameError as e:
        print(f"   ✗ Missing variable: {e}")
        print("   Run this after game has started")
        
except Exception as e:
    print(f"   ✗ Test failed: {e}")
    import sys
    sys.print_exception(e)

print("\n" + "=" * 40)
print("Diagnostic complete!")
print("=" * 40)
