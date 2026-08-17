---
name: hermes-tool-awareness
description: Maintain awareness of all available tools and prioritize their use over manual reasoning. Enforce systematic tool evaluation before attempting to solve tasks.
---

# Hermes Tool Awareness Registry

## Core Principle
*A tool exists to extend your capabilities.*

If a tool can perform a task more accurately, efficiently, or reliably than reasoning alone, **use the tool**.

---

## Trigger Conditions
Use this skill **before every task** or when:
- The user requests an action that could be automated.
- You consider solving a task through reasoning alone.
- You need to verify whether a tool exists for a task.
- You are unsure which tool or skill to use.

---

## Tool Usage Priority
Always follow this order:

1. **Existing skill** (proven workflow)
2. **Existing tool** (direct execution)
3. **Existing automation** (scripts, cron jobs)
4. **Existing workflow** (multi-step processes)
5. **New solution** (only if no existing option exists)

**Never recreate functionality that already exists.**

---

## Workflow

### 1. Goal Identification
Clarify the user's objective. If ambiguous, use `clarify` to confirm.

### 2. Tool Evaluation
Determine whether a tool, skill, or automation can help:
- **Web Research**: `web_search`, `web_extract`
- **File Operations**: `read_file`, `write_file`, `search_files`, `patch`
- **Code Execution**: `execute_code`, `terminal`
- **Browser Automation**: `browser_navigate`, `browser_click`, `browser_type`
- **Memory Recall**: `memory`, `session_search`, `fact_store`
- **Automation**: `cronjob`, `delegate_task`
- **Image Generation**: `image_generate`
- **Audio Generation**: `text_to_speech`
- **Vision Analysis**: `vision_analyze`

### 3. Tool Verification
List available tools:
```bash
hermes tools list
```
- Confirm required tools are enabled.
- Note any disabled or missing tools.
- **⚠️ CRITICAL: Cross-reference before declaring a tool non-existent.**
  - `hermes tools list` shows callable tools available to the agent in the current session. Some tools (e.g., `fact_store` for Holographic Memory) operate at the system/infrastructure layer and may NOT appear here.
  - Always cross-reference against the system prompt, loaded skills, and registry files before deprecating a tool.

### 4. Skill Verification
List installed skills:
```bash
hermes skills list
```
- Search for skills relevant to the task.
- Load relevant skills with `skill_view(name)` to confirm their capabilities.

### 5. Approach Selection
Select the best available approach:
- **Skills**: Load and follow the skill’s workflow.
- **Tools**: Execute the tool directly.
- **Automation**: Use scripts, cron jobs, or subagents.
- **Reasoning**: Only if no tool or skill exists.

### 6. Execution
Execute the task using the selected approach. Monitor progress and verify outcomes.

### 7. Analysis
Review the results:
- If successful, confirm completion with the user.
- If unsuccessful, retry with an alternative approach or explain limitations.

---

## Examples

### Example 1: User Asks for Web Research
1. **Goal**: Find recent articles about AI advancements.
2. **Tool Evaluation**: `web_search` and `web_extract` are available.
3. **Approach**: Use `web_search` to find articles, then `web_extract` to summarize them.
4. **Execution**:
   ```python
   results = web_search("recent AI advancements", limit=3)
   articles = web_extract([result["url"] for result in results["data"]["web"]])
   ```
5. **Analysis**: Compile results into a summary for the user.

### Example 2: User Asks to Read a File
1. **Goal**: Read the contents of `D:/notes/project_ideas.md`.
2. **Tool Evaluation**: `read_file` is available.
3. **Approach**: Use `read_file` to read the file.
4. **Execution**:
   ```python
   file_content = read_file("D:/notes/project_ideas.md")
   ```
5. **Analysis**: Return the content to the user.

### Example 3: User Asks to Generate an Image
1. **Goal**: Generate an image of a futuristic city.
2. **Tool Evaluation**: `image_generate` is available.
3. **Approach**: Use `image_generate` with a descriptive prompt.
4. **Execution**:
   ```python
   image = image_generate("futuristic city at sunset, cyberpunk style, neon lights")
   ```
5. **Analysis**: Return the image path to the user with `MEDIA:<path>`.

### Example 4: User Asks to Schedule a Task
1. **Goal**: Schedule a daily briefing at 9 AM.
2. **Tool Evaluation**: `cronjob` is available.
3. **Approach**: Use `cronjob` to schedule the task.
4. **Execution**:
   ```python
   cronjob(action="create", prompt="Generate a daily briefing with news and weather", schedule="0 9 * * *")
   ```
5. **Analysis**: Confirm the job was scheduled.

---

## Failure Modes To Avoid

### 1. Forgetting Available Tools
- Always list tools and skills before starting a task.
- Use `hermes tools list` and `hermes skills list`.

### 2. Ignoring Tools
- Do not default to manual reasoning if a tool exists.
- Example: Use `read_file` instead of `terminal("cat file.txt")`.

### 3. Replacing Tool Usage with Guesses
- Never assume information is up-to-date. Use `web_search` or `memory`.

### 4. Reimplementing Existing Skills
- Always check for relevant skills before creating a new workflow.
- Example: Use `github-pr-workflow` instead of manually scripting GitHub interactions.

### 5. Solving Manually When Automation Exists
- Use tools like `execute_code`, `terminal`, or `delegate_task` for repetitive tasks.

---

## Tool Selection Rule
Before every task, ask:

*"What tool, skill, automation, or workflow can best accomplish this goal?"*

Only proceed after evaluating all available options.

---

## Notes
- This skill is **mandatory** for all tasks involving tool evaluation or execution.
- Always verify tools and skills before acting.
- Update this skill whenever new tools or workflows are discovered or created.