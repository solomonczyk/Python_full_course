from typing import Any

from fastapi import APIRouter

from app.database import get_connection
from app.models import ProgressUpdate

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("")
def get_all_progress() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM progress").fetchall()
    return [dict(row) for row in rows]


@router.post("")
def update_progress(body: ProgressUpdate) -> dict[str, Any]:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO progress (lesson_id, completed, score)
            VALUES (?, ?, ?)
            ON CONFLICT(lesson_id) DO UPDATE SET
                completed = excluded.completed,
                score = excluded.score,
                updated_at = datetime('now')
            """,
            (body.lesson_id, int(body.completed), body.score),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM progress WHERE lesson_id = ?", (body.lesson_id,)
        ).fetchone()
    return dict(row)


@router.delete("/{lesson_id}")
def reset_progress(lesson_id: str) -> dict[str, str]:
    with get_connection() as conn:
        conn.execute("DELETE FROM progress WHERE lesson_id = ?", (lesson_id,))
        conn.commit()
    return {"status": "reset", "lesson_id": lesson_id}
