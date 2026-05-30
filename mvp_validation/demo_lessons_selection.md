# Demo Lessons Selection: Python Quest MVP
**Status**: READY_FOR_REAL_WORLD_TEST  
**Goal**: 3 lessons that demonstrate format, validate engagement, show final game connection

---

## DEMO LESSON 1: Твой голос в коде
**Topic**: print(), strings, input()  
**Slug**: demo-01-voice-in-code  
**Character**: Ксю  
**Duration**: 15-20 min  
**Difficulty**: Absolute beginner  
**Final Game Connection**: Game menu, player greeting

### Learning Objectives
1. Understand print() as output command
2. Create string literals with quotes
3. Use input() to get user data
4. Combine input and print for dialogue

### Scene Setup
**Setting**: Ксю встречает Новичка у входа в Академию. Новичок молчит — не знает, как заговорить с Python.

**Ксю says**:
```
«Привет! Ты, наверное, Новичок? 
Я Ксю. Буду твоей проводницей в мир Python.

Смотри, Python — это как помощник. 
Чтобы он что-то сказал, ему нужна команда.
Самая простая команда — print().

Попробуй:
```python
print("Привет, Python!")
```

Нажми Enter. Что видишь?»
```

### Explanation Block
**Новичок пробует**:
```python
print("Привет, Python!")
```

**Вывод**:
```
Привет, Python!
```

**Ксю explains**:
```
«Всё, что внутри кавычек — текст, который Python выводит.
Кавычки могут быть двойными " или одинарными ' — 
главное, чтобы пара совпадала.

Текст в кавычках называется строкой — str.
А print — функция, которая выводит строку на экран.»
```

### Visual Reminder
```
┌─────────────────────────────────┐
│  print("Текст")                 │
│        │                        │
│        └── то, что выведется   │
│  ───────                        │
│  команда вывода                 │
└─────────────────────────────────┘
```

### Mini-Quiz
**Question**: Что выведет этот код?
```python
print("2 + 2")
```

**Options**:
- [ ] 4
- [x] 2 + 2
- [ ] Ошибка

**Explanation**: Кавычки делают это строкой, не математикой. Python выводит "2 + 2", не считает.

### Find the Bug (Багус strikes)
**Code**:
```python
print(Привет)
```

**Error**: NameError

**Hint**: «Ты забыл кавычки! Багус loves this mistake.»

**Fix**:
```python
print("Привет")
```

### Input Introduction
**Ксю**:
```
«А теперь — магия. Что если программа 
должна говорить с человеком?

input() — команда, которая ждёт, 
пока пользователь что-то введёт.»
```

**Example**:
```python
name = input()
print("Привет,", name)
```

**How it works**:
1. Программа останавливается
2. Ждёт ввода (ты пишешь "Анна")
3. Сохраняет в переменную name
4. Выводит "Привет, Анна"

### Mission: Первый диалог
**Task**: Напиши программу, которая:
1. Спрашивает имя игрока
2. Приветствует его текстом "Добро пожаловать в КсюВаДа, [имя]!"

**Expected Output**:
```
[ввод: Макс]
Добро пожаловать в КсюВаДа, Макс!
```

**Character**: Да appears for mission briefing

**Да says**:
```
«Миссия 1: Персональное приветствие.
Создай диалог. Начни игру.»
```

### Connection to Final Game
```
В финальной игре «Побег из Башни Багуса» 
это станет началом:

================================
   ПОБЕГ ИЗ БАШНИ БАГУСА
================================

Введи имя героя: _
Добро пожаловать в игру, [имя]!
```

### Mini-Summary
- `print()` — вывод на экран
- Строки в кавычках: "текст"
- `input()` — ввод от пользователя
- Переменная = коробка для данных

---

## DEMO LESSON 2: Выбор пути
**Topic**: if / else, comparisons, bool  
**Slug**: demo-02-choice-path  
**Character**: Ва + Багус  
**Duration**: 20-25 min  
**Difficulty**: Beginner (builds on Lesson 1)  
**Final Game Connection**: Game choices, access control, conditions

### Learning Objectives
1. Understand if/else as decision point
2. Use comparison operators (==, !=, >, <)
3. Read bool values (True/False)
4. Find and fix syntax errors

