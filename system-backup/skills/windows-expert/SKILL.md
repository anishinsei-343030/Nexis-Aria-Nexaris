---
name: windows-expert
description: Expert guidance for Windows, PowerShell, WSL interop, and cross-platform development
version: 1.0.0
platforms: [windows, linux, macos]
---

# Windows-expert

## Launching Visible GUI Applications from Session 0

Hermes can launch GUI applications (e.g., browsers, file explorers) from **Session 0** (e.g., when running as a service or via Task Scheduler). However, due to **Session 0 isolation**, the window will be **invisible** to the user unless specific steps are taken.

### Steps to Launch Visible Applications:
1. **Run Hermes as `SYSTEM`** via Task Scheduler:
   ```powershell
   schtasks /change /tn "Hermes_Gateway" /ru SYSTEM
   ```
   *This ensures Hermes has the privileges required for `WTSQueryUserToken`.*

2. Use `CreateProcessWithTokenW` to launch the application in the **interactive user session**.
   - Example: `session_helper.py` provides `run_as_interactive_user()` for this purpose.
   - For browsers, use `--remote-debugging-port=9222` to enable CDP control.

3. Verify the process ID (PID) and CDP port (for browsers):
   ```python
   import requests
   resp = requests.get("http://127.0.0.1:9222/json")
   print(resp.json())  # List of open tabs
   ```

### Pitfalls:
- **$ escaping in git-bash (MSYS)**: When running PowerShell commands through the `terminal` tool (which uses git-bash), every `$` in the PowerShell script must be escaped as `\$`. MSYS consumes unescaped `$` as shell variable expansion, causing syntax errors like `Missing condition in if statement after 'if ('`. Example: `if (\$var)` instead of `if ($var)`. This applies to ALL PowerShell one-liners through the terminal tool.
- **Error 1314**: Occurs if `WTSQueryUserToken` is called by a non-`SYSTEM` user in Session 0. Fix: Run Hermes as `SYSTEM`.
- **Invisible Window**: If the window is still invisible, ensure the Task Scheduler task is configured to run as `SYSTEM` and not "Only when user is logged on."
- **Screenshot Failures**: Direct screen capture from Session 0 fails. Use `run_as_interactive_user()` to spawn a helper script in the user's session (see `desktop_screenshot.py`).
- **WSL_E_LOCAL_SYSTEM_NOT_SUPPORTED**: The `terminal` tool (bash/WSL wrapper) fails when Hermes runs as `SYSTEM`. Fix: Use `execute_code` (native Python) or `subprocess.Popen` (native Windows) to bypass WSL. Example:
  ```python
  from tools.browser_visible_manager import handle_browser_launch_visible
  result = handle_browser_launch_visible(args={})
  ```
- **PowerShell reserved variable conflicts**: Avoid using variable names that shadow PowerShell [automatic variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.4). Common culprits:
  - `$pid` — conflicts with `$PID` (process ID of the current session). Causes `Cannot overwrite variable PID because it is read-only or constant`.
  - `$host` — conflicts with automatic host variable.
  - `$true` / `$false` — reserved.
  - **Fix**: Use descriptive names like `$chromePid`, `$appPid`, `$currentHost`, etc.
  - **Detection**: If a script runs but errors on variable assignment lines, check for reserved name shadowing. The error message explicitly mentions 'read-only or constant'.

### References:
- [Session 0 GUI Launch Guide](references/session-0-gui-launch.md)
- [Visible Chrome Session Transcript (2026-06-14)](references/visible-chrome-session-2026-06-14.md)
- [Verification Script](scripts/verify_chrome_visible.py)
- Provide PowerShell examples alongside bash when relevant
- Use modern PowerShell conventions (cmdlets, pipelines)
- Suggest PowerShell Core (pwsh) for cross-platform scripts
- Help with Registry operations (Get-ItemProperty, Set-ItemProperty)
- Windows Services management
- Task Scheduler for automation
- Windows networking (netsh, Get-NetAdapter)
- NTFS permissions and ACLs
- Path length limitations (260 char limit)
- Case sensitivity differences
- Drive letter handling
- Windows Defender/Firewall interactions
- WSL2 networking quirks (bridge mode, port forwarding)


## Examples

Add examples of how to use this skill here.

## Visible Process Launch

### Pitfall: Non-Interactive Session Isolation
- **Symptoms:** Process launches successfully (PID returned, CDP port active), but window is **not visible** on the user's desktop. Screenshot tools fail with `Access is denied` or `screen grab failed`.
- **Root Cause:** The process is running in a non-interactive session (e.g., background service, SSH, or Hermes's runtime context) where window creation is not mapped to the interactive desktop.
- **Diagnostic Steps:**
  1. Verify process launch: `tasklist | findstr <PID>` (Windows) or `ps aux | grep <PID>` (WSL).
  2. Check session context: `query session` (Windows) or `loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}')` (WSL).
  3. Test screenshot: Run `desktop_screenshot` tool — if it fails with `Access is denied`, the process is not in the interactive session.

### Solution: Session-Aware Process Creation
- **Preferred Method:** Use `WTSQueryUserToken` + `CreateProcessAsUser` to launch the process in the **active desktop session** of the logged-in user.
  - Example (C++):
    ```cpp
    #include <Windows.h>
    #include <WtsApi32.h>
    #pragma comment(lib, "WtsApi32.lib")

    void LaunchVisibleProcess() {
        HANDLE hToken = NULL;
        if (WTSQueryUserToken(WTSGetActiveConsoleSessionId(), &hToken)) {
            STARTUPINFO si = { sizeof(si) };
            PROCESS_INFORMATION pi;
            si.lpDesktop = "winsta0\\default";
            CreateProcessAsUser(hToken, "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
            CloseHandle(hToken);
        }
    }
    ```
  - **Note:** Requires `SE_INCREASE_QUOTA_NAME` and `SE_ASSIGNPRIMARYTOKEN_NAME` privileges.

- **Fallback Method:** Use `psexec -i` to force the process into the interactive session.
  - Example:
    ```powershell
    psexec -i 1 -d "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
    ```
  - **Note:** `psexec` must be installed and available in `PATH`. Session ID (`-i 1`) may vary — use `query session` to confirm.

- **Workaround for Hermes:** If the above methods are unavailable, restart Hermes in the user's interactive session (e.g., via Task Scheduler with "Run only when user is logged on").

### Evidence
- **Chrome Launch:** PID + CDP port active, but window invisible.
- **Screenshot Tool:** Fails with `Access is denied` (PIL) or `screen grab failed` (mss).
- **Session Context:** `query session` shows Hermes running in session `0` (services), while the user is in session `1` (interactive).

### References
- See `references/visible-process-launch.md` for session transcripts and diagnostic logs.

## Notes

- This skill was auto-generated
- Edit this file to customize behavior
