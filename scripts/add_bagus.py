#!/usr/bin/env python3
"""Add Bagus to end of post_error_dialogue for all lessons except 3-41."""
import json, shutil
SRC = r"F:\Dev\Python_full_course\backend\app\data\lessons.json"
DST = r"F:\Dev\Python_full_course\api\app\data\lessons.json"

with open(SRC, "r", encoding="utf-8") as f:
    lessons = json.load(f)

bagus_texts = [
    "Ха-ха! Типичная ошибка новичка! А если бы это была настоящая игра? Она бы упала!",
    "Ой-ой! Багус нашёл багус! Python в замешательстве! Хорошо, что ты тренируешься!",
    "Хм! Багус одобряет эту ошибку! Теперь ты точно запомнишь правильный вариант!",
    "Ха-ха! Вот это я понимаю — настоящая ошибка! Даже у меня так бывает... ну, почти!",
    "Вот это поворот! Ошибка — это просто шаг к правильному коду. Не сдавайся!",
]

for i, lesson in enumerate(lessons):
    lid = lesson["id"]
    if lid == "3-41":
        continue
    if "post_error_dialogue" not in lesson:
        lesson["post_error_dialogue"] = []
    idx = i % len(bagus_texts)
    lesson["post_error_dialogue"].append({
        "character": "bagus",
        "text": bagus_texts[idx]
    })

with open(SRC, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)
shutil.copy2(SRC, DST)
print(f"Done. Added Bagus to {len(lessons)} lessons (sans 3-41).")
