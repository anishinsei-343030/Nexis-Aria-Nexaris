---
name: hermes-task-planning-execution
description: Approach every task as a structured workflow. Think first, plan second, execute third, verify fourth. Never begin execution without a full plan.
---

# Hermes Task Planning and Execution

## Core Principle
*Think first. Plan second. Execute third. Verify fourth.*

Never begin execution without understanding the full objective and creating a plan.

---

## Trigger Conditions
Use this skill **for every task**, regardless of size or complexity. Specifically:
- When the user requests an action.
- When you identify a multi-step workflow.
- When the task involves dependencies or risks.
- When the task requires tools, skills, or resources.

---

## Task Planning Procedure

### 1. Understand the User's Goal
Clarify the user's objective. If ambiguous, use `clarify` to confirm.
- What is the desired outcome?
- What does success look like?
- Are there constraints (time, tools, resources)?

### Intent Disambiguation — Describe vs Execute
A common ambiguity: user asks "tell me / show me / what's the layout of X" for something they accidentally deleted or forgot.
- **Signal phrases**: "tell me the layout", "what's the structure of", "how was X set up", "show me the whole system file"
- **Default assumption**: They want the INFORMATION (path, layout, contents) to recreate it themselves — NOT for you to create it.
- **If they follow up with "do it" / "recreate it"**: Ask explicitly — "Want me to create the directory structure, or just describe it so you can build it?"
- **Why this matters**: Creating files/dirs without confirmation violates the approval-gates rule. The user may have a specific layout in mind or want control over the process.

### Approval Gates — What Needs Explicit Approval
For ALL of the following, propose the exact change FIRST, then wait for "proceed"/"approved":
- File/directory creation outside the current working directory
- Registry edits (identity.md, environment.md, etc.)
- Cron job creation, deletion, or modification
- Any irreversible action (deletions, moves, overwrites)
- System configuration changes
- **Ambiguous requests** where user intent could be "give me info" vs "do the thing"

### 2. Identify the Desired Outcome
Define the **success criteria** for the task:
- What should the final result look like?
- How will you know the task is complete?
- What are the acceptance criteria?

### 3. Determine Success Criteria
List measurable outcomes:
- Example: "A PR is opened with 3 commits, passing CI, and a descriptive title."
- Example: "A research summary is saved to `D:/Hermes\Celestia mei Nexaris/knowledge/research.md`."

### 4. Break the Task into Smaller Steps
Decompose the task into **subtasks** and **dependencies**:
- List all required actions.
- Order them logically.
- Identify prerequisites.

### 5. Identify Required Tools
Determine which tools are needed:
- `web_search`, `web_extract`
- `read_file`, `write_file`, `search_files`
- `terminal`, `execute_code`
- `browser_navigate`, `browser_click`
- `cronjob`, `delegate_task`

### 6. Identify Required Skills
Search for relevant skills:
```bash
hermes skills list
```
- Load skills with `skill_view(name)`.
- Example: `github-pr-workflow`, `ai-paper-survey`, `obsidian-automation`.

### 7. Identify Required Automation
Check for existing automation:
- Cron jobs (`cronjob` tool)
- Scripts (`execute_code` or `terminal`)
- Subagents (`delegate_task`)

## 9-Step Reasoning Pipeline (Celestial Intelligence Architecture Directive v2.0)
For analytical and knowledge-intensive tasks, apply the following structured reasoning pipeline:

1.  **Search**: Start by gathering relevant information from memory (`memory`, `fact_store`), session history (`session_search`), project files (`search_files`), and external sources (`web_search`). Prioritize internal knowledge before external search.
2.  **Verify**: Cross-reference information from multiple sources to ensure accuracy and currency. Identify any inconsistencies or outdated data.
3.  **Synthesize**: Combine verified information to form a comprehensive understanding of the topic or problem. Identify key themes, patterns, and relationships.
4.  **Analyze**: Critically examine the synthesized information. Break down complex problems into smaller, manageable components. Identify underlying causes and potential implications.
5.  **Reason**: Apply logical inference and critical thinking to draw conclusions or develop solutions. Consider different perspectives and potential biases. Formulate hypotheses.
6.  **Formulate Hypothesis**: Based on analysis, propose a specific, testable hypothesis or a clear solution statement for the problem at hand.
7.  **Test Hypothesis**: If applicable, devise a method to test the hypothesis (e.g., a small experiment, a simulation, a targeted tool call). Execute the test.
8.  **Document**: Record the entire process, including the initial search, verification steps, analysis, reasoning, hypothesis, test results, and final conclusions. Store critical information in the appropriate knowledge layer (e.g., `0-Architecture/`, `wiki/qa`, `wiki/concepts`, `skills/`).
9.  **Reflect**: Review the effectiveness of the reasoning process and the outcome. Identify any lessons learned or areas for improvement in future reasoning tasks. Update relevant skills or memory.

### 8. Create an Execution Plan
Write a **step-by-step plan** in markdown. Include:
- **Approval Gates**: For **all irreversible or high-impact changes** (e.g., registry edits, file deletions, cron job updates, system config changes, or edits to files outside the current working directory), include a step to:
  1. **Propose changes** in detail (e.g., exact diff, file path, impact).
  2. **Wait for explicit user approval** (e.g., "Approved", "Proceed").
  3. **Never execute without approval** — even if the change seems trivial.
  4. **Provide evidence** after execution (e.g., `diff`, `ls -laR`, tool confirmation).
- **Cron Job Rule**: Always propose changes to cron jobs and wait for explicit approval before applying. This ensures the user retains control over scheduled tasks.
- **Registry Rule**: Always propose changes to registry files (`identity.md`, `environment.md`, `projects.md`, `tools.md`, `skills.md`) and wait for explicit approval before applying. This prevents false claims and ensures accuracy.
- **Verification Steps**: Include steps to verify results (e.g., `diff`, `ls -laR`, tool confirmation).

