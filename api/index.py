import json
import os
import sqlite3
import subprocess
import tempfile
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── paths ──────────────────────────────────────────────────────────────────
_HERE = Path(__file__).parent
_LESSONS_FILE = _HERE / "app" / "data" / "lessons.json"
_DB_PATH = Path(os.environ.get("DB_PATH", "/tmp/progress.db"))

# ── models ─────────────────────────────────────────────────────────────────
class ProgressUpdate(BaseModel):
    lesson_id: str
    completed: bool
    score: Optional[int] = None

class QuizAnswer(BaseModel):
    lesson_id: str
    answer_id: str

class ChatMessage(BaseModel):
    message: str
    lesson_id: str | None = None

class MissionSubmit(BaseModel):
    lesson_id: str
    code: str

# ── db ─────────────────────────────────────────────────────────────────────
_db_ready = False

def _ensure_db() -> None:
    global _db_ready
    if _db_ready:
        return
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            lesson_id TEXT PRIMARY KEY,
            completed INTEGER NOT NULL DEFAULT 0,
            score INTEGER,
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()
    _db_ready = True

@contextmanager
def _db() -> sqlite3.Connection:
    _ensure_db()
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# ── lessons ────────────────────────────────────────────────────────────────
def _lessons() -> list[dict[str, Any]]:
    with open(_LESSONS_FILE, encoding="utf-8") as f:
        return json.load(f)

# ── app ────────────────────────────────────────────────────────────────────
app = FastAPI(title="Python Quest API", version="1.0.0")

_extra = os.environ.get("ALLOWED_ORIGIN", "")
_production_origin = os.environ.get("PRODUCTION_ORIGIN", "")
_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    *([_extra] if _extra else []),
    *([_production_origin] if _production_origin else []),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_origin_regex=r"https://python-full-course.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── middleware: fix Vercel path rewrites ───────────────────────────────────
class VercelPathMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            # Handle Vercel rewrite paths
            if path.startswith("/api/index/"):
                scope["path"] = path[len("/api/index"):]  # /api/index/lessons -> /lessons
            elif path == "/api/index":
                scope["path"] = "/"
            elif path.startswith("/api/"):
                scope["path"] = path[4:]  # /api/lessons -> /lessons
            elif path == "/api":
                scope["path"] = "/"
        return await self.app(scope, receive, send)

app.add_middleware(VercelPathMiddleware)

# ── routes: lessons ────────────────────────────────────────────────────────
@app.get("/lessons")
def list_lessons() -> list[dict[str, Any]]:
    SUMMARY_FIELDS = ("id","part","chapter","lesson","slug","title","subtitle",
                      "topic","locked","difficulty","estimated_time_min")
    return [
        {k: l[k] for k in SUMMARY_FIELDS if k in l}
        | ({"scene_image": l["scene_image"]} if "scene_image" in l and l.get("scene_image") else {})
        for l in _lessons()
    ]

@app.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str) -> dict[str, Any]:
    for l in _lessons():
        if l["id"] == lesson_id:
            return {k: v for k, v in l.items() if v is not None or k != "scene_image"}
    raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")

# ── routes: progress ───────────────────────────────────────────────────────
@app.get("/progress")
def get_progress() -> list[dict[str, Any]]:
    with _db() as conn:
        rows = conn.execute("SELECT * FROM progress").fetchall()
    return [dict(r) for r in rows]

