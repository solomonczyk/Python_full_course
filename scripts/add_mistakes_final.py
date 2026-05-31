#!/usr/bin/env python3
"""Add common_mistakes to remaining 38 lessons."""
import json, shutil

SRC = "backend/app/data/lessons.json"
DST = "api/app/data/lessons.json"

with open(SRC, "r", encoding="utf-8") as f:
    lessons = json.load(f)

mistakes = {
    "1-5": [
        {"title": "Забыл int() для input", "wrong": 'age = input("Сколько лет? ")\nprint(age + 1)', "right": 'age = int(input("Сколько лет? "))\nprint(age + 1)', "note": "input() всегда возвращает строку. Чтобы считать число — оберни в int()."},
        {"title": "Конкатенация строки и числа", "wrong": 'print("Мне " + 10 + " лет")', "right": 'print("Мне " + str(10) + " лет")', "note": "Нельзя сложить строку и число. Преобразуй число в строку через str()."},
    ],
    "3-9": [
        {"title": "Путает and с or", "wrong": "age = 20\nhas_ticket = False\nif age >= 18 or has_ticket:\n    print('Вход разрешён')", "right": "age = 20\nhas_ticket = False\nif age >= 18 and has_ticket:\n    print('Вход разрешён')", "note": "and требует, чтобы ОБА условия были True. or — хотя бы ОДНО."},
        {"title": "Слишком много and", "wrong": "if x > 0 and x != 0:", "right": "if x > 0:", "note": "x > 0 уже подразумевает x != 0. Не усложняй."},
    ],
    "4-1": [
        {"title": "Флаг никогда не сбрасывается", "wrong": "found = False\nfor item in items:\n    if item == target:\n        found = True\n    else:\n        found = False", "right": "found = False\nfor item in items:\n    if item == target:\n        found = True\n        break", "note": "Флаг нашли — не сбрасывай его обратно. Добавь break для выхода."},
        {"title": "Путает флаг со счётчиком", "wrong": "flag = 0\nif условие:\n    flag = 1", "right": "flag = False\nif условие:\n    flag = True", "note": "Флаг — это bool: True или False. Не используй 0 и 1."},
    ],
    "4-2": [
        {"title": "break до вывода результата", "wrong": "for n in range(10):\n    break\n    print(n)", "right": "for n in range(10):\n    print(n)\n    if n == 5:\n        break", "note": "break завершает цикл немедленно. Весь код после break в цикле не выполнится."},
        {"title": "break вне цикла", "wrong": "if x > 5:\n    break", "right": "for i in range(10):\n    if i > 5:\n        break", "note": "break работает только внутри цикла (for, while). Вне цикла — SyntaxError."},
    ],
    "4-3": [
        {"title": "Стартовое значение для максимума — 0", "wrong": "mx = 0\nfor n in numbers:\n    if n > mx:\n        mx = n", "right": "mx = numbers[0]\nfor n in numbers:\n    if n > mx:\n        mx = n\nprint(mx)", "note": "Если все числа отрицательные, mx = 0 не сработает. Инициализируй первым элементом."},
    ],
    "4-4": [
        {"title": "Стартовое значение для минимума — 0", "wrong": "mn = 0\nfor n in numbers:\n    if n < mn:\n        mn = n", "right": "mn = numbers[0]\nfor n in numbers:\n    if n < mn:\n        mn = n\nprint(mn)", "note": "Если все числа положительные, mn = 0 не сработает. Инициализируй первым элементом."},
    ],
    "4-5": [
        {"title": "Сравнивает длину строки неправильно", "wrong": "words = ['cat', 'python', 'hi']\nprint(max(words))", "right": "words = ['cat', 'python', 'hi']\nprint(max(words, key=len))", "note": "max() без key сравнивает строки лексикографически, не по длине. Используй key=len."},
    ],
    "4-6": [
        {"title": "Отрицательный индекс = -0", "wrong": "items = [10, 20, 30]\nprint(items[-0])", "right": "items = [10, 20, 30]\nprint(items[-1])", "note": "-0 это то же самое, что 0 — первый элемент. Последний элемент — это -1."},
    ],
    "4-7": [
        {"title": "Путает None с 0 или False", "wrong": "result = None\nif result == False:\n    print('нет результата')", "right": "result = None\nif result is None:\n    print('нет результата')", "note": "None — это не 0 и не False. Проверяй через is None."},
    ],
    "4-8": [
        {"title": "Пишет код без плана", "wrong": "# Алгоритм: просто начну писать\nif x > 0:\n    y = x * 2\nfor i in range(y):\n    ...", "right": "# Алгоритм:\n# 1. Считаем сумму\n# 2. Удваиваем\n# 3. Выводим\n# А теперь код:", "note": "Сначала продумай алгоритм словами — это сэкономит часы отладки."},
    ],
    "4-9": [
        {"title": "Забыл разделитель в join", "wrong": "words = ['a', 'b', 'c']\nprint(join(words))", "right": "words = ['a', 'b', 'c']\nprint(''.join(words))", "note": "join() — метод строки-разделителя, не функция. Пиши: разделитель.join(список)."},
        {"title": "Числа в join без str()", "wrong": "nums = [1, 2, 3]\nprint('-'.join(nums))", "right": "nums = [1, 2, 3]\nprint('-'.join(str(n) for n in nums))", "note": "join() работает только со строками. Числа нужно преобразовать через str()."},
    ],
    "4-10": [
        {"title": "Путает \\n с /n", "wrong": 'print("Строка 1/nСтрока 2")', "right": 'print("Строка 1\\nСтрока 2")', "note": "Экранирование — обратная косая черта \\. /n — просто слеш и буква n."},
        {"title": "Думает \\n работает в любом print", "wrong": 'print("Строка 1\\nСтрока 2", end="\\n")', "right": 'print("Строка 1\\nСтрока 2")', "note": "По умолчанию print() уже добавляет \\n в конце. Не пиши end=\\n вручную."},
    ],
    "4-11": [
        {"title": "Несовпадение количества переменных", "wrong": "a, b = [1, 2, 3]", "right": "a, b, c = [1, 2, 3]", "note": "Количество переменных слева должно равняться количеству элементов справа."},
        {"title": "Путает распаковку с индексацией", "wrong": "a, *b = [1]\nprint(a, b)", "right": "a, b = [1, 2]", "note": "*b соберёт все оставшиеся элементы. Для одного элемента без * он распакуется."},
    ],
    "4-12": [
        {"title": "split() без переменной", "wrong": 'text = "a b c"\nsplit()\nprint(text)', "right": 'text = "a b c"\nwords = text.split()\nprint(words)', "note": "split() возвращает список. Его нужно сохранить в переменную."},
    ],
    "4-13": [
        {"title": "split() без аргумента когда нужен разделитель", "wrong": 'data = "a,b,c"\nprint(data.split())', "right": 'data = "a,b,c"\nprint(data.split(","))', "note": "split() без аргумента делит по пробелам. Для запятой укажи split(',')."},
    ],
    "4-14": [
        {"title": "Забывает list() для map", "wrong": "nums = ['1', '2', '3']\nprint(map(int, nums))", "right": "nums = ['1', '2', '3']\nprint(list(map(int, nums)))", "note": "map() возвращает итератор, а не список. Оберни в list() чтобы увидеть результат."},
    ],
    "4-15": [
        {"title": "sort() без ключа возвращает None", "wrong": "nums = [3, 1, 2]\nsorted_nums = nums.sort()\nprint(sorted_nums)", "right": "nums = [3, 1, 2]\nnums.sort()\nprint(nums)", "note": "sort() сортирует на месте и возвращает None. Используй sorted() для новой переменной."},
    ],
    "4-16": [
        {"title": "Думает, что sorted() меняет исходный", "wrong": "nums = [3, 1, 2]\nsorted(nums)\nprint(nums)", "right": "nums = [3, 1, 2]\nsorted_nums = sorted(nums)\nprint(sorted_nums)", "note": "sorted() возвращает новый список, не меняя исходный. Сохрани результат в переменную."},
    ],
    "4-17": [
        {"title": "Забывает key= при сортировке", "wrong": "people = [('Аня', 25), ('Боря', 18)]\nprint(sorted(people))", "right": "people = [('Аня', 25), ('Боря', 18)]\nprint(sorted(people, key=lambda x: x[1]))", "note": "Без key sorted() сравнивает по первому элементу. Укажи key= для другого критерия."},
    ],
    "4-18": [
        {"title": "Путает индексы во вложенных списках", "wrong": "matrix = [[1, 2], [3, 4]]\nprint(matrix[1][0])", "right": "matrix = [[1, 2], [3, 4]]\nprint(matrix[1][0])", "note": "matrix[1][0] — сначала выбираем строку [1], потом элемент [0] внутри неё = 3."},
    ],
    "4-19": [
        {"title": "Пытается изменить вложенный список через запятую", "wrong": "matrix = [[1, 2], [3, 4]]\nmatrix[0, 1] = 9", "right": "matrix = [[1, 2], [3, 4]]\nmatrix[0][1] = 9\nprint(matrix)", "note": "Доступ к вложенным элементам: список[строка][столбец], а не список[строка, столбец]."},
    ],
    "4-20": [
        {"title": "Один цикл вместо двух", "wrong": "matrix = [[1, 2], [3, 4]]\nfor row in matrix:\n    print(row)", "right": "matrix = [[1, 2], [3, 4]]\nfor row in matrix:\n    for item in row:\n        print(item)", "note": "print(row) выводит список целиком. Нужен вложенный цикл для каждого элемента."},
    ],
    "4-21": [
        {"title": "Путает присваивание с копированием", "wrong": "a = [1, 2, 3]\nb = a\na.append(4)\nprint(b)", "right": "a = [1, 2, 3]\nb = a.copy()\na.append(4)\nprint(b)", "note": "b = a не копирует список. b — это ссылка на тот же список. Используй copy()."},
    ],
    "4-22": [
        {"title": "Пытается изменить строку по индексу", "wrong": 's = "Python"\ns[0] = "J"', "right": 's = "Python"\ns = "J" + s[1:]\nprint(s)', "note": "Строки неизменяемы (immutable). Нельзя присвоить значение по индексу. Создай новую строку."},
    ],
    "4-23": [
        {"title": "Использует is для сравнения чисел", "wrong": "if x is 5:", "right": "if x == 5:", "note": "is проверяет идентичность объектов. Для сравнения значений используй ==."},
    ],
    "4-24": [
        {"title": "Думает, что copy() копирует всё", "wrong": "a = [[1, 2], [3, 4]]\nb = a.copy()\na[0].append(5)\nprint(b)", "right": "from copy import deepcopy\na = [[1, 2], [3, 4]]\nb = deepcopy(a)\na[0].append(5)\nprint(b)", "note": "copy() — поверхностная копия. Вложенные списки всё ещё общие. Используй deepcopy()."},
    ],
    "4-25": [
        {"title": "Забыл импортировать deepcopy", "wrong": "a = [[1, 2], [3, 4]]\nb = deepcopy(a)", "right": "from copy import deepcopy\na = [[1, 2], [3, 4]]\nb = deepcopy(a)", "note": "deepcopy() живёт в модуле copy. Не забудь импортировать."},
    ],
    "4-26": [
        {"title": "Забыл обновить счётчик — бесконечный цикл", "wrong": "i = 0\nwhile i < 5:\n    print(i)", "right": "i = 0\nwhile i < 5:\n    print(i)\n    i += 1", "note": "Без i += 1 условие никогда не станет False — цикл бесконечный. Нажми Ctrl+C для спасения."},
    ],
    "4-27": [
        {"title": "while True без break", "wrong": "while True:\n    print('бесконечно')", "right": "while True:\n    cmd = input('> ')\n    if cmd == 'выход':\n        break", "note": "while True без break — бесконечный цикл. Всегда предусматривай условие выхода."},
    ],
    "4-28": [
        {"title": "Не обновляет input внутри цикла", "wrong": "guess = int(input())\nwhile guess != secret:\n    print('Не угадал')", "right": "guess = 0\nwhile guess != secret:\n    guess = int(input())\n    if guess != secret:\n        print('Не угадал')", "note": "Если input() вне цикла, число будет проверяться вечно. Читай ввод внутри while."},
    ],
    "4-29": [
        {"title": "Не учитывает регистр", "wrong": "if msg == 'привет':\n    print('бот: Привет!')", "right": "if msg.lower() == 'привет':\n    print('бот: Привет!')", "note": "Python различает 'Привет' и 'привет'. Используй .lower() для регистронезависимости."},
    ],
    "4-30": [
        {"title": "Перезаписывает список вместо добавления", "wrong": "tasks = []\ntasks = 'купить хлеб'", "right": "tasks = []\ntasks.append('купить хлеб')\nprint(tasks)", "note": "tasks = 'купить хлеб' заменит список на строку. Используй append()."},
    ],
    "4-31": [
        {"title": "Не обновляет попытки", "wrong": "attempts = 3\nwhile attempts > 0:\n    guess = int(input())\n    if guess != secret:\n        print('Неверно')", "right": "attempts = 3\nwhile attempts > 0:\n    guess = int(input())\n    if guess != secret:\n        attempts -= 1\n        print(f'Осталось {attempts}')", "note": "Без attempts -= 1 количество попыток не уменьшается. Цикл будет бесконечным."},
        {"title": "Путает random.randint с random.choice", "wrong": "secret = random.choice([1, 2, 3])", "right": "secret = random.randint(1, 10)", "note": "randint(a, b) — случайное ЧИСЛО от a до b. choice — случайный элемент из списка."},
    ],
    "5-1": [
        {"title": "Забыл двоеточие после def", "wrong": "def greet()\n    print('Привет')", "right": "def greet():\n    print('Привет')", "note": "После def обязательно двоеточие — как после if или for."},
        {"title": "Вызывает функцию до её определения", "wrong": "greet()\ndef greet():\n    print('Привет')", "right": "def greet():\n    print('Привет')\ngreet()", "note": "Python выполняет код сверху вниз. Сначала определи функцию, потом вызывай."},
    ],
    "5-2": [
        {"title": "Забыл передать аргумент", "wrong": "def square(x):\n    print(x * x)\nsquare()", "right": "def square(x):\n    print(x * x)\nsquare(5)", "note": "Функция ожидает аргумент. Если не передать — TypeError."},
    ],
    "5-3": [
        {"title": "Код после return не выполняется", "wrong": "def calc(x):\n    return x * 2\n    print('готово')", "right": "def calc(x):\n    result = x * 2\n    print('готово')\n    return result", "note": "После return функция завершается. Если print стоит после return — он не выполнится."},
        {"title": "Забыл return — получает None", "wrong": "def add(a, b):\n    result = a + b\nprint(add(2, 3))", "right": "def add(a, b):\n    return a + b\nprint(add(2, 3))", "note": "Без return функция возвращает None. return — це отдаёт результат."},
    ],
    "5-4": [
        {"title": "Обращается к несуществующему ключу", "wrong": "hero = {'name': 'Ксю', 'hp': 100}\nprint(hero['mp'])", "right": "hero = {'name': 'Ксю', 'hp': 100}\nprint(hero.get('mp', 0))", "note": "Несуществующий ключ даёт KeyError. Используй get() со значением по умолчанию."},
        {"title": "Пытается создать dict с дублирующимся ключом", "wrong": "d = {'a': 1, 'a': 2}\nprint(d)", "right": "d = {'a': 1, 'b': 2}\nprint(d)", "note": "Дублирующийся ключ перезапишет первое значение. Ключи должны быть уникальными."},
    ],
    "5-7": [
        {"title": "Ловит слишком общее исключение", "wrong": "try:\n    x = int(input())\nexcept:\n    print('Ошибка')", "right": "try:\n    x = int(input())\nexcept ValueError:\n    print('Это не число')", "note": "except: без типа ловит ВСЕ ошибки. Указывай конкретный тип (ValueError, TypeError)."},
        {"title": "Забыл, что после except код продолжается", "wrong": "try:\n    x = int(input())\nexcept ValueError:\n    print('Ошибка')\n    x = 0\nprint(x)", "right": "Правильно! Код после try-except работает в любом случае.", "note": "try-except не завершает программу. После except выполнение продолжается как обычно."},
    ],
}

