---
name: hermes-agent-orchestration
description: Coordinate work within a multi-agent ecosystem. Delegate tasks to the most specialized agent available to maximize quality and reliability.
---

# Hermes Agent Orchestration

## Core Principle
*Do not solve every task yourself. Use the most specialized agent available.*

Your responsibility is to **coordinate expertise**, not to perform every task alone.

---

## Trigger Conditions
Use this skill **before every major task** or when:
- The task requires specialized expertise (e.g., code review, security audit, testing).
- The task is part of a larger workflow (e.g., planning → implementation → review).
- You identify that another agent could perform the task more effectively.
- The user explicitly requests delegation or coordination.

---

## Agent Selection Procedure

### 1. Understand the User's Goal
Clarify the user's objective. If ambiguous, use `clarify` to confirm.
- What is the desired outcome?
- What expertise is required?

### 2. Decompose the Task
Break the task into smaller steps or phases:
- Planning
- Implementation
- Review
- Testing
- Security
- Integration

### 3. Identify Required Expertise
Determine the type of expertise needed for each step:
- **Planning**: Strategy, architecture, roadmaps, requirements.
- **Implementation**: Coding, development, feature creation.
- **Review**: Code quality, refactoring, best practices.
- **Security**: Vulnerability detection, risk assessment.
- **Testing**: Validation, QA, regression detection.

### 4. Consult the Agent Registry
- Load **`registries/agents.md`** to identify the **best-suited agent** for the task.
- Match the task to the agent’s **role and responsibilities**.
- **Never guess agent roles** — always verify in the registry.
- **Consult only when relevant** — do not preload the registry for every task.

### 5. Prepare Delegation Context
List available agents and their roles (from `agents.md`):
- **Plan Agent**: Strategy, architecture, task decomposition.
- **Build Agent**: Implementation, coding, development.
- **Code-Reviewer Agent**: Code review, refactoring, maintainability.
- **Security-Auditor Agent**: Security review, vulnerability detection.
- **Test-Engineer Agent**: Testing, validation, QA.

---

## Agent Selection Rules

1. **Registry-First Selection**
   - Consult **`agents.md`** before delegating tasks to ensure the correct agent is chosen.
   - **Never guess agent roles** — always verify in the registry.

2. **Minimum Viable Agents**
   - Use **only the agents required** for the task.
   - Avoid duplication of responsibilities.

3. **Plan Agent First**
   - **Always run the Plan Agent before delegating to other agents.**
   - The Plan Agent determines which other agents are needed.

4. **Security Auditor Mandatory**
   - **Always use the Security Auditor for:**
     - External APIs.
     - System/file access.
     - Untrusted inputs.
     - Deployments or production changes.

5. **Test Engineer Required**
   - **Always use the Test Engineer after:**
     - Implementation.
     - Bug fixes.
     - Refactoring.

6. **Execution Order**
   ```
   Plan → Build → Review → Test → Security (if needed)
   ```

### 5. Delegate Work When Appropriate
Use `delegate_task` to assign work to the most suitable agent:
```python
delegate_task(
    goal="Review this Python code for best practices and maintainability.",
    context="File path: D:/project/main.py. Focus on readability, performance, and error handling.",
    toolsets=["terminal", "file"],
    role="code-reviewer"  # Explicitly target the Code-Reviewer agent
)
```

### 6. Collect Results
Retrieve the results from the delegated agent:
- Review the output for completeness and quality.
- Ensure the results meet the success criteria.

### 7. Verify Quality
Validate the delegated work:
- Confirm the agent followed best practices.
- Check for errors, omissions, or misalignments with the goal.

## Verification
Before confirming completion of irreversible actions (e.g., gateway restarts, config edits, file deletions), **gather and present detailed evidence** to the user:
- **Process status**: `hermes gateway status`, `ps`, `netstat`
- **Config diffs**: `diff`, `grep`
- **Logs**: `tail -30 ~/.hermes/gateway*.log`
- **File integrity**: `ls -la`, `cat`

Present the evidence in a clear, labeled format (e.g., "Process running: PID 1234 ✓", "Config updated: token present ✓").

## Delivery
Integrate the results and deliver them to the user:
- Summarize the work performed.
- **Attach evidence** of completion (e.g., file paths, URLs, screenshots, terminal output).
- Confirm the objective was achieved **only after user review of evidence**.

---

## Available Agent Roles

### Plan
**Best for**:
- Planning
- Architecture
- Roadmaps
- Requirements gathering
- Task decomposition

**When to use**:
- Before starting a project or feature.
- When the user needs a structured approach.

### Build
**Best for**:
- Implementation
- Coding
- Development
- Feature creation

**When to use**:
- When the user requests code or features.
- When implementing a plan created by the **Plan** agent.

### Code-Reviewer
**Best for**:
- Code review
- Refactoring
- Maintainability
- Best practices

**When to use**:
- After code is written by the **Build** agent.
- When the user requests a code review.

### Security-Auditor
**Best for**:
- Security review
- Vulnerability detection
- Risk assessment
- Permission analysis

**When to use**:
- After code is reviewed by the **Code-Reviewer** agent.
- When the user requests a security audit.

### Test-Engineer
**Best for**:
- Testing
- Validation
- QA
- Regression detection

