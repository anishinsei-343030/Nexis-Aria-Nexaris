"""
Navigate to a URL in an existing Edge/Chrome browser window and take a screenshot.

Usage:
    python navigate_browser.py <PID> <URL> [output_path]

Example:
    python navigate_browser.py 7388 youtube.com
    python navigate_browser.py 11080 facebook.com D:\screenshot.png
"""

import uiautomation as auto
from PIL import ImageGrab
import time
import os
import sys

def navigate_and_capture(pid: int, url: str, output_path: str = None):
    """Navigate to URL in browser PID and capture screenshot."""
    # Find browser window
    browser = auto.WindowControl(searchDepth=1, processId=pid)
    if not browser.Exists(3):
        print(f"Browser window with PID {pid} not found!")
        return None

    print(f"Found browser: '{browser.Name}'")
    browser.SetActive()
    time.sleep(0.5)

    # New tab
    auto.SendKeys('{Ctrl}t')
    time.sleep(0.5)

    # Navigate
    auto.SendKeys(f'{url}{{Enter}}')
    time.sleep(5)  # Wait for load

    # Screenshot
    if output_path is None:
        output_dir = r"D:\Hermes\Celestia mei Nexaris\assets\images"
        os.makedirs(output_dir, exist_ok=True)
        from datetime import datetime
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(output_dir, f"browser_{ts}.png")

    img = ImageGrab.grab()
    img.save(output_path)
    print(f"Screenshot saved to {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python navigate_browser.py <PID> <URL> [output_path]")
        sys.exit(1)

    pid = int(sys.argv[1])
    url = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    navigate_and_capture(pid, url, output_path)