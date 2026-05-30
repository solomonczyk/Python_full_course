"""
Generate unique, short, inspiring game_relevance from each lesson's analogy.
Each text is built from: unique analogy snippet + varied game connection.
All 87 will be unique because story_metaphors are unique + 10 varied endings.
Run: python scripts/generate_game_relevance.py
"""

import json, sys, io, shutil, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PATH = "api/app/data/lessons.json"

with open(PATH, encoding="utf-8") as f:
    lessons = json.load(f)

ENDINGS = [
    "В финальной игре это превратится в настоящий код — и ты увидишь, как теория оживает.",
    "Ты собираешь свою игру кирпичик за кирпичиком. Этот урок — ещё один кирпич в стене твоего приключения.",
    "Скоро ты напишешь свою первую игру. Каждый такой навык — шаг от «я не умею» к «я сделал это сам».",
    "В «Побеге из Башни Багуса» этот приём станет твоим секретным оружием. Продолжай в том же духе!",
    "Именно из таких маленьких кирпичиков и строятся большие игры. Ты на верном пути, герой.",
    "Когда будешь писать финальную игру, ты вспомнишь этот урок и скажешь: «Вот зачем я это учил!»",
    "Неважно, сколько ты уже знаешь — каждый новый приём делает твою игру на капельку круче.",
    "Программирование — это магия, где каждое новое заклинание открывает новые возможности. Ты учишь магию Python.",
    "Ты не просто учишь Python — ты учишься превращать идеи в работающие программы. Это суперсила.",
    "Финальная игра будет состоять из таких вот маленьких решений. С каждым уроком ты собираешь пазл.",
]

count = 0
for lesson in lessons:
    lid = lesson["id"]
    title = lesson.get("title", "")
    analogy = lesson.get("analogy", {})
    story = analogy.get("story_metaphor", "")
    analogy_title = analogy.get("title", "")

    if not story:
        ending = ENDINGS[int(hashlib.md5((lid + "alt").encode()).hexdigest(), 16) % len(ENDINGS)]
        text = f"Тема «{title}» — ещё один инструмент в твоём арсенале. {ending}"
        lesson["game_relevance"] = text
        lesson["connection_to_game"] = text
        count += 1
        continue

    # Extract first meaningful sentence from story_metaphor (up to 100 chars)
    sentences = story.replace("! ", "!||").replace("? ", "?||").replace(". ", ".||").split("||")
    core = ""
    for s in sentences:
        trimmed = s.strip()
        if not trimmed:
            continue
        if len(core) + len(trimmed) < 100:
            core += trimmed + " "
        else:
            break
    core = core.strip()
    if core.endswith(",") or core.endswith(":"):
        core = core[:-1] + "."
    if not core.endswith(".") and not core.endswith("!") and not core.endswith("?"):
        core += "."

    # Pick varied ending
    ending = ENDINGS[int(hashlib.md5(lid.encode()).hexdigest(), 16) % len(ENDINGS)]
    text = f"{core} {ending}"

    lesson["game_relevance"] = text
    count += 1

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

shutil.copy2(PATH, "backend/app/data/lessons.json")

print(f"Updated {count} lessons with unique game_relevance texts")
print()
for l in lessons[:5]:
    print(f"  {l['id']} ({l['title']}):")
    print(f"    {l['game_relevance']}")
    print()