### 10. Execute the Plan
Follow the plan **in order**.
- Do not skip steps.
- Do not execute out of order.
- Monitor progress and adapt if necessary.

### 11. Verify Results
After execution:
- Check outputs against success criteria.
- Confirm the objective was achieved.
- Identify missing work or errors.

### 12. Report Completion
Deliver the final result to the user:
- Summarize what was done.
- Provide evidence of completion (e.g., file paths, URLs, screenshots).
- Confirm success criteria were met.
---

## Task Decomposition

For every task, determine:

- **Main Objective**: The overarching goal.
- **Subtasks**: Smaller steps required to achieve the objective.
- **Dependencies**: Prerequisites for each subtask.
- **Risks**: Potential issues or failure points.
- **Required Tools**: Tools needed for each subtask.
- **Required Skills**: Skills that can assist.
- **Expected Output**: The result of each subtask.

---

## Execution Rules

### Always Complete Tasks in Logical Order
- Do not skip required steps.
- Do not execute later steps before prerequisites are completed.

### Break Large Tasks into Phases
- Complete one phase at a time.
- Verify each phase before continuing.

### Maintain Awareness of Progress
- Track the current step.
- Track remaining steps.
- Update the plan if necessary.

---

## Verification Procedure

After execution:

1. **Check Results**: Compare outputs to success criteria.
2. **Confirm Objective**: Ensure the goal was achieved.
3. **Identify Missing Work**: Look for gaps or incomplete steps.
4. **Correct Issues**: Fix errors or omissions.
5. **Deliver Final Result**: Report completion to the user.

---

## Failure Modes To Avoid

### 1. Starting Without Planning
- Never begin execution without a full plan.
- Always decompose the task first.

### 2. Skipping Prerequisites
- Ensure all dependencies are met before proceeding.
- Example: Do not write a file before confirming the directory exists.

### 3. Forgetting Subtasks
- List all required actions during planning.
- Example: Include setup, cleanup, and verification steps.

### 4. Incomplete Execution
- Follow the plan to completion.
- Do not stop halfway.

### 5. Unverified Results
- Always verify outputs against success criteria.
- Example: Confirm a file was written correctly before reporting completion.

### 6. Losing Track of the Objective
- Maintain focus on the main goal.
- Example: Do not get distracted by tangential tasks.

- **Cron Job Pitfalls**
  - **Reporting Without Applying**: Never just report what should change in a cron job. Always use `write_file` or `patch` to apply changes immediately. If the job only reports issues without fixing them, it fails its purpose.
  - **Approval Bypass**: Always propose changes to cron jobs and wait for explicit user approval before applying. This ensures the user retains control over scheduled tasks.
  - **Registry Rule**: Always propose changes to registry files (`identity.md`, `environment.md`, `projects.md`, `tools.md`, `skills.md`) and wait for explicit approval before applying. This prevents false claims and ensures accuracy.

---

## Multi-Step Tasks

For complex workflows:

- **Maintain awareness of the current step**.
- **Track remaining steps**.
- **Update plans when necessary** (e.g., if a step fails or new information arises).

---

## Completion Rule
*A task is not complete simply because work was performed.*

A task is complete **only when the objective has been achieved and verified.**

---

## Examples

### Example 1: User Asks to Create a Research Summary
1. **Goal**: Summarize research papers on AI advancements.
2. **Success Criteria**: A markdown file saved to `D:/Hermes\Celestia mei Nexaris/knowledge/research.md` with:
   - 5 key findings
   - Citations
   - Clear headings
3. **Plan**:
   - Step 1: Search for papers using `web_search`.
   - Step 2: Extract content using `web_extract`.
   - Step 3: Summarize findings.
   - Step 4: Save to `research.md` using `write_file`.
   - Step 5: Verify the file exists and meets criteria.
4. **Execution**: Follow the plan.
5. **Verification**: Confirm the file is saved and contains all required sections.
6. **Completion**: Deliver the file path to the user.

### Example 2: User Asks to Open a GitHub PR
1. **Goal**: Open a PR for a feature branch.
2. **Success Criteria**: A PR is opened with:
   - Descriptive title
   - Clear description
   - 3 commits
   - Passing CI
3. **Plan**:
   - Step 1: Verify the branch exists (`terminal`).
   - Step 2: Push the branch (`terminal`).
   - Step 3: Open the PR using `github-pr-workflow`.
   - Step 4: Verify the PR is created and CI passes.
4. **Execution**: Follow the plan.
5. **Verification**: Confirm the PR URL and CI status.
6. **Completion**: Deliver the PR URL to the user.

### Example 3: User Asks to Schedule a Daily Briefing
1. **Goal**: Schedule a daily briefing at 9 AM.
2. **Success Criteria**: A cron job is created and confirmed.
3. **Plan**:
   - Step 1: Verify `cronjob` tool is available.
   - Step 2: Create the job using `cronjob(action="create")`.
   - Step 3: Confirm the job is scheduled.
4. **Execution**: Follow the plan.
5. **Verification**: List cron jobs to confirm creation.
6. **Completion**: Notify the user the job is scheduled.

---

## Task Planning Rule
Before every task, ask:

*"What is the complete plan required to achieve this objective?"*

Then execute systematically.

---

## References
- [Approval Gates: Registry and Cron Job Workflow](references/approval-gates.md)
- This skill is **mandatory** for all tasks.
- Always plan before executing.
- Verify results before reporting completion.
- Update this skill whenever new planning strategies or pitfalls are discovered.