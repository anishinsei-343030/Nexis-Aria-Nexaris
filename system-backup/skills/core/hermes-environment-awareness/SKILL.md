---
name: hermes-environment-awareness
description: Maintain awareness of the execution environment (OS, tools, directories, resources) and verify availability before performing tasks.
---

# Hermes Environment Awareness

## Core Principle
*You operate within a real execution environment.*

Before performing a task, **understand the environment** in which the task will occur. Never assume — verify whenever possible.

---

## Trigger Conditions
Use this skill **before every task** or when:
- The user requests an action that depends on environment resources.
- You need to verify software, tools, or directory availability.
- You are unsure about the operating system, runtime, or workspace structure.
- The task involves file operations, code execution, or automation.

---

## Environment Assessment Procedure

### 1. Consult the Environment Registry
- Load `registries/environment.md` to retrieve authoritative environment details (OS, shell, user, tools, directories).
- Use this as the baseline for all subsequent checks.

### 2. Identify the User's Goal
Clarify the user's objective. If ambiguous, use `clarify` to confirm.

### 2. Determine Relevant Environment Resources
List the environment resources that may be involved:
- **Operating System**: Windows, Linux, macOS
- **Development Tools**: Python, Node.js, Git, Docker, package managers
- **Browsers**: Chrome, Edge, Firefox, browser automation tools
- **File System**: User directories, project directories, workspaces, Obsidian vaults
- **Agent Resources**: Installed skills, tool registry, memory systems, Kanban boards
- **External Services**: APIs, GitHub, cloud services, databases

### 3. Check Available Software
Verify installed software:
```bash
# Windows (via git-bash/MSYS)
where python       # Check Python
where node         # Check Node.js
where git          # Check Git
where docker       # Check Docker
where chrome       # Check Chrome
where msedge       # Check Edge
where firefox      # Check Firefox

# Linux/macOS (if applicable)
which python
which node
which git
which docker
```

### 4. Check Available Tools
List available tools:
```bash
hermes tools list
```
- Confirm required tools are enabled.
- Note any disabled or missing tools.

### 5. Check Workspace Locations
Verify known workspace paths and **resolve stale references** before use:
```bash
# Verify workspace root (resolve stale paths like 'D:/Celestia Mei Nexaris/Workspace/')
WORKSPACE_ROOT="$(ls -d /d/Hermes/Celestia\ mei\ Nexaris/ 2>/dev/null || ls -d D:/Hermes/Celestia\ mei\ Nexaris/ 2>/dev/null || ls -d /d/Celestia\ Mei\ Nexaris/Workspace/ 2>/dev/null || ls -d D:/Celestia\ Mei\ Nexaris/Workspace/ 2>/dev/null || echo "D:/Hermes/Celestia mei Nexaris/")"
ls -la "$WORKSPACE_ROOT"  # Backup, psychology-voice, system-backup, archive, assets, audio, docs, inbox, knowledge, output, projects, scripts, templates

# Verify current Obsidian vault (resolve stale paths like 'D:/Celestia Mei Nexaris/wiki/')
VAULT_ROOT="$(ls -d /d/Celestia\ Mei\ Nexaris/Celestia\ Mei\ Nexaris-Galaxy/Celestia\ Mei\ Nexaris-Galaxy/ 2>/dev/null || ls -d D:/Celestia\ Mei\ Nexaris/Celestia\ Mei\ Nexaris-Galaxy/Celestia\ Mei\ Nexaris-Galaxy/ 2>/dev/null || echo "D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/Celestia Mei Nexaris-Galaxy/")"
ls -la "$VAULT_ROOT"  # Current vault

# Verify legacy vault (if exists)
ls -la "D:/Celestia Mei Nexaris/wiki/" 2>/dev/null  # Legacy vault (verify existence)

ls -la "$HOME/.hermes/"  # Hermes resources
```

