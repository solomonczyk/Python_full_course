"""
Generate lessons.json from the curriculum markdown document.

Usage: python scripts/generate_lessons.py

Parses python_quest_full_parts_1_4_learning_program.md and outputs
a complete lessons.json matching the schema used by the FastAPI backend.
"""

import json
import re
import sys
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────
_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent
_MD_PATH = _PROJECT / "stitch_python_interactive_mastery_course" / "python_quest_full_parts_1_4_learning_program.md"
_OUTPUT_PATH = _PROJECT / "api" / "app" / "data" / "lessons.json"

# ── chapter mapping per part ───────────────────────────────────────────────
#   Maps (part, lesson_num) -> chapter
PART_CHAPTERS: dict[int, dict[int, int]] = {
    1: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 2},
    2: {1: 3, 2: 3, 3: 4, 4: 4, 5: 5, 6: 5},
    3: {i: (6 if i <= 5 else 7 if i <= 13 else 8 if i <= 18 else 9 if i <= 25 else 10 if i <= 35 else 11)
        for i in range(1, 41)},
    4: {i: (12 if i <= 5 else 13 if i <= 7 else 14 if i <= 15 else 15 if i <= 22 else 16 if i <= 27 else 17)
        for i in range(1, 32)},
}

# ── character assignments per topic type ───────────────────────────────────
# Character assignments: (pattern_in_title, character)
# First match wins — ordered from most specific to most general
TOPIC_CHARACTERS: list[tuple[str, str]] = [
    ("переменные в циклах", "da"),
    ("строки база", "ksyu"),
    ("for и range", "da"),
    ("perebor strok", "da"),
    ("срезы спи", "da"),
    ("изменение влож", "va"),
    ("перебор влож", "da"),
    ("вложен", "va"),
    ("if else", "va"),
    ("while true", "va"),
    ("правильного ввод", "ksyu"),
    ("чат-бот", "da"),
    ("таск-менедж", "da"),
    ("random + while", "da"),
    # Specific topics
    ("print", "ksyu"),
    ("строк", "ksyu"),
    ("перемен", "ksyu"),
    ("input", "ksyu"),
    ("int(input", "ksyu"),
    ("арифмет", "ksyu"),
    ("сравнени", "va"),
    ("if", "va"),
    ("elif", "va"),
    ("логическ", "va"),
    ("random", "da"),
    ("игра", "da"),
    ("for", "da"),
    ("range", "da"),
    ("float", "ksyu"),
    ("деление", "ksyu"),
    ("остаток", "ksyu"),
    ("чётнос", "ksyu"),
    ("bool", "va"),
    ("состоян", "va"),
    ("коротк", "va"),
    ("and", "va"),
    ("or", "va"),
    ("not", "va"),
    ("оптимиз", "va"),
    ("диапазон", "da"),
    ("шаг", "da"),
    ("обратн", "da"),
    ("len", "ksyu"),
    ("f-стр", "ksyu"),
    ("метод", "ksyu"),
    ("индекс", "ksyu"),
    ("срез", "ksyu"),
    ("списки", "da"),
    ("замен", "da"),
    ("pop", "da"),
    ("remove", "da"),
    ("append", "da"),
    ("index", "da"),
    ("сумма", "da"),
    ("count", "da"),
    ("фильтра", "da"),
    ("insert", "da"),
    ("extend", "da"),
    ("choice", "da"),
    ("shuffle", "da"),
    ("флаг", "va"),
    ("break", "va"),
    ("максим", "va"),
    ("минимум", "va"),
    ("длина", "va"),
    ("первый", "va"),
    ("none", "va"),
    ("алгорит", "va"),
    ("join", "ksyu"),
    ("перенос", "ksyu"),
    ("распаков", "ksyu"),
    ("split", "ksyu"),
    ("map", "va"),
    ("sort", "da"),
    ("sorted", "da"),
    ("key", "va"),
    ("ссылки", "va"),
    ("изменяе", "va"),
    ("is", "va"),
    ("copy", "ksyu"),
    ("deepcopy", "ksyu"),
    ("while", "va"),
]

