# How to Set Your Pet's Age

## The Problem

When you manually edit `pet_birth_time` in `pet_settings.txt`, you need to make sure it's calculated based on the **current RTC time** on your Pico. If you change the time in Settings after setting the birth time, the age calculation can go negative.

## The Solution: Use the Fix Script

### Method 1: Automatic Fix (Recommended)

1. **First, set the correct time in Settings**
   - Go to Settings (Clock icon)
   - Set the correct time
   - Save and exit

2. **Upload and run `fix_pet_age.py`**
   ```python
   # Edit the DESIRED_AGE variable in the script
   DESIRED_AGE = 80  # Change to whatever age you want
   
   # Then run it
   import fix_pet_age
   ```

3. **Restart your Pico**
   - The pet will now show the correct age!

### Method 2: Manual Calculation

1. **Set the time in Settings first**

2. **Run this in the Pico REPL:**
   ```python
   from time import time
   
   # Set your desired age
   desired_age_days = 80
   
   # Calculate birth time
   current_time = time()
   seconds_per_day = 24 * 60 * 60
   birth_time = current_time - (desired_age_days * seconds_per_day)
   
   print(f"Set pet_birth_time={int(birth_time)}")
   ```

3. **Copy the number and edit `pet_settings.txt`:**
   ```
   name=HUGO
   type=Fox
   setup_complete=True
   pet_birth_time=1234567890  # Use the number from step 2
   god_mode=False
   ```

4. **Restart your Pico**

## Why This Happens

The Pico's `time()` function returns seconds since an epoch (starting point). When you:
1. Set a birth time based on one current time
2. Then change the RTC time in Settings
3. The "current time" changes, making the calculation wrong

**Example:**
- You calculate birth time when current time is `1739145600`
- Birth time for 80 days old = `1739145600 - 6912000 = 1732233600`
- Then you change the time in Settings
- Now current time might be `1732000000` (earlier!)
- Age = `1732000000 - 1732233600 = -233600` seconds = **negative!**

## The Right Order

✅ **CORRECT:**
1. Set time in Settings
2. Calculate/set birth time
3. Restart

❌ **WRONG:**
1. Set birth time
2. Set time in Settings
3. Restart (age will be wrong!)

## Quick Reference

### For 80 Days Old
```python
# Run AFTER setting time in Settings
from time import time
birth_time = time() - (80 * 24 * 60 * 60)
print(f"pet_birth_time={int(birth_time)}")
```

### For Any Age
```python
# Run AFTER setting time in Settings
from time import time
desired_age = 100  # Change this
birth_time = time() - (desired_age * 24 * 60 * 60)
print(f"pet_birth_time={int(birth_time)}")
```

## Safeguard

The code now includes a safeguard: if it detects a negative age, it will automatically reset the birth time to 0 days old. You'll see a warning in the console:

```
Warning: Negative age detected (-3.2). Resetting birth time.
```

This prevents the display from showing negative numbers, but you should still fix it properly using the methods above.

## Files to Help You

- **`fix_pet_age.py`** - Automatic fix script (recommended)
- **`set_pet_age.py`** - Manual calculation helper
- **This guide** - Explains the problem and solutions

## Example: Setting Hugo's Pet to 80 Days

```python
# 1. Set time in Settings first (e.g., 7:00 PM)

# 2. Run this on the Pico:
import fix_pet_age
# (Make sure DESIRED_AGE = 80 in the script)

# 3. Restart Pico

# Done! Hugo's pet is now 80 days old
```

## Troubleshooting

**Still showing negative age?**
- Make sure you ran the fix AFTER setting the time
- Try restarting the Pico
- Check that pet_settings.txt was actually updated

**Age is wrong but not negative?**
- Recalculate using the fix script
- Make sure the RTC time is correct

**Age keeps resetting to 0?**
- The safeguard is triggering
- Use the fix script to set it properly
- Make sure you're not changing the time after setting birth time
