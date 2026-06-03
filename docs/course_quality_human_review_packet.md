# Course Quality Audit — Human Review Packet

**Generated:** 2026-06-03T05:40:50.945011+00:00
**Total Issues:** 19

---
## 🚨 Must Fix Now
**Count:** 0

_No must-fix issues found._

---
## 🔍 Needs Human Review
**Count:** 17

### PQA-0001: 1-7 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[1].text`
- **Current:** После if всегда ставь двоеточие. Это как знак: дальше команды для этого условия.
- **Reason:** Dialogue uses 'услови' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0002: 4-17 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[0].text`
- **Current:** А если я хочу отсортировать не по самому значению, а по длине строки или по возрасту из словаря?
- **Reason:** Dialogue uses 'словар' which relates to 'dict', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0003: 1-1 — suspicious_one_line_code
- **Surface:** lesson | **Field:** `find_bug.correct`
- **Current:** print("Привет")
- **Reason:** Correct solution appears joined into one line without proper formatting
- **Suggested Fix:** Format as multi-line code block

### PQA-0004: 4-10 — suspicious_one_line_code
- **Surface:** lesson | **Field:** `find_bug.correct`
- **Current:** print("\n".join(["a","b"]))
- **Reason:** Correct solution appears joined into one line without proper formatting
- **Suggested Fix:** Format as multi-line code block

### PQA-0005: 1-5 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Игрок вводит число своих монет — 8. Добавь 1 монету и выведи результат (9).
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0006: 1-6 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Атака = 7, защита = 6 у Багуса. Посчитай суммарный урон (7 + 6) и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0008: 2-3 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Напиши программу, которая имитирует бросок двух кубиков. Подключи random, создай две переменные dice1 и dice2 с random.randint(1, 6), вычисли их сумму и выведи результат в формате: 'Бросок: X + Y = Су
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0010: 3-1 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** В рецепте нужно 3.5 части муки и 2 части воды. Перемножь их и выведи результат (7.0).
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0011: 3-18 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Сложи числа от 1 до 4 включительно с помощью цикла и выведи результат (10).
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0012: 3-30 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Из списка ['a', 'b', 'c'] удали элемент 'b' по значению и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0013: 3-33 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Посчитай сумму чисел 1 + 2 + 3 с помощью цикла и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0014: 3-34 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** В списке [1, 2, 1, 3, 1] посчитай, сколько раз встречается 1, и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0015: 3-37 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Объедини списки [1, 2] и [3, 4] с помощью extend() и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0016: 3-39 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Напиши программу «Бросок монетки». Подключи random, создай список coins = ['орёл', 'решка']. Используй random.choice() чтобы выбрать сторону. Выведи результат. Затем добавь условие: если выпал 'орёл' 
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0017: 4-17 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Отсортируй список ['ccc', 'b', 'aa'] по длине строк и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0018: 4-23 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Создай список a = [1], присвой b = a. Выведи результат a is b.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0019: 5-3 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Создай функцию add(a, b), которая возвращает сумму двух чисел. Выведи результат вызова add(7, 8).
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

---
## 📂 Issues by Part

### Part 1 (4 issues)

- 🔍 **PQA-0001** `needs_human_review` — 1-7: dialogue_premature_concept (post_error_dialogue[1].text)
  - Dialogue uses 'услови' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0003** `needs_human_review` — 1-1: suspicious_one_line_code (find_bug.correct)
  - Correct solution appears joined into one line without proper formatting
- 🔍 **PQA-0005** `needs_human_review` — 1-5: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0006** `needs_human_review` — 1-6: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified

### Part 2 (3 issues)

- 💅 **PQA-0007** `non_blocking_polish` — 2-2: wording_overstated (mission.task)
  - Wording 'напиши программу' may overstate when only one line is expected
- 🔍 **PQA-0008** `needs_human_review` — 2-3: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 💅 **PQA-0009** `non_blocking_polish` — 2-3: wording_overstated (mission.task)
  - Wording 'напиши программу' may overstate when only one line is expected

### Part 3 (7 issues)

- 🔍 **PQA-0010** `needs_human_review` — 3-1: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0011** `needs_human_review` — 3-18: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0012** `needs_human_review` — 3-30: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0013** `needs_human_review` — 3-33: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0014** `needs_human_review` — 3-34: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0015** `needs_human_review` — 3-37: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0016** `needs_human_review` — 3-39: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified

### Part 4 (4 issues)

- 🔍 **PQA-0002** `needs_human_review` — 4-17: dialogue_premature_concept (pre_topic_dialogue[0].text)
  - Dialogue uses 'словар' which relates to 'dict', a forbidden concept before this lesson
- 🔍 **PQA-0004** `needs_human_review` — 4-10: suspicious_one_line_code (find_bug.correct)
  - Correct solution appears joined into one line without proper formatting
- 🔍 **PQA-0017** `needs_human_review` — 4-17: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0018** `needs_human_review` — 4-23: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified

### Part 5 (1 issues)

- 🔍 **PQA-0019** `needs_human_review` — 5-3: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified

---
## 🏷️ Issues by Type

### dialogue_premature_concept (2 issues)
- PQA-0001: 1-7 (needs_human_review)
- PQA-0002: 4-17 (needs_human_review)

### suspicious_one_line_code (2 issues)
- PQA-0003: 1-1 (needs_human_review)
- PQA-0004: 4-10 (needs_human_review)

### wording_ambiguous (13 issues)
- PQA-0005: 1-5 (needs_human_review)
- PQA-0006: 1-6 (needs_human_review)
- PQA-0008: 2-3 (needs_human_review)
- PQA-0010: 3-1 (needs_human_review)
- PQA-0011: 3-18 (needs_human_review)
- PQA-0012: 3-30 (needs_human_review)
- PQA-0013: 3-33 (needs_human_review)
- PQA-0014: 3-34 (needs_human_review)
- PQA-0015: 3-37 (needs_human_review)
- PQA-0016: 3-39 (needs_human_review)
- PQA-0017: 4-17 (needs_human_review)
- PQA-0018: 4-23 (needs_human_review)
- PQA-0019: 5-3 (needs_human_review)

### wording_overstated (2 issues)
- PQA-0007: 2-2 (non_blocking_polish)
- PQA-0009: 2-3 (non_blocking_polish)
