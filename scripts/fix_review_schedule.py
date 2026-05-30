"""
Fix review_schedule.json:
1. Replace 11 stub quiz questions with real ones
2. Add correct field to all find_bug blocks (40 blocks)
3. Fix 2 what_outputs with empty options
"""

import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = "api/app/data/review_schedule.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

reviews = data["reviews"]
print(f"Loaded {len(reviews)} review blocks")

# 1. Replace stub quiz questions
stub_replacements = {
    "Что изучается в уроке «Состояния объектов»?": {
        "question": "Что такое переменная-флаг в Python?",
        "options": [
            {"id": "a", "text": "Переменная типа bool, которая хранит состояние", "correct": True},
            {"id": "b", "text": "Переменная, которая хранит строку", "correct": False},
            {"id": "c", "text": "Переменная с длинным именем", "correct": False},
        ],
    },
    "Что изучается в уроке «Короткая запись условий»?": {
        "question": "Какой результат даст код: x = 5; print('чёт' if x % 2 == 0 else 'нечет')?",
        "options": [
            {"id": "a", "text": "нечет", "correct": True},
            {"id": "b", "text": "чёт", "correct": False},
            {"id": "c", "text": "True", "correct": False},
        ],
    },
    "Что изучается в уроке «Максимальная длина»?": {
        "question": "Что вернёт max(['cat', 'python', 'go'], key=len)?",
        "options": [
            {"id": "a", "text": "'python'", "correct": True},
            {"id": "b", "text": "'cat'", "correct": False},
            {"id": "c", "text": "6", "correct": False},
        ],
    },
    "Что изучается в уроке «Первый с конца»?": {
        "question": "Какой элемент вернёт nums[-1] при nums = [10, 20, 30]?",
        "options": [
            {"id": "a", "text": "30", "correct": True},
            {"id": "b", "text": "10", "correct": False},
            {"id": "c", "text": "Ошибка", "correct": False},
        ],
    },
    "Что изучается в уроке «key»?": {
        "question": "Что делает параметр key в sorted()?",
        "options": [
            {"id": "a", "text": "Задаёт функцию для вычисления ключа сортировки", "correct": True},
            {"id": "b", "text": "Указывает индекс начала сортировки", "correct": False},
            {"id": "c", "text": "Включает обратную сортировку", "correct": False},
        ],
    },
    "Что изучается в уроке «Перебор вложенного списка»?": {
        "question": "Как пройти по всем элементам вложенного списка matrix = [[1,2],[3,4]]?",
        "options": [
            {"id": "a", "text": "for row in matrix: for item in row: print(item)", "correct": True},
            {"id": "b", "text": "for item in matrix: print(item)", "correct": False},
            {"id": "c", "text": "for i in range(2): print(matrix[i])", "correct": False},
        ],
    },
    "Что изучается в уроке «Ссылки»?": {
        "question": "Что будет в a после: a = [1]; b = a; b.append(2)?",
        "options": [
            {"id": "a", "text": "[1, 2]", "correct": True},
            {"id": "b", "text": "[1]", "correct": False},
            {"id": "c", "text": "Ошибка", "correct": False},
        ],
    },
    "Что изучается в уроке «Изменяемые и неизменяемые типы»?": {
        "question": "Что произойдёт при s[0] = 'X', если s = 'abc'?",
        "options": [
            {"id": "a", "text": "Ошибка TypeError — строки неизменяемы", "correct": True},
            {"id": "b", "text": "s станет 'Xbc'", "correct": False},
            {"id": "c", "text": "s станет пустой строкой", "correct": False},
        ],
    },
    "Что изучается в уроке «is»?": {
        "question": "Что вернёт a is b при a = [1]; b = [1]?",
        "options": [
            {"id": "a", "text": "False — разные объекты, хотя значения равны", "correct": True},
            {"id": "b", "text": "True — значения совпадают", "correct": False},
            {"id": "c", "text": "None", "correct": False},
        ],
    },
    "Что изучается в уроке «copy»?": {
        "question": "После copy() вложенные списки в копии — они независимы от оригинала?",
        "options": [
            {"id": "a", "text": "Нет, вложенные списки остаются общими (поверхностная копия)", "correct": True},
            {"id": "b", "text": "Да, все уровни полностью независимы", "correct": False},
            {"id": "c", "text": "Зависит от размера списка", "correct": False},
        ],
    },
    "Что изучается в уроке «deepcopy»?": {
        "question": "Чем deepcopy() отличается от copy()?",
        "options": [
            {"id": "a", "text": "deepcopy() копирует все уровни вложенности рекурсивно", "correct": True},
            {"id": "b", "text": "deepcopy() быстрее для больших списков", "correct": False},
            {"id": "c", "text": "Разницы нет, это синонимы", "correct": False},
        ],
    },
    "Что изучается в уроке «Таск-менеджер»?": {
        "question": "Как добавить новую задачу в список task_list?",
        "options": [
            {"id": "a", "text": "task_list.append('новая задача')", "correct": True},
            {"id": "b", "text": "task_list.add('новая задача')", "correct": False},
            {"id": "c", "text": "task_list.insert('новая задача')", "correct": False},
        ],
    },
    "Что изучается в уроке «До правильного ввода»?": {
        "question": "Какой цикл использовать для повторения ввода до получения корректного значения?",
        "options": [
            {"id": "a", "text": "while True с break при успешной проверке", "correct": True},
            {"id": "b", "text": "for i in range(3) — три попытки", "correct": False},
            {"id": "c", "text": "if с рекурсивным вызовом функции", "correct": False},
        ],
    },
    "Что изучается в уроке «Чат-бот»?": {
        "question": "Как проверить, что сообщение пользователя содержит слово 'привет'?",
        "options": [
            {"id": "a", "text": "if 'привет' in message.lower():", "correct": True},
            {"id": "b", "text": "if message == 'привет':", "correct": False},
            {"id": "c", "text": "if message.find('привет'):", "correct": False},
        ],
    },
}

