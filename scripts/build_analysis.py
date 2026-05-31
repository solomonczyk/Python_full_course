#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive analysis of all 92 lessons in lessons.json.

Generates:
  1. lesson_table: 92 entries with ID, title, topics_covered, has_code, has_quiz, has_mission, depth
  2. coverage_matrix: topic presence for Blocks A, B, C, D
  3. quality_checklist: pass/fail per criterion
"""

import json

DATA_PATH = "F:/Dev/Python_full_course/backend/app/data/lessons.json"
OUTPUT_PATH = "F:/Dev/Python_full_course/scripts/content_analysis.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    lessons = json.load(f)

# ============================================================
# Helper: determine depth
# ============================================================
def determine_depth(lesson):
    diff = lesson.get("difficulty", "easy")
    expl_len = len(lesson.get("explanation", {}).get("text", ""))
    has_cw = "code_watch" in lesson
    has_vd = "variable_demo" in lesson
    has_extra = has_cw or has_vd

    if diff in ("hard", "boss"):
        return "deep"
    if has_extra:
        return "deep"
    if diff == "medium":
        if expl_len >= 70:
            return "deep"
        return "sufficient"
    # diff == "easy"
    if expl_len >= 80:
        return "deep"
    if expl_len >= 60:
        return "sufficient"
    return "superficial"


# ============================================================
# 13.1 Lesson Table
# ============================================================
def build_lesson_table(lessons):
    """Build lesson_table: list of dicts with ID, title, topics_covered, has_code, has_quiz, has_mission, depth."""
    table = []
    for lesson in lessons:
        lid = lesson["id"]
        title = lesson["title"]
        topic = lesson.get("topic", "")
        topics_covered = [topic]

        expl = lesson.get("explanation", {})
        has_code = "yes" if ("code_example" in expl and expl["code_example"]) else "no"
        has_quiz = "yes" if "quiz" in lesson else "no"
        has_mission = "yes" if "mission" in lesson else "no"
        depth = determine_depth(lesson)

        table.append({
            "id": lid,
            "title": title,
            "topics_covered": topics_covered,
            "has_code": has_code,
            "has_quiz": has_quiz,
            "has_mission": has_mission,
            "depth": depth
        })
    return table


# ============================================================
# 13.2 Coverage Matrix
# ============================================================
def build_coverage_matrix(lessons):
    """
    Check each topic in Blocks A-D and mark:
      ✅ present (dedicated lesson or substantial coverage)
      ⚠️ mentioned briefly (mentioned in dialogue/task but no dedicated lesson)
      ❌ absent
    """

    def topic_field_matches(lesson, keywords):
        """Check if the lesson's topic/title matches any keyword (stem-based)."""
        topic = lesson.get("topic", "").lower()
        title = lesson.get("title", "").lower()
        combined = topic + " " + title
        for kw in keywords:
            kw = kw.lower()
            if kw in topic or kw in title:
                return True
        return False

    def full_text_matches(lesson, keywords):
        """Check if any keyword appears in relevant text fields (not JSON keys)."""
        texts = []
        # Collect only human-readable text fields
        texts.append(lesson.get("title", ""))
        texts.append(lesson.get("subtitle", ""))
        texts.append(lesson.get("topic", ""))
        texts.append(lesson.get("story_placement", ""))
        texts.append(lesson.get("connection_to_game", ""))
        texts.append(lesson.get("game_relevance", ""))
        texts.append(lesson.get("mini_summary", ""))
        texts.append(lesson.get("syntax_reminder", {}).get("message", ""))
        for dialogue in lesson.get("pre_topic_dialogue", []):
            texts.append(dialogue.get("text", ""))
        for dialogue in lesson.get("post_error_dialogue", []):
            texts.append(dialogue.get("text", ""))
        if "explanation" in lesson:
            texts.append(lesson["explanation"].get("text", ""))
            texts.append(lesson["explanation"].get("code_example", ""))
            texts.append(lesson["explanation"].get("output", ""))
        if "quiz" in lesson:
            texts.append(lesson["quiz"].get("question", ""))
            for opt in lesson["quiz"].get("options", []):
                texts.append(opt.get("text", ""))
        if "what_outputs" in lesson:
            texts.append(lesson["what_outputs"].get("code", ""))
        if "mission" in lesson:
            texts.append(lesson["mission"].get("task", ""))
            texts.append(lesson["mission"].get("expected_output", ""))
        if "analogy" in lesson:
            texts.append(lesson["analogy"].get("story_metaphor", ""))
            texts.append(lesson["analogy"].get("python_mapping", ""))
            texts.append(lesson["analogy"].get("key_rule", ""))
        if "code_watch" in lesson:
            texts.append(json.dumps(lesson["code_watch"]))
        if "find_bug" in lesson:
            texts.append(lesson["find_bug"].get("description", ""))
            texts.append(lesson["find_bug"].get("code", ""))
        if "practice_subtasks" in lesson:
            for pt in lesson["practice_subtasks"]:
                texts.append(pt.get("task", ""))
                texts.append(pt.get("expected_output", ""))

        combined = " ".join(texts).lower()
        for kw in keywords:
            if kw.lower() in combined:
                return True
        return False

    # Manual mapping of topics to coverage matrix categories
    # (id, status) where status is "present" (dedicated), "mentioned" (brief), or None (absent)

    # Determine presence based on dedicated lessons
    def topic_status(keywords, lesson_ids_dedicated):
        """
        keywords: list of terms to search for
        lesson_ids_dedicated: specific lesson IDs that are dedicated to this topic
        Returns: "present" if dedicated lesson exists, "mentioned" if in full text, "absent" if nowhere
        """
        # Check dedicated lessons
        for lid in lesson_ids_dedicated:
            if any(l["id"] == lid for l in lessons):
                return "✅ present"

        # Check topic/title match
        for lesson in lessons:
            if topic_field_matches(lesson, keywords):
                return "✅ present"

        # Check full text mention
        for lesson in lessons:
            if full_text_matches(lesson, keywords):
                return "⚠️ mentioned briefly"

        return "❌ absent"

    # ========================
    # Block A - Basics
    # ========================
    block_a = {
        "install": topic_status(
            ["установк", "install python", "скачат python"],
            []
        ),
        "types": topic_status(
            ["тип данных", "тип"],
            ["3-1"]  # Float и типы данных
        ),
        "int": topic_status(
            ["int", "цел"],
            ["1-5"]  # int(input())
        ),
        "float": topic_status(
            ["float", "дробн"],
            ["3-1"]  # Float и типы данных
        ),
        "str": topic_status(
            ["str", "строк", "кавычк"],
            ["1-2", "3-19"]  # Строки и кавычки, Строки база
        ),
        "bool": topic_status(
            ["bool", "true", "false", "логическ"],
            ["3-6"]  # Bool
        ),
        "variables": topic_status(
            ["перемен"],
            ["1-3"]  # Переменные
        ),
        "arithmetic": topic_status(
            ["арифмет", "сложен", "вычитан", "умнож", "делен"],
            ["1-6"]  # Арифметика
        ),
        "input()": topic_status(
            ["input"],
            ["1-4", "1-5"]  # input(), int(input())
        ),
        "print()": topic_status(
            ["print"],
            ["1-1"]  # print()
        ),
        "if/elif/else": topic_status(
            ["if", "elif", "else", "услов"],
            ["1-8", "1-9", "2-1", "3-13"]  # if, if else, elif, вложенные if
        ),
        "for/range": topic_status(
            ["for", "range"],
            ["2-5", "2-6", "3-14", "3-15", "3-16", "3-17"]  # for, range lessons
        ),
        "while": topic_status(
            ["while"],
            ["4-26", "4-27", "4-28"]  # while lessons
        ),
        "break/continue": topic_status(
            ["break", "continue"],
            ["4-2"]  # break
        ),
        "functions(def/parameters/return)": topic_status(
            ["def", "функци", "return", "параметр"],
            ["5-1", "5-2", "5-3"]  # functions lessons
        ),
        "scope": topic_status(
            ["scope", "область", "глобал", "локаль", "nonlocal"],
            []  # Not covered
        ),
        "string methods/slices": topic_status(
            ["метод", "срез", "split", "join", "upper", "lower", "strip", "str."],
            ["3-23", "3-24", "3-25", "4-9", "4-12", "4-13"]  # string methods, indices, slices, join, split
        ),
    }

    # ========================
    # Block B - Data Structures
    # ========================
    block_b = {
        "list": topic_status(
            ["списк", "list", "pop", "append", "remove", "insert", "extend"],
            ["3-27", "3-28", "3-29", "3-30", "3-31", "3-32", "3-33", "3-34",
             "3-35", "3-36", "3-37", "3-38", "3-39", "3-40"]
        ),
        "tuple": topic_status(
            ["tuple", "кортеж"],
            []  # No dedicated lesson
        ),
        "dict": topic_status(
            ["dict", "словар"],
            ["5-4"]  # Телефонная книга (dict)
        ),
        "set": topic_status(
            ["set()", "set{", "frozenset", "множество"],
            []  # No dedicated lesson
        ),
        "nested structures": topic_status(
            ["вложен"],
            ["4-18", "4-19", "4-20"]  # Вложенные списки lessons
        ),
        "list comprehension": topic_status(
            ["list comprehension", "генератор спис", "[x for", "[n for"],
            []  # Mentioned in dialogue but no dedicated lesson
        ),
        "dict comprehension": topic_status(
            ["dict comprehension", "генератор словар"],
            []  # Not covered
        ),
    }

    # ========================
    # Block C - OOP & Modules
    # ========================
    block_c = {
        "classes": topic_status(
            ["class имя", "class Hero", "class My", "class Student", "class User"],
            []  # No dedicated OOP lesson
        ),
        "inheritance": topic_status(
            ["наслед", "inheritance"],
            []  # Not covered
        ),
        "magic methods": topic_status(
            ["__init__", "__str__", "__repr__", "магическ"],
            []  # Not covered
        ),
        "exceptions": topic_status(
            ["try/except", "исключен", "exception", "raise", "try", "except"],
            ["5-7"]  # Страховка альпиниста (try/except)
        ),
        "file I/O": topic_status(
            ["open(", "read(", "write(", "close(", "with open"],
            []  # No dedicated lesson
        ),
        "import": topic_status(
            ["import", "from ", "модул", "библиотек"],
            ["2-3"]  # random.randint (uses import)
        ),
        "std library": topic_status(
            ["библиотек", "стандарт", "stdlib", "модул"],
            []  # Mentioned but no dedicated lesson
        ),
        "pip": topic_status(
            ["pip", "install package"],
            []  # Not covered
        ),
    }

    # ========================
    # Block D - Advanced
    # ========================
    block_d = {
        "decorators": topic_status(
            ["декоратор", "decorator"],
            []  # Not really covered
        ),
        "generators": topic_status(
            ["yield", "generator function"],
            []  # Not covered
        ),
        "lambda": topic_status(
            ["lambda"],
            []  # Mentioned in 4-17 dialogue but no dedicated lesson
        ),
        "map/filter/zip": topic_status(
            ["map(", "filter(", "zip("],
            ["4-14"]  # map lesson
        ),
        "*args/**kwargs": topic_status(
            ["*args", "**kwargs", "args", "kwargs"],
            []  # Not covered
        ),
        "context managers": topic_status(
            ["context manager", "with ", "контекст"],
            []  # Not covered
        ),
        "type hints": topic_status(
            ["type hint", "аннотац", "typing", "-> int", "-> str"],
            []  # Not covered
        ),
        "async": topic_status(
            ["async", "await", "асинхрон"],
            []  # Not covered
        ),
    }

    return {
        "Block A (Basics)": block_a,
        "Block B (Data Structures)": block_b,
        "Block C (OOP & Modules)": block_c,
        "Block D (Advanced)": block_d,
    }


