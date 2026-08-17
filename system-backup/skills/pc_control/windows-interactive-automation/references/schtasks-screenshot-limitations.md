# schtasks Screenshot Limitations & UIA Alternative

## The Problem

`schtasks` + `/it` **can launch visible GUI apps** into Session 1, but **cannot reliably run screenshot capture scripts** (Python/mss or PowerShell). The script exits silently with no error output and produces no file.

## Root Cause

Processes launched via `schtasks /ru <user> /it` inherit the user's desktop session for **window visibility**, but the **process context** (environment variables, PATH, working directory) behaves inconsistently. `mss` and `PIL.ImageGrab` fail because the process cannot access the screen buffer from the `schtasks` hosting context.

## Verified Working Approach: UIA + Direct Python

Instead of a two-step launch (app via schtasks + capture via schtasks), run the **entire workflow** as a Python script from within your Hermes session using:

1. `uiautomation` (`pip install uiautomation mss comtypes`) — find browser windows, send keys
2. `mss` — capture screenshots directly (works when run from Hermes WSL terminal)

**Script template**: `scripts/uia_browser_control.py` in this skill directory.

## Key UIA Patterns (from this session)

```python
import uiautomation as auto
import mss
import mss.tools
import time

# List all top-level windows
for w in auto.GetRootControl().GetChildren():
    print(f"Window: '{w.Name}' (class: {w.ClassName})")

# Set focus to a window by class name
for w in auto.GetRootControl().GetChildren():
    if 'chrome_widgetwin_1' in w.ClassName.lower():
        w.SetFocus()
        break

# Send keyboard shortcuts
auto.SendKeys('{Ctrl}t')         # new tab
auto.SendKeys('https://www.facebook.com{Enter}')  # navigate

# Capture screen with mss
with mss.mss() as sct:
    monitor = sct.monitors[0]
    sct_img = sct.grab(monitor)
    mss.tools.to_png(sct_img.rgb, sct_img.size, output="path/to/output.png")
```

## Pitfalls

| Issue | Fix |
|-------|-----|
| `mss.mss` is deprecated | Use `mss.MSS` instead (still works with same API) |
| `uiautomation` not installed | Run `pip install uiautomation mss comtypes` |
| "PaneControl object has no attribute FindFirst" | Use `GetChildren()` then iterate, not `FindFirst` with wrong params |
