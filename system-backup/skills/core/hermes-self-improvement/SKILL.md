---
name: hermes-self-improvement
description: Continuously improve effectiveness through reflection, evaluation, and adaptation after every significant task.
---

# Hermes Self-Improvement

## Core Principle
*Every task contains information that can improve future performance.*

Successes should be reinforced. Failures should be analyzed. Mistakes should not be repeated.

---

## Trigger Conditions
Use this skill **after completing any significant task** or when:
- A task succeeds unexpectedly.
- A task fails or encounters issues.
- The user provides feedback.
- You identify a recurring pattern (positive or negative).
- You complete a multi-step workflow.

---

## Reflection Procedure

### 1. Review the Objective
- What was the user's goal?
- What were the success criteria?

### 2. Review the Plan
- What was the execution plan?
- Were all steps necessary?
- Were any steps missing?

### 3. Review Execution
- Did you follow the plan?
- Were there deviations?
- Did you use the right tools and skills?

### 4. Review Results
- What was the outcome?
- Did the result meet the success criteria?
- Were there unintended side effects?

### 5. Compare Outcome to Intended Outcome
- Did the task succeed or fail?
- If it failed, where did it go wrong?

### 6. Identify Strengths
- What went well?
- Which strategies were effective?
- Which tools or skills performed reliably?

### 7. Identify Weaknesses
- What went wrong?
- Were there planning failures?
- Were there execution errors?
- Were there tool or skill misselections?

### 8. Identify Opportunities for Improvement
- What could be done better next time?
- Could a skill or tool have improved the outcome?
- Could the plan have been more efficient?

### 9. Record Lessons Learned
- Save key insights to memory or as a skill.
- Example: `memory(action="add", target="memory", content="User prefers concise summaries for research tasks.")`
- Example: Save a new workflow as a skill with `skill_manage(action="create")`.

### 10. Apply Lessons to Future Tasks
- Use insights to improve planning, tool selection, and execution.
- Avoid repeating mistakes.

---

## Success Analysis

When a task succeeds:

- **Determine why it succeeded**: Was it due to planning, tool selection, or execution?
- **Identify effective strategies**: What worked well?
- **Reinforce successful behaviors**: Use the same approach for similar tasks.
- **Reuse successful workflows**: Save the workflow as a skill if it’s reusable.

---

## Failure Analysis

When a task fails:

- **Determine root cause**: What went wrong?
- **Identify missing information**: Was the environment or goal misunderstood?
- **Identify incorrect assumptions**: Were there false assumptions about tools, skills, or resources?
- **Identify planning failures**: Was the plan incomplete or flawed?
- **Identify tool misuse**: Was the wrong tool used?
- **Identify skill selection errors**: Was a relevant skill overlooked?
- **Identify execution errors**: Were there mistakes during execution?

---

## Learning Rules

### Do Not Treat Failures as Isolated Events
- Treat failures as learning opportunities.
- Identify patterns in failures to prevent recurrence.

### When a Similar Task Appears in the Future
- Recall previous lessons.
- Avoid previous mistakes.
- Apply improved approaches.

---

## Continuous Improvement Areas

- **Planning**: Improve task decomposition and success criteria.
- **Tool Usage**: Optimize tool selection and execution.
- **Skill Selection**: Identify and reuse relevant skills.
- **Communication**: Refine clarity, tone, and structure.
- **Automation**: Streamline workflows with scripts or cron jobs.
- **Coding**: Improve code quality and debugging.
- **Research**: Enhance information gathering and synthesis.
- **Decision Making**: Strengthen reasoning and trade-off analysis.
- **Task Execution**: Increase reliability and efficiency.

---

## Failure Modes To Avoid

### 1. Repeating Mistakes
- Never repeat the same mistake without analysis.

### 2. Ignoring Failures
- Always analyze failures to identify root causes.

### 3. Ignoring Successful Strategies
- Reinforce and reuse successful approaches.

### 4. Failing to Adapt
- Continuously update workflows based on lessons learned.

### 5. Assuming Current Performance is Optimal
- Always look for opportunities to improve.

---

## Self-Evaluation Questions

After major tasks, ask:

- **What went well?** (Strengths)
- **What went wrong?** (Weaknesses)
- **What should be improved?** (Opportunities)
- **What should be repeated?** (Reinforce)
- **What should be avoided?** (Mistakes)

---

## Examples

### Example 1: Task Succeeds Unexpectedly
1. **Task**: Generate a research summary.
2. **Outcome**: The summary is concise and well-received.
3. **Reflection**:
   - **Strengths**: Used `web_extract` for accurate content, structured the summary with clear headings.
   - **Opportunities**: Could save this workflow as a skill for future research tasks.
4. **Action**: Save the workflow as a skill:
   ```python
   skill_manage(action="create", name="research-summary-workflow", content="...")
   ```

### Example 2: Task Fails Due to Missing Information
1. **Task**: Schedule a cron job.
2. **Outcome**: The job fails because the `cronjob` tool was disabled.
3. **Reflection**:
   - **Weaknesses**: Did not verify tool availability before planning.
   - **Root Cause**: Assumed the tool was enabled.
   - **Opportunities**: Always check tool availability with `hermes tools list`.
4. **Action**: Save the lesson to memory:
   ```python
   memory(action="add", target="memory", content="Always verify tool availability with 'hermes tools list' before planning.")
   ```

### Example 3: Task Fails Due to Planning Error
1. **Task**: Open a GitHub PR.
2. **Outcome**: The PR fails because the branch was not pushed.
3. **Reflection**:
   - **Weaknesses**: Did not include branch push in the plan.
   - **Root Cause**: Incomplete planning.
   - **Opportunities**: Always verify branch status before opening a PR.
4. **Action**: Update the `github-pr-workflow` skill to include branch push:
   ```python
   skill_manage(action="patch", name="github-pr-workflow", old_string="- Step 1: Verify the branch exists.", new_string="- Step 1: Verify the branch exists and push it if necessary.")
   ```

---

## Notes
- This skill is **mandatory** for all significant tasks.
- Always reflect after completing or failing a task.
- Apply lessons learned to future tasks.
- Update this skill whenever new improvement strategies are discovered.