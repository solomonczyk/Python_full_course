import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("DB_PATH", "/tmp/progress.db"))

_db_initialized = False


def _ensure_db() -> None:
    global _db_initialized
    if _db_initialized:
        return
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
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
    _db_initialized = True


def get_connection() -> sqlite3.Connection:
    _ensure_db()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    _ensure_db()