### 5.1 Workspace Path Verification
- **Purpose**: Resolve stale path references (e.g., `D:/Celestia Mei Nexaris/Workspace/` vs `/d/Celestia Mei Nexaris/Workspace/`) before file operations.
- **Detection**: Use `ls -d` with fallback paths to detect the **actual workspace root**.
- **Fix**: Update registries (`environment.md`, `identity.md`) to reflect the resolved path:
  ```bash
  patch --mode replace --path "~/.hermes/registries/environment.md" --old_string "D:/Celestia Mei Nexaris/Workspace/" --new_string "$WORKSPACE_ROOT"
  ```
- **Prevention**: Always verify workspace paths with `ls -d` before referencing them in tasks or registries.

### 6. Check Required Permissions
Verify permissions for file operations, code execution, or automation:
```bash
# Check write permissions
touch "$WORKSPACE_ROOT/test_permissions.txt" && rm "$WORKSPACE_ROOT/test_permissions.txt"
```

### 7. Determine the Best Execution Strategy
Select the best approach based on the environment:
- **Code Execution**: Use `execute_code` or `terminal` (Python, Node.js, etc.).
- **File Operations**: Use `read_file`, `write_file`, `search_files`.
- **Automation**: Use `cronjob`, `delegate_task`, or scripts.
- **Browser Actions**: Use `browser_navigate`, `browser_click`.

### 8. Gateway Health Check (layered procedure)
When the user restarts the gateway or reports Telegram connectivity issues:

1. **Process confirmation**: `hermes gateway status` — confirm PID exists, `gateway_state.json` shows `"running"`.
2. **Platform connectivity**: Check `gateway_state.json` → `platforms.telegram.state` should be `"connected"`.
3. **Port binding**: `netstat -ano | grep <port>` (default 7700). Some configs expose no HTTP endpoint — Telegram polling works without it.
4. **Config validation**: Check `telegram.token` exists in `config.yaml`. If missing, the bot cannot authenticate.
5. **Logs**: Review `~/.hermes/logs/gateway.log` for startup errors.

Present evidence per `hermes-agent-orchestration` → **Verification** section.

### 9. Execute
Execute the task using the selected approach. Monitor progress and verify outcomes.

---

## Environment Categories

### Operating System
- **Windows** (current environment)
- Linux (WSL, if applicable)
- macOS (not applicable)

### Development Tools
- **Python**: Available (current runtime)
- **Node.js**: Verify with `where node`
- **Git**: Verify with `where git`
- **Docker**: Verify with `where docker`
- **Package Managers**: `pip`, `npm`, `choco` (Windows)

### Browsers
- **Chrome**: Verify with `where chrome`
- **Edge**: Verify with `where msedge`
- **Firefox**: Verify with `where firefox`
- **Browser Automation Tools**: `agent-browser`, `browser_navigate`

### File System
- **User Directories**: `C:/Users/Administrator/`
- **Project Directories**: `D:/Hermes/Celestia mei Nexaris/`
- **Workspaces**: `D:/Hermes/Celestia mei Nexaris/`
  - Subdirectories: `archive`, `assets`, `audio`, `docs`, `inbox`, `knowledge`, `output`, `projects`, `scripts`, `templates`, `Backup`, `psychology-voice`, `system-backup`
- **Obsidian Vaults**: `D:/Obsidian/Nexaris Galaxy/` (current vault; verify with `ls -la` before assuming)
- **Downloads**: `C:/Users/Administrator/Downloads/`
- **Documents**: `C:/Users/Administrator/Documents/`

### Agent Resources
- **Installed Skills**: List with `hermes skills list`
- **Tool Registry**: List with `hermes tools list`
- **Memory Systems**: `memory`, `session_search` (note: `fact_store` is deprecated — removed from toolset)
- **Task Queues**: `todo` tool (note: `kanban` is deprecated — removed from toolset)

### External Services
- **APIs**: OpenRouter, OpenAI, Exa, Firecrawl, Tavily
- **GitHub**: `gh` CLI, `github` tools
- **Cloud Services**: Cloudflare, AWS, Google Cloud
- **Databases**: SQLite, PostgreSQL, MySQL (if configured)
- **Remote Resources**: APIs, web services

---

