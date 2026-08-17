# Backup & Restore — Identity Persistence

Celestia's identity, memory, and skills survive system wipes through a structured backup pipeline. This reference documents the full lifecycle.

## What Gets Backed Up

| Component | Source Path | Format | Size |
|-----------|------------|--------|------|
| Memories | `~/.hermes/memories/` | Markdown (MEMORY.md, USER.md) | ~50 KB |
| Skills | `~/.hermes/skills/` | Markdown (SKILL.md + ref files) | ~500 KB |
| Cron jobs | `~/.hermes/cron/` | YAML/JSON | ~10 KB |
| Config | `~/.hermes/config.yaml` | YAML (secrets stripped) | ~50 KB |
| SOUL | `~/.hermes/SOUL.md` | Markdown | ~10 KB |
| Fact store | `~/.hermes/memory_store.db` | SQLite → exported as JSON | 1.3 MB → 2 MB JSON |

## Backup Workflow

### Manual Backup

```bash
# Export fact store (read-only — original untouched)
sqlite3 -readonly -json "$HOME/.hermes/memory_store.db" "SELECT * FROM facts;" > "/d/Hermes\Celestia mei Nexaris/Backup/fact_store.json"

# Verify original hash
sha256sum "$HOME/.hermes/memory_store.db"

# Archive everything
tar czf "/d/Hermes\Celestia mei Nexaris/Backup/hermes_backup_$(date +%Y%m%d_%H%M%S).tar.gz" \
  -C "$HOME/.hermes" memories skills cron config.yaml SOUL.md \
  -C "/d/Hermes\Celestia mei Nexaris/Backup" fact_store.json

# Push to GitHub
cd "/d/Hermes\Celestia mei Nexaris/Backup"
git add fact_store.json hermes_backup_*.tar.gz
git commit -m "Hermes backup $(date +%Y%m%d_%H%M%S)"
git push
```

### Automated Script

Location: `D:\Hermes\Celestia mei Nexaris\Backup\backup_hermes.sh`

Run anytime via bash:
```bash
bash "/d/Hermes\Celestia mei Nexaris/Backup/backup_hermes.sh"
```

### Cron (optional)

Schedule weekly or monthly via `cronjob` tool to auto-push backups.

## Fact Store Export Details

### Why SQLite read-only?

- `sqlite3 -readonly` opens DB in immutable mode — no locks, no WAL writes, no journaling
- Use `-json` flag for clean JSON array output
- Each fact includes: `id`, `subject`, `predicate`, `object`, `trust_score`, `created_at`, `updated_at`, `source`, `aliases`

### Verifying Original Untouched

Always run `sha256sum` on `memory_store.db` before and after export. Same hash = no writes.

## Restore from Backup

### Full recovery (fresh Hermes install)

1. Clone the backup repo:
   ```bash
   git clone https://github.com/anishinsei-343030/Celestia-Mei-Nexaris.git
   ```

2. Extract archive:
   ```bash
   tar xzf "Celestia-Mei-Nexaris/Backup/hermes_backup_<latest>.tar.gz" -C ~/.hermes/
   ```

3. Verify ownership and permissions.

4. Restart Hermes.

### Fact store recovery only

```bash
# Parse exported JSON and re-insert (hermes tool or manual sqlite3)
# Requires Hermes running — use skill_manage to load fact-import workflow if needed
```

## Pitfalls

- **Secrets**: `config.yaml` in backup must have secrets stripped — commit only the safe template
- **WAL files**: `memory_store.db-wal` and `memory_store.db-shm` are live state — don't back them up directly
- **File locks**: Never copy `memory_store.db` while Hermes is writing to it — use `-readonly` flag
- **MSYS paths**: On git-bash, use `/d/...` not `D:\...` for shell commands; `D:\...` works in `cmd.exe` only
- **No zip**: git-bash on this system doesn't have `zip`; use `tar.gz` instead
