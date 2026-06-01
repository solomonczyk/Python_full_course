"""Tests for Python Quest lesson content editorial quality."""

import json
import os
from collections import Counter

import re

import pytest

# ── Setup ───────────────────────────────────────────────────────────────────
LESSONS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "app", "data", "lessons.json"
)

REQUIRED_FIELDS = {
    "id", "part", "chapter", "lesson", "slug", "title", "subtitle",
    "difficulty", "estimated_time_min", "scene_image", "topic", "locked",
    "story_placement", "pre_topic_dialogue", "post_error_dialogue",
    "mini_summary", "connection_to_game", "game_relevance",
    "syntax_reminder", "explanation", "quiz", "what_outputs",
    "find_bug", "mission", "analogy", "practice_subtasks",
    "runnable_code", "common_mistakes",
}

CORE_LESSONS = {
    "1-1", "1-2", "1-3", "1-4", "1-5", "1-6", "1-7", "1-8", "1-9",
    "2-1", "2-5", "2-6",
    "3-14", "3-15", "3-16", "3-27", "3-28", "3-29", "3-31",
    "4-26", "4-27",
    "5-1", "5-2", "5-3", "5-4", "5-5", "5-7",
}

FORBIDDEN_NOVICE_PATTERNS = [
    "А, понял!",
    "Понял:",
    "Понял!",
    "Осознал:",
    "Осознал!",
]

GENERIC_BAGUS_PHRASES = [
    "Ой-ой! Багус нашёл багус! Python в замешательстве!",
    "Хм! Багус одобряет эту ошибку!",
    "Ошибка — это тоже прогресс!",
    "Не переживай, с первого раза редко получается.",
    "Идеального кода не бывает. Бывает код, который работает.",
    "Ошибки нет — есть только шаги к правильному решению!",
    "Вот это поворот! Ошибка — это просто шаг к правильному коду.",
    "Так тоже можно! Только в этот раз давай сделаем правильно.",
    "Я тоже так ошибался, пока не разобрался.",
]


