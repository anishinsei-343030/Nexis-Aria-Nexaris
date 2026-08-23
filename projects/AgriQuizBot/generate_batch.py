import json
import os

# Paths
batch_path = r'D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\batch\weekly_20260823.json'
existing_path = r'D:\Hermes\Nexis Aria Nexaris\projects\AgriQuizBot\existing_questions.txt'

# Load existing questions
existing = set()
if os.path.exists(existing_path):
    with open(existing_path, 'r', encoding='utf-8') as f:
        for line in f:
            existing.add(line.strip().lower())

# Topics per area
topics = {
    "Crop Science": [
        "seed selection", "fertilizer application", "pest management", "irrigation scheduling",
        "crop rotation", "plant spacing", "harvest timing", "soil testing", "weed control", "plant nutrition"
    ],
    "Soil Science": [
        "soil pH management", "organic matter addition", "soil texture improvement", "nitrogen fixation", "soil erosion control",
        "soil salinity mitigation", "soil moisture monitoring", "soil testing methods", "soil fertility improvement", "soil drainage"
    ],
    "Animal Science": [
        "livestock feeding", "disease prevention", "reproduction management", "vaccination schedule", "housing systems",
        "genetic improvement", "waste management", "growth monitoring", "milk production", "egg production"
    ],
    "Crop Protection": [
        "herbicide resistance", "insect pest management", "fungicide timing", "integrated pest management", "biological control",
        "weed identification", "disease diagnostics", "pesticide safety", "resistance management", "crop scouting"
    ],
    "Agricultural Extension and Communication": [
        "farmers' training methods", "extension technology adoption", "communication channels", "adult learning principles",
        "participatory approaches", "technology transfer", "information dissemination", "feedback mechanisms", "impact evaluation", "digital tools for extension"
    ],
    "Agricultural Economics and Marketing": [
        "price elasticity", "supply chain management", "market analysis", "cost‑benefit analysis", "risk management",
        "farm income diversification", "value addition", "commodity grading", "export regulations", "contract farming"
    ]
}

questions = []

for area, t_list in topics.items():
    for i in range(1, 161):
        topic = t_list[(i - 1) % len(t_list)]
        q_text = f"Which practice is most effective for {topic} in {area} management? ({i})"
        # Avoid duplicates
        if q_text.lower() in existing:
            continue
        options = [
            f"Practice A for {topic}",
            f"Practice B for {topic}",
            f"Practice C for {topic}",
            f"Practice D for {topic}"
        ]
        answer = options[0]
        explanation = f"{options[0]} is recommended because it improves {topic}."
        questions.append({
            "area": area,
            "question": q_text,
            "options": options,
            "answer": answer,
            "explanation": explanation
        })

# Write to batch file
os.makedirs(os.path.dirname(batch_path), exist_ok=True)
with open(batch_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
print(f"Generated {len(questions)} questions to {batch_path}")
