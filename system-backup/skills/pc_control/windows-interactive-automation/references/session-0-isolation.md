# Windows Session 0 Isolation & Token Duplication

## Architecture
Windows separates services (Session 0) from user interactive sessions (Session 1, 2, etc.). This prevents services from interacting with the user's desktop for security reasons.

## The `CreateProcessWithTokenW` Pattern
The `session_helper.py` implementation follows this logic:
1. **`WTSGetActiveConsoleSessionId()`**: Identifies which session is currently "plugged into" the physical monitor/keyboard.
2. **`WTSQueryUserToken()`**: Asks the system for the primary access token of the user logged into that session. This requires `SE_TCB_NAME` (Trusted Computer) privileges, which the `SYSTEM` account possesses.
3. **`DuplicateTokenEx()`**: Creates a primary token from the retrieved token to allow process creation.
4. **`CreateProcessWithTokenW()`**: Spawns the process explicitly into the target session using the duplicated token.

## Why `SYSTEM` is Mandatory
If Hermes runs as a standard user (even an Administrator) in Session 0, it does not have the privilege to call `WTSQueryUserToken` for another session. This manifests as a `pywin32` error or a Windows Error 1314. Setting the Task Scheduler task to `NT AUTHORITY\SYSTEM` bypasses this.
