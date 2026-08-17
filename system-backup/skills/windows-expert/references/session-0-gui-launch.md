# Session 0 GUI Launch Guide

## Overview
Windows isolates services and scheduled tasks in **Session 0**, which prevents GUI applications from being visible to the user. To launch a visible GUI application (e.g., Chrome, Notepad) from Hermes running in Session 0, you must:
1. Run Hermes as `SYSTEM` (via Task Scheduler).
2. Use `CreateProcessWithTokenW` to launch the process in the **interactive user session**.

---

## Implementation
### 1. `session_helper.py`
Zero’s implementation uses Win32 APIs to cross from Session 0 to the interactive session:

```python
import ctypes
from ctypes import wintypes

# Load Win32 APIs
WTSGetActiveConsoleSessionId = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId
WTSQueryUserToken = ctypes.windll.wtsapi32.WTSQueryUserToken
CreateProcessAsUser = ctypes.windll.advapi32.CreateProcessAsUserW

# Launch a process in the interactive session
def run_as_interactive_user(executable, args=""):
    session_id = WTSGetActiveConsoleSessionId()
    h_token = ctypes.c_void_p()
    if WTSQueryUserToken(session_id, ctypes.byref(h_token)):
        startup_info = STARTUPINFO()
        startup_info.lpDesktop = "winsta0\\default"
        process_info = PROCESS_INFORMATION()
        
        if CreateProcessAsUser(
            h_token, executable, args, None, None, False, 
            0, None, None, ctypes.byref(startup_info), ctypes.byref(process_info)
        ):
            return {"success": True, "pid": process_info.dwProcessId}
        else:
            return {"success": False, "error": ctypes.get_last_error()}
    else:
        return {"success": False, "error": ctypes.get_last_error()}
```

### 2. `browser_visible_manager.py`
Launches Chrome with `--remote-debugging-port=9222` for CDP control:

```python
from session_helper import run_as_interactive_user

def handle_browser_launch_visible(args):
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    chrome_args = "--remote-debugging-port=9222 --user-data-dir=C:\\Windows\\System32\\config\\systemprofile\\.hermes\\chrome_profile"
    result = run_as_interactive_user(chrome_path, chrome_args)
    if result["success"]:
        return {"success": True, "message": f"Visible Chrome launched (PID {result['pid']}).", "cdp_url": "http://127.0.0.1:9222"}
    else:
        return {"success": False, "error": result["error"]}
```

### 3. `desktop_screenshot.py`
Captures the screen in the interactive session using `mss`:

```python
from session_helper import run_as_interactive_user

def handle_desktop_screenshot(args):
    script = '''
import mss
import os
with mss.mss() as sct:
    output = os.path.join(os.environ["TEMP"], "screenshot.png")
    sct.shot(output=output)
    print(output)
'''
    result = run_as_interactive_user(
        python_exe=sys.executable,
        script_content=script
    )
    if result["success"]:
        return {"success": True, "path": result["output"].strip()}
    else:
        return {"success": False, "error": result["error"]}
```

---

## Debugging
### Error 1314: "A required privilege is not held by the client"
- **Cause**: `WTSQueryUserToken` requires Hermes to run as `SYSTEM`.
- **Fix**: Update the Task Scheduler task:
  ```powershell
  schtasks /change /tn "Hermes_Gateway" /ru SYSTEM
  ```

### Invisible Window
- **Cause**: Task Scheduler is set to "Run only when user is logged on."
- **Fix**: Ensure the task runs as `SYSTEM` and is not restricted to logged-on users.

### Screenshot Failures
- **Cause**: Direct `mss` calls from Session 0 fail.
- **Fix**: Use `run_as_interactive_user()` to spawn the capture script in the user’s session.