### Scene Setup
**Setting**: Новичок и Ва стоят перед дверью в Башню. Дверь требует пароль.

**Ва**:
```
«Дверь откроется только если пароль верный.
Это условие — if.

Смотри структуру:
```python
if условие:
    # что делать, если условие истинно
else:
    # что делать, если условие ложно
```

Двоеточие после условия — обязательно.
Отступы (4 пробела) — показывают, 
что код "внутри" условия.»
```

### Explanation Block
**Example**:
```python
password = input("Введите пароль: ")

if password == "python":
    print("Доступ разрешён")
else:
    print("Доступ запрещён")
```

**Ва explains**:
```
«== — это проверка "равно ли".
Не путай с = (присваивание)!

=   → кладём значение в переменную
==  → проверяем, равны ли значения

Результат проверки — bool:
• True  (истина, да)
• False (ложь, нет)
```

### Visual Reminder: if/else Structure
```
┌────────────────────────────────────┐
│  if условие:                       │
│  ░░░░действие_если_да              │
│  else:                             │
│  ░░░░действие_если_нет             │
│                                    │
│  ░░░░ = 4 пробела (отступ)         │
│  : = двоеточие обязательно!        │
└────────────────────────────────────┘
```

### Comparison Operators
```
==  равно          5 == 5  → True
!=  не равно       5 != 3  → True
>   больше         5 > 3   → True
<   меньше         5 < 3   → False
>=  больше или =   5 >= 5  → True
<=  меньше или =   5 <= 3  → False
```

### Mini-Quiz
**Question**: Что выведет код?
```python
x = 10
if x > 20:
    print("Большое")
else:
    print("Маленькое")
```

**Options**:
- [ ] Большое
- [x] Маленькое
- [ ] Ошибка

**Explanation**: 10 не больше 20 → условие ложно → выполняется else → "Маленькое"

### Find the Bug (Багус strikes)
**Code**:
```python
if password == "secret"
    print("Входи")
else:
    print("Неверно")
```

**Error**: SyntaxError (invalid syntax)

**Hint**: «Багус украл двоеточие! После условия if обязательно ставь :»

**Fix**:
```python
if password == "secret":
    print("Входи")
```

**Багус laughs**:
```
«Ха-ха! Без двоеточия Python не понимает,
где кончается условие и начинается тело.
Мелочь, а ломает всё.»
```

### Another Bug Hunt
**Code**:
```python
age = 15
if age > 18:
print("Взрослый")
else:
    print("Ребёнок")
```

**Error**: IndentationError

**Hint**: «Забыл отступ! Python живёт по отступам.»

**Fix**:
```python
if age > 18:
    print("Взрослый")
```

### Mission: Пропускной пункт
**Task**: Напиши программу, которая:
1. Спрашивает возраст
2. Если >= 18 — пишет "Доступ разрешён"
3. Иначе — пишет "Доступ запрещён"

**Expected Output**:
```
Сколько тебе лет? 20
Доступ разрешён

Сколько тебе лет? 15
Доступ запрещён
```

**Hint**: Не забудь int() — input() даёт строку!

**Solution skeleton**:
```python
age = int(input("Сколько тебе лет? "))
if age >= 18:
    print("Доступ разрешён")
else:
    print("Доступ запрещён")
```

### Connection to Final Game
```
В «Побеге из Башни Багуса» if/else — 
основа всех выборов:

• Проверка здоровья перед боем
• Проверка наличия ключа для двери
• Проверка, есть ли предмет в инвентаре
• Развилки: идти налево или направо

Пример из игры:
```python
if "ключ" in inventory:
    print("Дверь открывается!")
    room = "сокровищница"
else:
    print("Заперто. Нужен ключ.")
    print("Придётся искать дальше...")
```
```

### Mini-Summary
- `if условие:` — проверка
- `else:` — иначе
- `==` — равно (проверка)
- `=` — присвоить (действие)
- `:` — двоеточие обязательно
- Отступы — структура кода

---

## DEMO LESSON 3: Инвентарь героя
**Topic**: Lists, indexes, append, len()  
**Slug**: demo-03-inventory  
**Character**: Да + Ксю  
**Duration**: 20-25 min  
**Difficulty**: Beginner  
**Final Game Connection**: Inventory system, collecting items, game state

