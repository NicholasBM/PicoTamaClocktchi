from machine import I2C, Pin
from gui.ssd1306 import SSD1306_I2C
import time

# Define pins
sda = Pin(0)
scl = Pin(1)
i2c_id = 0

# Initialize I2C
i2c = I2C(id=i2c_id, sda=sda, scl=scl)

# Scan for I2C devices and print addresses
print("I2C scan results:")
devices = i2c.scan()
print(devices)

# Try to initialize the display
try:
    print("Trying address 0x3C...")
    oled = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=0x3C)
    print("OLED initialized successfully with address 0x3C")
except Exception as e:
    print(f"Error with 0x3C: {e}")
    try:
        print("Trying alternative address 0x3D...")
        oled = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=0x3D)
        print("OLED initialized successfully with address 0x3D")
    except Exception as e:
        print(f"Error with 0x3D: {e}")
        print("Could not initialize OLED display")
        raise

# If we get here, the display initialized successfully
print("Display test starting...")

# Clear the display
oled.fill(0)
oled.show()

# Display some text
oled.text("OLED Test", 0, 0)
oled.text("Line 2", 0, 10)
oled.text("Line 3", 0, 20)
oled.text("Line 4", 0, 30)
oled.show()

print("Test complete!")
