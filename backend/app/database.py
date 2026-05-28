import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "progress.db"
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                lesson_id TEXT PRIMARY KEY,
                completed INTEGER NOT NULL DEFAULT 0,
                score INTEGER,
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()
