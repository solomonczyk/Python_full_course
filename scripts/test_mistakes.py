import json

FILE = "backend/app/data/lessons.json"

with open(FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

lessons_to_update = {f"3-{i}" for i in range(27, 42)}

# Read mistakes from a separate JSON string
MISTAKES_JSON = r"""
{
  "3-27": [
    {"title": "Забыл квадратные скобки", "wrong": "items = \"меч\", \"щит\"
print(items)", "right": "items = [\"меч\", \"щит\"]
print(items)", "note": "Без [] Python создаёт кортеж (tuple), а не список."},
    {"title": "Индекс с 1, а не с 0", "wrong": "items = [\"меч\", \"щит\"]
print(items[1])", "right": "items = [\"меч\", \"щит\"]
print(items[0])", "note": "В Python индексация начинается с 0."}
  ]
}
"""

mistakes = json.loads(MISTAKES_JSON)

for lesson in data:
    lid = lesson.get("id", "")
    if lid in lessons_to_update and lid in mistakes:
        lesson["common_mistakes"] = mistakes[lid]
        print(f"Updated {lid}")

updated = [l["id"] for l in data if l.get("id", "") in lessons_to_update and "common_mistakes" in l]
print(f"Updated: {updated}")

with open(FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