### Learning Objectives
1. Create and use lists
2. Access elements by index (0-based)
3. Modify lists (append, remove)
4. Use loops with lists

### Scene Setup
**Setting**: Новичок собирается в путешествие. Да даёт список снаряжения.

**Да**:
```
«В Башне Багуса тебе понадобятся предметы.
Список предметов — это list.

Создаём:
```python
inventory = ["факел", "ключ", "зелье"]
```

Квадратные скобки. Элементы через запятую.
Строки в кавычках.»
```

### Explanation Block
**Creating a list**:
```python
inventory = ["факел", "ключ", "зелье"]
```

**Accessing elements** (Ксю explains):
```
«Индексация начинается с 0.
Не с 1! С нуля. Это важно.

inventory[0] → "факел"
inventory[1] → "ключ"
inventory[2] → "зелье"
```

### Visual Reminder: List Indexes
```
┌─────────────────────────────────────┐
│  inventory                          │
│                                     │
│  ┌───────┬───────┬───────┐          │
│  │"факел"│"ключ" │"зелье"│          │
│  └───┬───┴───┬───┴───┬───┘          │
│      │       │       │              │
│      0       1       2              │
│   [0]     [1]     [2]               │
│                                     │
│  inventory[0] → "факел"             │
│  inventory[2] → "зелье"             │
│  inventory[-1] → "зелье" (последний)│
└─────────────────────────────────────┘
```

### List Methods
```python
inventory = ["факел"]

# Добавить
inventory.append("ключ")
# → ["факел", "ключ"]

# Узнать длину
len(inventory)
# → 2

# Проверить наличие
"ключ" in inventory
# → True
```

### Loop Through List
```python
inventory = ["факел", "ключ", "зелье"]

for item in inventory:
    print(f"В инвентаре: {item}")
```

**Output**:
```
В инвентаре: факел
В инвентаре: ключ
В инвентаре: зелье
```

### Mini-Quiz
**Question**: Что выведет код?
```python
items = [10, 20, 30]
print(items[-1])
```

**Options**:
- [ ] 10
- [x] 30
- [ ] Ошибка

**Explanation**: Отрицательные индексы считают с конца. -1 = последний элемент.

### Find the Bug (Багус strikes)
**Code**:
```python
items = [1, 2, 3]
print(items[3])
```

**Error**: IndexError: list index out of range

**Багус**:
```
«Ха-ха! Ты забыл, что индексы с 0!
[1, 2, 3] имеет индексы 0, 1, 2.
Индекса 3 не существует!

Максимум — items[2]»
```

**Fix**:
```python
print(items[2])  # выведет 3
```

### Mission: Собери инвентарь
**Task**: Напиши программу, которая:
1. Создаёт пустой список инвентаря
2. Добавляет 3 предмета через input()
3. Выводит полный список
4. Показывает количество предметов

**Expected Output**:
```
Добавь предмет: факел
Добавь предмет: ключ
Добавь предмет: зелье

Ваш инвентарь:
- факел
- ключ
- зелье

Всего предметов: 3
```

**Solution skeleton**:
```python
inventory = []

item1 = input("Добавь предмет: ")
inventory.append(item1)

item2 = input("Добавь предмет: ")
inventory.append(item2)

item3 = input("Добавь предмет: ")
inventory.append(item3)

print("\nВаш инвентарь:")
for item in inventory:
    print(f"- {item}")

print(f"\nВсего предметов: {len(inventory)}")
```

### Connection to Final Game
```
В «Побеге из Башни Багуса» инвентарь — 
ключевая механика:

```python
inventory = ["факел"]
health = 100

# Находим сундук
print("Ты нашёл сундук!")
found_item = "ключ"
inventory.append(found_item)
print(f"{found_item} добавлен в инвентарь")

# Проверяем перед дверью
if "ключ" in inventory:
    print("У тебя есть ключ! Дверь открыта.")
else:
    print("Дверь заперта. Ищи ключ.")

# Показываем статус
print(f"\nЗдоровье: {health}")
print(f"Предметов: {len(inventory)}")
print("Инвентарь:", inventory)
```

Список = память игрока.
Без него нет игры.
```

