# Helper script to set pet age
# Run this on your Pico to calculate the birth time for a specific age
# 
# IMPORTANT: Run this AFTER setting the time in settings!
# The birth time is calculated based on the current RTC time.

from time import time

def calculate_birth_time(age_in_days):
    """Calculate the birth time for a pet of a given age"""
    current_time = time()
    seconds_per_day = 24 * 60 * 60
    age_in_seconds = age_in_days * seconds_per_day
    birth_time = current_time - age_in_seconds
    return birth_time

# Set desired age here
DESIRED_AGE_DAYS = 80

# Calculate birth time
current_time = time()
birth_time = calculate_birth_time(DESIRED_AGE_DAYS)

print("=" * 50)
print("PicoTamachibi Age Calculator")
print("=" * 50)
print(f"\nCurrent time (seconds since epoch): {int(current_time)}")
print(f"Desired age: {DESIRED_AGE_DAYS} days")
print(f"Calculated birth time: {int(birth_time)}")
print(f"\nTo make your pet {DESIRED_AGE_DAYS} days old:")
print(f"\n1. Make sure you've set the correct time in Settings first!")
print(f"2. Edit pet_settings.txt and change the pet_birth_time line to:")
print(f"\n   pet_birth_time={int(birth_time)}")
print(f"\n3. Restart your Pico")
print(f"\n4. Your pet will be {DESIRED_AGE_DAYS} days old!")
print("=" * 50)

# Verify the calculation
age_check = (current_time - birth_time) / (24 * 60 * 60)
print(f"\nVerification: Age would be {age_check:.1f} days")
print("=" * 50)
