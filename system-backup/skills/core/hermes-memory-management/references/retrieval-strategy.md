# Memory Retrieval Strategy

## Order of Operations

1. **`fact_store`**
   - Use for durable facts: user preferences, environment details, stable conventions.
   - Example: "Shin's favorite singer", "Celestia's birthday", "workspace directory".

2. **`session_search`**
   - **Always check `session_search` for recent context before asking the user**, even if `fact_store` or `memory` has a partial match. This prevents re-asking for information the user recently provided.
   - Use for task-specific context: recent discussions, decisions, or workflows.
   - Example: "What did we do about the cronjob last time?", "What was the last music request?", "Did the user already provide the Composio API key?".

3. **User Ask**
   - Only if both `fact_store` and `session_search` return no results.
   - Save the answer to `fact_store` immediately after receiving it.

## Trust Scoring

- **High trust score (0.7+)**: Trust unless contradicted by newer information.
- **Medium trust score (0.4–0.7)**: Verify if the context is critical.
- **Low trust score (<0.4)**: Re-confirm with the user or `session_search`.

## Enumerating All Facts (Memory Audit)

`memory(action='list')` is **NOT a valid action** — this tool only supports `add`, `replace`, and `remove`.

To enumerate all stored facts, use **`fact_store(action='list', limit=100)`**. This returns every fact with its `fact_id`, `content`, `category`, `tags`, `trust_score`, and timestamps. Facts exceeding the limit won't appear — pass a higher `limit` (max varies by backend; retry with `offset` if needed).

Use this for:
- Memory audits (find duplicates, stale entries, test artifacts)
- Before consolidation (identify what exists before merging)
- Capacity planning (count vs. any known hard limit)

### Duplicate Detection Patterns

When auditing facts, watch for:
- **Same content stored under different categories** — e.g., `user_pref` and `general` both saying the same addressing preference.
- **Evolving versions of the same rule** — e.g., multiple facts saying "cardinal rule" with progressive refinement. Keep only the latest/most detailed.
- **Splintered profiles** — one person stored as 12 separate facts (name, school, FB URL, relationship, etc.). Consolidate into 1 structured entry.

## Pitfalls

- **Over-asking the user**: Always check `fact_store` and **`session_search`** first. Even if `fact_store` or `memory` has a partial match, check `session_search` for recent context before asking the user again.
- **Over-asking due to partial memory matches**: If `fact_store` or `memory` has a partial match but the user recently provided the same information, check `session_search` before asking again.
- **Ignoring trust scores**: Disregarding high-trust facts leads to redundant questions.
- **Session-only search**: Relying only on `session_search` may miss durable facts in `fact_store`.
- **Assuming `memory(action='list')` works**: It does not. Use `fact_store(action='list')` to enumerate facts.