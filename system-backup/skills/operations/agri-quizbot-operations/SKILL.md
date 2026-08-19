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

Manage the daily and weekly question bank pipeline for the AgriQuizBot (D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot). The bot writes 90 fresh questions into a Google Form daily.

## Pipeline Logic

- **Daily Run:** `agri_quiz_bot.py` selects 90 unused questions (15 per area; numbering restarts 1-15 per subject).
- **Top-Up Trigger:** If unused questions < 90, bot returns `BANK_LOW n` (Exit 2).
- **Emergency Target:** Top up to 180 unused questions (30 per area).
- **Cron jobs:** "Pre-Board Exam Daily (20:00)" and "Pre-Board Exam 9PM Reminder (21:45)" — relay scripts live in `C:\Users\Administrator\.hermes\profiles\nexis\scripts\` (`agri_quiz_daily.py`, `agri_quiz_reminder.py`), NOT in the project dir. Full job prompts live in `~/.hermes/profiles/nexis/cron/jobs.json` (read via python, not grep-able JSON pretty-print).

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
- **Script arguments get mangled too (2026-08-19):** a backslash path passed as an argument loses its escapes in bash (`D:\DevTools\tts\hermes_tts.py` arrives as `D:DevToolsttshermes_tts.py` and resolves against cwd), and MSYS-style `/d/DevTools/...` handed to a Windows-native exe can come out as `D:\d\DevTools\...`. **FIX that worked:** `cd /d/DevTools/tts && "<python.exe>" hermes_tts.py ...` — cd into the script's directory and pass the bare filename. Forward-slash `D:/...` paths are safe for `--output` / `MEDIA:` style arguments and for `ls`.

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
"/c/Users/Administrator/AppData/Local/Python/hermes313/Scripts/python.exe" -c "import json; b=json.load(open(r'D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\question_bank.json',encoding='utf-8-sig')); print('UNUSED', sum(1 for q in b['questions'] if q['status']=='unused'))"
```

## Voice Notes in Cron Jobs (Telegram)

Both daily and reminder cron runs generate a voice note with a fresh motivational quote (1 line, <25 words, always English, study/future/life themed) via:
```bash
"/c/Users/Administrator/AppData/Local/Python/hermes313/Scripts/python.exe" D:/DevTools/tts/hermes_tts.py --ref nexis --output D:/Hermes/Nexis Aria Nexaris/projects/AgriQuizBot/voice/{daily|reminder}_YYYYMMDD.wav --text "<spoken message>"
```
Then verify the file exists and add `MEDIA:D:/Hermes/Nexis Aria Nexaris/projects/AgriQuizBot/voice/{daily|reminder}_YYYYMMDD.wav` to the reply so it delivers to the group.

## Reminder cron reply format (2026-08-19, updated)

- Reminder chat: Pre-Board Exam supergroup, Telegram `-1004302584573`.
- The reminder script's output is injected as "Script Output" — if it contains the reminder text, post it in warm voice keeping title, link, and submit-before-9PM line, plus ONE fresh researched motivational line (<25 words, always English). If the script prints nothing, reply `[SILENT]` — do not post.
- Voice note: spoken text = short reminder (quiz closes 9PM, link in chat) + the same motivational line, spoken aloud. Generate as `.ogg` (see pitfall below), then the reply MUST carry two lines, in order: `[[audio_as_voice]]` on its own line, then `MEDIA:D:/Hermes/Nexis Aria Nexaris/projects/AgriQuizBot/voice/reminder_YYYYMMDD.ogg`. End the reply with the exact text message that was posted.

**PITFALL (2026-08-18):** WAV files delivered via `MEDIA:` land in Telegram as downloadable attachments — they do NOT play inline. Telegram voice bubbles require OGG (Opus). Fix: convert WAV → OGG via FFmpeg (available on host) and use `.ogg` in both the `--output` path and the `MEDIA:` line. See `tts-voice-troubleshooting` section 9 for the implementation sketch. STATUS: the `hermes_tts.py` edit is BLOCKED by the write guardrail (out-of-workspace path; chat approval doesn't reach the gate) — Shin applies it manually, cron prompts stay `.wav` until then. Until the fix lands, keep verifying the `.wav` exists before the `MEDIA:` line.

**STATUS UPDATE (2026-08-19):** the `.ogg` conversion is now BUILT INTO `hermes_tts.py` — pass `--output <path>.ogg` and the script saves WAV then converts to OGG automatically, printing `OK <path>.ogg`. Cron jobs must now request `.ogg` directly (never `.wav`), and the `MEDIA:` line must point at the `.ogg`. Verified live: reminder cron generated `reminder_20260819.ogg` (39.7 KB, ~38.4s audio) and delivered as a voice bubble. Also verified 2026-08-18: without the `[[audio_as_voice]]` directive the `.ogg` still arrives as a downloadable attachment, so the directive stays mandatory.
