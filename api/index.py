import json
import os
import sqlite3
import subprocess
import tempfile
import urllib.request
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── paths ──────────────────────────────────────────────────────────────────
_HERE = Path(__file__).parent
_LESSONS_FILE = _HERE / "app" / "data" / "lessons.json"
_QUESTS_FILE = _HERE / "app" / "data" / "quests.json"
_RECAPS_FILE = _HERE / "app" / "data" / "recaps.json"
_DB_PATH = Path(os.environ.get("DB_PATH", "/tmp/progress.db"))

# ── models ─────────────────────────────────────────────────────────────────
class ProgressUpdate(BaseModel):
    lesson_id: str
    completed: bool = False
    quiz_passed: bool = False
    mission_done: bool = False
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

class BetaFeedbackRequest(BaseModel):
    """Feedback submission body for beta staged access."""
    feedback_text: str
    rating: int | None = None

# ── db ─────────────────────────────────────────────────────────────────────
_db_ready = False
_db_backend: str | None = None  # 'turso' or 'sqlite' once resolved

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL", "")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN", "")

# Production operator key for staged beta access control.
# In production, this MUST be overridden via Vercel env (never default).
OPERATOR_KEY = os.environ.get("OPERATOR_KEY", "op-python-quest-dev-2026")

# Environment detection: Vercel sets VERCEL_ENV=production for production deploys.
_ENVIRONMENT = os.environ.get("VERCEL_ENV", os.environ.get("APP_ENV", "development"))


def _resolve_backend() -> str:
    """Determine which persistence backend is active.

    Returns 'turso' if Turso/libsql is configured and importable.
    Returns 'sqlite' in non-production environments if Turso is unavailable.
    Raises RuntimeError in production if Turso cannot be used.
    """
    global _db_backend
    if _db_backend is not None:
        return _db_backend

    is_production = _ENVIRONMENT == "production"

    if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
        try:
            import libsql_experimental as libsql  # type: ignore
            conn = libsql.connect(TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
            conn.execute("SELECT 1")
            conn.close()
            _db_backend = "turso"
            return _db_backend
        except ImportError:
            if is_production:
                raise RuntimeError(
                    "Turso/libsql configured but libsql-experimental package is not installed. "
                    "Cannot fall back to /tmp SQLite in production."
                )
            _db_backend = "sqlite"
            return _db_backend
        except Exception as exc:
            if is_production:
                raise RuntimeError(
                    f"Turso configured but connection failed: {exc}. "
                    "Cannot fall back to /tmp SQLite in production."
                ) from exc
            _db_backend = "sqlite"
            return _db_backend

    # No Turso credentials configured
    if is_production:
        raise RuntimeError(
            "TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are not set. "
            "Production requires Turso for persistent progress storage. "
            "Cannot fall back to ephemeral /tmp SQLite."
        )

    _db_backend = "sqlite"
    return _db_backend


def get_backend_status() -> dict[str, object]:
    """Return current persistence backend status without exposing secrets."""
    try:
        backend = _resolve_backend()
        persistent = backend == "turso"
        safe = persistent
        error = None
    except RuntimeError as e:
        backend = "unavailable"
        persistent = False
        safe = False
        error = str(e)

    return {
        "backend": backend,
        "environment": _ENVIRONMENT,
        "persistent_storage": persistent,
        "sqlite_tmp_fallback": False,
        "safe_for_beta_progress": safe,
        "error": error,
    }


def get_connection() -> sqlite3.Connection:
    """Return a database connection to the resolved backend.

    In production, raises RuntimeError if Turso is not available
    (fail-closed). In development, falls back to local SQLite.
    """
    backend = _resolve_backend()
    _ensure_db()

    if backend == "turso":
        import libsql_experimental as libsql  # type: ignore
        raw = libsql.connect(TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
        # Wrap so that execute() returns dicts (libsql returns tuples by default)
        conn = _TursoDictConnection(raw)
        return conn

    # backend == "sqlite" (only reached in dev/test)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


class _TursoDictCursor:
    """Wraps a libsql cursor to convert tuple rows to dicts."""
    def __init__(self, cursor: Any):
        self._cursor = cursor
        self._description = None
        try:
            self._description = cursor.description
        except Exception:
            pass

    @property
    def description(self) -> Any:
        return self._description

    def fetchone(self) -> dict[str, Any] | None:
        row = self._cursor.fetchone()
        if row is None or not self._description:
            return row
        cols = [c[0] for c in self._description]
        return dict(zip(cols, row))

    def fetchall(self) -> list[dict[str, Any]]:
        rows = self._cursor.fetchall()
        if not rows or not self._description:
            return rows
        cols = [c[0] for c in self._description]
        return [dict(zip(cols, row)) for row in rows]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._cursor, name)


class _TursoDictConnection:
    """Wraps a libsql connection so execute() returns dict-row cursors."""
    def __init__(self, conn: Any):
        self._conn = conn

    def execute(self, sql: str, params: tuple | list | None = None) -> _TursoDictCursor:
        cursor = self._conn.execute(sql, params or ())
        return _TursoDictCursor(cursor)

    def commit(self) -> None:
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._conn, name)


