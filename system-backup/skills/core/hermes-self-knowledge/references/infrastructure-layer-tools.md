# Infrastructure-Layer vs. Agent-Callable Tools

## Background

Some tools in the Hermes ecosystem operate at the **system/infrastructure layer** — they are real, active, and critical, but they are NOT callable as agent tools via `hermes tools list` or the tool library in the agent's context.

## Examples

| Tool | Layer | Callable? | Purpose |
|------|-------|-----------|---------|
| `memory` | Agent | ✅ Yes | Save/retrieve durable facts |
| `session_search` | Agent | ✅ Yes | Search past conversations |
| `fact_store` | Infrastructure | ❌ No (not agent-callable) | Holographic Memory — deep structured memory with algebraic reasoning, entity resolution, trust scoring (probe, search, add, reason, contradict) |
| `fact_feedback` | Infrastructure | ❌ No | Rate facts to train trust scores |

## The Pitfall

`hermes tools list` only shows tools available to the agent's callable toolset. **Infrastructure tools do NOT appear there.** If you search for `fact_store` in the tool list, you will not find it — yet it is real and powers the Holographic Memory system described at the bottom of every system prompt.

## Verification Procedure (before declaring a tool non-existent)

1. Check `hermes tools list` — ✅ if found, it's callable.
2. If NOT found in step 1, check:
   - The system prompt / Holographic Memory header (printed below the tools list every turn)
   - Loaded skills — especially `hermes-memory-management/references/retrieval-strategy.md`
   - `memory` entries about tools and capabilities
   - The registry files (`tools.md`, `environment.md`, etc.)
   - **Ask the user** if still uncertain — infrastructure tools are sensitive and should never be removed without confirmation.

## Case Study: fact_store

- Listed in `tools.md` under "Memory & Knowledge Tools"
- NOT callable via the agent tool interface (`hermes tools list` will not show it)
- IS real and powers my Holographic Memory via `fact_store(action='search'|'probe'|'add'|'reason'|...)` in the fact_store entity database
- Attempting to deprecate or remove it will earn swift correction from the user
