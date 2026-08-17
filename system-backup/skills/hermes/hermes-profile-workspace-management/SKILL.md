---
name: hermes-profile-workspace-management
description: Manage per-profile workspace configuration, cron scheduling patterns, and git-backed workspace backups for Hermes profiles. Covers terminal.cwd, cron catchup limits, watchdog patterns, and git backup workflows.
version: 1.0.0
author: Nexis Aria Nexaris
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, profile, workspace, cron, git, backup]
    related_skills: [hermes-configuration]
---

# Hermes Profile Workspace & Cron Management

This skill captures patterns for configuring a Hermes profile's workspace, setting up cron jobs that survive irregular uptime, and backing up the workspace to git.

## 1. Per-Profile Workspace (terminal.cwd)

Each profile has its own `config.yaml`. The working directory for terminal/file operations is `terminal.cwd` in that profile's config.

```bash
hermes config set terminal.cwd "D:\path\to\workspace" --profile <name>
grep -n "cwd:" ~/.hermes/profiles/<name>/config.yaml   # verify
```

Effective on NEW sessions (gateway restart needed). Change anytime (e.g. folder renamed).

### Pitfalls

- **Never edit config.yaml with `patch`/`write_file`** — blocked by security guard. Use `hermes config set`.
- **sed mangles Windows backslashes** (eats `\` → `D:Celestia...`). If you use sed, verify with grep and fix via `hermes config set`.
- **File-mutation verifier false alarm**: failed `patch`/`write_file` triggers a yellow "File-mutation verifier" block even if a later `hermes config set` succeeded. The verifier only tracks patch/write tools. Always verify final state with grep and explicitly state the tool-level failure vs command-level success.

## 2. Cron Scheduling Patterns

### Catchup Window (Hard-Coded)

- Grace = `period // 2`, clamped to `[120s, 7200s]` (max 2h). Source: `cron/scheduler.py` `_compute_grace_seconds()`.
- NOT configurable via config.yaml or env (only `cron.script_timeout_seconds` and tick interval are settable).
- Gateway offline past the window → missed run silently skipped. Only recovery: manual `hermes cron run <job_id>`.

### Watchdog Pattern for Irregular-Uptime Hosts

- `no_agent: true` cron whose script exits 0 with EMPTY stdout when nothing changed (silent skip), prints only on change.
- `deliver: local` for fully invisible runs.
- Use `--check` flag in script to report changes without writing.

### Cron Script Path Restriction

- Script path must be relative to profile scripts dir (`~/.hermes/profiles/<name>/scripts/`) — absolute paths rejected.
- If real script lives elsewhere (workspace `scripts/`), write a thin wrapper in profile scripts dir that subprocess-calls the real script.

### Schedule Changes to Recurring Jobs

1. Present full plan: current schedule table, proposed times, inter-job dependencies (e.g., reminder must post AFTER quiz).
2. Ask for exact hour.
3. Update one job at a time with `cronjob update <job_id> --schedule "..."`.
4. Verify with `cronjob list` showing new `next_run_at`.

## 3. Workspace Scaffold & Git Backup

### Standard Folder Structure

```
workspace/
├── README.md            # Legend + auto-generated "Current Structure" tree
├── projects/            # One folder per project (each has local state README.md)
├── scripts/             # Reusable tool scripts (Python, Bash)
├── docs/                # specs/ (WHAT) + process/ (HOW)
├── knowledge/           # Deep research, references, long-form notes
├── assets/              # Media, images, design assets
├── output/              # Final deliverables (family convention)
├── templates/           # Reusable code/doc scaffolds
├── inbox/               # Landing zone for raw/unfiled data
└── archive/             # Versioned backup of completed work
```

### Self-Syncing README

- `scripts/update_workspace_readme.py` scans workspace (depth 2), regenerates `## Current Structure` section in README.md.
- Stores SHA256 of file tree in `.readme_tree_state` — only rewrites README when tree actually changed.
- Run manually after structural changes, and via watchdog cron (every 3h) for changes made externally.

### Git Backup Workflow

1. `git init` in workspace root.
2. `.gitignore` excludes: OS/editor junk, Python caches, large generated data (`batch/*.json`, media), secrets (`*secret*.json`, `*key*.json`).
3. **Exception**: Live data files critical to operation (e.g., `question_bank.json`, `last_post.json`) are un-ignored and committed for restorability.
4. Initial commit + push to GitHub. Future: `git add . && git commit -m "..." && git push` after major changes.

## 4. Memory Consolidation Under Cap Pressure

When `memory` store is near/full (e.g., 3,449/3,000 chars):
- Remove stale/low-value entries (old preferences, superseded details) in the same batch as new adds.
- Prefer `replace` to compress multiple entries into one concise line.
- Preserve high-signal entries: user preferences, environment facts, active protocols.
- Document the consolidation in the commit message or response so the user knows what was trimmed.

## 5. References

- [Workspace Scaffold & Git Backup](references/workspace-scaffold-git-backup.md): Full folder design, README sync script, git backup workflow, memory consolidation notes.
- [Cron Catchup Internals](references/cron-catchup-internals.md): Grace window source code, feature requests for `catchup` option, workarounds.