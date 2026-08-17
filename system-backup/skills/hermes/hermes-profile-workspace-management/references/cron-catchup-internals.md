# Cron Catchup Internals & Workarounds

## The 2-Hour Grace Window (Hard-Coded)

### How It Works

Hermes cron scheduler computes a grace period for missed recurring jobs:

```
grace = period // 2, clamped to [120s, 7200s]
```

- For a daily job (period = 86400s): grace = 43200s = **12 hours**?? — NO. Wait, that would be 12h.

### Correct Behavior

Per GitHub issue #30850 and `cron/scheduler.py`:

```
grace = _compute_grace_seconds(schedule)
if kind in ("cron", "interval") and (now - next_run_dt).total_seconds() > grace:
    new_next = compute_next_run(schedule, now)
    # Job is simply skipped — never executes, no warning
```

The clamp is `[120s, 7200s]` — **max 2 hours** regardless of period. So:
- Daily job missed by >2h → skipped silently, no notification
- Back online within 2h → runs immediately on next tick
- Only recovery outside window: manual `hermes cron run <job_id>`

### Is It Configurable?

**No.** Checked:
- No `cron.grace_seconds` key in config.yaml (only `cron.script_timeout_seconds`, tick interval are settable)
- No env var (only `HERMES_CRON_SCRIPT_TIMEOUT` exists)
- No per-job setting in `cronjob` tool
- Open feature requests: #30850 (queue missed jobs on startup), #27327 (per-job `catchup: boolean`) — both P3Low, unmerged

### Workarounds

1. **Schedule alignment**: Move recurring jobs to times the host is reliably on (evening for a PC that's off overnight)
2. **Manual catch-up**: `hermes cron run <job_id>` after boot
3. **Boot-time catcher**: External script (Windows Task Scheduler at startup) that checks `last_run_at` > 24h ago and triggers `hermes cron run`
4. **Modify source**: Edit `cron/scheduler.py` clamp — works but breaks on every Hermes update

## Cron Script Path Restriction

- `cronjob create` with `script` parameter requires **relative path** under `~/.hermes/profiles/<name>/scripts/`
- Absolute or home-relative paths rejected at creation: "Script path must be relative to ~/.hermes/scripts/"
- **Fix**: Thin wrapper in profile scripts dir:
  ```python
  import subprocess, sys
  REAL = r"D:\path\to\real\script.py"
  res = subprocess.run([sys.executable, REAL], capture_output=True, text=True)
  if res.returncode != 0:
      print(f"failed: {res.stderr or res.stdout}")
      sys.exit(1)
  if res.stdout.strip():
      print(res.stdout.strip())
  sys.exit(0)
  ```
  Exit 0 + empty stdout = silent (no delivery).

## Watchdog Pattern (Irregular-Uptime Hosts)

```
schedule: every 3h (or 2-4h)
no_agent: true
script: workspace_readme_watchdog.py (wrapper)
deliver: local
```

- Script exits 0, empty stdout → nothing sent
- Script prints message → delivered verbatim
- Non-zero exit → error alert (broken watchdog can't fail silently)

## Delivery Verification

Verify bot presence in a Telegram group before trusting cron delivery:
```bash
python3 - <<'EOF'
import os, json, urllib.request, urllib.parse
token = open(os.path.expanduser("~/.hermes/profiles/<name>/.env")).read()
# parse TELEGRAM_BOT_TOKEN
req = urllib.request.Request(f"https://api.telegram.org/bot{token}/getChat",
    data=urllib.parse.urlencode({"chat_id": "-1001234567890"}).encode())
print(json.loads(urllib.request.urlopen(req).read()))
EOF
```

"bot was kicked from the supergroup chat" → bot removed; must re-invite or update delivery target.
