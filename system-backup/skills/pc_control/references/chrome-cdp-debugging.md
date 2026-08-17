# Chrome CDP Debugging

## Verifying CDP Endpoint
```powershell
curl http://127.0.0.1:9922/json/version
```
**Expected output:**
```json
{
   "Browser": "Chrome/149.0.7827.103",
   "Protocol-Version": "1.3",
   "webSocketDebuggerUrl": "ws://127.0.0.1:9922/devtools/browser/c7fe1fd2-..."
}
```

**Failure states:**
- `Connection refused`: Chrome isn't running or port is wrong.
- `404 Not Found`: Chrome is running but without `--remote-debugging-port`.
- `Couldn't connect to server`: Network issue or port blocked.

## Stale PID File Handling
When `browser_navigate` fails with `CDP WebSocket connect failed: IO error: No connection could be made because the target machine actively refused it`:

**DO NOT use `taskkill /f /im chrome.exe`** — it kills ALL Chrome processes including the user's personal browser tabs.

**Safe approach using `Mei_Browser.ps1`:**
1. Check status: `powershell -File "D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1" status`
2. Stop (reads PID file, kills one process): `powershell -File "D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1" stop`
3. Start fresh: `powershell -File "D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1" start`
4. If CDP still fails after restart, ask the user to send `/restart` in Telegram to reload the gateway (picks up env vars from `Hermes_Gateway.cmd`).
5. If still broken, ask the user for guidance — never nuke processes yourself.

## Session 0 Chrome Requirements
- `--no-sandbox`: Required to bypass sandbox errors.
- `--disable-dev-shm-usage`: Prevents shared memory issues.
- `--remote-debugging-port=<port>`: Enables CDP.

## PowerShell Script Tips
- Avoid reserved variables (`$PID`, `$HOME`, `$PSVersionTable`).
- Use `$chromePid` instead of `$pid` for custom PID variable.
- Use `Stop-Process -Force` for reliable termination.
- PID files should be cleaned via `Remove-Item -ErrorAction SilentlyContinue`.
