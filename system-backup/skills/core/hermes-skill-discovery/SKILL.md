---
name: hermes-skill-discovery
description: Actively discover and reuse installed skills before creating new solutions. Enforce systematic skill evaluation before attempting to solve tasks.
---

# Hermes Skill Discovery

## Core Principle
*Installed skills represent proven workflows, knowledge, automations, and procedures.*

Whenever a relevant skill exists, **prefer using the skill** over creating a new workflow from scratch.

---

## Trigger Conditions
Use this skill **before every task** or when:
- The user requests an action that could be automated by a skill.
- You consider solving a task through manual reasoning or tool usage alone.
- You need to verify whether a skill exists for a task.
- You are unsure which skill to use.

---

## Skill Selection Procedure

### Step 1: Understand the User's Goal
Clarify the user's objective. If ambiguous, use `clarify` to confirm.

### Step 2: Search Installed Skills
List installed skills:
```bash
hermes skills list
```
- Search for skills related to the task using keywords (e.g., "research", "code", "automation", "file").
- Use `skill_view(name)` to review the full content of potentially relevant skills.

### Step 3: Identify Relevant Skills
Evaluate whether one or more installed skills can accomplish the task:
- **Coding**: `github-pr-workflow`, `test-driven-development`, `systematic-debugging`
- **Research**: `ai-paper-survey`, `deep-research-v60`, `web-investigation`
- **Automation**: `cronjob`, `delegate_task`, `subagent-driven-development`
- **File Management**: `obsidian-automation`, `local-file-delivery`, `search_files`
- **Browser Actions**: `agent-browser`, `web-extract`, `youtube-content`
- **Planning**: `agent-daily-planner`, `one-three-one-rule`, `writing-plans`
- **Productivity**: `google-workspace`, `notion`, `linear`
- **Content Creation**: `ai-video-editor-fixed`, `create-video`, `songwriting-and-ai-music`
- **Communication**: `ai-daily-briefing`, `telegram-bot-integration`, `user-communication-preferences`
- **Analysis**: `data-science`, `mlops`, `weights-and-biases`

### Step 4: Select the Best Skill
If multiple skills apply:
- **Prefer the most specialized skill** (e.g., `github-pr-workflow` over `terminal` for GitHub tasks).
- **Prefer proven workflows** (skills with clear steps, pitfalls, and examples).
- **Prefer reusable solutions** (skills designed for repeatability).

### Step 5: Execute the Skill
Load and follow the skill’s workflow:
```python
skill_view(name="skill-name")
```
- Follow the skill’s **trigger conditions**, **workflow**, and **pitfalls**.
- Use the skill’s **linked files** (templates, scripts, references) if available.

### Step 6: Create New Workflows Only When Necessary
If no suitable skill exists:
- Proceed with tools, automation, or manual reasoning.
- After completing the task, **offer to save it as a skill** for future reuse.

---

## Examples

### Example 1: User Asks to Review a GitHub PR
1. **Goal**: Review a GitHub pull request.
2. **Skill Search**: `github-pr-workflow` is installed.
3. **Skill Evaluation**: The skill provides a step-by-step workflow for PR reviews.
4. **Execution**: Load and follow `github-pr-workflow`.
5. **Result**: The PR is reviewed using the skill’s proven approach.

### Example 2: User Asks to Schedule a Daily Briefing
1. **Goal**: Schedule a daily briefing at 9 AM.
2. **Skill Search**: `ai-daily-briefing` is installed.
3. **Skill Evaluation**: The skill provides a workflow for generating and scheduling briefings.
4. **Execution**: Load and follow `ai-daily-briefing`.
5. **Result**: The briefing is scheduled using the skill’s template.

### Example 3: User Asks to Generate a Research Summary
1. **Goal**: Summarize research papers on a topic.
2. **Skill Search**: `ai-paper-survey` is installed.
3. **Skill Evaluation**: The skill provides a structured approach to paper surveys.
4. **Execution**: Load and follow `ai-paper-survey`.
5. **Result**: The research summary is generated using the skill’s methodology.

---

## Failure Modes To Avoid

### 1. Forgetting Installed Skills
- Always list skills before starting a task.
- Use `hermes skills list` and search for relevant keywords.

### 2. Rebuilding Existing Workflows
- Never recreate a workflow that already exists as a skill.
- Example: Use `github-pr-workflow` instead of manually scripting GitHub interactions.

### 3. Ignoring Specialized Skills
- Prefer specialized skills over generic tools.
- Example: Use `obsidian-automation` instead of `terminal` for Obsidian vault tasks.

### 4. Creating Duplicate Solutions
- Always check for existing skills before creating a new workflow.
- Example: Use `ai-video-editor-fixed` instead of manually scripting video edits.

### 5. Reinventing Capabilities
- Never assume a skill doesn’t exist without verification.
- Example: Use `songwriting-and-ai-music` for music-related tasks instead of starting from scratch.

---

## Skill Reuse Rule
Before every task, ask:

*"Do I already possess a skill that can accomplish this goal?"*

- **If yes**: Use the skill.
- **If no**: Proceed with planning a new solution, then **offer to save it as a skill** for future reuse.

---

## Continuous Awareness
- **Regularly review installed skills** to stay updated on available workflows.
- **Incorporate skills into task planning** to maximize efficiency.
- **Update this skill** whenever new skills are discovered or created.

---

## Notes
- This skill is **mandatory** for all tasks involving skill evaluation or execution.
- Always verify skills before acting.
- Update this skill whenever new skills are added or workflows are improved.