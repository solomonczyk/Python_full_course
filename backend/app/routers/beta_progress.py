"""Beta Progress Router — server-side progress persistence by participant_code.

All endpoints are prefixed with /beta/progress.
No personal data is stored — only participant_code and lightweight progress fields.
"""

import json
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.beta_progress import (
    BetaProgressCreate,
    BetaProgressCreateResponse,
    BetaProgressGetResponse,
    BetaProgressNotFoundResponse,
    BetaProgressResponse,
    BetaLessonStarted,
    BetaMissionResult,
    BetaHintUsed,
    BetaLessonCompleted,
    BetaProgressUpdate,
)


router = APIRouter(prefix="/beta/progress", tags=["beta_progress"])


# ── Helper: deterministic participant_id hash ────────────────────────────────

def _hash_participant_code(code: str) -> str:
    """Create a deterministic pseudonymous hash of participant code."""
    h = 0
    for ch in code:
        h = ((h << 5) - h) + ord(ch)
        h = h & h  # Convert to 32-bit integer
    # Take absolute value, convert to base-36
    abs_h = h if h >= 0 else -h
    return "p_" + format(abs_h, "x")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Helper: parse JSON columns ───────────────────────────────────────────────

def _parse_json_col(val: str, default: Any = None) -> Any:
    if default is None:
        default = {} if val.startswith("{") else []
    if not val:
        return default
    try:
        return json.loads(val)
    except (json.JSONDecodeError, TypeError):
        return default


# ── CRUD ─────────────────────────────────────────────────────────────────────

