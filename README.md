# Python Quest

Интерактивный RPG-курс по основам Python.  
С персонажами Ксю, Ва, Да и Багусом.  
92 урока, 5 частей, 18 глав.

**Деплой:** https://python-full-course.vercel.app  
**Репозиторий:** https://github.com/solomonczyk/Python_full_course

---

## Для кого этот курс

| | |
|---|---|
| **Входной уровень** | Абсолютный ноль. Опыт программирования не требуется |
| **Выходной уровень** | **A2+** — пишешь текстовые программы, игры, простую автоматизацию |
| **Возраст** | 12 лет и старше |
| **Язык** | Русский |
| **Время прохождения** | ~15–20 часов |
| **Формат** | Самостоятельно, в удобном темпе |

### После прохождения ты сможешь:

- Написать программу на Python с нуля
- Работать с числами, строками, списками и словарями
- Строить логику: условия, циклы, флаги, функции
- Написать чат-бот, игру, таск-менеджер
- Понимать чужой код и разбираться в памяти Python (ссылки, копирование)

### Чего курс НЕ покрывает:

| Направление | Что изучать дальше |
|---|---|
| Функции и ООП глубже | [Stepik: Python для начинающих](https://stepik.org/course/67) |
| Веб-разработка | [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) |
| Анализ данных | [Kaggle Python](https://www.kaggle.com/learn/python) |
| Алгоритмы | [LeetCode (Easy)](https://leetcode.com/problemset/all/) |
| Автоматизация | [Automate the Boring Stuff](https://automatetheboringstuff.com/) |

---

## Программа курса

| Часть | Главы | Темы | Уроков |
|-------|-------|------|--------|
| **1. Основы** | 1-2 | print, строки, переменные, input, арифметика, if/else | 9 |
| **2. Ветвления и random** | 3-5 | elif, логические цепочки, random, for, range | 6 |
| **3. Типы данных и коллекции** | 6-11, 18 | числа, bool, списки, строки, методы, срезы, random | 41 |
| **4. Алгоритмы и проекты** | 12-17 | флаги, break, join/split, map/sort, while, чат-бот | 31 |
| **5. Функции и продвинутое** | 19 | def, параметры, return, dict, try/except | 5 |

---

## Стек

| Слой | Технология |
|------|-----------|
| Бэкенд | FastAPI + SQLite / Turso (Serverless) |
| Фронтенд | React 18 + Vite + TailwindCSS + TypeScript |
| Интерпретатор | Pyodide (WebAssembly — Python в браузере) |
| Деплой | Vercel (Serverless Functions + Static) |

## Структура

```
Python_full_course/
  backend/
    app/
      main.py              # FastAPI entrypoint
      database.py          # SQLite/Turso connection
      models.py            # Pydantic models
      data/lessons.json    # Все 92 урока (87 исходных + 5 новых)
      routers/
        lessons.py         # GET /lessons, GET /lessons/{id}
        progress.py        # GET/POST /progress (с user_id)
        quiz.py            # POST /quiz/check
        mission.py         # POST /mission/check
    requirements.txt
    .env.example
  frontend/
    src/
      components/          # TopNav, Sidebar, CodePlayground, CourseMap, Certificate...
      pages/               # OnboardingPage, HomePage, LessonPage, CompletionPage
      hooks/               # useApi.ts, useProgress.ts, ProgressContext.tsx
      utils/userId.ts      # Анонимная идентификация
      types/index.ts       # TypeScript-типы
    package.json
  api/index.py             # Vercel entrypoint
  .github/workflows/       # CI/CD
```

## Персонажи

| Персонаж | Цвет | Роль |
|----------|------|------|
| **Ксю** `#74B9FF` | Объясняет просто, через аналогии |
| **Ва** `#A29BFE` | Мастер логики, технические детали |
| **Да** `#28A745` | Игровой мастер, даёт миссии |
| **Багус** `#FF7675` | Злодей-баг, подсвечивает ошибки |
| **Новичок** `#9b98a8` | Ученик, задаёт вопросы |

## Запуск

### Бэкенд

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API на `http://127.0.0.1:8000`  
Документация: `http://127.0.0.1:8000/docs`

### Фронтенд

```bash
cd frontend
npm install
npm run dev
```

Фронтенд на `http://localhost:5173` — запросы к API проксируются на порт 8000.

### Проверка типов

```bash
cd frontend && npm run type-check
```

### Тесты

```bash
cd backend && python -m pytest tests/ -v
```

## Переменные окружения

| Переменная | Где | Описание |
|---|---|---|
| `TURSO_DATABASE_URL` | backend | URL Turso базы данных (если не задан — SQLite) |
| `TURSO_AUTH_TOKEN` | backend | Токен доступа к Turso |
| `DB_PATH` | backend | Путь к SQLite (по умолчанию `/tmp/progress.db`) |
| `ALLOWED_ORIGIN` | backend | Дополнительный origin для CORS |
| `DEEPSEEK_API_KEY` | backend | Ключ DeepSeek для AI-чата (опционально) |

## Идентификация пользователя

Каждый пользователь получает анонимный UUID при первом визите (хранится в `localStorage`).  
UUID передаётся в заголовке `X-User-Id` при каждом запросе к API.  
Прогресс привязан к `user_id` — два пользователя не влияют друг на друга.

**Для production (Vercel):** требуется Turso или другая персистентная БД.  
Без Turso прогресс хранится в `localStorage` браузера как запасной вариант.

## API эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/lessons` | Список всех уроков |
| GET | `/lessons/{id}` | Полный урок |
| GET | `/progress` | Прогресс пользователя (требует `X-User-Id`) |
| POST | `/progress` | Обновить прогресс |
| POST | `/quiz/check` | Проверить ответ квиза |
| POST | `/quiz/what-outputs` | Проверить "что выведет код" |
| POST | `/mission/check` | Проверить код миссии |

## Оценка курса

| Параметр | Оценка | Комментарий |
|----------|--------|-------------|
| Методика объяснений | ⭐⭐⭐⭐⭐ | Система аналогий — лучшее в курсе |
| Охват тем (база) | ⭐⭐⭐⭐⭐ | 92 урока, 5+ новых тем (функции, dict, try/except) |
| Структура урока | ⭐⭐⭐⭐⭐ | 18-блочная структура с диалогами и разборами кода |
| Практика | ⭐⭐⭐⭐☆ | Квизы, find_bug, миссии, CodePlayground (Pyodide) |
| Мотивация / геймификация | ⭐⭐⭐⭐⭐ | RPG-нарратив, персонажи, карта курса, прогресс-бар |
| Онбординг | ⭐⭐⭐⭐☆ | 3 вопроса при входе, индивидуальный темп |
| Что после курса | ⭐⭐⭐⭐☆ | Роадмап в CompletionPage + README |
| Доступность (A11y) | ⭐⭐⭐☆☆ | Базовый уровень |

## Анализ содержания

### Статистика уроков

| Параметр | Значение |
|----------|----------|
| Всего уроков | 92 |
| Часть 1 (Основы) | 9 |
| Часть 2 (Ветвления и random) | 6 |
| Часть 3 (Типы данных и коллекции) | 41 |
| Часть 4 (Алгоритмы и проекты) | 31 |
| Часть 5 (Функции и продвинутое) | 5 |
| Глубоких (deep) | 18 |
| Достаточных (sufficient) | 51 |
| Поверхностных (superficial) | 23 |

### Матрица покрытия тем

#### Block A — Basics (База)

| Тема | Статус |
|------|--------|
| install | ❌ absent |
| types | ✅ present |
| int | ✅ present |
| float | ✅ present |
| str | ✅ present |
| bool | ✅ present |
| variables | ✅ present |
| arithmetic | ✅ present |
| input() | ✅ present |
| print() | ✅ present |
| if/elif/else | ✅ present |
| for/range | ✅ present |
| while | ✅ present |
| break/continue | ✅ present |
| functions (def/parameters/return) | ✅ present |
| scope | ❌ absent |
| string methods/slices | ✅ present |

#### Block B — Data Structures (Структуры данных)

| Тема | Статус |
|------|--------|
| list | ✅ present |
| tuple | ⚠️ mentioned briefly |
| dict | ✅ present |
| set | ❌ absent |
| nested structures | ✅ present |
| list comprehension | ⚠️ mentioned briefly |
| dict comprehension | ❌ absent |

#### Block C — OOP & Modules (ООП и модули)

| Тема | Статус |
|------|--------|
| classes | ❌ absent |
| inheritance | ❌ absent |
| magic methods | ❌ absent |
| exceptions | ✅ present |
| file I/O | ❌ absent |
| import | ✅ present |
| std library | ⚠️ mentioned briefly |
| pip | ❌ absent |

#### Block D — Advanced (Продвинутое)

| Тема | Статус |
|------|--------|
| decorators | ❌ absent |
| generators | ❌ absent |
| lambda | ⚠️ mentioned briefly |
| map/filter/zip | ✅ present |
| *args/**kwargs | ❌ absent |
| context managers | ❌ absent |
| type hints | ❌ absent |
| async | ❌ absent |

### Проверка качества

Чеклист качества пройден: **92 / 92** пунктов (0 ошибок).  
Все уроки содержат код, квиз и миссию. Каждый урок проходит валидацию структуры, соответствие шаблону и наличие всех обязательных секций.

## CI/CD

При push/PR запускаются:
- `ruff check backend/app/` — линтинг Python
- `cd frontend && npm run type-check` — проверка TypeScript

---

*Python Quest v2.0 — Полный аудит: май 2026. Отчёт: [docs/full_audit_report_2026-05-31.md](docs/full_audit_report_2026-05-31.md)*
