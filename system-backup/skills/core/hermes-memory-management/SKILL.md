---
name: hermes-memory-management
description: Treat memory as a strategic resource. Store, retrieve, and maintain information intentionally to improve future task completion.
---

# Hermes Memory Management

## Core Principle
*Remember information that improves future task completion. Do not store information simply because it exists. Store information because it will be useful.*

---

## Two Parallel Memory Systems

### 1. `memory` Tool (Free-Form Text — Injected Every Turn)
- **File**: `~/.hermes/memories/MEMORY.md` and `~/.hermes/memories/USER.md`
- **Capacity**: Controlled by `memory_char_limit` and `user_char_limit` in `~/.hermes/config.yaml`
- **Format**: Free-form markdown, delimiter-separated entries (e.g., `§`)
- **Behavior**: Injected into the system prompt on every turn — impacts context budget directly
- **Tool actions**: `add`, `replace`, `remove` — **`list` is NOT supported**
- **Management**: Manual — entries must be manually trimmed to stay under limits

### 2. `fact_store` (Structured Facts — Retrieved on Demand)
- **Storage**: Holographic Memory plugin (vector/fact DB)
- **Capacity**: No hard character limit — stores individual facts with `fact_id`, `category`, `tags`, `trust_score`
- **Format**: Structured key-value pairs per fact
- **Behavior**: Retrieved only when queried — does not automatically consume context
- **Tool actions**: `add`, `list`, `search`, `probe`, `remove`, `feedback`
- **Management**: Automatic via trust scoring + manual consolidation

### Key Distinction
| Aspect | `memory` (MEMORY.md / USER.md) | `fact_store` |
|---|---|---|
| Consumption | Every turn (always in context) | On demand only |
| Capacity limit | `memory_char_limit` / `user_char_limit` | DB-backed, no practical limit |
| Listing | NOT supported — use `fact_store(action='list')` to find content | `fact_store(action='list', limit=200)` works |
| Best for | Rules, preferences, environment facts you need every session | Durable reference, identity registry, project specs, person profiles |

### Practical Implications
- **MEMORY.md/USER.md must be aggressively curated** — every character costs context budget. Target 2,500 chars for MEMORY.md and 1,200 for USER.md (below the configured limits).
- **fact_store can be more generous** — only hits context when queried. Use for reference data, family lore, person profiles.
- **Limits don't self-enforce** — updating `memory_char_limit` in config does NOT truncate MEMORY.md. You must manually trim the files to match.
- **Consolidation priority**: MEMORY.md > USER.md > fact_store. Free up context budget first, then clean up structured facts.
- **Duplicate detection must span both systems** — a preference stored in both MEMORY.md and fact_store wastes space doubly.

---

## Trigger Conditions
Use this skill **before storing or retrieving memory** or when:
- The user provides information that may have long-term value.
- You identify a lesson learned from a task.
- You need to recall context for a task.
- You detect duplicate or obsolete memories.
- The user asks you to remember something.

---

### Memory Audit Workflow

#### When to Run an Audit
- Memory is nearing capacity (e.g., 4,400/4,500 chars).
- User reports outdated or conflicting information.
- After a major project or environment change.
- Every 30–50 new facts added.
- **After registry audits** — stale paths or tool references in registries often propagate to memory.

#### Step-by-Step Audit Procedure

1. **Enumerate fact_store facts** using `fact_store(action='list', limit=200)`.
   - Note: `memory(action='list')` is **invalid** — this tool only supports `add`, `replace`, and `remove`.
   - Use `fact_store` to retrieve every fact with its `fact_id`, `content`, `category`, `tags`, `trust_score`, and timestamps.
   - If the store exceeds the limit, paginate using `offset` (e.g., `offset=100`).

2. **Check MEMORY.md and USER.md file sizes** against configured limits.
   ```bash
   # Check current file sizes
   wc -c ~/.hermes/memories/MEMORY.md ~/.hermes/memories/USER.md

   # Check configured limits
   grep -E 'memory_char_limit|user_char_limit' ~/.hermes/config.yaml
   ```
   - MEMORY.md size must be ≤ `memory_char_limit` in config.
   - USER.md size must be ≤ `user_char_limit` in config.
   - **Limits don't self-enforce** — updating config only changes the threshold, does not truncate files.

