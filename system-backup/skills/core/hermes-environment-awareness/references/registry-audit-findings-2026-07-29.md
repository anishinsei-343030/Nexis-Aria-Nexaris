# Registry Audit Findings — July 29, 2026

## Summary
Read-only audit of Hermes registries. Found 7 misconfigurations, 1 missing directory, 1 outdated date, and 1 case-insensitive duplicate file.

## Findings

### 🔴 Misconfigurations
| File | Issue | Detail |
|------|-------|--------|
| **environment.md** | Stale workspace paths | Lines 24-25, 31, 35: Reference `D:/Celestia Mei Nexaris/` and subdirs (`Workspace/`, `Celestia Mei Nexaris-Galaxy/`). These paths **do not exist** on disk. Actual workspace is `/d/Zero/Workspace/`. |
| **environment.md** | Stale vault path | Lines 31, 35: Reference `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/` as Obsidian vault. No vault found at this path. No `.obsidian/` directory found anywhere on `/d/` or `/c/Users/Administrator/`. |
| **skills.md** | Stale vault path | Line 37: References `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/` for `obsidian` skill. No vault exists. |
| **tools.md** | Documented non-existent tools | Line 33: Lists `kanban` and `fact_store` as available tools. These tools **do not exist** in the current toolset. |
| **health.md** | Outdated date | Line 4: "June 25, 2026" — stale by 4 days. Current date: July 29, 2026. |
| **registries/** | Case-insensitive duplicate files | `AGENTS.md` and `agents.md` are **the same file** (same inode, size, content). Windows filesystem is case-insensitive. |
| **registries/** | Missing reference files | All reference files (`registry-audit-pitfalls.md`, `memory-audit-recipe.md`, `retrieval-strategy.md`, `duplicate-patterns.md`) **do not exist** in `~/.hermes/registries/references/`. |

### 🟡 Missing / Empty
| File | Issue | Detail |
|------|-------|--------|
| **workflows.md** | Empty workflows section | Lines 46-51: "Workflow Conventions" section exists, but no active workflows documented beyond the 5 listed. |
| **~/.hermes/registries/references/** | Missing directory | Directory does not exist. |

### ✅ Verified Correct
- All registry files exist: `identity.md`, `environment.md`, `agents.md`, `projects.md`, `skills.md`, `tools.md`, `health.md`, `workflows.md`.
- `AGENTS.md` and `agents.md` are identical. No content mismatch.
- Core skills count: 11 (matches `hermes skills list`).
- Telegram MEDIA paths use POSIX-style forward slashes (e.g., `D:/path`).
- Gateway log location: `~/.hermes/logs/gateway.log` exists and is writable.
- Hermes profile: `default` active. No cross-profile issues.

## Recommended Fixes
1. Update stale workspace/vault paths in `environment.md` and `skills.md` to `/d/Zero/Workspace/`.
2. Delete `AGENTS.md` (keep `agents.md`).
3. Update `health.md` date to "July 29, 2026".
4. Remove or mark `kanban` and `fact_store` as "(Deprecated)" in `tools.md`.
5. Create `~/.hermes/registries/references/` and populate with stub files for missing references.
6. Audit workspace subdirectories in `/d/Zero/Workspace/` and update `environment.md`.

## Session Context
- **Workspace Root**: `/d/Zero/` (not `D:/Celestia Mei Nexaris/`).
- **Obsidian Vault**: None found on system.
- **Tools**: `kanban` and `fact_store` do not exist (verified via `which`).
- **Filesystem**: Windows (case-insensitive).