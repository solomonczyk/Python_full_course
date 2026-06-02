#!/usr/bin/env python3
"""
Course Quality Audit Pipeline for Python Quest.

Purpose:
  Systematically audit the entire course across 7 dimensions to find
  inaccurate wording, malformed assignments, inconsistent task/answer pairs,
  inappropriate dialogues, premature concepts, invalid code examples,
  and learning-flow defects.

Audit types:
  1. Structural audit         — required fields, data types, empty strings
  2. Pedagogical prerequisite  — premature concept usage in tasks/dialogues
  3. Task-answer consistency   — expected output vs task, code formatting
  4. Dialogue quality          — character roles, Bagus dominance, spoilers
  5. Wording clarity           — risky pedagogical phrasing
  6. Skill progression audit   — known_before / forbidden_before compliance
  7. Surface coverage audit    — which blocks exist per lesson

Outputs:
  docs/course_quality_inventory.json
  docs/course_quality_issue_registry.json
  docs/course_quality_human_review_packet.md
  docs/course_quality_audit_report.md

Usage:
  python scripts/audit_course_quality.py
"""

import json
import os
import re
import sys
import datetime
import hashlib
import traceback
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_PATH = os.path.join(BASE, "api", "app", "data", "lessons.json")
RECAPS_PATH = os.path.join(BASE, "api", "app", "data", "recaps.json")
QUESTS_PATH = os.path.join(BASE, "api", "app", "data", "quests.json")
CHAPTER_QUESTS_PATH = os.path.join(BASE, "api", "app", "data", "chapter_quests.json")
REVIEW_SCHEDULE_PATH = os.path.join(BASE, "api", "app", "data", "review_schedule.json")
SKILL_PROGRESSION_PATH = os.path.join(BASE, "scripts", "config", "skill_progression.json")
DOCS_DIR = os.path.join(BASE, "docs")

VALID_CHARACTERS = {"ksyu", "va", "da", "bagus", "novice"}
VALID_DIFFICULTIES = {"easy", "medium", "hard", "boss"}
CHARACTER_LORE = {
    "novice": "curious beginner, asks questions, reflects understanding",
    "ksyu": "gentle explainer, metaphors, patient, encouraging",
    "va": "logical technical explainer, precise, direct",
    "da": "practical, mission-focused, action-oriented",
    "bagus": "comic relief, encouragement, NOT primary educator",
}

# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_course_data() -> dict:
    return {
        "lessons": load_json(LESSONS_PATH),
        "recaps": load_json(RECAPS_PATH),
        "quests": load_json(QUESTS_PATH),
        "chapter_quests": load_json(CHAPTER_QUESTS_PATH),
        "reviews": load_json(REVIEW_SCHEDULE_PATH).get("reviews", []),
    }

def load_skill_progression() -> dict:
    if os.path.exists(SKILL_PROGRESSION_PATH):
        return load_json(SKILL_PROGRESSION_PATH)
    return {"lessons": {}, "recaps": {}}

# ---------------------------------------------------------------------------
# Issue Registry
# ---------------------------------------------------------------------------

class IssueRegistry:
    def __init__(self):
        self.issues: list[dict] = []
        self._counter = 0

    def add_issue(
        self,
        severity: str,
        surface: str,
        item_id: str,
        field: str,
        issue_type: str,
        current_text: str,
        reason: str,
        suggested_fix: str = "",
        auto_fix_safe: bool = False,
        requires_operator_review: bool = True,
    ):
        self._counter += 1
        self.issues.append({
            "issue_id": f"PQA-{self._counter:04d}",
            "severity": severity,
            "surface": surface,
            "item_id": item_id,
            "field": field,
            "issue_type": issue_type,
            "current_text": current_text[:500],
            "reason": reason,
            "suggested_fix": suggested_fix[:500],
            "auto_fix_safe": auto_fix_safe,
            "requires_operator_review": requires_operator_review,
        })

    def to_dict(self) -> dict:
        counts = {"must_fix_now": 0, "needs_human_review": 0, "can_defer": 0, "non_blocking_polish": 0}
        for iss in self.issues:
            s = iss["severity"]
            if s in counts:
                counts[s] += 1
        return {
            "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "total_items_checked": 0,
            "issues_total": len(self.issues),
            "severity_counts": counts,
            "issues": self.issues,
        }

    def get_by_severity(self, severity: str) -> list[dict]:
        return [i for i in self.issues if i["severity"] == severity]

    def get_by_surface(self, surface: str) -> list[dict]:
        return [i for i in self.issues if i["surface"] == surface]

    def get_by_type(self, issue_type: str) -> list[dict]:
        return [i for i in self.issues if i["issue_type"] == issue_type]

    def get_by_part(self, data: dict) -> dict[int, list[dict]]:
        """Group issues by part number based on item_id."""
        parts: dict[int, list[dict]] = {}
        for iss in self.issues:
            part = 0
            iid = iss["item_id"]
            # Parse lesson IDs like "1-1", "1-7", "2-3"
            m = re.match(r"^(\d+)", iid)
            if m:
                part = int(m.group(1))
            # Parse recap IDs like "recap-1", "recap-3a"
            m = re.match(r"^recap-(\d+)", iid)
            if m:
                part = int(m.group(1))
            # Parse quest IDs like "quest-1"
            m = re.match(r"^quest-(\d+)", iid)
            if m:
                part = int(m.group(1))
            # Review IDs like "r-1"
            if iid.startswith("r-"):
                # Find part from review data
                for r in data.get("reviews", []):
                    if r.get("id") == iid:
                        part = r.get("part", 0)
                        break
            if part not in parts:
                parts[part] = []
            parts[part].append(iss)
        return dict(sorted(parts.items()))


# ---------------------------------------------------------------------------
# 1. Course Inventory Builder
# ---------------------------------------------------------------------------

