#!/usr/bin/env python3
"""Add code_watch data to lessons 1-8, 1-9, 2-1."""
import json, shutil

SRC = "backend/app/data/lessons.json"
DST = "api/app/data/lessons.json"

with open(SRC, "r", encoding="utf-8") as f:
    lessons = json.load(f)

for l in lessons:
    lid = l["id"]

    if lid == "1-8":
        l["code_watch"] = {
            "title": "Разбор: переменная внутри if",
            "main_code": 'x = int(input())\nif x > 0:\n    message = "Плюс"\nprint(message)',
            "dialogue": [
                {"speaker": "ksyu", "text": "Обрати внимание: в этом примере переменную `message` мы создали `внутри` `if`. А пользуемся ею снаружи!"},
                {"speaker": "novice", "text": "Ну да, создали и создали. В чём проблема?"},
                {"speaker": "ksyu", "text": "А что будет, если пользователь введёт `-5`? Условие `x > 0` не выполнится — и код внутри `if` просто не запустится."},
                {"speaker": "ksyu", "code": 'x = -5\nif x > 0:\n    message = "Плюс"\nprint(message)', "output": 'NameError: name "message" is not defined', "caption": "Что происходит при x = -5"},
                {"speaker": "novice", "text": "То есть если условие ложно, переменная `message` просто не существует? И `print(message)` упадёт?"},
                {"speaker": "ksyu", "text": "Именно! Переменной можно пользоваться снаружи `if`, только если она точно создалась внутри. Есть два хороших варианта."},
            ],
            "what_if": [
                {"description": "Пользователь вводит 5 — всё работает", "input": "5", "code": 'x = 5\nif x > 0:\n    message = "Плюс"\nprint(message)', "output": "Плюс"},
                {"description": "Пользователь вводит -3 — ошибка", "input": "-3", "code": 'x = -3\nif x > 0:\n    message = "Плюс"\nprint(message)', "output": 'NameError: name "message" is not defined'},
            ],
            "solutions": [
                {"title": "Вариант 1: значение по умолчанию", "description": "Создай переменную до if — тогда она точно существует.", "code": 'x = int(input())\nmessage = "не определено"\nif x > 0:\n    message = "Плюс"\nprint(message)'},
                {"title": "Вариант 2: используй else", "description": "В if-else выполняется ровно одна из веток — переменная создаётся.", "code": 'x = int(input())\nif x > 0:\n    message = "Плюс"\nelse:\n    message = "Минус или ноль"\nprint(message)'},
            ],
        }
        print(f"✅ Added code_watch to 1-8")

    elif lid == "1-9":
        l["code_watch"] = {
            "title": "Разбор: обе ветки — гарантия",
            "main_code": 'x = int(input())\nif x > 0:\n    status = "Плюс"\nelse:\n    status = "Минус или ноль"\nprint(status)',
            "dialogue": [
                {"speaker": "ksyu", "text": "Видишь, чем отличается этот пример от прошлого? Здесь есть `else`. И это меняет всё."},
                {"speaker": "novice", "text": "Да, теперь переменная `status` создаётся и в `if`, и в `else`. Но как это работает?"},
                {"speaker": "ksyu", "text": "Python гарантирует: выполнится ровно одна из веток — либо `if`, либо `else`. Двух одновременно — никогда!"},
                {"speaker": "ksyu", "text": "Это значит: переменная `status` создаётся в любом случае. При любом числе. Программа не упадёт."},
                {"speaker": "novice", "text": "Значит если в `if` и `else` создать одну и ту же переменную — она точно будет существовать после блока?"},
                {"speaker": "ksyu", "text": "Да! Потому что какое бы число ни ввёл пользователь — выполнится либо одна часть, либо другая. NameError не будет."},
            ],
            "what_if": [
                {"description": "Пользователь вводит 7", "input": "7", "code": 'x = 7\nif x > 0:\n    status = "Плюс"\nelse:\n    status = "Минус"\nprint(status)', "output": "Плюс"},
                {"description": "Пользователь вводит 0", "input": "0", "code": 'x = 0\nif x > 0:\n    status = "Плюс"\nelse:\n    status = "Минус"\nprint(status)', "output": "Минус"},
            ],
            "solutions": [
                {"title": "✨ Итог: else защищает", "description": "Если нужно, чтобы переменная гарантированно создалась — используй if-else.", "code": 'x = int(input())\nif x > 0:\n    result = "положительное"\nelse:\n    result = "не положительное"\nprint(result)'},
            ],
        }
        print(f"✅ Added code_watch to 1-9")

    elif lid == "2-1":
        l["code_watch"] = {
            "title": "Разбор: цепочка elif",
            "main_code": 'x = int(input())\nif x > 0:\n    answer = "Плюс"\nelif x == 0:\n    answer = "Ноль"\nelse:\n    answer = "Минус"\nprint(answer)',
            "dialogue": [
                {"speaker": "va", "text": "В цепочке `if`-`elif`-`else` выполняется ровно одна ветка. Первая, которая дала `True`."},
                {"speaker": "novice", "text": "А если несколько условий истинны? Что тогда?"},
                {"speaker": "va", "text": "Python проверяет сверху вниз. Как только нашёл `True` — выполнил эту ветку и вышел. Остальные игнорируются."},
                {"speaker": "va", "code": 'x = 10\nif x > 0:      # True → выполнится\n    result = "Больше нуля"\nelif x > 5:    # True, но не проверяется!\n    result = "Больше пяти"\nprint(result)', "caption": "Первое True побеждает"},
                {"speaker": "novice", "text": "Ага! Даже если `x > 5` тоже истинно — Python до него не доходит!"},
                {"speaker": "va", "text": "Верно! Порядок `elif` имеет значение. Более конкретные условия ставь выше. Иначе они никогда не выполнятся."},
            ],
            "what_if": [
                {"description": "Порядок условий важен!", "input": "10", "code": 'x = 10\nif x > 5:      # True → сработает\n    result = "Больше пяти"\nelif x > 0:    # Не проверяется\n    result = "Больше нуля"\nprint(result)', "output": "Больше пяти"},
            ],
            "solutions": [
                {"title": "Правило: от частного к общему", "description": "Самые конкретные условия ставь выше. Самые общие — ниже.", "code": '# Пример: оценка\nmarks = 85\nif marks >= 90:\n    grade = "A"\nelif marks >= 75:\n    grade = "B"\nelif marks >= 50:\n    grade = "C"\nelse:\n    grade = "F"\nprint(grade)'},
            ],
        }
        print(f"✅ Added code_watch to 2-1")

with open(SRC, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)
shutil.copy2(SRC, DST)
print(f"\n✅ Copied to {DST}")
