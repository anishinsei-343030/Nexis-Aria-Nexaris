---
name: hermes-project-awareness
description: Maintain awareness of project continuity, goals, history, decisions, milestones, and dependencies. Consult the Project Registry (`registries/projects.md`) as the authoritative source of truth before making assumptions.
---

# Hermes Project Awareness

## Core Principle
*Every project is a persistent system, not an isolated task.*

Projects have:
- Goals
- History
- Decisions
- Milestones
- Dependencies
- Context

You must maintain awareness of project continuity.

---

## Project Assessment Procedure

### 1. Consult the Project Registry
- Load `registries/projects.md` to retrieve authoritative project details (goals, milestones, architecture decisions, constraints).
- Use this as the baseline for all subsequent checks.

### 2. Identify the Project
- Determine which project the task belongs to.
- If unclear, use `clarify` to confirm with the user.

### 3. Determine Current Project State
- Review the project's current status (active, maintenance, research, personal).
- Cross-reference with the **Task Queue** (`todo` tool) for active tasks.

### 4. Review Relevant History
- Recall prior work, decisions, and milestones.
- Use `session_search` to retrieve past discussions or decisions.

### 5. Review Prior Decisions
- Identify architecture, design, or workflow decisions that may impact the task.
- Avoid revisiting settled decisions unless new information exists.

### 6. Review Active Tasks
- Check the task queue (`todo` tool) for overlapping or dependent tasks.
- Coordinate with other agents if necessary.

### 7. Review Milestones
- Identify upcoming or pending milestones.
- Align the task with project goals.

### 8. Determine Next Actions
- Plan the task while preserving project continuity.
- Execute with awareness of project context.

---

## Project Categories

### Active Projects
Projects currently under development.

### Maintenance Projects
Projects requiring ongoing support.

### Research Projects
Projects focused on learning and investigation.

### Personal Projects
Projects tied to user interests and goals.

---

## Project Knowledge

Maintain awareness of:
- Architecture decisions
- Design decisions
- Goals
- Constraints
- Roadmaps
- Completed milestones
- Pending milestones

---

## Decision Preservation

Important project decisions should be preserved in the **Project Registry** (`registries/projects.md`).

Avoid repeatedly revisiting settled decisions unless new information exists.

---

## Project Continuity Rules

When working on a project:
- Recall prior work.
- Recall prior decisions.
- Recall prior goals.
- Maintain consistency.

---

## Failure Modes To Avoid

- Treating projects as isolated tasks.
- Forgetting architecture decisions.
- Forgetting goals.
- Losing continuity.
- Repeating completed work.

---

## Project Rule

Before every project-related task, ask:

*"What is the current state of this project?"*

Then proceed using the project's history, goals, and context.