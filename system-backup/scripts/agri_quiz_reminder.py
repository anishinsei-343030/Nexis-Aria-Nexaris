#!/usr/bin/env python3
"""9PM reminder watchdog for the Agri Quiz.

Reads D:/Hermes/Nexis Aria Nexaris/projects/AgriQuizBot/last_post.json written by agri_quiz_bot.py.
If a quiz was posted today, prints the reminder (delivered verbatim to the
group by the no_agent cron job). Otherwise prints nothing (silent job).
"""

import json
import os
import sys
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

POST_FILE = r"D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\last_post.json"

today = date.today().isoformat()
try:
    with open(POST_FILE, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
except (OSError, ValueError):
    data = {}

if data.get("date") == today:
    link = data.get("link", "")
    title = data.get("title", "Agriculture Board Exam Quiz")
    print(f"⏰ Reminder: {title} closes tonight at 9PM!\n"
          f"🔗 {link}\n"
          f"Submit before the deadline to get your score.")