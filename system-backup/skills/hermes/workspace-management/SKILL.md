---
name: workspace-management
description: Manage per-profile AI agent workspaces, including structural scaffolding, state persistence via READMEs, and automated documentation syncing.
version: 1.0.0
author: Nexis Aria Nexaris
platforms: [windows]
metadata:
  hermes:
    tags: [workspace, file-system, organization, state-persistence, automation]
---

# Workspace Management

This skill governs the creation, maintenance, and synchronization of an AI agent's dedicated filesystem workspace. It focuses on transforming a folder from a simple directory into a "Deep Storage" layer that complements the agent's internal profile memory.

## 1. Standard Workspace Architecture
When scaffolding a new workspace, use the following structural standard:

- `/projects` - Individual project folders. Each MUST contain a `README.md` acting as a "save point" for goals, status, and next steps.
- `/scripts` - Reusable automation, utility scripts, and maintenance tools.
- `/docs` - Structured intelligence. Subdivided into `/specs` (Requirements/What) and `/process` (Plans/How).
- `/knowledge` - Long-form research, external references, and deep notes.
- `/assets` - Media, images, and raw resources.
- `/output` - Final deliverables and exported results (Nexaris Family Standard).
- `/templates` - Reusable scaffolds for code and documentation.
- `/inbox` - Landing zone for raw/unfiled data to prevent root clutter.
- `/archive` - Versioned backup of completed or legacy work.

## 2. State Persistence via READMEs
To avoid "context drift" or reliance on limited profile memory:
- Every new project folder must be initialized with a `README.md`.
- The agent must update this file at the end of significant milestones or sessions.
- Future sessions should read the project's `README.md` first to restore the operational state.

## 3. Automated Documentation (The Sync Loop)
To ensure the workspace map remains accurate as files/folders are added:
- Use a synchronization script (e.g., `scripts/update_workspace_readme.py`).
- The script should scan the tree (depth 2), filter junk dirs (e.g., `__pycache__`), and rewrite the `## Current Structure` section of the root `README.md`.
- **Trigger:** Run this script whenever a directory is created, renamed, or deleted.

## 4. Pitfalls & Constraints
- **Memory Overlap:** Do not create `/memory` or `SOUL.md` folders in the workspace if the agent uses a profile-based memory system (like Hermes). This causes redundancy and drift.
- **Path Validation:** Always verify the existence of the workspace root using `ls` before attempting scaffolding.
- **Config Sync:** Ensure `terminal.cwd` in the profile's `config.yaml` matches the workspace path for seamless tool execution.
- **Cron script-path constraint:** The `cronjob` tool rejects absolute script paths — scripts must be under `~/.hermes/scripts/` (or the profile's scripts dir) and referenced by bare filename. If the real script lives in the workspace, drop a thin wrapper in the profile scripts dir that shells out to it. Verified: cron wrapper `workspace_readme_watchdog.py` → workspace `scripts/update_workspace_readme.py`.
- **Workspace path changes:** When the user renames/moves the workspace root (e.g. `D:\Celestia...` → `D:\Hermes\Nexis Aria Nexaris`), update BOTH the profile `terminal.cwd` AND the memory note AND any scripts hard-coding the old path — the README-watchdog cron is no use if its target path is stale.

## 5. Support Files
- `scripts/update_workspace_readme.py` - Standard script for regenerating the workspace tree in the root README.
- `scripts/workspace_readme_watchdog.py` - Cron wrapper that calls the real script; lives in `~/.hermes/profiles/<name>/scripts/` (cron only accepts relative script paths there).