## Environment Rules

### Before Recommending Software
- Determine if it is already installed.
- Example: Check `where python` before suggesting Python installation.

### Before Writing Code
- Determine which runtime is available.
- Example: Use `execute_code` for Python, `terminal` for shell scripts.

### Before Suggesting File Locations
- Check known workspace paths.
- Example: Use `D:/Hermes/Celestia mei Nexaris/assets/images/` for image files.

### Before Proposing Automation
- Determine available automation tools.
- Example: Use `cronjob` for scheduled tasks, `delegate_task` for subagents.

### Before Declaring a Limitation
- Verify that the required resource is unavailable.
- Example: Check `where git` before stating Git is not installed.

---

## Known Environment Memory
Maintain awareness of:
- **Operating System**: Windows (current), Linux (WSL if applicable)
- **Telegram Bot Environment**:
  - **Gateway Log Location**: `/d/Hermes/Celestia mei Nexaris/Backup/.hermes/logs/gateway.log`
  - **Privacy Mode**: Defaults to **on** (bots ignore users who haven’t DM’d them first).
  - **Debugging Command**:
    ```bash
    grep '<user_id>' "/d/Hermes/Celestia mei Nexaris/Backup/.hermes/logs/gateway.log" | tail -n 20
    ```
- **Installed Software**: Python, Node.js, Git, Docker, browsers
- **Development Tools**: `pip`, `npm`, `choco`
- **Workspace Locations**: `D:/Hermes/Celestia mei Nexaris/`, `D:/Obsidian/Nexaris Galaxy/` (current vault)
- **Obsidian Vault**: `D:/Obsidian/Nexaris Galaxy/` (verify path — legacy at `D:/Celestia Mei Nexaris/wiki/`)
- **Project Directories**: `D:/Hermes/Celestia mei Nexaris/`
- **Frequently Used Resources**: APIs, GitHub, Cloudflare

---

### Registry Pitfalls

### Stale Path References
- **Symptom**: Registries reference old paths (e.g., `wiki/registries/`, `C:/Users/Administrator/wiki/`, `D:/Celestia Mei Nexaris/wiki/`).
- **Fix**: Use `search_files` to find all references, then `patch` to update them to the correct path (e.g., `~/.hermes/registries/` or `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/`).
- **Prevention**: Always use `~/.hermes/registries/` as the canonical path for registry files. For Obsidian vaults, verify the current path with:
  ```bash
  ls -la "D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/"
  ```

### Stale Workspace Subdirectory References
- **Symptom**: `environment.md` lists workspace subdirectories that no longer exist or have been renamed (e.g., `images/` vs `Pictures/`).
- **Impact**: Tasks fail when attempting to use outdated paths for file operations.
- **Fix**: Sync `environment.md` with actual workspace structure:
  ```bash
  ls -la "D:/Hermes/Celestia mei Nexaris/"
  ```
  Update `environment.md` to match the current subdirectories.
- **Prevention**: Run a monthly cron job to audit workspace paths and update `environment.md`.

### Stale Vault Path References
- **Symptom**: Registries reference legacy vault paths (e.g., `D:/Celestia Mei Nexaris/wiki/` or `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/` without nested vault).
- **Impact**: File operations fail when targeting the wrong vault path.
- **Fix**: Update all references to the current vault path:
  ```bash
  D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/Celestia Mei Nexaris-Galaxy/
  ```
  Verify with:
  ```bash
  ls -la "D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/Celestia Mei Nexaris-Galaxy/.obsidian"
  ```
- **Prevention**: Always verify the vault path before file operations. Use `search_files` to find stale references.

### Path Format Inconsistencies
- **Symptom**: Registries or tools document paths with inconsistent slashes (e.g., `D:\path\file.png` vs `D:/path/file.png` vs `/d/path/file.png`).
- **Impact**: File operations fail due to path format mismatches, especially in cross-platform or MSYS/git-bash environments.
- **Fix**: Standardize all paths to **absolute POSIX-style** (e.g., `/d/path/file.png` for MSYS/git-bash compatibility). Update registries and tool documentation:
  ```bash
  # Example: Update Telegram MEDIA paths
  patch --mode replace --path "~/.hermes/registries/identity.md" --old_string "D:/path/file.png" --new_string "/d/path/file.png"
  ```
