import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from app.models import QuizAnswer

router = APIRouter(prefix="/quiz", tags=["quiz"])

_DATA_FILE = Path(__file__).parent.parent / "data" / "lessons.json"


def _load_lessons() -> list[dict[str, Any]]:
    with open(_DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


@router.post("/check")
def check_quiz_answer(body: QuizAnswer) -> dict[str, Any]:
    lessons = _load_lessons()
    lesson = next((x for x in lessons if x["id"] == body.lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    quiz = lesson.get("quiz")
    if not quiz:
        raise HTTPException(status_code=400, detail="This lesson has no quiz")

    correct_option = next(
        (opt for opt in quiz["options"] if opt["correct"]), None
    )
    is_correct = correct_option and correct_option["id"] == body.answer_id

    return {
        "lesson_id": body.lesson_id,
        "answer_id": body.answer_id,
        "correct": bool(is_correct),
        "correct_id": correct_option["id"] if correct_option else None,
        "explanation": correct_option["text"] if correct_option else None,
    }


@router.post("/what-outputs")
def check_what_outputs(body: QuizAnswer) -> dict[str, Any]:
    lessons = _load_lessons()
    lesson = next((x for x in lessons if x["id"] == body.lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    what_outputs = lesson.get("what_outputs")
    if not what_outputs:
        raise HTTPException(status_code=400, detail="This lesson has no what_outputs section")

    is_correct = what_outputs["correct"] == body.answer_id
    return {
        "lesson_id": body.lesson_id,
        "answer": body.answer_id,
        "correct": is_correct,
        "correct_answer": what_outputs["correct"],
    }
