# Duplicate Patterns in Memory Systems

## Pattern: Triple Fact Syndrome
When consolidating facts, always check for **three or more copies** of the same information. After merging two, a third (or fourth) often remains.

### Examples from June 27, 2026 Audit

| Topic | Fact IDs | Consolidated To |
|-------|----------|-----------------|
| FB account info | #116, #117, #118 | #116 (updated) |
| "Verify before edit" rule | #119, #120, #121 | #119 (updated) |
| Browser setup specs | #108, #109 | #108 (updated) |
| Nexis sister rule | #16, #17 | #16 (updated) |
| Addressing preferences | #4, #15 | #4 (updated) |
| Favorite singer | #77, #115 | #77 (updated) |
| Family identity | #42, #43, #45, #46 | #42 (updated) |
| Credential scatter | #1, #8, #9, #10, #11, #12 | #1, #8, #9 (consolidated) |

### Root Cause
- **Incremental refinement**: Each fact is a slightly improved version of the last, but the old ones aren't removed.
- **Tool limitation**: `memory(action='replace')` requires a unique substring — if the old fact isn't unique enough, it stays.
- **Human oversight**: After merging two, the third is easy to miss.

### Detection Rule
After merging two facts, **always search for the topic one more time** — there's usually a third.

### Prevention
- **Atomic updates**: When updating a fact, remove the old version immediately.
- **Topic tagging**: Use a consistent tag (e.g., `#addressing`, `#fb-account`) to group related facts.
- **Audit hook**: Add a cron job that flags any topic with 3+ facts:
  ```bash
  hermes cronjob create --schedule "0 0 * * 1" --prompt "Audit memory for topics with 3+ facts. Report any found."
  ```

## Pattern: Config Double-Key Trap

### Example
```yaml
agent:
  reasoning_effort: xhigh
  reasoning_effort:   # empty value overrides xhigh
```

### Root Cause
- **YAML parsing**: Duplicate keys are allowed — the last one wins.
- **sed misfire**: A `sed` pattern that doesn't match exactly can insert a new key instead of replacing the old one.

### Detection
```bash
grep -n 'reasoning_effort\|memory_char_limit\|user_char_limit\|show_reasoning' ~/.hermes/config.yaml
```

### Prevention
- **Exact sed patterns**: Use line numbers or unique context to avoid inserting duplicates.
- **Post-edit verification**: Always `grep` the key after editing.
- **Config linting**: Add a cron job to check for duplicate keys:
  ```bash
  hermes cronjob create --schedule "0 0 * * 1" --prompt "Check ~/.hermes/config.yaml for duplicate keys. Report any found."
  ```

## Pattern: MEMORY.md vs fact_store Scatter

### Example
- MEMORY.md: "Shin's favorite singer is John Michael Howell."
- fact_store: "User's favorite singer: John Michael Howell (fact_id #77)"

### Root Cause
- **Two parallel systems**: MEMORY.md (injected every turn) and fact_store (retrieved on demand) are managed independently.
- **Context budget pressure**: MEMORY.md is aggressively curated; fact_store is more generous.
- **Migration lag**: Facts moved from MEMORY.md to fact_store aren't always removed from MEMORY.md.

### Detection
```bash
grep -F "favorite singer" ~/.hermes/memories/MEMORY.md
fact_store(action='search', query='favorite singer')
```

### Prevention
- **Demotion rule**: When moving a fact from MEMORY.md to fact_store, **remove it from MEMORY.md immediately**.
- **Topic audit**: After any consolidation, search both systems for the topic.
- **Signal-to-noise ratio**: Keep MEMORY.md under 2,500 chars — every character costs context budget.