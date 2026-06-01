import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/quests", tags=["quests"])

_DATA_FILE = Path(__file__).parent.parent / "data" / "chapter_quests.json"
_cache: list[dict[str, Any]] | None = None


def _load_quests() -> list[dict[str, Any]]:
    global _cache
    if _cache is None:
        with open(_DATA_FILE, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def invalidate_cache() -> None:
    global _cache
    _cache = None


@router.get("")
def list_quests() -> list[dict[str, Any]]:
    """Return all quests (summary fields)."""
    quests = _load_quests()
    SUMMARY_FIELDS = ("id", "part", "title")
    return [
        {k: quest[k] for k in SUMMARY_FIELDS if k in quest}
        for quest in quests
    ]


@router.get("/{quest_id}")
def get_quest(quest_id: str) -> dict[str, Any]:
    """Return a single quest by ID."""
    quests = _load_quests()
    for quest in quests:
        if quest["id"] == quest_id:
            return quest
    raise HTTPException(status_code=404, detail=f"Quest '{quest_id}' not found")