**When to use**:
- After code passes security review.
- When the user requests testing or validation.

---

## Delegation Rules

### Do Not Delegate Unnecessarily
- Use general reasoning for simple or low-stakes tasks.
- Example: Use `web_search` directly for quick information retrieval.

### Do Not Use Specialists When General Reasoning is Sufficient
- Reserve specialized agents for tasks requiring expertise.
- Example: Do not delegate a simple file read to the **Build** agent.

### Use Specialists When Expertise Improves Quality, Reliability, or Safety
- Delegate tasks that benefit from specialized knowledge.
- Example: Delegate code review to the **Code-Reviewer** agent.

---

## Multi-Agent Workflows

For complex projects, follow this sequence:

1. **Plan**: Creates the strategy and roadmap.
2. **Build**: Implements the plan.
3. **Code-Reviewer**: Reviews the code for quality.
4. **Security-Auditor**: Audits the code for vulnerabilities.
5. **Test-Engineer**: Validates the implementation.
6. **Hermes**: Integrates results and delivers the final outcome.

---

### Delegate Task Orchestration Pitfalls
- **Missing Orchestration Rules**: `delegate_task` has specific limitations (e.g., max 3 concurrent children, no nested delegation for this user). Undocumented rules can lead to silent failures or misuse.
- **Resolution**: Document `delegate_task` limitations clearly within this skill, or create a `references/delegate-task-orchestration.md` file.
- **Prevention**: Always verify `delegate_task` parameters against known limitations.

## Failure Modes To Avoid

### 1. Solving Specialist Work Alone
- Do not perform tasks that specialized agents can do better.
- Example: Do not review code if the **Code-Reviewer** agent is available.

### 2. Ignoring Available Expertise
- Always check for specialized agents before proceeding.
- Example: Use the **Security-Auditor** agent for security reviews.

### 3. Skipping Review Phases
- Always include review steps in multi-agent workflows.
- Example: Do not skip code review or security audit.

### 4. Skipping Testing
- Always validate work before delivery.
- Example: Use the **Test-Engineer** agent for QA.

### 5. Skipping Security Analysis
- Always assess security risks for code and automation.
- Example: Use the **Security-Auditor** agent for vulnerability detection.

---

## Agent Orchestration Rule
Before every major task, ask:

*"Which available agent is best suited for this work?"*

Then coordinate accordingly.

---

## Examples

### Example 1: User Requests a Code Review
1. **Goal**: Review a Python script for best practices.
2. **Expertise Needed**: Code review, refactoring, maintainability.
3. **Agent Selection**: **Code-Reviewer** agent.
4. **Delegation**:
   ```python
   delegate_task(
       goal="Review this Python script for best practices.",
       context="File path: D:/project/main.py. Focus on readability, performance, and error handling.",
       toolsets=["terminal", "file"],
       role="code-reviewer"
   )
   ```
5. **Result**: The **Code-Reviewer** agent provides feedback on code quality.
6. **Delivery**: Summarize the feedback and deliver it to the user.

### Example 2: User Requests a Feature Implementation
1. **Goal**: Implement a new feature in a Python project.
2. **Expertise Needed**: Planning, coding, review, testing.
3. **Workflow**:
   - **Plan**: Creates a roadmap for the feature.
   - **Build**: Implements the feature.
   - **Code-Reviewer**: Reviews the code.
   - **Test-Engineer**: Validates the implementation.
4. **Delegation**:
   ```python
   # Step 1: Plan
   plan_result = delegate_task(
       goal="Create a roadmap for implementing a new feature.",
       context="Feature: User authentication. Project: D:/project/",
       toolsets=["file"],
       role="plan"
   )

   # Step 2: Build
   build_result = delegate_task(
       goal="Implement the user authentication feature.",
       context=f"Roadmap: {plan_result}. Project: D:/project/",
       toolsets=["terminal", "file"],
       role="build"
   )

   # Step 3: Code Review
   review_result = delegate_task(
       goal="Review the user authentication feature implementation.",
       context=f"Code: {build_result}. Project: D:/project/",
       toolsets=["terminal", "file"],
       role="code-reviewer"
   )

   # Step 4: Testing
   test_result = delegate_task(
       goal="Test the user authentication feature.",
       context=f"Code: {build_result}. Project: D:/project/",
       toolsets=["terminal", "file"],
       role="test-engineer"
   )
   ```
5. **Integration**: Combine results and deliver the final implementation to the user.

### Example 3: User Requests a Security Audit
1. **Goal**: Audit a Python script for security vulnerabilities.
2. **Expertise Needed**: Security review, vulnerability detection.
3. **Agent Selection**: **Security-Auditor** agent.
4. **Delegation**:
   ```python
   delegate_task(
       goal="Audit this Python script for security vulnerabilities.",
       context="File path: D:/project/main.py. Focus on input validation, authentication, and data handling.",
       toolsets=["terminal", "file"],
       role="security-auditor"
   )
   ```
5. **Result**: The **Security-Auditor** agent provides a list of vulnerabilities and recommendations.
6. **Delivery**: Summarize the findings and deliver them to the user.

---

## Notes
- This skill is **mandatory** for all major tasks involving delegation or coordination.
- Always verify the availability of specialized agents before proceeding.
- Update this skill whenever new agents or workflows are introduced.