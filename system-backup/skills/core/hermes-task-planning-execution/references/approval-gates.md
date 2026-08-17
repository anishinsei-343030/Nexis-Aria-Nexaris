# Approval Gates: Registry and Cron Job Workflow

## Purpose
Ensure the user retains explicit control over high-impact changes — especially registry files and cron jobs — by enforcing a **propose-then-approve** workflow.

## Trigger Conditions
Apply approval gates for:
- **Registry files**: `identity.md`, `environment.md`, `projects.md`, `tools.md`, `skills.md`
- **Cron jobs**: Any change to an existing job or creation of a new one
- **File deletions**: Any file or folder removal
- **System config changes**: Edits to `.env`, `config.yaml`, or other critical configs
- **Edits outside the current working directory**: Any file modification outside the session's `workdir`

## Workflow

### 1. Propose Changes
- Present the **exact change** (e.g., diff, file path, impact).
- Example for registry files:
  ```markdown
  Proposed change to `environment.md`:
  ```diff
  - Python packages: pandas, selenium, beautifulsoup4
  + Python packages: pandas, selenium, beautifulsoup4, numpy
  ```
  Impact: Adds `numpy` to the documented environment.
  ```
- Example for cron jobs:
  ```markdown
  Proposed change to cron job `b46c12842992` (Daily Registry Self-Audit):
  - Prompt: Updated to enforce `write_file`/`patch` execution (not just reporting).
  - Skills: Added `hermes-memory-management` for registry updates.
  ```

### 2. Wait for Explicit Approval
- Use `clarify` to ask for approval:
  ```
  clarify("Proceed with the proposed change? Reply 'Approved' to confirm.")
  ```
- Do **not** proceed without the user's explicit "Approved" or "Proceed".

### 3. Execute and Verify
- Apply the change using the appropriate tool (`patch`, `write_file`, `cronjob`).
- Provide **evidence** of the change:
  - For files: `diff` output or `ls -laR` before/after.
  - For cron jobs: `cronjob(action="list")` output.
  - For registry files: `read_file` of the updated content.

## Pitfalls
- **False Claims**: Never claim a change was applied without evidence. Always verify and show the result.
- **Approval Bypass**: Never assume approval. Always wait for explicit confirmation.
- **Silent Failures**: If a change fails, report the error immediately and propose a fix.
- **Registry Staleness**: If a registry file is outdated, propose updates and wait for approval before applying.
- **Untrusted Audit Reports**: Cron audit reports are self-generated and can be wrong — sometimes on most of their claims. Never propose or apply changes based solely on an audit report's assertions. Always verify each claim against:
  - The actual filesystem (`ls`, `read_file`, `search_files`)
  - The system prompt's Holographic Memory header for infrastructure-layer tools
  - Loaded skills and their references
  - The user, if still uncertain
  - Pattern: an audit claimed AGENTS.md was a duplicate (file didn't exist), claimed stale vault paths (paths were already correct), and claimed fact_store was non-existent (it's critical infrastructure). Every claim needed independent verification.

## Examples

### Example 1: Registry Update
1. **Propose**:
   ```markdown
   Proposed change to `tools.md`:
   ```diff
   - image_gen: Disabled by default
   + image_gen: Enabled (Stability AI backend)
   ```
   Impact: Enables image generation via Stability AI.
   ```
2. **Wait for Approval**:
   ```
   clarify("Proceed with the proposed change to `tools.md`? Reply 'Approved' to confirm.")
   ```
3. **Execute and Verify**:
   ```bash
   patch(path="wiki/registries/tools.md", old_string="image_gen: Disabled by default", new_string="image_gen: Enabled (Stability AI backend)")
   ```
   ```bash
   read_file(path="wiki/registries/tools.md")
   ```

### Example 2: Cron Job Update
1. **Propose**:
   ```markdown
   Proposed change to cron job `b46c12842992` (Daily Registry Self-Audit):
   - Prompt: Updated to enforce `write_file`/`patch` execution.
   - Skills: Added `hermes-memory-management`.
   ```
2. **Wait for Approval**:
   ```
   clarify("Proceed with the proposed change to cron job `b46c12842992`? Reply 'Approved' to confirm.")
   ```
3. **Execute and Verify**:
   ```bash
   cronjob(action="update", job_id="b46c12842992", prompt="Updated prompt...")
   ```
   ```bash
   cronjob(action="list")
   ```

## Notes
- Approval gates are **non-negotiable** for registry files and cron jobs.
- Always provide **evidence** after execution to confirm the change was applied.
- If the user rejects a proposal, discard the change and do not retry unless new information arises.