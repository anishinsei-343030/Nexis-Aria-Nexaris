# AgriQuizBot

Daily Agriculture Board Exam Quiz for the Nexis Family — writes 90 fresh
questions into the live Google Form each morning, auto-graded, posted to the
Pre-Board Exam supergroup on Telegram.

## State (2026-08-17)

- Question bank: 1078 questions, 0 placeholders, ~504 unused (6 LEA areas).
- Live form: rebuilt 2026-08-17 with 90 real questions (6 sections × 15,
  numbered 1–15 per subject), title "Pre-Board Exam — {date}".
- Delivery target: `telegram:-1004302584573` (Pre-Board Exam).
- Service account key: `D:\Zero\secrets\nexis-quiz-bot.json` (not in this folder).

## Pipeline

- **Weekly refill (Sunday 18:00, agent job):** Nexis researches ~960 new
  questions (160 per LEA area), writes a batch JSON, runs `bank_add.py`.
- **Daily quiz (20:00, script + Nexis posts):** `agri_quiz_daily.py` runs
  `agri_quiz_bot.py`; Nexis relays the resulting message to the group.
- **9PM reminder (20:45, no_agent):** `agri_quiz_reminder.py` prints a nudge
  only if today's quiz was posted.

## Commands

```powershell
# Add questions from a batch file (JSON list; see bank_add.py header for schema)
python D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\bank_add.py D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\batch\weekly_YYYYMMDD.json

# Run the daily worker (needs D:\Zero\secrets\nexis-quiz-bot.json)
python D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\agri_quiz_bot.py

# Dry-run selection (no API calls)
python D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\agri_quiz_bot.py --dry-run
```

Use the hermes313 python: `C:\Users\Administrator\AppData\Local\Python\hermes313\Scripts\python.exe`

## Rules

- Question bank: `question_bank.json` (live data; never hand-edit).
- Questions are used once and retired — `status: "unused" | "used"`.
- 90 questions per day, 15 per area; if unused < 90 the bot prints
  `BANK_LOW n` and the agent must top up before it runs again.
- Batch files: one per session, saved under `batch\`, deleted after a
  successful `bank_add.py` run.
- Areas: Crop Science, Soil Science, Animal Science, Crop Protection,
  Agricultural Extension and Communication, Agricultural Economics and Marketing.
- No LLM calls, no API keys in the bot — only the service account key.
- `bank_add.py` rejects template/placeholder questions (quality gate).

## Exit codes (agri_quiz_bot.py)

- `0` + `QUIZ_OK` — success; the printed message goes to the group.
- `2` + `BANK_LOW n` — insufficient unused questions; top up first.
- `3` + `KEY_MISSING` — SA key not at `D:\Zero\secrets\nexis-quiz-bot.json`.
- `4` + `API_ERROR` — Forms API failure (details on stderr).