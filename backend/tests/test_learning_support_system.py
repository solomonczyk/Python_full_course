"""Tests for the Foundation / Glossary / Recap / Quest learning support system.

Tests cover:
- Glossary JSON loads and has required fields
- Recaps exist for all parts
- Quests exist for all parts
- Foundation blocks exist for first 10 lessons
- Lesson 1-1 has specific foundation terms
- No duplicate IDs
- Lesson count remains 92
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

DATA_DIR = Path(__file__).resolve().parent.parent / "app" / "data"


def _load_json(name: str) -> list | dict:
    path = DATA_DIR / name
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class TestGlossaryData:
    """Tests for glossary.json completeness and validity."""

    def test_glossary_exists(self):
        data = _load_json("glossary.json")
        assert isinstance(data, list), "glossary.json must be a list"
        assert len(data) >= 35, f"Expected >= 35 terms, got {len(data)}"

    def test_glossary_required_fields(self):
        data = _load_json("glossary.json")
        required = {"id", "term", "python_name", "category", "simple_definition",
                     "analogy", "code_example", "common_mistake", "mistake_explanation",
                     "related_lessons", "beginner_level"}
        for term in data:
            missing = required - set(term.keys())
            assert not missing, f"Term '{term.get('id', '?')}' missing fields: {missing}"

    def test_glossary_no_duplicate_ids(self):
        data = _load_json("glossary.json")
        ids = [t["id"] for t in data]
        duplicates = {i for i in ids if ids.count(i) > 1}
        assert not duplicates, f"Duplicate glossary IDs: {duplicates}"

    def test_glossary_has_print_term(self):
        data = _load_json("glossary.json")
        ids = [t["id"] for t in data]
        assert "print" in ids, "glossary must have 'print' term"

    def test_glossary_has_quotes_term(self):
        data = _load_json("glossary.json")
        ids = [t["id"] for t in data]
        assert "quotes" in ids, "glossary must have 'quotes' term"

    def test_glossary_has_variable_term(self):
        data = _load_json("glossary.json")
        ids = [t["id"] for t in data]
        assert "variable" in ids, "glossary must have 'variable' term"

    def test_glossary_has_if_term(self):
        data = _load_json("glossary.json")
        ids = [t["id"] for t in data]
        assert "if_statement" in ids, "glossary must have 'if_statement' term"


class TestRecapsData:
    """Tests for recaps.json completeness."""

    def test_recaps_exists(self):
        data = _load_json("recaps.json")
        assert isinstance(data, list), "recaps.json must be a list"
        assert len(data) >= 5, f"Expected >= 5 recaps (1 per part), got {len(data)}"

    def test_recaps_required_fields(self):
        data = _load_json("recaps.json")
        required = {"id", "part", "title", "story_summary", "learned_terms",
                     "hero_skills", "key_rules", "mini_check"}
        for recap in data:
            missing = required - set(recap.keys())
            assert not missing, f"Recap '{recap.get('id', '?')}' missing fields: {missing}"

    def test_recaps_cover_all_parts(self):
        data = _load_json("recaps.json")
        parts = sorted(set(r["part"] for r in data))
        expected = list(range(1, 6))
        assert parts == expected, f"Expected recaps for parts {expected}, got {parts}"

    def test_recaps_no_duplicate_ids(self):
        data = _load_json("recaps.json")
        ids = [r["id"] for r in data]
        assert len(ids) == len(set(ids)), "Duplicate recap IDs found"


class TestQuestsData:
    """Tests for chapter_quests.json completeness."""

    def test_quests_exists(self):
        data = _load_json("chapter_quests.json")
        assert isinstance(data, list), "chapter_quests.json must be a list"
        assert len(data) >= 5, f"Expected >= 5 quests (1 per part), got {len(data)}"

    def test_quests_required_fields(self):
        data = _load_json("chapter_quests.json")
        required = {"id", "part", "title", "story", "required_lessons",
                     "required_constructs", "task", "starter_code",
                     "example_solution", "test_cases", "success_criteria", "hints"}
        for quest in data:
            missing = required - set(quest.keys())
            assert not missing, f"Quest '{quest.get('id', '?')}' missing fields: {missing}"

    def test_quests_cover_all_parts(self):
        data = _load_json("chapter_quests.json")
        parts = sorted(set(q["part"] for q in data))
        expected = list(range(1, 6))
        assert parts == expected, f"Expected quests for parts {expected}, got {parts}"

    def test_quests_have_multiple_constructs(self):
        data = _load_json("chapter_quests.json")
        for quest in data:
            assert len(quest["required_constructs"]) >= 3, \
                f"Quest '{quest['id']}' has < 3 required constructs (single-topic)"

    def test_quests_no_duplicate_ids(self):
        data = _load_json("chapter_quests.json")
        ids = [q["id"] for q in data]
        assert len(ids) == len(set(ids)), "Duplicate quest IDs found"

    def test_quests_have_test_cases(self):
        data = _load_json("chapter_quests.json")
        for quest in data:
            assert len(quest["test_cases"]) >= 1, \
                f"Quest '{quest['id']}' has no test cases"

    def test_quests_have_hints(self):
        data = _load_json("chapter_quests.json")
        for quest in data:
            assert len(quest["hints"]) >= 1, \
                f"Quest '{quest['id']}' has no hints"


class TestFoundationBlocks:
    """Tests for foundation blocks in lessons.json."""

    def test_lesson_count_remains_92(self):
        data = _load_json("lessons.json")
        assert len(data) == 92, f"Expected 92 lessons, got {len(data)}"

    def test_lesson_1_1_has_foundation(self):
        data = _load_json("lessons.json")
        lesson = next(l for l in data if l["id"] == "1-1")
        assert "foundation" in lesson, \
            f"Lesson '1-1' missing foundation block"
        assert isinstance(lesson["foundation"], dict), \
            "Lesson '1-1' foundation is not a dict"

    def test_lesson_1_1_has_terms(self):
        data = _load_json("lessons.json")
        lesson = next(l for l in data if l["id"] == "1-1")
        assert "terms" in lesson["foundation"], \
            "Lesson '1-1' foundation missing 'terms'"
        assert len(lesson["foundation"]["terms"]) >= 10, \
            f"Lesson '1-1' foundation has {len(lesson['foundation']['terms'])} terms, expected at least 10"

    def test_lesson_1_1_foundation_has_print(self):
        data = _load_json("lessons.json")
        lesson = next(l for l in data if l["id"] == "1-1")
        foundation = lesson.get("foundation", {})
        terms = foundation.get("terms", [])
        term_ids = [t.get("term_id") for t in terms]
        assert "print" in term_ids, \
            f"Lesson 1-1 foundation must include 'print' term, got: {term_ids}"
        assert "quotes" in term_ids, \
            "Lesson 1-1 foundation must include 'quotes' term"
        assert "error" in term_ids or "syntax_error" in term_ids, \
            "Lesson 1-1 foundation must include error-related term"


class TestBagusFix:
    """Tests that Bagus duplicate lines are fixed."""

    def test_no_consecutive_bagus_lines_in_1_1(self):
        data = _load_json("lessons.json")
        lesson = next(l for l in data if l["id"] == "1-1")
        dialogue = lesson.get("post_error_dialogue", [])
        bagus_indices = [i for i, line in enumerate(dialogue)
                        if line.get("character") == "bagus"]
        for i in bagus_indices:
            adjacent = [j for j in bagus_indices if abs(j - i) == 1]
            assert not adjacent, \
                f"Lesson 1-1 has consecutive Bagus lines at indices {i} and {adjacent[0]}"


class TestDataIntegrity:
    """Cross-data integrity checks."""

    def test_glossary_ids_match_lesson_refs(self):
        """Check that glossary term IDs referenced in lessons exist."""
        glossary = _load_json("glossary.json")
        glossary_ids = {t["id"] for t in glossary}
        lessons = _load_json("lessons.json")
        for lesson in lessons:
            foundation = lesson.get("foundation", {})
            g_terms = foundation.get("glossary_terms", [])
            for term_id in g_terms:
                assert term_id in glossary_ids, \
                    f"Lesson '{lesson['id']}' references unknown glossary term '{term_id}'"

    def test_related_lessons_in_glossary_exist(self):
        glossary = _load_json("glossary.json")
        lessons = _load_json("lessons.json")
        lesson_ids = {l["id"] for l in lessons}
        for term in glossary:
            for ref in term.get("related_lessons", []):
                assert ref in lesson_ids, \
                    f"Glossary term '{term['id']}' references unknown lesson '{ref}'"
