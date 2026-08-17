---
name: windows-interactive-automation
description: Guide for launching visible GUI applications and capturing screenshots when Hermes runs as SYSTEM in Session 0 (Task Scheduler).
triggers: [visible browser, desktop screenshot, GUI window, Session 0, Access is denied screen capture, invisible window]
---

# Windows Interactive Automation

## User Directive: Logged-In Platforms

**Always use PC browser control for logged-in platforms** (Gmail, Facebook, YouTube, freelance accounts, social media, banking, or any service requiring persistent sessions). Agent Browser (headless) is **only for public, non-authenticated, or disposable tasks**. This is a **non-negotiable rule** — violating it will break user workflows and require re-authentication.

When in doubt, **ask the user**: "Should I use your PC browser for this task?"

---

When Hermes is configured to run as `NT AUTHORITY\SYSTEM` via Task Scheduler, it operates in **Session 0**. Processes started in Session 0 are isolated from the user's interactive desktop, meaning GUI windows are invisible and screen capture tools (like `mss` or `PIL`) will fail with "Access Denied" or "Screen grab failed".

## Primary Solution: Hermes Desktop Session Agent

The preferred method for desktop interaction is now the **Hermes Desktop Session Agent**. This agent automatically handles the Session 0 to Session 1 transition and provides direct access to desktop tools (mouse, keyboard, window management, screenshots) without requiring manual token duplication or `schtasks` commands.

### Using the Desktop Session Agent

Refer to the `windows-ui-automation` skill for details on using the Session Agent and its available tools (`desktop_screenshot`, `mouse_move`, `keyboard_type`, `window_list`, etc.). These tools are directly callable by the agent.

**Pitfall**: Direct terminal commands (`powershell`, `cmd.exe /c start`) from Session 0 fail with `Bash/WSL_E_LOCAL_SYSTEM_NOT_SUPPORTED`. Use the dedicated desktop tools when available.

### Workaround: schtasks Bridge (when Session Agent unavailable)

If the Desktop Session Agent is not configured, the **schtasks bridge** via `cmd.exe /c` + `.bat` file can launch visible GUI apps. This works because `schtasks` with the `/it` flag creates a task that runs in the interactive user session.

**Critical detail**: Git Bash (MSYS) corrupts `schtasks /create` flags (interprets `/create` as a path). Wrap schtasks commands in a `.bat` file and execute via `cmd.exe /c "path\to\script.bat"`.

See `references/schtasks-bridge.md` for the complete working pattern.

## Alternative Solution: Manual Token Duplication (Legacy/Advanced)

If the Desktop Session Agent is unavailable or for advanced manual control, Hermes can still "cross" from Session 0 into the active interactive session using token duplication. This is achieved by:
1. Finding the ID of the active console session (`WTSGetActiveConsoleSessionId`).
2. Retrieving the user token for that session (`WTSQueryUserToken`).
3. Launching the target process using that token (`CreateProcessWithTokenW`).

**Note**: The following sections on `Implementation Workflow` still apply for this manual method.

## Implementation Workflow

### 1. Requirements
- Hermes must be running as `SYSTEM`. (Standard users in Session 0 cannot retrieve other user tokens, resulting in Error 1314).
- The `session_helper.py` utility must be available in the tools directory.

### 2. Launching GUI Apps (e.g., Chrome)
Instead of `subprocess.Popen`, use the `run_as_interactive_user` wrapper:
```python
from tools.session_helper import run_as_interactive_user

result = run_as_interactive_user(
    python_exe="path/to/python.exe", 
    script_path="path/to/launch_script.py",
    workdir="C:/path/to/workdir"
)
```

### 3. Capturing Screenshots
Direct calls to `mss` from the main agent will fail. You must launch a separate "capture script" in the interactive session:
1. Write a temporary Python script that uses `mss` to save a file to a shared location (e.g., `%TEMP%`).
2. Execute that script via `run_as_interactive_user`.
3. Read the resulting image file from the shared location.

## Pitfalls & Troubleshooting

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| **Window is invisible** | Process launched in Session 0 | Use schtasks bridge (.bat + cmd.exe /c) |
| **Error 1314 (Access Denied)** | Hermes is not running as `SYSTEM` | Check Task Scheduler task config — must run as `NT AUTHORITY\\SYSTEM` |
| **Screen grab failed** | Attempting to capture Session 0 | **schtasks bridge fails for screenshots** — use UIA + `uiautomation` + `mss` instead (see `scripts/uia_browser_control.py`) |
| **schtasks /create garbled** | Git Bash interprets `/create` as path `/c/create` | Wrap in `.bat` file + `cmd.exe /c` |
| **schtasks succeeds but app doesn't open** | Single quotes around exe path in `/tr` | Use plain double quotes: `"path\to\app.exe"`, NOT `"'path'"` |
| **Chrome profile locked** | Multiple instances using same profile | Use `--new-window` flag to re-use existing instance |
| **Facebook/Gmail not logged in** | Used Agent Browser instead of PC browser | **Always use PC browser control for logged-in platforms** — never Agent Browser |
## Missing Module Fixes
- **UIA script fails with 'No module named uiautomation'**: Run `pip install uiautomation mss comtypes` in the user session