# ============================================================
# 13.5 Quality Checklist
# ============================================================
def build_quality_checklist(lessons):
    """
    Check ALL 92 lessons against 8 criteria.
    Returns: {"pass": N, "fail": {criterion: [lesson_ids], ...}}
    """
    fails = {
        "motivation": [],
        "character_explanation": [],
        "code_example": [],
        "runnable_code": [],
        "quiz_2plus_options": [],
        "practical_quiz": [],
        "mission_concrete": [],
        "mission_expected_output": [],
    }

    for lesson in lessons:
        lid = lesson["id"]

        # 1. Has motivation ("why this matters")?
        # pre_topic_dialogue serves as motivation
        dialogue = lesson.get("pre_topic_dialogue", [])
        has_motivation = False
        for entry in dialogue:
            text = entry.get("text", "")
            # Dialogue entries > 30 chars with motivational/contextual words
            if len(text) > 30:
                has_motivation = True
                break
        if not has_motivation and len(dialogue) >= 2:
            total_len = sum(len(d.get("text", "")) for d in dialogue)
            if total_len > 60:
                has_motivation = True
        if not has_motivation:
            fails["motivation"].append(lid)

        # 2. Explanation by a character, not faceless text
        expl = lesson.get("explanation", {})
        character = expl.get("character", None)
        if not character:
            fails["character_explanation"].append(lid)

        # 3. Has at least 1 code example
        code = expl.get("code_example", "")
        if not code or not code.strip():
            fails["code_example"].append(lid)

        # 4. Code is runnable (has runnable_code field)
        runnable = lesson.get("runnable_code", "")
        if not runnable:
            fails["runnable_code"].append(lid)

        # 5. Has quiz with 2+ options
        quiz = lesson.get("quiz", {})
        options = quiz.get("options", [])
        if len(options) < 2:
            fails["quiz_2plus_options"].append(lid)

        # 6. Has practical quiz question ("what will this code output?")
        what_outputs = lesson.get("what_outputs", None)
        if not what_outputs:
            fails["practical_quiz"].append(lid)

        # 7. Has mission with concrete task
        mission = lesson.get("mission", None)
        if not mission:
            fails["mission_concrete"].append(lid)
        else:
            task = mission.get("task", "")
            if not task or len(task) < 10:
                fails["mission_concrete"].append(lid)

        # 8. Mission has clear expected_output
        expected = mission.get("expected_output", "") if mission else ""
        if not expected or not expected.strip():
            fails["mission_expected_output"].append(lid)

    # Count unique lessons that fail at least one criterion
    all_failing_ids = set()
    for lst in fails.values():
        all_failing_ids.update(lst)
    pass_count = 92 - len(all_failing_ids)

    non_empty_fails = {k: v for k, v in fails.items() if v}

    return {
        "pass": pass_count,
        "fail": non_empty_fails
    }


# ============================================================
# MAIN
# ============================================================
lesson_table = build_lesson_table(lessons)
coverage_matrix = build_coverage_matrix(lessons)
quality_checklist = build_quality_checklist(lessons)

report = {
    "lesson_table": lesson_table,
    "coverage_matrix": coverage_matrix,
    "quality_checklist": quality_checklist
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"Report written to {OUTPUT_PATH}")
print(f"Lesson table: {len(lesson_table)} entries")

depth_counts = {}
for entry in lesson_table:
    d = entry["depth"]
    depth_counts[d] = depth_counts.get(d, 0) + 1
print(f"Depth distribution: {depth_counts}")

has_code_yes = sum(1 for e in lesson_table if e["has_code"] == "yes")
has_quiz_yes = sum(1 for e in lesson_table if e["has_quiz"] == "yes")
has_mission_yes = sum(1 for e in lesson_table if e["has_mission"] == "yes")
print(f"Has code: {has_code_yes}/92, Has quiz: {has_quiz_yes}/92, Has mission: {has_mission_yes}/92")

qc = quality_checklist
print(f"Quality: pass={qc['pass']}, fail_categories={list(qc['fail'].keys())}")
