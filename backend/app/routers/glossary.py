import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/glossary", tags=["glossary"])

_DATA_FILE = Path(__file__).parent.parent / "data" / "glossary.json"
_cache: list[dict[str, Any]] | None = None


def _load_terms() -> list[dict[str, Any]]:
    global _cache
    if _cache is None:
        with open(_DATA_FILE, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def invalidate_cache() -> None:
    global _cache
    _cache = None


@router.get("")
def list_terms() -> list[dict[str, Any]]:
    """Return all glossary terms (summary fields)."""
    terms = _load_terms()
    SUMMARY_FIELDS = ("id", "term", "python_name", "category", "beginner_level")
    return [
        {k: term[k] for k in SUMMARY_FIELDS if k in term}
        for term in terms
    ]


@router.get("/{term_id}")
def get_term(term_id: str) -> dict[str, Any]:
    """Return a single glossary term by ID."""
    terms = _load_terms()
    for term in terms:
        if term["id"] == term_id:
            return term
    raise HTTPException(status_code=404, detail=f"Glossary term '{term_id}' not found")


@router.get("/category/{category}")
def list_by_category(category: str) -> list[dict[str, Any]]:
    """Return all terms in a given category."""
    terms = _load_terms()
    filtered = [t for t in terms if t.get("category") == category]
    if not filtered:
        raise HTTPException(status_code=404, detail=f"No terms found for category '{category}'")
    SUMMARY_FIELDS = ("id", "term", "python_name", "category", "beginner_level")
    return [
        {k: term[k] for k in SUMMARY_FIELDS if k in term}
        for term in filtered
    ]
