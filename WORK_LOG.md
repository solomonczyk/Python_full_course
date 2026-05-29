# Python Quest — Work Log

## Сессия 3: 2026-05-29

### ✅ Что сделано

#### Фаза 2 (завершена ✅)
- `scripts/generate_lessons.py`:
  - Добавлен `STORY_PLACEMENT_MAP` — 40+ шаблонов (topic → место в сюжете)
  - Добавлен `PRE_TOPIC_DIALOGUE_MAP` — 35 диалогов перед темой (формат DialogueLine[])
  - Добавлен `POST_ERROR_DIALOGUE_MAP` — 16 диалогов после ошибки
  - Добавлен `MINI_SUMMARY_MAP` — 40+ шаблонов мини-итогов (с fallback по part)
  - Добавлен `CONNECTION_TO_GAME_MAP` — 35+ шаблонов связи с финальной игрой (с fallback по part)
  - Функции: `get_story_placement()`, `get_pre_topic_dialogue()`, `get_post_error_dialogue()`, `get_mini_summary()`, `get_connection_to_game()`
  - `parse_lessons()`: обновлена — генерирует все 6 новых полей для каждого урока
  - `main()`: обновлён вывод статистики (D/S/C колонки)
- Регенерирован `api/app/data/lessons.json` — все 86 уроков с новыми полями
- TypeScript build: 0 ошибок

### 📊 Покрытие новых полей

| Поле                    | Покрытие       |
|-------------------------|----------------|
| `story_placement`       | 86/86 (100%)   |
| `pre_topic_dialogue`    | 86/86 (100%)   |
| `post_error_dialogue`   | 86/86 (100%)   |
| `game_relevance`        | 86/86 (100%)   |
| `mini_summary`          | 86/86 (100%)   |
| `connection_to_game`    | 86/86 (100%)   |


#### Детали архитектуры fallback

- **Tier 1** — topic-specific: прямой матчинг по шаблону (regex / substring)
- **Tier 2** — category-specific: групповые шаблоны для смежных тем (float&деление, ссылки&копирование, макс/мин, чат-бот/таск-менеджер)
- **Tier 3** — part-specific: контекст части (1-4) с генерацией через `_infer_part_from_combined()`
- **Tier 4** — hard fallback: emergency-диалог/текст, никогда не возвращает None

### 🛠 Инструменты

- `scripts/verify_coverage.py` — проверка 100% покрытия + TypeScript build + JSON-отчёт (`coverage_report.json`)

### 📋 Текущий статус
- Проект стабилен, все 86 уроков работают, TypeScript 0 ошибок
- Фаза 1 ✅ (типы)
- Фаза 2 ✅ (генератор контента)
- Фазы 3-7 не начаты

### ▶️ С чего продолжить
1. **Фаза 3**: 5 новых UI компонентов:
   - `GameRelevanceBlock` — зачем тема нужна для финальной игры
   - `DialogueScene` — мультиперсонажные диалоги
   - `MiniSummaryBlock` — мини-итог урока
   - `StoryPlacementBlock` — место в истории
   - `ConnectionToGameBlock` — связь с будущей игрой
2. **Фаза 4**: обновить LessonPage с новыми блоками

## Последняя сессия: 2026-05-28

### ✅ Что сделано

#### 1. Реализованы все 86 уроков (части 1-4)
- Создан `scripts/generate_lessons.py` — парсер curriculum markdown (5000+ строк)
- Сгенерирован `api/app/data/lessons.json` — с 7 → 86 уроков (+4834 строк)
- Каждый урок содержит: explanation, quiz, what_outputs, find_bug, mission
- Все уроки разблокированы (locked=false)
- Все API endpoints работают, фронтенд собирается с 0 ошибок TypeScript

#### 2. Исправления
- Sidebar: индикатор активного урока через box-shadow (вместо border, чтобы не было layout shift)
- HomePage: добавлена метка Part 4 "Башня алгоритмов"

#### 3. Коммиты и пуш
- `6cca77e` — sidebar shadow fix
- `90f7779` — 86-lesson curriculum
- Всё запущено на GitHub

---

### 📋 Текущий статус

Проект в стабильном состоянии:
- 86 уроков, 4 части, полный курс
- Все уроки доступны, прогресс сохраняется
- AI-чат работает (DeepSeek API)

---

### 🗺️ Что предстоит (Scenario Pack v2)

На основе `python_quest_full_dialogue_scenario_pack.md` — план переработки курса под единую цель "финальная консольная игра".

План разбит на **7 фаз** (всего ~22 часа работы):

#### Фаза 1 — Типы данных
- Добавить `game_relevance`, `dialogue`, `summary`, `story` поля в TypeScript типы
- Все поля опциональные (обратная совместимость)
- Новый интерфейс `DialogueLine`

#### Фаза 2 — Генератор контента
- Шаблоны `game_relevance` для каждого топика (по аналогии с QUIZ_TEMPLATES)
- Обновлённый парсер секций (0-6 + story + game relevance)
- Регенерация lessons.json

#### Фаза 3 — Новые компоненты
- `GameRelevanceBlock` — зачем тема нужна для финальной игры
- `DialogueScene` — мультиперсонажные диалоги
- `MiniSummaryBlock` — мини-итог урока
- `StoryPlacementBlock` — место в истории
- `ConnectionToGameBlock` — связь с будущей игрой

#### Фаза 4 — Обновление LessonPage
- Вставить новые блоки между существующими секциями
- Навигация через границы частей → PartTransitionPage
- Все новые секции опциональны

#### Фаза 5 — Мини-игры (4 шт.)
- **Part 1:** "Проверка героя" — имя, возраст, сила, рейтинг, if/else
- **Part 2:** "Кубик судьбы" — выбор кубика, random, ходы
- **Part 3:** "Инвентарь героя" — предметы, инвентарь, ключ
- **Part 4:** "Побег из Башни Багуса" — полная text adventure

#### Фаза 6 — Маршрутизация
- `/transition/:part` — страницы переходов между частями
- `/mini-game/*` — 4 маршрута для мини-игр

#### Фаза 7 — QA
- TypeScript build check
- Ручное тестирование всех уроков и мини-игр

---

### ▶️ С чего продолжить

**Фаза 1: Типы данных** — самый безопасный старт, не ломает существующий код.

1. Открыть `frontend/src/types/index.ts`
2. Добавить `DialogueLine` interface
3. Добавить опциональные поля в `Lesson` (game_relevance, pre_topic_dialogue, post_error_dialogue, mini_summary, connection_to_game, story_placement)

Параллельно можно начинать **Фазу 2**:
- Обновить `scripts/generate_lessons.py`
- Добавить GAME_RELEVANCE_MAP (topic → текст)
- Обновить парсер секций
- Регенерировать lessons.json

### Ключевые файлы

| Файл | Роль |
|---|---|
| `scripts/generate_lessons.py` | Генератор уроков из markdown |
| `api/app/data/lessons.json` | Все 86 уроков |
| `frontend/src/types/index.ts` | TypeScript типы |
| `frontend/src/pages/LessonPage.tsx` | Страница урока |
| `frontend/src/components/` | Все UI компоненты |
| `python_quest_full_dialogue_scenario_pack.md` | Сценарный пакет v2 (что внедряем) |
