import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "review_schedule.json"


def _load_review_schedule() -> dict:
    if not _DATA_PATH.exists():
        return {"total_reviews": 0, "reviews": []}
    with open(_DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@router.get("")
def list_reviews():
    """Return a summary list of all review blocks."""
    data = _load_review_schedule()
    results = []
    for r in data.get("reviews", []):
        results.append({
            "id": r["id"],
            "type": r["type"],
            "title": r["title"],
            "subtitle": r["subtitle"],
            "position_after": r["position_after"],
            "part": r["part"],
            "chapter": r["chapter"],
            "topics": r["topics"],
        })
    return results


@router.get("/{review_id}")
def get_review(review_id: str):
    """Return a single review block by ID."""
    data = _load_review_schedule()
    for r in data.get("reviews", []):
        if r["id"] == review_id:
            return r
    raise HTTPException(status_code=404, detail=f"Review {review_id} not found")
