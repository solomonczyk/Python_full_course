# Course Quality Audit — Human Review Packet

**Generated:** 2026-06-03T05:24:32.508040+00:00
**Total Issues:** 41

**Operator Review (2026-06-03):** All 41 items reviewed as part of `PYTHON-QUEST-POST-ACCEPTANCE-OPERATOR-REVIEW-REMAINING-WORDING-POLISH-001`.

- **False positives:** 26 — audit flagged natural Russian words (если, пока, повтор) as premature programming concepts, or misapplied formatting rules.
- **Acceptable:** 15 — items that are contextually clear or pedagogically appropriate.
- **Fixes applied:** 0 — no wording change was needed; all items are either false positives or acceptable in context.

---
## 🚨 Must Fix Now
**Count:** 0

_No must-fix issues found._

---
## 🔍 Needs Human Review
**Count:** 39

### PQA-0001: 1-1 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[2].text`
- **Current:** То есть `print()` — это как крик в пещеру. Я говорю что-то внутри скобок, и Python повторяет это на экране?
- **Reason:** Dialogue uses 'повтор' which relates to 'for', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0002: 1-1 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[4].text`
- **Current:** А, то есть если я напишу `print('Привет')`, Python выведет «Привет» на экран? А если `print(5 + 3)` — он сначала посчитает и выведет 8?
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0003: 1-2 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[1].text`
- **Current:** У тебя есть банка с вареньем и банка с солёными огурцами. Если на них нет этикеток — ты через месяц не вспомнишь, где что. Кавычки — это этикетка для текста. Без них Python не понимает: это текст (вар
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0004: 1-2 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[3].text`
- **Current:** А если я поставлю одинарную кавычку в начале и двойную в конце — Python выдаст ошибку? Они должны в паре ходить?
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0005: 1-3 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[3].text`
- **Current:** Да! `name = "Ксю"` — в сундук `name` положили строку. `health = 100` — в сундук `health` положили число. Имя сундука без кавычек, значение — с кавычками если текст, без кавычек если число.
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0006: 1-4 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[1].text`
- **Current:** Представь, что ты звонишь в дверь магазинчика. Ты ждёшь, пока продавец откроет и скажет «Здравствуйте!». `input()` — это звонок. Программа ждёт, пока ты что-то напишешь и нажмёшь Enter.
- **Reason:** Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0007: 1-4 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[4].text`
- **Current:** `input()` ждёт, пока пользователь что-то введёт, и возвращает это как строку. Звонок в дверь программы.
- **Reason:** Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0008: 1-4 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[1].text`
- **Current:** input() возвращает строку. Даже если ввели число. Преобразуй через int().
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0009: 1-4 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[3].text`
- **Current:** То есть `input()` всегда возвращает текст, даже если я ввожу число? И чтобы складывать, нужно заворачивать в `int()`?
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0010: 1-4 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[4].text`
- **Current:** Я тоже так ошибался, пока не разобрался. Попробуй ещё!
- **Reason:** Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0011: 1-5 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[1].text`
- **Current:** Ты позвонил в дверь, продавец что-то сказал — но сказал он это на иностранном языке. Ты слышишь звуки, но не понимаешь числа. `input()` возвращает строку, даже если ввели цифры. `int()` — переводчик, 
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0012: 1-5 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[1].text`
- **Current:** int(input()) — стандартный приём. Но если введут букву — будет ValueError.
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0013: 1-5 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[3].text`
- **Current:** То есть если я сделаю int("5") + 3 — получится 8, а "5" + 3 — ошибка? Типы должны совпадать?
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0014: 1-6 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[3].text`
- **Current:** Да. `10 + 5 * 2` — Python сначала умножает, потом складывает (как в школе). Если хочешь другой порядок — ставь скобки: `(10 + 5) * 2 = 30`. Скобки работают как в математике.
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0015: 1-6 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[1].text`
- **Current:** Умножение и деление выполняются до сложения и вычитания. Если хочешь другой порядок — используй скобки.
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0016: 1-6 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[3].text`
- **Current:** То есть если я напишу 10 + 2 * 3, будет 16, а не 36? Надо запомнить про порядок.
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0017: 1-7 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[1].text`
- **Current:** Представь старинные весы с двумя чашами. На одну кладёшь число игрока, на другую — число врага. Весы опускаются вниз на той стороне, где число больше. Если чаши на одном уровне — числа равны. `==`, `>
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0018: 1-7 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[1].text`
- **Current:** После if всегда ставь двоеточие. Это как знак: дальше команды для этого условия.
- **Reason:** Dialogue uses 'услови' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0019: 1-7 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[3].text`
- **Current:** Ясно: == проверяет, = присваивает. Ошибка компиляции сразу покажет, если перепутал.
- **Reason:** Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0020: 2-1 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[4].text`
- **Current:** Значит, `elif` — это как дополнительная проверка между `if` и `else`? Сначала `if` спросил — не подошло, тогда `elif` спрашивает, и так пока `else` не сработает?
- **Reason:** Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0021: 2-2 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[1].text`
- **Current:** Вспомни турнир паровых големов: пока первый бой не закончился — второй не начинается. Как только один голем победил — турнир окончен, остальные матчи отменяются. Логическая цепочка работает так же: пе
- **Reason:** Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0022: 2-2 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[4].text`
- **Current:** Я тоже так ошибался, пока не разобрался. Попробуй ещё!
- **Reason:** Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0023: 3-11 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `post_error_dialogue[4].text`
- **Current:** Я тоже так ошибался, пока не разобрался. Попробуй ещё!
- **Reason:** Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0024: 4-17 — dialogue_premature_concept
- **Surface:** lesson | **Field:** `pre_topic_dialogue[0].text`
- **Current:** А если я хочу отсортировать не по самому значению, а по длине строки или по возрасту из словаря?
- **Reason:** Dialogue uses 'словар' which relates to 'dict', a forbidden concept before this lesson
- **Suggested Fix:** Rephrase to avoid referencing this concept

### PQA-0025: 1-1 — suspicious_one_line_code
- **Surface:** lesson | **Field:** `find_bug.correct`
- **Current:** print("Привет")
- **Reason:** Correct solution appears joined into one line without proper formatting
- **Suggested Fix:** Format as multi-line code block

### PQA-0026: 4-10 — suspicious_one_line_code
- **Surface:** lesson | **Field:** `find_bug.correct`
- **Current:** print("\n".join(["a","b"]))
- **Reason:** Correct solution appears joined into one line without proper formatting
- **Suggested Fix:** Format as multi-line code block

### PQA-0027: 1-5 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Игрок вводит число своих монет — 8. Добавь 1 монету и выведи результат (9).
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0028: 1-6 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Атака = 7, защита = 6 у Багуса. Посчитай суммарный урон (7 + 6) и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0030: 2-3 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Напиши программу, которая имитирует бросок двух кубиков. Подключи random, создай две переменные dice1 и dice2 с random.randint(1, 6), вычисли их сумму и выведи результат в формате: 'Бросок: X + Y = Су
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0032: 3-1 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** В рецепте нужно 3.5 части муки и 2 части воды. Перемножь их и выведи результат (7.0).
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0033: 3-18 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Сложи числа от 1 до 4 включительно с помощью цикла и выведи результат (10).
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0034: 3-30 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Из списка ['a', 'b', 'c'] удали элемент 'b' по значению и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0035: 3-33 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Посчитай сумму чисел 1 + 2 + 3 с помощью цикла и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0036: 3-34 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** В списке [1, 2, 1, 3, 1] посчитай, сколько раз встречается 1, и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0037: 3-37 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Объедини списки [1, 2] и [3, 4] с помощью extend() и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0038: 3-39 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Напиши программу «Бросок монетки». Подключи random, создай список coins = ['орёл', 'решка']. Используй random.choice() чтобы выбрать сторону. Выведи результат. Затем добавь условие: если выпал 'орёл' 
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0039: 4-17 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Отсортируй список ['ccc', 'b', 'aa'] по длине строк и выведи результат.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0040: 4-23 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Создай список a = [1], присвой b = a. Выведи результат a is b.
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

### PQA-0041: 5-3 — wording_ambiguous
- **Surface:** lesson | **Field:** `mission.task`
- **Current:** Создай функцию add(a, b), которая возвращает сумму двух чисел. Выведи результат вызова add(7, 8).
- **Reason:** Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- **Suggested Fix:** Clearly specify what should be displayed

---
## 📂 Issues by Part

### Part 1 (22 issues)

- 🔍 **PQA-0001** `needs_human_review` — 1-1: dialogue_premature_concept (pre_topic_dialogue[2].text)
  - Dialogue uses 'повтор' which relates to 'for', a forbidden concept before this lesson
- 🔍 **PQA-0002** `needs_human_review` — 1-1: dialogue_premature_concept (pre_topic_dialogue[4].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0003** `needs_human_review` — 1-2: dialogue_premature_concept (pre_topic_dialogue[1].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0004** `needs_human_review` — 1-2: dialogue_premature_concept (post_error_dialogue[3].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0005** `needs_human_review` — 1-3: dialogue_premature_concept (pre_topic_dialogue[3].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0006** `needs_human_review` — 1-4: dialogue_premature_concept (pre_topic_dialogue[1].text)
  - Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- 🔍 **PQA-0007** `needs_human_review` — 1-4: dialogue_premature_concept (pre_topic_dialogue[4].text)
  - Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- 🔍 **PQA-0008** `needs_human_review` — 1-4: dialogue_premature_concept (post_error_dialogue[1].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0009** `needs_human_review` — 1-4: dialogue_premature_concept (post_error_dialogue[3].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0010** `needs_human_review` — 1-4: dialogue_premature_concept (post_error_dialogue[4].text)
  - Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- 🔍 **PQA-0011** `needs_human_review` — 1-5: dialogue_premature_concept (pre_topic_dialogue[1].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0012** `needs_human_review` — 1-5: dialogue_premature_concept (post_error_dialogue[1].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0013** `needs_human_review` — 1-5: dialogue_premature_concept (post_error_dialogue[3].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0014** `needs_human_review` — 1-6: dialogue_premature_concept (pre_topic_dialogue[3].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0015** `needs_human_review` — 1-6: dialogue_premature_concept (post_error_dialogue[1].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0016** `needs_human_review` — 1-6: dialogue_premature_concept (post_error_dialogue[3].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0017** `needs_human_review` — 1-7: dialogue_premature_concept (pre_topic_dialogue[1].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0018** `needs_human_review` — 1-7: dialogue_premature_concept (post_error_dialogue[1].text)
  - Dialogue uses 'услови' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0019** `needs_human_review` — 1-7: dialogue_premature_concept (post_error_dialogue[3].text)
  - Dialogue uses 'если' which relates to 'if', a forbidden concept before this lesson
- 🔍 **PQA-0025** `needs_human_review` — 1-1: suspicious_one_line_code (find_bug.correct)
  - Correct solution appears joined into one line without proper formatting
- 🔍 **PQA-0027** `needs_human_review` — 1-5: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0028** `needs_human_review` — 1-6: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified

### Part 2 (6 issues)

- 🔍 **PQA-0020** `needs_human_review` — 2-1: dialogue_premature_concept (pre_topic_dialogue[4].text)
  - Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- 🔍 **PQA-0021** `needs_human_review` — 2-2: dialogue_premature_concept (pre_topic_dialogue[1].text)
  - Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- 🔍 **PQA-0022** `needs_human_review` — 2-2: dialogue_premature_concept (post_error_dialogue[4].text)
  - Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- 💅 **PQA-0029** `non_blocking_polish` — 2-2: wording_overstated (mission.task)
  - Wording 'напиши программу' may overstate when only one line is expected
- 🔍 **PQA-0030** `needs_human_review` — 2-3: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 💅 **PQA-0031** `non_blocking_polish` — 2-3: wording_overstated (mission.task)
  - Wording 'напиши программу' may overstate when only one line is expected

### Part 3 (8 issues)

- 🔍 **PQA-0023** `needs_human_review` — 3-11: dialogue_premature_concept (post_error_dialogue[4].text)
  - Dialogue uses 'пока ' which relates to 'while', a forbidden concept before this lesson
- 🔍 **PQA-0032** `needs_human_review` — 3-1: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0033** `needs_human_review` — 3-18: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0034** `needs_human_review` — 3-30: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0035** `needs_human_review` — 3-33: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0036** `needs_human_review` — 3-34: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0037** `needs_human_review` — 3-37: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0038** `needs_human_review` — 3-39: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified

### Part 4 (4 issues)

- 🔍 **PQA-0024** `needs_human_review` — 4-17: dialogue_premature_concept (pre_topic_dialogue[0].text)
  - Dialogue uses 'словар' which relates to 'dict', a forbidden concept before this lesson
- 🔍 **PQA-0026** `needs_human_review` — 4-10: suspicious_one_line_code (find_bug.correct)
  - Correct solution appears joined into one line without proper formatting
- 🔍 **PQA-0039** `needs_human_review` — 4-17: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified
- 🔍 **PQA-0040** `needs_human_review` — 4-23: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified

### Part 5 (1 issues)

- 🔍 **PQA-0041** `needs_human_review` — 5-3: wording_ambiguous (mission.task)
  - Wording 'выведи результат' is ambiguous if expected output is not clearly specified

---
## 🏷️ Issues by Type

### dialogue_premature_concept (24 issues)
- PQA-0001: 1-1 (needs_human_review)
- PQA-0002: 1-1 (needs_human_review)
- PQA-0003: 1-2 (needs_human_review)
- PQA-0004: 1-2 (needs_human_review)
- PQA-0005: 1-3 (needs_human_review)
- PQA-0006: 1-4 (needs_human_review)
- PQA-0007: 1-4 (needs_human_review)
- PQA-0008: 1-4 (needs_human_review)
- PQA-0009: 1-4 (needs_human_review)
- PQA-0010: 1-4 (needs_human_review)
- PQA-0011: 1-5 (needs_human_review)
- PQA-0012: 1-5 (needs_human_review)
- PQA-0013: 1-5 (needs_human_review)
- PQA-0014: 1-6 (needs_human_review)
- PQA-0015: 1-6 (needs_human_review)
- PQA-0016: 1-6 (needs_human_review)
- PQA-0017: 1-7 (needs_human_review)
- PQA-0018: 1-7 (needs_human_review)
- PQA-0019: 1-7 (needs_human_review)
- PQA-0020: 2-1 (needs_human_review)
- PQA-0021: 2-2 (needs_human_review)
- PQA-0022: 2-2 (needs_human_review)
- PQA-0023: 3-11 (needs_human_review)
- PQA-0024: 4-17 (needs_human_review)

### suspicious_one_line_code (2 issues)
- PQA-0025: 1-1 (needs_human_review)
- PQA-0026: 4-10 (needs_human_review)

### wording_ambiguous (13 issues)
- PQA-0027: 1-5 (needs_human_review)
- PQA-0028: 1-6 (needs_human_review)
- PQA-0030: 2-3 (needs_human_review)
- PQA-0032: 3-1 (needs_human_review)
- PQA-0033: 3-18 (needs_human_review)
- PQA-0034: 3-30 (needs_human_review)
- PQA-0035: 3-33 (needs_human_review)
- PQA-0036: 3-34 (needs_human_review)
- PQA-0037: 3-37 (needs_human_review)
- PQA-0038: 3-39 (needs_human_review)
- PQA-0039: 4-17 (needs_human_review)
- PQA-0040: 4-23 (needs_human_review)
- PQA-0041: 5-3 (needs_human_review)

### wording_overstated (2 issues)
- PQA-0029: 2-2 (non_blocking_polish)
- PQA-0031: 2-3 (non_blocking_polish)
