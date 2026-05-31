from pydantic import BaseModel
from typing import Optional


class ProgressUpdate(BaseModel):
    lesson_id: str
    completed: bool = False
    quiz_passed: bool = False
    mission_done: bool = False
    score: Optional[int] = None


class QuizAnswer(BaseModel):
    lesson_id: str
    answer_id: str


class CodeSubmission(BaseModel):
    lesson_id: str
    code: str
