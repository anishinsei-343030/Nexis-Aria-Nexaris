# Visible Process Launch — Session Isolation Issue

## Session Transcript

**User:** "I still can't see the browser open in my PC though"
**Agent:** Diagnosed Chrome launch (PID 14920, CDP port 9222 active) but window invisible. Screenshot tool failed with `Access is denied`.

**Root Cause:** Hermes runtime context is non-interactive (session `0`), while the user is in an interactive session (`1`).

## Diagnostic Logs

### Chrome Launch (Success)
```json
{
  "success": true,
  "message": "Visible Chrome launched (PID 14920). All browser tools now use this window.",
  "cdp_url": "http://127.0.0.1:9222",
  "profile": "C:\\Users\\Administrator/.hermes/chrome_profile"
}
```

### Screenshot Tool (Failure)
```
Traceback (most recent call last):
  File "<string>", line 3, in <module>
    result = json.loads(handle_desktop_screenshot(None))
  File "C:\Users\Administrator\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\tools\desktop_screenshot.py", line 19, in handle_desktop_screenshot
    sct.shot(output=filepath)
  File "C:\Users\Administrator\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\mss\base.py", line 432, in shot
    return next(self.save(**kwargs))
  File "C:\Users\Administrator\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\mss\base.py", line 423, in save
    sct = self.grab(monitor)
  File "C:\Users\Administrator\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\mss\base.py", line 312, in grab
    img_data_and_maybe_size = self._impl.grab(monitor)
  File "C:\Users\Administrator\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\mss\windows\gdi.py", line 380, in grab
    gdi.BitBlt(memdc, 0, 0, width, height, srcdc, monitor["left"], monitor["top"], SRCCOPY | CAPTUREBLT)
mss.exception.ScreenShotError: Windows graphics function failed: BitBlt: Access is denied.
```

### Session Context
```
C:\> query session
 SESSIONNAME       USERNAME                 ID  STATE   TYPE        DEVICE
 services                                    0  Disc
 console           Administrator              1  Active
```

## Zero's Diagnostic Report

> **Problem:** Chrome window invisible despite `STARTUPINFO(dwFlags=STARTF_USESHOWWINDOW, wShowWindow=SW_SHOW)` and `CREATE_BREAKAWAY_FROM_JOB`.
> **Root Cause:** Process is in session `0` (non-interactive), while the user is in session `1` (interactive).
> **Solution:** Use `WTSQueryUserToken` + `CreateProcessAsUser` or `psexec -i` to launch in the user's session.

## References
- [WTSQueryUserToken Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-wtsqueryusertoken)
- [CreateProcessAsUser Documentation](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera)
- [PsExec Documentation](https://learn.microsoft.com/en-us/sysinternals/downloads/psexec)