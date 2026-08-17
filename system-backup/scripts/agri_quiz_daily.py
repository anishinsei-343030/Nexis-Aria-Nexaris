#!/usr/bin/env python3
"""Daily Agri Quiz relay: runs the bot and passes its output to the agent.

Default cron --script mode: stdout is injected into the agent's prompt, so
Nexis sees the bot's output (QUIZ_OK + message, BANK_LOW n, or API_ERROR)
and decides what to post. Always exits 0; the bot's real exit code is
reported in the output as BOT_EXIT n.
"""

import subprocess
import sys

PYTHON = r"C:\Users\Administrator\AppData\Local\Python\hermes313\Scripts\python.exe"
BOT = r"D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\agri_quiz_bot.py"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

r = subprocess.run([PYTHON, BOT], capture_output=True, text=True, encoding="utf-8")
out = (r.stdout or "").strip()
err = (r.stderr or "").strip()
if out:
    print(out)
if err:
    print(err)
print(f"BOT_EXIT {r.returncode}")
sys.exit(0)