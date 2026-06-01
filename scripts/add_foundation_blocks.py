#!/usr/bin/env python3
"""Add foundation blocks to all 92 lessons and fix Bagus duplicate in lesson 1-1.

Usage:
    python scripts/add_foundation_blocks.py
"""

import json
from pathlib import Path


# ── Foundation block templates per lesson topic ───────────────────────────

FOUNDATION_TEMPLATES: dict[str, dict] = {
    "print()": {
        "title": "Перед стартом",
        "terms": [
            {
                "term_id": "command",
                "label": "Команда",
                "definition": "Команда (инструкция) — это указание Python выполнить действие. Каждая строка кода — это команда."
            },
            {
                "term_id": "print",
                "label": "print()",
                "definition": "print() — это функция, которая выводит текст или значение на экран. Всё, что внутри скобок, появляется на экране."
            },
            {
                "term_id": "parentheses",
                "label": "Скобки ()",
                "definition": "Скобки после print показывают, что это вызов. Без скобок Python не поймёт, что ты хочешь вызвать print."
            },
            {
                "term_id": "quotes",
                "label": "Кавычки",
                "definition": "Текст в Python обязательно берётся в кавычки. Кавычки — это этикетка: «внутри текст, не ищи переменную»."
            },
            {
                "term_id": "string",
                "label": "Текст vs Переменная",
                "definition": "Текст в кавычках — это просто текст. Без кавычек Python ищет переменную с таким именем. print(Привет) вызовет ошибку."
            },
            {
                "term_id": "error",
                "label": "Python точен",
                "definition": "Python очень точный. Любая опечатка, пропущенная кавычка или скобка — и программа не запустится. Это дисциплина, не плохо."
            },
            {
                "term_id": "syntax_error",
                "label": "Ошибки — это обратная связь",
                "definition": "Ошибка — не провал, а подсказка. Python сообщает, что именно пошло не так. Читай сообщения — они говорят, что исправить."
            }
        ],
        "glossary_terms": ["command", "print", "parentheses", "quotes", "string", "error", "syntax_error"],
        "rules": [
            "Python выполняет команды строго по порядку — сверху вниз",
            "Текст в print() всегда берётся в кавычки",
            "Имена переменных пишутся без кавычек",
            "Каждая открытая скобка должна быть закрыта",
            "Ошибка — не страшно. Читай сообщение и исправляй"
        ]
    },
    "строки": {
        "title": "Перед стартом",
        "terms": [
            {
                "term_id": "string",
                "label": "Строка",
                "definition": "Строка (str) — это тип данных для текста. Любой текст в кавычках — это строка."
            },
            {
                "term_id": "quotes",
                "label": "Кавычки",
                "definition": "Кавычки могут быть одинарными ' или двойными \". Главное — открывать и закрывать одинаковыми."
            }
        ],
        "glossary_terms": ["string", "quotes", "concatenation", "error"],
        "rules": [
            "Текст всегда в кавычках — иначе Python ищет переменную",
            "Кавычки с обеих сторон должны быть одинаковыми",
            "Можно использовать '...' или \"...\" — разницы нет",
            "Пустая строка — это тоже строка: '' или \"\""
        ]
    },
    "переменные": {
        "title": "Перед стартом",
        "terms": [
            {
                "term_id": "variable",
                "label": "Переменная",
                "definition": "Переменная — это именованный контейнер для хранения данных. Имя без пробелов, без кавычек."
            },
            {
                "term_id": "value",
                "label": "Значение",
                "definition": "Значение — то, что хранится в переменной. Справа от знака = находится значение."
            }
        ],
        "glossary_terms": ["variable", "value", "string", "error", "pep8"],
        "rules": [
            "Имя переменной — одно слово, без пробелов",
            "Имя не может начинаться с цифры",
            "Знак = присваивает значение: имя = значение",
            "Имена переменных пишутся без кавычек",
            "PEP8 советует имена в нижнем регистре: my_variable, не MyVariable"
        ]
    },
    "input": {
        "title": "Перед стартом",
        "terms": [
            {
                "term_id": "input",
                "label": "input()",
                "definition": "input() ждёт, пока пользователь что-то введёт с клавиатуры. Программа останавливается и слушает."
            },
            {
                "term_id": "string",
                "label": "Тип данных",
                "definition": "input() всегда возвращает строку (текст). Даже если ввели число — это будет строка."
            }
        ],
        "glossary_terms": ["input", "string", "variable", "type_conversion"],
        "rules": [
            "input() всегда возвращает строку",
            "Для числа используй int(input(...))",
            "Текст в input('Вопрос: ') — это подсказка пользователю",
            "Переменная = input() — сохраняем ответ"
        ]
    },
    "числа": {
        "title": "Перед стартом",
        "terms": [
            {
                "term_id": "int",
                "label": "int()",
                "definition": "int() превращает строку в целое число. Нужно, когда получаешь число из input()."
            },
            {
                "term_id": "operator",
                "label": "Операторы",
                "definition": "Знаки действий: +, -, *, /, //, %, **. Каждый делает свою операцию."
            }
        ],
        "glossary_terms": ["int", "number", "operator", "type_conversion", "modulo"],
        "rules": [
            "int('5') превращает строку '5' в число 5",
            "Строку и число складывать нельзя — ошибка",
            "% — остаток от деления, / — деление",
            "** — степень, // — целочисленное деление",
            "str(5) превращает число 5 в строку '5'"
        ]
    },
    "if": {
        "title": "Перед стартом",
        "terms": [
            {
                "term_id": "comparison",
                "label": "Сравнение",
                "definition": "==, !=, <, >, <=, >= — сравнение значений. Результат: True или False."
            },
            {
                "term_id": "if_statement",
                "label": "if",
                "definition": "if проверяет условие и выполняет блок кода, только если оно истинно."
            }
        ],
        "glossary_terms": ["condition", "comparison", "if_statement", "else_statement", "colon", "indentation", "boolean"],
        "rules": [
            "После if обязательно ставится двоеточие :",
            "Код внутри if пишется с отступом (4 пробела)",
            "= — присвоить, == — сравнить (не путай!)",
            "if/else — как развилка: или одно, или другое",
            "elif — сокращение от else if: проверка следующего условия"
        ]
    },
}

