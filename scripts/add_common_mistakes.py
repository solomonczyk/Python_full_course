#!/usr/bin/env python3
"""Add common_mistakes data to lessons 3-27 through 3-41."""
import json

FILE = "backend/app/data/lessons.json"

with open(FILE, "r", encoding="utf-8") as f:
    lessons = json.load(f)

mistakes_map = {
    "3-27": [
        {"title": "Забыл квадратные скобки", "wrong": "items = \"меч\", \"щит\"\nprint(items)", "right": "items = [\"меч\", \"щит\"]\nprint(items)", "note": "Без [] Python создаёт кортеж (tuple), а не список. Всегда используй квадратные скобки для списка."},
        {"title": "Думает, что первый элемент — индекс 1", "wrong": "items = [\"меч\", \"щит\"]\nprint(items[1])", "right": "items = [\"меч\", \"щит\"]\nprint(items[0])", "note": "В Python индексация начинается с 0. Первый элемент — items[0], второй — items[1]."},
    ],
    "3-28": [
        {"title": "Пытается заменить элемент без индекса", "wrong": "items = [\"меч\", \"щит\"]\nitems = \"новый меч\"", "right": "items = [\"меч\", \"щит\"]\nitems[0] = \"новый меч\"\nprint(items)", "note": "Чтобы заменить элемент списка, укажи индекс в квадратных скобках: items[0] = новое_значение."},
        {"title": "Выходит за границы списка при замене", "wrong": "items = [\"меч\", \"щит\"]\nitems[5] = \"шлем\"", "right": "items = [\"меч\", \"щит\"]\nitems.append(\"шлем\")", "note": "Нельзя заменить элемент по индексу, которого нет. Чтобы добавить новый — используй append()."},
    ],
    "3-29": [
        {"title": "Вызывает pop() на пустом списке", "wrong": "items = []\nitems.pop()", "right": "items = []\nif items:\n    items.pop()", "note": "pop() на пустом списке вызывает IndexError. Всегда проверяй, что список не пуст."},
        {"title": "Путает pop() с remove()", "wrong": "items = [\"меч\", \"щит\"]\nitems.pop(\"щит\")", "right": "items = [\"меч\", \"щит\"]\nitems.remove(\"щит\")\nprint(items)", "note": "pop() удаляет по индексу, а remove() — по значению."},
    ],
    "3-30": [
        {"title": "Удаляет несуществующий элемент", "wrong": "items = [\"меч\", \"щит\"]\nitems.remove(\"шлем\")", "right": "items = [\"меч\", \"щит\"]\nif \"шлем\" in items:\n    items.remove(\"шлем\")", "note": "remove() вызывает ValueError, если элемента нет. Проверяй через in перед удалением."},
        {"title": "Думает, что remove() удаляет все вхождения", "wrong": "items = [\"болт\", \"гайка\", \"болт\"]\nitems.remove(\"болт\")\nprint(items)", "right": "items = [x for x in items if x != \"болт\"]\nprint(items)", "note": "remove() удаляет только ПЕРВОЕ вхождение. Чтобы удалить все — используй list comprehension."},
    ],
    "3-31": [
        {"title": "Присваивает результат append() переменной", "wrong": "items = []\nitems = items.append(\"ключ\")", "right": "items = []\nitems.append(\"ключ\")\nprint(items)", "note": "append() изменяет список на месте и возвращает None. Не присваивай результат обратно."},
        {"title": "Пытается добавить несколько элементов за раз", "wrong": "items = []\nitems.append(\"меч\", \"щит\")", "right": "items = []\nitems.append(\"меч\")\nitems.append(\"щит\")\nprint(items)", "note": "append() принимает только один аргумент."},
    ],
    "3-32": [
        {"title": "Ищет несуществующий элемент", "wrong": "items = [\"меч\", \"щит\"]\nprint(items.index(\"шлем\"))", "right": "items = [\"меч\", \"щит\"]\nif \"шлем\" in items:\n    print(items.index(\"шлем\"))\nelse:\n    print(-1)", "note": "index() вызывает ValueError, если элемента нет. Сначала проверяй через in."},
        {"title": "Путает — передаёт индекс вместо значения", "wrong": "items = [\"меч\", \"щит\"]\nprint(items.index(1))", "right": "items = [\"меч\", \"щит\"]\nprint(items[1])", "note": "index(value) ищет ПО ЗНАЧЕНИЮ и возвращает индекс. items[индекс] получает значение по индексу."},
    ],
    "3-33": [
        {"title": "Пытается сложить строки через sum()", "wrong": "words = [\"a\", \"b\", \"c\"]\nprint(sum(words))", "right": "words = [\"a\", \"b\", \"c\"]\nprint(\"\".join(words))", "note": "sum() работает только с числами. Для строк используй метод join()."},
        {"title": "Забыл инициализировать сумму в цикле", "wrong": "numbers = [1, 2, 3]\nfor n in numbers:\n    total += n", "right": "numbers = [1, 2, 3]\ntotal = 0\nfor n in numbers:\n    total += n\nprint(total)", "note": "Перед циклом с накоплением создай total = 0, иначе Python выдаст NameError."},
    ],
    "3-34": [
        {"title": "Вызывает count() как функцию, а не метод", "wrong": "items = [1, 2, 1, 3]\nprint(count(1))", "right": "items = [1, 2, 1, 3]\nprint(items.count(1))", "note": "count() — метод списка. Вызывай через точку: список.count(значение)."},
        {"title": "Путает count() с len()", "wrong": "items = [1, 2, 3]\nprint(items.count())", "right": "items = [1, 2, 3]\nprint(len(items))", "note": "count(значение) считает вхождения элемента. len(список) возвращает длину списка."},
    ],
    "3-35": [
        {"title": "Путает порядок в list comprehension", "wrong": "nums = [1, 2, 3, 4]\nevens = [if n % 2 == 0 for n in nums]", "right": "nums = [1, 2, 3, 4]\nevens = [n for n in nums if n % 2 == 0]\nprint(evens)", "note": "Порядок: [выражение for элемент in список if условие]. Сначала пиши for, потом if."},
        {"title": "Забывает квадратные скобки", "wrong": "nums = [1, 2, 3, 4]\nresult = (n for n in nums if n > 2)", "right": "nums = [1, 2, 3, 4]\nresult = [n for n in nums if n > 2]\nprint(result)", "note": "Круглые скобки создают генератор, а не список. Используй квадратные [] для списка."},
    ],
    "3-36": [
        {"title": "Забывает передать значение для вставки", "wrong": "items = [\"меч\", \"щит\"]\nitems.insert(1)", "right": "items = [\"меч\", \"щит\"]\nitems.insert(1, \"шлем\")\nprint(items)", "note": "insert() требует два аргумента: индекс и значение."},
        {"title": "Путает insert(-1, x) с добавлением в конец", "wrong": "items = [\"меч\", \"щит\"]\nitems.insert(-1, \"шлем\")\nprint(items)", "right": "items = [\"меч\", \"щит\"]\nitems.append(\"шлем\")\nprint(items)", "note": "insert(-1, x) вставляет ПЕРЕД последним элементом. Для добавления в конец используй append()."},
    ],
    "3-37": [
        {"title": "Передаёт число, а не коллекцию", "wrong": "a = [1, 2]\na.extend(3)", "right": "a = [1, 2]\na.append(3)\nprint(a)", "note": "extend() ожидает коллекцию (список, строку). Для одного элемента используй append()."},
        {"title": "Не учитывает, что extend разбивает строку", "wrong": "a = [1, 2]\na.extend(\"abc\")\nprint(a)", "right": "a = [1, 2]\na.append(\"abc\")\nprint(a)", "note": "extend(\"abc\") разобьёт строку на символы. Чтобы добавить строку целиком, используй append()."},
    ],
    "3-38": [
        {"title": "Думает, что конечный индекс входит в срез", "wrong": "a = [10, 20, 30, 40]\nprint(a[1:3])", "right": "a = [10, 20, 30, 40]\nprint(a[1:3])", "note": "Срез [start:end] не включает элемент с индексом end. a[1:3] даёт элементы с индексами 1 и 2 (20, 30)."},
        {"title": "Путает синтаксис среза с функцией", "wrong": "a = [10, 20, 30, 40]\nprint(a.slice(1, 3))", "right": "a = [10, 20, 30, 40]\nprint(a[1:3])", "note": "В Python срезы пишутся через квадратные скобки и двоеточие: список[старт:конец]."},
    ],
    "3-39": [
        {"title": "Забыл import random", "wrong": "items = [\"меч\", \"щит\"]\nprint(random.choice(items))", "right": "import random\nitems = [\"меч\", \"щит\"]\nprint(random.choice(items))", "note": "Модуль random нужно импортировать до использования."},
        {"title": "Вызывает choice() на пустом списке", "wrong": "items = []\nprint(random.choice(items))", "right": "items = []\nif items:\n    print(random.choice(items))\nelse:\n    print(\"Список пуст\")", "note": "random.choice() выдаёт IndexError на пустом списке. Проверяй, что список не пуст."},
    ],
    "3-40": [
        {"title": "Присваивает результат shuffle() переменной", "wrong": "import random\ncards = [1, 2, 3]\nshuffled = random.shuffle(cards)\nprint(shuffled)", "right": "import random\ncards = [1, 2, 3]\nrandom.shuffle(cards)\nprint(cards)", "note": "shuffle() перемешивает на месте и возвращает None. Выводи сам список, а не результат."},
        {"title": "Не копирует список, теряя оригинальный порядок", "wrong": "import random\noriginal = [1, 2, 3, 4, 5]\nrandom.shuffle(original)", "right": "import random\noriginal = [1, 2, 3, 4, 5]\nshuffled = original.copy()\nrandom.shuffle(shuffled)", "note": "shuffle() меняет исходный список. Сохрани копию через .copy() до перемешивания."},
    ],
    "3-41": [
        {"title": "Смешивает табуляцию и пробелы", "wrong": "if True:\n    print(1)\n\tprint(2)", "right": "if True:\n    print(1)\n    print(2)", "note": "Нельзя смешивать табуляцию и пробелы. Используй 4 пробела — это стандарт Python."},
        {"title": "Забыл двоеточие после if/for/while", "wrong": "x = 5\nif x > 0\n    print(\"Положительное\")", "right": "x = 5\nif x > 0:\n    print(\"Положительное\")", "note": "После if, for, while, def обязательно ставится двоеточие :. Без него Python не понимает, где блок."},
        {"title": "Разные отступы внутри одного блока", "wrong": "if True:\n    print(1)\n      print(2)", "right": "if True:\n    print(1)\n    print(2)", "note": "Все строки внутри блока должны иметь одинаковый отступ. 4 пробела для каждой строки."},
    ],
}

count = 0
for l in lessons:
    lid = l["id"]
    if lid in mistakes_map:
        l["common_mistakes"] = mistakes_map[lid]
        count += 1
        print(f"  {lid}: added {len(mistakes_map[lid])} mistakes")

with open(FILE, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

print(f"Added common_mistakes to {count} lessons")
