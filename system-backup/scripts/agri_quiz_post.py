#!/usr/bin/env python3
"""One-shot quiz post: prints the full quiz message from last_post.json
if a quiz was posted today (delivered verbatim by a no_agent cron job)."""

import json
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

if data.get("date") != today:
    sys.exit("NO_POST_TODAY")

title = data.get("title", "Agriculture Board Exam Quiz")
link = data.get("link", "")
questions = data.get("questions", 120)
print(f"{title}")
print(f"\U0001F4DD {questions} fresh questions \u2022 6 LEA areas \u2022 auto-graded")
print(f"\U0001F517 {link}")
print("\u23F0 Submit before 9PM tonight!")