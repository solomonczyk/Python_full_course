"""Pydantic schemas for Beta Staged Access API."""

from typing import Optional

from pydantic import BaseModel, Field


class BetaAccessGetResponse(BaseModel):
    """Response for GET /beta/access/{code}."""
    ok: bool = True
    participant_code: str
    current_stage: int = 1
    max_stage: int = 5
    has_feedback: bool = False
    feedback_submitted_at: Optional[str] = None


class BetaFeedbackRequest(BaseModel):
    """Request body for providing feedback."""
    feedback_text: str = Field(..., min_length=10, max_length=2000)
    rating: Optional[int] = Field(None, ge=1, le=5)


class BetaFeedbackResponse(BaseModel):
    """Response after submitting feedback."""
    ok: bool = True
    message: str = "Feedback submitted"


class BetaOperatorUnlockResponse(BaseModel):
    """Response after operator unlocks next stage."""
    ok: bool = True
    previous_stage: int
    current_stage: int
    message: str = "Stage unlocked"


class BetaAccessErrorResponse(BaseModel):
    """Error response."""
    ok: bool = False
    detail: str


class PendingFeedbackItem(BaseModel):
    """A single pending feedback entry for operator review."""
    participant_code: str
    current_stage: int
    feedback_text: str
    feedback_rating: Optional[int] = None
    feedback_submitted_at: str


class PendingFeedbackResponse(BaseModel):
    """Response listing pending feedback."""
    ok: bool = True
    pending: list[PendingFeedbackItem] = Field(default_factory=list)
