# Python Quest

Интерактивный курс Python в формате ролевой игры — с персонажами Ксю, Ва, Да и Багусом.

## Стек

| Слой | Технология |
|------|-----------|
| Бэкенд | FastAPI + SQLite |
| Фронтенд | React 18 + Vite + TailwindCSS |
| Язык | Python 3.11+ / TypeScript |

## Структура

```
Python_full_course/
  backend/
    app/
      main.py          # FastAPI entrypoint
      routers/
        lessons.py     # GET /lessons, GET /lessons/{id}
        progress.py    # GET/POST /progress
        quiz.py        # POST /quiz/check, /quiz/what-outputs
      data/
        lessons.json   # Данные всех уроков
      database.py      # SQLite init + connection
      models.py        # Pydantic models
    requirements.txt
    pyproject.toml
  frontend/
    src/
      components/      # TopNav, Sidebar, DialogueBubble, CodeBlock, QuizSection, MissionCard
      pages/           # HomePage, LessonPage
      hooks/           # useApi.ts (fetch helpers)
      types/           # TypeScript типы
    index.html
    vite.config.ts
    tailwind.config.js
```

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

API доступен на `http://127.0.0.1:8000`  
Документация: `http://127.0.0.1:8000/docs`

### Фронтенд

```bash
cd frontend
npm install
npm run dev
```

Фронтенд на `http://localhost:5173` — запросы к API проксируются через Vite на порт 8000.

## API эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/lessons` | Список всех уроков (без деталей) |
| GET | `/lessons/{id}` | Полный урок с квизом и миссией |
| GET | `/progress` | Весь прогресс пользователя |
| POST | `/progress` | Обновить прогресс урока |
| DELETE | `/progress/{id}` | Сбросить прогресс урока |
| POST | `/quiz/check` | Проверить ответ на квиз |
| POST | `/quiz/what-outputs` | Проверить "что выведет код?" |

## Персонажи

- **Ксю** `#74B9FF` — объясняет просто и спокойно
- **Ва** `#A29BFE` — строгий мастер логики
- **Да** `#28A745` — игровой мастер, миссии и задачи
- **Багус** `#FF7675` — злодей ошибок, подсвечивает баги
