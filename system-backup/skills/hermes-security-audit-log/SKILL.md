---\nname: hermes-security-audit-log\ndescription: name: hermes-security-audit-log\nversion: 1.0.0\nplatforms: [linux, macos, windows]\n---
name: hermes-security-audit-log
title: Hermes Security Audit Log
category: security
lang: markdown

description: |
  Log of all skills that triggered Hermes security scanner during initial installation.
  Tracks verdicts, findings, and final installation status.
---

## Audit Log

### Blocked (DANGEROUS — forced skip)
- **ai-music-video** (38 findings: obfuscation, exfiltration, execution)
- **aima-doctor** (1 finding: supply chain)
- **multi-group-chat-manager** (11 findings: persistence, network, execution)
- **ai-skillhub** (7 findings: destructive, exfiltration, injection)
- **academic-paper-reviewer** (11 findings: injection, exfiltration)
- **ars-deep-research** (9 findings: injection, exfiltration, persistence)

### Installed (CAUTION — forced)
- **youtube-downloader-clipper** (5 findings: privilege escalation, supply chain)
- **create-video** (19 findings: privilege escalation, exfiltration, network, supply chain)
- **elevenlabs-tts** (1 finding: privilege escalation)
- **faceless-video** (2 findings: exfiltration)
- **academic-citation-manager** (8 findings: obfuscation, supply chain)
- **edge-tts-english** (0 findings: safe, manual confirm)

### Installed (SAFE)
- **one-three-one-rule** (builtin, safe)
- **scrapling** (builtin, safe)
- **apa7-reference-helper-mia956** (community, safe)
- **toby-deep-research** (community, safe)
- **academic-polish** (community, safe)
- **searchapi-scholar-search** (community, safe)
- **toby-academic-writing** (community, safe)
- **academic-writing-polisher** (community, safe)
- **deep-research-v60** (community, caution → forced)
- **ai-paper-survey** (community, caution → forced)
- **akashic-knowledge-base** (community, safe)

### Already Installed
- **ai-daily-briefing**
- **ai-skill-optimizer**
- **agent-browser-juan**
- **agent-daily-planner**
- **ai-video-editor-fixed**
- **arxiv**

### Summary
- **Total requested**: 30
- **Installed**: 23
- **Blocked (DANGEROUS)**: 6
- **Date**: Initial setup (June 13, 2026)
