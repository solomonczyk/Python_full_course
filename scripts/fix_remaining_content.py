#!/usr/bin/env python3
"""Fix remaining content issues: subtask mismatches, find_bug, quiz, syntax_reminder, connection_to_game."""
import json, shutil

SRC = "backend/app/data/lessons.json"
DST = "api/app/data/lessons.json"

with open(SRC, "r", encoding="utf-8") as f:
    lessons = json.load(f)

# ── 1. FIX practice_subtask mismatches ──
print("1. Fixing practice_subtask mismatches...")

# 3-27: second subtask is about replacement (3-28 topic), fix to list basics
for l in lessons:
    if l["id"] == "3-27":
        l["practice_subtasks"][1] = {
            "title": "Длина списка",
            "task": "Дан список fruits = ['яблоко', 'банан', 'апельсин', 'киви']. Выведи количество элементов через len().",
            "expected_output": "4",
            "hint": "print(len(fruits))"
        }
        print("  ✅ 3-27: fixed subtask to list basics")

# 3-31: second subtask uses pop(), fix to append
    if l["id"] == "3-31":
        l["practice_subtasks"][1] = {
            "title": "Сбор монет",
            "task": "Создай пустой список coins. Добавь в него 10, затем 20, затем 30 через append(). Выведи весь список.",
            "expected_output": "[10, 20, 30]",
            "hint": "coins = []; coins.append(10); coins.append(20); coins.append(30); print(coins)"
        }
        print("  ✅ 3-31: fixed subtask to append")

# 4-1: second subtask is plain if/elif without flag, fix to boolean flag
    if l["id"] == "4-1":
        l["practice_subtasks"][1] = {
            "title": "Флаг открытия",
            "task": "Дан список doors = ['закрыто', 'закрыто', 'открыто', 'закрыто']. Используй флаг found = False. Найди 'открыто' в цикле, поставь found = True. Выведи found.",
            "expected_output": "True",
            "hint": "found = False; for door in doors: if door == 'открыто': found = True; break; print(found)"
        }
        print("  ✅ 4-1: fixed subtask to use boolean flag")

# ── 2. FIX find_bug off-topic ──
print("\n2. Fixing find_bug off-topic...")

for l in lessons:
    if l["id"] == "4-8":  # algorithmic thinking — bug in algorithm logic
        l["find_bug"]["description"] = "Программа должна найти сумму всех положительных чисел. Но алгоритм считает неправильно. Найди ошибку."
        l["find_bug"]["code"] = "numbers = [-3, 5, -1, 2]\ntotal = 0\nfor n in numbers:\n    if n > 0:\n        total = n\nprint(total)"
        l["find_bug"]["hint"] = "Переменная total не накапливает сумму — она просто перезаписывается. Нужно total += n."
        l["find_bug"]["correct"] = "numbers = [-3, 5, -1, 2]\ntotal = 0\nfor n in numbers:\n    if n > 0:\n        total += n\nprint(total)"
        print("  ✅ 4-8: fixed find_bug to algorithm logic")

    elif l["id"] == "4-20":  # nested list iteration — bug in nested loop
        l["find_bug"]["description"] = "Нужно вывести каждый элемент вложенного списка. Но код выводит не то."
        l["find_bug"]["code"] = "matrix = [[1, 2], [3, 4]]\nfor row in matrix:\n    print(row)"
        l["find_bug"]["hint"] = "print(row) выводит весь список целиком. Нужен вложенный цикл для каждого элемента."
        l["find_bug"]["correct"] = "matrix = [[1, 2], [3, 4]]\nfor row in matrix:\n    for item in row:\n        print(item)"
        print("  ✅ 4-20: fixed find_bug to nested iteration")

    elif l["id"] == "4-22":  # mutable vs immutable — bug with string mutation
        l["find_bug"]["description"] = "Программа пытается изменить строку, но это вызывает ошибку. Что не так?"
        l["find_bug"]["code"] = 'name = "Python"\nname[0] = "J"\nprint(name)'
        l["find_bug"]["hint"] = "Строки неизменяемы! Нельзя присвоить значение по индексу. Создай новую строку."
        l["find_bug"]["correct"] = 'name = "Python"\nname = "J" + name[1:]\nprint(name)'
        print("  ✅ 4-22: fixed find_bug to string immutability")

    elif l["id"] == "4-23":  # is vs == — bug confusing identity and equality
        l["find_bug"]["description"] = "Программа должна проверить, являются ли два объекта одним и тем же. Но проверка неверная."
        l["find_bug"]["code"] = "a = [1, 2]\nb = [1, 2]\nif a == b:\n    print('один объект')"
        l["find_bug"]["hint"] = "== проверяет равенство значений, а не идентичность объектов. Нужен is."
        l["find_bug"]["correct"] = "a = [1, 2]\nb = [1, 2]\nif a is b:\n    print('один объект')"
        print("  ✅ 4-23: fixed find_bug to is vs ==")

    elif l["id"] == "4-29":  # chatbot — bug in message handling logic
        l["find_bug"]["description"] = "Чат-бот должен отвечать 'Привет!' на 'привет'. Но он не распознаёт слово."
        l["find_bug"]["code"] = "msg = 'Привет'\nif msg == 'привет':\n    print('бот: Привет!')"
        l["find_bug"]["hint"] = "Python чувствителен к регистру. 'Привет' и 'привет' — разные строки. Используй .lower()."
        l["find_bug"]["correct"] = "msg = 'Привет'\nif msg.lower() == 'привет':\n    print('бот: Привет!')"
        print("  ✅ 4-29: fixed find_bug to message case handling")

