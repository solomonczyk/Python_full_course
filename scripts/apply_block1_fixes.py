"""
Block 1: Apply all critical data fixes to api/app/data/lessons.json

1.1 — Replace pre_topic_dialogue for 22 lessons
1.2 — Replace stub quizzes for 16 lessons
1.3 — Fix find_bug for lesson 3-2 (hint + correct)
1.4 — Fix what_outputs for lessons 1-4, 1-5
1.5 — Reduce template phrase repetition

Reads from pre_topic_dialogues.json and quizzes.json for content.
"""

import json
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

SRC = Path("api/app/data/lessons.json")
DIALOGUES_FILE = Path("pre_topic_dialogues.json")
QUIZZES_FILE = Path("new_quizzes.json")
BACKUP = Path("api/app/data/lessons.json.block1_backup")

# ============================================================
# LOAD
# ============================================================

with open(SRC, encoding="utf-8") as f:
    lessons = json.load(f)

with open(DIALOGUES_FILE, encoding="utf-8") as f:
    new_dialogues = json.load(f)

# Quiz content — inline here from the agent's output
# If new_quizzes.json exists, load from it; otherwise use inline data
if QUIZZES_FILE.exists():
    with open(QUIZZES_FILE, encoding="utf-8") as f:
        new_quizzes = json.load(f)