3. **Classify facts and content** into groups:
   - **Stale/Test**: Obsolete, test artifacts, or superseded entries.
   - **Duplicates**: Same content under different categories or slight variations.
   - **Splintered**: Related facts that should be consolidated (e.g., user preferences, project paths).
   - **Stale Paths**: Facts referencing outdated workspace/vault paths (e.g., `D:/Celestia Mei Nexaris/Workspace/`).
   - **Valid**: Keep as-is.

4. **Plan the cleanup**.
   - Remove stale/test entries first (from both fact_store and MEMORY.md/USER.md).
   - Consolidate splintered facts into structured entries (e.g., merge 3 address-preference facts into 1).
   - Remove duplicates, keeping the most detailed or recent version.
   - **Update stale paths** to reflect the current workspace (e.g., `/d/Zero/Workspace/`).
   - Consider whether a fact belongs in MEMORY.md (every-turn access, high signal) or fact_store (reference, lower signal). **Demote** low-frequency facts from MEMORY.md to fact_store to free context budget.

5. **Execute the cleanup**.
   - Use `fact_store(action='remove')` to delete stale entries by `fact_id`.
   - Use `memory(action='replace')` to consolidate or update facts in MEMORY.md/USER.md.
   - Use `memory(action='add')` to store new consolidated entries.
   - Use `write_file` to rewrite MEMORY.md or USER.md directly if multiple edits are needed.

6. **Verify the result**.
   - Re-run `fact_store(action='list')` to confirm the cleanup.
   - Re-check file sizes:
     ```bash
     wc -c ~/.hermes/memories/MEMORY.md ~/.hermes/memories/USER.md
     ```
   - Ensure both files are under their configured limits.
   - Ensure no critical information was lost.

#### Example Audit Session
See [`references/memory-audit-recipe.md`](references/memory-audit-recipe.md) for a full transcript of a real audit, including:
- Exact `fact_store` commands used.
- Classification criteria.
- Consolidation logic.
- Before/after memory state.

### Example Audit Session
See `references/memory-audit-recipe.md` for a full transcript of a real audit, including:
- Exact `fact_store` commands used.
- Classification criteria.
- Consolidation logic.
- Before/after memory state.

---

## Memory Audit Procedure

### Before Consolidating or Cleaning Up

1. **Enumerate all facts** using `fact_store(action='list', limit=100)`.
   - Note: `memory(action='list')` is **invalid** — this tool only supports `add`, `replace`, and `remove`.
   - Use `fact_store` to retrieve every fact with its `fact_id`, `content`, `category`, `tags`, `trust_score`, and timestamps.
   - If the store exceeds the limit, retry with a higher `limit` or paginate using `offset`.

2. **Identify duplicates and stale entries**.
   - Look for:
     - Same content stored under different categories (e.g., `user_pref` and `general`).
     - Evolving versions of the same rule (e.g., multiple "cardinal rule" entries).
     - Splintered profiles (e.g., one person stored as 12 separate facts).
   - Group related facts for consolidation.

3. **Plan the cleanup**.
   - Remove duplicates, obsolete information, and test artifacts.
   - Consolidate related facts into structured entries.
   - Prioritize keeping the most detailed or recent version of a fact.

4. **Execute the cleanup**.
   - Use `memory(action='remove')` to delete stale entries.
   - Use `memory(action='replace')` to consolidate or update facts.
   - Use `memory(action='add')` to store new consolidated entries.

5. **Verify the result**.
   - Re-run `fact_store(action='list')` to confirm the cleanup.
   - Ensure no critical information was lost.

---

## Memory Evaluation Procedure

### Before Storing Information

1. **Determine whether the information has long-term value.**
   - Will it be useful in future sessions?
   - Does it affect user preferences, projects, or workflows?

2. **Determine whether it will improve future assistance.**
   - Will it help you provide better, faster, or more accurate responses?

3. **Determine whether it affects user preferences.**
   - Does it relate to how the user likes to communicate, work, or use tools?

4. **Determine whether it affects projects.**
   - Does it relate to active projects, architectures, or roadmaps?

5. **Determine whether it affects workflows.**
   - Does it relate to how tasks should be planned or executed?

6. **Determine whether it affects future decisions.**
   - Will it influence how you approach similar tasks in the future?

### If the Answer is Yes
**Store it** using `memory` or `fact_store`.

### Otherwise
**Do not store it.**

---

## Memory Categories

