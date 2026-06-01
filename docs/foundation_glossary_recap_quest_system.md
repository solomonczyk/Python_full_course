# Foundation / Glossary / Recap / Quest System

> **Версия:** 1.0  
> **Дата:** 2026-06-01  
> **Слой:** PYTHON-QUEST-FOUNDATION-GLOSSARY-RECAP-QUEST-SYSTEM-001

---

## 1. Зачем добавлен этот слой

Операторский ревью выявил системный методический дефект:

- Урок 1-1 сразу стартует с `print()` без объяснения базовых понятий: команды, скобок, кавычек, текста vs переменной
- Нет централизованного глоссария — ученик не может быстро найти определение термина
- После каждого раздела нет напоминалки (recap) с ключевыми правилами
- Нет итоговых квестов, которые бы связывали все темы раздела в одну задачу
- Роль Багуса местами непонятна: он одновременно и создаёт, и исправляет ошибки без объяснения

Этот слой решает все эти проблемы как единая образовательная архитектура.

---

## 2. Архитектура

### 2.1 Data Flow

```
lessons.json ──→ /lessons API ──→ LessonPage (с FoundationBlock)
                                     ↓
glossary.json ──→ /glossary API ──→ GlossaryPage + GlossaryLessonLinks
                                     ↓
recaps.json ────→ /recaps API ────→ RecapPage + Sidebar + HomePage
                                     ↓
chapter_quests.json ──→ /quests API ──→ QuestPage + Sidebar + HomePage
```

### 2.2 Компоненты системы

| Компонент | Данные | API | Фронтенд |
|-----------|--------|-----|----------|
| Foundation | Встроен в `lessons.json` | Нет отдельного API | `FoundationBlock.tsx` в `LessonPage` |
| Glossary | `glossary.json` | `GET /glossary`, `GET /glossary/{id}` | `GlossaryPage.tsx`, `GlossaryLessonLinks.tsx` |
| Recap | `recaps.json` | `GET /recaps`, `GET /recaps/{id}` | `RecapPage.tsx`, ссылки в сайдбаре |
| Quest | `chapter_quests.json` | `GET /quests`, `GET /quests/{id}` | `QuestPage.tsx`, ссылки в сайдбаре |

---

## 3. Data Model

### 3.1 Foundation Block (в lessons.json)

Добавлено поле `foundation` в каждый урок:

```json
{
  "foundation": {
    "title": "Перед стартом",
    "terms": [
      {
        "term_id": "print",
        "label": "print()",
        "definition": "Функция, которая выводит текст на экран..."
      }
    ],
    "glossary_terms": ["print", "quotes", "string", "error", "syntax_error"],
    "rules": [
      "Текст в print() всегда берётся в кавычки",
      "Имена переменных пишутся без кавычек"
    ]
  }
}
```

- **Первые 9 уроков (1-1 до 1-9):** полные блоки с `terms` (определениями)
- **Остальные 83 урока:** блоки с `glossary_terms` (ссылками на глоссарий) и общими правилами

### 3.2 Glossary

Файл: `backend/app/data/glossary.json` (и `api/app/data/glossary.json`)

```json
{
  "id": "quotes",
  "term": "Кавычки",
  "python_name": "' ' / \" \"",
  "category": "basics",
  "simple_definition": "...",
  "analogy": "...",
  "code_example": "print(\"Привет\")",
  "common_mistake": "print(Привет)",
  "mistake_explanation": "...",
  "related_lessons": ["1-1", "1-2"],
  "beginner_level": "foundation"
}
```

Категории: `basics`, `strings`, `variables`, `numbers`, `conditions`, `loops`, `functions`, `lists`, `errors`, `style`

### 3.3 Recap

Файл: `backend/app/data/recaps.json`

```json
{
  "id": "recap-1",
  "part": 1,
  "title": "Напоминалка: Hello Python",
  "story_summary": "...",
  "learned_terms": ["print", "quotes", ...],
  "hero_skills": [
    {
      "name": "Голос героя",
      "python": "print()",
      "meaning": "Показать сообщение на экране",
      "analogy": "Герой произносит фразу вслух."
    }
  ],
  "key_rules": ["Текст в кавычках.", ...],
  "mini_check": [
    {
      "question": "Почему print(Привет) ломается?",
      "answer": "Без кавычек Python думает, что это переменная."
    }
  ]
}
```

### 3.4 Chapter Quest

Файл: `backend/app/data/chapter_quests.json`