# ── quiz templates per topic ───────────────────────────────────────────────
# Fallback: if no specific template matches, generate a generic one
QUIZ_TEMPLATES: list[tuple[re.Pattern, str, list[tuple[str, bool]]]] = [
    (re.compile(r"print", re.I), "Что делает функция print()?", [
        ("Выводит текст или значение на экран", True),
        ("Удаляет файл", False),
        ("Запрашивает ввод от пользователя", False),
    ]),
    (re.compile(r"строк|кавычк", re.I), "Что такое строка в Python?", [
        ("Текст в кавычках", True),
        ("Число", False),
        ("Специальный символ", False),
    ]),
    (re.compile(r"переменн", re.I), "Как создать переменную в Python?", [
        ("name = 'Python'", True),
        ("var name = 'Python'", False),
        ("let name = 'Python'", False),
    ]),
    (re.compile(r"input", re.I), "Какой тип данных возвращает input()?", [
        ("str (строка)", True),
        ("int (число)", False),
        ("bool (True/False)", False),
    ]),
    (re.compile(r"int\(input|преобра|int\(\s*input", re.I), "Зачем нужен int() вокруг input()?", [
        ("Чтобы преобразовать строку в число", True),
        ("Чтобы вывести текст на экран", False),
        ("Чтобы создать переменную", False),
    ]),
    (re.compile(r"арифмет", re.I), "Что делает оператор + в Python?", [
        ("Складывает числа", True),
        ("Умножает числа", False),
        ("Делит числа", False),
    ]),
    (re.compile(r"сравнени|больше|меньше", re.I), "Что возвращает операция сравнения?", [
        ("True или False", True),
        ("Число", False),
        ("Строку", False),
    ]),
    (re.compile(r"\bif\b(?!.*else)", re.I), "Когда выполняется код внутри if?", [
        ("Когда условие истинно (True)", True),
        ("Когда условие ложно (False)", False),
        ("Всегда", False),
    ]),
    (re.compile(r"if else|if.else", re.I), "Когда выполняется блок else?", [
        ("Когда условие if ложно", True),
        ("Когда условие if истинно", False),
        ("Всегда после if", False),
    ]),
    (re.compile(r"elif", re.I), "Сколько условий можно проверить с помощью elif?", [
        ("Сколько угодно", True),
        ("Только одно", False),
        ("Максимум два", False),
    ]),
    (re.compile(r"логическ|цепочк", re.I), "Что такое логическая цепочка?", [
        ("Несколько условий, проверяемых по порядку", True),
        ("Одно условие", False),
        ("Математическая формула", False),
    ]),
    (re.compile(r"random\.randint|random", re.I), "Что возвращает random.randint(a, b)?", [
        ("Случайное целое число от a до b", True),
        ("Случайное вещественное число", False),
        ("Случайную строку", False),
    ]),
    (re.compile(r"игра", re.I), "Что нужно импортировать для работы со случайными числами?", [
        ("import random", True),
        ("import math", False),
        ("import game", False),
    ]),
    (re.compile(r"\bfor\b", re.I), "Сколько раз выполнится цикл for i in range(5)?", [
        ("5 раз", True),
        ("4 раза", False),
        ("6 раз", False),
    ]),
    (re.compile(r"\brange\b", re.I), "Что создаёт функция range(3)?", [
        ("Последовательность 0, 1, 2", True),
        ("Последовательность 1, 2, 3", False),
        ("Число 3", False),
    ]),
    (re.compile(r"float", re.I), "Какой тип у числа 3.14 в Python?", [
        ("float (вещественное число)", True),
        ("int (целое число)", False),
        ("str (строка)", False),
    ]),
    (re.compile(r"деление", re.I), "Что вернёт выражение 7 / 2?", [
        ("3.5 (вещественное число)", True),
        ("3 (целое число)", False),
        ("Ошибку", False),
    ]),
    (re.compile(r"остаток|%|чётность", re.I), "Что вернёт выражение 7 % 2?", [
        ("1 (остаток от деления)", True),
        ("3", False),
        ("0", False),
    ]),
    (re.compile(r"bool|правда|ложь", re.I), "Сколько значений у типа bool?", [
        ("Два: True и False", True),
        ("Одно: True", False),
        ("Три: True, False и None", False),
    ]),
    (re.compile(r"\band\b", re.I), "Когда условие с and истинно?", [
        ("Когда обе части истинны", True),
        ("Когда хотя бы одна часть истинна", False),
        ("Когда обе части ложны", False),
    ]),
    (re.compile(r"\bor\b(?!.*\bnot\b)", re.I), "Когда условие с or истинно?", [
        ("Когда хотя бы одна часть истинна", True),
        ("Когда обе части истинны", False),
        ("Когда обе части ложны", False),
    ]),
    (re.compile(r"\bnot\b", re.I), "Что делает оператор not?", [
        ("Инвертирует значение (True → False)", True),
        ("Удваивает значение", False),
        ("Проверяет наличие значения", False),
    ]),
    (re.compile(r"оптимиз", re.I), "Для чего нужна оптимизация if?", [
        ("Чтобы сократить громоздкие конструкции", True),
        ("Чтобы программа работала быстрее", False),
        ("Чтобы добавить больше условий", False),
    ]),
    (re.compile(r"вложенны[хй] if|вложенны[хй] услов", re.I), "Что такое вложенный if?", [
        ("If внутри другого if", True),
        ("If после else", False),
        ("Несколько if подряд", False),
    ]),
    (re.compile(r"for.*range|range.*for", re.I), "Что делает цикл for?", [
        ("Повторяет код заданное количество раз", True),
        ("Проверяет условие один раз", False),
        ("Создаёт новую переменную", False),
    ]),
    (re.compile(r"диапазон|range\(start|start.*stop", re.I), "Что делает range(2, 5)?", [
        ("Генерирует числа 2, 3, 4", True),
        ("Генерирует числа 2, 3, 4, 5", False),
        ("Генерирует числа 0, 1, 2", False),
    ]),
    (re.compile(r"шаг.*range|range.*шаг", re.I), "Что вернёт range(0, 10, 2)?", [
        ("0, 2, 4, 6, 8", True),
        ("0, 2, 4, 6, 8, 10", False),
        ("2, 4, 6, 8", False),
    ]),
    (re.compile(r"обратн.*ход|reversed|наоборот", re.I), "Как перебрать числа от 5 до 1?", [
        ("range(5, 0, -1)", True),
        ("range(1, 5)", False),
        ("range(5, 1)", False),
    ]),
    (re.compile(r"строк.*база|строки\b|str", re.I), "Что из этого является строкой?", [
        ("'Привет'", True),
        ("123", False),
        ("True", False),
    ]),
    (re.compile(r"\bin\b", re.I), "Что проверяет оператор in?", [
        ("Есть ли элемент в строке или списке", True),
        ("Равны ли два элемента", False),
        ("Больше ли один элемент другого", False),
    ]),
    (re.compile(r"\blen\b", re.I), "Что возвращает функция len()?", [
        ("Количество элементов в объекте", True),
        ("Длину самого длинного элемента", False),
        ("Сумму всех элементов", False),
    ]),
    (re.compile(r"f-стр|f string|формат", re.I), "Что делает f-строка?", [
        ("Подставляет значения переменных в текст", True),
        ("Форматирует числа", False),
        ("Создаёт новую строку", False),
    ]),
    (re.compile(r"метод.*строк|строк.*метод", re.I), "Что делают строковые методы?", [
        ("Преобразуют или анализируют строку", True),
        ("Изменяют тип данных", False),
        ("Создают новую переменную", False),
    ]),
    (re.compile(r"индекс", re.I), "Какой индекс у первого символа строки?", [
        ("0", True),
        ("1", False),
        ("-1", False),
    ]),
    (re.compile(r"срез|slice", re.I), "Что вернёт 'Python'[0:3]?", [
        ("'Pyt'", True),
        ("'Pyth'", False),
        ("'ython'", False),
    ]),
    (re.compile(r"перебор строк|итерация.*строк", re.I), "Как перебрать все символы строки?", [
        ("for ch in 'строка':", True),
        ("for i in range(5):", False),
        ("while ch in 'строка':", False),
    ]),
    (re.compile(r"списк.*база|списки\b", re.I), "Какой индекс у первого элемента списка?", [
        ("0", True),
        ("1", False),
        ("-1", False),
    ]),
    (re.compile(r"замен.*элемент|изменен.*списк", re.I), "Как изменить элемент списка?", [
        ("spisok[0] = новое_значение", True),
        ("spisok[0] == новое_значение", False),
        ("spisok[0] = новое_значение()", False),
    ]),
    (re.compile(r"pop", re.I), "Что делает метод pop()?", [
        ("Удаляет и возвращает элемент по индексу", True),
        ("Удаляет элемент по значению", False),
        ("Добавляет элемент в конец", False),
    ]),
    (re.compile(r"remove", re.I), "Что делает метод remove()?", [
        ("Удаляет первый элемент с указанным значением", True),
        ("Удаляет элемент по индексу", False),
        ("Удаляет все элементы", False),
    ]),
    (re.compile(r"append", re.I), "Что делает метод append()?", [
        ("Добавляет элемент в конец списка", True),
        ("Добавляет элемент в начало списка", False),
        ("Удаляет последний элемент", False),
    ]),
    (re.compile(r"\bindex\b", re.I), "Что возвращает метод list.index(x)?", [
        ("Индекс первого вхождения элемента x", True),
        ("Значение элемента по индексу x", False),
        ("Количество вхождений элемента x", False),
    ]),
    (re.compile(r"сумма|подсчёт", re.I), "Как найти сумму чисел в списке?", [
        ("sum(spisok)", True),
        ("spisok.sum()", False),
        ("sum(spisok, 0)", False),
    ]),
    (re.compile(r"\bcount\b", re.I), "Что возвращает метод count()?", [
        ("Количество вхождений элемента", True),
        ("Индекс элемента", False),
        ("Сумму элементов", False),
    ]),
    (re.compile(r"фильтра", re.I), "Как оставить в списке только чётные числа?", [
        ("[x for x in nums if x % 2 == 0]", True),
        ("nums.filter(even)", False),
        ("filter(nums, even)", False),
    ]),
    (re.compile(r"insert", re.I), "Что делает spisok.insert(0, x)?", [
        ("Вставляет x на позицию 0", True),
        ("Удаляет элемент на позиции 0", False),
        ("Заменяет элемент на позиции 0", False),
    ]),
    (re.compile(r"extend", re.I), "Что делает метод extend()?", [
        ("Добавляет все элементы другого списка в конец", True),
        ("Добавляет один элемент в конец", False),
        ("Удаляет все элементы", False),
    ]),
    (re.compile(r"срезы списк", re.I), "Что вернёт [1, 2, 3, 4][1:3]?", [
        ("[2, 3]", True),
        ("[1, 2]", False),
        ("[2, 3, 4]", False),
    ]),
    (re.compile(r"choice", re.I), "Что делает random.choice(list)?", [
        ("Возвращает случайный элемент из списка", True),
        ("Выбирает первый элемент", False),
        ("Сортирует список случайным образом", False),
    ]),
    (re.compile(r"shuffle", re.I), "Что делает random.shuffle(list)?", [
        ("Перемешивает элементы списка случайным образом", True),
        ("Возвращает перемешанную копию списка", False),
        ("Сортирует список по возрастанию", False),
    ]),
    (re.compile(r"флаг|flag", re.I), "Что такое переменная-флаг?", [
        ("True/False переменная для отслеживания состояния", True),
        ("Переменная для хранения числа", False),
        ("Функция для проверки условия", False),
    ]),
    (re.compile(r"break", re.I), "Что делает оператор break?", [
        ("Немедленно завершает цикл", True),
        ("Пропускает текущую итерацию", False),
        ("Завершает программу", False),
    ]),
    (re.compile(r"максимум|max", re.I), "Как найти максимальное число в списке?", [
        ("max(spisok)", True),
        ("spisok.max()", False),
        ("maximum(spisok)", False),
    ]),
    (re.compile(r"минимум|min", re.I), "Как найти минимальное число в списке?", [
        ("min(spisok)", True),
        ("spisok.min()", False),
        ("minimum(spisok)", False),
    ]),
    (re.compile(r"none|ничего", re.I), "Что означает None в Python?", [
        ("Отсутствие значения", True),
        ("Ноль", False),
        ("Пустую строку", False),
    ]),
    (re.compile(r"алгорит", re.I), "Что такое алгоритмическое мышление?", [
        ("Умение разбивать задачу на шаги", True),
        ("Знание всех функций Python", False),
        ("Скорость написания кода", False),
    ]),
    (re.compile(r"join", re.I), "Что делает ' | '.join(list)?", [
        ("Соединяет элементы списка через ' | '", True),
        ("Разделяет строку по ' | '", False),
        ("Добавляет ' | ' в конец строки", False),
    ]),
    (re.compile(r"перенос|\\\\n|спецсимвол", re.I), "Что делает символ \\n в строке?", [
        ("Переносит текст на новую строку", True),
        ("Добавляет пробел", False),
        ("Удаляет предыдущий символ", False),
    ]),
    (re.compile(r"распаков", re.I), "Что делает `*` перед списком?", [
        ("Распаковывает элементы списка", True),
        ("Умножает все элементы", False),
        ("Создаёт копию списка", False),
    ]),
    (re.compile(r"split", re.I), "Что возвращает 'a b c'.split()?", [
        ("['a', 'b', 'c']", True),
        ("'a', 'b', 'c'", False),
        ("['a b c']", False),
    ]),
    (re.compile(r"map", re.I), "Что делает функция map()?", [
        ("Применяет функцию к каждому элементу последовательности", True),
        ("Создаёт карту маршрутов", False),
        ("Преобразует тип данных", False),
    ]),
    (re.compile(r"sort\b", re.I), "Что делает метод list.sort()?", [
        ("Сортирует список на месте", True),
        ("Возвращает отсортированную копию", False),
        ("Переворачивает список", False),
    ]),
    (re.compile(r"sorted\b", re.I), "Что делает функция sorted()?", [
        ("Возвращает отсортированную копию последовательности", True),
        ("Сортирует список на месте", False),
        ("Проверяет, отсортирован ли список", False),
    ]),
    (re.compile(r"while", re.I), "Когда выполняется цикл while?", [
        ("Пока условие истинно", True),
        ("Пока условие ложно", False),
        ("Только один раз", False),
    ]),
]