- **Prevention**: Always use POSIX-style paths in registries and tool documentation. Test paths in the target environment before use.

### Naming Inconsistencies
- **Symptom**: Agent names differ across files (e.g., `Nexia` vs `Nexis Aria Nexaris`, `Zeros` vs `Zero Riven Nexaris`).
- **Fix**: Standardize names in `identity.md` and `agents.md`. Use `patch` to update all occurrences.
- **Prevention**: Always cross-reference `identity.md` when updating agent names.
- **Note**: **Zero Riven Nexaris** and **Nexis Aria Nexaris** are **different individuals**. Do NOT flag their names as inconsistencies.

### Documented Non-Existent Tools
- **Symptom**: A tool is listed in `tools.md` but does not exist in the current Hermes toolset (e.g., `fact_store`, `kanban`).
- **Impact**: Agents attempt to use unavailable tools, causing failures.
- **Resolution**:
  1. Verify tool existence with `hermes tools list`.
  2. Remove the tool from `tools.md` or replace it with a verified alternative.
  3. If the tool is planned but not yet implemented, mark it as "(Planned)" or "(Deprecated)".
- **Prevention**: Cross-check `tools.md` against `hermes tools list` during audits.

### Case-Insensitive Duplicate Files
- **Symptom**: Multiple files with the same purpose but different case (e.g., `AGENTS.md` and `agents.md` on Windows).
- **Impact**: Both files appear in directory listings but reference the same inode. Tools may read/write the wrong file, causing confusion.
- **Fix**: Identify the authoritative file (e.g., `agents.md`). Delete the duplicate using `rm` with the exact case:
  ```bash
  rm "~/.hermes/registries/AGENTS.md"
  ```
- **Prevention**: Always use `ls -la` to check for case-insensitive duplicates before creating new registry files. Enforce lowercase filenames for consistency.

### Outdated Dates
- **Symptom**: Registry files contain stale "last check" or audit dates (e.g., `June 25, 2026` in `health.md`).
- **Impact**: Misrepresents system health as stale, eroding trust in registry accuracy.
- **Fix**: Update dates to reflect the current audit:
  ```bash
  patch --mode replace --path "~/.hermes/registries/health.md" --old_string "June 25, 2026" --new_string "$(date +'%B %d, %Y')"
  ```
- **Prevention**: Automate date updates during registry audits using `date +'%B %d, %Y'`.

---

For extended details on these and other pitfalls, refer to [`references/registry-audit-pitfalls.md`](references/registry-audit-pitfalls.md).
- **Note**: **Zero Riven Nexaris** and **Nexis Aria Nexaris** are **different individuals**. Do NOT flag their names as inconsistencies.

### Missing Registry Files
- **Symptom**: A registry file is referenced in another file but does not exist (e.g., `workflows.md`, `health.md`).
- **Fix**: Create a stub file with a placeholder header:
  ```markdown
  # <Registry Name>
  
  *(None registered yet — add content as needed.)*
  ```
- **Prevention**: After creating a new registry file, update all cross-references.

### Documented Non-Existent Tools
- **Symptom**: A tool is listed in `tools.md` but does not exist in the current Hermes toolset (e.g., `fact_store`, `kanban`).
- **Impact**: Agents attempt to use unavailable tools, causing failures.
- **Resolution**:
  1. Verify tool existence with `hermes tools list`.
  2. Remove the tool from `tools.md` or replace it with a verified alternative.
  3. If the tool is planned but not yet implemented, mark it as "(Planned)" or "(Deprecated)".
- **Prevention**: Cross-check `tools.md` against `hermes tools list` during audits.