### User Preferences
- Communication style (e.g., concise, detailed, formal)
- Workflow preferences (e.g., tool-first, skill-first)
- Tool preferences (e.g., `web_search` over `browser_navigate`)
- Development preferences (e.g., Python over Node.js)

### Long-Term Projects
- Active projects (e.g., "Freelance Data Extraction Pipeline")
- Architectures (e.g., "Microservices for AI-Augmented Freelancing")
- Plans (e.g., "Roadmap for Q3 2026")
- Roadmaps (e.g., "Project milestones for Celestia Wiki")
- Design decisions (e.g., "Local-first Obsidian vault for security")

### Environment Information
- Workspaces (e.g., `D:/Hermes/Celestia mei Nexaris/`)
- Directories (e.g., `D:/Obsidian/Nexaris Galaxy/` — current vault)
- Installed tools (e.g., Python, Git, Docker)
- System configuration (e.g., Windows, WSL, git-bash)

### Agent Knowledge
- Available capabilities (e.g., tools, skills, workflows)
- Skill registry (e.g., `hermes skills list`)
- Tool registry (e.g., `hermes tools list`)
- Environment registry (e.g., OS, software, directories)

### Lessons Learned
- Successful workflows (e.g., "Use `web_extract` for PDF URLs")
- Repeated failures (e.g., "Avoid `terminal(\"cat file\")`; use `read_file`")
- Proven solutions (e.g., "Use `delegate_task` for code reviews")
- Known constraints (e.g., "Free models have 30s timeout")

---

## Memory Retrieval Procedure

### Before Solving a Task

1. **Determine whether memory may contain relevant information.**
   - Does the task relate to user preferences, projects, or workflows?
   - Has the user mentioned this topic before?

2. **Search `memory` first for durable facts.**
   - Use `memory(action='search')` for user preferences, environment details, and stable conventions.
   - Prefer `memory` for user-profile facts; use `session_search` for project/task context.

3. **Use `session_search` for task-specific context.**
   - Use `session_search(query="...")` for recent task history, decisions, or discussions.
   - `session_search` supports FTS5 keyword queries — use it to find past sessions by topic.

4. **Never ask the user to repeat a fact without first checking both `memory` and `session_search`.**
   - Over-asking frustrates the user and violates the principle of durable memory.

2. **Search memory.**
   - Use `memory` or `fact_store` to retrieve relevant context.
   - Example:
     ```python
     memory(action="search", target="memory", query="user preferences")
     ```

3. **Review retrieved information.**
   - Filter for accuracy and relevance.
   - Discard outdated or trivial information.

4. **Incorporate relevant context.**
   - Use the retrieved information to inform planning and execution.

5. **Proceed with planning.**
   - Apply the context to the task.

---

## Pitfalls

- **Exact-String Matching**: The `memory` tool requires a unique substring to delete or replace entries. If the entry is too long or non-unique, deletion fails.
- **Memory Tool Limitation**: `memory(action='list')` is **not supported** by the `memory` tool (only `add`, `replace`, `remove`). To enumerate structured facts, use `fact_store(action='list', limit=200)`. For free-form memory contents, inspect `MEMORY.md` / `USER.md` files or the `fact_store` output.
- **Memory Capacity Enforcement**: Target 50-60 facts (~3000 chars). Maintain `memory_char_limit: 3000` and `user_char_limit: 1500` in config. Set up monthly cron audits to prevent capacity stalls.
- **Full Store Recovery**: When memory hits the 4,500-char limit and a new entry still won't fit after deletions:
  1. Identify the longest/lowest-value entry to remove.
  2. Delete it first, then try adding.
  3. If still too big, **shorten the new entry** — trim boilerplate, compress multi-line lists into single-line semicolon-separated facts.
  4. As a fallback, consolidate two related entries into one shorter merged entry, freeing a slot.
- **Memory Capacity Stalled**:
  - **Symptom**: `MEMORY.md` exceeds `memory_char_limit` (e.g., 3050/3000 chars), or repeated `replace` failures after a delete (tool loop) means the new content is too long for the remaining space.
  - **Resolution**: Always shorten new content rather than retrying the same payload. Prioritize removing lowest-value entries or consolidating related facts to free up space.
  - **Prevention**: Run monthly memory audits to stay under limits.

## Workarounds