else:
    new_quizzes = {
        "3-7": {
            "question": "Что такое переменная-флаг?",
            "options": [
                {"id": "a", "text": "Переменная типа bool, которая хранит состояние и меняется при наступлении события", "correct": True},
                {"id": "b", "text": "Переменная, которая хранит строку с именем пользователя", "correct": False},
                {"id": "c", "text": "Переменная, которая меняет тип данных во время выполнения программы", "correct": False}
            ]
        },
        "3-8": {
            "question": "Какой результат выведет код: x = 5; result = 'чётное' if x % 2 == 0 else 'нечётное'; print(result)?",
            "options": [
                {"id": "a", "text": "нечётное", "correct": True},
                {"id": "b", "text": "чётное", "correct": False},
                {"id": "c", "text": "True", "correct": False}
            ]
        },
        "3-12": {
            "question": "Что вернёт условие if name and phone:, если name — пустая строка, а phone — непустая строка?",
            "options": [
                {"id": "a", "text": "Условие будет ложным, так как пустая строка считается False", "correct": True},
                {"id": "b", "text": "Условие будет истинным, так как phone не пустой", "correct": False},
                {"id": "c", "text": "Произойдёт ошибка, так нельзя сравнивать строки с and", "correct": False}
            ]
        },
        "4-5": {
            "question": "Что вернёт max(['a', 'bb', 'ccc'], key=len)?",
            "options": [
                {"id": "a", "text": "'ccc'", "correct": True},
                {"id": "b", "text": "'a'", "correct": False},
                {"id": "c", "text": "3", "correct": False}
            ]
        },
        "4-6": {
            "question": "Какое значение получит переменная x после выполнения кода: numbers = [10, 20, 30]; x = numbers[-1]?",
            "options": [
                {"id": "a", "text": "30", "correct": True},
                {"id": "b", "text": "10", "correct": False},
                {"id": "c", "text": "Ошибка: индекс -1 недопустим", "correct": False}
            ]
        },
        "4-17": {
            "question": "Что делает параметр key= в функциях sort() и sorted()?",
            "options": [
                {"id": "a", "text": "Указывает функцию, по результату которой элементы сравниваются при сортировке", "correct": True},
                {"id": "b", "text": "Указывает индекс элемента, с которого начинается сортировка", "correct": False},
                {"id": "c", "text": "Задаёт порядок сортировки: по возрастанию или убыванию", "correct": False}
            ]
        },
        "4-18": {
            "question": "Чему равно t[1][0], если t = [[1, 2], [3, 4]]?",
            "options": [
                {"id": "a", "text": "3", "correct": True},
                {"id": "b", "text": "2", "correct": False},
                {"id": "c", "text": "[3, 4]", "correct": False}
            ]
        },
        "4-20": {
            "question": "Как правильно перебрать все элементы вложенного списка matrix = [[1, 2], [3, 4]]?",
            "options": [
                {"id": "a", "text": "for row in matrix:\n    for item in row:\n        print(item)", "correct": True},
                {"id": "b", "text": "for item in matrix:\n    print(item)", "correct": False},
                {"id": "c", "text": "for i in range(matrix):\n    print(matrix[i])", "correct": False}
            ]
        },
        "4-21": {
            "question": "Что будет в списке a после выполнения кода: a = [1, 2]; b = a; b.append(3)?",
            "options": [
                {"id": "a", "text": "[1, 2, 3]", "correct": True},
                {"id": "b", "text": "[1, 2]", "correct": False},
                {"id": "c", "text": "Произойдёт ошибка, так как a и b — разные списки", "correct": False}
            ]
        },
        "4-22": {
            "question": "Что произойдёт при попытке выполнить s[0] = 'b', если s = 'abc'?",
            "options": [
                {"id": "a", "text": "Возникнет ошибка TypeError, так как строки неизменяемы", "correct": True},
                {"id": "b", "text": "Строка s станет равной 'bbc'", "correct": False},
                {"id": "c", "text": "Строка s станет равной 'b'", "correct": False}
            ]
        },
        "4-23": {
            "question": "Какое значение вернёт выражение a is b, если a = [1] и b = [1]?",
            "options": [
                {"id": "a", "text": "False — это разные объекты в памяти, хотя значения совпадают", "correct": True},
                {"id": "b", "text": "True — значения одинаковые, значит это один объект", "correct": False},
                {"id": "c", "text": "None", "correct": False}
            ]
        },
        "4-24": {
            "question": "После копирования списка через copy() и изменения вложенного элемента в копии — изменится ли оригинал?",
            "options": [
                {"id": "a", "text": "Да, так как copy() создаёт поверхностную копию, и вложенные списки остаются общими", "correct": True},
                {"id": "b", "text": "Нет, copy() создаёт полностью независимую копию всех уровней", "correct": False},
                {"id": "c", "text": "Зависит от длины исходного списка", "correct": False}
            ]
        },
        "4-25": {
            "question": "Чем deepcopy() отличается от обычного copy() при копировании вложенных списков?",
            "options": [
                {"id": "a", "text": "deepcopy() создаёт полностью независимые копии на всех уровнях вложенности", "correct": True},
                {"id": "b", "text": "deepcopy() копирует только элементы верхнего уровня, а copy() копирует всё", "correct": False},
                {"id": "c", "text": "deepcopy() работает только с числами, а copy() — с любыми типами", "correct": False}
            ]
        },
        "4-28": {
            "question": "Какая конструкция используется, чтобы запрашивать ввод у пользователя, пока он не введёт корректное значение?",
            "options": [
                {"id": "a", "text": "while True с break внутри при успешной проверке", "correct": True},
                {"id": "b", "text": "if с проверкой внутри for-цикла", "correct": False},
                {"id": "c", "text": "try без except", "correct": False}
            ]
        },
        "4-29": {
            "question": "Как в чат-боте на Python проверить, содержит ли сообщение пользователя определённое слово?",
            "options": [
                {"id": "a", "text": "if 'привет' in message.lower():", "correct": True},
                {"id": "b", "text": "if message == 'привет':", "correct": False},
                {"id": "c", "text": "if message.find('привет') is True:", "correct": False}
            ]
        },
        "4-30": {
            "question": "Какой метод списка используется для добавления новой задачи в таск-менеджер?",
            "options": [
                {"id": "a", "text": "tasks.append('новая задача')", "correct": True},
                {"id": "b", "text": "tasks.add('новая задача')", "correct": False},
                {"id": "c", "text": "tasks.push('новая задача')", "correct": False}
            ]
        }
    }


# ============================================================
# BACKUP
# ============================================================
if not BACKUP.exists():
    with open(BACKUP, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)
    print(f"Backup saved to {BACKUP}")

# ============================================================
# TASK 1.1 — Replace pre_topic_dialogue for 22 lessons
# ============================================================
lessons_by_id = {l["id"]: l for l in lessons}
replaced_dialogue_count = 0

for lesson_id, new_dialogue in new_dialogues.items():
    if lesson_id in lessons_by_id:
        lessons_by_id[lesson_id]["pre_topic_dialogue"] = new_dialogue
        replaced_dialogue_count += 1
        print(f"  ✓ Dialogue replaced: lesson {lesson_id}")
    else:
        print(f"  ✗ Lesson {lesson_id} not found, skipping dialogue")

