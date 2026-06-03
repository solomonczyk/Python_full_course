"""Tests for Beta Staged Access API.

Tests the modular backend (backend/app/main.py) which includes the
beta_access router. All endpoints are prefixed with /beta/access.
"""

import sys
from pathlib import Path

# Point to the backend modular app
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app
from app.database import get_connection

client = TestClient(app)

# ── Fixtures ─────────────────────────────────────────────────────────────────

TEST_CODE = "BETA-ACCESS1"
TEST_CODE_ALT = "BETA-ACCESS2"
OPERATOR_KEY = "op-python-quest-dev-2026"
BAD_OPERATOR_KEY = "wrong-key"


def _cleanup_test_data():
    """Remove test data from the database after tests."""
    with get_connection() as conn:
        conn.execute("DELETE FROM beta_stages WHERE participant_code LIKE 'BETA-ACCESS%'")
        conn.commit()


# ── 1. Default stage ─────────────────────────────────────────────────────────


def test_get_access_default_stage():
    """GET /beta/access/{code} returns stage=1 for new participant."""
    _cleanup_test_data()
    r = client.get(f"/beta/access/{TEST_CODE}")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["participant_code"] == TEST_CODE
    assert data["current_stage"] == 1
    assert data["max_stage"] == 5
    assert data["has_feedback"] is False
    assert data["feedback_submitted_at"] is None


# ── 2. Provide feedback ──────────────────────────────────────────────────────


