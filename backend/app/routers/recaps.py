import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/recaps", tags=["recaps"])

_DATA_FILE = Path(__file__).parent.parent / "data" / "recaps.json"
_cache: list[dict[str, Any]] | None = None


def _load_recaps() -> list[dict[str, Any]]:
    global _cache
    if _cache is None:
        with open(_DATA_FILE, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def invalidate_cache() -> None:
    global _cache
    _cache = None


@router.get("")
def list_recaps() -> list[dict[str, Any]]:
    """Return all recaps (summary fields)."""
    recaps = _load_recaps()
    SUMMARY_FIELDS = ("id", "part", "title")
    return [
        {k: recap[k] for k in SUMMARY_FIELDS if k in recap}
        for recap in recaps
    ]


@router.get("/{recap_id}")
def get_recap(recap_id: str) -> dict[str, Any]:
    """Return a single recap by ID."""
    recaps = _load_recaps()
    for recap in recaps:
        if recap["id"] == recap_id:
            return recap
    raise HTTPException(status_code=404, detail=f"Recap '{recap_id}' not found")
