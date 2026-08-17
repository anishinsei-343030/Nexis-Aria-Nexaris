# schtasks Bridge — Launch Visible GUI Apps from Session 0

Verified working technique for launching GUI apps into the user's desktop (Session 1) when Desktop Session Agent is unavailable.

## Prerequisites

- Hermes running as `NT AUTHORITY\SYSTEM` (sessions registered in Task Scheduler)
- Target user identified via `qwinsta` (look for `>console` row, note ID and username)
- `schtasks` available at `C:\Windows\system32\schtasks`

## The Pattern

### Step 1: Identify the active user session

```bash
qwinsta
```

Output:
```
SESSIONNAME       USERNAME                 ID  STATE   TYPE        DEVICE
services                                    0  Disc
>console           AniShinSei_30             1  Active
```

Key: `ID=1`, `USERNAME=AniShinSei_30`.

### Step 2: Write a .bat script

Git Bash (MSYS) corrupts `/create` flags in `schtasks` — the shell interprets `/create` as a path under `/c/`. **Do NOT run schtasks directly from bash.** Always wrap in a `.bat` file.

```batch
schtasks /create /tn "Celestia_App_Launch" /tr "C:\Program Files\Google\Chrome\Application\chrome.exe" /sc once /st 00:00 /f /ru AniShinSei_30 /it
schtasks /run /tn "Celestia_App_Launch" /i
schtasks /delete /tn "Celestia_App_Launch" /f
```

Template variables to fill:
- `"Celestia_App_Launch"` — unique task name (change per invocation to avoid collisions)
- `/tr` — the exe path wrapped in **plain double quotes**: `"C:\Program Files\...\app.exe"` or `"C:\Program Files\...\app.exe --flag"`
- ⚠️ **Do NOT use single quotes** — `"'path'"` fails silently (`/create` succeeds but task points to a nonexistent path starting with `'`)
- `/ru` — target username from `qwinsta`
- `/ru` — target username from `qwinsta`
- `/it` — **critical flag**: runs the task in the interactive session, making the window visible

### Step 3: Execute via cmd.exe /c

```bash
cmd.exe /c "C:\path\to\launch_script.bat" 2>&1
```

This bypasses Git Bash shell interpretation and runs the batch file through the Windows command processor.

## Templates

### scripts/launch-app.bat — generic template

```batch
schtasks /create /tn "%~n0" /tr "'%~1'" /sc once /st 00:00 /f /ru %2 /it
schtasks /run /tn "%~n0" /i
schtasks /delete /tn "%~n0" /f
```

Usage from Hermes terminal:
```bash
# Write the .bat (one-time per app), then:
cmd.exe /c "C:\Users\Administrator\.hermes\temp\launch-app.bat" "C:\Program Files\Google\Chrome\Application\chrome.exe" AniShinSei_30
```

## Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `schtasks` command garbled | Git Bash interprets `/create` as path `/c/create` | Use `.bat` file + `cmd.exe /c` |
| Task created but window invisible | Missing `/it` flag on `schtasks /create` | Add `/it` |
| Task created but window invisible | Wrong `/ru` username | Check `qwinsta` — user might be in Session 2+ |
| "Access is denied" on `/create` | Hermes not running as SYSTEM | Check Task Scheduler config |
| No output from `cmd.exe /c` | Batch ran but `schtasks` output went to Windows console, not bash pipe | Check `tasklist | grep chrome` to verify |
| "WARNING: The task will be created..." | Normal for `/create` with `/it` | Confirm with Y (no interaction needed from .bat) |

## Verification

```bash
tasklist | grep -i chrome
```

Process count should increase by 1 (or more if `--new-window` spawned multiple).

## Why Not Use Desktop Session Agent?

The Hermes Desktop Session Agent is the preferred approach, but:
- It requires explicit setup (separate `schtasks` process itself)
- It adds ~10s initialization latency on first call
- Not all Hermes installations have it configured

The schtasks bridge is simpler, zero-setup, and verified to work. Use it for one-shot app launches.