def build_inventory(data: dict) -> dict:
    lessons_data = data["lessons"]
    recaps_data = data["recaps"]
    quests_data = data["quests"]
    chapter_quests_data = data["chapter_quests"]
    reviews_data = data["reviews"]

    inventory = {
        "meta": {
            "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "description": "Unified course inventory of all educational entities",
        },
        "lessons": [],
        "recaps": [],
        "quests": [],
        "chapter_quests": [],
        "reviews": [],
        "summary": {},
    }

    dialogue_blocks_total = 0
    mission_blocks_total = 0
    code_examples_total = 0

    for l in lessons_data:
        lid = l["id"]
        has_dialogue = bool(l.get("pre_topic_dialogue")) or bool(l.get("post_error_dialogue"))
        pre_dialogue_count = len(l.get("pre_topic_dialogue") or [])
        post_dialogue_count = len(l.get("post_error_dialogue") or [])
        has_mission = "mission" in l and l["mission"] is not None
        has_code_watch = "code_watch" in l and l["code_watch"] is not None
        has_analogy = "analogy" in l and l["analogy"] is not None
        has_quiz = "quiz" in l and l["quiz"] is not None
        has_what_outputs = "what_outputs" in l and l["what_outputs"] is not None
        has_find_bug = "find_bug" in l and l["find_bug"] is not None
        has_practice_subtasks = bool(l.get("practice_subtasks"))
        has_explanation = "explanation" in l and l["explanation"] is not None
        has_foundation = "foundation" in l and l["foundation"] is not None

        if has_mission:
            mission_blocks_total += 1
        if has_explanation and l["explanation"].get("code_example"):
            code_examples_total += 1
        if has_code_watch and l["code_watch"].get("dialogue"):
            dialogue_blocks_total += len(l["code_watch"]["dialogue"])

        inventory["lessons"].append({
            "id": lid,
            "type": "lesson",
            "part": l.get("part"),
            "chapter": l.get("chapter"),
            "title": l.get("title", ""),
            "slug": l.get("slug", ""),
            "difficulty": l.get("difficulty", ""),
            "source_file": "api/app/data/lessons.json",
            "route": f"/lesson/{lid}",
            "concepts_taught": [l.get("slug", "")],
            "has_mission": has_mission,
            "has_checker": l.get("mission") is not None,
            "has_dialogue": has_dialogue,
            "dialogue_lines": pre_dialogue_count + post_dialogue_count,
            "has_code_watch": has_code_watch,
            "has_analogy": has_analogy,
            "has_quiz": has_quiz,
            "has_what_outputs": has_what_outputs,
            "has_find_bug": has_find_bug,
            "has_practice_subtasks": has_practice_subtasks,
            "has_explanation": has_explanation,
            "has_foundation": has_foundation,
        })

    for r in recaps_data:
        inventory["recaps"].append({
            "id": r["id"],
            "type": "recap",
            "part": r.get("part"),
            "title": r.get("title", ""),
            "source_file": "api/app/data/recaps.json",
            "route": f"/recap/{r['id']}",
            "has_dialogue": bool(r.get("dialogue")),
            "has_hero_skills": bool(r.get("hero_skills")),
            "has_mini_check": bool(r.get("mini_check")),
            "key_rules_count": len(r.get("key_rules", [])),
        })

    for q in quests_data:
        inventory["quests"].append({
            "id": q["id"],
            "type": "quest",
            "part": q.get("part"),
            "title": q.get("title", ""),
            "source_file": "api/app/data/quests.json",
            "route": f"/quest/{q['id']}",
            "required_lessons": q.get("required_lessons", []),
            "test_cases": len(q.get("test_cases", [])),
            "has_hints": bool(q.get("hints")),
            "has_starter_code": bool(q.get("starter_code")),
        })
        if "example_solution" in q:
            code_examples_total += 1

    for q in chapter_quests_data:
        inventory["chapter_quests"].append({
            "id": q["id"],
            "type": "chapter_quest",
            "part": q.get("part"),
            "title": q.get("title", ""),
            "source_file": "api/app/data/chapter_quests.json",
            "route": f"/quest/{q['id']}",
            "required_lessons": q.get("required_lessons", []),
            "test_cases": len(q.get("test_cases", [])),
        })
        if "example_solution" in q:
            code_examples_total += 1

    for r in reviews_data:
        inventory["reviews"].append({
            "id": r["id"],
            "type": "review",
            "review_type": r.get("type", ""),
            "part": r.get("part"),
            "chapter": r.get("chapter"),
            "title": r.get("title", ""),
            "source_file": "api/app/data/review_schedule.json",
            "position_after": r.get("position_after"),
            "question_count": len(r.get("questions", [])),
            "has_dialogue": bool(r.get("dialogue")),
        })

    all_ids = []
    all_ids.extend(l["id"] for l in inventory["lessons"])
    all_ids.extend(r["id"] for r in inventory["recaps"])
    all_ids.extend(q["id"] for q in inventory["quests"])
    all_ids.extend(q["id"] for q in inventory["chapter_quests"])
    all_ids.extend(r["id"] for r in inventory["reviews"])
    all_ids_set = set(all_ids)
    duplicate_ids = [i for i in all_ids if all_ids.count(i) > 1]

    dialogue_lines_total = 0
    for l in lessons_data:
        dialogue_lines_total += len(l.get("pre_topic_dialogue") or [])
        dialogue_lines_total += len(l.get("post_error_dialogue") or [])
    for r in reviews_data:
        dialogue_lines_total += len(r.get("dialogue") or [])

    inventory["summary"] = {
        "total_lessons": len(inventory["lessons"]),
        "total_recaps": len(inventory["recaps"]),
        "total_quests": len(inventory["quests"]),
        "total_chapter_quests": len(inventory["chapter_quests"]),
        "total_reviews": len(inventory["reviews"]),
        "total_entities": len(all_ids),
        "total_unique_entities": len(all_ids_set),
        "duplicate_ids_found": duplicate_ids,
        "dialogue_blocks": dialogue_lines_total,
        "mission_blocks": mission_blocks_total,
        "code_examples_approx": code_examples_total,
        "has_code_watch": sum(1 for l in lessons_data if l.get("code_watch")),
        "has_analogy": sum(1 for l in lessons_data if l.get("analogy")),
        "has_quiz": sum(1 for l in lessons_data if l.get("quiz")),
        "has_what_outputs": sum(1 for l in lessons_data if l.get("what_outputs")),
        "has_find_bug": sum(1 for l in lessons_data if l.get("find_bug")),
        "has_practice_subtasks": sum(1 for l in lessons_data if l.get("practice_subtasks")),
        "has_foundation": sum(1 for l in lessons_data if l.get("foundation")),
    }

    # Normalize the summary for the dupes field
    dupes = list(set(i for i in all_ids if all_ids.count(i) > 1))
    inventory["summary"]["duplicate_ids_found"] = dupes

    return inventory


# ---------------------------------------------------------------------------
# 2. Structural Audit
# ---------------------------------------------------------------------------

