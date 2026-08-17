---
name: hermes-cron-missed-run-handling
description: Guidance on Hermes Agent cron job missed-run behavior and mitigation strategies.
version: 1.0.0
author: Nexis Aria Nexaris
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [cron, scheduling, missed-run, catchup, reliability]
---

# Hermes Cron Missed-Run Handling

## Overview
Hermes cron jobs run only when the gateway is active. If the gateway is offline when a job is scheduled, the scheduler applies a *grace period*:

- Grace = period // 2, clamped to [120s, 7200s] (2‑hour max).
- If the gateway comes back **within** this window, the missed run executes immediately.
- If offline **longer** than the grace period, the run is **silently skipped**.

## Implications
- Daily jobs at 08:00 will not fire if the machine boots after ~10:00.
- Weekly jobs at 18:00 will be skipped if the PC powers on after 20:00.
- No automatic notification is sent for skipped runs.

## Mitigation Strategies
1. **Install the gateway as a persistent Windows service** so it stays up across reboots.
2. **Adjust schedules** to times when the machine is reliably on.
3. **External catch‑up script**: run at boot and invoke `hermes cron run <job_id>` for jobs whose `last_run_at` is older than expected.
4. **Use `catchup` option** (future feature) when available.

## Example Boot‑Catchup Script (Windows PowerShell)
```powershell
# cron_catchup_boot.ps1
$jobs = hermes cron list --json | ConvertFrom-Json
foreach ($job in $jobs) {
    $now = Get-Date -Format s
    $last = [datetime]::Parse($job.last_run_at)
    # Simplified: assume schedule is a fixed interval in seconds (real parsing needed)
    $period = 86400  # placeholder 24h in seconds
    if (($now - $last).TotalSeconds -gt $period) {
        Write-Host "Running missed job $($job.name)..."
        hermes cron run $job.job_id
    }
}
```
Place the script under `scripts/cron_catchup_boot.ps1` and schedule it with Windows Task Scheduler to run at logon.

## Pitfalls
- The script assumes the schedule can be parsed; customize for cron expressions.
- Running missed jobs may cause duplicate actions (e.g., duplicate posts). Ensure the job itself is idempotent or checks state before acting.
- For time‑sensitive actions (e.g., sending a reminder), consider redesigning the logic to tolerate being delayed.

## References
- Hermes Agent issue #30850 (catchup window documentation).
- Hermes docs: https://hermes-agent.nousresearch.com/docs/user-guide/cron.
- `references/agri-quiz-catchup.md` — concrete Windows boot catch-up recipe for the Agri Quiz daily job (includes dual-post guard via `last_post.json`).
