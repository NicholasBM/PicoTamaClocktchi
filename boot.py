# boot.py - Runs on every boot (before main.py)
# This file sets up the basic system configuration for Enhanced PicoTamachibi

import gc
import time

print("🔧 Enhanced PicoTamachibi boot sequence starting...")

# Enable garbage collection - important for memory management
gc.enable()
print("✓ Garbage collection enabled")

# Set up memory management for better performance
gc.threshold(4096)  # Trigger GC when 4KB of allocations occur
print("✓ Garbage collection threshold set")

# Small delay to let system stabilize
time.sleep(0.5)

# Print memory info
print(f"✓ Free memory: {gc.mem_free()} bytes")

print("✓ Boot sequence complete")
print("🐾 Starting Enhanced PicoTamachibi...")