print(f"\nTask 1.1: Replaced dialogues for {replaced_dialogue_count} lessons\n")

# ============================================================
# TASK 1.2 — Replace stub quizzes for 16 lessons
# ============================================================
replaced_quiz_count = 0

for lesson_id, new_quiz in new_quizzes.items():
    if lesson_id in lessons_by_id:
        lessons_by_id[lesson_id]["quiz"] = new_quiz
        replaced_quiz_count += 1
        print(f"  ✓ Quiz replaced: lesson {lesson_id}")
    else:
        print(f"  ✗ Lesson {lesson_id} not found, skipping quiz")

print(f"\nTask 1.2: Replaced quizzes for {replaced_quiz_count} lessons\n")

# ============================================================
# TASK 1.3 — Fix find_bug for lesson 3-2
# ============================================================
if "3-2" in lessons_by_id:
    fb = lessons_by_id["3-2"]["find_bug"]
    # Fix hint: should explain that // is integer division, not regular /
    fb["hint"] = "Задача требует обычного деления с дробным результатом. Какой оператор нужен вместо //?"
    # Ensure correct field
    fb["correct"] = "a = int(input())\nb = int(input())\nprint(a / b)"
    print(f"  ✓ Fixed find_bug for lesson 3-2")

# Add correct field to ALL find_bug blocks that don't have it
# (The analysis showed all 87 already have it, but let's double-check)
missing_correct = []
for lesson in lessons:
    fb = lesson.get("find_bug", {})
    if fb and "correct" not in fb:
        missing_correct.append(lesson["id"])
    elif fb and not fb.get("correct"):
        missing_correct.append(lesson["id"])

if missing_correct:
    print(f"  ⚠ {len(missing_correct)} find_bug blocks still missing 'correct': {missing_correct}")
else:
    print(f"  ✓ All find_bug blocks have the 'correct' field")

print()

# ============================================================
# TASK 1.4 — Fix what_outputs for lessons with input()
# ============================================================
# Lesson 1-4: input() → deterministic
if "1-4" in lessons_by_id:
    lessons_by_id["1-4"]["what_outputs"] = {
        "code": "name = \"Ксю\"\nprint(\"Привет\")\nprint(name)",
        "options": ["Привет", "Ксю", "Привет\nКсю"],
        "correct": "Привет"
    }
    print(f"  ✓ Fixed what_outputs for lesson 1-4")

# Lesson 1-5: int(input()) → deterministic
if "1-5" in lessons_by_id:
    lessons_by_id["1-5"]["what_outputs"] = {
        "code": "x = int(\"5\")\nprint(x * 2)",
        "options": ["10", "55", "Ошибка"],
        "correct": "10"
    }
    print(f"  ✓ Fixed what_outputs for lesson 1-5")

# Check for any other lessons with empty what_outputs options
other_empty = []
for lesson in lessons:
    wo = lesson.get("what_outputs", {})
    if wo and not wo.get("options"):
        other_empty.append(lesson["id"])

if other_empty:
    print(f"  ⚠ Other lessons with empty what_outputs options: {other_empty}")
else:
    print(f"  ✓ No other lessons with empty what_outputs options")

print()

# ============================================================
# TASK 1.5 — Reduce template phrase repetition
# Uses per-lesson-id replacement for precise targeting
# ============================================================

phrase1 = "Кажется, дошло. Можно попробовать самому?"
phrase2 = "Точно. В следующий раз буду внимательнее."

# Pre-count
cnt1 = cnt2 = 0
for lesson in lessons:
    for d in lesson.get("pre_topic_dialogue", []) + lesson.get("post_error_dialogue", []):
        if d.get("character") == "novice":
            if d.get("text") == phrase1: cnt1 += 1
            elif d.get("text") == phrase2: cnt2 += 1
print(f"Template phrase counts BEFORE:  phrase1={cnt1}  phrase2={cnt2}")

