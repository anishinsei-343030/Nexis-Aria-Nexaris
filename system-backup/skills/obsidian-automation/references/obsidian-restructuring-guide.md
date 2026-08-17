# Obsidian Vault Restructuring Guide

## Goal
Transform a wiki-style Obsidian vault into a long-term, scalable note-taking system optimized for retrieval, flexibility, and low maintenance.

## Steps

### 1. Backup the Vault
```bash
cp -r "/path/to/vault" "/path/to/vault-backup-$(date +%Y%m%d)"
```

### 2. Create New Folder Structure
```bash
mkdir -p "1-Projects" "2-Areas" "3-Resources" "4-Archive" "Attachments" "Daily" "Templates"
```
Note: Do NOT create "0-Inbox" unless the user specifically requests it — PARA starts at 1-Projects for users who prefer no inbox.

### 3. Move and Rename Notes
- **Concepts/Entities → 3-Resources/**
  ```bash
  mv "concepts/ai-augmented-freelancing.md" "3-Resources/20260615-freelance-ai-tools.md"
  mv "entities/aoi.md" "3-Resources/aoi.md"
  ```
- **Daily Logs → Daily/**
  ```bash
  mv "dailylogs/2026-06-13-daily-log.md" "Daily/20260613-daily.md"
  ```
  **Filename convention:** `YYYYMMDD-<tag>` (e.g., `20260613-daily`, `20260615-freelance-upwork`). Always rename the file when the link target changes — ghost nodes (wikilinks to nonexistent files) corrupt the graph.

### 4. Add Frontmatter
```yaml
---
id: 20260615-freelance-ai-tools
tags: [ai, freelance, project/active]
created: 2026-06-15
---
```

### 5. Replace Wikilinks
- Convert `[[shin]]` to plain text or `[[YYYYMMDD-title]]`
- Example: `[[ai-augmented-freelancing]]` → `[[20260615-freelance-ai-tools]]`

### 6. Create Templates
- **Daily Note** (`Templates/daily-note.md`):
  ```markdown
  ---
  id: {{date:YYYYMMDD}}
  tags: [daily]
  created: {{date:YYYY-MM-DD}}
  ---
  
  # {{date:YYYY-MM-DD}}
  
  ## Tasks
  - [ ] 
  
  ## Notes
  
  ## Ideas
  
  ## Links
  - [[{{date-1:YYYYMMDD}}]] | [[{{date+1:YYYYMMDD}}]]
  ```
- **Project Note** (`Templates/project-note.md`):
  ```markdown
  ---
  id: {{date:YYYYMMDD}}-{{title}}
  tags: [project/active]
  created: {{date:YYYY-MM-DD}}
  ---
  
  # {{title}}
  
  ## Goal
  
  ## Tasks
  - [ ] 
  
  ## Resources
  - 
  
  ## Links
  ```

### 7. Keep Hub Pages
- **index.md**: Keep as a hub page in the root. Populate with links to all major notes (projects, resources, entities).
- **REPORT.md**: Keep as a dynamic report in the root.

### 8. Run Cross-Linker
- Update backlinks to match new structure

### 9. Set Up Git Backup (Local Only)
```bash
git init
git add .
git commit -m "Initial commit after restructuring"
```
**Note:** Never push to a remote without explicit user confirmation. Use local Git for version control only.

## Key Decisions
- **Hybrid PARA + Zettelkasten**: Balances structure (PARA) and flexibility (Zettelkasten)
- **Flat Folder Hierarchy**: Max 2 subfolders deep (e.g., `3-Resources/`)
- **Atomic Notes**: Unique IDs (e.g., `20260615-freelance-ai-tools.md`)
- **Tags > Folders**: Prefer tags (e.g., `#project/active`) over deep nesting
- **Git Backup (Local Only)**: Version control for the vault — no remote pushes without explicit consent

## Common Pitfalls

### Ghost Nodes in Graph View
When you change a wikilink target (e.g., `[[2026-06-13]]` → `[[20260613-daily]]`), **always rename the file too**. Obsidian creates a ghost node for any wikilink that doesn't resolve to an existing file. The graph shows both nodes: the real file (with edges) and the ghost (isolated).

**Fix:** `mv "Daily/2026-06-13.md" "Daily/20260613-daily.md"`, then update the frontmatter `id` field.

### Template `:null` in Frontmatter
When applying a template with `{{date:YYYYMMDD}}` in the `id` property, Obsidian's Template plugin may render it as `id: 20260613:null` because the property renderer doesn't always resolve the template variable correctly.

**Fix:** The template itself is fine; this is a rendering artifact. The property value is stored correctly in the .md file. If it bothers the user, use a static default or a Templater hotkey (Alt+T) instead of the core Templates plugin.