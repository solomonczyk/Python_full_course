"""Beta Access Router — Staged Access Control for Beta Participants.

All endpoints are prefixed with /beta/access.
Uses X-Operator-Key header for operator actions.
"""

import os
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Header, HTTPException

from app.database import get_connection
from app.schemas.beta_access import (
    BetaAccessErrorResponse,
    BetaAccessGetResponse,
    BetaFeedbackRequest,
    BetaFeedbackResponse,
    BetaOperatorUnlockResponse,
    PendingFeedbackItem,
    PendingFeedbackResponse,
)

router = APIRouter(prefix="/beta/access", tags=["beta_access"])

# Stage-to-parts mapping: stage N grants access to all parts ≤ N
STAGE_PARTS: dict[int, list[int]] = {
    1: [1],
    2: [1, 2],
    3: [1, 2, 3],
    4: [1, 2, 3, 4],
    5: [1, 2, 3, 4, 5],
}

MAX_STAGE = 5

OPERATOR_KEY = os.environ.get("OPERATOR_KEY", "op-python-quest-dev-2026")


# ── Helpers ────────────────────────────────────────────────────────────────


def _now_iso() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def _get_stage_row(participant_code: str) -> dict[str, Any] | None:
    """Fetch beta_stages row or None."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM beta_stages WHERE participant_code = ?",
            (participant_code,),
        ).fetchone()
    return dict(row) if row else None


def _ensure_stage_row(participant_code: str) -> dict[str, Any]:
    """Get existing row or create with defaults (stage=1)."""
    existing = _get_stage_row(participant_code)
    if existing:
        return existing

    now = _now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO beta_stages
                (participant_code, current_stage, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (participant_code, 1, now, now),
        )
        conn.commit()
    result = _get_stage_row(participant_code)
    return result or {"participant_code": participant_code, "current_stage": 1}


def get_current_stage(participant_code: str) -> int:
    """Get current stage for a participant. Auto-creates row if missing.

    This is the public utility function imported by lessons.py.
    """
    row = _ensure_stage_row(participant_code.upper())
    return int(row.get("current_stage", 1))


def _validate_operator_key(x_operator_key: str | None) -> bool:
    """Validate operator key header."""
    if not x_operator_key:
        return False
    return x_operator_key == OPERATOR_KEY


# ── Endpoints ──────────────────────────────────────────────────────────────


@router.get(
    "/{participant_code}",
    response_model=BetaAccessGetResponse,
)
def get_beta_access(participant_code: str) -> BetaAccessGetResponse:
    """Get current stage and feedback status for a participant."""
    code = participant_code.strip().upper()
    row = _ensure_stage_row(code)

    return BetaAccessGetResponse(
        ok=True,
        participant_code=code,
        current_stage=int(row.get("current_stage", 1)),
        max_stage=MAX_STAGE,
        has_feedback=bool(row.get("feedback_submitted", 0)),
        feedback_submitted_at=row.get("feedback_submitted_at"),
    )


@router.post(
    "/{participant_code}/provide-feedback",
    response_model=BetaFeedbackResponse | BetaAccessErrorResponse,
)
def provide_feedback(
    participant_code: str,
    body: BetaFeedbackRequest,
) -> BetaFeedbackResponse | BetaAccessErrorResponse:
    """Submit feedback. Required before operator can unlock next stage."""
    code = participant_code.strip().upper()
    now = _now_iso()

    _ensure_stage_row(code)

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE beta_stages
            SET feedback_submitted = 1,
                feedback_text = ?,
                feedback_rating = ?,
                feedback_submitted_at = ?,
                updated_at = ?
            WHERE participant_code = ?
            """,
            (body.feedback_text, body.rating, now, now, code),
        )
        conn.commit()

    return BetaFeedbackResponse(ok=True, message="Feedback submitted")


@router.post(
    "/{participant_code}/operator-unlock",
    response_model=BetaOperatorUnlockResponse | BetaAccessErrorResponse,
)
def operator_unlock(
    participant_code: str,
    x_operator_key: str | None = Header(None, alias="X-Operator-Key"),
) -> BetaOperatorUnlockResponse | BetaAccessErrorResponse:
    """Operator unlocks the next stage for a participant.

    Requires X-Operator-Key header.
    Checks that feedback has been submitted before unlocking.
    """
    if not _validate_operator_key(x_operator_key):
        raise HTTPException(status_code=403, detail="Invalid operator key")

    code = participant_code.strip().upper()
    row = _ensure_stage_row(code)
    current = int(row.get("current_stage", 1))

    if current >= MAX_STAGE:
        return BetaAccessErrorResponse(
            ok=False,
            detail=f"Already at maximum stage ({MAX_STAGE})",
        )

    if not bool(row.get("feedback_submitted", 0)):
        return BetaAccessErrorResponse(
            ok=False,
            detail="Feedback required before unlock. Participant must submit feedback first.",
        )

    new_stage = current + 1
    now = _now_iso()

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE beta_stages
            SET current_stage = ?,
                operator_unlocked_at = ?,
                updated_at = ?
            WHERE participant_code = ?
            """,
            (new_stage, now, now, code),
        )
        conn.commit()

    return BetaOperatorUnlockResponse(
        ok=True,
        previous_stage=current,
        current_stage=new_stage,
        message=f"Stage unlocked to {new_stage}",
    )


@router.get(
    "/operator/pending-feedback",
    response_model=PendingFeedbackResponse,
)
def get_pending_feedback(
    x_operator_key: str | None = Header(None, alias="X-Operator-Key"),
) -> PendingFeedbackResponse:
    """List participants with pending feedback who haven't reached max stage.

    Requires X-Operator-Key header.
    """
    if not _validate_operator_key(x_operator_key):
        raise HTTPException(status_code=403, detail="Invalid operator key")

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT participant_code, current_stage, feedback_text,
                   feedback_rating, feedback_submitted_at
            FROM beta_stages
            WHERE feedback_submitted = 1
              AND current_stage < ?
            ORDER BY feedback_submitted_at ASC
            """,
            (MAX_STAGE,),
        ).fetchall()

    pending = [
        PendingFeedbackItem(
            participant_code=row["participant_code"],
            current_stage=row["current_stage"],
            feedback_text=row["feedback_text"],
            feedback_rating=row["feedback_rating"],
            feedback_submitted_at=row["feedback_submitted_at"],
        )
        for row in rows
    ]

    return PendingFeedbackResponse(ok=True, pending=pending)
