---
name: pc_control
description: PC-level control — browsers, GUI automation, Windows session management. Umbrella for controlling desktop applications from Session 0.
version: 1.0.0
platforms: [linux, macos, windows]
---

# PC Control — User Interaction Rules

**Cardinal Rule: Explicit Approval for Irreversible Actions**

- **Always confirm** before editing, deleting, or moving files — even if the action is a rollback or seems safe.
- Present the **exact proposed change** (e.g., file diff, command) and wait for explicit approval ("proceed"/"approved").
- Never batch changes; propose one at a time for individual review.

---

# PC Control — Browser Inventory Reference

### Managing Chrome via PowerShell Scripts

When running Chrome via custom PowerShell scripts (e.g., `D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1`):

1.  **Launch Chrome with correct flags**:
    -   `--remote-debugging-port=<port>`: Essential for CDP connection.
    -   `--no-sandbox`, `--disable-dev-shm-usage`: Often required for Chrome in Session 0/service contexts to prevent crashes.
    -   `--user-data-dir=<path>`: Specifies the profile directory for session persistence.

2.  **Verify CDP Connectivity**:
    -   Use `curl http://127.0.0.1:<port>/json/version` to confirm the CDP endpoint is live.
    -   An empty or 404 response means debug mode isn't active or the port is blocked.

### CRITICAL PITFALL: Never use `taskkill /f /im chrome.exe`

This command kills ALL Chrome processes on the machine, including the user's personal browser with all their tabs, causing irrecoverable data loss. **Strictly forbidden.**

**Correct browser management with `Mei_Browser.ps1`:**

- **Script location**: `D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1` (moved from `D:\Celestia\Mei_Browser.ps1`)
- **Start your Chrome**: `powershell -Command "& 'D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1' start"`
- **Stop only your Chrome** (reads PID file, kills one process): `powershell -Command "& 'D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1' stop"`
- **Check status**: `powershell -Command "& 'D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1' status"`
- **Check your specific PID**: `Get-Process -Id (Get-Content D:\\Celestia Mei Nexaris\\playwright\\chrome.pid)`

**IMPORTANT**: When calling from bash (git-bash/MSYS), use single quotes inside the `-Command` string and `&` to invoke: `powershell -Command "& 'D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1' start"`. The old syntax `D:\Celestia\...` fails because bash treats `:` as a path separator.

**CDP fallback when `browser_navigate` fails but Chrome is running:**
- Create a new tab: `browser_cdp(method='Target.createTarget', params={'url':'about:blank'})` — returns `targetId`
- Navigate in that tab: `browser_cdp(method='Page.navigate', params={'url':'<url>'}, target_id='<targetId>')`
- Verify title: `browser_cdp(method='Runtime.evaluate', params={'expression':'document.title','returnByValue':true}, target_id='<targetId>')`
- Then use `browser_navigate` normally after the tab exists

If the browser is broken or unresponsive, **ask the user for guidance** before taking drastic action. Never guess.

**After env var changes in `Hermes_Gateway.cmd`:** Ask the user to send `/restart` in Telegram to reload the gateway before testing.

### CDP Connectivity Fails After Restart
Chrome is live on the port but `browser_navigate` gets 404 / connection refused:
1. Verify via `curl http://127.0.0.1:9922/json/version` — look for `webSocketDebuggerUrl`
2. If Chrome is there but tool can't connect, check if gateway needs `/restart` (env vars stale)
3. **Fallback via raw CDP** (works even when `browser_navigate` / `browser_vision` fail):
   - List existing tabs: `browser_cdp(method='Target.getTargets')`
   - Create a new tab: `browser_cdp(method='Target.createTarget', params={'url':'about:blank'})` → returns `targetId`
   - Navigate: `browser_cdp(method='Page.navigate', params={'url':'<url>'}, target_id='<targetId>')`
   - Check state: `browser_cdp(method='Runtime.evaluate', params={'expression':'document.title','returnByValue':true}, target_id='<targetId>')`
   - Execute JS: `browser_cdp(method='Runtime.evaluate', params={'expression':'<js>'}, target_id='<targetId>')`
4. If `Target.getTargets` returns no `page` targets and only `service_worker` targets, Chrome may have been launched without a default tab. Create one via `Target.createTarget`.
5. **`browser_vision` will also fail** in this state — screenshot depends on the same auto-connected session. Use CDP `Page.captureScreenshot` as an alternative if vision is needed.

3.  **Handle Stale Processes and PID Files**:
    -   Scripts should check for existing PID files and Chrome processes.
    -   Gracefully kill stale processes via script (not `taskkill /im`).

4.  **PowerShell Variable Conflicts**:
    -   Avoid using variable names that conflict with PowerShell's [automatic variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.4) (e.g., `$PID`).
    -   Rename conflicting variables (e.g., `$chromePid` instead of `$pid`).

5.  **Browser Tool Interaction**:
    -   If `BROWSER_CDP_URL` is set, ensure the browser tool connects to the existing instance and doesn't attempt to auto-launch.
    -   If the tool defaults to auto-launch, consider temporarily renaming the tool or patching its configuration to prioritize the CDP URL.
    -   After env var changes in Hermes_Gateway.cmd, ask the user to send `/restart` to reload the gateway before testing.