def _ensure_dict(row: Any) -> dict[str, Any]:
    """Convert a DB result row to dict (works with sqlite3.Row and libsql rows)."""
    if row is None:
        return {}
    if isinstance(row, dict):
        return row
    if hasattr(row, "keys"):
        return dict(row)
    if isinstance(row, (tuple, list)):
        # Fallback: plain tuple — try to use .description from a known cursor
        # (shouldn't normally happen, but defend against it)
        return {f"col{i}": v for i, v in enumerate(row)}
    return {"value": row}


def _ensure_db() -> None:
    global _db_ready
    if _db_ready:
        return

    backend = _db_backend
    if backend is None:
        backend = _resolve_backend()

    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    schema = """
        CREATE TABLE IF NOT EXISTS progress (
            user_id TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            quiz_passed INTEGER NOT NULL DEFAULT 0,
            mission_done INTEGER NOT NULL DEFAULT 0,
            score INTEGER,
            updated_at TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (user_id, lesson_id)
        )
    """

    if backend == "turso":
        import libsql_experimental as libsql  # type: ignore
        conn = libsql.connect(TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
        conn.execute(schema)
        conn.commit()
        conn.close()
    elif backend == "sqlite":
        conn = sqlite3.connect(str(_DB_PATH))
        conn.execute(schema)
        try:
            conn.execute("SELECT user_id FROM progress LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("DROP TABLE IF EXISTS progress")
            conn.execute(schema)
        conn.commit()
        conn.close()

    _db_ready = True

# ── lessons ────────────────────────────────────────────────────────────────
def _lessons() -> list[dict[str, Any]]:
    with open(_LESSONS_FILE, encoding="utf-8") as f:
        return json.load(f)

# ── quests ─────────────────────────────────────────────────────────────────
class QuestCheckRequest(BaseModel):
    code: str

def _quests() -> list[dict[str, Any]]:
    with open(_QUESTS_FILE, encoding="utf-8") as f:
        return json.load(f)

def _recaps() -> list[dict[str, Any]]:
    with open(_RECAPS_FILE, encoding="utf-8") as f:
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
    allow_origin_regex=r"https://.*\.vercel\.app",
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
def _get_user_id(request: Request) -> str:
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=400, detail="X-User-Id header required")
    return user_id

@app.get("/progress")
def get_progress(request: Request) -> list[dict[str, Any]]:
    user_id = _get_user_id(request)
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM progress WHERE user_id = ? ORDER BY lesson_id", (user_id,)
    ).fetchall()
    conn.close()
    return [_ensure_dict(r) for r in rows]

@app.post("/progress")
def update_progress(request: Request, body: ProgressUpdate) -> dict[str, Any]:
    user_id = _get_user_id(request)
    conn = get_connection()
    conn.execute(
        """INSERT INTO progress (user_id, lesson_id, completed, quiz_passed, mission_done, score)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(user_id, lesson_id) DO UPDATE SET
             completed=excluded.completed,
             quiz_passed=excluded.quiz_passed,
             mission_done=excluded.mission_done,
             score=excluded.score,
             updated_at=datetime('now')""",
        (user_id, body.lesson_id, int(body.completed), int(body.quiz_passed),
         int(body.mission_done), body.score),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM progress WHERE user_id=? AND lesson_id=?", (user_id, body.lesson_id)
    ).fetchone()
    conn.close()
    return _ensure_dict(row)

