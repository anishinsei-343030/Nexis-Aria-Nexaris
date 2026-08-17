# Workspace Scaffold & Git Backup Reference

Complete specification for the Nexis Aria Nexaris workspace folder structure, self-syncing README pattern, and git-backed backup workflow.

## 1. Folder Structure Rationale

| Folder | Purpose | Why It Exists |
|--------|---------|---------------|
| `projects/` | One folder per active project | Each project has local state README.md — no need to rely on agent memory for continuity |
| `scripts/` | Reusable automation scripts | Separated from project code — tools vs products |
| `docs/specs` | Requirements, ideas (WHAT) | Agent reading specs needs requirements context |
| `docs/process` | Plans, how-tos (HOW) | Agent reading plans needs step sequence |
| `knowledge/` | Deep research, references | Large context exceeding Hermes memory char limits |
| `assets/` | Media, images, design assets | Binary/large files not suitable for memory |
| `output/` | Final deliverables | Family convention (matches Celestia's Workspace/output) |
| `templates/` | Reusable scaffolds | Starting points for new projects |
| `inbox/` | Landing zone for raw data | Prevents root clutter — "Misc" = chaos per research |
| `archive/` | Versioned backup of completed work | Reversible over delete — matches "verify before delete" rule |

**Dropped from standard patterns:** `memory/` (redundant with Hermes profile memory), `SOUL.md` (already in profile).

## 2. Self-Syncing README Pattern

**File:** `scripts/update_workspace_readme.py`

### Features
- Scans workspace to depth 2, skips junk dirs (`__pycache__`, `.git`, `.venv`, `node_modules`, etc.)
- Generates tree in markdown code block under `## Current Structure`
- Stores SHA256 hash of file tree in `.readme_tree_state` (same dir as script)
- Only rewrites README.md when tree hash differs → silent no-op when unchanged
- CLI: `python update_workspace_readme.py` (writes), `python update_workspace_readme.py --check` (reports only)

### Integration
1. **Manual**: Run after creating/renaming/deleting folders
2. **Watchdog cron**: Every 3h, `no_agent: true`, delivers `local` — catches external changes (Explorer drag-drop, other agents)

## 3. Git Backup Workflow

### Initial Setup
```bash
cd D:\Hermes\Nexis Aria Nexaris
git init
git config user.name "Nexis Aria Nexaris"
git config user.email "nexis@nexaris.local"
git remote add origin https://github.com/anishinsei-343030/Nexis-Aria-Nexaris.git
```

### .gitignore Strategy

**Exclude:**
- OS/editor junk (`.DS_Store`, `Thumbs.db`, `*.swp`, `.vscode/`, `.idea/`)
- Python caches (`__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.env`)
- Node/JS caches (`node_modules/`, `npm-debug.log*`)
- Large generated data: `batch/*.json` (weekly seed files), media (`*.wav`, `*.ogg`, `*.mp4`)
- Secrets: `*secret*.json`, `*key*.json`, `*token*.json`
- Runtime state: `*.pid`, `*.lock`, `*.state`

**Include (un-ignored):**
- `question_bank.json` — core quiz data, live state per AGENTS.md ("never hand-edit")
- `last_post.json` — posting state
- All structural files: README, scripts, docs, templates

### Commit Cadence
- Initial scaffold commit (this session)
- After adding new project folders
- After significant script/template changes
- Periodic `git add . && git commit -m "sync" && git push` (manual or scheduled)

### Restore Procedure
```bash
git clone https://github.com/anishinsei-343030/Nexis-Aria-Nexaris.git
cd Nexis-Aria-Nexaris
# Workspace ready — run update_workspace_readme.py to regenerate tree
```

## 4. Memory Consolidation Under Cap Pressure

When memory store hits 3,000 char limit:

### Removal Candidates (low signal, high volume)
- Old preference notes superseded by newer rules
- One-time setup details no longer needed (e.g., old relay preference after "prefer web tools" rule)
- Redundant FB link notes (already in profile fact)
- Registry/config edit details covered by "propose then approve" rule

### Compression via Replace
- Merge multiple entries on same topic into one concise line
- Keep: user preferences, environment facts, active protocols, cron rules

### This Session's Consolidation
- Removed: "Shin's FB URL" (112 chars), "Registry/config edits" (144 chars), "Guest/Restricted tier" (156 chars), "Vault path for Celestia" (158 chars)
- Replaced: "Cardinal rule" entry with compact version (saved ~40 chars)
- Added: "Workspace README auto-refresh" rule (101 chars)
- Updated: AgriQuiz entry with new path (net +20 chars)
- Result: 3,449 → 2,994 chars (within 3,000 limit)