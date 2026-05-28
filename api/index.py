import json
import os
import sqlite3
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

def _db() -> sqlite3.Connection:
    _ensure_db()
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

# ── lessons ────────────────────────────────────────────────────────────────
def _lessons() -> list[dict[str, Any]]:
    with open(_LESSONS_FILE, encoding="utf-8") as f:
        return json.load(f)

# ── app ────────────────────────────────────────────────────────────────────
app = FastAPI(title="Python Quest API", version="1.0.0")

_extra = os.environ.get("ALLOWED_ORIGIN", "")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", *([_extra] if _extra else [])],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── routes: lessons ────────────────────────────────────────────────────────
@app.get("/api/lessons")
def list_lessons() -> list[dict[str, Any]]:
    return [
        {k: l[k] for k in ("id","part","chapter","lesson","slug","title","subtitle","topic","locked")}
        for l in _lessons()
    ]

@app.get("/api/lessons/{lesson_id}")
def get_lesson(lesson_id: str) -> dict[str, Any]:
    for l in _lessons():
        if l["id"] == lesson_id:
            return l
    raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")

# ── routes: progress ───────────────────────────────────────────────────────
@app.get("/api/progress")
def get_progress() -> list[dict[str, Any]]:
    with _db() as conn:
        rows = conn.execute("SELECT * FROM progress").fetchall()
    return [dict(r) for r in rows]

@app.post("/api/progress")
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

@app.delete("/api/progress/{lesson_id}")
def reset_progress(lesson_id: str) -> dict[str, str]:
    with _db() as conn:
        conn.execute("DELETE FROM progress WHERE lesson_id=?", (lesson_id,))
        conn.commit()
    return {"status": "reset", "lesson_id": lesson_id}

# ── routes: quiz ───────────────────────────────────────────────────────────
@app.post("/api/quiz/check")
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

@app.post("/api/quiz/what-outputs")
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

# ── health ─────────────────────────────────────────────────────────────────
@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
