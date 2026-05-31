#!/usr/bin/env python3
"""Add common_mistakes data to first 10 lessons."""
import json, shutil

SRC = "backend/app/data/lessons.json"
DST = "api/app/data/lessons.json"

with open(SRC, "r", encoding="utf-8") as f:
    lessons = json.load(f)

mistakes_map = {
    "1-1": [
        {"title": "Забыл кавычки для текста", "wrong": "print(Привет, мир!)", "right": "print(\"Привет, мир!\")", "note": "Текст в print() всегда должен быть в кавычках — иначе Python ищет переменную."},
        {"title": "Знак = после print", "wrong": "print = (\"Привет\")", "right": "print(\"Привет\")", "note": "print = ... не вызовет функцию, а перезапишет её. Просто пиши print(\"...\")"},
    ],
    "1-2": [
        {"title": "Смешиваю кавычки", "wrong": "print('Привет\")", "right": "print('Привет') или print(\"Привет\")", "note": "Нельзя начать с ' и закрыть \". Кавычки должны быть одинаковыми с обеих сторон."},
        {"title": "Забыл закрыть кавычки", "wrong": "text = \"Привет", "right": "text = \"Привет\"", "note": "Незакрытая кавычка — SyntaxError. Проверяй, что каждая кавычка имеет пару."},
    ],
    "1-3": [
        {"title": "Имя переменной с цифры", "wrong": "1player = \"Ксю\"", "right": "player1 = \"Ксю\"", "note": "Имя переменной не может начинаться с цифры. Можно использовать буквы, цифры и _."},
        {"title": "Пробел в имени", "wrong": "my name = \"Ксю\"", "right": "my_name = \"Ксю\"", "note": "Пробелы в имени переменной запрещены. Используй знак подчёркивания."},
    ],
    "1-4": [
        {"title": "Забыл преобразовать input", "wrong": "age = input()\nprint(age + 1)", "right": "age = int(input())\nprint(age + 1)", "note": "input() возвращает строку. Чтобы считать число — оберни в int()."},
    ],
    "1-6": [
        {"title": "Путаю = и ==", "wrong": "if x = 5:", "right": "if x == 5:", "note": "= это присваивание. == это сравнение. В if всегда используй ==."},
        {"title": "Порядок операций", "wrong": "print(3 + 2 * 2)  # думаю будет 10", "right": "print(3 + 2 * 2)  # будет 7", "note": "Умножение выполняется раньше сложения. Используй скобки: (3 + 2) * 2"},
    ],
    "1-7": [
        {"title": "Путаю = и ==", "wrong": "if x = 5:", "right": "if x == 5:", "note": "= присваивает. == проверяет равенство. В условиях — всегда =="},
    ],
    "1-8": [
        {"title": "Двоеточие после if", "wrong": "if x > 5\n    print(\"x большой\")", "right": "if x > 5:\n    print(\"x большой\")", "note": "После if обязательно двоеточие (:). Без него Python выдаст SyntaxError."},
        {"title": "Отступы", "wrong": "if x > 5:\nprint(\"x большой\")", "right": "if x > 5:\n    print(\"x большой\")", "note": "Код внутри if должен быть с отступом (4 пробела). Иначе Python не поймёт, что это часть условия."},
    ],
    "1-9": [
        {"title": "else без отступа", "wrong": "if x > 0:\n    print(\"Плюс\")\n    else:\n    print(\"Минус\")", "right": "if x > 0:\n    print(\"Плюс\")\nelse:\n    print(\"Минус\")", "note": "else должен быть на том же уровне отступа, что и if. Не внутри блока if."},
    ],
    "2-1": [
        {"title": "elif без if", "wrong": "elif x > 0:", "right": "if x > 0:\n    ...\nelif x > 5:", "note": "elif нельзя использовать без if. elif — это продолжение, а не начало."},
    ],
    "2-3": [
        {"title": "Забыл import random", "wrong": "print(random.randint(1, 6))  # NameError", "right": "import random\nprint(random.randint(1, 6))", "note": "Перед использованием random нужно написать import random в начале программы."},
    ],
}

count = 0
for l in lessons:
    lid = l["id"]
    if lid in mistakes_map:
        l["common_mistakes"] = mistakes_map[lid]
        count += 1
        print(f"✅ {lid}: added {len(mistakes_map[lid])} mistakes")

with open(SRC, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)
shutil.copy2(SRC, DST)
print(f"\n✅ Added common_mistakes to {count} lessons")
