"""Pydantic schemas for Beta Progress API."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class BetaProgressCreate(BaseModel):
    """Request to create beta progress for a participant.
    Format validation is done in the endpoint after uppercasing.
    """
    participant_code: str


class BetaMissionStatsPayload(BaseModel):
    """Mission stats for a single lesson."""
    attempts: int = 0
    failed: int = 0
    passed: bool = False
    hints_used: int = 0


class BetaLessonStarted(BaseModel):
    """Request body for lesson-started endpoint."""
    lesson_id: str


class BetaMissionResult(BaseModel):
    """Request body for mission-result endpoint."""
    lesson_id: str
    passed: bool
    attempts: int = 1
    hints_used: int = 0


class BetaHintUsed(BaseModel):
    """Request body for hint-used endpoint."""
    lesson_id: str


class BetaLessonCompleted(BaseModel):
    """Request body for lesson-completed endpoint."""
    lesson_id: str


class BetaProgressUpdate(BaseModel):
    """Request to update beta progress fields."""
    current_lesson_id: Optional[str] = None
    completed_lessons: Optional[list[str]] = None
    lesson_status: Optional[dict[str, str]] = None
    mission_stats: Optional[dict[str, Any]] = None


class BetaProgressResponse(BaseModel):
    """Response for beta progress requests."""
    ok: bool = True


class BetaProgressCreateResponse(BetaProgressResponse):
    """Response after creating beta progress."""
    participant_code: str
    participant_id: str
    current_lesson_id: str = "1-1"
    completed_lessons: list[str] = Field(default_factory=list)
    created_at: str


class BetaProgressGetResponse(BetaProgressResponse):
    """Response when getting beta progress."""
    found: bool = True
    participant_code: str = ""
    participant_id: str = ""
    current_lesson_id: str = "1-1"
    completed_lessons: list[str] = Field(default_factory=list)
    lesson_status: dict[str, str] = Field(default_factory=dict)
    mission_stats: dict[str, Any] = Field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    last_active_at: str = ""
    message: Optional[str] = None


class BetaProgressNotFoundResponse(BaseModel):
    """Response when participant code not found."""
    ok: bool = True
    found: bool = False
    message: str = "Progress not found"
