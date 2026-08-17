---
name: windows-edge-session-control
description: Control existing Edge/Chrome browser windows with logged-in sessions preserved, using UIA window discovery + SendKeys + PIL.ImageGrab directly from Session 0.
triggers: [edge, chrome, browser, logged-in, UIA, SendKeys, session 0, facebook, youtube, gmail, browser control, desktop screenshot]
---

# Windows Edge/Chrome Session Control — UIA + PIL from Session 0

## Context

Hermes runs as **SYSTEM in Session 0**. User's browsers (Edge, Chrome) run in **Session 1** with all logged-in sessions intact.

**Key discovery**: UIA (`uiautomation` library) can discover and control windows across sessions from Session 0. `WindowControl(processId=...)` + `SetActive()` + `SendKeys()` injects input into the correct session automatically. Only **screenshots** needed a workaround — `mss` (DXGI) fails in Session 0, `PIL.ImageGrab.grab()` (GDI) works.

**No schtasks bridge needed.** Run UIA + PIL scripts directly from the Hermes terminal.

## Launching a New Browser Instance (not controlling an existing one)

When the user says "open [site]" or requests a new browser window (not just a tab):

### Preferred method — PowerShell via terminal (git-bash)

```bash
# Launch Edge to Freelancer.com (new instance)
powershell -Command "\$edgePath = (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe' -ErrorAction SilentlyContinue).'(Default)'; if (\$edgePath) { Start-Process -FilePath \"\$edgePath\" -ArgumentList 'https://www.freelancer.com' } else { Write-Host 'Edge not found'; exit 1 }"
```

**Critical**: `$` signs MUST be escaped as `\$` when running PowerShell through git-bash/MSYS. Unescaped `$` gets consumed by MSYS as shell variable expansion. Applies to ALL PowerShell commands through the terminal tool (see `windows-expert` skill).

```bash
# Launch Chrome (simpler — known path)
powershell -Command "Start-Process -FilePath \"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" -ArgumentList 'https://www.freelancer.com'"

# Launch with profile
powershell -Command "Start-Process -FilePath \"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" -ArgumentList '--profile-directory=\"Default\"', 'https://www.freelancer.com'"
```

### Verify it launched

```bash
tasklist | grep -i -E "msedge|chrome"
```

Then take a screenshot with PIL to confirm the page loaded.

### When to use this vs UIA control

| Scenario | Default Approach | Fallback |
|----------|------------------|----------|
| "Open [site]" | Hermes browser tools (Playwright-backed, persistent profile) | Edge (UIA) launch via PowerShell |
| "Go to [site] in my browser" | Hermes browser tools (Playwright-backed, persistent profile) | Edge (UIA) launch via PowerShell |
| "Control my browser to..." | Hermes browser tools (browser_navigate/click/snapshot) | Edge UIA + SendKeys |
| "Extract data / scrape from [site]" | Hermes browser tools (Playwright-backed) | CDP via WebSocket on Edge |
| "Log in to X" | Hermes browser tools (persistent profile likely has login) | Edge UIA launch + wait for user |
| Take a screenshot | PIL.ImageGrab.grab() for desktop; CDP Page.captureScreenshot for browser-only |

## CDP (Chrome DevTools Protocol) — WebSocket Control

### When to use CDP

| Scenario | CDP | UIA/SendKeys |
|----------|-----|--------------|
| Extract page content (HTML, text) | ✅ Best | ❌ No |
| Navigate to 10+ pages | ✅ Fast, no UI | ❌ Slow, flaky |
| Fill forms / click buttons | ✅ Precise | ✅ Works |
| Screenshot browser viewport | ✅ High quality | ✅ Works |
| Screenshot desktop | ❌ No | ✅ PIL.ImageGrab |
| Logged-in session required | ✅ Preserved | ✅ Preserved |

### Launch Edge with CDP enabled

