---\nname: obsidian-automation\ndescription: name: Obsidian Automation\nversion: 1.0.0\nplatforms: [linux, macos, windows]\n---
name: Obsidian Automation
description: Automate Obsidian knowledge management, note linking, and personal knowledge base workflows
version: 1.0.0
author: Claude Office Skills
category: productivity
tags:
  - obsidian
  - notes
  - knowledge-management
  - markdown
  - pkm
department: content
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: notes-mcp
  tools:
    - obsidian_create_note
    - obsidian_search
    - obsidian_link
    - obsidian_template
capabilities:
  - Note creation
  - Knowledge linking
  - Template application
  - Graph exploration
input:
  - Note content
  - Search queries
  - Template configurations
  - Link patterns
output:
  - Created notes
  - Linked knowledge
  - Search results
  - Graph insights
languages:
  - en
related_skills:
  - notion-automation
  - deep-research
  - meeting-notes
---

# Obsidian Automation

Automate Obsidian knowledge management and personal knowledge base workflows.

## Core Capabilities

### Note Creation
```yaml
note_templates:
  daily_note:
    filename: "{{date:YYYY-MM-DD}}"
    folder: "Daily Notes"
    template: |
      # {{date:dddd, MMMM D, YYYY}}
      
      ## Morning Intentions
      - [ ] 
      
      ## Tasks
      - [ ] 
      
      ## Notes
      
      ## Evening Reflection
      
      ---
      [[{{date:YYYY-MM-DD|-1d}}|← Yesterday]] | [[{{date:YYYY-MM-DD|+1d}}|Tomorrow →]]

  meeting_note:
    filename: "Meeting - {{title}} - {{date}}"
    folder: "Meetings"
    template: |
      ---
      date: {{date}}
      attendees: {{attendees}}
      tags: meeting
      ---
      
      # {{title}}
      
      ## Agenda
      
      ## Notes
      
      ## Action Items
      - [ ] 
      
      ## Follow-ups
      
      [[Meetings MOC]]
```

### Smart Linking
```yaml
auto_linking:
  rules:
    - pattern: "[[Person/{{name}}]]"
      trigger: "@{{name}}"
      create_if_missing: true
      
    - pattern: "[[Project/{{project}}]]"
      trigger: "#proj/{{project}}"
      
  backlink_suggestions:
    enabled: true
    min_mentions: 2
    
  alias_support:
    - "[[Machine Learning|ML]]"
    - "[[Artificial Intelligence|AI]]"
```

### Dataview Queries
```yaml
dataview_examples:
  tasks_due_today:
    query: |
      ```dataview
      TASK
      WHERE !completed AND due = date(today)
      SORT due ASC
      ```
      
  recent_meetings:
    query: |
      ```dataview
      TABLE date, attendees
      FROM "Meetings"
      WHERE date >= date(today) - dur(7 days)
      SORT date DESC
      LIMIT 10
      ```
      
  project_dashboard:
    query: |
      ```dataview
      TABLE status, due, priority
      FROM #project
      WHERE status != "completed"
      SORT priority ASC
      ```
```

### Templates
```yaml
templates:
  zettelkasten:
    filename: "{{date:YYYYMMDDHHmmss}}"
    content: |
      ---
      id: {{date:YYYYMMDDHHmmss}}
      tags: 
      links: 
      ---
      
      # {{title}}
      
      ## Idea
      
      ## Source
      
      ## Connections
      - Related to: 
      
      ## References
      
  book_note:
    filename: "Book - {{title}}"
    content: |
      ---
      author: {{author}}
      finished: 
      rating: 
      tags: book
      ---
      
      # {{title}}
      by {{author}}
      
      ## Summary
      
      ## Key Ideas
      
      ## Highlights
      
      ## My Thoughts
      
      ## Action Items
```

## Workflow Automations

### Obsidian Vault Restructuring

Transform a wiki-style vault into a long-term note-taking system. See [Restructuring Guide](references/obsidian-restructuring-guide.md) for step-by-step instructions.

```yaml
restructuring_workflow:
  steps:
    - backup_vault
    - create_folders: ["0-Inbox", "1-Projects", "2-Areas", "3-Resources", "4-Archive", "Daily", "Templates"]
    - move_notes:
        concepts: "3-Resources"
        entities: "3-Resources"
        dailylogs: "Daily"
    - add_frontmatter: ["id", "tags", "created"]
    - replace_wikilinks
    - create_templates: ["daily-note", "project-note"]
    - remove_wiki_files: ["index.md", "log.md", "SCHEMA.md"]
    - run_cross_linker
    - setup_git_backup
```

## Graph Analysis

```yaml
graph_insights:
  orphan_notes:
    query: "notes without incoming links"
    action: suggest_connections
    
  clusters:
    identify: true
    visualize: true
    
  link_suggestions:
    based_on: content_similarity
    threshold: 0.7
```

## Best Practices

1. **Atomic Notes**: One idea per note (e.g., `20260615-freelance-ai-tools.md`)
2. **Flat Folder Structure**: Max 2 subfolders deep (e.g., `3-Resources/`, `Daily/`)
3. **Frontmatter**: Always include `id`, `tags`, and `created` for metadata
4. **Avoid Wikilinks**: Replace `[[shin]]` with plain text or `[[YYYYMMDD-title]]` for atomic notes
5. **Templates**: Use for daily notes, projects, and atomic notes (store in `Templates/`)
6. **PARA + Zettelkasten**: Hybrid approach for long-term scalability
   - **PARA**: `0-Inbox/`, `1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archive/`
   - **Zettelkasten**: Atomic notes with unique IDs (e.g., `20260615-title.md`)
7. **Git Backup (Local Only)**: Version control for the vault, strictly local unless explicitly instructed otherwise. Never push to a remote without user confirmation.
8. **Remove Wiki Overhead**: Delete `index.md`, `log.md`, `SCHEMA.md`
9. **Tags > Folders**: Prefer tags (e.g., `#project/active`) over deep nesting
10. **Cross-Linker**: Run after restructuring to update backlinks
