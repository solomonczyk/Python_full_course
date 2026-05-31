#!/usr/bin/env python3
"""Add practice_subtasks to remaining 17 lessons."""
import json, shutil

SRC = "backend/app/data/lessons.json"
DST = "api/app/data/lessons.json"

with open(SRC, "r", encoding="utf-8") as f:
    lessons = json.load(f)

subtasks_map = {
    "1-2": [
        {"title": "Имя в кавычках", "task": "Создай переменную name = 'Ксю' и выведи её на экран.", "expected_output": "Ксю", "hint": "print(name)"},
        {"title": "Одинарные и двойные", "task": "Создай строку text = \"Привет, 'Python'!\" и выведи её.", "expected_output": "Привет, 'Python'!", "hint": "print(text)"},
    ],
    "1-3": [
        {"title": "Обмен значениями", "task": "Создай a = 5, b = 10. Поменяй их значения местами и выведи a и b.", "expected_output": "10\n5", "hint": "temp = a; a = b; b = temp"},
        {"title": "Имя и возраст", "task": "Создай переменные name = 'Да' и age = 25. Выведи их на отдельных строках.", "expected_output": "Да\n25", "hint": "print(name); print(age)"},
    ],
    "1-5": [
        {"title": "Преобразование числа", "task": "Дано num_str = '10'. Преобразуй его в int, прибавь 5 и выведи результат.", "expected_output": "15", "hint": "num = int(num_str); print(num + 5)"},
        {"title": "Сумма двух int", "task": "Даны a = '7', b = '3'. Преобразуй в int и выведи их сумму.", "expected_output": "10", "hint": "print(int(a) + int(b))"},
    ],
    "1-6": [
        {"title": "Калькулятор", "task": "Посчитай: 15 + 3, 15 - 3, 15 * 3, 15 / 3. Каждый результат на отдельной строке.", "expected_output": "18\n12\n45\n5.0", "hint": "print(15+3); print(15-3); print(15*3); print(15/3)"},
        {"title": "Сложное выражение", "task": "Выведи результат: (10 + 5) * 2 — 3.", "expected_output": "27", "hint": "print((10 + 5) * 2 - 3)"},
    ],
    "1-7": [
        {"title": "Сравнение чисел", "task": "Даны a = 5, b = 10. Выведи результат a > b, a < b, a == b.", "expected_output": "False\nTrue\nFalse", "hint": "print(a > b); print(a < b); print(a == b)"},
        {"title": "Проверка равенства", "task": "Даны x = 7, y = 7. Выведи результат x == y и x != y.", "expected_output": "True\nFalse", "hint": "print(x == y); print(x != y)"},
    ],
    "1-8": [
        {"title": "Проверка положительности", "task": "Дано число n = -3. Если n > 0 — выведи 'Плюс', иначе ничего не делай.", "expected_output": "", "hint": "n = -3; if n > 0: print('Плюс')"},
        {"title": "Проверка возраста", "task": "Дано age = 18. Если age >= 18 — выведи 'Доступ разрешён'.", "expected_output": "Доступ разрешён", "hint": "if age >= 18: print('Доступ разрешён')"},
    ],
    "2-1": [
        {"title": "Оценка по баллам", "task": "Дано score = 85. Если score >= 90 — 'A'. Если >= 75 — 'B'. Если >= 50 — 'C'. Иначе — 'D'.", "expected_output": "B", "hint": "if score >= 90: ... elif score >= 75: ..."},
        {"title": "Время суток", "task": "Дано hour = 14. Если hour < 12 — 'утро'. Если hour < 18 — 'день'. Иначе — 'вечер'.", "expected_output": "день", "hint": "Цепочка if/elif/else"},
    ],
    "2-3": [
        {"title": "Случайное число", "task": "Подключи random, создай secret = random.randint(1, 6) и выведи его.", "expected_output": "(будет число от 1 до 6)", "hint": "import random; print(random.randint(1, 6))"},
        {"title": "Кубик", "task": "Подключи random и выведи результат броска кубика (1-6) три раза подряд.", "expected_output": "(три случайных числа)", "hint": "print(random.randint(1, 6)); print(random.randint(1, 6)); print(random.randint(1, 6))"},
    ],
    "2-4": [
        {"title": "Угадай число", "task": "Загадай secret = random.randint(1, 10). Спроси число через guess = int(input()). Если угадал — выведи 'Победа!'.", "expected_output": "Победа!", "hint": "secret = random.randint(1, 10); guess = int(input()); if guess == secret: print('Победа!')"},
    ],
    "2-5": [
        {"title": "Пять шагов", "task": "Выведи числа от 1 до 5 с помощью for и range.", "expected_output": "1\n2\n3\n4\n5", "hint": "for i in range(1, 6): print(i)"},
        {"title": "Десять шагов", "task": "Выведи числа от 0 до 9 с помощью for i in range(10).", "expected_output": "0\n1\n2\n3\n4\n5\n6\n7\n8\n9", "hint": "for i in range(10): print(i)"},
    ],
    "2-6": [
        {"title": "Диапазон 2-6", "task": "Выведи числа от 2 до 6 с помощью range(2, 7).", "expected_output": "2\n3\n4\n5\n6", "hint": "for i in range(2, 7): print(i)"},
        {"title": "Список диапазона", "task": "Создай список от 0 до 4 через list(range(5)) и выведи его.", "expected_output": "[0, 1, 2, 3, 4]", "hint": "print(list(range(5)))"},
    ],
    "3-1": [
        {"title": "Float из int", "task": "Выведи результат деления 7 / 2 и тип результата через type().", "expected_output": "3.5", "hint": "print(7 / 2); print(type(7 / 2))"},
        {"title": "Явное преобразование", "task": "Дано n = 5. Преобразуй его в float через float(n) и выведи.", "expected_output": "5.0", "hint": "print(float(n))"},
    ],
    "3-2": [
        {"title": "Обычное деление", "task": "Выведи результат 10 / 3, 9 / 2, 7 / 4 каждый на новой строке.", "expected_output": "3.3333333333333335\n4.5\n1.75", "hint": "print(10/3); print(9/2); print(7/4)"},
    ],
    "3-3": [
        {"title": "Целочисленное деление", "task": "Выведи результат 10 // 3, 9 // 2, 7 // 4.", "expected_output": "3\n4\n1", "hint": "print(10//3); print(9//2); print(7//4)"},
        {"title": "Разница делений", "task": "Выведи 10 / 3 и 10 // 3 — сравни разницу.", "expected_output": "3.3333333333333335\n3", "hint": "print(10/3); print(10//3)"},
    ],
    "3-4": [
        {"title": "Остаток от деления", "task": "Выведи остаток: 10 % 3, 9 % 4, 7 % 5.", "expected_output": "1\n1\n2", "hint": "print(10%3); print(9%4); print(7%5)"},
        {"title": "Проверка чётности", "task": "Дано n = 7. Если n % 2 == 0 — выведи 'чётное', иначе 'нечётное'.", "expected_output": "нечётное", "hint": "if n % 2 == 0: ... else: ..."},
    ],
    "3-5": [
        {"title": "Чётные числа", "task": "Выведи все чётные числа от 1 до 10 через цикл и проверку n % 2 == 0.", "expected_output": "2\n4\n6\n8\n10", "hint": "for n in range(1, 11): if n % 2 == 0: print(n)"},
        {"title": "Остаток от 8", "task": "Выведи результат 8 % 2, 8 % 3, 8 % 5.", "expected_output": "0\n2\n3", "hint": "print(8%2); print(8%3); print(8%5)"},
    ],
    "3-6": [
        {"title": "Сравнения", "task": "Выведи результат: 5 > 2, 3 == 3, 4 != 7, 6 <= 5.", "expected_output": "True\nTrue\nTrue\nFalse", "hint": "print(5 > 2); print(3 == 3); print(4 != 7); print(6 <= 5)"},
        {"title": "Логический тип", "task": "Выведи тип True и тип False через type().", "expected_output": "<class 'bool'>\n<class 'bool'>", "hint": "print(type(True)); print(type(False))"},
    ],
}

count = 0
for l in lessons:
    lid = l["id"]
    if lid in subtasks_map:
        l["practice_subtasks"] = subtasks_map[lid]
        count += 1
        print(f"✅ {lid}: {l['title']} — added {len(subtasks_map[lid])} subtasks")

with open(SRC, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)
shutil.copy2(SRC, DST)
print(f"\n✅ Added subtasks to {count} lessons")
print(f"✅ Copied to {DST}")
