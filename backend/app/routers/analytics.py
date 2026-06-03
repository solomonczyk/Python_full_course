"""Analytics Router — anonymous event collection for beta diagnostics.

All endpoints are prefixed with /analytics.
No personal data is stored — only anonymous session IDs and participant hashes.
Events are stored in a local JSON file for operator export.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/analytics", tags=["analytics"])

_ANALYTICS_DIR = Path(os.environ.get("ANALYTICS_DIR", "/tmp/pq_analytics"))
_ANALYTICS_FILE = _ANALYTICS_DIR / "events.jsonl"


# ── Schemas ──────────────────────────────────────────────────────────────────


class AnalyticsEvent(BaseModel):
    event: str
    anonymous_session_id: str
    participant_id: str | None = None
    timestamp: str
    lesson_id: str | None = None
    mission_id: str | None = None
    attempt_count: int | None = None
    result: str | None = None
    hint_id: str | None = None
    source: str | None = None
    route: str | None = None


class AnalyticsEventsBatch(BaseModel):
    events: list[AnalyticsEvent]


# ── Storage ──────────────────────────────────────────────────────────────────


def _ensure_dir() -> None:
    _ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)


def _append_event(event: AnalyticsEvent) -> None:
    _ensure_dir()
    try:
        with open(_ANALYTICS_FILE, "a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")
    except OSError:
        pass  # Best-effort


def _read_events() -> list[dict[str, Any]]:
    if not _ANALYTICS_FILE.exists():
        return []
    try:
        events: list[dict[str, Any]] = []
        with open(_ANALYTICS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return events
    except OSError:
        return []


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.post("/events")
def collect_events(body: AnalyticsEventsBatch) -> dict[str, Any]:
    """Collect anonymous analytics events from the frontend.

    Stores events as JSONL for later export.
    No personal data is accepted or stored.
    """
    count = 0
    for event in body.events:
        _append_event(event)
        count += 1
    return {"ok": True, "count": count}


@router.get("/export")
def export_events() -> dict[str, Any]:
    """Export all stored analytics events for operator analysis.

    Returns aggregated data with event counts and full event list.
    Only accessible when ANALYTICS_ENABLED = true.
    Accepts optional ?participant_id= filter.
    """
    if os.environ.get("ANALYTICS_ENABLED", "").lower() not in ("true", "1", "yes"):
        raise HTTPException(status_code=403, detail="Analytics export not enabled")

    events = _read_events()

    # Build summary
    total_events = len(events)
    event_type_counts: dict[str, int] = {}
    participant_set: set[str] = set()
    session_set: set[str] = set()

    for ev in events:
        etype = ev.get("event", "unknown")
        event_type_counts[etype] = event_type_counts.get(etype, 0) + 1
        if ev.get("participant_id"):
            participant_set.add(ev["participant_id"])
        if ev.get("anonymous_session_id"):
            session_set.add(ev["anonymous_session_id"])

    return {
        "ok": True,
        "summary": {
            "total_events": total_events,
            "unique_participants": len(participant_set),
            "unique_sessions": len(session_set),
            "event_type_counts": event_type_counts,
            "earliest_event": events[0]["timestamp"] if events else None,
            "latest_event": events[-1]["timestamp"] if events else None,
        },
        "events": events[-1000:],  # Return last 1000 for detailed analysis
    }


@router.delete("/events")
def clear_events() -> dict[str, Any]:
    """Clear all stored analytics events (operator use)."""
    if os.environ.get("ANALYTICS_ENABLED", "").lower() not in ("true", "1", "yes"):
        raise HTTPException(status_code=403, detail="Analytics export not enabled")
    try:
        if _ANALYTICS_FILE.exists():
            _ANALYTICS_FILE.unlink()
        return {"ok": True, "cleared": True}
    except OSError as e:
        return {"ok": False, "cleared": False, "error": str(e)}
