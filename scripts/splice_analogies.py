"""
Splice analogy entries into lessons.json and sync to backend copy.
Usage: python scripts/splice_analogies.py
"""

import json, sys, io, shutil, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LESSONS_PATH = "api/app/data/lessons.json"
BACKEND_PATH = "backend/app/data/lessons.json"

# Collect all analogy files
analogy_files = [
    f for f in os.listdir("scripts")
    if f.startswith("analogies_part") and f.endswith(".json")
]

if not analogy_files:
    print("No analogy files found (scripts/analogies_part*.json)")
    print("Run the agents first, then save their output to scripts/analogies_part*.json")
    sys.exit(1)

analogies = {}
for fname in sorted(analogy_files):
    with open(os.path.join("scripts", fname), encoding="utf-8") as f:
        data = json.load(f)
    analogies.update(data)
    print(f"  Loaded {len(data)} entries from {fname}")

print(f"\nTotal analogy entries: {len(analogies)}")

# Read lessons
with open(LESSONS_PATH, encoding="utf-8") as f:
    lessons = json.load(f)

missing = []
added = 0
for lesson in lessons:
    lid = lesson["id"]
    if lid in analogies:
        lesson["analogy"] = analogies[lid]
        added += 1
    else:
        missing.append(lid)

if missing:
    print(f"\nMissing analogies for: {missing}")

# Write
with open(LESSONS_PATH, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

# Sync to backend
shutil.copy2(LESSONS_PATH, BACKEND_PATH)

print(f"  Added {added} analogies to lessons.json")
print(f"  Synced to {BACKEND_PATH}")
print(f"  Total lessons: {len(lessons)}")
print(f"  Lessons with analogy: {sum(1 for l in lessons if 'analogy' in l)}")
