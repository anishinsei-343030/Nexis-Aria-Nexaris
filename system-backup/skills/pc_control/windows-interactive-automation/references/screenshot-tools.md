---
name: screenshot-tools
category: pc_control
---

# Screenshot Tools Comparison — Session 0 vs Session 1

## Overview

| Tool | Session 0 (Hermes) | Session 1 (User Desktop) | Notes |
|------|---------------------|---------------------------|-------|
| **PIL.ImageGrab.grab()** | ✅ Works | ✅ Works | Uses Windows desktop API (gdi32.dll). No session dependency. |
| **mss.mss().shot()** | ❌ Black screen | ✅ Works | Captures the active session's framebuffer. Fails in Session 0. |
| **pyautogui.screenshot()** | ❌ Black screen | ✅ Works | Wrapper around PIL or mss. Same limitations. |
| **UIA + mss** | ❌ Black screen | ✅ Works | Requires schtasks bridge to Session 1. |

## PIL.ImageGrab.grab() — Preferred for Session 0

### Why it works
- Uses Windows desktop API (`gdi32.dll`) to capture the **primary monitor** at the OS level.
- **No session dependency** — captures the desktop regardless of which session is active.
- Lightweight, no external dependencies beyond Pillow.

### Example

```python
from PIL import ImageGrab

img = ImageGrab.grab()
img.save(r"D:\Hermes\Celestia mei Nexaris\assets\images\desktop_capture.png")
```

### Limitations
- Captures **only the primary monitor** (no multi-monitor support).
- No window targeting — captures the entire desktop.

## mss — Preferred for Session 1

### Why it works
- Captures the **active session's framebuffer**, so it sees the user's desktop.
- Supports **multi-monitor** and **window targeting**.

### Example

```python
import mss

with mss.mss() as sct:
    monitor = sct.monitors[1]  # Primary monitor
    sct.shot(output=r"D:\Hermes\Celestia mei Nexaris\assets\images\desktop_capture.png")
```

### Limitations
- **Fails in Session 0** — returns a black screen or "Access Denied".

## UIA + mss — Advanced Session 1 Control

### When to use
- Targeting a **specific window** (e.g., Edge with Facebook logged in).
- Multi-monitor setups.

### Example

```python
import uiautomation as auto
import mss

# Find Edge window by PID
edge_window = auto.WindowControl(searchDepth=1, processId=7388)
edge_window.SetActive()

# Capture window region
with mss.mss() as sct:
    monitor = {"top": edge_window.BoundingRectangle.top, "left": edge_window.BoundingRectangle.left, "width": edge_window.BoundingRectangle.width(), "height": edge_window.BoundingRectangle.height()}
    sct.shot(output=r"D:\Hermes\Celestia mei Nexaris\assets\images\edge_capture.png")
```

### Limitations
- **Requires Session 1** — must run via schtasks bridge.
- **Complex setup** — needs `uiautomation` + `mss` installed in the user's Python.

## Recommendations

| Task | Tool | Session | Bridge |
|------|------|---------|--------|
| Quick desktop screenshot | PIL.ImageGrab.grab() | Session 0 | ❌ |
| Logged-in browser window | UIA + mss | Session 1 | ✅ schtasks |
| Multi-monitor capture | mss | Session 1 | ✅ schtasks |

**Always prefer PIL for Session 0** — it's the only tool that works without a bridge.