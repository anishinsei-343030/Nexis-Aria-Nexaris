#!/usr/bin/env python3
"""Add questions to the Agri Quiz bank from a batch JSON file.

Usage:
    python bank_add.py <batch_file.json> [--bank question_bank.json] [--allow-dup]

Batch file format:
    [
      {"area": "Crop Science", "question": "...", "options": ["A","B","C","D"],
       "answer": "A", "explanation": "optional"},
      ...
    ]
    or {"questions": [ ... ], "area": "default area for entries missing one"}

Validation rules:
    - area must be one of the bank's areas
    - question must be a non-empty string
    - options must be 2-8 unique non-empty strings
    - answer must exactly match one option
    - question text must not already exist (unless --allow-dup)
    - placeholder/template content is rejected (answers like "Option A",
      "Explanation for X question N" feedback, "Exam Topic" titles, short
      or templated explanations) — real questions only

Each added question gets: id (Q + zero-padded), status "unused",
created_date (today), used_date null. Writes back atomically.
"""

import argparse
import json
import os
import re
import sys
from datetime import date

BANK_DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "question_bank.json")


def load_bank(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        bank = json.load(f)
    bank.setdefault("meta", {})
    bank["meta"].setdefault("areas", [])
    bank.setdefault("questions", [])
    return bank


def save_bank(bank, path):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def clean_text(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


PLACEHOLDER_PATTERNS = [
    re.compile(r"exam topic", re.I),
    re.compile(r"key concept of", re.I),
    re.compile(r"placeholder|todo|fixme|dummy|lorem", re.I),
    re.compile(r"^option [a-d]$", re.I),
    re.compile(r"^explanation for", re.I),
    re.compile(r"question \d+", re.I),
]


def is_placeholder(question, answer, explanation):
    for pat in PLACEHOLDER_PATTERNS:
        if pat.search(question) or pat.search(answer) or pat.search(explanation or ""):
            return True
    if answer.strip().lower().startswith("option"):
        return True
    if explanation and len(clean_text(explanation)) < 15:
        return True
    return False


def validate_entry(entry, areas, existing_texts, allow_dup, idx, default_area):
    errors = []
    area = clean_text(entry.get("area") or default_area)
    if area not in areas:
        errors.append(f"entry {idx}: unknown area {area!r} (allowed: {areas})")
    question = clean_text(entry.get("question"))
    if not question:
        errors.append(f"entry {idx}: empty question")
    if question and question.lower() in existing_texts and not allow_dup:
        errors.append(f"entry {idx}: duplicate question: {question[:60]}")
    options = [clean_text(o) for o in entry.get("options", [])]
    options = [o for o in options if o]
    if len(options) < 2 or len(options) > 8:
        errors.append(f"entry {idx}: options must be 2-8 non-empty values (got {len(options)})")
    if len(set(options)) != len(options):
        errors.append(f"entry {idx}: duplicate options")
    answer = clean_text(entry.get("answer"))
    if answer not in options:
        errors.append(f"entry {idx}: answer {answer!r} not among options")
    explanation = clean_text(entry.get("explanation"))
    if question and answer in options and is_placeholder(question, answer, explanation):
        errors.append(
            f"entry {idx}: placeholder/template question rejected: {question[:70]}"
        )
    return {
        "area": area,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "errors": errors,
    }


def main():
    ap = argparse.ArgumentParser(description="Add questions to the Agri Quiz bank")
    ap.add_argument("batch_file", help="JSON file with questions to add")
    ap.add_argument("--bank", default=BANK_DEFAULT, help="path to question_bank.json")
    ap.add_argument("--allow-dup", action="store_true", help="allow duplicate questions")
    args = ap.parse_args()

    if not os.path.isfile(args.bank):
        sys.exit(f"ERROR: bank not found: {args.bank}")
    if not os.path.isfile(args.batch_file):
        sys.exit(f"ERROR: batch file not found: {args.batch_file}")

    bank = load_bank(args.bank)
    areas = bank["meta"]["areas"]
    existing = [clean_text(q["question"]).lower() for q in bank["questions"]]
    existing_set = set(existing)

    with open(args.batch_file, "r", encoding="utf-8-sig") as f:
        raw = json.load(f)
    if isinstance(raw, dict):
        default_area = clean_text(raw.get("area"))
        entries = raw.get("questions", [])
    else:
        default_area = None
        entries = raw
    if not isinstance(entries, list):
        sys.exit("ERROR: batch file must be a list of questions or an object with a 'questions' list")

    next_num = len(bank["questions"]) + 1
    today = date.today().isoformat()
    added = 0
    rejected = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            rejected.append(f"entry {i}: not an object")
            continue
        v = validate_entry(entry, areas, existing_set, args.allow_dup, i, default_area)
        if v["errors"]:
            rejected.append("; ".join(v["errors"]))
            continue
        bank["questions"].append({
            "id": f"Q{next_num:05d}",
            "area": v["area"],
            "question": v["question"],
            "options": v["options"],
            "answer": v["answer"],
            "explanation": v["explanation"],
            "status": "unused",
            "created_date": today,
            "used_date": None,
        })
        existing_set.add(v["question"].lower())
        next_num += 1
        added += 1

    save_bank(bank, args.bank)
    by_area = {}
    for q in bank["questions"][-added:]:
        by_area[q["area"]] = by_area.get(q["area"], 0) + 1

    print(f"ADDED {added} questions")
    for a, c in sorted(by_area.items()):
        print(f"  {a}: {c}")
    unused = sum(1 for q in bank["questions"] if q["status"] == "unused")
    print(f"BANK_TOTAL {len(bank['questions'])}  UNUSED {unused}")
    if rejected:
        print(f"REJECTED {len(rejected)}")
        for r in rejected:
            print(f"  - {r}")


if __name__ == "__main__":
    main()