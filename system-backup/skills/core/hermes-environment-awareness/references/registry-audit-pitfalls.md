# Registry Audit Pitfalls

## Documented Non-Existent Tools
- **Symptom**: A tool is listed in `tools.md` but does not exist in the current Hermes toolset (e.g., `fact_store`, `kanban`).
- **Impact**: Agents attempt to use unavailable tools, causing failures.
- **Detection**:
  ```bash
  hermes tools list | grep -i "fact_store\|kanban" || echo "NOT_FOUND"
  ```
- **Resolution**:
  1. Remove the tool from `tools.md` or mark it as "(Deprecated)".
  2. Add a **Deprecated Tools** section to `workflows.md` with migration guidance:
     ```markdown
     ## Deprecated Tools
     - **fact_store**: Removed from toolset. Migrate to `memory` or `session_search`.
     - **kanban**: Removed from toolset. Use `todo` for task lists.
     ```
- **Prevention**: Cross-check `tools.md` against `hermes tools list` during every registry audit.

## Stale Path References
- **Symptom**: Registries reference old paths (e.g., `D:/Celestia Mei Nexaris/wiki/`, `wiki/registries/`).
- **Impact**: File operations fail when using outdated paths.
- **Detection**:
  ```bash
  grep -r "wiki/" ~/.hermes/registries/
  ```
- **Resolution**:
  1. Update all references to the current vault path:
     ```bash
     patch("~/.hermes/registries/environment.md", "D:/Celestia Mei Nexaris/wiki/", "D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/")
     ```
  2. Verify the new path exists:
     ```bash
     ls -la "D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/"
     ```
- **Prevention**: Use `ls -la` to verify paths before referencing them in registries.

## Case-Insensitive Duplicate Files
- **Symptom**: Multiple files with the same purpose but different case (e.g., `AGENTS.md` and `agents.md` on Windows).
- **Impact**: Tools may read/write the wrong file, causing confusion.
- **Detection**:
  ```bash
  ls -la ~/.hermes/registries/ | grep -i "\.md$"
  ```
- **Resolution**:
  1. Identify the authoritative file (e.g., `agents.md`).
  2. Delete the duplicate:
     ```bash
     rm "~/.hermes/registries/AGENTS.md"
     ```
- **Prevention**: Enforce lowercase filenames for all registry files.

## Memory Capacity Stalled
- **Symptom**: `MEMORY.md` exceeds `memory_char_limit` (e.g., 3050/3000 chars).
- **Impact**: New entries fail to save, causing data loss.
- **Detection**:
  ```bash
  wc -c ~/.hermes/memories/MEMORY.md
  ```
- **Resolution**:
  1. Identify the lowest-value entry (e.g., stale environment facts).
  2. Remove it:
     ```python
     memory(action="remove", target="memory", old_text="<unique substring>")
     ```
  3. If still over limit, consolidate related entries into a single shorter entry.
- **Prevention**: Run monthly memory audits to stay under limits.

## Registry Self-Audit Report Gaps
- **Symptom**: Audit reports omit **documented non-existent tools** or **stale workflow references**.
- **Impact**: Agents continue to use deprecated tools or outdated procedures.
- **Detection**:
  - Check `tools.md` for tools not listed in `hermes tools list`.
  - Check `workflows.md` for references to deprecated tools.
- **Resolution**:
  1. Add a **Deprecated Tools** section to `workflows.md`.
  2. Update the **Registry Self-Audit Procedure** to explicitly check for:
     - Tools listed in `tools.md` but not in `hermes tools list`.
     - Workflows referencing deprecated tools.
- **Prevention**: Include tool verification in every audit.