@app.delete("/progress/{lesson_id}")
def reset_progress(lesson_id: str, request: Request) -> dict[str, str]:
    user_id = _get_user_id(request)
    conn = get_connection()
    conn.execute(
        "DELETE FROM progress WHERE user_id=? AND lesson_id=?", (user_id, lesson_id)
    )
    conn.commit()
    conn.close()
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

        # Try python first, fall back to python3
        py_cmd = "python3"
        try:
            subprocess.run(["python", "--version"], capture_output=True, timeout=2)
            py_cmd = "python"
        except Exception:
            pass

        result = subprocess.run(
            [py_cmd, tmp_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
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


# ── routes: quests ──────────────────────────────────────────────────────────
@app.get("/quests")
def list_quests() -> list[dict[str, Any]]:
    SUMMARY_FIELDS = ("id", "part", "title")
    return [
        {k: q[k] for k in SUMMARY_FIELDS if k in q}
        | ({"is_capstone": True} if q.get("is_capstone") else {})
        for q in _quests()
    ]


@app.get("/quests/{quest_id}")
def get_quest(quest_id: str) -> dict[str, Any]:
    for q in _quests():
        if q["id"] == quest_id:
            return q
    raise HTTPException(status_code=404, detail=f"Quest '{quest_id}' not found")


@app.post("/quests/{quest_id}/check")
def check_quest(quest_id: str, body: QuestCheckRequest) -> dict[str, Any]:
    quests = _quests()
    quest = next((q for q in quests if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quest '{quest_id}' not found")

    test_cases = quest.get("test_cases", [])
    if not test_cases:
        raise HTTPException(status_code=400, detail="No test cases for this quest")

    code_lower = body.code.lower()
    for forbidden in _FORBIDDEN_IMPORTS:
        if forbidden in code_lower:
            return {
                "quest_id": quest_id,
                "results": [],
                "all_passed": False,
                "error": "Использование запрещённых модулей не допускается",
            }

    results = []
    all_passed = True

    for tc in test_cases:
        tc_input = tc.get("input", "")
        expected = tc.get("expected_contains", [])

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as f:
                f.write(body.code)
                tmp_path = f.name

            py_cmd = "python3"
            try:
                subprocess.run(["python", "--version"], capture_output=True, timeout=2)
                py_cmd = "python"
            except Exception:
                pass

            proc = subprocess.run(
                [py_cmd, tmp_path],
                input=tc_input,
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )

            actual = proc.stdout
            stderr = proc.stderr.strip()

            missing = [e for e in expected if e not in actual]
            passed = len(missing) == 0 and not stderr
            if not passed:
                all_passed = False

            results.append({
                "passed": passed,
                "input": tc_input.strip()[:100],
                "actual_output": actual.strip()[:300] if actual else "",
                "missing_contains": missing,
                "error": stderr[:200] if stderr else None,
            })

        except subprocess.TimeoutExpired:
            all_passed = False
            results.append({
                "passed": False,
                "input": tc_input.strip()[:100],
                "actual_output": "",
                "missing_contains": expected,
                "error": "Превышено время выполнения (5 сек)",
            })
        except Exception as e:
            all_passed = False
            results.append({
                "passed": False,
                "input": tc_input.strip()[:100],
                "actual_output": "",
                "missing_contains": expected,
                "error": str(e)[:200],
            })
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    return {
        "quest_id": quest_id,
        "results": results,
        "all_passed": all_passed,
    }


# ── routes: recaps ──────────────────────────────────────────────────────────
@app.get("/recaps")
def list_recaps() -> list[dict[str, Any]]:
    SUMMARY_FIELDS = ("id", "part", "title")
    return [
        {k: r[k] for k in SUMMARY_FIELDS if k in r}
        for r in _recaps()
    ]


@app.get("/recaps/{recap_id}")
def get_recap(recap_id: str) -> dict[str, Any]:
    for r in _recaps():
        if r["id"] == recap_id:
            return r
    raise HTTPException(status_code=404, detail=f"Recap '{recap_id}' not found")

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


# ── routes: beta progress persistence ────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_participant_code(code: str) -> str:
    h = 0
    for ch in code:
        h = ((h << 5) - h) + ord(ch)
        h = h & h
    abs_h = h if h >= 0 else -h
    return "p_" + format(abs_h, "x")


def _ensure_beta_progress_table() -> None:
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS beta_progress (
            participant_code TEXT PRIMARY KEY,
            participant_id TEXT NOT NULL,
            current_lesson_id TEXT NOT NULL DEFAULT '1-1',
            completed_lessons TEXT NOT NULL DEFAULT '[]',
            lesson_status TEXT NOT NULL DEFAULT '{}',
            mission_stats TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            last_active_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


# ── beta access / staged access helpers ──────────────────────────────────────

MAX_STAGE = 5


def _ensure_beta_stages_table() -> None:
    """Create beta_stages table for staged beta access control."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS beta_stages (
            participant_code TEXT PRIMARY KEY,
            current_stage INTEGER NOT NULL DEFAULT 1,
            feedback_submitted INTEGER NOT NULL DEFAULT 0,
            feedback_text TEXT,
            feedback_rating INTEGER,
            feedback_submitted_at TEXT,
            operator_unlocked_at TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def _validate_operator_key(x_operator_key: str | None) -> bool:
    """Return True if the provided header matches the configured OPERATOR_KEY."""
    if not x_operator_key:
        return False
    return x_operator_key == OPERATOR_KEY


STAGE_PARTS: dict[int, list[int]] = {
    1: [1],
    2: [1, 2],
    3: [1, 2, 3],
    4: [1, 2, 3, 4],
    5: [1, 2, 3, 4, 5],
}


def _get_stage_row(participant_code: str) -> dict[str, Any] | None:
    """Fetch beta_stages row or None."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM beta_stages WHERE participant_code = ?",
        (participant_code,),
    ).fetchone()
    conn.close()
    return _ensure_dict(row) if row else None


def _ensure_stage_row(participant_code: str) -> dict[str, Any]:
    """Get existing row or create with defaults (stage=1)."""
    existing = _get_stage_row(participant_code)
    if existing:
        return existing
    now = _now_iso()
    conn = get_connection()
    conn.execute(
        """INSERT INTO beta_stages
            (participant_code, current_stage, created_at, updated_at)
           VALUES (?, ?, ?, ?)""",
        (participant_code, 1, now, now),
    )
    conn.commit()
    conn.close()
    result = _get_stage_row(participant_code)
    return result or {"participant_code": participant_code, "current_stage": 1}


class BetaProgressCreateBody(BaseModel):
    participant_code: str


class BetaLessonStartedBody(BaseModel):
    lesson_id: str


class BetaMissionResultBody(BaseModel):
    lesson_id: str
    passed: bool
    attempts: int = 1
    hints_used: int = 0


class BetaHintUsedBody(BaseModel):
    lesson_id: str


class BetaLessonCompletedBody(BaseModel):
    lesson_id: str


class BetaProgressUpdateBody(BaseModel):
    current_lesson_id: str | None = None
    completed_lessons: list[str] | None = None
    lesson_status: dict[str, str] | None = None
    mission_stats: dict[str, Any] | None = None


def _parse_beta_json(val: str, default: Any = None) -> Any:
    if default is None:
        default = {} if val.startswith("{") else []
    if not val:
        return default
    try:
        return json.loads(val)
    except (json.JSONDecodeError, TypeError):
        return default


def _get_beta_row(participant_code: str) -> dict[str, Any] | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM beta_progress WHERE participant_code = ?",
        (participant_code,),
    ).fetchone()
    conn.close()
    return _ensure_dict(row) if row else None


def _beta_row_to_response(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": True,
        "found": True,
        "participant_code": row.get("participant_code", ""),
        "participant_id": row.get("participant_id", ""),
        "current_lesson_id": row.get("current_lesson_id", "1-1"),
        "completed_lessons": _parse_beta_json(row.get("completed_lessons", "[]"), []),
        "lesson_status": _parse_beta_json(row.get("lesson_status", "{}"), {}),
        "mission_stats": _parse_beta_json(row.get("mission_stats", "{}"), {}),
        "created_at": row.get("created_at", ""),
        "updated_at": row.get("updated_at", ""),
        "last_active_at": row.get("last_active_at", ""),
    }


@app.post("/beta/progress/create")
def create_beta_progress(body: BetaProgressCreateBody) -> dict[str, Any]:
    _ensure_beta_progress_table()
    participant_code = body.participant_code.strip().upper()
    participant_id = _hash_participant_code(participant_code)

    existing = _get_beta_row(participant_code)
    if existing:
        return {
            "ok": True,
            "participant_code": existing["participant_code"],
            "participant_id": existing["participant_id"],
            "current_lesson_id": existing["current_lesson_id"],
            "completed_lessons": _parse_beta_json(existing.get("completed_lessons", "[]"), []),
            "created_at": existing["created_at"],
        }

    now = datetime.now(timezone.utc).isoformat() if hasattr(datetime, 'timezone') else _now_iso()
    conn = get_connection()
    conn.execute(
        """INSERT INTO beta_progress
           (participant_code, participant_id, current_lesson_id,
            completed_lessons, lesson_status, mission_stats,
            created_at, updated_at, last_active_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (participant_code, participant_id, "1-1", "[]", "{}", "{}", now, now, now),
    )
    conn.commit()
    conn.close()
    return {
        "ok": True,
        "participant_code": participant_code,
        "participant_id": participant_id,
        "current_lesson_id": "1-1",
        "completed_lessons": [],
        "created_at": now,
    }


@app.get("/beta/progress/{participant_code}")
def get_beta_progress(participant_code: str) -> dict[str, Any]:
    _ensure_beta_progress_table()
    row = _get_beta_row(participant_code.strip().upper())
    if not row:
        return {"ok": True, "found": False, "message": "Progress not found"}
    return _beta_row_to_response(row)


@app.put("/beta/progress/{participant_code}")
def update_beta_progress(
    participant_code: str, body: BetaProgressUpdateBody
) -> dict[str, Any]:
    _ensure_beta_progress_table()
    participant_code = participant_code.strip().upper()
    existing = _get_beta_row(participant_code)
    if not existing:
        return {"ok": True, "found": False, "message": "Progress not found"}

    participant_id = existing["participant_id"]
    completed_lessons = _parse_beta_json(existing.get("completed_lessons", "[]"), [])
    lesson_status = _parse_beta_json(existing.get("lesson_status", "{}"), {})
    mission_stats = _parse_beta_json(existing.get("mission_stats", "{}"), {})

    if body.completed_lessons is not None:
        completed_lessons = body.completed_lessons
    if body.lesson_status is not None:
        lesson_status = body.lesson_status
    if body.mission_stats is not None:
        mission_stats = body.mission_stats

    now = _now_iso()
    conn = get_connection()
    conn.execute(
        """UPDATE beta_progress SET
           current_lesson_id = ?, completed_lessons = ?, lesson_status = ?,
           mission_stats = ?, updated_at = ?, last_active_at = ?
           WHERE participant_code = ?""",
        (
            body.current_lesson_id or existing.get("current_lesson_id", "1-1"),
            json.dumps(completed_lessons),
            json.dumps(lesson_status),
            json.dumps(mission_stats),
            now, now,
            participant_code,
        ),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM beta_progress WHERE participant_code = ?", (participant_code,)
    ).fetchone()
    conn.close()
    return _beta_row_to_response(_ensure_dict(row)) if row else _beta_row_to_response(existing)


@app.post("/beta/progress/{participant_code}/lesson-started")
def beta_lesson_started(participant_code: str, body: BetaLessonStartedBody) -> dict[str, Any]:
    _ensure_beta_progress_table()
    participant_code = participant_code.strip().upper()
    existing = _get_beta_row(participant_code)
    now = _now_iso()

    if existing:
        lesson_status = _parse_beta_json(existing.get("lesson_status", "{}"), {})
        if body.lesson_id not in lesson_status:
            lesson_status[body.lesson_id] = "started"
        conn = get_connection()
        conn.execute(
            """UPDATE beta_progress SET current_lesson_id = ?, lesson_status = ?,
               updated_at = ?, last_active_at = ? WHERE participant_code = ?""",
            (body.lesson_id, json.dumps(lesson_status), now, now, participant_code),
        )
        conn.commit()
        conn.close()
    else:
        participant_id = _hash_participant_code(participant_code)
        conn = get_connection()
        conn.execute(
            """INSERT INTO beta_progress
               (participant_code, participant_id, current_lesson_id,
                completed_lessons, lesson_status, mission_stats,
                created_at, updated_at, last_active_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (participant_code, participant_id, body.lesson_id,
             "[]", json.dumps({body.lesson_id: "started"}), "{}",
             now, now, now),
        )
        conn.commit()
        conn.close()
    return {"ok": True}


@app.post("/beta/progress/{participant_code}/mission-result")
def beta_mission_result(participant_code: str, body: BetaMissionResultBody) -> dict[str, Any]:
    _ensure_beta_progress_table()
    participant_code = participant_code.strip().upper()
    existing = _get_beta_row(participant_code) or {}
    participant_id = existing.get("participant_id", _hash_participant_code(participant_code))
    mission_stats = _parse_beta_json(existing.get("mission_stats", "{}"), {})
    lesson_status = _parse_beta_json(existing.get("lesson_status", "{}"), {})
    completed_lessons = _parse_beta_json(existing.get("completed_lessons", "[]"), [])

    if body.lesson_id not in mission_stats:
        mission_stats[body.lesson_id] = {"attempts": 0, "failed": 0, "passed": False, "hints_used": 0}
    stats = mission_stats[body.lesson_id]
    stats["attempts"] = body.attempts
    stats["hints_used"] = body.hints_used
    if body.passed:
        stats["passed"] = True
        lesson_status[body.lesson_id] = "completed"
        if body.lesson_id not in completed_lessons:
            completed_lessons.append(body.lesson_id)
    else:
        stats["failed"] += 1

    now = _now_iso()
    conn = get_connection()
    conn.execute(
        """INSERT INTO beta_progress
           (participant_code, participant_id, current_lesson_id,
            completed_lessons, lesson_status, mission_stats,
            created_at, updated_at, last_active_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(participant_code) DO UPDATE SET
             mission_stats = excluded.mission_stats,
             lesson_status = excluded.lesson_status,
             completed_lessons = excluded.completed_lessons,
             updated_at = excluded.updated_at,
             last_active_at = excluded.last_active_at""",
        (participant_code, participant_id, body.lesson_id,
         json.dumps(completed_lessons), json.dumps(lesson_status),
         json.dumps(mission_stats), now, now, now),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@app.post("/beta/progress/{participant_code}/hint-used")
def beta_hint_used(participant_code: str, body: BetaHintUsedBody) -> dict[str, Any]:
    _ensure_beta_progress_table()
    participant_code = participant_code.strip().upper()
    existing = _get_beta_row(participant_code)
    if not existing:
        return {"ok": True}

    mission_stats = _parse_beta_json(existing.get("mission_stats", "{}"), {})
    if body.lesson_id not in mission_stats:
        mission_stats[body.lesson_id] = {"attempts": 0, "failed": 0, "passed": False, "hints_used": 0}
    mission_stats[body.lesson_id]["hints_used"] += 1

    now = _now_iso()
    conn = get_connection()
    conn.execute(
        "UPDATE beta_progress SET mission_stats = ?, updated_at = ?, last_active_at = ? WHERE participant_code = ?",
        (json.dumps(mission_stats), now, now, participant_code),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@app.post("/beta/progress/{participant_code}/lesson-completed")
def beta_lesson_completed(participant_code: str, body: BetaLessonCompletedBody) -> dict[str, Any]:
    _ensure_beta_progress_table()
    participant_code = participant_code.strip().upper()
    existing = _get_beta_row(participant_code)
    if not existing:
        return {"ok": True}

    lesson_status = _parse_beta_json(existing.get("lesson_status", "{}"), {})
    completed_lessons = _parse_beta_json(existing.get("completed_lessons", "[]"), [])
    lesson_status[body.lesson_id] = "completed"
    if body.lesson_id not in completed_lessons:
        completed_lessons.append(body.lesson_id)

    now = _now_iso()
    conn = get_connection()
    conn.execute(
        "UPDATE beta_progress SET lesson_status = ?, completed_lessons = ?, updated_at = ?, last_active_at = ? WHERE participant_code = ?",
        (json.dumps(lesson_status), json.dumps(completed_lessons), now, now, participant_code),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


# ── routes: beta access / staged access ──────────────────────────────────────


@app.get("/beta/access/{participant_code}")
def get_beta_access(participant_code: str) -> dict[str, Any]:
    """Get current stage and feedback status for a beta participant."""
    _ensure_beta_stages_table()
    code = participant_code.strip().upper()
    row = _ensure_stage_row(code)

    return {
        "ok": True,
        "participant_code": code,
        "current_stage": int(row.get("current_stage", 1)),
        "max_stage": MAX_STAGE,
        "has_feedback": bool(row.get("feedback_submitted", 0)),
        "feedback_submitted_at": row.get("feedback_submitted_at"),
    }


@app.post("/beta/access/{participant_code}/provide-feedback")
def provide_feedback(
    participant_code: str,
    body: BetaFeedbackRequest,
) -> dict[str, Any]:
    """Submit feedback. Required before operator can unlock next stage."""
    code = participant_code.strip().upper()
    if not body.feedback_text or len(body.feedback_text.strip()) < 10:
        raise HTTPException(
            status_code=422,
            detail="Feedback must be at least 10 characters",
        )

    _ensure_beta_stages_table()
    _ensure_stage_row(code)
    now = _now_iso()

    conn = get_connection()
    conn.execute(
        """UPDATE beta_stages
           SET feedback_submitted = 1,
               feedback_text = ?,
               feedback_rating = ?,
               feedback_submitted_at = ?,
               updated_at = ?
           WHERE participant_code = ?""",
        (body.feedback_text, body.rating, now, now, code),
    )
    conn.commit()
    conn.close()

    return {"ok": True, "message": "Feedback submitted"}


@app.post("/beta/access/{participant_code}/operator-unlock")
def operator_unlock(
    participant_code: str,
    x_operator_key: str | None = Header(None, alias="X-Operator-Key"),
) -> dict[str, Any]:
    """Operator unlocks the next stage for a participant.

    Requires X-Operator-Key header.
    Checks that feedback has been submitted before unlocking.
    """
    if not _validate_operator_key(x_operator_key):
        raise HTTPException(status_code=403, detail="Invalid operator key")

    _ensure_beta_stages_table()
    code = participant_code.strip().upper()
    row = _ensure_stage_row(code)
    current = int(row.get("current_stage", 1))

    if current >= MAX_STAGE:
        return {"ok": False, "detail": f"Already at maximum stage ({MAX_STAGE})"}

    if not bool(row.get("feedback_submitted", 0)):
        return {
            "ok": False,
            "detail": "Feedback required before unlock. Participant must submit feedback first.",
        }

    new_stage = current + 1
    now = _now_iso()

    conn = get_connection()
    conn.execute(
        "UPDATE beta_stages SET current_stage = ?, operator_unlocked_at = ?, updated_at = ? WHERE participant_code = ?",
        (new_stage, now, now, code),
    )
    conn.commit()
    conn.close()

    return {
        "ok": True,
        "previous_stage": current,
        "current_stage": new_stage,
        "message": f"Stage unlocked to {new_stage}",
    }


@app.get("/beta/access/operator/pending-feedback")
def get_pending_feedback(
    x_operator_key: str | None = Header(None, alias="X-Operator-Key"),
) -> dict[str, Any]:
    """List participants with submitted feedback who are not yet at max stage.

    Requires X-Operator-Key header.
    """
    if not _validate_operator_key(x_operator_key):
        raise HTTPException(status_code=403, detail="Invalid operator key")

    _ensure_beta_stages_table()
    conn = get_connection()
    rows = conn.execute(
        """SELECT participant_code, current_stage, feedback_text,
                  feedback_rating, feedback_submitted_at
           FROM beta_stages
           WHERE feedback_submitted = 1
             AND current_stage < ?
           ORDER BY feedback_submitted_at ASC""",
        (MAX_STAGE,),
    ).fetchall()
    conn.close()

    pending = []
    for row in rows:
        d = _ensure_dict(row)
        pending.append({
            "participant_code": d["participant_code"],
            "current_stage": d["current_stage"],
            "feedback_text": d.get("feedback_text"),
            "feedback_rating": d.get("feedback_rating"),
            "feedback_submitted_at": d.get("feedback_submitted_at"),
        })

    return {"ok": True, "pending": pending}


# ── routes: analytics ────────────────────────────────────────────────────────
_ANALYTICS_FILE = Path("/tmp/pq_analytics/events.jsonl")


@app.post("/analytics/events")
def collect_analytics_events(body: dict[str, Any]) -> dict[str, Any]:
    """Collect anonymous analytics events from the frontend."""
    events = body.get("events", [])
    if not isinstance(events, list):
        return {"ok": False, "count": 0}
    _ANALYTICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    for event in events:
        try:
            with open(_ANALYTICS_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
            count += 1
        except OSError:
            pass
    return {"ok": True, "count": count}


@app.get("/analytics/export")
def export_analytics() -> dict[str, Any]:
    """Export stored analytics events (operator only)."""
    if os.environ.get("ANALYTICS_ENABLED", "").lower() not in ("true", "1", "yes"):
        raise HTTPException(status_code=403, detail="Analytics export not enabled")
    if not _ANALYTICS_FILE.exists():
        return {"ok": True, "summary": {"total_events": 0, "event_type_counts": {}}, "events": []}
    events = []
    try:
        with open(_ANALYTICS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except OSError:
        pass

    event_type_counts: dict[str, int] = {}
    participant_set: set[str] = set()
    session_set: set[str] = set()
    for ev in events:
        etype = ev.get("event", "unknown")
        event_type_counts[etype] = event_type_counts.get(etype, 0) + 1
        if ev.get("participant_id"):
            participant_set.add(ev["participant_id"])
        if ev.get("anonymous_session_id"):
            session_set.add(ev["anonymous_session_id"])

    return {
        "ok": True,
        "summary": {
            "total_events": len(events),
            "unique_participants": len(participant_set),
            "unique_sessions": len(session_set),
            "event_type_counts": event_type_counts,
            "earliest_event": events[0].get("timestamp") if events else None,
            "latest_event": events[-1].get("timestamp") if events else None,
        },
        "events": events[-1000:],
    }


@app.delete("/analytics/events")
def clear_analytics() -> dict[str, Any]:
    """Clear all stored analytics events (operator use)."""
    if os.environ.get("ANALYTICS_ENABLED", "").lower() not in ("true", "1", "yes"):
        raise HTTPException(status_code=403, detail="Analytics export not enabled")
    try:
        if _ANALYTICS_FILE.exists():
            _ANALYTICS_FILE.unlink()
        return {"ok": True, "cleared": True}
    except OSError as e:
        return {"ok": False, "cleared": False, "error": str(e)}


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

@app.get("/health/persistence")
def persistence_health() -> dict[str, object]:
    """Report persistence backend status for diagnostics.

    Returns:
      - backend: "turso" | "sqlite" | "unavailable"
      - environment: "production" | "development" | "test"
      - persistent_storage: true if backend is Turso
      - sqlite_tmp_fallback: always false (intentionally disabled)
      - safe_for_beta_progress: true only if Turso is active
      - error: description if backend is unavailable (never exposes secrets)
    """
    return get_backend_status()


# ── Vercel ASGI handler ────────────────────────────────────────────────────
# Export app for Vercel serverless runtime
__all__ = ["app"]