# ── Parsing helpers ────────────────────────────────────────────────────────

# Simple transliteration map for slugs
_TRANSLIT: dict[str, str] = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}

def slugify(title: str) -> str:
    """Generate a URL-friendly slug from a lesson title."""
    s = title.lower().strip()
    # Transliterate Cyrillic
    result = []
    for ch in s:
        result.append(_TRANSLIT.get(ch, ch))
    s = "".join(result)
    s = s.replace(" ", "-")
    s = re.sub(r"[^a-z0-9_.-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-.")
    return s.replace("._", "-").replace("_.", "-")  # clean up edge cases


def generate_subtitle(topic: str, lesson_title: str) -> str:
    """Generate a subtitle based on the lesson topic."""
    combined = f"{topic} {lesson_title}".lower()
    subtitles = [
        ("print", "Твой голос в коде"),
        ("стр", "Текст и кавычки"),
        ("перемен", "Именованные контейнеры"),
        ("input", "Диалог с программой"),
        ("int(input", "Превращаем текст в числа"),
        ("арифмет", "Сложение, вычитание и умножение"),
        ("сравн", "Больше, меньше или равно"),
        ("if else", "Выбор пути"),
        ("elif", "Множественный выбор"),
        ("if ", "Ветвление в коде"),
        ("логич", "Цепочка условий"),
        ("random", "Элемент неожиданности"),
        ("игра", "Случайность в действии"),
        ("for", "Повторение — мать учения"),
        ("range", "Генератор чисел"),
        ("float", "Числа с запятой"),
        ("деление", "Арифметика чисел"),
        ("остаток", "Остаток от деления"),
        ("чёт", "Проверка на чётность"),
        ("bool", "Правда или ложь"),
        ("состоян", "Флаги состояния"),
        ("коротк", "Сокращённая запись"),
        ("and", "Логическое И"),
        ("or", "Логическое ИЛИ"),
        ("not", "Логическое НЕ"),
        ("оптимиз", "Улучшаем условия"),
        ("влож", "Условие в условии"),
        ("шаг", "Шаг вперёд"),
        ("обрат", "Движение назад"),
        ("цикл", "Счётчики и накопление"),
        ("строки", "Работа с текстом"),
        ("in ", "Поиск в тексте"),
        ("len", "Длина объекта"),
        ("f-стр", "Подстановка значений"),
        ("метод", "Инструменты строк"),
        ("индекс", "Доступ по номеру"),
        ("срез", "Извлечение части"),
        ("списк", "Коллекции данных"),
        ("замен", "Изменение элемента"),
        ("pop", "Удаление по индексу"),
        ("remove", "Удаление по значению"),
        ("append", "Добавление в конец"),
        ("index", "Поиск по значению"),
        ("сумма", "Подсчёт элементов"),
        ("count", "Количество вхождений"),
        ("фильтр", "Отбор элементов"),
        ("insert", "Вставка элемента"),
        ("extend", "Расширение списка"),
        ("choice", "Случайный выбор"),
        ("shuffle", "Перемешивание"),
        ("флаг", "Сигнальные переменные"),
        ("break", "Прерывание цикла"),
        ("максим", "Поиск максимума"),
        ("минимум", "Поиск минимума"),
        ("длина", "Измерение длины"),
        ("первый", "Итерация с конца"),
        ("none", "Пустое значение"),
        ("алгорит", "Планирование кода"),
        ("join", "Сборка строки"),
        ("перенос", "Спецсимволы"),
        ("распаков", "Распаковка значений"),
        ("split", "Разделение строки"),
        ("map", "Преобразование данных"),
        ("sort", "Сортировка"),
        ("sorted", "Сортировка с копией"),
        ("key", "Ключ сортировки"),
        ("влож", "Матрёшка данных"),
        ("измен", "Редактирование"),
        ("ссылк", "Связи объектов"),
        ("изменя", "Изменяемость типов"),
        ("is", "Сравнение объектов"),
        ("copy", "Копирование"),
        ("deepcopy", "Глубокое копирование"),
        ("while", "Цикл с условием"),
        ("правил", "Контроль ввода"),
        ("чат-бот", "Диалоговый бот"),
        ("таск", "Менеджер задач"),
    ]
    for key, val in subtitles:
        if key in combined:
            return val
    return "Продолжаем изучать Python"


