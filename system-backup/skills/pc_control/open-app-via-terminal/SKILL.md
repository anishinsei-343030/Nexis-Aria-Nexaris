---
name: open-app-via-terminal
description: Opens applications on the user's Windows PC using terminal commands via Git Bash (MSYS).
authors:
  - Celestia Mei Nexaris
enabled: true
tags:
  - pc_control
  - apps
  - terminal
  - windows
version: 2.0.0
---

# Open App Via Terminal (Windows) — DEPRECATED

> **⚠️ This skill is partially deprecated for Hermes on Windows.**
>
> **Context**: Hermes runs in **Session 0** (SYSTEM context). Direct Git Bash commands like `start` and raw `schtasks` fail because MSYS shell interprets their flags as paths. However, `cmd.exe /c` + `.bat` files **do work** — the schtasks bridge pattern (Scenario C below) is verified and functional.
>
> **Preferred approach**: Use the **Hermes Desktop Session Agent** (`windows-ui-automation` skill) when available. It provides direct desktop tools (`keyboard_hotkey`, `window_list`, etc.).
>
> **When to use this skill**: Use Scenario C (schtasks bridge) when the Session Agent is unavailable and you need a one-shot GUI app launch.

This skill documents how to open apps via Git Bash (MSYS) terminal on Windows, but **it does not work in Hermes** due to Session 0 constraints.

## Application Path Lookup

On Windows, Git Bash does NOT have apps in PATH by default. Use these ordered methods to find an app:

1. **`where <exe_name>`** — queries Windows PATH. Works for apps registered in system PATH.
2. **`ls /c/Program\ Files/<vendor>/`** — check common install locations for Chrome (`Google/Chrome/Application/chrome.exe`), Edge (`Microsoft/Edge/Application/msedge.exe` under `Program Files` or `Program Files (x86)`).
3. **`search_files` tool** with `file_glob="<app>.exe"` under `C:\Program Files\` and `C:\Program Files (x86)\`.

### Known install paths (Windows defaults)

| App       | Typical Path                                                                 |
|-----------|------------------------------------------------------------------------------|
| Chrome    | `C:\Program Files\Google\Chrome\Application\chrome.exe`                      |
| Edge      | `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`               |
| Notepad   | `C:\Windows\System32\notepad.exe`                                            |
| Terminal  | `C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\wt.exe`                 |
| Calculator| `C:\Program Files\WindowsApps\...` (requires shell: protocol — use `start shell:AppsFolder\Microsoft.WindowsCalculator_8wekyb3d8bbwe!App`) |

## Launch Commands by Scenario

### Scenario A: App is NOT already running
```bash
# Use the full path directly
"C:\Program Files\Google\Chrome\Application\chrome.exe"
```

### Scenario B: App IS already running (ProcessSingleton lock)
When the app is already open, starting a second instance fails with:
```
Lock file can not be created! Error code: 32
Failed to create a ProcessSingleton...
```

**Fix:** Use `start` with `--new-window` to request a new window from the existing instance:
```bash
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window "about:blank"
```

### Scenario C: Launching from a Non-Interactive Session (Session 0 -> Session 1)
If the app starts but the window is invisible, use the **Task Scheduler Bridge** to target the user's active session:

1. **Get the active session ID and username**:
   ```bash
   qwinsta
   ```
   Look for the `>console` row and note the `ID` and `USERNAME` (e.g., `AniShinSei_30`).

2. **Task Scheduler Bridge** (recommended for Hermes):
   - **Critical**: Do NOT run `schtasks` directly from Git Bash — the shell interprets `/create` as a path under `/c/`. Instead, write a `.bat` file and execute it via `cmd.exe /c`.
   - Create a temporary task:
     ```batch
     schtasks /create /tn "HermesLaunch" /tr "'full_path_to_exe'" /sc once /st 00:00 /f /ru <username> /it
     ```
   - Run it interactively:
     ```batch
     schtasks /run /tn "HermesLaunch" /i
     ```
   - Delete the task:
     ```batch
     schtasks /delete /tn "HermesLaunch" /f
     ```
   - Example `.bat` file:
     ```batch
     schtasks /create /tn "Celestia_Chrome_Launch" /tr "'C:\Program Files\Google\Chrome\Application\chrome.exe'" /sc once /st 00:00 /f /ru AniShinSei_30 /it
     schtasks /run /tn "Celestia_Chrome_Launch" /i
     schtasks /delete /tn "Celestia_Chrome_Launch" /f
     ```
   - Execute via:
     ```bash
     cmd.exe /c "C:\path\to\launch_chrome.bat" 2>&1
     ```

   **Pitfall: Git Bash Shell Interpretation**
   `schtasks` commands often fail in Git Bash due to the shell interpreting the `/create` flag as a path (e.g., `/C/Program Files/Git/create`). Wrap commands in a batch file (`.bat`) or use `cmd.exe /c` to bypass the Git Bash shell.

3. **PsExec** (alternative):
   ```bash
   psexec -i <session_id> -u <username> "full_path_to_exe"
   ```
   Replace `<session_id>` with the ID from `qwinsta` and `<username>` with the target user (e.g., `AniShinSei_30`).


## Pre-launch Checks

Before launching, always check if the app is already running:
```bash
tasklist | grep -i "<process_name>"
```
- If running: use Scenario B (--new-window or start)
- If not running: use Scenario A (direct exe path)

## Pitfalls

- **`start` without full path** (`start chrome`) often fails in Git Bash because the app's directory is not in the MSYS PATH. Always resolve the full path first.
- **Chrome/Edge profile lock**: You cannot launch a second instance of the same browser profile. A `--user-data-dir=<path>` flag can work around this but creates a separate profile. Prefer existing instance + new window.
- **Background & operator**: Do NOT use `&` in foreground terminal commands — the Hermes terminal tool blocks this and returns an error. Use `start ""` instead for GUI apps that should detach.
- **Admin-elevated apps**: Some apps (e.g., system utilities) need admin rights and will silently fail from a non-elevated Git Bash. Check exit code.
- **Session 0 Isolation**: Processes running in Session 0 (e.g., Hermes terminal) cannot directly interact with GUI apps in Session 1 (user desktop). Use the **Task Scheduler Bridge** or **PsExec** to target the user's session.

## Verification

After launch, verify with:
```bash
tasklist | grep -i "<process_name>"
```
The process count should increase, confirming a new instance or window was created.
