"""Tests for Beta Progress Persistence API.

Tests the modular backend (backend/app/main.py) which includes the
beta_progress router. All endpoints are prefixed with /beta/progress.
"""

import sys
import json
from pathlib import Path

# Point to the backend modular app
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app
from app.database import get_connection

client = TestClient(app)


# ── Fixtures ─────────────────────────────────────────────────────────────────

TEST_CODE = "BETA-TEST12"
TEST_CODE_ALT = "BETA-TEST34"
INVALID_CODE = "BETA-INVALID"  # not created


def _cleanup_test_data():
    """Remove test data from the database after tests."""
    with get_connection() as conn:
        conn.execute("DELETE FROM beta_progress WHERE participant_code LIKE 'BETA-TEST%'")
        conn.commit()


# ── 1. Create progress by participant code ───────────────────────────────────

def test_create_beta_progress():
    """POST /beta/progress/create creates a new beta progress entry."""
    _cleanup_test_data()
    r = client.post("/beta/progress/create", json={"participant_code": TEST_CODE})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["participant_code"] == TEST_CODE
    assert data["participant_id"].startswith("p_")
    assert data["current_lesson_id"] == "1-1"
    assert data["completed_lessons"] == []
    assert "created_at" in data


def test_create_beta_progress_idempotent():
    """POST /beta/progress/create is idempotent — second call returns existing."""
    _cleanup_test_data()
    # First create
    r1 = client.post("/beta/progress/create", json={"participant_code": TEST_CODE_ALT})
    assert r1.status_code == 200
    # Second create (same code)
    r2 = client.post("/beta/progress/create", json={"participant_code": TEST_CODE_ALT})
    assert r2.status_code == 200
    data = r2.json()
    assert data["ok"] is True
    assert data["participant_code"] == TEST_CODE_ALT
    assert data["created_at"] == r1.json()["created_at"]  # Same timestamp


# ── 2. Get progress by participant code ──────────────────────────────────────

def test_get_beta_progress():
    """GET /beta/progress/{code} returns created progress."""
    _cleanup_test_data()
    client.post("/beta/progress/create", json={"participant_code": TEST_CODE})
    r = client.get(f"/beta/progress/{TEST_CODE}")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["found"] is True
    assert data["participant_code"] == TEST_CODE
    assert data["current_lesson_id"] == "1-1"
    assert data["completed_lessons"] == []


# ── 3. Invalid code returns safe not found ───────────────────────────────────

def test_get_beta_progress_not_found():
    """GET /beta/progress/{invalid} returns found=False, safe message."""
    r = client.get(f"/beta/progress/{INVALID_CODE}")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["found"] is False
    assert "message" in data
    # No stack traces or internal errors
    assert "error" not in data
    assert "traceback" not in str(data).lower()


# ── 4. Update current lesson ─────────────────────────────────────────────────

