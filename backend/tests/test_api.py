"""Tests for Python Quest API."""

import sys
import json
from pathlib import Path

# Make sure we can import the api module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "api"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient

# Import the app — try both possible locations
try:
    from api.index import app
except (ImportError, ModuleNotFoundError):
    try:
        from index import app
    except (ImportError, ModuleNotFoundError) as e:
        print(f"Could not import app: {e}")
        print(f"sys.path: {sys.path}")
        sys.exit(1)

client = TestClient(app)


def test_lessons():
    """GET /lessons returns a list of all lessons."""
    r = client.get("/lessons")
    assert r.status_code == 200
    lessons = r.json()
    assert isinstance(lessons, list)
    assert len(lessons) > 50, f"Expected 50+ lessons, got {len(lessons)}"
    # Check summary fields
    lesson = lessons[0]
    assert "id" in lesson
    assert "difficulty" in lesson, f"Missing difficulty in {lesson.get('id')}"
    assert "estimated_time_min" in lesson, f"Missing estimated_time_min in {lesson.get('id')}"


def test_lesson_detail():
    """GET /lessons/{id} returns full lesson data."""
    r = client.get("/lessons/1-1")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "1-1"
    assert len(data["pre_topic_dialogue"]) > 0
    assert "quiz" in data
    assert "what_outputs" in data
    assert "mission" in data


def test_quiz_check():
    """POST /quiz/check returns correct result."""
    r = client.post("/quiz/check", json={"lesson_id": "1-1", "answer_id": "a"})
    assert r.status_code == 200
    result = r.json()
    assert "correct" in result
    assert "explanation" in result


def test_mission_check():
    """POST /mission/check validates code output."""
    r = client.post("/mission/check", json={
        "lesson_id": "1-1",
        "code": "print('Я начинаю путь Python')",
    })
    assert r.status_code == 200
    result = r.json()
    assert "correct" in result
    assert "actual_output" in result


def test_mission_check_forbidden():
    """POST /mission/check rejects forbidden imports."""
    r = client.post("/mission/check", json={
        "lesson_id": "1-1",
        "code": "import os\nprint('test')",
    })
    assert r.status_code == 200
    result = r.json()
    assert result["correct"] is False
    assert "запрещён" in (result.get("error") or "").lower()


def test_reviews():
    """GET /reviews returns review blocks."""
    r = client.get("/reviews")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    # Should have at least 8 review blocks
    assert len(data) >= 8, f"Expected 8+ reviews, got {len(data)}"


def test_review_detail():
    """GET /reviews/{id} returns a single review block."""
    r = client.get("/reviews/r-1")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "r-1"
    assert "dialogue" in data
    assert "questions" in data


def test_dialogues_not_templated():
    """Lesson 2-3 pre_topic_dialogue should not mention 'and, or, not'."""
    r = client.get("/lessons/2-3")
    data = r.json()
    dialogues = data.get("pre_topic_dialogue", [])
    texts = [d["text"] for d in dialogues]
    assert not any("and, or, not" in t for t in texts), (
        "Lesson 2-3 still has copied and/or/not dialogue"
    )


def test_quiz_not_placeholder():
    """Lesson 3-7 quiz should not be a stub."""
    r = client.get("/lessons/3-7")
    data = r.json()
    question = data["quiz"]["question"]
    assert "Что изучается в уроке" not in question, (
        f"Lesson 3-7 still has stub quiz: {question}"
    )


def test_find_bug_3_2_fixed():
    """Lesson 3-2 find_bug should have correct answer with / not //."""
    r = client.get("/lessons/3-2")
    data = r.json()
    fb = data["find_bug"]
    assert "correct" in fb
    assert "print(a / b)" in fb["correct"], (
        f"Expected print(a / b) in correct, got: {fb['correct']}"
    )
    assert "//" in fb["hint"].lower() or "целочисленн" in fb["hint"].lower(), (
        f"Hint should mention //: {fb['hint']}"
    )


def test_what_outputs_has_options():
    """No lesson should have empty what_outputs options."""
    r = client.get("/lessons")
    lessons = r.json()
    for lesson_summary in lessons:
        detail = client.get(f"/lessons/{lesson_summary['id']}")
        data = detail.json()
        wo = data.get("what_outputs", {})
        if wo and not wo.get("options"):
            assert False, f"Lesson {data['id']} has empty what_outputs options"


def test_no_stub_quizzes_in_lessons():
    """No lesson should have a stub quiz question."""
    r = client.get("/lessons")
    lessons = r.json()
    for lesson_summary in lessons:
        detail = client.get(f"/lessons/{lesson_summary['id']}")
        data = detail.json()
        q = data.get("quiz", {})
        if "Что изучается" in q.get("question", ""):
            assert False, f"Lesson {data['id']} still has stub quiz: {q['question']}"


def test_no_stub_quizzes_in_reviews():
    """No review should have a stub quiz question."""
    r = client.get("/reviews")
    reviews = r.json()
    for review_summary in reviews:
        detail = client.get(f"/reviews/{review_summary['id']}")
        data = detail.json()
        for q in data.get("questions", []):
            if "Что изучается" in q.get("question", ""):
                assert False, (
                    f"Review {data['id']} still has stub quiz: {q['question']}"
                )


