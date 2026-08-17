# Registry Self-Audit Example

## Input
- **Trigger**: Daily cron job (`b46c12842992`).
- **Files Scanned**: `environment.md`, `tools.md`, `skills.md`, `projects.md`, `identity.md`, `agents.md`.

## Findings

### 🔴 Misconfigurations

| File | Issue | Detail |
|------|-------|--------|
| skills.md | Count mismatch | Header says `(10)` but table lists 11 items. |

### 🟡 Named Persona Mismatches

| File | Issue | Detail |
|------|-------|--------|
| identity.md | Agent names | Uses `Zero Riven Nexaris` / `Nexis Aria Nexaris`. |
| agents.md | Agent names | Uses `Zeros` / `Nexia`. |

### 🟡 Missing Files

| File | Issue | Detail |
|------|-------|--------|
| workflows.md | Does not exist | Referenced in `environment.md` but missing. |
| health.md | Does not exist | Mentioned in memory but never created. |

### 🟢 Stale Path References

| File | Issue | Status |
|------|-------|--------|
| environment.md | Contained 3 stale `wiki/` path references | Already patched to `~/.hermes/registries/`. |

### ✅ Verified Correct

| Check | Result |
|-------|--------|
| `D:/Celestia Mei Nexaris/Workspace/` | ✅ Exists |
| `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/.obsidian/` | ✅ Exists |
| No remaining `wiki/` references | ✅ Clean |

## Fixes Applied

1. **skills.md** — `(10)` → `(11)`.
2. **agents.md** — `Nexia`/`Zeros` → `Nexis Aria Nexaris`/`Zero Riven Nexaris`.
3. **workflows.md** — Created stub.
4. **health.md** — Created stub.
5. **Cron job prompt** — Updated to avoid stale path references.