```json
{
  "id": "quest-1",
  "part": 1,
  "title": "Финальный квест: Ворота Первого Храма",
  "story": "...",
  "required_lessons": ["1-1", ..., "1-9"],
  "required_constructs": ["print", "variable", "input", "int_call", "comparison", "if_else"],
  "task": "...",
  "starter_code": "",
  "example_solution": "...",
  "test_cases": [{"input": "...", "expected_contains": [...]}],
  "success_criteria": ["Используется input", ...],
  "hints": ["Сначала спроси имя через input()", ...]
}
```

---

## 4. Routes

| Route | Page | Layout | Описание |
|-------|------|--------|----------|
| `/glossary` | `GlossaryPage` | `Layout` (auth) | Список терминов с поиском и фильтрацией |
| `/recap/:id` | `RecapPage` | `Layout` (auth) | Напоминалка по разделу |
| `/quest/:id` | `QuestPage` | `Layout` (auth) | Финальный квест раздела |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/glossary` | GET | Список терминов (summary) |
| `/glossary/{id}` | GET | Полный термин |
| `/glossary/category/{cat}` | GET | Термины категории |
| `/recaps` | GET | Список рекапов |
| `/recaps/{id}` | GET | Полный рекап |
| `/quests` | GET | Список квестов |
| `/quests/{id}` | GET | Полный квест |

---

## 5. Как глоссарий связан с уроками

1. **Прямые ссылки:** У каждого термина в глоссарии есть `related_lessons` — массив ID уроков, где этот термин используется
2. **Lesson links:** Компонент `GlossaryLessonLinks` показывает на странице урока ссылки на релевантные термины
3. **Foundation:** Уроки 1-1 до 1-9 содержат `foundation.terms` — встроенные определения ключевых понятий
4. **Hash-anchor:** Ссылки вида `/glossary#print` прокручивают к соответствующему термину

---

## 6. Как устроены рекапы

Каждый рекап (recap) содержит:

1. **Story summary** — краткое описание пройденного материала в игровой форме
2. **Hero skills** — таблица навыков: что герой научился делать, какой Python-код для этого нужен, аналогия
3. **Key rules** — ключевые правила раздела (шпаргалка)
4. **Mini-check** — вопросы для самопроверки с ответами (на кнопке)
5. **CTA** — кнопка «Перейти к финальному квесту»

Рекапы доступны:
- Из сайдбара (секция «Повторение»)
- С главной страницы
- С последнего урока каждой части (через навигацию)

---

## 7. Как устроены финальные квесты

Каждый квест:

1. **Story** — игровое введение, связывающее все темы раздела
2. **Required lessons** — список уроков, которые нужно пройти
3. **Required constructs** — конструкции Python, которые нужно использовать
4. **Task** — подробное описание задачи (многошаговое)
5. **Code editor** — поле для ввода кода с starter_code
6. **Check** — проверка через `/mission/check` endpoint
7. **Hints** — пошаговые подсказки (раскрываются по кнопке)
8. **Example solution** — пример решения (после попытки)
9. **Success criteria** — чеклист того, что должно быть в коде

Квесты охватывают **минимум 3-6 конструкций Python** каждый, комбинируя темы раздела.

---

## 8. Роль Багуса

Багус — **инспектор ловушек / проводник по ошибкам**, а не случайный злодей.

- UI-лейблы: «Багус предупреждает», «Ловушка Багуса», «Типичная ошибка»
- Две реплики Багуса подряд в одном диалоге — запрещены (сливаются в одну)
- Реплики Багуса — конкретные, по делу, с юмором

---

## 9. Известные ограничения

1. **Quest code checking** — использует существующий `/mission/check` endpoint, который сравнивает вывод. Для точной проверки квестов с input() нужен улучшенный чекер (следующий слой)
2. **Static glossary links** — встроены через `foundation.glossary_terms`, а не через автоматический NLP-разбор текста урока
3. **Backend duplication** — данные дублируются между `backend/` и `api/` для Vercel-деплоя
4. **No progress tracking for recaps/quests** — текущий слой не отмечает рекапы и квесты как пройденные (следующий слой)
5. **Part 5 recap and quest** — созданы, но Part 5 состоит всего из 5 уроков, поэтому квест и рекап компактнее

---

## 10. Следующий рекомендованный слой

1. **Quest Checker V3** — полноценная проверка квестов через AST с тест-кейсами (input → output)
2. **Quest/Term Progress Tracking** — отмечать в прогресс пройденные квесты и просмотренные термины
3. **Auto-linking glossary terms in dialogues** — NLP для автоматического связывания терминов в диалогах
4. **Interactive analogies** — анимированные аналогии для ключевых понятий
5. **Part 5 expansion** — расширение Part 5 до полноценного раздела
