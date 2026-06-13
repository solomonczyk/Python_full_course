from pydantic import BaseModel
from typing import Optional


class ProgressUpdate(BaseModel):
    lesson_id: str
    completed: bool
    score: Optional[int] = None


class QuizAnswer(BaseModel):
    lesson_id: str
    answer_id: str


class CodeSubmission(BaseModel):
    lesson_id: str
    code: str


# ── Narrative layer models ──────────────────────────────────────────────

class Hook(BaseModel):
    character: str
    emotion: str
    text: str


class LessonEnd(BaseModel):
    character: str
    emotion: str
    text: str


# ── Story layer models ────────────────────────────────────────────────────

class StoryEvent(BaseModel):
    """Scene-setting narration at the start of a lesson (third-person)."""
    location: str
    text: str
    bagus_presence: Optional[str] = None


class Callback(BaseModel):
    """Character references a past lesson event."""
    references_lesson: str
    character: str
    text: str


class CharacterGrowth(BaseModel):
    """Malek's internal monologue at the end of a part (recap lessons only)."""
    character: str
    internal: str