def test_provide_feedback():
    """POST /beta/access/{code}/provide-feedback stores feedback."""
    _cleanup_test_data()
    # Ensure row exists first
    client.get(f"/beta/access/{TEST_CODE}")

    r = client.post(
        f"/beta/access/{TEST_CODE}/provide-feedback",
        json={"feedback_text": "Great course! I learned a lot about print()."},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["message"] == "Feedback submitted"

    # Verify the feedback was stored
    r2 = client.get(f"/beta/access/{TEST_CODE}")
    assert r2.json()["has_feedback"] is True
    assert r2.json()["feedback_submitted_at"] is not None


def test_provide_feedback_min_length():
    """POST /beta/access/{code}/provide-feedback rejects short feedback."""
    _cleanup_test_data()
    client.get(f"/beta/access/{TEST_CODE}")

    r = client.post(
        f"/beta/access/{TEST_CODE}/provide-feedback",
        json={"feedback_text": "OK"},
    )
    assert r.status_code == 422  # Pydantic validation error


def test_provide_feedback_with_rating():
    """POST /beta/access/{code}/provide-feedback accepts optional rating."""
    _cleanup_test_data()
    client.get(f"/beta/access/{TEST_CODE}")

    r = client.post(
        f"/beta/access/{TEST_CODE}/provide-feedback",
        json={"feedback_text": "Excellent course with clear explanations.", "rating": 4},
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True


# ── 3. Operator unlock ────────────────────────────────────────────────────────


def test_operator_unlock_success():
    """POST /beta/access/{code}/operator-unlock unlocks next stage after feedback."""
    _cleanup_test_data()
    # Create + submit feedback
    client.get(f"/beta/access/{TEST_CODE}")
    client.post(
        f"/beta/access/{TEST_CODE}/provide-feedback",
        json={"feedback_text": "Ready for more! Part 1 was great."},
    )

    # Unlock via operator
    r = client.post(
        f"/beta/access/{TEST_CODE}/operator-unlock",
        headers={"X-Operator-Key": OPERATOR_KEY},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["previous_stage"] == 1
    assert data["current_stage"] == 2
    assert "Stage unlocked" in data["message"]

    # Verify stage persisted
    r2 = client.get(f"/beta/access/{TEST_CODE}")
    assert r2.json()["current_stage"] == 2


def test_operator_unlock_requires_feedback():
    """POST /beta/access/{code}/operator-unlock fails without feedback."""
    _cleanup_test_data()
    client.get(f"/beta/access/{TEST_CODE}")  # Create row, no feedback

    r = client.post(
        f"/beta/access/{TEST_CODE}/operator-unlock",
        headers={"X-Operator-Key": OPERATOR_KEY},
    )
    assert r.status_code == 200  # Returns error response, not 4xx
    data = r.json()
    assert data["ok"] is False
    assert "feedback" in data["detail"].lower()


def test_operator_unlock_invalid_key():
    """POST /beta/access/{code}/operator-unlock rejects invalid operator key."""
    _cleanup_test_data()
    client.get(f"/beta/access/{TEST_CODE}")

    r = client.post(
        f"/beta/access/{TEST_CODE}/operator-unlock",
        headers={"X-Operator-Key": BAD_OPERATOR_KEY},
    )
    assert r.status_code == 403
    assert "Invalid operator key" in r.json()["detail"]


def test_operator_unlock_missing_key():
    """POST /beta/access/{code}/operator-unlock rejects missing operator key."""
    _cleanup_test_data()
    client.get(f"/beta/access/{TEST_CODE}")

    r = client.post(f"/beta/access/{TEST_CODE}/operator-unlock")
    assert r.status_code == 403


def test_operator_unlock_max_stage():
    """POST /beta/access/{code}/operator-unlock fails at max stage."""
    _cleanup_test_data()
    # Create row, submit feedback, unlock through all stages
    client.get(f"/beta/access/{TEST_CODE}")
    client.post(
        f"/beta/access/{TEST_CODE}/provide-feedback",
        json={"feedback_text": f"Unlock to stage {s}" for s in range(2, 6)},
    )

    # Unlock 1→2, 2→3, 3→4, 4→5
    for _ in range(4):
        client.post(
            f"/beta/access/{TEST_CODE}/operator-unlock",
            headers={"X-Operator-Key": OPERATOR_KEY},
        )
        # Re-submit feedback for next unlock
        client.post(
            f"/beta/access/{TEST_CODE}/provide-feedback",
            json={"feedback_text": "More please!"},
        )

    # Now at stage 5, try to unlock again
    r = client.post(
        f"/beta/access/{TEST_CODE}/operator-unlock",
        headers={"X-Operator-Key": OPERATOR_KEY},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "maximum" in data["detail"].lower()


# ── 4. Lesson stage enforcement ──────────────────────────────────────────────


def test_lesson_stage_blocked_403():
    """GET /lessons/{id} with X-Participant-Code returns 403 if part beyond stage."""
    _cleanup_test_data()
    # Participant at stage 1 (Part 1 only)
    client.get(f"/beta/access/{TEST_CODE}")

    # Try to access a Part 3 lesson
    r = client.get(
        "/lessons/3-1",
        headers={"X-Participant-Code": TEST_CODE},
    )
    assert r.status_code == 403
    data = r.json()
    detail = data["detail"]
    assert detail["reason"] == "staged_access"
    assert detail["current_stage"] == 1
    assert detail["lesson_part"] == 3
    assert detail["max_stage"] == 5


def test_lesson_stage_allowed():
    """GET /lessons/{id} with X-Participant-Code returns 200 if part within stage."""
    _cleanup_test_data()
    # Participant at stage 1 (Part 1 only)
    client.get(f"/beta/access/{TEST_CODE}")

    r = client.get(
        "/lessons/1-1",
        headers={"X-Participant-Code": TEST_CODE},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "1-1"
    assert data["part"] == 1


def test_lesson_unlocked_after_operator():
    """Lesson that was 403 becomes 200 after operator unlocks next stage."""
    _cleanup_test_data()
    # Create + submit feedback
    client.get(f"/beta/access/{TEST_CODE}")
    client.post(
        f"/beta/access/{TEST_CODE}/provide-feedback",
        json={"feedback_text": "Unlock Part 2 please!"},
    )

    # Initially blocked
    r1 = client.get(
        "/lessons/2-1",
        headers={"X-Participant-Code": TEST_CODE},
    )
    assert r1.status_code == 403

    # Operator unlocks to stage 2
    client.post(
        f"/beta/access/{TEST_CODE}/operator-unlock",
        headers={"X-Operator-Key": OPERATOR_KEY},
    )

    # Now Part 2 is accessible
    r2 = client.get(
        "/lessons/2-1",
        headers={"X-Participant-Code": TEST_CODE},
    )
    assert r2.status_code == 200
    assert r2.json()["id"] == "2-1"


# ── 5. Pending feedback ───────────────────────────────────────────────────────


def test_pending_feedback():
    """GET /beta/access/operator/pending-feedback lists participants needing review."""
    _cleanup_test_data()
    # Create participant with feedback
    client.get(f"/beta/access/{TEST_CODE}")
    client.post(
        f"/beta/access/{TEST_CODE}/provide-feedback",
        json={"feedback_text": "I enjoyed Part 1!"},
    )

    r = client.get(
        "/beta/access/operator/pending-feedback",
        headers={"X-Operator-Key": OPERATOR_KEY},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    pending = data["pending"]
    # Our test code should appear in pending
    codes = [p["participant_code"] for p in pending]
    assert TEST_CODE in codes


def test_pending_feedback_invalid_key():
    """GET /beta/access/operator/pending-feedback rejects invalid key."""
    r = client.get(
        "/beta/access/operator/pending-feedback",
        headers={"X-Operator-Key": BAD_OPERATOR_KEY},
    )
    assert r.status_code == 403


# ── 6. Multi-stage progression ────────────────────────────────────────────────


def test_multiple_stage_progression():
    """Operator can unlock through multiple stages incrementally."""
    _cleanup_test_data()
    client.get(f"/beta/access/{TEST_CODE}")

    for target in range(2, 5):
        # Re-submit feedback before each unlock
        client.post(
            f"/beta/access/{TEST_CODE}/provide-feedback",
            json={"feedback_text": f"Please unlock to stage {target}!"},
        )

        r = client.post(
            f"/beta/access/{TEST_CODE}/operator-unlock",
            headers={"X-Operator-Key": OPERATOR_KEY},
        )
        assert r.status_code == 200
        assert r.json()["current_stage"] == target

        # Verify lesson access matches new stage
        part_to_check = target
        lesson_id = f"{part_to_check}-1"
        r_lesson = client.get(
            f"/lessons/{lesson_id}",
            headers={"X-Participant-Code": TEST_CODE},
        )
        assert r_lesson.status_code == 200
        assert r_lesson.json()["part"] == part_to_check


# ── 7. No header → backward compatible ───────────────────────────────────────


def test_lesson_without_participant_code():
    """GET /lessons/{id} without X-Participant-Code works as before."""
    # No header at all — should work for all lessons
    r = client.get("/lessons/3-1")
    assert r.status_code == 200
    assert r.json()["id"] == "3-1"

    r = client.get("/lessons/5-7")
    assert r.status_code == 200
    assert r.json()["id"] == "5-7"

    r = client.get("/lessons/1-1")
    assert r.status_code == 200
    assert r.json()["id"] == "1-1"


# ── 8. No personal data in responses ─────────────────────────────────────────


def test_no_personal_data_stored():
    """Ensure no personal data leaks in responses."""
    _cleanup_test_data()
    r = client.get(f"/beta/access/{TEST_CODE}")
    data = r.json()
    # Only participant code is stored, no PII
    assert "email" not in data
    assert "password" not in data
    assert "name" not in data
    assert "phone" not in data
    assert "feedback_text" not in data  # feedback text is in detail endpoint
    assert r.status_code == 200
