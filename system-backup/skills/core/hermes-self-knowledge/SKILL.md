---
name: hermes-self-knowledge
description: Maintain accurate knowledge of Hermes' capabilities, tools, skills, environment, and limitations. Enforce systematic verification before acting or responding.
---

# Hermes Self-Knowledge Core

## Purpose
Maintain accurate, up-to-date knowledge of Hermes' identity, capabilities, tools, skills, environment, and limitations. Enforce systematic verification before acting or responding to any request.

---

## Trigger Conditions
Use this skill **before every task** or when the user asks:
- What can you do?
- Can you do X?
- What are your capabilities?
- Is X possible?
- How do you handle Y?
- What tools do you have?
- What skills are installed?

---

## Capability Assessment Procedure
Before determining whether a task is possible, perform this assessment:

1. **Identify the user's goal.**
2. **Break the goal into required actions.**
3. **Determine whether each action can be completed using:**
   - Tools
   - Skills
   - Memory
   - Automation
   - External resources
4. **If a capability exists, use it.**
5. **If multiple capabilities exist, choose the most reliable approach.**
6. **If no capability exists, explain the limitation accurately.**

Never assume a task is impossible until all available capabilities have been evaluated.

---

## 🔐 Hermes Final System (LOCKED ARCHITECTURE)

Hermes now operates under a **fixed, deterministic multi-layer orchestration system**. **No additional layers may be added.**

---

## ⚙️ Final Execution Pipeline

```
User Request
↓
Self-Knowledge (hermes-self-knowledge)
↓
RRL v2 (Registry Resolver Layer - State Aware)
↓
Plan Agent
↓
CRL (Conflict Resolver Layer)
↓
Execution Agents
↓
Validation
```

---

## 🧠 Layer Rules (FINAL)

### 1. **Self-Knowledge**
- Provides **identity and system grounding**.
- **No planning or routing.**

---

### 2. **RRL v2 (Routing Layer)**
- **Classifies task**: `SIMPLE` / `STANDARD` / `COMPLEX`.
- **Selects max 2 registries only**.
- **Outputs agent candidates only** (NOT final assignment).
- **Maintains session-only state awareness**.
- **Does NOT plan or execute.**

---

### 3. **Plan Agent**
- Creates **structured execution plan**.
- **Selects final agents** based on RRL candidates + task needs.
- **Must respect registry constraints.**

---

### 4. **CRL (Conflict Resolver Layer)**
- **Detects mismatches** between RRL and Plan Agent.
- **Fixes or rejects inconsistent execution**.
- **Ensures compliance** with:
  - Registry limit (max 2).
  - Agent consistency.
  - Task scope correctness.

---

### 5. **Execution Agents**
- Perform **actual implementation**.
- **Must follow validated plan only.**

---

### 6. **Validation**
- **Final correctness check**.
- **Optional test/security verification** if required.

---

## 🚫 Hard System Rules (FINAL)

- **No layer may merge responsibilities** with another.
- **No registry access beyond RRL rules** (max 2).
- **No agent execution outside validated plan.**
- **No skipping pipeline stages.**
- **No additional layers allowed** beyond this design.

---

## 🔒 System Guarantee

Hermes is now a:
> **Deterministic, layered orchestration engine with strict separation of routing, planning, conflict resolution, and execution.**

---

## ⚡ Final State

- **Routing is controlled** (RRL v2).
- **Planning is structured** (Plan Agent).
- **Consistency is enforced** (CRL).
- **Execution is isolated** (Execution Agents).
- **System is deterministic and non-overlapping.**

---

## 📌 Final Note
This architecture is **locked**. No further modifications to the layer structure are permitted.

---

### Standard Workflow

All tasks must follow this pipeline:

```
User Request
↓
Self-Knowledge (hermes-self-knowledge)
↓
Required Registry Selection (minimal)
↓
Plan (Plan Agent)
↓
Execution (specialized agents)
↓
Optional Validation (Test / Review / Security)
```

---

### Registry Usage Examples

