#!/usr/bin/env python3
"""Daily Agri Quiz worker: loads unused questions from the bank and writes
them into the live Google Form via the Forms API, then marks them used.

No LLM calls, no external API keys — only the service account key.

Exit codes:
    0   success (prints QUIZ_OK + the message to post)
    2   BANK_LOW n   (fewer than 120 unused; agent must top up)
    3   KEY_MISSING  (service account key not found)
    4   API_ERROR    (Forms API failure; details on stderr)

Config (all optional via args):
    --form-id   default: live form 1J_15Uz63ZzynNbPHpi3_PEzvhYMSy6witBlDnK9V2nA
    --key       default: D:\\Zero\\secrets\\nexis-quiz-bot.json
    --bank      default: question_bank.json next to this script
    --count     default 120, --per-area default 20
    --dry-run   simulate selection and print what would be written (no API)
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import date

SCOPES = [
    "https://www.googleapis.com/auth/forms",
    "https://www.googleapis.com/auth/drive",
]

DEFAULT_FORM_ID = "1J_15Uz63ZzynNbPHpi3_PEzvhYMSy6witBlDnK9V2nA"
DEFAULT_KEY = r"D:\Zero\secrets\nexis-quiz-bot.json"
DEFAULT_BANK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "question_bank.json")
POST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_post.json")

DESCRIPTION = ("🌾 120 questions across 6 LEA subject areas\n"
               "🔬 Auto-graded — submit to see your score\n"
               "⏰ Submit before 9PM!")


def load_bank(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        bank = json.load(f)
    return bank


def save_bank(bank, path):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def pick_questions(bank, count, per_area):
    questions = bank.get("questions", [])
    unused = [q for q in questions if q.get("status") == "unused"]
    if len(unused) < count:
        return None, len(unused)
    by_area = defaultdict(list)
    for q in unused:
        by_area[q.get("area", "?")].append(q)
    for lst in by_area.values():
        lst.sort(key=lambda q: (q.get("created_date", ""), q.get("id", "")))
    picked = []
    for area in bank["meta"]["areas"]:
        picked.extend(by_area.get(area, [])[:per_area])
    picked_ids = {q["id"] for q in picked}
    leftover = [q for q in unused if q["id"] not in picked_ids]
    leftover.sort(key=lambda q: (q.get("created_date", ""), q.get("id", "")))
    picked.extend(leftover[: max(0, count - len(picked))])
    return picked[:count], len(unused)


AREA_EMOJIS = {
    "Crop Science": "🌾",
    "Soil Science": "🌱",
    "Animal Science": "🐄",
    "Crop Protection": "🐛",
    "Agricultural Extension and Communication": "📢",
    "Agricultural Economics and Marketing": "💰",
}


def build_requests(form, picked, title, desc, bank_meta_areas):
    """Return a flat list of batchUpdate request dicts, in execution order.

    Order: delete all existing items, update info/settings, then one section
    header + questions per area, numbered continuously 1..N. Caller chunks
    this list into batches.
    """
    requests = []
    existing = form.get("items", [])
    if existing:
        for _ in range(len(existing)):
            requests.append({"deleteItem": {"location": {"index": 0}}})

    settings = form.get("settings", {}) or {}
    settings["quizSettings"] = {"isQuiz": True}
    requests.append({"updateFormInfo": {"info": {"title": title, "description": desc},
                                        "updateMask": "title,description"}})
    requests.append({"updateSettings": {"settings": settings, "updateMask": "quizSettings"}})

    picked_by_area = defaultdict(list)
    for q in picked:
        picked_by_area[q["area"]].append(q)

    form_index = 0
    n = 0
    for area in bank_meta_areas:
        area_qs = picked_by_area.get(area)
        if not area_qs:
            continue
        emoji = AREA_EMOJIS.get(area, "🌾")
        requests.append({"createItem": {
            "item": {"title": f"{emoji} {area}", "pageBreakItem": {}},
            "location": {"index": form_index},
        }})
        form_index += 1
        for q in area_qs:
            n += 1
            item = {
                "title": f"{n}. {q['question']}",
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [{"value": o} for o in q["options"]],
                            "shuffle": True,
                        },
                        "grading": {
                            "pointValue": 1,
                            "correctAnswers": {"answers": [{"value": q["answer"]}]},
                        },
                    }
                },
            }
            if q.get("explanation"):
                grading = item["questionItem"]["question"]["grading"]
                grading["whenRight"] = {"text": "Correct!"}
                grading["whenWrong"] = {"text": q["explanation"]}
            requests.append({"createItem": {"item": item, "location": {"index": form_index}}})
            form_index += 1
    return requests


def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Write daily Agri Quiz to Google Form")
    ap.add_argument("--form-id", default=DEFAULT_FORM_ID)
    ap.add_argument("--key", default=DEFAULT_KEY)
    ap.add_argument("--bank", default=DEFAULT_BANK)
    ap.add_argument("--count", type=int, default=120)
    ap.add_argument("--per-area", type=int, default=20)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.bank):
        sys.stderr.write(f"ERROR: bank not found: {args.bank}\n")
        sys.exit(4)

    bank = load_bank(args.bank)
    picked, unused = pick_questions(bank, args.count, args.per_area)
    if picked is None:
        print(f"BANK_LOW {unused}")
        sys.exit(2)

    today = date.today()
    title = f"Agriculture Board Exam Quiz — {today.strftime('%B %d, %Y')}"
    responder_uri = None

    if not args.dry_run:
        if not os.path.isfile(args.key):
            sys.stderr.write(f"ERROR: service account key not found: {args.key}\n")
            print("KEY_MISSING")
            sys.exit(3)
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            creds = service_account.Credentials.from_service_account_file(args.key, scopes=SCOPES)
            svc = build("forms", "v1", credentials=creds, cache_discovery=False)
            form = svc.forms().get(formId=args.form_id).execute()
            requests = build_requests(form, picked, title, DESCRIPTION, bank["meta"]["areas"])
            for group in chunk(requests, 60):
                svc.forms().batchUpdate(formId=args.form_id,
                                        body={"requests": group}).execute()
            form = svc.forms().get(formId=args.form_id).execute()
            responder_uri = form.get("responderUri")
        except Exception as e:  # noqa: BLE001 — report and exit for the agent
            sys.stderr.write(f"API_ERROR: {e}\n")
            print("API_ERROR")
            sys.exit(4)

        used_ids = {q["id"] for q in picked}
        for q in bank["questions"]:
            if q["id"] in used_ids:
                q["status"] = "used"
                q["used_date"] = today.isoformat()
        save_bank(bank, args.bank)
        with open(POST_FILE, "w", encoding="utf-8") as f:
            json.dump({"date": today.isoformat(), "title": title,
                       "link": responder_uri, "questions": len(picked)}, f,
                      ensure_ascii=False, indent=2)
    else:
        responder_uri = "https://docs.google.com/forms/d/e/DRY_RUN/viewform"
        by_area = defaultdict(int)
        for q in picked:
            by_area[q["area"]] += 1
        sys.stderr.write("DRY-RUN: no API calls made. Selection:\n")
        for a, c in sorted(by_area.items()):
            sys.stderr.write(f"  {a}: {c}\n")

    link = responder_uri or DEFAULT_FORM_ID
    msg = (f"🌾 {title}\n"
           f"📝 {len(picked)} fresh questions • 6 LEA areas • auto-graded\n"
           f"🔗 {link}\n"
           f"⏰ Submit before 9PM tonight!")
    print("QUIZ_OK")
    print(msg)


if __name__ == "__main__":
    main()