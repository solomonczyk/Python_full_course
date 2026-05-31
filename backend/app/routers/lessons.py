import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/lessons", tags=["lessons"])

_DATA_FILE = Path(__file__).parent.parent / "data" / "lessons.json"
_cache: list[dict[str, Any]] | None = None


def _load_lessons() -> list[dict[str, Any]]:
    global _cache
    if _cache is None:
        with open(_DATA_FILE, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def invalidate_cache() -> None:
    global _cache
    _cache = None


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
def get_lesson(lesson_id: str) -> dict[str, Any]:
    lessons = _load_lessons()
    for lesson in lessons:
        if lesson["id"] == lesson_id:
            return lesson
    raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")
