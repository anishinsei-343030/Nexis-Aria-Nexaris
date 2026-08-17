# Delegate Task Orchestration Reference

## Current Limitations (this environment)

| Constraint | Value |
|------------|-------|
| Max concurrent children | 3 |
| Max spawn depth | 1 (no nested delegation) |
| Nesting policy | OFF — leaf agents cannot delegate further |
| `notify_on_complete` | Required for long-running tasks |

## When to Use

- **Reasoning-heavy subtasks** (debugging, code review, research synthesis)
- **Tasks that would flood parent context** with intermediate data
- **Parallel independent workstreams** (research A and B simultaneously)

## When NOT to Use

| Scenario | Alternative |
|----------|-------------|
| Mechanical multi-step work with no reasoning | `execute_code` |
| Single tool call | Call the tool directly |
| Tasks needing user interaction | Subagents cannot use `clarify` |
| Long-running background work (must survive current turn) | `cronjob(action='create')` or `terminal(background=true, notify_on_complete=true)` |

## Verification Rule

Subagent summaries are **self-reports, not verified facts**. For operations with external side-effects (HTTP POST/PUT, remote writes, file creation at shared paths, publishing):

1. Require subagent to return a verifiable handle (URL, ID, absolute path, HTTP status).
2. Verify independently — fetch the URL, stat the file, read back content.
3. Only then report success to the user.

## Lifecycle

- `delegate_task` runs **synchronously** inside the parent turn.
- If the parent is interrupted (user sends new message, `/stop`, `/new`), the child is **cancelled** with status `interrupted` and its work is discarded.
- Children **cannot** continue in the background.

## Memory and Context

- Subagents have **no memory** of your conversation.
- Pass all relevant info (file paths, error messages, constraints) via the `context` field.
- If the user is writing in a non-English language, or asked for output in a specific language/ tone, say so in `context`.