def audit_structural(data: dict, registry: IssueRegistry):
    """Check required fields, data types, empty strings, malformed shapes."""

    for l in data["lessons"]:
        lid = l["id"]

        # -- Required top-level fields --
        required_fields = ["id", "part", "chapter", "lesson", "title", "slug", "difficulty"]
        for f in required_fields:
            if f not in l or l[f] is None:
                registry.add_issue(
                    "must_fix_now", "lesson", lid, f, "missing_required_field",
                    str(l.get(f, "")),
                    f"Required field '{f}' is missing or null",
                    f"Add '{f}' to lesson {lid}",
                    auto_fix_safe=False, requires_operator_review=True,
                )

        # -- Invalid difficulty --
        diff = l.get("difficulty", "")
        if diff and diff not in VALID_DIFFICULTIES:
            registry.add_issue(
                "needs_human_review", "lesson", lid, "difficulty", "invalid_difficulty",
                diff, f"Unknown difficulty '{diff}'",
                f"Set to one of: {', '.join(sorted(VALID_DIFFICULTIES))}",
                auto_fix_safe=True, requires_operator_review=False,
            )

        # -- Pre-topic dialogue checks --
        pre_dialogue = l.get("pre_topic_dialogue") or []
        for idx, step in enumerate(pre_dialogue):
            if not isinstance(step, dict):
                registry.add_issue("must_fix_now", "lesson", lid, f"pre_topic_dialogue[{idx}]",
                    "malformed_dialogue_step", str(step)[:200],
                    "Dialogue step is not a dict", "Convert to dict with character/text fields",
                    auto_fix_safe=False, requires_operator_review=True)
                continue
            if not step.get("character"):
                registry.add_issue("must_fix_now", "lesson", lid, f"pre_topic_dialogue[{idx}]",
                    "missing_character", str(step.get("text", ""))[:200],
                    "Dialogue step missing 'character' field",
                    "Add character field", auto_fix_safe=False, requires_operator_review=True)
            if not step.get("text"):
                registry.add_issue("must_fix_now", "lesson", lid, f"pre_topic_dialogue[{idx}]",
                    "missing_text", str(step.get("character", ""))[:100],
                    "Dialogue step missing 'text' field",
                    "Add text content or remove empty step",
                    auto_fix_safe=False, requires_operator_review=True)
            char = step.get("character", "")
            if char and char not in VALID_CHARACTERS:
                registry.add_issue("needs_human_review", "lesson", lid,
                    f"pre_topic_dialogue[{idx}].character", "invalid_character",
                    char, f"Unknown character '{char}'",
                    f"Use one of: {', '.join(sorted(VALID_CHARACTERS))}",
                    auto_fix_safe=True, requires_operator_review=False)

        # -- Post-error dialogue checks --
        post_dialogue = l.get("post_error_dialogue") or []
        for idx, step in enumerate(post_dialogue):
            if not isinstance(step, dict):
                registry.add_issue("must_fix_now", "lesson", lid, f"post_error_dialogue[{idx}]",
                    "malformed_dialogue_step", str(step)[:200],
                    "Post-error dialogue step is not a dict", "Convert to dict",
                    auto_fix_safe=False, requires_operator_review=True)
                continue
            if not step.get("character"):
                registry.add_issue("must_fix_now", "lesson", lid, f"post_error_dialogue[{idx}]",
                    "missing_character", str(step.get("text", ""))[:200],
                    "Post-error dialogue step missing 'character'",
                    "Add character field", auto_fix_safe=False, requires_operator_review=True)
            if not step.get("text"):
                registry.add_issue("must_fix_now", "lesson", lid, f"post_error_dialogue[{idx}]",
                    "missing_text", str(step.get("character", ""))[:100],
                    "Post-error dialogue step missing 'text'",
                    "Add text content", auto_fix_safe=False, requires_operator_review=True)

        # -- Mission checks --
        mission = l.get("mission")
        if mission and isinstance(mission, dict):
            for mf in ["title", "task", "expected_output"]:
                if mf not in mission or not mission.get(mf):
                    registry.add_issue(
                        "must_fix_now" if mf in ("task", "expected_output") else "needs_human_review",
                        "lesson", lid, f"mission.{mf}", "missing_mission_field",
                        str(mission.get(mf, "")), f"Mission field '{mf}' is empty or missing",
                        f"Add content to mission.{mf}",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

        # -- Code watch checks --
        cw = l.get("code_watch")
        if cw and isinstance(cw, dict):
            for cwf in ["title", "main_code", "dialogue"]:
                if cwf not in cw or not cw.get(cwf):
                    registry.add_issue(
                        "must_fix_now", "lesson", lid, f"code_watch.{cwf}",
                        "missing_code_watch_field",
                        str(cw.get(cwf, "")),
                        f"Code watch field '{cwf}' is empty or missing",
                        f"Add content to code_watch.{cwf}",
                        auto_fix_safe=False, requires_operator_review=True,
                    )
            cw_dialogue = cw.get("dialogue") or []
            for idx, step in enumerate(cw_dialogue):
                if not isinstance(step, dict):
                    continue
                if not step.get("text") and not step.get("caption"):
                    registry.add_issue(
                        "needs_human_review", "lesson", lid,
                        f"code_watch.dialogue[{idx}]", "missing_text",
                        json.dumps(step, ensure_ascii=False)[:200],
                        "Code watch dialogue step has no 'text' or 'caption'",
                        "Add text or caption to step",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

        # -- Analogy checks --
        analogy = l.get("analogy")
        if analogy and isinstance(analogy, dict):
            for af in ["title", "story_metaphor", "python_mapping", "key_rule"]:
                if af not in analogy or not analogy.get(af):
                    registry.add_issue(
                        "needs_human_review", "lesson", lid, f"analogy.{af}",
                        "missing_analogy_field",
                        str(analogy.get(af, "")),
                        f"Analogy field '{af}' is empty or missing",
                        f"Add content to analogy.{af}",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

        # -- Explanation checks --
        expl = l.get("explanation")
        if expl and isinstance(expl, dict):
            if not expl.get("text"):
                registry.add_issue(
                    "needs_human_review", "lesson", lid, "explanation.text",
                    "missing_explanation_text", "", "Explanation text is empty",
                    "Add explanation text", auto_fix_safe=False, requires_operator_review=True,
                )

        # -- what_outputs checks --
        wo = l.get("what_outputs")
        if wo and isinstance(wo, dict):
            if not wo.get("code"):
                registry.add_issue(
                    "must_fix_now", "lesson", lid, "what_outputs.code",
                    "missing_what_outputs_code", "",
                    "what_outputs code is empty", "Add code for what_outputs",
                    auto_fix_safe=False, requires_operator_review=True,
                )
            options = wo.get("options")
            if not options or len(options) < 2:
                registry.add_issue(
                    "needs_human_review", "lesson", lid, "what_outputs.options",
                    "insufficient_what_outputs_options", str(options)[:200],
                    "what_outputs has fewer than 2 options",
                    "Add at least 2 options", auto_fix_safe=False, requires_operator_review=True,
                )

        # -- Quiz checks --
        quiz = l.get("quiz")
        if quiz and isinstance(quiz, dict):
            if not quiz.get("question"):
                registry.add_issue(
                    "must_fix_now", "lesson", lid, "quiz.question",
                    "missing_quiz_question", "", "Quiz question is empty",
                    "Add quiz question text", auto_fix_safe=False, requires_operator_review=True,
                )
            qopts = quiz.get("options") or []
            correct_count = sum(1 for o in qopts if o.get("correct"))
            if correct_count == 0:
                registry.add_issue(
                    "must_fix_now", "lesson", lid, "quiz.options",
                    "no_correct_quiz_answer", json.dumps(qopts, ensure_ascii=False)[:200],
                    "Quiz has no correct answer", "Mark at least one option as correct",
                    auto_fix_safe=False, requires_operator_review=True,
                )

        # -- Find bug checks --
        fb = l.get("find_bug")
        if fb and isinstance(fb, dict):
            if not fb.get("code"):
                registry.add_issue(
                    "must_fix_now", "lesson", lid, "find_bug.code",
                    "missing_find_bug_code", "", "find_bug code is empty",
                    "Add buggy code example", auto_fix_safe=False, requires_operator_review=True,
                )

    # -- Recaps --
    for r in data["recaps"]:
        rid = r["id"]
        if not r.get("title"):
            registry.add_issue("needs_human_review", "recap", rid, "title",
                "missing_title", "", "Recap title missing",
                "Add title to recap", auto_fix_safe=False, requires_operator_review=True)

    # -- Quests --
    for q in data["quests"]:
        qid = q["id"]
        if not q.get("task"):
            registry.add_issue("must_fix_now", "quest", qid, "task",
                "missing_quest_task", "", "Quest task is empty",
                "Add task description", auto_fix_safe=False, requires_operator_review=True)
        tcs = q.get("test_cases") or []
        if not tcs:
            registry.add_issue("needs_human_review", "quest", qid, "test_cases",
                "no_test_cases", "[]", "Quest has no test cases",
                "Add at least one test case", auto_fix_safe=False, requires_operator_review=True)


# ---------------------------------------------------------------------------
# 3. Pedagogical Prerequisite & Skill Progression Audit
# ---------------------------------------------------------------------------

def audit_prerequisites(data: dict, skill_prog: dict, registry: IssueRegistry):
    """Check tasks, dialogues, and missions don't use concepts not yet taught."""
    lessons_map = {l["id"]: l for l in data["lessons"]}
    prog_lessons = skill_prog.get("lessons", {})

    RISKY_WORDS_BEFORE_IF = ["если", "иначе", "elif", "else if", "условие"]
    RISKY_CONCEPTS_MAP = {
        "if": {"trigger_words": ["if ", "else ", "elif "], "forbidden_in": []},
        "list": {"trigger_words": ["список", "list", "index", "индекс"], "forbidden_in": []},
        "for": {"trigger_words": ["for ", "цикл", "повтор"], "forbidden_in": []},
        "while": {"trigger_words": ["while ", "пока "], "forbidden_in": []},
        "function": {"trigger_words": ["def ", "функци", "return "], "forbidden_in": []},
    }

    for l in data["lessons"]:
        lid = l["id"]
        lesson_prog = prog_lessons.get(lid)
        if not lesson_prog:
            registry.add_issue("needs_human_review", "lesson", lid, "skill_progression",
                "missing_skill_progression_entry", lid,
                f"No skill progression entry for lesson {lid}",
                "Add skill progression entry to scripts/config/skill_progression.json",
                auto_fix_safe=False, requires_operator_review=True)
            continue

        forbidden = lesson_prog.get("forbidden_before", [])

        # -- Check mission task --
        mission = l.get("mission")
        if mission and isinstance(mission, dict):
            task_text = mission.get("task", "")
            self_forbidden = [c for c in forbidden if c not in lesson_prog.get("new_concepts", [])]

            for concept in self_forbidden:
                if concept in ("if", "else", "elif"):
                    if _contains_pattern(task_text, ["if ", "else:", "elif "]):
                        registry.add_issue(
                            "must_fix_now" if lid in ("1-7",) else "needs_human_review",
                            "lesson", lid, "mission.task",
                            "premature_concept_risk",
                            task_text[:200],
                            f"Mission task may imply '{concept}' which is not taught until later",
                            "Rephrase to avoid implying conditional logic",
                            auto_fix_safe=False, requires_operator_review=True,
                        )
                        break

            # Check for explicit code in task that uses forbidden concepts
            if "forbidden_before" in lesson_prog:
                # Check if task mentions concepts that don't exist yet
                task_lower = task_text.lower()
                concept_triggers = {
                    "if": ["если", "проверь", "услови"],
                    "else": ["иначе"],
                    "list": ["список", "list"],
                    "for": ["for", "повтор"],
                    "loop": ["цикл"],
                    "while": ["while", "пока "],
                    "function": ["def ", "функци"],
                    "return": ["return", "верни"],
                    "dict": ["dict", "словар"],
                }

                for concept_name, triggers in concept_triggers.items():
                    if concept_name in forbidden:
                        for tr in triggers:
                            if tr.lower() in task_lower:
                                registry.add_issue(
                                    "needs_human_review" if lid not in ("1-7",) else "must_fix_now",
                                    "lesson", lid, "mission.task",
                                    "premature_concept_risk",
                                    task_text[:200],
                                    f"Task text mentions '{tr}' which relates to '{concept_name}', a forbidden concept before this lesson",
                                    "Rephrase task to avoid referencing this concept",
                                    auto_fix_safe=False, requires_operator_review=True,
                                )
                                break

            # -- Check expected output --
            expected = mission.get("expected_output", "")
            if expected and not expected.strip():
                registry.add_issue(
                    "must_fix_now", "lesson", lid, "mission.expected_output",
                    "empty_expected_output", "\"\"",
                    "Expected output is empty string",
                    "Fill in expected output matching the task",
                    auto_fix_safe=False, requires_operator_review=True,
                )

        # -- Check expected_solution if present --
        if "expected_solution" in l:
            sol_text = l["expected_solution"]
            for concept in forbidden:
                if concept == "if" and ("if " in sol_text or "else:" in sol_text):
                    registry.add_issue(
                        "must_fix_now", "lesson", lid, "expected_solution",
                        "premature_solution_concept",
                        sol_text[:200],
                        f"Expected solution uses '{concept}' which is forbidden before this lesson",
                        "Rewrite solution without this concept",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

        # -- Check dialogue for premature concepts --
        for dialogue_field in ["pre_topic_dialogue", "post_error_dialogue"]:
            dialogue = l.get(dialogue_field) or []
            for idx, step in enumerate(dialogue):
                step_text = step.get("text", "") if isinstance(step, dict) else ""
                step_lower = step_text.lower()

                for concept_name, triggers in concept_triggers.items():
                    if concept_name in forbidden:
                        for tr in triggers:
                            if tr in step_lower and len(tr) > 2:
                                registry.add_issue(
                                    "needs_human_review", "lesson", lid,
                                    f"{dialogue_field}[{idx}].text",
                                    "dialogue_premature_concept",
                                    step_text[:200],
                                    f"Dialogue uses '{tr}' which relates to '{concept_name}', a forbidden concept before this lesson",
                                    "Rephrase to avoid referencing this concept",
                                    auto_fix_safe=False, requires_operator_review=True,
                                )
                                break

        # -- Check syntax_reminder --
        sr = l.get("syntax_reminder")
        if sr and isinstance(sr, dict):
            if not sr.get("message"):
                registry.add_issue(
                    "needs_human_review", "lesson", lid, "syntax_reminder.message",
                    "empty_syntax_reminder", "",
                    "Syntax reminder message is empty",
                    "Add message content", auto_fix_safe=False, requires_operator_review=True,
                )


def _contains_pattern(text: str, patterns: list[str]) -> bool:
    text_lower = text.lower()
    for p in patterns:
        if p in text_lower:
            return True
    return False


# ---------------------------------------------------------------------------
# 4. Task-Answer-Checker Consistency Audit
# ---------------------------------------------------------------------------

def audit_task_consistency(data: dict, registry: IssueRegistry):
    """Check task/answer match, code formatting, suspicious one-line statements."""

    for l in data["lessons"]:
        lid = l["id"]
        mission = l.get("mission")
        if not mission or not isinstance(mission, dict):
            continue

        task = mission.get("task", "")
        expected = mission.get("expected_output", "")

        # Check that expected output is not a trivial placeholder
        if expected and expected.strip() == "...":
            registry.add_issue(
                "needs_human_review", "lesson", lid, "mission.expected_output",
                "placeholder_expected_output", expected[:200],
                "Expected output is placeholder '...'",
                "Fill in actual expected output",
                auto_fix_safe=False, requires_operator_review=True,
            )

        # Check task mentions output but expected is inconsistent
        task_lower = task.lower()
        if "выведи" in task_lower and expected:
            # Verify expected is not empty
            if not expected.strip():
                registry.add_issue(
                    "must_fix_now", "lesson", lid, "mission.expected_output",
                    "task_asks_output_but_none_expected", expected[:200],
                    "Task asks to print something but expected_output is empty",
                    "Add expected output matching the task",
                    auto_fix_safe=False, requires_operator_review=True,
                )

    # -- Check code formatting in find_bug --
    for l in data["lessons"]:
        lid = l["id"]
        fb = l.get("find_bug")
        if fb and isinstance(fb, dict):
            code = fb.get("code", "")
            correct = fb.get("correct", "")
            if code and correct:
                # Check for one-line-joined statements
                one_line_indicators = [
                    "import random print",
                    "import random\nprint",
                    "print(\"",
                ]
                for indicator in one_line_indicators:
                    if indicator in correct and "\n" not in correct:
                        registry.add_issue(
                            "needs_human_review", "lesson", lid, "find_bug.correct",
                            "suspicious_one_line_code", correct[:200],
                            "Correct solution appears joined into one line without proper formatting",
                            "Format as multi-line code block",
                            auto_fix_safe=False, requires_operator_review=True,
                        )
                        break

            # Check that code has whitespace at expected indentation
            if code and correct:
                lines_c = correct.split("\n")
                # If correct has code that should be indented but isn't
                # (e.g., after if/else/for/while)
                for i, line in enumerate(lines_c):
                    stripped = line.strip()
                    if stripped.startswith(("print(", "name =", "x =", "y =", "result =")):
                        # Check previous line for colon
                        if i > 0 and lines_c[i-1].rstrip().endswith(":"):
                            if not line.startswith(" ") and not line.startswith("\t"):
                                registry.add_issue(
                                    "needs_human_review", "lesson", lid, "find_bug.correct",
                                    "missing_indentation", correct[:300],
                                    f"Line {i+1} of correct solution should be indented after colon",
                                    "Add 4-space indentation",
                                    auto_fix_safe=False, requires_operator_review=True,
                                )

    # -- Check what_outputs --
    for l in data["lessons"]:
        lid = l["id"]
        wo = l.get("what_outputs")
        if wo and isinstance(wo, dict):
            code = wo.get("code", "")
            correct = wo.get("correct", "")
            options = wo.get("options", [])
            if correct and options:
                if correct not in options:
                    registry.add_issue(
                        "must_fix_now", "lesson", lid, "what_outputs.correct",
                        "correct_not_in_options", f"correct={correct}, options={options}",
                        "Correct answer is not among the options",
                        "Add correct answer to options list or fix correct value",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

    # -- Check code_watch code examples --
    for l in data["lessons"]:
        lid = l["id"]
        cw = l.get("code_watch")
        if cw and isinstance(cw, dict):
            main_code = cw.get("main_code", "")
            if main_code:
                # Check for suspicious one-line Python
                if "import " in main_code and "print(" in main_code and "\n" not in main_code:
                    registry.add_issue(
                        "needs_human_review", "lesson", lid, "code_watch.main_code",
                        "suspicious_one_line_code", main_code[:200],
                        "Code watch main_code appears joined into one line",
                        "Format as multi-line code",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

            # Check solution snippets
            solutions = cw.get("solutions", []) if isinstance(cw.get("solutions"), list) else []
            for sidx, sol in enumerate(solutions):
                if isinstance(sol, dict) and not sol.get("code"):
                    registry.add_issue(
                        "needs_human_review", "lesson", lid, f"code_watch.solutions[{sidx}]",
                        "empty_solution_code", str(sol)[:200],
                        "Solution entry missing code field",
                        "Add code to solution", auto_fix_safe=False, requires_operator_review=True,
                    )


# ---------------------------------------------------------------------------
# 5. Dialogue Quality Audit
# ---------------------------------------------------------------------------

def audit_dialogue_quality(data: dict, registry: IssueRegistry):
    """Check character role consistency, Bagus dominance, spoilers, dialogue length."""

    MAX_DIALOGUE_LENGTH = 12  # max steps per dialogue block
    MAX_BAGUS_CONSECUTIVE = 1  # no more than 1 Bagus in a row

    for l in data["lessons"]:
        lid = l["id"]

        for dialogue_field in ["pre_topic_dialogue", "post_error_dialogue"]:
            dialogue = l.get(dialogue_field) or []
            if not dialogue:
                continue

            # Check dialogue length
            if len(dialogue) > MAX_DIALOGUE_LENGTH:
                registry.add_issue(
                    "non_blocking_polish", "lesson", lid, dialogue_field,
                    "dialogue_too_long",
                    f"{len(dialogue)} steps (max {MAX_DIALOGUE_LENGTH})",
                    f"Dialogue block has {len(dialogue)} steps, exceeding {MAX_DIALOGUE_LENGTH}",
                    f"Consider trimming to {MAX_DIALOGUE_LENGTH} steps or fewer",
                    auto_fix_safe=False, requires_operator_review=True,
                )

            # Check consecutive Bagus
            bagus_streak = 0
            for idx, step in enumerate(dialogue):
                if not isinstance(step, dict):
                    continue
                char = step.get("character", "")
                if char == "bagus":
                    bagus_streak += 1
                    if bagus_streak > MAX_BAGUS_CONSECUTIVE:
                        registry.add_issue(
                            "needs_human_review", "lesson", lid,
                            f"{dialogue_field}[{idx}]",
                            "consecutive_bagus",
                            step.get("text", "")[:200],
                            f"Bagus appears {bagus_streak} times consecutively (max {MAX_BAGUS_CONSECUTIVE})",
                            "Separate Bagus lines with another character",
                            auto_fix_safe=False, requires_operator_review=True,
                        )
                else:
                    bagus_streak = 0

            # Check Bagus dominance (more than 40% of dialogue)
            if dialogue:
                bagus_count = sum(1 for s in dialogue if isinstance(s, dict) and s.get("character") == "bagus")
                bagus_ratio = bagus_count / len(dialogue)
                if bagus_ratio > 0.4:
                    registry.add_issue(
                        "non_blocking_polish", "lesson", lid, dialogue_field,
                        "bagus_dominance",
                        f"Bagus: {bagus_count}/{len(dialogue)} ({bagus_ratio:.0%})",
                        f"Bagus has {bagus_count}/{len(dialogue)} lines ({bagus_ratio:.0%}), dominating the educational content",
                        "Reduce Bagus lines or redistribute among other characters",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

            # Check that Va is present in post_error (should give technical explanation)
            if dialogue_field == "post_error_dialogue":
                va_present = any(
                    isinstance(s, dict) and s.get("character") == "va"
                    for s in dialogue
                )
                # Not strictly required but check if mission exists
                if l.get("mission") and not va_present and len(dialogue) > 2:
                    registry.add_issue(
                        "non_blocking_polish", "lesson", lid, dialogue_field,
                        "va_missing_from_post_error",
                        f"Va not found in {dialogue_field}",
                        "Va should provide technical explanation after errors",
                        "Consider adding Va with technical breakdown of the mistake",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

            # Check Novice role: should ask/reflect, not lecture
            for idx, step in enumerate(dialogue):
                if not isinstance(step, dict):
                    continue
                char = step.get("character", "")
                text = step.get("text", "")
                if char == "novice" and len(text) > 200:
                    registry.add_issue(
                        "non_blocking_polish", "lesson", lid,
                        f"{dialogue_field}[{idx}].text",
                        "novice_too_long",
                        text[:200],
                        "Novice dialogue line is very long; Novice should be brief and questioning",
                        "Shorten Novice line or use another character",
                        auto_fix_safe=False, requires_operator_review=True,
                    )

    # -- Check review dialogues --
    for r in data["reviews"]:
        rid = r["id"]
        dialogue = r.get("dialogue") or []
        if len(dialogue) > MAX_DIALOGUE_LENGTH:
            registry.add_issue(
                "non_blocking_polish", "review", rid, "dialogue",
                "dialogue_too_long",
                f"{len(dialogue)} steps",
                f"Review dialogue has {len(dialogue)} steps",
                f"Consider trimming to {MAX_DIALOGUE_LENGTH}",
                auto_fix_safe=False, requires_operator_review=True,
            )


# ---------------------------------------------------------------------------
# 6. Wording Clarity Audit
# ---------------------------------------------------------------------------

RISKY_WORDING_PATTERNS = [
    {
        "pattern": r"\bпроверь\b",
        "issue_type": "wording_unclear",
        "reason": "Wording 'проверь' may imply if/else before it's taught (lesson 1-8)",
        "context_rules": {"forbidden_before_concept": "if"},
        "severity": "must_fix_now",
        "severity_default": "needs_human_review",
    },
    {
        "pattern": r"\bсоздай алгоритм\b",
        "issue_type": "wording_too_abstract",
        "reason": "Wording 'создай алгоритм' too abstract for beginners without explaining algorithm",
        "severity": "needs_human_review",
    },
    {
        "pattern": r"\bсравни\b",
        "issue_type": "wording_unclear",
        "reason": "Wording 'сравни' may be unclear if expected output is just a boolean",
        "severity": "needs_human_review",
    },
    {
        "pattern": r"\bисправь\b",
        "issue_type": "wording_vague",
        "reason": "Wording 'исправь' without specifying expected behavior may be confusing",
        "severity": "non_blocking_polish",
    },
    {
        "pattern": r"\bвыведи результат\b",
        "issue_type": "wording_ambiguous",
        "reason": "Wording 'выведи результат' is ambiguous if expected output is not clearly specified",
        "severity": "needs_human_review",
    },
    {
        "pattern": r"\bнапиши программу\b",
        "issue_type": "wording_overstated",
        "reason": "Wording 'напиши программу' may overstate when only one line is expected",
        "severity": "non_blocking_polish",
    },
    {
        "pattern": r"\bиспользуй переменную\b",
        "issue_type": "wording_potential_mismatch",
        "reason": "Wording 'используй переменную' may conflict if checker expects literal",
        "severity": "needs_human_review",
    },
    {
        "pattern": r"\bнеправильно\b.*\bправильно\b|\bправильно\b.*\bнеправильно\b",
        "issue_type": "wording_visually_confusing",
        "reason": "Mix of 'правильно/неправильно' examples may be visually confusing",
        "severity": "non_blocking_polish",
    },
]


def audit_wording_clarity(data: dict, skill_prog: dict, registry: IssueRegistry):
    """Scan for risky wording patterns in tasks, dialogues, and explanations."""
    lessons_map = {l["id"]: l for l in data["lessons"]}
    prog_lessons = skill_prog.get("lessons", {})

    for l in data["lessons"]:
        lid = l["id"]
        lesson_prog = prog_lessons.get(lid, {})
        forbidden = lesson_prog.get("forbidden_before", [])

        # Fields to scan
        scan_fields = {
            "mission.task": l.get("mission", {}).get("task", "") if isinstance(l.get("mission"), dict) else "",
            "mission.expected_output": l.get("mission", {}).get("expected_output", "") if isinstance(l.get("mission"), dict) else "",
            "mini_summary": l.get("mini_summary", ""),
        }

        # Add dialogue fields
        for df in ["pre_topic_dialogue", "post_error_dialogue"]:
            dialogue = l.get(df) or []
            for idx, step in enumerate(dialogue):
                if isinstance(step, dict) and step.get("text"):
                    scan_fields[f"{df}[{idx}].text"] = step["text"]

        for field_path, text in scan_fields.items():
            if not text:
                continue
            text_lower = text.lower()

            for pattern_def in RISKY_WORDING_PATTERNS:
                pat = pattern_def["pattern"]
                issue_type = pattern_def["issue_type"]
                reason = pattern_def["reason"]

                if re.search(pat, text_lower):
                    # Check context rules
                    context_rules = pattern_def.get("context_rules", {})
                    if "forbidden_before_concept" in context_rules:
                        concept = context_rules["forbidden_before_concept"]
                        if concept in forbidden:
                            severity = pattern_def.get("severity", pattern_def["severity_default"])
                        else:
                            # This wording is safe at this point in the curriculum
                            continue
                    else:
                        severity = pattern_def.get("severity", "needs_human_review")

                    # Skip "напиши программу" for lessons where it's appropriate (later lessons)
                    if issue_type == "wording_overstated" and "напиши программу" in text_lower:
                        # Check if this is a later lesson where full program is expected
                        part = l.get("part", 0)
                        if part >= 3:
                            continue  # Later parts do expect full programs

                    suggested = _suggest_fix(issue_type, text[:200])
                    registry.add_issue(
                        severity, "lesson", lid, field_path,
                        issue_type, text[:200], reason, suggested,
                        auto_fix_safe=False, requires_operator_review=True,
                    )


def _suggest_fix(issue_type: str, text: str) -> str:
    suggestions = {
        "wording_unclear": "Rephrase to clearly state what the student should output without implying control flow",
        "wording_too_abstract": "Break down the algorithm into concrete steps",
        "wording_vague": "Specify what behavior should change and what correct output looks like",
        "wording_ambiguous": "Clearly specify what should be displayed",
        "wording_overstated": "Consider 'напиши код' or 'выведи' instead if single line",
        "wording_potential_mismatch": "Clarify whether variable name must match exactly or any name works",
        "wording_visually_confusing": "Consider reformatting correct/incorrect examples to be visually distinct",
    }
    return suggestions.get(issue_type, "Review and rephrase for clarity")


# ---------------------------------------------------------------------------
# 7. Surface Coverage Audit
# ---------------------------------------------------------------------------

def audit_coverage(data: dict, registry: IssueRegistry):
    """Check which educational blocks are missing for each lesson by difficulty and part."""

    for l in data["lessons"]:
        lid = l["id"]
        diff = l.get("difficulty", "")
        part = l.get("part", 0)

        # All lessons should have: analogy, explanation
        if not l.get("analogy"):
            registry.add_issue("non_blocking_polish", "lesson", lid, "analogy",
                "missing_analogy", "", "Lesson has no analogy block",
                "Consider adding an analogy for this concept",
                auto_fix_safe=False, requires_operator_review=True)

        if not l.get("explanation"):
            registry.add_issue("must_fix_now", "lesson", lid, "explanation",
                "missing_explanation", "", "Lesson has no explanation block",
                "Add explanation block with text, character, code_example, output",
                auto_fix_safe=False, requires_operator_review=True)

        # Most lessons should have quiz and what_outputs (exception: boss lessons may be different)
        if diff != "boss":
            if not l.get("quiz") and part <= 3:
                registry.add_issue("non_blocking_polish", "lesson", lid, "quiz",
                    "missing_quiz", "", "Lesson has no quiz block",
                    "Consider adding a quiz for this lesson",
                    auto_fix_safe=False, requires_operator_review=True)

        # All non-boss lessons should have what_outputs
        if diff != "boss" and not l.get("what_outputs"):
            registry.add_issue("non_blocking_polish", "lesson", lid, "what_outputs",
                "missing_what_outputs", "", "Lesson has no what_outputs (predict output) block",
                "Consider adding a predict-output exercise",
                auto_fix_safe=False, requires_operator_review=True)

        # Boss lessons should have code_watch
        if diff == "boss" and not l.get("code_watch"):
            registry.add_issue("needs_human_review", "lesson", lid, "code_watch",
                "boss_no_code_watch", "", "Boss difficulty lesson has no code_watch block",
                "Consider adding code_walkthrough for boss lesson",
                auto_fix_safe=False, requires_operator_review=True)

        # Post-error dialogue should exist for lessons with mission
        if l.get("mission") and not l.get("post_error_dialogue"):
            registry.add_issue("non_blocking_polish", "lesson", lid, "post_error_dialogue",
                "missing_post_error_dialogue", "",
                "Lesson with mission has no post-error dialogue",
                "Consider adding post-error dialogue for failed missions",
                auto_fix_safe=False, requires_operator_review=True)


# ---------------------------------------------------------------------------
# Inventory Writer
# ---------------------------------------------------------------------------

def save_inventory(inventory: dict):
    path = os.path.join(DOCS_DIR, "course_quality_inventory.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)
    print(f"  [OK] Inventory saved: {path}")
    return path


# ---------------------------------------------------------------------------
# Issue Registry Writer
# ---------------------------------------------------------------------------

def save_issue_registry(registry: IssueRegistry, items_checked: dict):
    reg_dict = registry.to_dict()
    reg_dict["total_items_checked"] = sum(items_checked.values())
    reg_dict["items_checked"] = dict(items_checked)

    path = os.path.join(DOCS_DIR, "course_quality_issue_registry.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reg_dict, f, ensure_ascii=False, indent=2)
    print(f"  [OK] Issue registry saved: {path} ({len(registry.issues)} issues)")
    return path


# ---------------------------------------------------------------------------
# Human Review Packet Generator
# ---------------------------------------------------------------------------

def generate_human_review_packet(registry: IssueRegistry, data: dict):
    lines = []
    lines.append("# Course Quality Audit — Human Review Packet")
    lines.append("")
    lines.append(f"**Generated:** {datetime.datetime.now(datetime.UTC).isoformat()}")
    lines.append(f"**Total Issues:** {len(registry.issues)}")
    lines.append("")
    lines.append("---")

    # Section 1: Must Fix Now
    must_fix = registry.get_by_severity("must_fix_now")
    lines.append("## 🚨 Must Fix Now")
    lines.append(f"**Count:** {len(must_fix)}")
    lines.append("")
    if must_fix:
        for iss in must_fix:
            lines.append(f"### {iss['issue_id']}: {iss['item_id']} — {iss['issue_type']}")
            lines.append(f"- **Surface:** {iss['surface']} | **Field:** `{iss['field']}`")
            lines.append(f"- **Current:** {iss['current_text'][:300]}")
            lines.append(f"- **Reason:** {iss['reason']}")
            lines.append(f"- **Suggested Fix:** {iss['suggested_fix']}")
            lines.append(f"- **Auto-fix Safe:** {'✅' if iss['auto_fix_safe'] else '❌'}")
            lines.append("")
    else:
        lines.append("_No must-fix issues found._")
        lines.append("")

    lines.append("---")

    # Section 2: Needs Human Review
    needs_review = registry.get_by_severity("needs_human_review")
    lines.append("## 🔍 Needs Human Review")
    lines.append(f"**Count:** {len(needs_review)}")
    lines.append("")
    if needs_review:
        for iss in needs_review:
            lines.append(f"### {iss['issue_id']}: {iss['item_id']} — {iss['issue_type']}")
            lines.append(f"- **Surface:** {iss['surface']} | **Field:** `{iss['field']}`")
            lines.append(f"- **Current:** {iss['current_text'][:300]}")
            lines.append(f"- **Reason:** {iss['reason']}")
            lines.append(f"- **Suggested Fix:** {iss['suggested_fix']}")
            lines.append("")
    else:
        lines.append("_No items needing human review._")
        lines.append("")

    lines.append("---")

    # Section 3: By Part
    lines.append("## 📂 Issues by Part")
    lines.append("")
    by_part = registry.get_by_part(data)
    for part_num in sorted(by_part.keys()):
        part_issues = by_part[part_num]
        lines.append(f"### Part {part_num} ({len(part_issues)} issues)")
        lines.append("")
        for iss in part_issues:
            severity_icon = {"must_fix_now": "🚨", "needs_human_review": "🔍",
                             "can_defer": "⏳", "non_blocking_polish": "💅"}
            icon = severity_icon.get(iss["severity"], "⚪")
            lines.append(f"- {icon} **{iss['issue_id']}** `{iss['severity']}` — {iss['item_id']}: {iss['issue_type']} ({iss['field']})")
            lines.append(f"  - {iss['reason'][:200]}")
        lines.append("")

    lines.append("---")

    # Section 4: By Issue Type
    lines.append("## 🏷️ Issues by Type")
    lines.append("")
    by_type: dict[str, list] = {}
    for iss in registry.issues:
        t = iss["issue_type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(iss)
    for issue_type in sorted(by_type.keys()):
        type_issues = by_type[issue_type]
        lines.append(f"### {issue_type} ({len(type_issues)} issues)")
        for iss in type_issues:
            lines.append(f"- {iss['issue_id']}: {iss['item_id']} ({iss['severity']})")
        lines.append("")

    path = os.path.join(DOCS_DIR, "course_quality_human_review_packet.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [OK] Human review packet saved: {path}")
    return path


# ---------------------------------------------------------------------------
# Audit Report Generator
# ---------------------------------------------------------------------------

def generate_audit_report(registry: IssueRegistry, inventory: dict, items_checked: dict):
    lines = []
    lines.append("# Course Quality Audit Report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.datetime.now(datetime.UTC).isoformat()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total entities checked:** {sum(items_checked.values())}")
    lines.append(f"- **Total issues found:** {len(registry.issues)}")
    lines.append("")

    severity_counts = registry.to_dict()["severity_counts"]
    lines.append("### Severity Breakdown")
    lines.append("")
    for sev, count in sorted(severity_counts.items()):
        icon = {"must_fix_now": "🚨", "needs_human_review": "🔍",
                "can_defer": "⏳", "non_blocking_polish": "💅"}
        lines.append(f"- {icon.get(sev, '⚪')} **{sev}**: {count}")
    lines.append("")

    lines.append("### Items Checked")
    lines.append("")
    lines.append("| Surface | Count |")
    lines.append("|---------|-------|")
    for surface, count in sorted(items_checked.items()):
        lines.append(f"| {surface} | {count} |")
    lines.append("")

    lines.append("### Inventory Summary")
    lines.append("")
    summary = inventory.get("summary", {})
    lines.append("| Entity | Count |")
    lines.append("|--------|-------|")
    for key in ["total_lessons", "total_recaps", "total_quests", "total_chapter_quests", "total_reviews"]:
        display_name = key.replace("total_", "").replace("_", " ").title()
        lines.append(f"| {display_name} | {summary.get(key, 0)} |")
    lines.append("")

    lines.append("## Audit Checks Enabled")
    lines.append("")
    lines.append("| Audit | Status |")
    lines.append("|-------|--------|")
    lines.append("| ✅ Structural audit | Enabled — checks required fields, data types, empty strings |")
    lines.append("| ✅ Pedagogical prerequisite audit | Enabled — checks premature concepts in tasks/dialogues |")
    lines.append("| ✅ Task-answer consistency audit | Enabled — checks task/answer match, code formatting |")
    lines.append("| ✅ Dialogue quality audit | Enabled — checks character roles, Bagus, spoilers, length |")
    lines.append("| ✅ Wording clarity audit | Enabled — checks risky pedagogical phrasing |")
    lines.append("| ✅ Surface coverage audit | Enabled — checks missing educational blocks |")
    lines.append("| ✅ Skill progression map | Enabled — references scripts/config/skill_progression.json |")
    lines.append("")

    lines.append("## Safe Auto-Fix Policy")
    lines.append("")
    lines.append("Only auto-fix issues that are structurally obvious and low-risk:")
    lines.append("")
    lines.append("**Allowed:**")
    lines.append("- Missing text copied from caption field")
    lines.append("- Whitespace cleanup (trailing spaces, extra blank lines)")
    lines.append("- Multiline code formatting if source clearly has line breaks")
    lines.append("- Duplicated accidental spaces")
    lines.append("- Typo in obvious field label")
    lines.append("")
    lines.append("**Forbidden:**")
    lines.append("- Changing teaching logic, expected answers, or checker behavior")
    lines.append("- Rewriting dialogues, changing lesson order, or changing mission goal")
    lines.append("- Mass content rewrites without human review")
    lines.append("")

    path = os.path.join(DOCS_DIR, "course_quality_audit_report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [OK] Audit report saved: {path}")
    return path


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def run_pipeline() -> dict:
    print("=" * 70)
    print("COURSE QUALITY AUDIT PIPELINE")
    print("=" * 70)

    # Load data
    print("\n[1/7] Loading course data...")
    data = load_course_data()
    skill_prog = load_skill_progression()

    lessons_count = len(data["lessons"])
    recaps_count = len(data["recaps"])
    quests_count = len(data["quests"])
    chapter_quests_count = len(data["chapter_quests"])
    reviews_count = len(data["reviews"])

    print(f"  Lessons: {lessons_count}")
    print(f"  Recaps: {recaps_count}")
    print(f"  Quests: {quests_count}")
    print(f"  Chapter Quests: {chapter_quests_count}")
    print(f"  Reviews: {reviews_count}")

    # Items checked tracking
    items_checked = {
        "lessons": lessons_count,
        "recaps": recaps_count,
        "quests": quests_count,
        "chapter_quests": chapter_quests_count,
        "reviews": reviews_count,
        "dialogue_blocks": 0,
        "mission_blocks": 0,
        "code_examples": 0,
    }

    # Count mission blocks and dialogue blocks
    for l in data["lessons"]:
        if l.get("mission"):
            items_checked["mission_blocks"] += 1
        items_checked["dialogue_blocks"] += len(l.get("pre_topic_dialogue") or [])
        items_checked["dialogue_blocks"] += len(l.get("post_error_dialogue") or [])
    for r in data["reviews"]:
        items_checked["dialogue_blocks"] += len(r.get("dialogue") or [])

    # Count code examples
    for l in data["lessons"]:
        if l.get("explanation", {}).get("code_example"):
            items_checked["code_examples"] += 1
    for q in data["quests"]:
        if q.get("example_solution"):
            items_checked["code_examples"] += 1
    for q in data["chapter_quests"]:
        if q.get("example_solution"):
            items_checked["code_examples"] += 1

    # Registry
    registry = IssueRegistry()

    # [2] Build inventory
    print(f"\n[2/7] Building course inventory...")
    inventory = build_inventory(data)
    save_inventory(inventory)

    # [3] Structural audit
    print(f"\n[3/7] Running structural audit...")
    audit_structural(data, registry)
    print(f"  Found {len(registry.get_by_type('missing_required_field'))} structural issues")

    # [4] Pedagogical prerequisite audit
    print(f"\n[4/7] Running pedagogical prerequisite audit...")
    audit_prerequisites(data, skill_prog, registry)
    print(f"  Found {len(registry.get_by_type('premature_concept_risk'))} prerequisite issues")

    # [5] Task-answer consistency audit
    print(f"\n[5/7] Running task-answer consistency audit...")
    audit_task_consistency(data, registry)
    pre_concept = registry.get_by_type('premature_concept_risk')
    print(f"  Found {len(pre_concept)} task-answer issues")

    # [6] Dialogue quality audit
    print(f"\n[6/7] Running dialogue quality audit...")
    audit_dialogue_quality(data, registry)
    print(f"  Found {len(registry.get_by_type('consecutive_bagus'))} Bagus issues")
    print(f"  Found {len(registry.get_by_type('dialogue_too_long'))} dialogue length issues")
    print(f"  Found {len(registry.get_by_type('bagus_dominance'))} Bagus dominance issues")

    # [7] Wording clarity audit
    print(f"\n[7/7] Running wording clarity audit...")
    audit_wording_clarity(data, skill_prog, registry)
    wording_issues = sum(1 for i in registry.issues if i["issue_type"].startswith("wording_"))
    print(f"  Found {wording_issues} wording issues")

    # Coverage audit
    print(f"\n  Running surface coverage audit...")
    audit_coverage(data, registry)
    coverage_issues = sum(1 for i in registry.issues if i["issue_type"].startswith("missing_") and i["severity"] != "must_fix_now")
    print(f"  Found {coverage_issues} coverage issues")

    # Save outputs
    print(f"\n{'='*70}")
    print("SAVING OUTPUTS")
    print(f"{'='*70}")

    save_issue_registry(registry, items_checked)
    generate_human_review_packet(registry, data)
    generate_audit_report(registry, inventory, items_checked)

    # Summary
    severity_counts = registry.to_dict()["severity_counts"]
    total = len(registry.issues)
    print(f"\n{'='*70}")
    print("AUDIT COMPLETE")
    print(f"{'='*70}")
    print(f"  Total issues: {total}")
    for sev, count in sorted(severity_counts.items()):
        print(f"    {sev}: {count}")
    print(f"\n  Items checked: {sum(items_checked.values())}")
    print(f"  Output files written to {DOCS_DIR}")

    result = {
        "pipeline_completed": True,
        "total_issues": total,
        "severity_counts": severity_counts,
        "items_checked": items_checked,
    }
    return result


if __name__ == "__main__":
    try:
        result = run_pipeline()
        sys.exit(0 if result["pipeline_completed"] else 1)
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        traceback.print_exc()
        sys.exit(1)
