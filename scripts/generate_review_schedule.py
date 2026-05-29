"""
Generate review_schedule.json from lessons.json.

Reads api/app/data/lessons.json, applies a spaced review schedule,
and outputs api/app/data/review_schedule.json.

Schedule:
  - quick_recall   every 3 regular lessons
  - chapter_review at chapter boundaries
  - boss_review    before mini-project (end of part)
  - part_review    after each part (final review)
"""

import json
import random
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent
_LESSONS_PATH = _PROJECT / "api" / "app" / "data" / "lessons.json"
_OUTPUT_PATH = _PROJECT / "api" / "app" / "data" / "review_schedule.json"

random.seed(42)


# ── Dialogue templates per review type ─────────────────────────────────────

REVIEW_DIALOGUES: dict[str, list[dict[str, str]]] = {
    "quick_recall": [
        {"character": "ksyu", "text": "Давай быстро проверим, что ты запомнил из последних уроков. Это поможет закрепить материал."},
        {"character": "va", "text": "Не спеши, читай вопрос внимательно. Ошибки на повторении — это нормально."},
    ],
    "chapter_review": [
        {"character": "va", "text": "Глава пройдена. Перед тем как идти дальше, проверим, всё ли усвоено."},
        {"character": "ksyu", "text": "Повторение — ключ к уверенности. Даже если всё кажется простым, пара вопросов не помешает."},
    ],
    "boss_review": [
        {"character": "da", "text": "Скоро мини-игра! Но сначала проверим, готов ли ты. Это будет небольшая разминка перед финалом части."},
        {"character": "va", "text": "Вопросы будут по всей части. Не переживай, если что-то забыл — это часть процесса."},
    ],
    "part_review": [
        {"character": "da", "text": "Часть завершена! Ты прошёл большой путь. Давай закрепим всё, что ты узнал."},
        {"character": "ksyu", "text": "Финальное повторение части — это не экзамен, а способ увидеть, как далеко ты продвинулся."},
    ],
}

REVIEW_TITLES: dict[str, tuple[str, str]] = {
    "quick_recall": ("Быстрое повторение", "Проверь, что ты помнишь"),
    "chapter_review": ("Повторение главы", "Закрепление пройденного материала"),
    "boss_review": ("Проверка перед мини-игрой", "Готов ли ты к испытанию?"),
    "part_review": ("Финальное повторение части", "Поздравляем с завершением части!"),
}


def pick_random_quiz(lessons: list[dict], count: int = 2) -> list[dict]:
    """Pick random quiz questions from a list of lessons."""
    pool = [l for l in lessons if l.get("quiz") and l["quiz"].get("options")]
    return random.sample(pool, min(count, len(pool)))


def pick_what_outputs(lessons: list[dict]) -> dict | None:
    """Pick a random what_outputs from lessons."""
    pool = [l for l in lessons if l.get("what_outputs") and l["what_outputs"].get("code")]
    if not pool:
        return None
    return random.choice(pool)["what_outputs"]


def pick_find_bug(lessons: list[dict]) -> dict | None:
    """Pick a random find_bug from lessons."""
    pool = [l for l in lessons if l.get("find_bug") and l["find_bug"].get("code")]
    if not pool:
        return None
    chosen = random.choice(pool)["find_bug"]
    return chosen


def generate_task(lessons: list[dict], topic: str) -> dict:
    """Generate a mini coding task related to a topic."""
    tasks = {
        "print": {"title": "Вывод текста", "description": "Напиши программу, которая выводит приветствие.", "expected_output": "Привет, мир!"},
        "строк": {"title": "Работа со строками", "description": "Создай строку с именем и выведи её.", "expected_output": "Меня зовут Python"},
        "перемен": {"title": "Объявление переменных", "description": "Создай переменную и выведи её значение.", "expected_output": "42"},
        "input": {"title": "Ввод данных", "description": "Напиши программу, которая запрашивает имя и выводит приветствие.", "expected_output": "Привет, Алекс"},
        "арифмет": {"title": "Арифметика", "description": "Напиши программу, которая складывает два числа.", "expected_output": "15"},
        "if": {"title": "Условный оператор", "description": "Напиши проверку числа на положительность.", "expected_output": "Число положительное"},
        "for": {"title": "Цикл for", "description": "Выведи числа от 1 до 5 через пробел.", "expected_output": "1 2 3 4 5"},
        "while": {"title": "Цикл while", "description": "Выведи числа от 1 до 5, используя while.", "expected_output": "1 2 3 4 5"},
        "списк": {"title": "Списки", "description": "Создай список из трёх элементов и выведи его.", "expected_output": "[1, 2, 3]"},
    }
    for key, val in tasks.items():
        if key in topic.lower():
            return val
    return {"title": "Мини-задача", "description": "Напиши программу по теме пройденного урока.", "expected_output": "Готово!"}


