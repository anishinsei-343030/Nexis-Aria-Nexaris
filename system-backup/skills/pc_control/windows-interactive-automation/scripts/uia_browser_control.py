import os
import uiautomation as auto
import mss
import mss.tools
import time
import subprocess

# This script attempts to open Facebook in an existing Edge/Chrome window or launches Chrome if not found.
# It then takes a screenshot of the primary monitor.

# Wait for windows to stabilize before searching
time.sleep(1)

# Flag to track if Facebook was found and processed
facebook_processed = False

# --- Step 1: Try to find an existing browser window and open Facebook ---
# Iterate through top-level windows to find Edge or Chrome
print("Searching for existing browser windows...")
for w in auto.GetRootControl().GetChildren():
    window_name = w.Name
    window_class_name = w.ClassName
    
    # Check for Edge (Chrome_WidgetWin_1) or Chrome (Chrome_WidgetWin_1)
    if ('chrome_widgetwin_1' in window_class_name.lower()) and \
       (('edge' in window_name.lower() and 'microsoft' in window_name.lower()) or ('chrome' in window_name.lower() and 'google' in window_name.lower())):
        
        print(f"Found potential browser window: '{window_name}' (class: {window_class_name})")
        # Bring the window to foreground and focus
        w.SetFocus()
        time.sleep(0.5)
        
        # Open a new tab (Ctrl+T)
        print("Opening new tab (Ctrl+T)...")
        auto.SendKeys('{Ctrl}t')
        time.sleep(1)
        
        # Type Facebook URL and press Enter
        print("Navigating to Facebook...")
        auto.SendKeys('https://www.facebook.com{Enter}')
        time.sleep(5) # Give it time to load
        
        facebook_processed = True
        break # Exit loop after processing the first suitable browser

if not facebook_processed:
    # --- Step 2: If no suitable browser found or Facebook not opened, launch Chrome fresh ---
    print("No existing browser with Facebook found, launching Chrome...")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    try:
        subprocess.Popen([chrome_path, 'https://www.facebook.com'])
        time.sleep(8) # Give Chrome time to launch and load Facebook
        facebook_processed = True
    except FileNotFoundError:
        print(f"Error: Chrome executable not found at {chrome_path}")
    except Exception as e:
        print(f"Error launching Chrome: {e}")

if facebook_processed:
    # --- Step 3: Take a screenshot of the primary monitor ---
    print("Attempting to capture screenshot...")
    output_dir = r"D:\Hermes\Celestia mei Nexaris\assets\images"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "facebook_check.png")
    
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[0] # Primary monitor
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)
        print(f"Screenshot saved to {output_path}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
else:
    print("Could not process Facebook. No screenshot taken.")

print("Script finished.")
