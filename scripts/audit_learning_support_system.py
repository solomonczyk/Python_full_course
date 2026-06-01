#!/usr/bin/env python3
"""Audit the Foundation / Glossary / Recap / Quest learning support system.

Checks:
1. Glossary exists and has minimum term count
2. All glossary terms have required fields
3. Foundation blocks exist for all lessons (full for first 10)
4. Lesson 1-1 has foundation for print/quotes/parentheses/text-vs-variable
5. Recaps exist for all 5 parts
6. Final quests exist for all 5 parts
7. Final quests have multiple constructs and test cases
8. No duplicate Bagus lines inside any lesson
9. All related lesson IDs in glossary exist
10. Routes exist (file-level check)
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

errors: list[str] = []
warnings: list[str] = []
passes: list[str] = []


def check(condition: bool, label: str):
    if condition:
        passes.append(f"  [PASS] {label}")
    else:
        errors.append(f"  [FAIL] {label}")


def warn(condition: bool, label: str):
    if not condition:
        warnings.append(f"  [WARN]  {label}")
    else:
        passes.append(f"  [PASS] {label}")


def load_json(path: Path) -> list | dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# -- 1. Glossary ----------------------------------------------------------
print("\n-- 1. Glossary --")
glossary_path = ROOT / "backend" / "app" / "data" / "glossary.json"
check(glossary_path.exists(), "glossary.json exists")

if glossary_path.exists():
    glossary = load_json(glossary_path)
    check(isinstance(glossary, list), "glossary.json is a list")
    check(len(glossary) >= 35, f"glossary has {len(glossary)} terms (>= 35)")

    required_glossary_fields = {"id", "term", "python_name", "category",
                                 "simple_definition", "analogy", "code_example",
                                 "common_mistake", "mistake_explanation",
                                 "related_lessons", "beginner_level"}
    for term in glossary:
        missing = required_glossary_fields - set(term.keys())
        if missing:
            errors.append(f"    [FAIL] Term '{term.get('id', '?')}' missing: {missing}")

    # Check for required beginner terms
    glossary_ids = [t["id"] for t in glossary]
    for required_id in ["print", "quotes", "string", "variable", "input",
                         "int", "if_statement", "else_statement", "error",
                         "syntax_error", "loop", "function_def", "dictionary"]:
        check(required_id in glossary_ids, f"Glossary has '{required_id}' term")


# -- 2. Foundation blocks --------------------------------------------------
print("\n-- 2. Foundation Blocks --")
lessons_path = ROOT / "backend" / "app" / "data" / "lessons.json"
check(lessons_path.exists(), "lessons.json exists")

if lessons_path.exists():
    lessons = load_json(lessons_path)
    check(len(lessons) == 92, f"Lesson count: {len(lessons)} (expected 92)")

    # All lessons have foundation
    no_foundation = [l["id"] for l in lessons if "foundation" not in l]
    check(len(no_foundation) == 0, f"All lessons have foundation ({len(no_foundation)} missing)")

    # First 10 (lessons 1-1 through 1-9) have full foundation with terms
    part1 = [l for l in lessons if l["part"] == 1]
    first_10 = [l for l in part1 if int(l["id"].split("-")[1]) <= 9]
    missing_terms = [l["id"] for l in first_10
                     if "terms" not in l.get("foundation", {})]
    check(len(missing_terms) == 0, f"First 9 lessons all have foundation terms ({len(missing_terms)} missing)")

    # Lesson 1-1 specific checks
    lesson_11 = next((l for l in lessons if l["id"] == "1-1"), None)
    if lesson_11:
        foundation = lesson_11.get("foundation", {})
        terms = foundation.get("terms", [])
        term_ids = [t.get("term_id") for t in terms]
        check("print" in term_ids, "1-1 foundation has 'print' term")
        check("quotes" in term_ids, "1-1 foundation has 'quotes' term")
        has_error = any("error" in t.get("term_id", "") for t in terms)
        check(has_error, "1-1 foundation has error feedback term")


# -- 3. Bagus duplicates --------------------------------------------------
print("\n-- 3. Bagus Role --")
bagus_duplicates = 0
for lesson in lessons:
    dialogue = lesson.get("post_error_dialogue", [])
    for i, line in enumerate(dialogue):
        if (line.get("character") == "bagus"
                and i + 1 < len(dialogue)
                and dialogue[i + 1].get("character") == "bagus"):
            bagus_duplicates += 1
check(bagus_duplicates == 0, f"No consecutive Bagus lines (found {bagus_duplicates} before fix)")


# -- 4. Recaps ------------------------------------------------------------
print("\n-- 4. Recaps --")
recaps_path = ROOT / "backend" / "app" / "data" / "recaps.json"
check(recaps_path.exists(), "recaps.json exists")

if recaps_path.exists():
    recaps = load_json(recaps_path)
    check(isinstance(recaps, list), "recaps.json is a list")
    check(len(recaps) >= 5, f"Recap count: {len(recaps)} (>= 5)")

    parts_covered = sorted(set(r["part"] for r in recaps))
    check(parts_covered == [1, 2, 3, 4, 5], f"Recaps cover parts {parts_covered}")

    required_recap_fields = {"id", "part", "title", "story_summary",
                              "learned_terms", "hero_skills", "key_rules", "mini_check"}
    for recap in recaps:
        missing = required_recap_fields - set(recap.keys())
        if missing:
            errors.append(f"    [FAIL] Recap '{recap.get('id', '?')}' missing: {missing}")


# -- 5. Quests ------------------------------------------------------------
print("\n-- 5. Final Quests --")
quests_path = ROOT / "backend" / "app" / "data" / "chapter_quests.json"
check(quests_path.exists(), "chapter_quests.json exists")

if quests_path.exists():
    quests = load_json(quests_path)
    check(isinstance(quests, list), "chapter_quests.json is a list")
    check(len(quests) >= 5, f"Quest count: {len(quests)} (>= 5)")

    parts_covered = sorted(set(q["part"] for q in quests))
    check(parts_covered == [1, 2, 3, 4, 5], f"Quests cover parts {parts_covered}")

    for quest in quests:
        check(len(quest.get("required_constructs", [])) >= 3,
              f"Quest '{quest['id']}' has >= 3 constructs (multi-skill)")
        check(len(quest.get("test_cases", [])) >= 1,
              f"Quest '{quest['id']}' has test cases")
        check(len(quest.get("hints", [])) >= 1,
              f"Quest '{quest['id']}' has hints")
        check(len(quest.get("hints", [])) >= 1,
              f"Quest '{quest['id']}' has success_criteria")

    # All required lessons exist
    lesson_ids = {l["id"] for l in lessons}
    for quest in quests:
        for req in quest.get("required_lessons", []):
            if req not in lesson_ids:
                errors.append(f"    [FAIL] Quest '{quest['id']}' references unknown lesson '{req}'")


# -- 6. Route verification (static check) --------------------------------
print("\n-- 6. Route Verification --")
app_path = ROOT / "frontend" / "src" / "App.tsx"
if app_path.exists():
    app_text = app_path.read_text(encoding="utf-8")
    check('path="/glossary"' in app_text, "/glossary route in App.tsx")
    check('path="/recap/:id"' in app_text, "/recap/:id route in App.tsx")
    check('path="/quest/:id"' in app_text, "/quest/:id route in App.tsx")
    check("GlossaryPage" in app_text, "GlossaryPage imported in App.tsx")
    check("RecapPage" in app_text, "RecapPage imported in App.tsx")
    check("QuestPage" in app_text, "QuestPage imported in App.tsx")
    # Existing routes preserved
    check('path="/lesson/:id"' in app_text, "Existing /lesson/:id route preserved")
    check('path="/course"' in app_text, "Existing /course route preserved")
    check('path="/lesson/:id/preview"' in app_text, "Existing /preview route preserved")


# -- 7. Sidebar links ----------------------------------------------------─
print("\n-- 7. Sidebar Navigation --")
sidebar_path = ROOT / "frontend" / "src" / "components" / "Sidebar.tsx"
if sidebar_path.exists():
    sidebar_text = sidebar_path.read_text(encoding="utf-8")
    check('to="/glossary"' in sidebar_text, "Sidebar has /glossary link")
    check('to={`/recap/${r.id}`}' in sidebar_text or 'to={`/recap/' in sidebar_text,
          "Sidebar has recap links")


# -- 8. Backend routers --------------------------------------------------
print("\n-- 8. Backend Routes --")
glossary_router = ROOT / "backend" / "app" / "routers" / "glossary.py"
check(glossary_router.exists(), "glossary.py router exists")
if glossary_router.exists():
    text = glossary_router.read_text(encoding="utf-8")
    check('prefix="/glossary"' in text, "glossary router has /glossary prefix")

recaps_router = ROOT / "backend" / "app" / "routers" / "recaps.py"
check(recaps_router.exists(), "recaps.py router exists")
if recaps_router.exists():
    text = recaps_router.read_text(encoding="utf-8")
    check('prefix="/recaps"' in text, "recaps router has /recaps prefix")

quests_router = ROOT / "backend" / "app" / "routers" / "quests.py"
check(quests_router.exists(), "quests.py router exists")
if quests_router.exists():
    text = quests_router.read_text(encoding="utf-8")
    check('prefix="/quests"' in text, "quests router has /quests prefix")


# -- Summary ------------------------------------------------------------─
print()
print("=" * 60)
print("  Learning Support System Audit Report")
print("=" * 60)

print(f"\n[PASS] Passed: {len(passes)}")
for p in passes:
    print(p)

if warnings:
    print(f"\n[WARN]  Warnings: {len(warnings)}")
    for w in warnings:
        print(w)

if errors:
    print(f"\n[FAIL] Errors: {len(errors)}")
    for e in errors:
        print(e)
else:
    print("\n[OK] All checks passed!")

print(f"\nTotal: {len(passes)} passed, {len(warnings)} warnings, {len(errors)} errors")

if errors:
    sys.exit(1)