```bash
# Kill existing Edge (if running)
taskkill /IM msedge.exe /F

# Launch with remote debugging
powershell -Command "Start-Process -FilePath \"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe\" -ArgumentList '--remote-debugging-port=9222', '--remote-allow-origins=*', 'https://www.freelancer.com'"
```

### Verify CDP endpoint

```bash
curl http://127.0.0.1:9222/json
```

Returns:
```json
[{
  "description": "",
  "devtoolsFrontendUrl": "/devtools/inspector.html?ws=127.0.0.1:9222/devtools/page/163ADEE812BD60767FF1C64B958991F6",
  "id": "163ADEE812BD60767FF1C64B958991F6",
  "title": "Freelancer: Freelance Jobs & Contests | Find Work Today | Freelancer",
  "type": "page",
  "url": "https://www.freelancer.com/jobs/copy-writing/",
  "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/page/163ADEE812BD60767FF1C64B958991F6"
}]
```

### Connect via WebSocket (Python)

```python
import websocket
import json
import requests

# Get tab
resp = requests.get('http://127.0.0.1:9222/json')
tabs = resp.json()
target_tab = tabs[0]  # or filter by URL

ws_url = target_tab['webSocketDebuggerUrl']
ws = websocket.create_connection(ws_url)

# Get page HTML
ws.send(json.dumps({
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.documentElement.outerHTML"
    }
}))
resp = ws.recv()
result = json.loads(resp)
html = result['result']['result']['value']

# Navigate to URL
ws.send(json.dumps({
    "id": 2,
    "method": "Page.navigate",
    "params": {
        "url": "https://www.freelancer.com/jobs/copy-writing/"
    }
}))
resp = ws.recv()

# Screenshot (browser viewport only)
ws.send(json.dumps({
    "id": 3,
    "method": "Page.captureScreenshot",
    "params": {
        "format": "png"
    }
}))
resp = ws.recv()
result = json.loads(resp)
with open("screenshot.png", "wb") as f:
    f.write(base64.b64decode(result['result']['data']))

ws.close()
```

### Common CDP Commands

| Task | Method | Payload |
|------|--------|---------|
| Get HTML | `Runtime.evaluate` | `{"expression": "document.documentElement.outerHTML"}` |
| Navigate | `Page.navigate` | `{"url": "..."}` |
| Screenshot | `Page.captureScreenshot` | `{"format": "png"}` |
| Scroll | `Runtime.evaluate` | `{"expression": "window.scrollTo(0, document.body.scrollHeight)"}` |
| Extract links | `Runtime.evaluate` | `{"expression": "JSON.stringify(Array.from(document.querySelectorAll('a')).map(a => ({text: a.innerText, href: a.href})))"}` |

### Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `Page.navigate` typo | Typo in URL (e.g., `freancer.com`) | Double-check URL before sending |
| WebSocket closed | Browser tab closed | Reconnect to new tab ID |
| No `Page` methods | `Page.enable` not called | Send `{"id": 1, "method": "Page.enable"}` first |
| Screenshot black | Browser not visible | Use PIL.ImageGrab for desktop screenshots |
| HTML empty | Page not loaded | Wait for `Page.loadEventFired` event |

### Script: [`scripts/cdp_browser.py`](scripts/cdp_browser.py)

Reusable CDP client for navigation, content extraction, and screenshots.

Usage:
```bash
python scripts/cdp_browser.py 9222 navigate "https://www.freelancer.com/jobs/copy-writing/"
python scripts/cdp_browser.py 9222 extract html > freelancer.html
python scripts/cdp_browser.py 9222 extract links > freelancer_links.json
```

```bash
# Find main Edge or Chrome process
tasklist | grep -i -E "msedge|chrome"
```

The process with the highest memory usage (`K` column) is usually the main browser instance with all tabs.

### Open a URL in existing browser (Python one-liner)

```python
python -c "
import uiautomation as auto, time
from PIL import ImageGrab
import os

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
path = r'D:\Hermes\Celestia mei Nexaris\assets\images\capture.png'
ImageGrab.grab().save(path)
print(path)
"
```

### Quick screenshot only

