import json
with open(r'D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\question_bank.json', 'r', encoding='utf-8-sig') as f:
    bank = json.load(f)
ids = [q['id'] for q in bank['questions']]
print(f"Total: {len(ids)}")
print(f"Last 5: {ids[-5:]}")
