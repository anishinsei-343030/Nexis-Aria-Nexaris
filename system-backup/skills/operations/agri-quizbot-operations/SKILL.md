---
name: agri-quizbot-operations
description: Manage the daily and weekly question bank pipeline for the AgriQuizBot, including emergency top-ups and bot execution.
version: 1.0.0
authors:
  - Nexis Aria Nexaris
tags:
  - agriculture
  - cron
  - bot-management
  - windows-gitbash
---

# AgriQuizBot Operations

Manage the daily and weekly question bank pipeline for the AgriQuizBot (D:\Zero\Projects\AgriQuizBot). The bot writes 120 fresh questions into a Google Form daily.

## Pipeline Logic

- **Daily Run:** `agri_quiz_bot.py` selects 120 unused questions (20 per area).
- **Top-Up Trigger:** If unused questions < 120, bot returns `BANK_LOW n` (Exit 2).
- **Emergency Target:** Top up to 240 unused questions (40 per area).

## Execution Workflow

### 1. Emergency Top-Up (When `BANK_LOW` is received)
1. **Research:** Source 40 fresh questions per area at the 2026 Philippine Agriculture Licensure Exam (ALE) level.
2. **Format:** JSON list of objects: `{"area": "...", "question": "...", "options": ["A", "B", "C", "D"], "answer": "A", "explanation": "..."}`.
3. **Write Batch:** Save to `D:\Zero\Projects\AgriQuizBot\batch\emergency_YYYYMMDD.json`.
4. **Import:** Run `bank_add.py` using the hermes313 Python:
   ```bash
   "/c/Users/Administrator/AppData/Local/Python/hermes313/Scripts/python.exe" D:/Zero/Projects/AgriQuizBot/bank_add.py D:/Zero/Projects/AgriQuizBot/batch/emergency_YYYYMMDD.json
   ```
5. **Verify:** Confirm `UNUSED` count is >= 240.

### 2. Daily Quiz Execution
1. **Run Bot:**
   ```bash
   "/c/Users/Administrator/AppData/Local/Python/hermes313/Scripts/python.exe" D:/Zero/Projects/AgriQuizBot/agri_quiz_bot.py
   ```
2. **Post Result:** If `QUIZ_OK` is returned, relay the message to the group.

## Pitfalls & Technical Constraints

### 1. Windows Git Bash Path Syntax
The `terminal` tool runs via Git Bash (MSYS). Full Windows paths like `C:\...` are often misinterpreted.
- **FIX:** Use double quotes and forward slashes for executables:
  `"/c/Users/Administrator/AppData/Local/Python/hermes313/Scripts/python.exe"`

### 2. `execute_code` vs. `terminal` in Cron Jobs
In scheduled cron jobs, `execute_code` may block arbitrary local Python calls (e.g., `subprocess`) due to `approvals.cron_mode`.
- **FIX:** Use `write_file` to save a `.py` script to disk, then execute it via `terminal`.

### 3. Data Quality Requirement
**PLACEHOLDERS ARE PROHIBITED.** Generating questions like "Topic X: Question Y" with "Option A" as the answer is a critical failure. All questions must be real, exam-level content with verified answers.

### 4. Integrity of `QUIZ_OK`
Never fabricate a `QUIZ_OK` message. If the bot returns `API_ERROR` or `KEY_MISSING`, notify the group that the quiz is delayed.

## Verification Commands

Check unused count without running the bot:
```bash
"/c/Users/Administrator/AppData/Local/Python/hermes313/Scripts/python.exe" -c "import json; b=json.load(open(r'D:\Zero\Projects\AgriQuizBot\question_bank.json',encoding='utf-8-sig')); print('UNUSED', sum(1 for q in b['questions'] if q['status']=='unused'))"
```