# Per-lesson replacements for phrase1 (pre_topic_dialogue final novice line)
# Keyed by lesson_id — each gets a unique reply tied to that lesson's topic
phrase1_replacements = {
    "1-1": "Хорошо, print() как голос программы — запомнил.",
    "1-2": "Выходит, любая строка — это текст в кавычках. Без них — NameError.",
    "1-3": "Переменная хранит значение, а имя переменной — без кавычек. Ясно.",
    "1-4": "То есть input() без int() вернёт строку, даже если ввели число?",
    "1-5": "Значит int(input()) — это два в одном: сначала ввод, потом превращение в число.",
    "1-6": "Понял: умножение и деление раньше сложения и вычитания. Скобки меняют порядок.",
    "1-7": "То есть == сравнивает, а = присваивает. Теперь не перепутаю.",
    "1-8": "Значит if проверяет условие, и если True — выполняет код внутри. Без двоеточия — ошибка.",
    "1-9": "Ага, if и else как развилка: если True — один путь, если False — другой.",
    "2-1": "elif — это else if, ещё одна проверка, если первая не сработала.",
    "2-2": "Несколько elif подряд — как лестница: первое истинное срабатывает, остальные пропускаются.",
    "3-1": "float — это дробные числа. int — целые. Деление / всегда даёт float.",
    "3-2": "Обычное деление — это /. // — целочисленное. Важно не перепутать.",
    "3-3": "// отбрасывает дробную часть. Полезно, когда нужен только целый результат.",
    "3-4": "Остаток от деления % — удобно проверять чётность и делить нацело.",
    "3-5": "x % 2 == 0 — число чётное. x % 2 == 1 — нечётное. Простая и мощная проверка.",
    "3-6": "bool — это True или False. Всё остальное Python сам приводит к bool при проверке.",
    "3-13": "Вложенные if — это проверка внутри проверки. Как матрёшка.",
    "3-15": "range(2, 7) даёт 2, 3, 4, 5, 6. Первое включается, последнее — нет.",
    "3-16": "range(0, 10, 2) — каждый второй. Шаг можно любой, даже отрицательный.",
    "3-17": "range(5, 0, -1) идёт от 5 до 1. Отрицательный шаг — обратный отсчёт.",
    "3-18": "Переменная в цикле может накапливать сумму: total = total + i.",
    "3-19": "Строки можно складывать: 'при' + 'вет' = 'привет'. Это конкатенация.",
    "3-20": "Оператор in проверяет, есть ли подстрока: 'key' in 'monkey' → True.",
    "3-21": "len() считает символы в строке или элементы в списке. Индексация с нуля.",
    "3-24": "s[0] — первый символ, s[-1] — последний. Python считает от начала и от конца.",
    "3-25": "s[1:4] берёт символы с индекса 1 по 3. Последний не включается.",
    "3-26": "for char in word: — перебирает каждый символ. Удобно для анализа текста.",
    "3-27": "Список — это коллекция элементов в квадратных скобках. Можно хранить что угодно.",
    "3-28": "lst[0] = 'новое' — замена элемента по индексу. Списки можно менять напрямую.",
    "3-29": "pop() удаляет и возвращает последний элемент. Как стопка тарелок.",
    "3-30": "remove() удаляет первый элемент с заданным значением. Если значения нет — ошибка.",
    "3-31": "append() добавляет элемент в конец списка. Самый частый метод для списков.",
    "3-32": "index() возвращает индекс первого вхождения элемента. Если элемента нет — ошибка.",
    "3-33": "sum(lst) складывает все числа в списке. max() и min() тоже работают.",
    "3-34": "count() считает, сколько раз элемент встречается в списке.",
    "3-35": "list comprehension — это генератор списка в одной строке: [x for x in lst if x > 0].",
    "3-36": "insert(0, x) вставляет в начало. insert(len(lst), x) — в конец, как append.",
    "3-37": "extend() добавляет все элементы другого списка. В отличие от append, не создаёт вложенность.",
    "3-38": "lst[1:4] для списков работает как со строками — возвращает новый список-срез.",
    "3-41": "Отступы в Python — не украшение, а синтаксис. Один лишний пробел — и ошибка.",
    "4-1": "flag = True/False — простой способ запомнить состояние: был ли ключ найден.",
    "4-2": "break выходит из цикла немедленно. Для while True это единственный способ остановиться.",
    "4-3": "max = lst[0]; for x in lst: if x > max: max = x. Ручной поиск максимума.",
    "4-4": "min = lst[0]; for x in lst: if x < min: min = x. Ручной поиск минимума.",
    "4-7": "None — это ничего. Не ноль, не пустая строка, а именно отсутствие значения.",
    "4-9": '"-".join(items) склеивает список через разделитель. Быстро и удобно.',
    "4-10": '\\n — перенос строки внутри текста. print("строка1\\nстрока2") выведет две строки.',
    "4-11": "a, b = [1, 2] распаковывает список в переменные. Количество должно совпадать.",
    "4-12": '"a b c".split() режет строку по пробелам и возвращает список слов.',
    "4-13": '"1,2,3".split(",") режет по любому разделителю, не только по пробелу.',
    "4-14": "map(int, items) применяет int к каждому элементу. Удобно для конвертации строк в числа.",
    "4-17": "key=len в сортировке: sorted(words, key=len) сортирует по длине слова.",
    "4-18": "Вложенный список — это список внутри списка. matrix[0][1] — элемент первой строки, второй колонки.",
    "4-19": "matrix[0][1] = 5 меняет элемент внутри вложенного списка. Работает как с обычным списком.",
    "4-20": "for row in matrix: for item in row: — два цикла, чтобы добраться до каждого элемента.",
    "4-23": "a is b проверяет, один ли объект. a == b — равны ли значения. Разные проверки.",
    "4-24": "copy() — поверхностная копия. Верхний уровень независим, вложенный — общий.",
    "4-25": "deepcopy() копирует всё до любого уровня. Полная независимость.",
    "4-26": "while условие: выполняется, пока условие истинно. Если условие всегда True — бесконечный цикл.",
    "4-27": "while True с break — стандартный паттерн для игр: делай вечно, пока не скажут стоп.",
    "4-28": "while True: if valid: break — пока не получишь корректный ввод.",
    "4-29": 'if "привет" in msg.lower(): — поиск ключевых слов в сообщении пользователя.',
    "4-30": "Список задач = список Python. append — добавить, for — показать все.",
    "4-31": "random.randint + while True + if/break = каркас любой консольной игры.",
}

