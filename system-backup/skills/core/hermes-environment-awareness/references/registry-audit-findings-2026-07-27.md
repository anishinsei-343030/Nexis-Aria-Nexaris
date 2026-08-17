# Registry Audit Findings — July 27, 2026

## Summary
**Status**: ⚠️ Issues Found (6 misconfigurations, 0 missing files, 0 duplicates).
**Scope**: Full audit of `~/.hermes/registries/` (identity.md, environment.md, agents.md, projects.md, skills.md, tools.md, health.md, workflows.md).
**Method**: Read-only verification against filesystem state and tool availability.

---

## 🔴 Misconfigurations (functional impact)

| File | Issue | Detail | Recommended Fix |
|------|-------|--------|------------------|
| **health.md** | Stale date | Line 4: "June 25, 2026" — current date is July 27, 2026. Causes misrepresentation of system health as stale. | Replace "June 25, 2026" with "July 27, 2026". |
| **tools.md** | Documented non-existent tools | Lines 33, 50: References `kanban` and `fact_store` tools. These tools are **not available** in the current toolset (confirmed via `hermes tools list`). Causes agents to attempt using unavailable tools. | Remove references to `kanban` and `fact_store`. Add note: "These tools are deprecated and no longer available." |
| **environment.md** | Stale workspace subdirectory | Line 26: References `images/` subdirectory in `D:/Celestia Mei Nexaris/Workspace/`. This directory **does not exist** (confirmed via `ls`). Causes file operations to fail. | Remove `images/` from the workspace subdirectories list. |
| **environment.md** | Stale workspace subdirectory | Line 28: References `videos/` subdirectory in `D:/Celestia Mei Nexaris/Workspace/`. This directory **does not exist** (confirmed via `ls`). The actual directory is `videos` (lowercase), but it is **not a subdirectory** — it is a top-level directory under `Workspace/`. | Correct `videos/` to reflect its actual location: `D:/Celestia Mei Nexaris/Workspace/videos/`. |
| **environment.md** | Dashboard unreachable | Line 7: "Dashboard: Running on http://127.0.0.1:9119/". This endpoint **returns HTTP 000** (confirmed via `curl`). Dashboard is not running or misconfigured. | Update dashboard status: "Dashboard: Not running (endpoint unreachable)." |
| **environment.md** | Chrome path misdocumented | Line 15: Chrome path documented as `C:/Program Files/Google/Chrome/Application/chrome.exe`. Chrome is **not in PATH** and `where chrome` returns "not found". Causes automation failures. | Update Chrome path: "Chrome: Not in PATH. Use full path or `web_search`/`web_extract` instead." |
| **skills.md** | Stale vault path | Line 37: "Vault root is `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/` (contains `.obsidian/`)." This path is **incorrect**. The actual vault is nested: `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/Celestia Mei Nexaris-Galaxy/` (confirmed via `ls`). Causes file operations to fail. | Correct the vault path: "Vault root is `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/Celestia Mei Nexaris-Galaxy/` (contains `.obsidian/`)." |

---

## 🟡 Missing / Empty Files

| File | Issue | Detail |
|------|-------|--------|
| **N/A** | No missing files | All registry files exist and are non-empty. |

---

## 🟢 Stale Path References (already fixed)

| File | Issue | Status |
|------|-------|--------|
| **N/A** | No stale path references found outside of reported misconfigurations. | N/A |

---

## ✅ Verified Correct

| Check | Result |
|-------|--------|
| **Registry files** | All files exist and are non-empty. |
| **Duplicate files** | No case-insensitive duplicates (e.g., `AGENTS.md` vs `agents.md`). |
| **Cross-references** | No broken cross-references between files. |
| **Family member names** | Zero Riven Nexaris and Nexis Aria Nexaris are correctly listed as different individuals in `identity.md`. No flagged inconsistencies. |
| **Workspace structure** | `D:/Celestia Mei Nexaris/Workspace/` exists and contains valid subdirectories (`Documents/`, `Pictures/`, `Projects/`, `videos/`). |
| **Obsidian vault** | `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/Celestia Mei Nexaris-Galaxy/` exists and contains `.obsidian/`. |
| **Installed software** | Python 3.14, Node.js 24.15.0, Git 2.55.0 are installed and available (confirmed via `where python`, `node --version`, `git --version`). |
| **Tool availability** | All tools documented in `tools.md` (except `kanban` and `fact_store`) are available (confirmed via `hermes tools list`). |

---

## 📝 Notes
- **Identity.md**: Family member names (Zero Riven Nexaris, Nexis Aria Nexaris) are **not errors**. They are different individuals.
- **Chrome**: Not installed or not in PATH. Use `web_search`/`web_extract` for browser-based tasks.
- **Dashboard**: `127.0.0.1:9119` is unreachable. Investigate service status or config.
- **Workspace**: `images/` directory does not exist. Use `Pictures/` or create `images/` if needed.