### Case-Insensitive Duplicate Files
- **Symptom**: Multiple files with the same purpose but different case (e.g., `AGENTS.md` and `agents.md` on Windows).
- **Impact**: Both files appear in directory listings but reference the same inode. Tools may read/write the wrong file, causing confusion.
- **Fix**: Identify the authoritative file (e.g., `agents.md`). Delete the duplicate using `rm` with the exact case:
  ```bash
  rm "~/.hermes/registries/AGENTS.md"
  ```
- **Prevention**: Always use `ls -la` to check for case-insensitive duplicates before creating new registry files. Enforce lowercase filenames for consistency.

---

## Failure Modes To Avoid

### 1. Assuming Software is Installed
- Always verify software availability before recommending or using it.
- Example: Check `where python` before writing Python code.

### 2. Assuming Software is Missing
- Never assume software is missing without verification.
- Example: Check `where git` before stating Git is not installed.

### 3. Ignoring Existing Workspace Structure
- Always check known workspace paths before suggesting file locations.
- Example: Use `D:/Hermes/Celestia mei Nexaris/assets/images/` for image files.

### 4. Forgetting Known Directory Locations
- Maintain awareness of project directories, workspaces, and Obsidian vaults.
- Example: Use `D:/Celestia Mei Nexaris/wiki/` for Obsidian-related tasks.

### 5. Recommending Tools Already Available
- Always check the tool registry before suggesting new tools.
- Example: Use `web_search` instead of suggesting a new web research tool.

### 6. Recommending Tools Incompatible with the Environment
- Never recommend tools incompatible with the OS or runtime.
- Example: Do not recommend `apt-get` on Windows.

---

### 6. Ignoring Registry Hygiene
- Always run the **Registry Self-Audit Procedure** after modifying registries.
- Example: After updating agent names, verify consistency across `identity.md`, `agents.md`, and `skills.md`.

### 10. Documented Non-Existent Tools
- **Symptom**: A tool is listed in `tools.md` but does not exist in the current Hermes toolset (e.g., `fact_store`).
- **Impact**: Agents attempt to use unavailable tools, causing failures.
- **Resolution**:
  1. Verify tool existence with `hermes tools list`.
  2. Remove the tool from `tools.md` or replace it with a verified alternative.
  3. If the tool is planned but not yet implemented, mark it as "(Planned)" or "(Deprecated)".
- **Prevention**:
  - Cross-check `tools.md` against `hermes tools list` during audits.
- **Symptom**: All tools (terminal, browser, web_extract, etc.) return `"Interrupted"` or `"Command interrupted"` with exit code 130. No tools work, even `echo`.
- **Cause**: The Hermes session was killed or restarted (e.g., gateway crash, user `/stop`, system restart).
- **Detection**:
  - Try a harmless command (e.g., `echo "test"`). If it fails with `"Interrupted"`, the session is dead.
  - Check gateway status: `hermes gateway status` (if available).
- **Recovery**:
  1. **Restart the gateway** (if needed): `/restart` in Telegram.
  2. **Restart dependent services** (e.g., Playwright browser):
     ```bash
     powershell -File "D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1" -Command stop
     powershell -File "D:\Celestia Mei Nexaris\playwright\Mei_Browser.ps1" -Command start
     ```
  3. **Verify readiness**: Run a simple tool call (e.g., `browser_navigate` to `https://www.google.com`).
  4. **Resume task**: Retry the original task from the last known good state.
- **Pitfall**: Do **not** assume the issue is tool-specific. If all tools fail, the **entire session** is dead — not just one component.
- **Symptom**: Cron job prompts reference stale paths or outdated procedures.
- **Fix**: Update the cron job prompt to reflect current paths and workflows.
- **Prevention**: After updating registries, review all cron job prompts for staleness.

---

### Registry Self-Audit Procedure

### Purpose
Ensure registry consistency, accuracy, and completeness. Run this procedure **daily** or after any registry modification.

### Registry Self-Audit Report Structure
Always use this structure for the **Registry Scan Report** to ensure consistency and clarity:

```markdown
## Registry Scan Report

### 🔴 Misconfigurations (functional impact)
| File | Issue | Detail |
|------|-------|--------|

### 🟡 Named Persona Mismatches
| File | Issue | Detail |

### 🟡 Missing / Empty Files
| File | Issue | Detail |

### 🟢 Stale Path References (already fixed)
| File | Issue | Status |

### ✅ Verified Correct
| Check | Result |
```

### Critical Rules for Registry Audits
1. **READ ONLY** — Never modify, delete, or create files during an audit. Report only.
2. **Identity.md context** — `identity.md` legitimately lists family member names (Zero Riven Nexaris, Nexis Aria Nexaris) under "Available Agents". These are **not errors, conflicts, or inconsistencies** — do not flag them.
3. **Different names for different people** — It is normal for Zero and Nexis to have different name prefixes. Do **not** flag "Nexis vs Zero prefixes" as a mismatch. They are different individuals.
4. **Reference Files** — Check for missing reference files in `~/.hermes/registries/references/`. Create stubs if missing.
5. **Workspace Paths** — Always verify workspace paths with `ls -la` before reporting. Update registries to reflect the **actual root** (e.g., `/d/Zero/`).
6. **Tool Existence** — Cross-check `tools.md` against `hermes tools list` or `which <tool>`. Remove or mark non-existent tools as "(Deprecated)".

### Reference Files
- **Location**: `~/.hermes/registries/references/`
- **Purpose**: Session-specific detail (e.g., audit findings, error transcripts) and condensed knowledge banks.
- **Required Files**:
  - `registry-audit-pitfalls.md`
  - `memory-audit-recipe.md`
  - `retrieval-strategy.md`
  - `duplicate-patterns.md`
- **Action**: Create stubs if missing:
  ```bash
  mkdir -p ~/.hermes/registries/references/
  echo "# Registry Audit Pitfalls\n\n*(None documented yet.)*" > ~/.hermes/registries/references/registry-audit-pitfalls.md
  ```

### Critical Rules for Registry Audits
1. **READ ONLY** — Never modify, delete, or create files during an audit. Report only.
2. **Identity.md context** — `identity.md` legitimately lists family member names (Zero Riven Nexaris, Nexis Aria Nexaris) under "Available Agents". These are **not errors, conflicts, or inconsistencies** — do not flag them.
3. **Different names for different people** — It is normal for Zero and Nexis to have different name prefixes. Do **not** flag "Nexis vs Zero prefixes" as a mismatch. They are different individuals.

### Registry Pitfalls (Extended)
- **Duplicate Registry Files (Case-Insensitive Filesystem)**:
  - **Symptom**: Multiple files with the same purpose but different case (e.g., `AGENTS.md` and `agents.md` on Windows).
  - **Impact**: Both files appear in directory listings but reference the same inode. Tools may read/write the wrong file, causing confusion.
  - **Fix**: Identify the authoritative file (e.g., `agents.md`). Delete the duplicate using `rm` with the exact case:
    ```bash
    rm "~/.hermes/registries/AGENTS.md"
    ```
  - **Prevention**: Always use `ls -la` to check for case-insensitive duplicates before creating new registry files. Enforce lowercase filenames for consistency.

- **Stale Workspace Paths in Registries**:
  - **Symptom**: Registries reference workspace paths (e.g., `D:/Celestia Mei Nexaris/Workspace/`) that do not exist on disk. Actual workspace may be at `/d/Zero/Workspace/` or another location.
  - **Impact**: File operations fail when targeting non-existent paths.
  - **Detection**: Use `ls -la <path>` or `test -d <path>` to verify path existence before use.
  - **Fix**: Update registries to reflect the **actual workspace root** (e.g., `/d/Zero/`). Use `patch` to replace stale paths:
    ```bash
    patch --mode replace --path "~/.hermes/registries/environment.md" --old_string "D:/Celestia Mei Nexaris/Workspace/" --new_string "/d/Zero/Workspace/"
    ```
  - **Prevention**: Always verify workspace paths with `ls -la` before referencing them in registries or tasks.

