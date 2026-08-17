# Visible Chrome Launch Session - 2026-06-14

## Context
- **Goal**: Launch a visible Chrome browser from Hermes (running as `SYSTEM`) and retain login sessions (e.g., Facebook).
- **Constraints**: Session 0 isolation, WSL/bash limitations, fallback paths.

---

## Attempt 1: Terminal Tool (Failed)
**Command**:
```bash
python -m tools.browser_visible_manager --action launch
```

**Error**:
```
Running WSL as local system is not supported.
Error code: Bash/WSL_E_LOCAL_SYSTEM_NOT_SUPPORTED
```

**Root Cause**: The `terminal` tool wraps commands in WSL/bash, which fails when Hermes runs as `SYSTEM`.

---

## Attempt 2: Execute Code (Fallback Success)
**Code**:
```python
from tools.browser_visible_manager import handle_browser_launch_visible
result = handle_browser_launch_visible(args={})
```

**Result**:
```json
{
  "success": true,
  "message": "Chrome launched via fallback (PID 148). Window may not be visible.",
  "cdp_url": "http://127.0.0.1:9222",
  "profile": "C:\\WINDOWS\\system32\\config\\systemprofile\\.hermes\\chrome_profile"
}
```

**Limitation**: Window is **invisible** (Session 0 fallback). CDP port active, but user cannot interact.

---

## Attempt 3: Debug `run_as_interactive_user` (Pending)
**Issue**: `CreateProcessWithTokenW` path fails silently (no PID returned).
**Diagnosis**:
1. Verify `WTSGetActiveConsoleSessionId()` returns a valid session ID.
2. Check `WTSQueryUserToken` succeeds (Error 1314 if not).
3. Ensure `CreateProcessWithTokenW` is called with correct arguments.

**Next Steps**:
- Test `session_helper.py` functions individually.
- Log session ID and token retrieval steps.

---

## Key Takeaways
1. **Avoid WSL/bash** when Hermes runs as `SYSTEM`. Use `execute_code` or native Python.
2. **Fallback Path**: `subprocess.Popen` works but produces invisible windows.
3. **Persistent Profile**: Chrome profile at `C:\WINDOWS\system32\config\systemprofile\.hermes\chrome_profile` retains sessions.
4. **CDP Control**: Navigate, screenshot, and interact via `http://127.0.0.1:9222`.

---

## Files Involved
- `tools/browser_visible_manager.py`: Main launcher.
- `tools/session_helper.py`: Cross-session process spawning.
- `tools/desktop_screenshot.py`: Screen capture (fails in Session 0).