# Per-lesson replacements for phrase2 (post_error_dialogue final novice line)
phrase2_replacements = {
    "1-1": "Осознал: print('текст') — кавычки обязательны. Без них Python лезет искать переменную.",
    "1-2": "Понял: кавычки должны быть одинаковыми с обеих сторон. Смешивать ' и \" нельзя.",
    "1-3": "Ясно: print(имя_переменной) без кавычек выводит значение. С кавычками — просто текст.",
    "1-4": "Понял: input() возвращает строку. Если нужно число — заворачивай в int().",
    "1-5": "Запомнил: int('5') + 3 работает, '5' + 3 — ошибка. Типы нужно согласовывать.",
    "1-6": "Понял: / всегда даёт float. Даже 6 / 2 = 3.0, а не 3. Если нужен int — используй //.",
    "1-7": "Ясно: == проверяет, = присваивает. Ошибка компиляции сразу покажет, если перепутал.",
    "1-8": "Запомнил: после if обязательно двоеточие и отступ. Без этого SyntaxError.",
    "1-9": "Ясно: else без if не работает. А if без else — работает, это нормально.",
    "2-1": "Понял: elif нельзя использовать без if. Это продолжение, а не начало.",
    "2-2": "Ясно: порядок elif важен — первое истинное условие побеждает.",
    "3-1": "Запомнил: 3.14 — float, 3 — int. type() показывает, что внутри.",
    "3-2": "Ясно: / — это дробь, // — целая часть. Для обычной математики нужно /.",
    "3-3": "Понял: // отбрасывает остаток. Для деления нацело — то что надо.",
    "3-4": "Ясно: % возвращает остаток. 7 % 2 = 1, потому что 7 = 3*2 + 1.",
    "3-5": "Понял: if n % 2 == 0 — чётное. Это стандартная проверка, запомнил.",
    "3-6": "Запомнил: True и False с большой буквы. true — это просто имя переменной.",
    "3-13": "Понял: без правильного отступа Python не поймёт, где внешний if, а где внутренний.",
    "3-15": "Ясно: range(2, 5) = 2,3,4. Последнее число не входит. Запомню как 'до, но не включая'.",
    "3-16": "Понял: range(10, 0, -2) = 10,8,6,4,2. Шаг и направление — два параметра.",
    "3-17": "Ясно: range(4, -1, -1) — это 4,3,2,1,0. Удобно для обратного обхода списка.",
    "3-18": "Понял: total += i — это total = total + i. Сокращённая запись для накопления.",
    "3-19": "Ясно: '2' + '2' = '22', а не 4. Строки не складываются как числа.",
    "3-20": "Понял: in проверяет наличие, а == проверяет равенство. Разные операции.",
    "3-21": "Ясно: len() считает символы, а индексы идут с 0. len('abc') = 3, последний индекс = 2.",
    "3-24": "Понял: s[-1] — последний символ, s[-2] — предпоследний. Отрицательные индексы с конца.",
    "3-25": "Ясно: срез s[0:2] включает 0 и 1, но не 2. Работает как range.",
    "3-26": "Понял: for char in text перебирает каждый символ. Не нужно следить за индексами.",
    "3-27": "Запомнил: первый элемент списка имеет индекс 0, а не 1. Распространённая ошибка.",
    "3-28": "Ясно: lst[0] = x меняет список. Для строк такое не пройдёт — они неизменяемы.",
    "3-29": "Понял: pop() без аргумента удаляет последний. pop(0) — первый. И возвращает удалённое.",
    "3-30": "Ясно: remove() удаляет по значению. Если значения нет — ValueError.",
    "3-31": "Понял: append() не возвращает новый список. Он меняет текущий и возвращает None.",
    "3-32": "Ясно: index() падает с ошибкой, если элемент не найден. Сначала проверяй через in.",
    "3-33": "Понял: sum([1, 2, 3]) = 6. Для строк не работает — нужно join().",
    "3-34": "Запомнил: count() считает вхождения. Если 0 — значит элемента нет в списке.",
    "3-35": "Понял: фильтрация через list comprehension быстрее и короче, чем цикл с if.",
    "3-36": "Ясно: insert(0, x) сдвигает все элементы вправо. Для больших списков это медленно.",
    "3-37": "Понял: extend() — как несколько append подряд. Но принимает список, а не один элемент.",
    "3-38": "Ясно: срез списка создаёт новый список. Оригинал не меняется.",
    "3-41": "Понял: отступы в Python — это 4 пробела, не табуляция. Смешивать их нельзя.",
    "4-1": "Запомнил: флаг переключается с False на True при наступлении события. Один бит информации.",
    "4-2": "Ясно: break выходит только из одного цикла. Из двух вложенных — только из внутреннего.",
    "4-3": "Понял: начальное значение для максимума должно быть минимально возможным.",
    "4-4": "Ясно: начальное значение для минимума наоборот — максимально возможным.",
    "4-7": "Понял: None и 0 — не одно и то же. None — отсутствие значения, 0 — число.",
    "4-9": "Ясно: join() работает только со списком строк. ' '.join([1, 2]) — ошибка TypeError.",
    "4-10": "Понял: \\n внутри строки создаёт новую строку. Для читаемого вывода многострочного текста.",
    "4-11": "Запомнил: количество переменных слева должно равняться количеству элементов справа.",
    "4-12": "Понял: split() без аргументов режет по пробелам и табуляции. Режет всё подряд.",
    "4-13": "Ясно: split(',') режет строго по запятой. Если запятой нет — вернёт список из одного элемента.",
    "4-14": "Понял: map() возвращает итератор, а не список. list(map(...)) если нужен список.",
    "4-17": "Ясно: key=len сортирует по длине, key=str.lower — без учёта регистра.",
    "4-18": "Понял: t[1] — это весь вложенный список [3,4], t[1][0] — число 3 из него.",
    "4-19": "Запомнил: изменение во вложенном списке видно всем ссылкам. Ссылки — это ярлыки.",
    "4-26": "Понял: если забыть обновить условие — получится бесконечный цикл. Ctrl+C для спасения.",
    "4-27": "Ясно: while True без break внутри — вечный цикл. break — единственный выход.",
    "4-31": "Понял: import random + while True + input + if — базовый набор для консольной игры.",
    # --- Missing phrase2 replacements for remaining 29 lessons ---
    "2-3": "Понял: import random сначала, потом random.randint. Модуль надо подключить до вызова.",
    "2-4": "Понял: secret = randint, guess = int(input()), сравниваю через if. Угадайка готова.",
    "2-5": "Ясно: for сам повторяет блок кода. range(n) говорит сколько раз.",
    "2-6": "Понял: range(5) — это 0,1,2,3,4. Если нужно с единицы — range(1, 6).",
    "3-7": "Понял: флаг — это bool-переменная. False → True при событии. Просто и надёжно.",
    "3-8": "Ясно: тернарник — это x if условие else y. Для простых веток, не для сложных.",
    "3-9": "Понял: and требует оба True. Если первое False — второе не проверяется.",
    "3-10": "Ясно: or требует хотя бы одно True. Первое True — и проверка закончена.",
    "3-11": "Понял: not переворачивает True↔False. Читается как 'если не'.",
    "3-12": "Понял: if not var: лучше чем if var == False:. Чистый код короче.",
    "3-14": "Ясно: for i in range(n) — i пробегает 0..n-1. range — счётчик, for — повторитель.",
    "3-22": "Понял: f'{var}' подставляет значение. Не нужны ни плюсы, ни str().",
    "3-23": "Ясно: .lower().strip() чистят ввод. .split() режет на слова. Без этого команды не сравнить.",
    "3-39": "Понял: random.choice(список) берёт случайный элемент. Удобнее randint + индекс.",
    "3-40": "Ясно: shuffle на месте меняет порядок. Копировать нужно до, а не после.",
    "4-5": "Понял: longest = ''; for s in list: if len(s) > len(longest): longest = s.",
    "4-6": "Ясно: [-1] — последний. [:-1] — все кроме последнего. Отрицательные индексы удобны.",
    "4-8": "Понял: сначала алгоритм словами, потом код. Шаг за шагом, а не всё сразу.",
    "4-15": "Понял: sort() на месте меняет список и не возвращает ничего. sorted() — новый список.",
    "4-16": "Ясно: sorted() не трогает оригинал, sort() — меняет. Для безопасной сортировки — sorted.",
    "4-20": "Понял: for row in matrix: for item in row: — два цикла для вложенных списков.",
    "4-21": "Ясно: b = a не копирует список. b и a — два имени одной коробки. Нужен copy().",
    "4-22": "Понял: список изменяем, строка — нет. s[0] = 'x' — ошибка для строк.",
    "4-23": "Ясно: a is b проверяет, один ли объект. a == b проверяет, равны ли значения.",
    "4-24": "Понял: copy() — поверхностная копия. Вложенные списки всё равно общие.",
    "4-25": "Ясно: deepcopy() копирует всё, включая вложенные списки. Полностью независимая копия.",
    "4-28": "Понял: while True: input() if valid: break — стандартный паттерн для ввода.",
    "4-29": "Ясно: if 'слово' in message.lower(): — проверка ключевых слов без учёта регистра.",
    "4-30": "Понял: список задач — это список. append добавляет, pop удаляет, for перебирает.",
}