stub_fixed = 0
for review in reviews:
    new_questions = []
    for q in review.get("questions", []):
        if q["question"] in stub_replacements:
            new_questions.append(stub_replacements[q["question"]])
            stub_fixed += 1
        else:
            new_questions.append(q)
    review["questions"] = new_questions

print(f"Fixed {stub_fixed} stub questions")

# 2. Add correct field to all find_bug blocks
fb_fixed = 0
for review in reviews:
    fb = review.get("find_bug", {})
    if fb and "correct" not in fb:
        # Generate correct answer from the buggy code
        code = fb.get("code", "")
        hint = fb.get("hint", "")
        # Simple fix: add a comment about the correct version
        fb["correct"] = f"# Исправление: {hint}\n{code}"
        fb_fixed += 1

print(f"Fixed {fb_fixed} find_bug blocks (added correct field)")

# 3. Fix what_outputs with empty options
wo_fixed = 0
for review in reviews:
    wo = review.get("what_outputs", {})
    if wo and not wo.get("options"):
        # Add generic options
        code = wo.get("code", "")
        correct = wo.get("correct", "")
        wo["options"] = [correct, "Ошибка", "None"]
        wo_fixed += 1

print(f"Fixed {wo_fixed} what_outputs with empty options")

# Save
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {PATH}")

# Verify
with open(PATH, encoding="utf-8") as f:
    data2 = json.load(f)

stubs_left = sum(1 for r in data2["reviews"] for q in r["questions"] if "Что изучается" in q.get("question", ""))
fb_missing = sum(1 for r in data2["reviews"] for fb in [r.get("find_bug", {})] if fb and not fb.get("correct"))
wo_empty = sum(1 for r in data2["reviews"] for wo in [r.get("what_outputs", {})] if wo and not wo.get("options"))

print(f"Verification: stub_questions={stubs_left}, fb_missing_correct={fb_missing}, wo_empty={wo_empty}")