def get_character(lesson_title: str, topic: str) -> str:
    """Determine which character explains this lesson."""
    combined = f"{lesson_title} {topic}".lower()
    for pattern, char in TOPIC_CHARACTERS:
        if pattern.lower() in combined:
            return char
    return "ksyu"  # default


def generate_quiz(lesson_title: str, topic: str) -> dict | None:
    """Generate a quiz based on the lesson topic."""
    combined = f"{lesson_title} {topic}"
    for pattern, question, options in QUIZ_TEMPLATES:
        if pattern.search(combined):
            opts = []
            for i, (text, correct) in enumerate(options):
                opts.append({"id": chr(97 + i), "text": text, "correct": correct})
            return {"question": question, "options": opts}
    return None


def parse_lessons(md_text: str) -> list[dict]:
    """Parse the full markdown into lesson dicts."""

    # Split by lesson headers
    lesson_blocks = re.split(r'\n(?=## Урок \d+\.\d+)', md_text)
    lessons = []

    for block in lesson_blocks:
        block = block.strip()
        if not block or not block.startswith("## Урок "):
            continue

        # Extract lesson ID
        id_match = re.match(r"## Урок (\d+)\.(\d+)\.\s*(.+)", block)
        if not id_match:
            continue

        part = int(id_match.group(1))
        lesson_num = int(id_match.group(2))
        raw_title = id_match.group(3).strip()

        # Build lesson ID like "1-6"
        lesson_id = f"{part}-{lesson_num}"

        # Split by sections: ### 0. , ### 1. , etc.
        # After split:
        #   [0] = header (## Урок...)
        #   [1] = 0. Объяснение с примером  (explanation)
        #   [2] = 1. Мини-квиз               (skip - generated)
        #   [3] = 2. Что выведет код          (what outputs)
        #   [4] = 3. Маленькая задача         (mission)
        #   [5] = 4. Найди ошибку             (find bug)
        sections = re.split(r'\n### \d+\.\s*', block)

        explanation_text = ""
        explanation_code = ""
        explanation_output = ""
        what_code = ""
        what_correct = ""
        task_input = ""
        task_output = ""
        bug_code = ""
        bug_hint = ""

        def _extract_code_and_output(text: str) -> tuple[str, str]:
            """Extract python code block and its output from text."""
            code_match = re.search(r'```python\s*\n(.*?)```', text, re.DOTALL)
            code = code_match.group(1).strip() if code_match else ""
            output = ""
            if code_match:
                # Look for result text after the code block
                rest = text[code_match.end():].strip()
                # Output might be in the next line or after "---"
                rest = rest.split("---")[0].strip()
                # Try to extract meaningful output
                lines = [l.strip() for l in rest.split("\n") if l.strip() and "**" not in l and "#" not in l]
                # Remove common breadcrumbs
                lines = [l for l in lines if l not in ("", "---") and not l.startswith("###")]
                if lines:
                    output = lines[0]
            return code, output

        for i, section in enumerate(sections):
            section = section.strip()
            if i == 0:
                continue  # Skip header-only section

            if i == 1:
                # --- Explanation ---
                # Find **Идея:** content
                idea_match = re.search(r'\*\*Идея:\*\*\s*(.+?)(?:\n\n|\n```|$)', section, re.DOTALL)
                if idea_match:
                    explanation_text = idea_match.group(1).strip()

                # Extract code example and output
                explanation_code, explanation_output = _extract_code_and_output(section)

            elif i == 2:
                continue  # Skip quiz section

            elif i == 3:
                # --- What outputs ---
                code_match = re.search(r'```python\s*\n(.*?)```', section, re.DOTALL)
                if code_match:
                    what_code = code_match.group(1).strip()
                what_correct = estimate_what_outputs_answer(what_code)
                if what_correct and "\n" in what_correct:
                    what_correct = what_correct.split("\n")[0]  # use first output line

            elif i == 4:
                # --- Task / Mission ---
                input_match = re.search(r'\*\*Входные данные:\*\*\s*```text\s*\n(.*?)```', section, re.DOTALL)
                if input_match:
                    task_input = input_match.group(1).strip()

                output_match = re.search(r'\*\*Выходные данные:\*\*\s*```text\s*\n(.*?)```', section, re.DOTALL)
                if output_match:
                    task_output = output_match.group(1).strip()

            elif i == 5:
                # --- Find bug ---
                code_match = re.search(r'```python\s*\n(.*?)```', section, re.DOTALL)
                if code_match:
                    bug_code = code_match.group(1).strip()

                if bug_code:
                    parts = section.split("```")
                    if len(parts) >= 3:
                        hint_text = parts[2].strip()
                        hint_text = re.sub(r'\n---.*$', '', hint_text, flags=re.DOTALL).strip()
                        bug_hint = hint_text
                if not bug_hint:
                    bug_hint = "Найди ошибку в этом коде и исправь её."

        # Skip if no content was extracted
        if not explanation_text and not explanation_code:
            continue

        # Determine character
        character = get_character(raw_title, raw_title)

        # Generate subtopic/topic
        topic = raw_title.lower().split(" ")[0] if raw_title else lesson_id

        # Generate subtitle
        subtitle = generate_subtitle(raw_title, raw_title)

        # Build explanation output
        if not explanation_output and explanation_code:
            # Try to derive output from the code
            explanation_output = derive_code_output(explanation_code)

        # Generate quiz
        quiz = generate_quiz(raw_title, raw_title)
        if not quiz:
            # Fallback quiz
            quiz = {
                "question": f"Что изучается в уроке «{raw_title}»?",
                "options": [
                    {"id": "a", "text": raw_title.split(" ")[0] if " " in raw_title else raw_title, "correct": True},
                    {"id": "b", "text": "Другая тема", "correct": False},
                    {"id": "c", "text": "Пока не знаю", "correct": False},
                ]
            }

        # Build what_outputs
        what_outputs = None
        if what_code:
            # Generate answer options
            options = generate_what_outputs_options(what_code, what_correct)
            what_outputs = {
                "code": what_code,
                "options": options,
                "correct": what_correct or options[0] if options else what_code.split("\n")[-1] if what_code else ""
            }

        # Build find_bug
        find_bug = None
        if bug_code:
            bug_desc = "В этом коде есть ошибка. Найди и исправь её."
            # Make description more specific based on content
            if re.search(r'кавычк|пропущен.*кавычк', bug_hint, re.I):
                bug_desc = "Этот код вызовет ошибку. Почему?"
            elif re.search(r'int\(.*input|input.*int|преобразова', bug_hint, re.I):
                bug_desc = "Почему этот код не складывает числа?"
            elif re.search(r'двоеточи', bug_hint, re.I):
                bug_desc = "Чего не хватает в этом коде?"
            elif re.search(r'отступ', bug_hint, re.I):
                bug_desc = "Проблема с форматированием кода. Что не так?"
            elif re.search(r'кавычк.*строк|cannot concatenate|typeerror', bug_hint, re.I):
                bug_desc = "Почему типы данных не совпадают?"
            elif re.search(r'переменн.*созда|nameerror|не определ', bug_hint, re.I) or 'NameError' in bug_hint:
                bug_desc = "Этот код вызовет NameError. Почему?"
            elif re.search(r'indexerror|выход.*предел|индекс', bug_hint, re.I):
                bug_desc = "Этот код вызовет IndexError. Почему?"
            elif re.search(r'return|верну', bug_hint, re.I):
                bug_desc = "Функция не возвращает результат. Почему?"
            elif re.search(r'import|импорт|подключ', bug_hint, re.I):
                bug_desc = "Чего не хватает для работы кода?"
            elif re.search(r'guess|угада', bug_hint, re.I):
                bug_desc = "Почему код работает не так, как ожидается?"
            elif re.search(r'равенств|== |присваив|сравн|надо.*=', bug_hint, re.I):
                bug_desc = "В этом коде перепутаны == и =. Найди ошибку."

            find_bug = {
                "description": bug_desc,
                "code": bug_code,
                "hint": bug_hint
            }

        # Build mission
        mission_character = "da" if character != "da" else character
        mission = None
        if task_output:
            mission = {
                "title": f"Миссия: {raw_title.split(':')[0] if ':' in raw_title else raw_title}",
                "description": f"Напиши программу по теме урока «{raw_title}»",
                "task": f"Напиши программу, которая выводит следующий результат:",
                "expected_output": task_output if "\n" not in task_output else task_output.split("\n")[0],
                "character": mission_character
            }

        # Chapter mapping
        chapter = PART_CHAPTERS.get(part, {}).get(lesson_num, 1)

        lesson = {
            "id": lesson_id,
            "part": part,
            "chapter": chapter,
            "lesson": lesson_num,
            "slug": slugify(raw_title),
            "title": raw_title,
            "subtitle": subtitle,
            "topic": topic,
            "locked": False,
            "explanation": {
                "text": explanation_text,
                "character": character,
                "code_example": explanation_code,
                "output": explanation_output,
            },
            "quiz": quiz,
            "what_outputs": what_outputs,
            "find_bug": find_bug,
            "mission": mission,
        }

        lessons.append(lesson)

    return lessons