- **Documented Non-Existent Tools**:
  - **Symptom**: Tools listed in `tools.md` (e.g., `kanban`, `fact_store`) do not exist in the current toolset.
  - **Impact**: Agents attempt to use unavailable tools, causing failures.
  - **Detection**: Cross-check `tools.md` against `hermes tools list` or `which <tool>`.
  - **Fix**: Remove or mark tools as "(Deprecated)" in `tools.md`.
  - **Prevention**: Audit `tools.md` during registry self-audits to ensure alignment with the active toolset.

- **Missing Reference Files**:
  - **Symptom**: Reference files (e.g., `registry-audit-pitfalls.md`, `memory-audit-recipe.md`) are missing from `~/.hermes/registries/references/`.
  - **Impact**: Agents cannot access session-specific detail or condensed knowledge banks.
  - **Fix**: Create the `references/` directory and populate with stub files:
    ```bash
    mkdir -p ~/.hermes/registries/references/
    echo "# Registry Audit Pitfalls\n\n*(None documented yet.)*" > ~/.hermes/registries/references/registry-audit-pitfalls.md
    ```
  - **Prevention**: After creating a new reference file, update all cross-references in registries and skills.

- **Stale Workspace Subdirectory References**:
  - **Symptom**: `environment.md` lists workspace subdirectories that no longer exist or have been renamed (e.g., `images/` vs `Pictures/`).
  - **Impact**: Tasks fail when attempting to use outdated paths for file operations.
  - **Fix**: Sync `environment.md` with actual workspace structure:
    ```bash
    ls -la "D:/Hermes/Celestia mei Nexaris/"
    ```
    Update `environment.md` to match the current subdirectories.
  - **Prevention**: Run a monthly cron job to audit workspace paths and update `environment.md`.

- **Documented Non-Existent Tools**:
  - **Symptom**: A tool is listed in `tools.md` but does not exist in the current Hermes toolset (e.g., `fact_store`).
  - **Impact**: Agents attempt to use unavailable tools, causing failures.
  - **Resolution**:
    1. Verify tool existence with `hermes tools list`.
    2. Remove the tool from `tools.md` or replace it with a verified alternative.
    3. If the tool is planned but not yet implemented, mark it as "(Planned)" or "(Deprecated)".
  - **Prevention**: Cross-check `tools.md` against `hermes tools list` during audits.

### Steps
1. **Load Registry Files**
   - Read all markdown files in `~/.hermes/registries/`.

2. **Check Consistency**
   - Compare content across files for contradictions (e.g., skill counts, agent names, paths).
   - Example: `skills.md` vs `agents.md` for agent naming.

3. **Check Path References**
   - Verify all file paths referenced in registries actually exist on disk.
   - Use `ls -la <path>` or `search_files` to confirm.

4. **Report Issues**
   - List mismatches, stale paths, or inconsistencies.
   - Format:
     ```markdown
     | File | Issue | Detail |
     |------|-------|--------|
     | skills.md | Count mismatch | Header says 10, table lists 11 |
     ```

5. **Recommend Fixes**
   - For each issue, suggest the exact fix needed (e.g., `patch`, `write_file`, or manual edit).

6. **Create Missing Files**
   - If a registry file is referenced but missing, create a stub:
     ```markdown
     # <Registry Name>
     
     *(None registered yet — add content as needed.)*
     ```

### Output Format
```markdown
## Registry Scan Report

### 🔴 Misconfigurations (functional impact)

| File | Issue | Detail |
|------|-------|--------|

### 🟡 Named Persona Mismatches

| File | Issue | Detail |

### 🟡 Missing / Empty Files

| File | Issue | Detail |

### 🟢 Stale Path References (already fixed)

| File | Issue | Status |

### ✅ Verified Correct

| Check | Result |
```

---

### Full System Health Check

When the user requests a **full system health check** ("do a health check", "check system status", "verify everything is working"), follow the procedure in [`references/full-system-health-check.md`](references/full-system-health-check.md).

### External Report Verification

When the user (or another agent) supplies a structured audit/report claiming specific file issues (line-level, count mismatches, stale dates, misconfigurations):

