import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from app.routers.beta_access import STAGE_PARTS, get_current_stage

router = APIRouter(prefix="/lessons", tags=["lessons"])

_DATA_FILE = Path(__file__).parent.parent / "data" / "lessons.json"


def _load_lessons() -> list[dict[str, Any]]:
    with open(_DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


@router.get("")
def list_lessons() -> list[dict[str, Any]]:
    lessons = _load_lessons()
    SUMMARY_FIELDS = ("id","part","chapter","lesson","slug","title","subtitle",
                      "topic","locked","difficulty","estimated_time_min")
    return [
        {k: lesson[k] for k in SUMMARY_FIELDS if k in lesson}
        | ({"scene_image": lesson["scene_image"]} if "scene_image" in lesson and lesson.get("scene_image") else {})
        for lesson in lessons
    ]


@router.get("/{lesson_id}")
def get_lesson(lesson_id: str, request: Request) -> dict[str, Any]:
    lessons = _load_lessons()
    for lesson in lessons:
        if lesson["id"] == lesson_id:
            participant_code = request.headers.get("X-Participant-Code")
            if participant_code:
                code = participant_code.strip().upper()
                stage = get_current_stage(code)
                allowed_parts = STAGE_PARTS.get(stage, [1])
                if lesson["part"] not in allowed_parts:
                    raise HTTPException(
                        status_code=403,
                        detail={
                            "reason": "staged_access",
                            "message": (
                                f"Part {lesson['part']} is not yet available. "
                                f"You have access to Stage {stage}/5 "
                                f"(Parts {', '.join(str(p) for p in allowed_parts)}). "
                                "Complete the current stage and provide feedback "
                                "to unlock the next one."
                            ),
                            "current_stage": stage,
                            "max_stage": 5,
                            "lesson_part": lesson["part"],
                        },
                    )
            return lesson
    raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")