### Mei Browser Manager (Chrome Instance)
For controlling Shin's Playwright-based Chrome instance (Mei_Browser.ps1) for Hermes browser tools. See [references/mei-browser-manager.md](references/mei-browser-manager.md) for full details.

**Safety Rules (FIRST)**:
- **NEVER** run `taskkill /f /im chrome.exe` — it kills **every** Chrome process on the machine.
- Allowed commands only: `Mei_Browser.ps1 start`, `stop`, `status`

**Where Things Live:**
| Component | Path |
|-----------|------|
| Management script | `D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1` |
| PID file | `D:\Celestia Mei Nexaris\playwright\chrome.pid` |
| Debug port | 9922 |

**Basic Usage:**
```bash
powershell -File "D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1" -Command status
powershell -File "D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1" -Command start
powershell -File "D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1" -Command stop
```

**CDP Fallback Workflow:** When Hermes browser tools can't connect to the running Chrome instance, use raw CDP commands:
```bash
browser_cdp(method="Target.getTargets", params={})
browser_cdp(method="Target.createTarget", params={"url": "https://target-site.com"})
```

**Pitfalls:**
- **PID Detection Bug**: `Start-Process` returns the spawner PID, not the actual Chrome process. Fixed by using `Get-NetTCPConnection -LocalPort $port -State Listen` after a 2-second delay.
- **Session Crash**: If all browser tools return "Interrupted", the entire Hermes session may need a restart — ask for `/restart`.
- **Logged-In Browsing**: The persistent profile (`mei_profile/`) keeps cookies and logins across sessions.

## Verification Workflow (Always Follow)

After any logged-in browser action:
1. **Take a screenshot** via UIA + mss (`scripts/uia_browser_control.py`)
2. **Send the screenshot** to the user via `MEDIA:path` or `vision_analyze`
3. **Confirm visually** what's on screen — don't assume the action succeeded
4. **Report findings** clearly: "Logged in as [account]", "Seen: [content]", etc.

**Always include a screenshot** — the user is blind to what you're doing.

## Screenshot Tools

### PIL.ImageGrab.grab() — Preferred for Session 0

**Why**: Works in Session 0 (unlike `mss` or `pyautogui`). Uses Windows desktop API (`gdi32.dll`) to capture the primary monitor. No session dependency.

**Example**:
```python
from PIL import ImageGrab
img = ImageGrab.grab()
img.save(r"D:\Hermes\Celestia mei Nexaris\assets\images\desktop_capture.png")
```

**Limitations**: Captures only the primary monitor. No window targeting.

## Session 0 Browser Control — UIA + SendKeys

**Discovery**: UIA (`uiautomation` library) can discover and control browser windows across sessions from Session 0. `WindowControl(processId=...)` + `SetActive()` + `SendKeys()` injects input into the correct session automatically. No schtasks bridge needed.

**Pattern**:
```python
import uiautomation as auto
from PIL import ImageGrab
import time

# Find browser window by PID
browser = auto.WindowControl(searchDepth=1, processId=7388)
browser.SetActive()
time.sleep(0.5)

# New tab + navigate
auto.SendKeys('{Ctrl}t')
time.sleep(0.5)
auto.SendKeys('youtube.com{Enter}')
time.sleep(5)

# Screenshot
ImageGrab.grab().save(r'D:\Hermes\Celestia mei Nexaris\assets\images\capture.png')
```

**Pitfall**: schtasks bridge is no longer needed — UIA+PIL works directly from Session 0. Avoid it unless you need to launch a new GUI app (not just control an existing one).

**See also**: `windows-edge-session-control` skill for full details and reusable scripts.

### mss — Preferred for Session 1

**Why**: Captures the active session's framebuffer. Supports multi-monitor and window targeting.

**Pitfall**: Fails in Session 0 (black screen). Must run via schtasks bridge.

### UIA + mss — Advanced Session 1 Control

**When**: Targeting a specific window (e.g., Edge with Facebook logged in).

**Pitfall**: Requires `uiautomation` + `mss` installed in the user's Python.

## Verification Checklist (Updated)

After any logged-in browser action:
1. **Take a screenshot** — use `PIL.ImageGrab.grab()` for general Session 0 desktop capture, or UIA + `PIL.ImageGrab.grab()` for targeted browser control in Session 0 (see `windows-edge-session-control`).
2. **Send the screenshot** to the user via `MEDIA:path` or `vision_analyze`.
3. **Confirm visually** what's on screen — don't assume the action succeeded.
4. **Report findings** clearly: "Logged in as [account]", "Seen: [content]".

**Always include a screenshot** — the user is blind to what you're doing.

## References
- `references/screenshot-tools.md`: Comparison of PIL, mss, and UIA for screenshots in Session 0 vs Session 1.
- `references/schtasks-bridge.md`: Verified zero-setup technique to launch GUI apps into user desktop.
- `references/session-0-isolation.md`: Deep dive into Windows Session 0 architecture.
- `references/schtasks-screenshot-limitations.md`: Why schtasks bridge fails for screenshots.
- `scripts/uia_browser_control.py`: Reusable script for opening Facebook in a browser and taking a screenshot via UIA + mss.
