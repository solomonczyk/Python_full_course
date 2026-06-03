import os
import sqlite3
from pathlib import Path

# Load .env file for local development
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

DB_PATH = Path(os.environ.get("DB_PATH", "/tmp/progress.db"))

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL", "")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN", "")

_db_initialized = False


def _ensure_db() -> None:
    global _db_initialized
    if _db_initialized:
        return

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Create table — works for both SQLite and Turso (libsql)
    schemas = [
        """
        CREATE TABLE IF NOT EXISTS progress (
            user_id TEXT NOT NULL DEFAULT 'anonymous',
            lesson_id TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            quiz_passed INTEGER NOT NULL DEFAULT 0,
            mission_done INTEGER NOT NULL DEFAULT 0,
            score INTEGER,
            updated_at TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (user_id, lesson_id)
        )
        """,
        """
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
        """,
    ]

    if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
        conn = get_connection()
        for schema in schemas:
            conn.execute(schema)
        conn.commit()
    else:
        conn = sqlite3.connect(str(DB_PATH))
        for schema in schemas:
            conn.execute(schema)
        # Migrate old progress table (without user_id) if exists
        try:
            conn.execute("SELECT user_id FROM progress LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("DROP TABLE IF EXISTS progress")
            conn.execute(schemas[0])
        conn.commit()
        conn.close()

    _db_initialized = True


def get_connection() -> sqlite3.Connection:
    _ensure_db()

    if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
        try:
            import libsql_experimental as libsql  # type: ignore
            conn = libsql.connect(
                TURSO_DATABASE_URL,
                auth_token=TURSO_AUTH_TOKEN,
            )
            conn.row_factory = sqlite3.Row
            return conn
        except ImportError:
            pass  # Fall through to local SQLite

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    _ensure_db()