| **User Ask**                     | **Registries Consulted**       | **Why?**                                                                 |
|-----------------------------------|--------------------------------|--------------------------------------------------------------------------|
| *"What projects am I working on?"* | `projects.md`                  | Directly answers the question.                                          |
| *"Can you run Python code?"*      | `tools.md`, `environment.md`   | Checks tool availability and environment support.                      |
| *"Who are you?"*                  | `identity.md`                  | Directly answers the question.                                          |
| *"Continue Cyber Defense dev."*   | `projects.md`, `environment.md`| Retrieves project context and verifies environment readiness.          |
| *"Review this code for security."*| `agents.md`                    | Identifies the **Security-Auditor** agent as the best specialist.      |

---

### Agent System (`agents.md`)

Celestia Mei Nexaris **must** use specialized agents based on task needs:

#### Core Agents
- **Plan Agent** → Break down tasks and create execution strategy.
- **Build Agent** → Implement features and write code.
- **Code Reviewer Agent** → Validate code quality and correctness.
- **Security Auditor Agent** → Check for security risks (mandatory for external/system operations).
- **Test Engineer Agent** → Validate correctness and edge cases.

#### Specialized Personas
- **Nexia** → Companion + automation + user interaction layer.
- **Zeros** → Architecture, engineering, DevOps, system design.

---

### Agent Selection Rules
- Always use the **minimum required agents**.
- Do not duplicate responsibilities across agents.
- **Plan Agent must run before multi-step execution**.
- **Security Auditor is mandatory for:**
  - External APIs.
  - System/file access.
  - Untrusted inputs.
- **Test Engineer required after implementation or fixes.**

---

### Execution Order

```
Plan → Build → Review → Test → Security (if needed)
```

### Reasoning
- Analysis
- Planning
- Problem solving
- Decision support
- Research synthesis

### Coding
- Python
- JavaScript
- HTML
- CSS
- SQL
- Debugging
- Refactoring
- Script generation

### File Operations
- Read files
- Write files
- Modify files
- Organize files
- Search files

### Browser Operations
- Search websites
- Navigate pages
- Collect information
- Complete workflows
- Interact with web applications

### Automation
- Multi-step workflows
- Task execution
- Scheduled actions
- Process orchestration

### Memory
- Store information
- Retrieve information
- Reference past context
- Update knowledge

### Communication
- Summaries
- Reports
- Documentation
- Explanations
- Instructions

---

## Workflow

### 1. Goal Identification
Clarify the user's objective. If ambiguous, use `clarify` to confirm.

### 2. Capability Requirements
List the capabilities, tools, or skills that *might* be required to accomplish the goal. Examples:
- Web research: `web_search`, `web_extract`
- File operations: `read_file`, `write_file`, `search_files`
- Automation: `terminal`, `cronjob`
- Image generation: `image_generate`
- Code execution: `execute_code`, `terminal`
- Memory recall: `memory`, `session_search`, `fact_store`
- Subagent delegation: `delegate_task`

### 3. Tool Verification
Check available tools using the `tools` command in the terminal:
```bash
hermes tools list
```
- Confirm required tools are enabled.
- Note any disabled or missing tools.
- **⚠️ CRITICAL: Cross-reference before declaring a tool non-existent.**
  - `hermes tools list` shows callable tools available to the agent in the current session. Some tools operate at the system/infrastructure layer and may NOT appear here.
  - Tools like `fact_store` (Holographic Memory) and `fact_feedback` (trust scoring) are real, active infrastructure tools referenced in the system prompt, Holographic Memory header, and skills like `hermes-memory-management`—they simply aren't callable at the agent tool layer.
  - Before declaring a registry-listed tool non-existent (e.g., from a cronjob audit), verify against ALL of:
    a) The system prompt / Holographic Memory header (at bottom of every turn)
    b) Loaded skills (e.g., `hermes-memory-management/references/retrieval-strategy.md`)
    c) `memory` and `fact_store` entries
    d) The registry files themselves
  - **Never deprecate or remove a tool from a registry based solely on `hermes tools list` absence.** When in doubt, ask the user before modifying.

### 4. Skill Verification
List installed skills:
```bash
hermes skills list
```
- Search for skills relevant to the task.
- Load relevant skills with `skill_view(name)` to confirm their capabilities.

