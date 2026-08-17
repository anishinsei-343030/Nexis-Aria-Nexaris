---
name: core
description: Core Hermes skills for self-awareness, memory, and task execution. Includes subskills for environment awareness, project continuity, and tool management.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [core, self-improvement, memory, task-planning]
    related_skills: [hermes-environment-awareness, hermes-memory-management, hermes-task-planning-execution]
---

# Core Skills

## Purpose
Core skills provide foundational capabilities for Hermes agents:
- **Self-awareness**: Track capabilities, tools, and environment.
- **Memory**: Persist user preferences and project context.
- **Task planning**: Break down goals into executable steps.

## Subskills
| Name | Purpose |
|------|---------|
| hermes-environment-awareness | Detect OS, tools, and runtime constraints. |
| hermes-memory-management | Store/retrieve user preferences and project facts. |
| hermes-task-planning-execution | Plan and execute tasks with validation. |

## Usage
Load this skill when:
- Initializing a new session.
- Managing long-term memory or project state.
- Planning multi-step tasks.

## Pitfalls
- Do not load `core` recursively (e.g., from within a subskill).
- Avoid modifying `core` unless fixing syntax/logic errors.