def test_update_current_lesson():
    """PUT /beta/progress/{code} updates current_lesson_id."""
    _cleanup_test_data()
    client.post("/beta/progress/create", json={"participant_code": TEST_CODE})
    r = client.put(
        f"/beta/progress/{TEST_CODE}",
        json={"current_lesson_id": "2-3"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["current_lesson_id"] == "2-3"


# ── 5. Lesson started ────────────────────────────────────────────────────────

def test_lesson_started():
    """POST /beta/progress/{code}/lesson-started marks lesson as started."""
    _cleanup_test_data()
    client.post("/beta/progress/create", json={"participant_code": TEST_CODE})
    r = client.post(
        f"/beta/progress/{TEST_CODE}/lesson-started",
        json={"lesson_id": "1-2"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True

    # Verify it was saved
    r2 = client.get(f"/beta/progress/{TEST_CODE}")
    data2 = r2.json()
    assert data2["lesson_status"].get("1-2") == "started"
    assert data2["current_lesson_id"] == "1-2"


# ── 6. Save mission failed ───────────────────────────────────────────────────

def test_mission_failed():
    """POST /beta/progress/{code}/mission-result saves failure."""
    _cleanup_test_data()
    client.post("/beta/progress/create", json={"participant_code": TEST_CODE})

    r = client.post(
        f"/beta/progress/{TEST_CODE}/mission-result",
        json={"lesson_id": "1-1", "passed": False, "attempts": 1, "hints_used": 0},
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True

    r2 = client.get(f"/beta/progress/{TEST_CODE}")
    stats = r2.json()["mission_stats"]["1-1"]
    assert stats["passed"] is False
    assert stats["failed"] >= 1
    assert stats["attempts"] == 1


# ── 7. Save mission passed ───────────────────────────────────────────────────

def test_mission_passed():
    """POST /beta/progress/{code}/mission-result saves pass and completion."""
    _cleanup_test_data()
    client.post("/beta/progress/create", json={"participant_code": TEST_CODE})

    r = client.post(
        f"/beta/progress/{TEST_CODE}/mission-result",
        json={"lesson_id": "1-1", "passed": True, "attempts": 2, "hints_used": 1},
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True

    r2 = client.get(f"/beta/progress/{TEST_CODE}")
    data = r2.json()
    stats = data["mission_stats"]["1-1"]
    assert stats["passed"] is True
    assert stats["attempts"] == 2
    assert stats["hints_used"] == 1
    assert "1-1" in data["completed_lessons"]
    assert data["lesson_status"]["1-1"] == "completed"


# ── 8. Save hint used ────────────────────────────────────────────────────────

def test_hint_used():
    """POST /beta/progress/{code}/hint-used increments hints_used."""
    _cleanup_test_data()
    client.post("/beta/progress/create", json={"participant_code": TEST_CODE})
    # First mark a mission attempt to initialize stats
    client.post(
        f"/beta/progress/{TEST_CODE}/mission-result",
        json={"lesson_id": "1-1", "passed": False, "attempts": 1, "hints_used": 0},
    )

    r = client.post(
        f"/beta/progress/{TEST_CODE}/hint-used",
        json={"lesson_id": "1-1"},
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True

    r2 = client.get(f"/beta/progress/{TEST_CODE}")
    stats = r2.json()["mission_stats"]["1-1"]
    assert stats["hints_used"] >= 1


# ── 9. Save lesson completed ─────────────────────────────────────────────────

def test_lesson_completed():
    """POST /beta/progress/{code}/lesson-completed marks lesson done."""
    _cleanup_test_data()
    client.post("/beta/progress/create", json={"participant_code": TEST_CODE})

    r = client.post(
        f"/beta/progress/{TEST_CODE}/lesson-completed",
        json={"lesson_id": "2-1"},
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True

    r2 = client.get(f"/beta/progress/{TEST_CODE}")
    data = r2.json()
    assert "2-1" in data["completed_lessons"]
    assert data["lesson_status"]["2-1"] == "completed"


# ── 10. No personal fields accepted/stored ───────────────────────────────────

def test_no_personal_data_stored():
    """Beta progress endpoint rejects personal data fields."""
    _cleanup_test_data()
    # The model only accepts participant_code — personal fields are not in the schema
    r = client.post(
        "/beta/progress/create",
        json={
            "participant_code": TEST_CODE,
            "email": "test@example.com",
            "child_name": "Test",
        },
    )
    # FastAPI ignores extra fields — but verify they are NOT in the response
    assert r.status_code == 200
    data = r.json()
    assert "email" not in data
    assert "child_name" not in data
    assert "phone" not in data

    # Also verify they are not in the DB
    r2 = client.get(f"/beta/progress/{TEST_CODE}")
    data2 = r2.json()
    assert "email" not in data2
    assert "child_name" not in data2
    assert "phone" not in data2


# ── 11. Case insensitivity ───────────────────────────────────────────────────

def test_participant_code_case_insensitive():
    """Participant codes are case-insensitive (stored upper)."""
    _cleanup_test_data()
    r = client.post("/beta/progress/create", json={"participant_code": "beta-test99"})
    assert r.status_code == 200
    assert r.json()["participant_code"] == "BETA-TEST99"


# ── 12. Auto-create on lesson-started for new code ───────────────────────────

def test_lesson_started_auto_creates():
    """lesson-started auto-creates progress for new participant code."""
    _cleanup_test_data()
    code = "BETA-AUTO1"
    r = client.post(
        f"/beta/progress/{code}/lesson-started",
        json={"lesson_id": "3-1"},
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True

    r2 = client.get(f"/beta/progress/{code}")
    assert r2.json()["found"] is True
    assert r2.json()["current_lesson_id"] == "3-1"


# ── 13. Multiple lessons accumulation ────────────────────────────────────────

def test_multiple_lessons_accumulate():
    """Progress accumulates across multiple lessons."""
    _cleanup_test_data()
    client.post("/beta/progress/create", json={"participant_code": TEST_CODE})

    # Complete 1-1
    client.post(
        f"/beta/progress/{TEST_CODE}/lesson-completed",
        json={"lesson_id": "1-1"},
    )
    # Complete 1-2
    client.post(
        f"/beta/progress/{TEST_CODE}/lesson-completed",
        json={"lesson_id": "1-2"},
    )

    r = client.get(f"/beta/progress/{TEST_CODE}")
    data = r.json()
    assert "1-1" in data["completed_lessons"]
    assert "1-2" in data["completed_lessons"]
    assert len(data["completed_lessons"]) == 2


# ── 14. Participant ID is deterministic hash ─────────────────────────────────

def test_participant_id_is_deterministic_hash():
    """participant_id is a deterministic hash, not the raw code."""
    _cleanup_test_data()
    r = client.post("/beta/progress/create", json={"participant_code": TEST_CODE})
    pid = r.json()["participant_id"]
    assert pid.startswith("p_")
    assert TEST_CODE.lower() not in pid  # Not the raw code
    assert TEST_CODE not in pid

    # Same code produces same hash
    r2 = client.post("/beta/progress/create", json={"participant_code": TEST_CODE})
    assert r2.json()["participant_id"] == pid


# ── Cleanup ──────────────────────────────────────────────────────────────────

def _cleanup_all_test_data():
    _cleanup_test_data()