@app.post("/progress")
def update_progress(body: ProgressUpdate) -> dict[str, Any]:
    with _db() as conn:
        conn.execute(
            """INSERT INTO progress (lesson_id, completed, score)
               VALUES (?, ?, ?)
               ON CONFLICT(lesson_id) DO UPDATE SET
                 completed=excluded.completed,
                 score=excluded.score,
                 updated_at=datetime('now')""",
            (body.lesson_id, int(body.completed), body.score),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM progress WHERE lesson_id=?", (body.lesson_id,)).fetchone()
    return dict(row)

@app.delete("/progress/{lesson_id}")
def reset_progress(lesson_id: str) -> dict[str, str]:
    with _db() as conn:
        conn.execute("DELETE FROM progress WHERE lesson_id=?", (lesson_id,))
        conn.commit()
    return {"status": "reset", "lesson_id": lesson_id}

# ── routes: quiz ───────────────────────────────────────────────────────────
@app.post("/quiz/check")
def check_quiz(body: QuizAnswer) -> dict[str, Any]:
    lesson = next((l for l in _lessons() if l["id"] == body.lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    quiz = lesson.get("quiz")
    if not quiz:
        raise HTTPException(status_code=400, detail="No quiz in this lesson")
    correct = next((o for o in quiz["options"] if o["correct"]), None)
    return {
        "correct": bool(correct and correct["id"] == body.answer_id),
        "correct_id": correct["id"] if correct else None,
        "explanation": correct["text"] if correct else None,
    }

@app.post("/quiz/what-outputs")
def check_what_outputs(body: QuizAnswer) -> dict[str, Any]:
    lesson = next((l for l in _lessons() if l["id"] == body.lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    wo = lesson.get("what_outputs")
    if not wo:
        raise HTTPException(status_code=400, detail="No what_outputs in this lesson")
    return {
        "correct": wo["correct"] == body.answer_id,
        "correct_answer": wo["correct"],
    }

# ── routes: mission check ───────────────────────────────────────────────
_FORBIDDEN_IMPORTS = [
    "import os", "import sys", "import subprocess",
    "import socket", "__import__", "exec(", "eval(",
    "import shutil", "import pathlib", "import requests",
]

@app.post("/mission/check")
def check_mission(body: MissionSubmit) -> dict[str, Any]:
    lesson = next((l for l in _lessons() if l["id"] == body.lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    mission = lesson.get("mission")
    if not mission:
        raise HTTPException(status_code=400, detail="No mission in this lesson")
    expected = mission["expected_output"].strip()

    code_lower = body.code.lower()
    for forbidden in _FORBIDDEN_IMPORTS:
        if forbidden in code_lower:
            return {
                "correct": False,
                "actual_output": None,
                "expected_output": expected,
                "error": "Использование запрещённых модулей не допускается",
            }

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(body.code)
            tmp_path = f.name

        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=5,
            env={"PATH": "/usr/bin:/bin"},
        )

        actual = result.stdout.strip()
        stderr = result.stderr.strip()
        first_line = actual.split("\n")[0] if actual else ""
        correct = first_line == expected or actual == expected

        return {
            "correct": correct,
            "actual_output": actual,
            "expected_output": expected,
            "error": stderr if not correct and stderr else None,
        }
    except subprocess.TimeoutExpired:
        return {
            "correct": False,
            "actual_output": None,
            "expected_output": expected,
            "error": "Превышено время выполнения (5 сек). Проверь, нет ли бесконечного цикла",
        }
    except Exception as e:
        return {
            "correct": False,
            "actual_output": None,
            "expected_output": expected,
            "error": str(e),
        }
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

# ── routes: reviews ─────────────────────────────────────────────────────
_REVIEWS_FILE = _HERE / "app" / "data" / "review_schedule.json"

def _load_reviews() -> dict:
    if not _REVIEWS_FILE.exists():
        return {"total_reviews": 0, "reviews": []}
    with open(_REVIEWS_FILE, encoding="utf-8") as f:
        return json.load(f)

@app.get("/reviews")
def list_reviews() -> list[dict[str, Any]]:
    data = _load_reviews()
    results = []
    for r in data.get("reviews", []):
        results.append({
            "id": r["id"],
            "type": r["type"],
            "title": r["title"],
            "subtitle": r["subtitle"],
            "position_after": r["position_after"],
            "part": r["part"],
            "chapter": r["chapter"],
            "topics": r["topics"],
        })
    return results

@app.get("/reviews/{review_id}")
def get_review(review_id: str) -> dict[str, Any]:
    data = _load_reviews()
    for r in data.get("reviews", []):
        if r["id"] == review_id:
            return r
    raise HTTPException(status_code=404, detail=f"Review {review_id} not found")

# ── AI chat ────────────────────────────────────────────────────────────────
_AI_ENDPOINT = os.environ.get("DEEPSEEK_API_ENDPOINT", "https://api.deepseek.com/v1/chat/completions")
_AI_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

_FALLBACK_RESPONSES: dict[str, str] = {
    "print": "`print()` выводит данные в консоль. Пример: `print('Hello, World!')`",
    "input": "`input()` читает строку от пользователя. Пример: `name = input('Как тебя зовут? ')`",
    "variable": "Переменные хранят данные. Пример: `name = 'Ксю'` — теперь в name лежит строка 'Ксю'.",
    "if": "`if` проверяет условие. Пример: `if x > 5: print('Больше 5')`",
    "else": "`else` — ветка, которая выполняется, если условие if ложно. Пример: `if x > 5: ... else: ...`",
    "elif": "`elif` = else if. Позволяет проверить несколько условий подряд.",
    "for": "`for i in range(n):` повторяет код n раз. Пример: `for i in range(3): print(i)`",
    "range": "`range(start, stop, step)` генерирует последовательность чисел.",
    "while": "`while условие:` выполняет код, пока условие истинно. Будь осторожен с бесконечными циклами!",
    "list": "Список — упорядоченная коллекция. `items = [1, 2, 3]`. Индексация с нуля.",
    "def": "`def имя_функции():` создаёт функцию. Пример: `def greet(): print('Привет!')`",
    "return": "`return` возвращает значение из функции. Без return функция вернёт None.",
    "class": "Классы — чертежи для объектов. `class Hero: def __init__(self, name): self.name = name`",
    "string": "Строки — текст в кавычках. Можно складывать: `'Hello' + ' ' + 'World'`",
    "f-string": "f-строки подставляют значения: `f'Привет, {name}!'`",
    "import": "`import random` импортирует модуль. `random.randint(1, 10)` — случайное число от 1 до 10.",
}

def _fallback_reply(message: str) -> str:
    msg_lower = message.lower()
    for keyword, reply in _FALLBACK_RESPONSES.items():
        if keyword in msg_lower:
            explanations = {
                "не работает": "Проверь синтаксис: двоеточия после if/for/def, отступы (4 пробела), закрытые кавычки.",
                "ошибк": "NameError — переменная не определена. TypeError — несовместимые типы. SyntaxError — ошибка в синтаксисе.",
            }
            for ek, ev in explanations.items():
                if ek in msg_lower:
                    return ev + "\n\n" + reply
            return reply
    return ("Я — Python-эксперт из Python Quest. Задай мне вопрос по Python: "
            "как работает функция, как исправить ошибку, что значит этот код. "
            "Постараюсь помочь! Если вопрос сложный — попроси Ксю подключить API-ключ для доступа к полной версии.")

GUARD_PROMPT = "You are a Python expert tutor in the Python Quest interactive course. Answer clearly and concisely in Russian. Provide code examples where helpful."

@app.post("/ai/chat")
def ai_chat(body: ChatMessage) -> dict[str, str]:
    system_prompt = GUARD_PROMPT
    if body.lesson_id:
        lesson = next((l for l in _lessons() if l["id"] == body.lesson_id), None)
        if lesson:
            lesson_ctx = (
                f"\nCurrent lesson: {lesson['title']} — {lesson.get('topic', '')}. "
                f"Explanation: {lesson['explanation']['text']} "
                f"Example: {lesson['explanation']['code_example']}"
            )
            system_prompt += lesson_ctx

    if _AI_KEY:
        try:
            payload = json.dumps({
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": body.message},
                ],
                "max_tokens": 1024,
                "temperature": 0.7,
            }).encode()
            req = urllib.request.Request(
                _AI_ENDPOINT,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {_AI_KEY}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            reply = data["choices"][0]["message"]["content"]
            return {"reply": reply}
        except Exception as e:
            return {"reply": f"Ошибка подключения к AI: {e}\n\nИспользую встроенную базу знаний:\n\n{_fallback_reply(body.message)}"}
    return {"reply": _fallback_reply(body.message)}


# ── health ─────────────────────────────────────────────────────────────────
@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


# ── Vercel ASGI handler ────────────────────────────────────────────────────
# Export app for Vercel serverless runtime
__all__ = ["app"]
