---
name: hermes-profile-management
description: Manage Hermes Agent profiles — per-profile configuration (workspace dirs, providers), config file editing safeguards, and profile isolation semantics. Use when setting up or changing a profile's default workspace, config keys, or when profile config edits are refused.
version: 1.0.0
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [hermes, profiles, config, workspace, terminal]
---

# Hermes Profile Management

Per-profile configuration for Hermes Agent — workspace defaults, config edits, and isolation semantics. Applies to multi-agent setups where each agent (Nexis, Mei, Zero, Chloe...) runs under its own profile.

## Profile Isolation Semantics

- A profile is a separate Hermes state home: `~/.hermes/profiles/<name>/` holds its own `config.yaml`, `.env`, memories, skills, cron jobs, sessions.
- Profiles isolate **Hermes state**, NOT OS access. The agent still reaches the full user filesystem.
- The profile working directory is a **separate setting** from the profile boundary. Setting `cwd` does not move profile state, and profile state location does not affect `cwd`.

## Setting a Profile's Default Workspace

The working directory for terminal/file operations is `terminal.cwd` in the profile's `config.yaml`.

```bash
hermes config set terminal.cwd "<absolute path>" --profile <name>
```

- New sessions start in that directory; the current session keeps its old cwd until restarted.
- Existing files keep living where they are — this only changes where new commands start.
- Verify after the change:
  ```bash
  grep -n "cwd:" ~/.hermes/profiles/<name>/config.yaml
  ```
- A memory note (soft convention, not enforced) can complement the hard setting: agents typically record their workspace in profile memory so the setting and the habit agree.

## Editing Config Files — Guardrails

**Both global and per-profile config.yaml are write-protected.** `patch` and `write_file` fail with:
"Refusing to write to Hermes config file" / "Write denied: protected system/credential file."

The official path that works:

```bash
hermes config set <key> <value>                # global
hermes config set <key> <value> --profile <name>  # any profile
```

Only fall back to `sed` when `hermes config` cannot express the change (e.g. structural edits). When using sed:

- **Windows/MSYS backslash mangling**: `sed` treats `\` as an escape. `s|old|D:\A\B|` writes `D:AB`. Use single-quoted replacement with escaped backslashes (`'D:\\A\\B'`), or prefer `hermes config set` which handles raw backslashes.
- **Duplicate key trap**: YAML allows duplicate keys — the last wins. A non-matching sed old_string can silently insert a second copy of a key. Always `grep -n` the key after editing to confirm exactly one occurrence with the right value.

## Restart Requirement

Changes to `config.yaml` take effect on NEW sessions. Tell the user a gateway/session restart is needed before the workspace change is live. On this setup, the gateway restart is gated on explicit user approval (see gateway restart protocol in profile memory).

## Pitfalls

- Do not attempt `patch`/`write_file` on config.yaml files — refused every time; go straight to `hermes config set`.
- `hermes config set` output confirms target file path — read it to verify you edited the intended profile, not the global config.
- `terminal.cwd` accepts absolute Windows paths with raw backslashes via `hermes config set`; quote the value so the shell doesn't split on spaces in paths like `D:\Celestia Mei Nexaris\Nexis Aria Nexaris`.