count = 0
for l in lessons:
    lid = l["id"]
    if lid in mistakes:
        l["common_mistakes"] = mistakes[lid]
        count += 1
        print(f"✅ {lid}: added {len(mistakes[lid])} mistakes")

# Also fill any lessons with only 1 mistake (add 1 more)
add_more = {
    "1-4": {"title": "input() без переменной", "wrong": "input('Как тебя зовут?')\nprint('Привет')", "right": "name = input('Как тебя зовут?')\nprint('Привет,', name)", "note": "input() возвращает строку, но если не сохранить её в переменную — ты её потеряешь."},
    "1-6": {"title": "Ділення на 0", "wrong": "print(10 / 0)", "right": "if divisor != 0:\n    print(10 / divisor)\nelse:\n    print('На ноль делить нельзя')", "note": "Ділення на 0 дає ZeroDivisionError. Завжди перевіряй дільник."},
    "1-7": {"title": "Потрійне порівняння", "wrong": "if 5 < x < 10:", "right": "if x > 5 and x < 10:", "note": "У Python можна писати 5 < x < 10! Але новачки думають, що це не працює."},
    "2-1": {"title": "Багато if замість elif", "wrong": "if x > 0:\n    ...\nif x == 0:\n    ...\nif x < 0:\n    ...", "right": "if x > 0:\n    ...\nelif x == 0:\n    ...\nelse:", "note": "elif гарантує, що виконається тільки одна гілка. if-и можуть виконатись кілька."},
    "1-9": {"title": "Else без if", "wrong": "x = 5\nelse:\n    print('???')", "right": "if x > 0:\n    print('Плюс')\nelse:\n    print('Минус')", "note": "else використовується тільки після if або elif. Сам по собі — SyntaxError."},
}

for l in lessons:
    lid = l["id"]
    if lid in add_more and lid in mistakes:
        pts = l.get("common_mistakes", [])
        # Add the extra mistake
        pts.append(add_more[lid])
        print(f"  → {lid}: added extra mistake")

with open(SRC, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)
shutil.copy2(SRC, DST)

# Final check
with open(SRC, "r", encoding="utf-8") as f:
    lessons = json.load(f)
has = sum(1 for l in lessons if l.get("common_mistakes"))
total = sum(len(l.get("common_mistakes", [])) for l in lessons)
missing = [l["id"] for l in lessons if not l.get("common_mistakes")]
print(f"\n✅ With common_mistakes: {has}/{len(lessons)}")
print(f"✅ Total mistakes: {total}")
if missing:
    print(f"⚠️ Missing ({len(missing)}): {missing}")
else:
    print("🎉 ALL lessons have common_mistakes!")