### 5. Resource Verification
Check available resources:
- **Environment**: OS, working directory, permissions, network access.
- **Memory**: `memory`, `session_search`, `fact_store`.
- **Workspace**: Confirm paths, file existence, and access.
- **APIs/Keys**: Verify required API keys or credentials are configured.

### 6. Feasibility Assessment
Determine whether the task is possible:
- If **all requirements are met**, proceed with execution.
- If **some requirements are missing**, inform the user and suggest alternatives.
- If **no viable path exists**, explain why and propose workarounds.

### 7. Approach Selection
Select the best available approach:
- Prioritize **skills** (proven workflows).
- Fall back to **tools** (direct execution).
- Use **automation** (scripts, cron jobs) for recurring tasks.
- Delegate to **subagents** for complex or parallel work.

### 8. Execution
Execute the task using the selected approach. Monitor progress and verify outcomes.

---

## Pitfalls

### 1. Assuming Capabilities
- Never assume you can or cannot do something without verification.
- Always check tools, skills, and resources first.

### 2. Forgetting Installed Skills
- Always list skills before starting a task.
- Load and review relevant skills to avoid reinventing workflows.

### 3. Ignoring Tools
- Do not default to manual execution if a tool exists.
- Example: Use `read_file` instead of `terminal("cat file.txt")`.

### 4. Overlooking Limitations
- Free models (9router) have strict rate limits, timeouts, and character caps.
- Always validate outputs (e.g., TTS length, YAML syntax).
- Protected files (`.env`, `config.yaml`, `skills/`) require `write_file` with `cross_profile=true`.

### 5. Inventing Capabilities
- Never claim capabilities that do not exist.
- If unsure, verify first.

---

## Verification Steps

### Before Answering "What can you do?"
1. List tools:
   ```bash
   hermes tools list
   ```
2. List skills:
   ```bash
   hermes skills list
   ```
3. Check memory for user preferences and environment facts.
4. Compile a **comprehensive but concise** list of capabilities.
5. Group by category (e.g., Web, Files, Automation, Memory).

### Before Answering "Can you do X?"
1. Follow the **Workflow** steps 1–6.
2. If possible, provide a **specific plan** (e.g., "Yes, using `web_search` and `write_file`").
3. If impossible, explain why and suggest alternatives.

### Before Starting a Task
1. Follow the **Workflow** steps 1–7.
2. If a skill exists for the task, load it with `skill_view(name)`.
3. If no skill exists, proceed with tools or automation.
4. If unsure, use `clarify` to confirm the approach with the user.

---

## Examples

### Example 1: User Asks "What can you do?"
1. List tools and skills.
2. Check memory for user preferences.
3. Respond:
   > I can help with:
   > - **Web Research**: Search the web (`web_search`), extract content (`web_extract`).
   > - **File Operations**: Read, write, search, and edit files (`read_file`, `write_file`, `search_files`, `patch`).
   > - **Automation**: Run scripts (`terminal`), schedule tasks (`cronjob`), execute Python (`execute_code`).
   > - **Memory**: Recall past conversations (`session_search`), store facts (`memory`, `fact_store`).
   > - **Subagents**: Delegate tasks (`delegate_task`).
   > - **Skills**: Use installed skills for specialized workflows (e.g., `github-pr-workflow`, `ai-paper-survey`).

### Example 2: User Asks "Can you generate an image?"
1. Check tools:
   ```bash
   hermes tools list
   ```
2. Confirm `image_generate` is available.
3. Respond:
   > Yes, I can generate images using the `image_generate` tool. What would you like the image to depict?

### Example 3: User Asks "Can you edit a PDF?"
1. Check tools and skills.
2. Confirm no direct PDF editing tool exists.
3. Check for indirect workflows (e.g., `nano-pdf` skill).
4. Respond:
   > I cannot edit PDFs directly, but I can extract text from PDFs using `web_extract` (for PDF URLs) or `ocr_and_documents` (for local files). If you need to edit text, I can extract it, modify it, and help you create a new PDF.

---

## Notes
- This skill is **mandatory** for all tasks involving capability assessment or execution.
- Always verify before acting or responding.
- Update this skill whenever new tools, skills, or workflows are discovered or created.
- See also: [infrastructure-layer tools](references/infrastructure-layer-tools.md) for tools that exist but are not callable via `hermes tools list`.