# Default lightweight foundation for all other lessons
DEFAULT_LIGHTWEIGHT: dict = {
    "title": "Перед стартом",
    "glossary_terms": ["print", "variable", "error", "syntax_error"],
    "rules": [
        "Повторяй пройденное в глоссарии, если что-то забыл",
        "Ошибка — это подсказка, читай сообщение",
        "Пиши код аккуратно: отступы, скобки, кавычки"
    ]
}

# Map lesson topics/slugs to foundation templates
# Key is a topic keyword to match against lesson's topic field
TOPIC_MAP: dict[str, str] = {
    "print": "print()",
    "строк": "строки",
    "кавычк": "строки",
    "перемен": "переменные",
    "input": "input",
    "int": "числа",
    "числ": "числа",
    "арифметик": "числа",
    "оператор": "числа",
    "if": "if",
    "else": "if",
    "elif": "if",
    "услови": "if",
    "сравнени": "if",
    "логиче": "if",
}


def get_foundation_for_lesson(lesson: dict) -> dict:
    """Determine the appropriate foundation block for a lesson."""
    topic = (lesson.get("topic") or "").lower()
    slug = (lesson.get("slug") or "").lower()
    title = (lesson.get("title") or "").lower()

    # Try to match by topic first
    for keyword, template_key in TOPIC_MAP.items():
        if keyword in topic or keyword in slug or keyword in title:
            return dict(FOUNDATION_TEMPLATES[template_key])

    # No specific match — use lightweight
    return dict(DEFAULT_LIGHTWEIGHT)


def fix_bagus_duplicate(lesson: dict) -> bool:
    """Fix duplicate Bagus lines in post_error_dialogue. Returns True if changed."""
    dialogue = lesson.get("post_error_dialogue", [])
    if not dialogue:
        return False

    changed = False
    new_dialogue = []
    skip_next = False

    for i, line in enumerate(dialogue):
        if skip_next:
            skip_next = False
            continue

        # Check if current line is Bagus and next line is also Bagus
        if (line.get("character") == "bagus" and
                i + 1 < len(dialogue) and
                dialogue[i + 1].get("character") == "bagus"):
            # Merge the two lines
            merged_text = line["text"].rstrip()
            if not merged_text.endswith((".", "!", "?")):
                merged_text += "."
            merged_text += " " + dialogue[i + 1]["text"]
            new_dialogue.append({"character": "bagus", "text": merged_text})
            skip_next = True
            changed = True
        else:
            new_dialogue.append(line)

    if changed:
        lesson["post_error_dialogue"] = new_dialogue
    return changed


def process_lessons_file(filepath: str) -> tuple[int, int]:
    """Add foundation blocks and fix Bagus in a lessons.json file.
    Returns (foundation_count, bagus_fix_count)."""
    path = Path(filepath)
    if not path.exists():
        print(f"  ❌ File not found: {filepath}")
        return 0, 0

    with open(path, encoding="utf-8") as f:
        lessons = json.load(f)

    foundation_count = 0
    bagus_fix_count = 0

    for lesson in lessons:
        # Add foundation block if not already present
        if "foundation" not in lesson:
            lesson["foundation"] = get_foundation_for_lesson(lesson)
            foundation_count += 1

        # Fix Bagus duplicates
        if fix_bagus_duplicate(lesson):
            bagus_fix_count += 1

    # Verify lesson count preserved
    assert len(lessons) == 92, f"Expected 92 lessons, got {len(lessons)}"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)

    return foundation_count, bagus_fix_count


def main():
    base_dir = Path(__file__).resolve().parent.parent
    paths = [
        base_dir / "backend" / "app" / "data" / "lessons.json",
        base_dir / "api" / "app" / "data" / "lessons.json",
    ]

    total_foundations = 0
    total_bagus_fixes = 0

    for p in paths:
        print(f"\nProcessing: {p}")
        f_count, b_count = process_lessons_file(str(p))
        total_foundations += f_count
        total_bagus_fixes += b_count
        print(f"  Foundations added: {f_count}")
        print(f"  Bagus duplicates fixed: {b_count}")

    print(f"\n{'='*50}")
    print(f"Total foundations added: {total_foundations}")
    print(f"Total Bagus fixes: {total_bagus_fixes}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
