# Full System Health Check

Covers: tools, runtimes, gateway, workspace, disk, memory, backup system, browsers.
Run on user request ("do a health check") or when troubleshooting.

## Procedure

### 1. Date / Timestamp
```bash
date +'%B %d, %Y'
```

### 2. Runtimes
```bash
where python   # Python 3.x
where node     # Node.js
where git      # Git
where docker   # Docker (optional — may not be installed)
```

### 3. Browsers in PATH
```bash
where chrome   # Usually not in PATH on Windows — OK
where msedge
where firefox
```
Note: absence from PATH does NOT mean unavailable. Desktop browser may be accessible via Playwright/CDP (Mei_Browser.ps1).

### 4. Workspace Structure
```bash
ls -la /d/Celestia\ Mei\ Nexaris/Workspace/
```
Check expected dirs: Artwork, Audio, Video, Scripts, Documents, Backup, Output, Projects, System_Backup.

### 5. Gateway Health
```bash
hermes gateway status
```
Expected: PID running, scheduled task Ready.

### 6. System Resources
```bash
systeminfo | grep -i "total physical memory" -m1   # RAM
df -h /d/ | tail -1                                 # D: drive free space
```

### 7. Backup System
```bash
# Verify script exists and is executable
ls -la /d/Celestia\ Mei\ Nexaris/Workspace/Scripts/git_auto_backup.sh

# Verify git remote
cd /d/Celestia\ Mei\ Nexaris/Workspace && git remote -v

# Verify cron job active
cronjob action=list  # look for backup job ID 18a916fcdb3e
```

### 8. Output Format

```
**🟢 Category** — check1 ✅, check2 ✅
**🟡 Category** — check ⚠️ (minor note)
**🔴 Category** — check ❌ (requires attention)
```

Use bullet format (Telegram — no tables).

## Common Healthy State

| Component | Expected |
|-----------|----------|
| Python | 3.14+ |
| Gateway PID | Running |
| D: drive | ≥40 GB free |
| Workspace | All subdirs present |
| Backup script | Executable, git remote configured |
| Cron (backup) | Active, every 2h schedule, 72h dedup |