# Apply replacements
replaced_1 = 0
replaced_2 = 0
found_lessons_1 = set()
found_lessons_2 = set()

for lesson in lessons:
    lid = lesson["id"]
    # Replace phrase1 in pre_topic_dialogue
    for d in lesson.get("pre_topic_dialogue", []):
        if d.get("character") == "novice" and d.get("text") == phrase1:
            if lid in phrase1_replacements:
                d["text"] = phrase1_replacements[lid]
                replaced_1 += 1
                found_lessons_1.add(lid)
    # Replace phrase2 in post_error_dialogue
    for d in lesson.get("post_error_dialogue", []):
        if d.get("character") == "novice" and d.get("text") == phrase2:
            if lid in phrase2_replacements:
                d["text"] = phrase2_replacements[lid]
                replaced_2 += 1
                found_lessons_2.add(lid)

# Count remaining
new_cnt1 = new_cnt2 = 0
for lesson in lessons:
    for d in lesson.get("pre_topic_dialogue", []) + lesson.get("post_error_dialogue", []):
        if d.get("character") == "novice":
            if d.get("text") == phrase1: new_cnt1 += 1
            elif d.get("text") == phrase2: new_cnt2 += 1

print(f"\nTemplate phrase counts AFTER:")
print(f"  '{phrase1}' — {new_cnt1} (was {cnt1}, replaced {replaced_1} in {len(found_lessons_1)} lessons)")
print(f"  '{phrase2}' — {new_cnt2} (was {cnt2}, replaced {replaced_2} in {len(found_lessons_2)} lessons)")
print(f"  Replaced total: {replaced_1 + replaced_2}")

# ============================================================
# WRITE
# ============================================================

with open(SRC, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

print(f"\n✅ Written to {SRC}")
print(f"Total lessons in file: {len(lessons)}")
