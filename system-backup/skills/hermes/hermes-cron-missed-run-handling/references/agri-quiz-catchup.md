# Cron Catch-Up for Agri Quiz (Windows)

Hermes missed-run behavior: gateway offline > grace period (period//2, max 2h) → job silently skipped.

Agri Quiz jobs are cron-scheduled; the daily quiz at 08:00 needs catch-up if PC was off.

## Boot catch-up approach (option 3)

1. Script `cron_catchup_boot.ps1` in `~/.hermes/scripts/`:
   - Parse `hermes cron list --json` (or jobs.json at `~/.hermes/profiles/nexis/cron/jobs.json`).
   - For each enabled recurring job, compare `last_run_at` to now.
   - If `now - last_run_at > expected_period`, run `hermes cron run <job_id>`.

2. Register with Windows Task Scheduler:
   ```powershell
   schtasks /Create /TN "HermesCronCatchup" /TR "powershell -File C:\Users\Administrator\.hermes\scripts\cron_catchup_boot.ps1" /SC ONLOGON /RL HIGHEST
   ```

3. Idempotency: guard against double-post. For AgriQuiz daily, check `last_post.json` before posting again; if today's quiz already posted, exit silently.

## Verification
- `hermes cron status` and `hermes cron list` after boot.
- Check `~/.hermes/profiles/nexis/cron/output/` for job run logs.
- Confirm the quiz message landed in Chaos Control (-1003740504045) once, not twice.