### Mini-Summary
- `[]` — пустой список
- `["a", "b"]` — список с элементами
- `list[0]` — первый элемент (индекс 0!)
- `list[-1]` — последний элемент
- `list.append(x)` — добавить в конец
- `len(list)` — количество элементов
- `x in list` — проверить наличие
- `for x in list:` — перебрать все элементы

---

## DEMO LESSONS SUMMARY

### What These 3 Lessons Demonstrate

| Aspect | Lesson 1 | Lesson 2 | Lesson 3 |
|--------|----------|----------|----------|
| **Topic** | print/input | if/else | lists |
| **Character** | Ксю | Ва + Багус | Да + Ксю |
| **Format** | Explanation → Quiz → Bug → Mission | Explanation → Quiz → Bug → Mission | Explanation → Quiz → Bug → Mission |
| **Final Game** | Greeting dialog | Access control | Inventory system |
| **Bug Type** | Missing quotes | Missing colon/indent | Index out of range |
| **Engagement** | First success | Puzzle solving | Building something |

### Progressive Complexity
```
Lesson 1: Single command → immediate output
Lesson 2: Logic structure → decision making  
Lesson 3: Data structure → building systems
```

### Character Arc in Demos
```
Lesson 1: Ксю welcomes — warm entry
Lesson 2: Ва teaches + Багус challenges — core conflict
Lesson 3: Да pushes + success — momentum building
```

### Call to Action at End of Lesson 3
```
«Ты создал инвентарь. Ты понял if. Ты умеешь диалог.

В полном курсе ты соберёшь:
• Систему здоровья
• Случайные события
• Боевую механику
• Побег из Башни

Хочешь продолжить?»

[Получить полный курс — когда запустим]
[Узнать о запуске первым]
```

---

## DELIVERY FORMAT OPTIONS

### Option A: Markdown + Email
- Send 3 lessons as formatted email series
- Day 1: Lesson 1
- Day 2: Lesson 2
- Day 3: Lesson 3 + CTA

### Option B: Simple Web Pages
- Static HTML pages on landing site
- Code syntax highlighting (Prism.js or similar)
- Next lesson unlocked after "mark complete"

### Option C: PDF Guide
- Downloadable 3-lesson PDF
- Mobile-friendly
- Shareable

### Option D: Telegram Format
- Lessons delivered as Telegram messages
- Code blocks formatted
- Interactive polls for quizzes

**Recommended for MVP**: Option A (email) or Option D (Telegram) — lowest friction

---

## TRACKING METRICS FOR DEMO LESSONS

| Metric | Lesson 1 | Lesson 2 | Lesson 3 |
|--------|----------|----------|----------|
| Open rate | Email metric | — | — |
| Click-through | — | — | — |
| Completion rate | Self-reported | Self-reported | Self-reported |
| Mission submission | Track via form | Track via form | Track via form |
| Bug hunt success | Track clicks | Track clicks | Track clicks |
| Time spent | Estimate | Estimate | Estimate |
| Drop-off point | Where they stop | Where they stop | Where they stop |

---

## DEMO LESSON PRODUCTION CHECKLIST

### Content
- [ ] Lesson 1: print/input draft complete
- [ ] Lesson 2: if/else draft complete
- [ ] Lesson 3: lists draft complete
- [ ] All 3 mini-quizzes written
- [ ] All 3 bug hunt scenarios written
- [ ] All 3 missions written with expected output
- [ ] Connection to final game explained in each

### Review
- [ ] Test code examples run correctly
- [ ] Check all syntax is valid Python
- [ ] Verify difficulty progression
- [ ] Ensure character voices are distinct
- [ ] Validate 15-20 min time estimate per lesson

### Formatting
- [ ] Code blocks formatted
- [ ] Visual reminders created (ASCII art or simple graphics)
- [ ] Mobile-readable layout
- [ ] Clear CTAs at end of Lesson 3

### Delivery
- [ ] Email sequence configured
- [ ] Subject lines written
- [ ] Landing page links to email capture
- [ ] Confirmation email with Lesson 1 ready

---

*Status: READY_FOR_REAL_WORLD_TEST*
