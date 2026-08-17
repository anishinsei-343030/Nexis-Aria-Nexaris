import requests
import psutil
import sys

def verify_chrome_visible(pid, cdp_port=9222):
    """Verify Chrome is running and visible by checking PID and CDP port."""
    # Check if process exists
    if not psutil.pid_exists(pid):
        print(f"ERROR: PID {pid} not found")
        return False
    
    # Check CDP endpoint
    try:
        resp = requests.get(f"http://127.0.0.1:{cdp_port}/json")
        tabs = resp.json()
        print(f"SUCCESS: Chrome visible (PID {pid}, {len(tabs)} tabs open)")
        print("Open tabs:")
        for tab in tabs:
            print(f"- {tab.get('title', 'N/A')} ({tab.get('url', 'N/A')})")
        return True
    except requests.RequestException as e:
        print(f"ERROR: CDP port {cdp_port} unreachable - {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_chrome_visible.py <PID>")
        sys.exit(1)
    verify_chrome_visible(int(sys.argv[1]))