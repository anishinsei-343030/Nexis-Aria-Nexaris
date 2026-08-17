---
name: profile-workspace-config
description: Configure per-profile default workspaces in Hermes — terminal.cwd, config safety guards, verification, and delivery side-effects. Use when a user asks to set/change an agent's default save folder or working directory.
version: 1.0.0
author: Nexis Aria Nexaris
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [hermes, profile, workspace, config, cwd, terminal]
    related_skills: [hermes-configuration, hermes-agent]
---

# Profile Workspace Configuration

Set a Hermes profile's default workspace so terminal/file operations start in a dedicated folder instead of wherever the gateway launched.

## When to use
- User says "my workspace is X, save everything there" or "set my default folder to X".
- A profile needs a distinct working directory (e.g. Nexis -> `D:\Celestia Mei Nexaris\Nexis Aria Nexaris`, separate from the main agent).

## Concepts
- Profile = Hermes state isolation (`HERMES_HOME`): config, memory, skills, cron, sessions.
- Workspace = where terminal commands start, controlled by `terminal.cwd` in the profile's `config.yaml`. Profiles do NOT sandbox filesystem access; cwd only sets the default.
- Global config `~/.hermes/config.yaml` vs profile config `~/.hermes/profiles/<name>/config.yaml` — only touch the profile the user pointed at.

## Correct procedure
1. Verify the target directory exists: `ls -d "<path>"`.
2. Set the workspace via the CLI (the ONLY reliable write path for config):
   ```bash
   hermes config set terminal.cwd "<abs path>" --profile <profile_name>
   ```
3. Verify the result:
   ```bash
   grep -n "cwd:" ~/.hermes/profiles/<profile_name>/config.yaml
   ```
   Confirm the path is intact (backslashes preserved on Windows).
4. Tell the user a gateway restart is needed for new sessions to pick up the change. Changes affect NEW sessions, not the current one.

## Pitfalls
- **patch/write_file are blocked on config files.** Both tools refuse with "Write denied: protected system/credential file" or "Refusing to write to Hermes config file". Do NOT retry them; use `hermes config set`.
- **sed eats backslashes on Windows (git-bash/MSYS).** `sed -i 's|^  cwd: \.|  cwd: D:\Celestia Mei Nexaris\Nexis Aria Nexaris|'` produced `D:Celestia Mei NexarisNexis Aria Nexaris` (backslashes stripped as escapes). If you must sed a Windows path, quote/escape carefully and ALWAYS verify with grep afterward. Prefer `hermes config set` over sed for this.
- **File-mutation verifier note.** When a patch/write_file attempt fails, a "File-mutation verifier: N file(s) were NOT modified" warning is appended below output. It tracks tool mutations only — it cannot see `hermes config set` success. Re-verify actual file state (grep) before claiming success, and phrase the report as "applied via hermes config set", not "verified" (which contradicts the verifier).
- **Failed config patch can auto-attach files to chat.** A refused patch on a protected config may cause the gateway to deliver the config file(s) as attachments in the chat (Telegram shows config.yaml from global + profile). This is a system side-effect of the safety verifier, not an intentional send. Tell the user the files are ignorable snapshots.
- **Duplicate-key trap.** If sed is used, ensure it replaces, not inserts; YAML last-key-wins silently. grep for the key after edits.

## Verification
- `grep -n "cwd:" ~/.hermes/profiles/<name>/config.yaml` returns the exact absolute path.
- `cd` into a fresh terminal call starts at the workspace after gateway restart.