```python
python -c "from PIL import ImageGrab; img=ImageGrab.grab(); img.save(r'D:\Hermes\Celestia mei Nexaris\assets\images\desktop.png')"
```

## Working Pattern

### 1. Verify browser is running

```bash
tasklist | grep -i -E "msedge|chrome"
```

Pick a PID — use the one with the largest memory footprint (main instance). **Multiple chrome.exe/msedge.exe processes are child processes — any top-level PID works.** Multiple chrome.exe/msedge.exe processes are child processes, any top-level PID works.

### 2. Write & run the control script

Components:

| Step | Tool | Notes |
|------|------|-------|
| Find window | `auto.WindowControl(searchDepth=1, processId=PID)` | Works across sessions |
| Focus | `.SetActive()` or `.SetFocus()` | Brings to foreground |
| Type in address bar | `auto.SendKeys('{Ctrl}t')` then URL + `{Enter}` | Ctrl+T = new tab, URL auto-searches/navigates |
| Wait for load | `time.sleep(5)` | Adjust for slow connections |
| Capture screen | `PIL.ImageGrab.grab().save(path)` | GDI, works in Session 0 |

### 3. Deliver screenshot

```
MEDIA:D:\Hermes\Celestia mei Nexaris\assets\images\capture.png
```

Always auto-deliver — user can't see your actions.

## Common Navigation Patterns

### YouTube
```python
auto.SendKeys('{Ctrl}t')
time.sleep(0.5)
auto.SendKeys('youtube.com{Enter}')
time.sleep(5)
```

### Facebook
```python
auto.SendKeys('{Ctrl}t')
time.sleep(0.5)
auto.SendKeys('facebook.com{Enter}')
time.sleep(5)
```

### Gmail
```python
auto.SendKeys('{Ctrl}t')
time.sleep(0.5)
auto.SendKeys('mail.google.com{Enter}')
time.sleep(5)
```

### Search / type text on a page
```python
auto.SendKeys('{Ctrl}t')
time.sleep(0.5)
auto.SendKeys('{Ctrl}k')  # Search or type URL
time.sleep(0.3)
auto.SendKeys('my search query{Enter}')
```

## Script: [`scripts/navigate_browser.py`](scripts/navigate_browser.py)

Reusable script for quick navigation + screenshot:
- Accepts URL and browser PID as arguments
- Opens new tab, navigates, waits, captures screenshot
- Saves to workspace with timestamp

Usage:
```bash
python scripts/navigate_browser.py 7388 youtube.com
```

### schtasks bridge
| Problem | Cause | Fix |
|---------|-------|-----|
| schtasks bridge | Confusion with old method | Don't use it — UIA+PIL works directly from Session 0 |

| Problem | Cause | Fix |
|---------|-------|-----|
| `WindowControl` not found | Wrong PID or browser not running | `tasklist` first, pick correct PID |
| Screenshot black/blank | Using `mss` in Session 0 | Use `PIL.ImageGrab.grab()` — GDI works across sessions |
| SendKeys not reaching browser | Window not active | Add longer sleep after `SetActive()`, try `.SetTopmost(True)` |
| Multiple browser instances | Several PIDs from tasklist | Pick the one with highest memory — it's the main window |
| schtasks bridge | Confusion with old method | Don't use it — UIA+PIL works directly from Session 0 |
| URL didn't load | Network or slow page | Increase sleep after Enter to 8-10s |
| "No module named PIL" | Missing Pillow | `pip install Pillow` |
| "No module named uiautomation" | Missing UIA library | `pip install uiautomation` |

## Verification Checklist

- [ ] Browser PID identified via tasklist
- [ ] `pip install uiautomation Pillow` (done once)
- [ ] Script opens new tab + navigates to URL
- [ ] Screenshot saved to `D:\Hermes\Celestia mei Nexaris\assets\images\`
- [ ] Screenshot delivered via `MEDIA:/path/to/file`
- [ ] Logged-in session visible (Facebook, YouTube, Gmail, etc.)