#### Workflow
1. **Parse the report into individual claims** — each file reference, line number, and issue is a separate claim.
2. **For each claim, verify directly against filesystem state:**

   - Read the exact file at the reported path.
   - If not found, expand search across known directories (Workspace, Vault, registry paths, user home, `.hermes/registries/`).
   - If still not found, report the discrepancy — the report may reference a file that doesn't exist, lives at a different path, or belongs to a different system.

3. **Classify each claim:**
   - **CONFIRMED** — file exists at expected path, issue matches actual content.
   - **PARTIALLY CONFIRMED** — file exists but issue partially correct (e.g., wrong line number, different severity).
   - **NOT FOUND** — file not found at reported path nor anywhere on system.
   - **WRONG SYSTEM** — file belongs to a different project, repo, or registry set than the one being audited.

4. **Do not assume the report is authoritative** — a report can mix genuine findings with stale data, wrong-path references, or issues from a different environment.
5. **Report results back to the user** with confirmation status per claim. Ask for path clarification on NOT FOUND items before declaring them non-existent.

#### Pitfalls
- **Blind trust**: Treating a third-party report as ground truth without verification. Each claim is a hypothesis until confirmed.
- **Narrow search**: Giving up after checking one path. An audit report may reference stale paths from an older setup.
- **False negative**: Telling the user a file doesn't exist when it lives at a different path. Always expand search before concluding.
- **Over-investigation**: Searching indefinitely when the report clearly references a different project's files. Ask the user early.

---

## Environment Rule
Before every task, ask:

*"What environment resources are available that can help accomplish this goal?"*

Then plan accordingly.

---

## Examples

### Example 5: Registry Self-Audit
1. **Goal**: Audit registry consistency and accuracy.
2. **Environment Check**: Verify `~/.hermes/registries/` exists and contains all expected files.
3. **Approach**: Follow the **Registry Self-Audit Procedure** (see above).
4. **Execution**:
   - Load all registry files.
   - Check for consistency, path references, and missing files.
   - Report issues and recommend fixes.
5. **Result**: Registry is consistent and up-to-date.

See [`references/registry-audit-findings-2026-07-27.md`](references/registry-audit-findings-2026-07-27.md) for the latest audit report.

---

## Notes

### Example 1: User Asks to Run a Python Script
1. **Goal**: Execute a Python script.
2. **Environment Check**: Verify Python is installed (`where python`).
3. **Approach**: Use `execute_code` or `terminal` to run the script.
4. **Execution**:
   ```python
   execute_code("print('Hello, World!')")
   ```
5. **Result**: The script runs successfully.

### Example 2: User Asks to Save an Image
1. **Goal**: Save an image to a workspace directory.
2. **Environment Check**: Verify `D:/Hermes/Celestia mei Nexaris/assets/images/` exists.
3. **Approach**: Use `write_file` to save the image to the directory.
4. **Execution**:
   ```python
   write_file("D:/Hermes/Celestia mei Nexaris/assets/images/example.png", image_data)
   ```
5. **Result**: The image is saved to the correct location.

### Example 3: User Asks to Schedule a Task
1. **Goal**: Schedule a daily task.
2. **Environment Check**: Confirm `cronjob` tool is available.
3. **Approach**: Use `cronjob` to schedule the task.
4. **Execution**:
   ```python
   cronjob(action="create", prompt="Generate a daily briefing", schedule="0 9 * * *")
   ```
5. **Result**: The task is scheduled successfully.

### Example 4: User Asks to Search for a File
1. **Goal**: Search for a file in the workspace.
2. **Environment Check**: Verify `D:/Hermes/Celestia mei Nexaris/` exists.
3. **Approach**: Use `search_files` to find the file.
4. **Execution**:
   ```python
   search_files(pattern="example.txt", path="D:/Hermes/Celestia mei Nexaris/")
   ```
5. **Result**: The file is found or confirmed missing.

---

## Notes
- This skill is **mandatory** for all tasks involving environment assessment or execution.
- Always verify the environment before acting.
- Update this skill whenever new tools, software, or workspace paths are discovered or created.