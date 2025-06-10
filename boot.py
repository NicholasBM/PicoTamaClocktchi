# boot.py - Runs on boot before main.py
import gc
import machine
import time

print("PicoTamachibi Boot Sequence")
print("==========================")

# Initialize hardware
print("Initializing hardware...")

# Set CPU frequency to maximum for best performance
try:
    machine.freq(133000000)  # 133 MHz
    print(f"CPU frequency set to {machine.freq() / 1000000} MHz")
except:
    print("Could not set CPU frequency")

# Run garbage collection to free up memory
print("Cleaning memory...")
gc.collect()
print(f"Free memory: {gc.mem_free()} bytes")

# Small delay to allow hardware to stabilize
time.sleep(0.5)

print("Boot sequence complete")
print("==========================")