def test_locked_lessons():
    """Parts 2+ lessons should be locked (except 2-1)."""
    r = client.get("/lessons")
    lessons = r.json()
    for l in lessons:
        if l["part"] == 1:
            assert l["locked"] is False, f"Lesson {l['id']} part 1 should be unlocked"
        elif l["id"] == "2-1":
            assert l["locked"] is False, "Lesson 2-1 should be unlocked"
        else:
            assert l["locked"] is True, f"Lesson {l['id']} part 2+ should be locked"


def test_progress_endpoint():
    """GET /progress without X-User-Id returns 400."""
    r = client.get("/progress")
    assert r.status_code == 400
    data = r.json()
    assert "X-User-Id" in data.get("detail", "")


def test_health():
    """GET /health returns healthy."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_review_find_bug_has_correct():
    """All review find_bug blocks should have correct field."""
    r = client.get("/reviews")
    reviews = r.json()
    for rs in reviews:
        detail = client.get(f"/reviews/{rs['id']}")
        data = detail.json()
        fb = data.get("find_bug", {})
        if fb and not fb.get("correct"):
            assert False, f"Review {data['id']} find_bug missing correct field"


def test_progress_with_user_id():
    """GET /progress with X-User-Id returns 200."""
    r = client.get("/progress", headers={"X-User-Id": "test-user"})
    assert r.status_code == 200


# ── Quest endpoint tests ────────────────────────────────────────────────────

def test_quests():
    """GET /quests returns all quests."""
    r = client.get("/quests")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 6, f"Expected 6+ quests, got {len(data)}"
    quest = data[0]
    assert "id" in quest
    assert "part" in quest
    assert "title" in quest


def test_quest_detail():
    """GET /quests/{id} returns full quest data."""
    r = client.get("/quests/quest-1")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "quest-1"
    assert "story" in data
    assert "test_cases" in data
    assert "task" in data
    assert "starter_code" in data


def test_capstone_quest():
    """GET /quests/quest-6 returns capstone quest."""
    r = client.get("/quests/quest-6")
    assert r.status_code == 200
    data = r.json()
    assert data.get("is_capstone") is True, "quest-6 should have is_capstone=true"
    required = data.get("required_lessons", [])
    assert len(required) >= 80, f"Capstone should reference 80+ lessons, got {len(required)}"


def test_quest_not_found():
    """GET /quests/nonexistent returns 404."""
    r = client.get("/quests/nonexistent-quest")
    assert r.status_code == 404


def test_quest_check_valid():
    """POST /quests/{quest_id}/check validates code for quest-1."""
    code = "name = input()\nlevel = int(input())\nelement = input()\nprint('Герой:', name)\nprint('Стихия:', element)\nif level >= 5:\n    print('Врата открываются!')\nelse:\n    print('Нужно больше тренировок.')"
    r = client.post("/quests/quest-1/check", json={"code": code})
    assert r.status_code == 200
    result = r.json()
    assert "all_passed" in result
    assert result["all_passed"] is True, f"Quest check should pass, got: {result}"
    assert len(result["results"]) == 2


def test_quest_check_invalid():
    """POST /quests/{quest_id}/check with bad code returns failures."""
    code = "print('hello')"
    r = client.post("/quests/quest-1/check", json={"code": code})
    assert r.status_code == 200
    result = r.json()
    assert result["all_passed"] is False


def test_quest_check_forbidden():
    """POST /quests/{quest_id}/check rejects forbidden imports."""
    code = "import os\nprint('hello')"
    r = client.post("/quests/quest-1/check", json={"code": code})
    assert r.status_code == 200
    result = r.json()
    assert result["all_passed"] is False
    assert "запрещён" in (result.get("error") or "").lower()


# ── Recap endpoint tests ────────────────────────────────────────────────────

def test_recaps():
    """GET /recaps returns all recaps."""
    r = client.get("/recaps")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 9, f"Expected 9+ recaps, got {len(data)}"


def test_recap_detail():
    """GET /recaps/{id} returns a single recap."""
    r = client.get("/recaps/recap-1")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "recap-1"
    assert "story_summary" in data
    assert "hero_skills" in data
    assert "key_rules" in data
    assert "mini_check" in data


def test_sub_recap_detail():
    """GET /recaps/recap-3a returns Part 3 checkpoint recap."""
    r = client.get("/recaps/recap-3a")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "recap-3a"
    assert data["part"] == 3
    assert len(data.get("mini_check", [])) >= 3
    assert len(data.get("key_rules", [])) >= 5


def test_sub_recap_all_exist():
    """All 4 Part 3 sub-recaps exist."""
    for rid in ["recap-3a", "recap-3b", "recap-3c", "recap-3d"]:
        r = client.get(f"/recaps/{rid}")
        assert r.status_code == 200, f"Sub-recap {rid} not found"
        assert r.json()["part"] == 3


def test_recap_not_found():
    """GET /recaps/nonexistent returns 404."""
    r = client.get("/recaps/nonexistent-recap")
    assert r.status_code == 404