def derive_code_output(code: str) -> str:
    """Derive expected output from a Python code snippet by executing it."""
    import io
    import contextlib

    if not code or "input(" in code:
        return ""

    try:
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            exec(code, {"__builtins__": __builtins__})
        result = f.getvalue().strip()
        return result
    except Exception:
        return ""


def estimate_what_outputs_answer(code: str) -> str:
    """Estimate what the 'what outputs' code would print by executing it."""
    if not code or "input(" in code:
        return ""
    try:
        import io
        import contextlib
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            exec(code, {"__builtins__": __builtins__})
        return f.getvalue().strip()
    except Exception:
        return ""


def generate_what_outputs_options(code: str, correct: str) -> list[str]:
    """Generate plausible multiple-choice options for 'what outputs'."""
    if not correct:
        return []

    # Build distractors based on the correct answer
    common_wrong: list[str] = []
    c = correct.strip()

    if c.isdigit():
        n = int(c)
        common_wrong = [str(n + 1), str(n - 1)] if n > 1 else [str(n + 1), str(n + 2)]
    elif c == "True":
        common_wrong = ["False", "None"]
    elif c == "False":
        common_wrong = ["True", "None"]
    elif c in ("0", "1"):
        common_wrong = ["True", "False"]
    elif c.isalpha():
        common_wrong = ["Ошибка", "None"]
    else:
        common_wrong = ["Ошибка", "None"]

    options = [c]
    for w in common_wrong:
        if w != c and w not in options:
            options.append(w)
        if len(options) >= 3:
            break
    while len(options) < 3:
        options.append("Ошибка")

    return options[:3]


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    # Ensure UTF-8 output for Windows console
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")  # type: ignore
        except Exception:
            pass

    if not _MD_PATH.exists():
        print(f"ERROR: Markdown file not found at {_MD_PATH}")
        sys.exit(1)

    print(f"Reading curriculum from {_MD_PATH}")
    md_text = _MD_PATH.read_text(encoding="utf-8")

    print("Parsing lessons...")
    lessons = parse_lessons(md_text)
    print(f"Parsed {len(lessons)} lessons")

    # Output as JSON
    output = json.dumps(lessons, ensure_ascii=False, indent=2)
    _OUTPUT_PATH.write_text(output, encoding="utf-8")
    print(f"Written to {_OUTPUT_PATH}")

    # Summary
    parts = set(l["part"] for l in lessons)
    for p in sorted(parts):
        p_lessons = [l for l in lessons if l["part"] == p]
        print(f"  Part {p}: {len(p_lessons)} lessons")
        for l in p_lessons:
            has_quiz = "+" if l.get("quiz") else "-"
            has_wo = "+" if l.get("what_outputs") else "-"
            has_bug = "+" if l.get("find_bug") else "-"
            has_mission = "+" if l.get("mission") else "-"
            print(f"    {l['id']}: {l['title']}  Q:{has_quiz} W:{has_wo} B:{has_bug} M:{has_mission}")


if __name__ == "__main__":
    main()