# ── 3. FIX quiz duplicate 3-4/3-5 ──
print("\n3. Fixing quiz duplicate...")
for l in lessons:
    if l["id"] == "3-5":  # should test parity, not %
        old_q = l["quiz"]["question"]
        l["quiz"]["question"] = "Как проверить, является ли число n чётным?"
        l["quiz"]["options"] = [
            {"id": "a", "text": "n % 2 == 0", "correct": True},
            {"id": "b", "text": "n // 2 == 0", "correct": False},
            {"id": "c", "text": "n / 2 == 0", "correct": False},
        ]
        print(f"  ✅ 3-5: quiz changed: \"{old_q}\" -> \"Как проверить, является ли число n чётным?\"")

# ── 4. ADD syntax_reminder to 51 lessons ──
print("\n4. Adding syntax_reminder...")

syntax_map = {
    "1-2": {"type": "indentation_reminder", "message": "Не забудь закрыть кавычки: '\"Привет\"' — и одинарные, и двойные работают."},
    "1-3": {"type": "indentation_reminder", "message": "Имя переменной: только буквы, цифры и _, начинается с буквы."},
    "1-6": {"type": "indentation_reminder", "message": "Порядок операций: сначала */, потом +-, как в математике."},
    "1-7": {"type": "indentation_reminder", "message": "== проверяет равенство, = присваивает. Не путай!"},
    "2-1": {"type": "colon_reminder", "message": "После каждого if, elif и else обязательно ставь двоеточие."},
    "2-2": {"type": "colon_reminder", "message": "В цепочке условий важен порядок: первое True побеждает."},
    "2-3": {"type": "block_structure_reminder", "message": "import random — в самом начале программы, один раз."},
    "2-5": {"type": "colon_reminder", "message": "После for обязательно двоеточие: for i in range(5):"},
    "2-6": {"type": "range_reminder", "message": "range(n) даёт 0..n-1, range(1, n) даёт 1..n-1."},
    "3-1": {"type": "input_conversion_reminder", "message": "int() — для целых, float() — для дробных."},
    "3-2": {"type": "indentation_reminder", "message": "/ всегда даёт float, даже если делится нацело."},
    "3-3": {"type": "indentation_reminder", "message": "// отбрасывает дробную часть — получается целое число."},
    "3-4": {"type": "indentation_reminder", "message": "% возвращает остаток от деления."},
    "3-5": {"type": "indentation_reminder", "message": "n % 2 == 0 — проверка чётности. Запомни это!"},
    "3-6": {"type": "indentation_reminder", "message": "True и False пишутся с большой буквы."},
    "3-7": {"type": "indentation_reminder", "message": "Флаг — это bool-переменная: False в начале, True при событии."},
    "3-8": {"type": "indentation_reminder", "message": "Тернарник: x if условие else y — всё в одной строке."},
    "3-10": {"type": "indentation_reminder", "message": "or: True если хотя бы одно True."},
    "3-11": {"type": "indentation_reminder", "message": "not переворачивает: not True = False, not False = True."},
    "3-12": {"type": "indentation_reminder", "message": "if var: — короткая запись вместо if var == True."},
    "3-13": {"type": "block_structure_reminder", "message": "Вложенный if должен быть с отступом внутри внешнего if."},
    "3-14": {"type": "colon_reminder", "message": "for i in range(n): — повторяет блок кода n раз."},
    "3-15": {"type": "range_reminder", "message": "range(start, stop): start INCLUDED, stop EXCLUDED."},
    "3-16": {"type": "range_reminder", "message": "range(start, stop, step): шаг может быть отрицательным."},
    "3-19": {"type": "indentation_reminder", "message": "Строки можно складывать: 'Привет, ' + 'мир!'"},
    "3-20": {"type": "indentation_reminder", "message": "in проверяет вхождение: 'a' in 'cat' → True."},
    "3-21": {"type": "indentation_reminder", "message": "len() работает и для строк, и для списков."},
    "3-22": {"type": "indentation_reminder", "message": "f'{var}' подставляет значение переменной прямо в строку."},
    "3-23": {"type": "mutation_reminder", "message": "Методы строк возвращают новую строку, не меняют исходную."},
    "3-24": {"type": "index_reminder", "message": "Индексы начинаются с 0. s[0] — первый символ."},
    "3-26": {"type": "loop_stop_reminder", "message": "for char in text: перебирает каждый символ."},
    "3-29": {"type": "indentation_reminder", "message": "pop() удаляет и возвращает последний элемент."},
    "3-30": {"type": "indentation_reminder", "message": "remove() удаляет по значению, а не по индексу."},
    "3-32": {"type": "indentation_reminder", "message": "index() возвращает индекс первого вхождения."},
    "3-34": {"type": "indentation_reminder", "message": "count() считает, сколько раз элемент встречается в списке."},
    "3-35": {"type": "indentation_reminder", "message": "filter = [x for x in list if условие] — list comprehension."},
    "3-36": {"type": "indentation_reminder", "message": "insert(i, x) вставляет элемент на позицию i."},
    "3-37": {"type": "indentation_reminder", "message": "extend() добавляет все элементы из другого списка."},
    "3-38": {"type": "index_reminder", "message": "list[a:b] — срез от a до b-1."},
    "3-39": {"type": "indentation_reminder", "message": "random.choice(list) — случайный элемент из списка."},
    "3-40": {"type": "indentation_reminder", "message": "shuffle() перемешивает список на месте, возвращает None."},
    "3-41": {"type": "block_structure_reminder", "message": "Отступы в Python — 4 пробела. Не смешивай с табуляцией."},
    "4-2": {"type": "loop_stop_reminder", "message": "break выходит из цикла немедленно."},
    "4-3": {"type": "indentation_reminder", "message": "Максимум: mx = numbers[0]; for n in nums: if n > mx: mx = n"},
    "4-5": {"type": "indentation_reminder", "message": "max(list, key=len) — элемент с максимальной длиной."},
    "4-6": {"type": "index_reminder", "message": "s[-1] — последний элемент, s[-2] — предпоследний."},
    "4-7": {"type": "indentation_reminder", "message": "None — отсутствие значения. Не путай с 0 или пустой строкой."},
    "4-8": {"type": "block_structure_reminder", "message": "Сначала продумай алгоритм словами, потом пиши код."},
    "4-10": {"type": "indentation_reminder", "message": "\\n внутри строки — перенос на новую строку."},
    "4-11": {"type": "indentation_reminder", "message": "a, b = [1, 2] — распаковка списка в переменные."},
    "4-12": {"type": "indentation_reminder", "message": "split() без аргументов делит по пробелам."},
    "4-14": {"type": "indentation_reminder", "message": "map() возвращает итератор. Оберни в list() для списка."},
    "4-17": {"type": "indentation_reminder", "message": "key= в sort/sorted задаёт функцию для сравнения."},
    "4-18": {"type": "index_reminder", "message": "matrix[r][c] — доступ к элементу вложенного списка."},
    "4-21": {"type": "copy_reference_reminder", "message": "b = a не копирует список. b — это ссылка на тот же список."},
    "4-23": {"type": "indentation_reminder", "message": "is проверяет идентичность объектов, == — равенство значений."},
    "4-24": {"type": "copy_reference_reminder", "message": "copy() — поверхностная копия. Вложенные списки — общие."},
    "4-25": {"type": "copy_reference_reminder", "message": "deepcopy() — полная копия со всеми вложенными объектами."},
    "4-27": {"type": "loop_stop_reminder", "message": "while True: — бесконечный цикл, нужен break для выхода."},
    "4-28": {"type": "loop_stop_reminder", "message": "Паттерн: while True: input() if valid: break"},
    "4-29": {"type": "indentation_reminder", "message": "msg.lower() приводит строку к нижнему регистру для сравнения."},
    "4-31": {"type": "indentation_reminder", "message": "random.randint(a, b) — случайное целое от a до b включительно."},
    "5-1": {"type": "indentation_reminder", "message": "def имя(): — создаёт функцию. Весь код внутри — с отступом."},
    "5-2": {"type": "indentation_reminder", "message": "Параметры функции — переменные внутри скобок: def f(x, y):"},
    "5-3": {"type": "indentation_reminder", "message": "return возвращает значение из функции. После return код не выполняется."},
    "5-4": {"type": "indentation_reminder", "message": "dict[key] = value — добавить или изменить элемент словаря."},
    "5-7": {"type": "indentation_reminder", "message": "try: код; except: что делать при ошибке — страховка программы."},
}