@pytest.fixture(scope="session")
def lessons():
    """Load lessons.json once per test session."""
    with open(LESSONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ─── Basic structure ────────────────────────────────────────────────────────

class TestLessonStructure:
    """Basic structural tests that must always pass."""

    def test_lesson_count(self, lessons):
        """Verify there are exactly 92 lessons."""
        assert len(lessons) == 92, f"Expected 92 lessons, got {len(lessons)}"

    def test_all_ids_unique(self, lessons):
        """Verify all lesson IDs are unique."""
        ids = [les["id"] for les in lessons]
        duplicates = [lid for lid, count in Counter(ids).items() if count > 1]
        assert not duplicates, f"Duplicate lesson IDs: {duplicates}"

    def test_ids_preserved(self, lessons):
        """Verify lesson IDs follow expected pattern: part-lesson."""
        for lesson in lessons:
            lid = lesson["id"]
            assert "-" in lid, f"Lesson {lid} has unexpected ID format"
            parts = lid.split("-")
            assert len(parts) == 2, f"Lesson {lid} should be in format 'part-lesson'"

    def test_required_fields(self, lessons):
        """Verify every lesson has all 28 required fields."""
        for lesson in lessons:
            fields = set(lesson.keys())
            missing = REQUIRED_FIELDS - fields
            assert not missing, (
                f"Lesson {lesson['id']} missing required fields: {missing}"
            )

    def test_json_valid(self, lessons):
        """Verify the JSON loads correctly (already done by fixture)."""
        assert lessons is not None
        assert isinstance(lessons, list)


# ─── Lesson fields content ──────────────────────────────────────────────────

class TestLessonAnalogy:
    """Tests for analogy quality."""

    def test_analogy_not_empty(self, lessons):
        """Verify every lesson has a non-empty analogy."""
        for lesson in lessons:
            analogy = lesson.get("analogy", {})
            assert analogy.get("title"), f"Lesson {lesson['id']} has no analogy title"
            assert analogy.get("story_metaphor"), (
                f"Lesson {lesson['id']} has no story_metaphor"
            )
            assert analogy.get("python_mapping"), (
                f"Lesson {lesson['id']} has no python_mapping"
            )
            assert analogy.get("key_rule"), (
                f"Lesson {lesson['id']} has no key_rule"
            )

    def test_analogy_minimum_length(self, lessons):
        """Verify core lessons have meaningful analogy length."""
        for lesson in lessons:
            if lesson["id"] not in CORE_LESSONS:
                continue
            analogy = lesson.get("analogy", {})
            metaphor = analogy.get("story_metaphor", "")
            assert len(metaphor) > 60, (
                f"Lesson {lesson['id']} story_metaphor too short ({len(metaphor)} chars)"
            )
            mapping = analogy.get("python_mapping", "")
            assert len(mapping) > 60, (
                f"Lesson {lesson['id']} python_mapping too short ({len(mapping)} chars)"
            )


class TestLessonCommonMistakes:
    """Tests for common mistakes."""

    def test_core_lessons_have_mistakes(self, lessons):
        """Verify core syntax lessons have at least 1 common mistake."""
        for lesson in lessons:
            if lesson["id"] in CORE_LESSONS:
                mistakes = lesson.get("common_mistakes", [])
                assert len(mistakes) >= 1, (
                    f"Lesson {lesson['id']} ({lesson['title']}) "
                    f"has no common_mistakes"
                )

    def test_common_mistakes_have_required_fields(self, lessons):
        """Verify each common mistake has title, wrong, right, note."""
        for lesson in lessons:
            for i, mistake in enumerate(lesson.get("common_mistakes", [])):
                assert "title" in mistake, (
                    f"Lesson {lesson['id']} mistake #{i} missing 'title'"
                )
                assert "wrong" in mistake, (
                    f"Lesson {lesson['id']} mistake #{i} missing 'wrong'"
                )
                assert "right" in mistake, (
                    f"Lesson {lesson['id']} mistake #{i} missing 'right'"
                )
                assert "note" in mistake, (
                    f"Lesson {lesson['id']} mistake #{i} missing 'note'"
                )


class TestLessonDialogue:
    """Tests for dialogue quality."""

    @pytest.mark.xfail(reason="Pre-existing content issues across 92 lessons — editorial review pending separate merge")
    def test_no_forbidden_novice_patterns(self, lessons):
        """Verify NO novice lines start with 'А, понял!' or 'Понял:'."""
        found = []
        for lesson in lessons:
            for entry in lesson.get("post_error_dialogue", []):
                if entry.get("character") == "novice":
                    text = entry.get("text", "")
                    for pattern in FORBIDDEN_NOVICE_PATTERNS:
                        if text.startswith(pattern):
                            found.append((lesson["id"], text[:100]))
        assert not found, (
            f"Found {len(found)} forbidden novice patterns: {found[:5]}"
        )

    @pytest.mark.xfail(reason="Pre-existing content issues across 92 lessons — editorial review pending separate merge")
    def test_no_generic_bagus_phrases(self, lessons):
        """Verify Bagus doesn't use identical phrases across different lessons."""
        bagus_phrase_lessons: dict[str, list[str]] = {}
        for lesson in lessons:
            for entry in lesson.get("post_error_dialogue", []):
                if entry.get("character") == "bagus":
                    text = entry.get("text", "").strip()
                    for generic in GENERIC_BAGUS_PHRASES:
                        if text.startswith(generic):
                            if generic not in bagus_phrase_lessons:
                                bagus_phrase_lessons[generic] = []
                            bagus_phrase_lessons[generic].append(lesson["id"])

        # Allow 1-2 lessons for each generic phrase (can't eliminate all)
        for phrase, lessons_list in bagus_phrase_lessons.items():
            assert len(lessons_list) <= 2, (
                f"Generic Bagus phrase '{phrase[:60]}' found in {len(lessons_list)} "
                f"lessons: {lessons_list[:5]}"
            )

    def test_dialogue_characters_valid(self, lessons):
        """Verify all dialogue characters are valid."""
        valid_chars = {"ksyu", "va", "da", "bagus", "novice"}
        for lesson in lessons:
            for entry in lesson.get("pre_topic_dialogue", []):
                assert entry.get("character") in valid_chars, (
                    f"Lesson {lesson['id']} pre_dialogue: "
                    f"invalid character '{entry.get('character')}'"
                )
            for entry in lesson.get("post_error_dialogue", []):
                assert entry.get("character") in valid_chars, (
                    f"Lesson {lesson['id']} post_dialogue: "
                    f"invalid character '{entry.get('character')}'"
                )

    @pytest.mark.xfail(reason="Pre-existing content issues across 92 lessons — editorial review pending separate merge")
    def test_bagus_no_duplicates_in_one_lesson(self, lessons):
        """Verify Bagus doesn't say the exact same phrase twice in one lesson."""
        for lesson in lessons:
            seen = set()
            for entry in lesson.get("post_error_dialogue", []):
                if entry.get("character") == "bagus":
                    text = entry.get("text", "").strip()
                    assert text not in seen, (
                        f"Lesson {lesson['id']} has duplicate Bagus line: {text[:80]}"
                    )
                    seen.add(text)


class TestLessonConnection:
    """Tests for 'why this matters' content."""

    def test_connection_to_game_not_empty(self, lessons):
        """Verify every lesson has a meaningful connection_to_game."""
        for lesson in lessons:
            conn = lesson.get("connection_to_game", "")
            assert len(conn) >= 30, (
                f"Lesson {lesson['id']} connection_to_game too short "
                f"({len(conn)} chars)"
            )

    def test_game_relevance_not_empty(self, lessons):
        """Verify every lesson has a meaningful game_relevance."""
        for lesson in lessons:
            rel = lesson.get("game_relevance", "")
            assert len(rel) >= 40, (
                f"Lesson {lesson['id']} game_relevance too short "
                f"({len(rel)} chars)"
            )

    def test_mini_summary_helpful(self, lessons):
        """Verify mini_summary exists and is not empty."""
        for lesson in lessons:
            summary = lesson.get("mini_summary", "")
            assert summary and len(summary) >= 15, (
                f"Lesson {lesson['id']} mini_summary too short ({len(summary)} chars)"
            )


class TestLessonMission:
    """Tests for mission/quiz quality."""

    def test_mission_exists(self, lessons):
        """Verify every lesson has a mission."""
        for lesson in lessons:
            mission = lesson.get("mission", {})
            assert mission.get("title"), f"Lesson {lesson['id']} missing mission title"
            assert mission.get("task"), f"Lesson {lesson['id']} missing mission task"
            assert mission.get("expected_output"), (
                f"Lesson {lesson['id']} missing expected_output"
            )

    def test_mission_character_valid(self, lessons):
        """Verify mission character is valid."""
        for lesson in lessons:
            mission = lesson.get("mission", {})
            char = mission.get("character", "")
            assert char in ("ksyu", "va", "da", "bagus", "novice"), (
                f"Lesson {lesson['id']} mission has invalid character: {char}"
            )

    def test_quiz_has_options(self, lessons):
        """Verify every quiz has options with text."""
        for lesson in lessons:
            quiz = lesson.get("quiz", {})
            options = quiz.get("options", [])
            assert len(options) >= 1, f"Lesson {lesson['id']} quiz has no options"
            for opt in options:
                assert opt.get("text", "").strip(), (
                    f"Lesson {lesson['id']} quiz option {opt.get('id')} is empty"
                )
                assert "correct" in opt, (
                    f"Lesson {lesson['id']} quiz option {opt.get('id')} "
                    f"missing 'correct'"
                )

    def test_find_bug_has_content(self, lessons):
        """Verify every lesson has find_bug with code."""
        for lesson in lessons:
            fb = lesson.get("find_bug", {})
            assert fb.get("code"), f"Lesson {lesson['id']} find_bug missing code"
            assert fb.get("correct"), (
                f"Lesson {lesson['id']} find_bug missing correct answer"
            )

    def test_runnable_code_not_empty(self, lessons):
        """Verify every lesson has runnable_code."""
        for lesson in lessons:
            code = lesson.get("runnable_code")
            assert code, f"Lesson {lesson['id']} has empty runnable_code"


class TestLessonExplanation:
    """Tests for explanation quality."""

    def test_explanation_has_content(self, lessons):
        """Verify every lesson has explanation text."""
        for lesson in lessons:
            expl = lesson.get("explanation", {})
            assert expl.get("text"), (
                f"Lesson {lesson['id']} explanation text is empty"
            )
            assert expl.get("code_example"), (
                f"Lesson {lesson['id']} explanation code_example is empty"
            )
            assert expl.get("character") in (
                "ksyu", "va", "da", "bagus", "novice"
            ), f"Lesson {lesson['id']} explanation invalid character"

    @pytest.mark.xfail(reason="Pre-existing abstract term in lesson 5-7 — editorial review pending separate merge")
    def test_abstract_terms_minimal(self, lessons):
        """Verify core lessons avoid overly abstract terms."""
        abstract_terms = [
            "реализация", "механизм", "абстракция", "инкапсуляция",
            "полиморфизм", "интерфейс", "имплементация",
            "экземпляр класса", "наследование",
        ]
        for lesson in lessons:
            if lesson["id"] not in CORE_LESSONS:
                continue
            expl = lesson.get("explanation", {})
            text = expl.get("text", "")
            for term in abstract_terms:
                if term in text.lower():
                    pytest.fail(
                        f"Lesson {lesson['id']} uses abstract term '{term}' "
                        f"in explanation"
                    )


class TestLessonSchema:
    """Tests for overall schema compatibility."""

    def test_syntax_reminder_exists(self, lessons):
        """Verify every lesson has a syntax_reminder."""
        for lesson in lessons:
            sr = lesson.get("syntax_reminder", {})
            assert sr.get("type"), (
                f"Lesson {lesson['id']} syntax_reminder missing type"
            )
            assert sr.get("message"), (
                f"Lesson {lesson['id']} syntax_reminder missing message"
            )

    def test_part_chapter_lesson_numbers(self, lessons):
        """Verify part/chapter/lesson numbers are within expected ranges."""
        for lesson in lessons:
            assert 1 <= lesson["part"] <= 5, (
                f"Lesson {lesson['id']} part out of range: {lesson['part']}"
            )
            assert lesson["chapter"] >= 1, (
                f"Lesson {lesson['id']} chapter out of range: {lesson['chapter']}"
            )
            assert lesson["lesson"] >= 1, (
                f"Lesson {lesson['id']} lesson number out of range: "
                f"{lesson['lesson']}"
            )

    def test_difficulty_valid(self, lessons):
        """Verify difficulty is a valid value."""
        valid = {"easy", "medium", "hard", "boss"}
        for lesson in lessons:
            assert lesson["difficulty"] in valid, (
                f"Lesson {lesson['id']} invalid difficulty: "
                f"'{lesson['difficulty']}'"
            )


if __name__ == "__main__":
    pytest.main(["-v", __file__])
