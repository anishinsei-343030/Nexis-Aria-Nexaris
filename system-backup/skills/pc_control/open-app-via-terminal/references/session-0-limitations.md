# Session 0 Limitations (Windows)

## Background
The Hermes terminal runs under the `Administrator` account in **Session 0** (services/headless). The user's desktop is in **Session 1** (or higher). This creates two key limitations:

## Limitation 1: GUI Visibility
Apps launched directly from `terminal()` in Session 0 will start but their GUI windows **will not appear** on the user's desktop in Session 1. The process runs invisible.

**Fix:** Use the Task Scheduler Bridge or PsExec (see SKILL.md Scenario C).

## Limitation 2: Screenshot Capture
`pyautogui.screenshot()` or PowerShell's `CopyFromScreen()` will fail from Session 0 with:
```
Exception calling "CopyFromScreen": "The handle is invalid"
```

This is because Session 0 has no interactive desktop to capture.

**Workarounds:**
- **Not available from Session 0 directly.** The screenshot must be captured from a process running *inside* the user's Session 1.
- Use `browser_vision` tool (Hermes browser) to screenshot a web page the agent navigated to.
- Create a scheduled task that runs a screenshot script in the user's session:
  ```batch
  schtasks /create /tn "CaptureScreenshot" /tr "powershell -File C:\path\to\screenshot.ps1" /sc once /st 00:00 /f /ru AniShinSei_30
  schtasks /run /tn "CaptureScreenshot" /i
  ```
- Use NirCmd (`nircmd.exe savescreenshot C:\path\output.png`) if available, launched via Task Scheduler Bridge.
