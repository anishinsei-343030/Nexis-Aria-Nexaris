---
name: session0-desktop-capture
title: Session 0 Desktop Screenshot (GDI)
description: Capture and deliver the user's desktop from Session 0 using PIL.ImageGrab (GDI). Works across sessions, preserves logged-in state, no browser restart. Auto-delivers screenshot via MEDIA:/path.
---

## When to Use
- User asks "what's on my screen?", "show me Aoi's desktop", or similar.
- Need to verify UI state (e.g., logged-in browser, open apps).
- Session 1 browser control (UIA/schtasks) is overkill or failing.

## Requirements
- Python with PIL (`pip install pillow`)
- Session 0 terminal access (Hermes default)
- Write access to `D:\Hermes\Celestia mei Nexaris\assets\images\`

## Steps
1. **Run capture** (one-liner):
   ```bash
   python -c "from PIL import ImageGrab; img=ImageGrab.grab(); img.save(r'D:\\Hermes\Celestia mei Nexaris\\assets\\images\\desktop_$(date +'%Y%m%d_%H%M%S').png')"
   ```
   - Uses GDI (not DXGI) → works across sessions.
   - Timestamped filename avoids collisions.

2. **Deliver screenshot**:
   ```markdown
   MEDIA:D:\Hermes\Celestia mei Nexaris\assets\images\desktop_<timestamp>.png
   ```
   - Platform auto-renders as native image (Telegram photo).

## Pitfalls
- **Black screens**: If `mss` is used instead of PIL, DXGI fails in Session 0. Always use PIL.
- **Path escaping**: Windows paths need `\\` in Python strings (raw string `r''` helps).
- **Session mismatch**: Session 1 tools (UIA, Playwright) won’t work in Session 0 — stick to GDI.

## Verification
- Check file exists:
  ```bash
  ls -l "D:\Hermes\Celestia mei Nexaris\assets\images\desktop_*.png"
  ```
- Confirm size > 100KB (black screens are ~1KB).

## Example Output
```
-rw-r--r-- 1 Administrator 1920x1080 155961 Jun 16 15:04 desktop_20260616_150419.png
```