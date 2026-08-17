# Registry Audit Findings — 2026-06-30

## Summary
Read-only audit of Hermes registries. No edits applied. Findings below.

---

## 🔴 Misconfigurations (Functional Impact)

| File | Issue | Detail |
|------|-------|--------|
| `tools.md` | Documented non-existent tool | Lists `fact_store` tool, which does not exist in `hermes tools list`. Causes failed tool calls if invoked. |
| `environment.md` | Stale workspace subdirectories | Lists `images/` and `documents/` (lowercase), but actual subdirs are `Pictures/` and `Documents/` (case mismatch). Unlisted subdirs: `Hermes-Cloud/`, `Hermes-Social/`, `Psychology Videos/`, `Psychology Voice/`, `Scripts/`, `videos/`. |

---

## 🟡 Outdated Metadata

| File | Issue | Detail |
|------|-------|--------|
| `health.md` | Stale last-check date | Last updated June 25, 2026 (5 days stale). |

---

## 🟢 Stale Path References (Already Fixed in Registries)

| File | Issue | Status |
|------|-------|--------|
| `registries/*` | `wiki/` paths | No stale `wiki/` paths found in registries. |

---

## 🔄 Cross-Skill Stale References

| Skill | File | Issue | Lines |
|-------|------|-------|-------|
| `hermes-environment-awareness` | `SKILL.md` | Stale `wiki/` paths | 73, 131, 187, 188, 234 |
| `hermes-memory-management` | `SKILL.md` | Stale `wiki/` path | 201 |

---

## ✅ Verified Correct

| Check | Result |
|-------|--------|
| Registry files present | 8/8 files exist (`identity.md`, `environment.md`, `agents.md`, `projects.md`, `skills.md`, `tools.md`, `health.md`, `workflows.md`). |
| Case-insensitive duplicates | `AGENTS.md` and `agents.md` are same inode (Windows filesystem). No functional impact. |
| Cross-references | No broken cross-references found. |
| Family member names | `identity.md` lists Zero Riven Nexaris and Nexis Aria Nexaris — valid, not a mismatch. |
| Vault path | Current vault: `D:/Celestia Mei Nexaris/Celestia Mei Nexaris-Galaxy/`. No stale `D:/Celestia Mei Nexaris/wiki/` references in registries. |