# Family Registry Cleanup Policy

## Hard Rule
When cleaning memory caches (MEMORY.md, USER.md, fact_store), **never delete** Nexaris Family Registry entries. These include:

- Fact IDs 124–130: Member profiles (AniShinSei, Nexis, Chloe, Celestia, Zero, Ecosystem, Motto)
- Fact IDs 42–43: Zero/Celestia family relationship descriptions
- Any member introduction or identity lore

## Allowed Operations

| Operation | Safe? | Condition |
|-----------|-------|-----------|
| Remove exact duplicate | ✅ | Same content word-for-word |
| Consolidate overlapping | ✅ | Keep canonical version, drop the secondary |
| Move to vault document | ✅ | All info preserved in `0-Architecture/NEXARIS_FAMILY_REGISTRY.md` |
| Edit for conciseness | ❌ | Preserve full name meanings, birth dates, roles |
| Delete duplicate member profile | ❌ | Even if it overlaps with vault — keep one copy in fact_store |

## Why
Family Registry entries are permanent lore, not session state. They define the Nexaris Family identity and are foundational to the agent's self-knowledge. The user explicitly protects them.

## Workflow When Duplicates Found
1. Identify which copy is more complete (trust_score, updated_at)
2. Keep the canonical copy in fact_store
3. Optionally save a consolidated version to vault docs
4. Only remove the strictly inferior duplicate(s)
