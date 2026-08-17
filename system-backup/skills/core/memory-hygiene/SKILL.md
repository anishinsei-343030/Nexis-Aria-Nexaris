---
name: memory-hygiene
description: Periodic memory audit and cleanup workflow — trim MEMORY.md/USER.md to limits, consolidate fact_store duplicates, and vault identity data without deletion.
---

# Memory Hygiene

## When to Use

- User asks to "clean up memory," "audit facts," "reduce memory usage," or similar
- Memory limits are being breached (MEMORY.md > `memory_char_limit`, USER.md > `user_char_limit`)
- Monthly/scheduled memory maintenance
- Before major system upgrades that add new persistent knowledge

## Workflow

### 1. Assess Current State

- Read memory files: `read_file ~/.hermes/memories/MEMORY.md` and `read_file ~/.hermes/memories/USER.md`
- List all fact_store entries: `fact_store(action='list', limit=100)` — note: `memory(action='list')` is **not supported**, use `fact_store` instead
- Check char counts: `wc -c ~/.hermes/memories/MEMORY.md ~/.hermes/memories/USER.md`

### 2. Trim MEMORY.md / USER.md

- Remove stale placeholder lines (e.g. "Placeholder check — looking up existing user info")
- Consolidate verbose entries into concise single-line facts
- Use `patch` for targeted removals or `write_file` for full rewrite
- Target: under `memory_char_limit` (default 3000) and `user_char_limit` (default 1500)

### 3. Clean fact_store

**Remove duplicates (safe to delete):**
- Exact content duplicates (same info repeated in multiple fact IDs)
- Stale task notes, old postmortems, session artifacts
- Superseded preferences where a newer fact covers the same ground

**Consolidate overlapping facts (remove old → add merged):**
- Merge multiple addressing-preference facts into one compact entry
- Merge duplicate tool-config facts (e.g. Playwright path stored in 3 facts → 1)
- Add the consolidated fact first, then remove the originals

**CRITICAL: Family Registry / Identity Data**
- **Never delete** Nexaris Family Registry entries (#124-#130), identity profiles, or member introductions
- If duplicates exist among identity facts: keep one canonical entry, remove exact duplicates only
- When moving content out of fact_store: create a vault document at `0-Architecture/NEXARIS_FAMILY_REGISTRY.md` and preserve all information intact
- Rule: move to vault or consolidate duplicates — never delete non-duplicate identity data

### 4. Verify

- Re-check MEMORY.md and USER.md char counts
- Re-list fact_store to confirm cleanup took effect
- Update vault `index.md` if new permanent documents were created

## Pitfalls

- **`memory(action='list')` is not a valid command** — use `fact_store(action='list', limit=100)` instead
- **Never delete core identity facts** — Family Registry entries contain permanent lore. Only remove exact duplicates.
- **Don't compress identity data** — preserve full name meanings, birth dates, and role descriptions when vaulting
- MEMORY.md/USER.md hard limits are set in `config.yaml` — enforce them strictly while preserving substantive content
- After trimming, re-verify the file still reads correctly — aggressive consolidation can lose nuance

## Reference Files

- `references/family-registry-cleanup-policy.md` — the no-deletion rule for identity data during cleanup

## Related

- `hermes-memory-management` core skill (protected — this skill implements the user-specific workflow on top of it)
- Vault docs under `0-Architecture/` for permanent knowledge storage