def _get_beta_progress(participant_code: str) -> dict[str, Any] | None:
    """Fetch beta progress row or None."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM beta_progress WHERE participant_code = ?",
            (participant_code,),
        ).fetchone()
    return dict(row) if row else None


def _upsert_beta_progress(
    participant_code: str,
    participant_id: str,
    **fields: Any,
) -> dict[str, Any]:
    """Upsert beta progress row and return the full row."""
    now = _now_iso()

    # Build SET clause dynamically for partial updates
    set_parts = ["updated_at = ?", "last_active_at = ?"]
    set_values: list[Any] = [now, now]

    for key, value in fields.items():
        if value is not None:
            if isinstance(value, (list, dict)):
                set_parts.append(f"{key} = ?")
                set_values.append(json.dumps(value))
            else:
                set_parts.append(f"{key} = ?")
                set_values.append(str(value))

    # Check if row exists
    existing = _get_beta_progress(participant_code)

    if existing:
        sql = f"""
            UPDATE beta_progress
            SET {', '.join(set_parts)}
            WHERE participant_code = ?
        """
        set_values.append(participant_code)
        with get_connection() as conn:
            conn.execute(sql, set_values)
            conn.commit()
    else:
        # Insert new row
        completed_lessons = json.dumps(fields.get("completed_lessons", []))
        lesson_status = json.dumps(fields.get("lesson_status", {}))
        mission_stats = json.dumps(fields.get("mission_stats", {}))
        current_lesson_id = fields.get("current_lesson_id", "1-1")

        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO beta_progress
                    (participant_code, participant_id, current_lesson_id,
                     completed_lessons, lesson_status, mission_stats,
                     created_at, updated_at, last_active_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    participant_code,
                    participant_id,
                    current_lesson_id,
                    completed_lessons,
                    lesson_status,
                    mission_stats,
                    now,
                    now,
                    now,
                ),
            )
            conn.commit()

    return _get_beta_progress(participant_code) or {}


def _row_to_get_response(row: dict[str, Any]) -> BetaProgressGetResponse:
    """Convert a DB row to a BetaProgressGetResponse."""
    return BetaProgressGetResponse(
        ok=True,
        found=True,
        participant_code=row.get("participant_code", ""),
        participant_id=row.get("participant_id", ""),
        current_lesson_id=row.get("current_lesson_id", "1-1"),
        completed_lessons=_parse_json_col(
            row.get("completed_lessons", "[]"), []
        ),
        lesson_status=_parse_json_col(
            row.get("lesson_status", "{}"), {}
        ),
        mission_stats=_parse_json_col(
            row.get("mission_stats", "{}"), {}
        ),
        created_at=row.get("created_at", ""),
        updated_at=row.get("updated_at", ""),
        last_active_at=row.get("last_active_at", ""),
    )


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.post("/create", response_model=BetaProgressCreateResponse)
def create_beta_progress(body: BetaProgressCreate) -> BetaProgressCreateResponse:
    """Create a new beta progress entry for a participant code.

    Idempotent: if already exists, returns existing without error.
    """
    participant_code = body.participant_code.strip().upper()
    participant_id = _hash_participant_code(participant_code)

    existing = _get_beta_progress(participant_code)
    if existing:
        return BetaProgressCreateResponse(
            ok=True,
            participant_code=existing["participant_code"],
            participant_id=existing["participant_id"],
            current_lesson_id=existing["current_lesson_id"],
            completed_lessons=_parse_json_col(
                existing.get("completed_lessons", "[]"), []
            ),
            created_at=existing["created_at"],
        )

    now = _now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO beta_progress
                (participant_code, participant_id, current_lesson_id,
                 completed_lessons, lesson_status, mission_stats,
                 created_at, updated_at, last_active_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                participant_code,
                participant_id,
                "1-1",
                "[]",
                "{}",
                "{}",
                now,
                now,
                now,
            ),
        )
        conn.commit()

    return BetaProgressCreateResponse(
        ok=True,
        participant_code=participant_code,
        participant_id=participant_id,
        current_lesson_id="1-1",
        completed_lessons=[],
        created_at=now,
    )


@router.get(
    "/{participant_code}",
    response_model=BetaProgressGetResponse | BetaProgressNotFoundResponse,
)
def get_beta_progress(participant_code: str) -> BetaProgressGetResponse | BetaProgressNotFoundResponse:
    """Get beta progress by participant code.

    Never exposes personal data or stack traces.
    Returns found=False with a safe message if code not found.
    """
    row = _get_beta_progress(participant_code.strip().upper())
    if not row:
        return BetaProgressNotFoundResponse(
            ok=True,
            found=False,
            message="Progress not found",
        )
    return _row_to_get_response(row)


@router.put(
    "/{participant_code}",
    response_model=BetaProgressGetResponse | BetaProgressNotFoundResponse,
)
def update_beta_progress(
    participant_code: str,
    body: BetaProgressUpdate,
) -> BetaProgressGetResponse | BetaProgressNotFoundResponse:
    """Update beta progress fields for a participant code."""
    participant_code = participant_code.strip().upper()
    existing = _get_beta_progress(participant_code)
    if not existing:
        return BetaProgressNotFoundResponse(
            ok=True,
            found=False,
            message="Progress not found",
        )

    participant_id = existing["participant_id"]

    # Merge existing JSON columns with updates
    completed_lessons = _parse_json_col(
        existing.get("completed_lessons", "[]"), []
    )
    lesson_status = _parse_json_col(
        existing.get("lesson_status", "{}"), {}
    )
    mission_stats = _parse_json_col(
        existing.get("mission_stats", "{}"), {}
    )

    if body.completed_lessons is not None:
        completed_lessons = body.completed_lessons
    if body.lesson_status is not None:
        lesson_status = body.lesson_status
    if body.mission_stats is not None:
        mission_stats = body.mission_stats

    _upsert_beta_progress(
        participant_code,
        participant_id,
        current_lesson_id=body.current_lesson_id
        or existing.get("current_lesson_id", "1-1"),
        completed_lessons=completed_lessons,
        lesson_status=lesson_status,
        mission_stats=mission_stats,
    )

    updated = _get_beta_progress(participant_code) or existing
    return _row_to_get_response(updated)


@router.post(
    "/{participant_code}/lesson-started",
    response_model=BetaProgressResponse,
)
def lesson_started(
    participant_code: str,
    body: BetaLessonStarted,
) -> BetaProgressResponse:
    """Mark a lesson as started for the participant."""
    participant_code = participant_code.strip().upper()
    existing = _get_beta_progress(participant_code)

    if existing:
        lesson_status = _parse_json_col(
            existing.get("lesson_status", "{}"), {}
        )
        if body.lesson_id not in lesson_status:
            lesson_status[body.lesson_id] = "started"

        _upsert_beta_progress(
            participant_code,
            existing["participant_id"],
            current_lesson_id=body.lesson_id,
            lesson_status=lesson_status,
        )
    else:
        # Auto-create progress if not exists
        participant_id = _hash_participant_code(participant_code)
        _upsert_beta_progress(
            participant_code,
            participant_id,
            current_lesson_id=body.lesson_id,
            lesson_status={body.lesson_id: "started"},
        )

    return BetaProgressResponse(ok=True)


@router.post(
    "/{participant_code}/mission-result",
    response_model=BetaProgressResponse,
)
def mission_result(
    participant_code: str,
    body: BetaMissionResult,
) -> BetaProgressResponse:
    """Record a mission attempt result (pass/fail)."""
    participant_code = participant_code.strip().upper()
    existing = _get_beta_progress(participant_code)
    if not existing:
        # Auto-create
        existing_pid = _hash_participant_code(participant_code)
        _upsert_beta_progress(
            participant_code, existing_pid,
            current_lesson_id=body.lesson_id,
        )
        existing = _get_beta_progress(participant_code)
        if not existing:
            return BetaProgressResponse(ok=True)

    participant_id = existing["participant_id"]
    mission_stats = _parse_json_col(
        existing.get("mission_stats", "{}"), {}
    )
    lesson_status = _parse_json_col(
        existing.get("lesson_status", "{}"), {}
    )
    completed_lessons = _parse_json_col(
        existing.get("completed_lessons", "[]"), []
    )

    # Init mission stats for this lesson if needed
    if body.lesson_id not in mission_stats:
        mission_stats[body.lesson_id] = {
            "attempts": 0,
            "failed": 0,
            "passed": False,
            "hints_used": 0,
        }

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

    _upsert_beta_progress(
        participant_code,
        participant_id,
        current_lesson_id=body.lesson_id,
        mission_stats=mission_stats,
        lesson_status=lesson_status,
        completed_lessons=completed_lessons,
    )

    return BetaProgressResponse(ok=True)


@router.post(
    "/{participant_code}/hint-used",
    response_model=BetaProgressResponse,
)
def hint_used(
    participant_code: str,
    body: BetaHintUsed,
) -> BetaProgressResponse:
    """Record that a hint was used for a lesson."""
    participant_code = participant_code.strip().upper()
    existing = _get_beta_progress(participant_code)
    if not existing:
        return BetaProgressResponse(ok=True)

    participant_id = existing["participant_id"]
    mission_stats = _parse_json_col(
        existing.get("mission_stats", "{}"), {}
    )

    if body.lesson_id not in mission_stats:
        mission_stats[body.lesson_id] = {
            "attempts": 0,
            "failed": 0,
            "passed": False,
            "hints_used": 0,
        }

    mission_stats[body.lesson_id]["hints_used"] += 1

    _upsert_beta_progress(
        participant_code,
        participant_id,
        mission_stats=mission_stats,
    )

    return BetaProgressResponse(ok=True)


@router.post(
    "/{participant_code}/lesson-completed",
    response_model=BetaProgressResponse,
)
def lesson_completed(
    participant_code: str,
    body: BetaLessonCompleted,
) -> BetaProgressResponse:
    """Record that a lesson was completed."""
    participant_code = participant_code.strip().upper()
    existing = _get_beta_progress(participant_code)
    if not existing:
        return BetaProgressResponse(ok=True)

    participant_id = existing["participant_id"]
    lesson_status = _parse_json_col(
        existing.get("lesson_status", "{}"), {}
    )
    completed_lessons = _parse_json_col(
        existing.get("completed_lessons", "[]"), []
    )

    lesson_status[body.lesson_id] = "completed"
    if body.lesson_id not in completed_lessons:
        completed_lessons.append(body.lesson_id)

    _upsert_beta_progress(
        participant_code,
        participant_id,
        lesson_status=lesson_status,
        completed_lessons=completed_lessons,
    )

    return BetaProgressResponse(ok=True)