def generate_review_entry(rid: str, rtype: str, part: int, chapter: int,
                           recent_lessons: list[dict],
                           older_lessons: list[dict] | None = None) -> dict:
    """Generate one review entry from recent + older lesson data."""
    all_sources = recent_lessons + (older_lessons or [])
    topics = [l["title"] for l in recent_lessons]
    position_after = recent_lessons[-1]["id"] if recent_lessons else "0-0"

    title, subtitle = REVIEW_TITLES[rtype]
    dialogue = REVIEW_DIALOGUES[rtype]
    quiz_lessons = pick_random_quiz(all_sources, 2)
    questions = [l["quiz"] for l in quiz_lessons if l.get("quiz")]
    what_outputs = pick_what_outputs(all_sources)
    find_bug = pick_find_bug(all_sources)
    main_topic = recent_lessons[-1]["topic"] if recent_lessons else ""
    task = generate_task(recent_lessons, main_topic)

    entry = {
        "id": rid,
        "type": rtype,
        "title": title,
        "subtitle": subtitle,
        "position_after": position_after,
        "part": part,
        "chapter": chapter,
        "topics": topics,
        "dialogue": dialogue,
        "questions": questions,
        "what_outputs": what_outputs,
        "find_bug": find_bug,
        "task": task,
    }
    return entry


def build_schedule(lessons: list[dict]) -> list[dict]:
    """Build the full review schedule from the lesson list."""
    reviews: list[dict] = []
    rid_counter = 0

    # Group lessons by part
    parts: dict[int, list[dict]] = {}
    for l in lessons:
        p = l["part"]
        parts.setdefault(p, []).append(l)

    for part_num in sorted(parts.keys()):
        part_lessons = parts[part_num]
        lesson_buffer: list[dict] = []
        current_chapter = part_lessons[0]["chapter"]

        for i, l in enumerate(part_lessons):
            lesson_buffer.append(l)
            chapter = l["chapter"]
            is_last_lesson = i == len(part_lessons) - 1

            # Chapter boundary: insert chapter_review and reset buffer
            if chapter != current_chapter:
                prev_lessons = lesson_buffer[:-1]
                if prev_lessons:
                    recent = prev_lessons[-3:] if len(prev_lessons) >= 3 else prev_lessons
                    rid_counter += 1
                    reviews.append(generate_review_entry(
                        f"r-{rid_counter}", "chapter_review",
                        part_num, current_chapter,
                        recent, None,
                    ))
                current_chapter = chapter
                # Reset buffer to start fresh for new chapter (keep only current lesson)
                lesson_buffer = [l]

            # Quick recall every 3 regular lessons (skip if last lesson — boss covers it)
            elif len(lesson_buffer) >= 3 and not is_last_lesson:
                older = [x for x in lesson_buffer[:-3]] or None
                rid_counter += 1
                reviews.append(generate_review_entry(
                    f"r-{rid_counter}", "quick_recall",
                    part_num, chapter,
                    lesson_buffer[-3:], older,
                ))
                lesson_buffer = []

        # Boss review before mini-project (end of Part 1, 2, 3 — not for Part 4 which is final project)
        if part_num < 4:
            rid_counter += 1
            recent = part_lessons[-3:] if len(part_lessons) >= 3 else part_lessons
            older = part_lessons[:-3] if len(part_lessons) > 3 else None
            reviews.append(generate_review_entry(
                f"r-{rid_counter}", "boss_review",
                part_num, current_chapter,
                recent, older,
            ))

        # Part review at end of part
        rid_counter += 1
        recent = part_lessons[-3:] if len(part_lessons) >= 3 else part_lessons
        older = part_lessons[:-3] if len(part_lessons) > 3 else None
        reviews.append(generate_review_entry(
            f"r-{rid_counter}", "part_review",
            part_num, current_chapter,
            recent, older,
        ))

    return reviews


def main():
    if not _LESSONS_PATH.exists():
        print(f"ERROR: lessons.json not found at {_LESSONS_PATH}")
        return 1

    with open(_LESSONS_PATH, encoding="utf-8") as f:
        lessons = json.load(f)

    print(f"Loaded {len(lessons)} lessons")
    reviews = build_schedule(lessons)
    print(f"Generated {len(reviews)} review blocks")

    # Type summary
    type_counts: dict[str, int] = {}
    for r in reviews:
        type_counts[r["type"]] = type_counts.get(r["type"], 0) + 1
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}")

    # Max gap calculation
    all_ids = set(l["id"] for l in lessons)
    review_positions = set(r["position_after"] for r in reviews)
    max_gap = 0
    current_gap = 0
    for l in lessons:
        current_gap += 1
        if l["id"] in review_positions:
            max_gap = max(max_gap, current_gap)
            current_gap = 0
    max_gap = max(max_gap, current_gap)  # tail
    print(f"  Max gap without review: {max_gap} lessons")

    output = {
        "total_reviews": len(reviews),
        "max_gap_without_review": max_gap,
        "type_counts": type_counts,
        "reviews": reviews,
    }

    _OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Written to {_OUTPUT_PATH}")

    return 0 if max_gap <= 3 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
