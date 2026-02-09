# Fix Pet Age Script
# Use this if your pet is showing a negative age or wrong age
# 
# This script will:
# 1. Read your current pet_settings.txt
# 2. Calculate the correct birth time based on current RTC
# 3. Update the file with the correct value
#
# Run this AFTER you've set the correct time in Settings!

from time import time

def fix_pet_age(desired_age_days):
    """Fix the pet age by recalculating birth time"""
    
    # Calculate correct birth time
    current_time = time()
    seconds_per_day = 24 * 60 * 60
    age_in_seconds = desired_age_days * seconds_per_day
    birth_time = current_time - age_in_seconds
    
    print("=" * 50)
    print("Pet Age Fix Tool")
    print("=" * 50)
    
    # Read existing settings
    settings = {}
    try:
        with open('pet_settings.txt', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    settings[key] = value
        print("\n✓ Current settings loaded")
    except:
        print("\n✗ Could not read pet_settings.txt")
        return
    
    # Show current values
    print(f"\nCurrent pet_birth_time: {settings.get('pet_birth_time', 'Not set')}")
    print(f"Current time: {int(current_time)}")
    
    # Calculate new birth time
    print(f"\nDesired age: {desired_age_days} days")
    print(f"New pet_birth_time: {int(birth_time)}")
    
    # Update settings
    settings['pet_birth_time'] = str(int(birth_time))
    
    # Write back to file
    try:
        with open('pet_settings.txt', 'w') as f:
            for key, value in settings.items():
                f.write(f"{key}={value}\n")
        print("\n✓ Settings updated successfully!")
        print("\nRestart your Pico to see the changes.")
    except Exception as e:
        print(f"\n✗ Error writing settings: {e}")
    
    # Verify
    age_check = (current_time - birth_time) / (24 * 60 * 60)
    print(f"\nVerification: Pet will be {age_check:.1f} days old")
    print("=" * 50)

# ============================================
# CONFIGURE YOUR DESIRED AGE HERE
# ============================================
DESIRED_AGE = 80  # Change this to whatever age you want

# Run the fix
fix_pet_age(DESIRED_AGE)