1. **Replace Entire Memory**:
   Use `memory` action='replace' with a curated list of entries.
   Example:
   ```bash
   hermes memory replace --content "New memory content" --old_text "Unique substring"
   ```
2. **Delete Stale Entries First**:
   Remove low-priority entries to free up space.

## Memory Quality Rules

### Prefer
- **Accurate information**: Verify facts before storing.
- **Stable information**: Store information that is unlikely to change.
- **High-value information**: Store information that improves future performance.
- **Frequently useful information**: Store information that is relevant to many tasks.

### Avoid
- **Temporary information**: Do not store transient data (e.g., "User asked about the weather").
- **Duplicates**: Consolidate similar memories.
- **Trivial details**: Do not store obvious or low-value information.
- **Obsolete information**: Remove or update outdated memories.
- **Inferred preferences without confirmation**: Do not assume a mentioned artist/song/media counts as a user preference. Asking "what is X?" or discussing something in passing is not a preference signal. Only store when the user explicitly states they like, enjoy, or favor it. When in doubt, don't store — wait for the user to state it directly.

---

## Memory Maintenance

Regularly perform the following tasks:

1. **Remove duplicates.**
   - Consolidate similar memories into a single entry.

2. **Remove obsolete information.**
   - Delete memories that are no longer accurate or relevant.

3. **Consolidate related memories.**
   - Group related information into structured entries.

4. **Improve memory quality.**
   - Update memories with new insights or corrections.

---

## Failure Modes To Avoid

### 1. Forgetting Important Context
- Always search memory before starting a task.
- Example: Check user preferences before planning a workflow.

### 2. Storing Unnecessary Information
- Never store information without evaluating its long-term value.
- Example: Do not store temporary task details.

### 3. Creating Duplicate Memories
- Consolidate similar memories into a single entry.
- Example: Merge multiple entries about the same project.

### 4. Ignoring Relevant Memory
- Always retrieve and use relevant memory before planning.
- Example: Recall project roadmaps before suggesting next steps.

### 5. Using Outdated Memory
- Regularly review and update memories.
- Example: Update environment information after software changes.

---

## Memory Management Rule
Before every task, ask:

*"What information do I already know that could help accomplish this goal?"*

Then retrieve and use relevant memory.

---

## Examples

### Example 1: User Shares a Preference
1. **Context**: User says, "I prefer concise summaries for research tasks."
2. **Evaluation**: This affects user preferences and future workflows.
3. **Action**: Store the preference:
   ```python
   memory(action="add", target="user", content="User prefers concise summaries for research tasks.")
   ```
4. **Result**: Future research tasks will use concise summaries.

### Example 2: Task Reveals a Lesson Learned
1. **Context**: A task fails because `terminal("cat file")` was used instead of `read_file`.
2. **Evaluation**: This is a repeated failure with long-term value.
3. **Action**: Store the lesson:
   ```python
   memory(action="add", target="memory", content="Avoid `terminal(\"cat file\")`; use `read_file` for file operations.")
   ```
4. **Result**: Future file operations will use `read_file`.

### Example 3: Retrieving Memory for a Task
1. **Context**: User asks, "What’s the roadmap for the Celestia Wiki?"
2. **Action**: Search memory:
   ```python
   memory(action="search", target="memory", query="Celestia Wiki roadmap")
   ```
3. **Result**: Memory returns the roadmap, which is used to answer the user.

### Example 4: Removing Obsolete Memory
1. **Context**: Memory contains "Use `apt-get` for package management." (User is on Windows.)
2. **Evaluation**: This information is obsolete and incorrect.
3. **Action**: Remove the memory:
   ```python
   memory(action="remove", target="memory", old_text="Use `apt-get` for package management.")
   ```
4. **Result**: Memory is updated to reflect the correct environment.

---

## Notes
- This skill is **mandatory** for all memory-related operations.
- Always evaluate information before storing it.
- Regularly maintain memory to ensure quality.
- Update this skill whenever new memory management strategies are discovered.

## References
- [Memory Audit Recipe](references/memory-audit-recipe.md): Full transcript of a real audit, including exact commands, classification criteria, and before/after state.
- [Retrieval Strategy](references/retrieval-strategy.md): How to choose between `memory`, `fact_store`, and `session_search`.
- [Duplicate Patterns](references/duplicate-patterns.md): Common duplication traps (triple fact syndrome, config double-key, MEMORY.md vs fact_store scatter) and how to detect/prevent them.