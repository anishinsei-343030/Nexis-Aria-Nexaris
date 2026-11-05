
import json
import sys

bank_path = sys.argv[1]

with open(bank_path, 'r', encoding='utf-8') as f:
    bank = json.load(f)

existing_questions = set()
for q in bank['questions']:
    existing_questions.add(q['question'])

print(json.dumps(list(existing_questions)))