count = 0
for l in lessons:
    lid = l["id"]
    if lid in syntax_map and not l.get("syntax_reminder"):
        l["syntax_reminder"] = syntax_map[lid]
        count += 1

print(f"  ✅ Added syntax_reminder to {count} lessons")

# ── 5. FIX connection_to_game duplicates ──
print("\n5. Fixing connection_to_game duplicates...")

unique_ctg = {
    "2-3": "В финальной игре randint будет кидать кубики, выбирать случайные события и определять, какой монстр появится.",
    "2-4": "Полноценная игра-угадайка — основа для финального босса. Ты уже сейчас пишешь механику угадывания!",
    "2-5": "В финальной игре for перебирает инвентарь, ходы игроков, этапы битвы — каждый раз одно и то же.",
    "2-6": "range задаёт, сколько раз повторить действие: будь то попытки в игре или количество врагов.",
    "3-9": "В финальной игре and проверяет: есть ключ И игрок у двери — два условия сразу.",
    "3-10": "В финальной игре or даёт доступ: есть пропуск ИЛИ знаешь код — уже проходишь.",
    "3-11": "В финальной игре not переворачивает условия: 'если не мёртв — можешь атаковать'.",
    "3-14": "В финальной игре for + range управляют раундами битвы, перебором врагов, циклами игры.",
    "3-15": "range(start, stop) задаёт диапазон: от первого врага до последнего, но stop не включается.",
    "3-16": "range со шагом — это 'каждый второй ход', 'каждый третий враг'. Пропускай лишнее!",
    "3-27": "В финальной игре списки — это инвентарь, список комнат и список монстров. Основа данных.",
    "3-28": "Замена элемента списка — как заменить меч на лазерный меч в инвентаре по индексу.",
    "3-33": "Сумма элементов списка пригодится для подсчёта очков, монет и здоровья в финальной игре.",
    "3-35": "Фильтрация списка — отбираем только зелья, только монстров выше 10 уровня.",
    "3-38": "Срезы списков — взять первые 3 предмета из инвентаря или топ-10 результатов.",
    "4-18": "Вложенные списки — это карта уровней: список строк, где каждая строка — список символов.",
    "4-19": "Изменение вложенных списков — как изменить клетку на карте: matrix[r][c] = новое_значение.",
    "4-20": "Перебор вложенных списков — обойти все клетки карты: for row in map: for cell in row:",
    "3-19": "В финальной игре строки — это названия комнат, имена предметов и диалоги персонажей.",
    "3-22": "f-строки — это шаблоны: 'У {hero.name} осталось {hp} здоровья'. Удобно и наглядно.",
    "3-26": "Перебор строки по символам пригодится для поиска ключевых букв или шифрования текста.",
    "4-10": "\\n в строке — как начать новую строку в диалоге: 'Строка 1\\nСтрока 2'.",
    "1-2": "В финальной игре строки — это имена героев, названия предметов и диалоги с NPC.",
    "3-2": "В финальной игре / нужно для расчёта среднего урона, дележа монет, шансов выпадения.",
    "3-3": "// пригодится, чтобы разделить 10 монет на 3 игроков поровну: 10 // 3 = 3 без остатка.",
    "3-5": "Проверка чётности через % 2 == 0 — базовая механика для 'каждый второй ход'.",
}

count_ctg = 0
for l in lessons:
    lid = l["id"]
    if lid in unique_ctg:
        old = l.get("connection_to_game", "")
        if old != unique_ctg[lid]:
            l["connection_to_game"] = unique_ctg[lid]
            count_ctg += 1

print(f"  ✅ Fixed connection_to_game for {count_ctg} lessons")

# ── SAVE ──
with open(SRC, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)
shutil.copy2(SRC, DST)
print(f"\n✅ Saved to {SRC} and {DST}")

# Summary
print(f"\n=== SUMMARY ===")
print(f"1. Practice subtask mismatches: fixed 3 lessons")
print(f"2. Find bug off-topic: fixed 5 lessons")
print(f"3. Quiz duplicate: fixed 3-5")
print(f"4. Syntax reminders: added to {count} lessons")
print(f"5. Connection_to_game: fixed {count_ctg} lessons")
