from typing import Any

from fastapi import APIRouter, Request, HTTPException

from app.database import get_connection
from app.models import ProgressUpdate

router = APIRouter(prefix="/progress", tags=["progress"])


def _get_user_id(request: Request) -> str:
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=400, detail="X-User-Id header required")
    return user_id


@router.get("")
def get_all_progress(request: Request) -> list[dict[str, Any]]:
    user_id = _get_user_id(request)
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM progress WHERE user_id = ?", (user_id,)
        ).fetchall()
    return [dict(row) for row in rows]


@router.post("")
def update_progress(request: Request, body: ProgressUpdate) -> dict[str, Any]:
    user_id = _get_user_id(request)
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO progress (user_id, lesson_id, completed, quiz_passed, mission_done, score)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, lesson_id) DO UPDATE SET
                completed = excluded.completed,
                quiz_passed = excluded.quiz_passed,
                mission_done = excluded.mission_done,
                score = excluded.score,
                updated_at = datetime('now')
            """,
            (
                user_id,
                body.lesson_id,
                int(body.completed),
                int(body.quiz_passed),
                int(body.mission_done),
                body.score,
            ),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM progress WHERE user_id = ? AND lesson_id = ?",
            (user_id, body.lesson_id),
        ).fetchone()
    if row is None:
        return {"user_id": user_id, "lesson_id": body.lesson_id, "completed": False}
    return dict(row)


@router.delete("/{lesson_id}")
def reset_progress(request: Request, lesson_id: str) -> dict[str, str]:
    user_id = _get_user_id(request)
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM progress WHERE user_id = ? AND lesson_id = ?",
            (user_id, lesson_id),
        )
        conn.commit()
    return {"status": "reset", "lesson_id": lesson_id, "user_id": user_id}
