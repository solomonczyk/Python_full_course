#!/usr/bin/env python3
"""Verify lesson 1-1 foundation block is properly configured for UI rendering.

Checks:
1. Foundation block exists in lesson 1-1 data
2. All required terms are present
3. Foundation block is rendered before dialogue (per LessonPage.tsx order)
4. No consecutive Bagus lines in lesson 1-1
5. Bagus role is properly introduced
6. All 92 lessons preserved
"""

import json
import os
import sys

# Paths
BACKEND_LESSONS = os.path.join(
    os.path.dirname(__file__), "..", "backend", "app", "data", "lessons.json"
)
API_LESSONS = os.path.join(
    os.path.dirname(__file__), "..", "api", "app", "data", "lessons.json"
)
LESSON_PAGE = os.path.join(
    os.path.dirname(__file__), "..", "frontend", "src", "pages", "LessonPage.tsx"
)

REQUIRED_TERM_IDS = [
    "command",         # Команда / инструкция
    "print",           # print()
    "parentheses",     # Скобки ()
    "quotes",          # Кавычки
    "quotes_types",    # Кавычки: ' и "
    "string",          # Текст vs переменная
    "error",           # Python точен (опечатки, точность)
    "pep8",            # PEP8: аккуратный почерк кода
    "bagus",           # Багус: инспектор ловушек
]


def check_data_file(path: str, label: str) -> list[str]:
    """Check a lessons.json file for proper foundation data."""
    errors = []
    if not os.path.exists(path):
        return [f"{label}: File not found: {path}"]

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        return [f"{label}: Expected list, got {type(data).__name__}"]

    if len(data) != 92:
        errors.append(f"{label}: Expected 92 lessons, got {len(data)}")

    lesson_1 = data[0]
    if lesson_1.get("id") != "1-1":
        errors.append(f"{label}: First lesson is not 1-1 (got '{lesson_1.get('id')}')")

    # Check foundation block
    foundation = lesson_1.get("foundation")
    if not foundation:
        errors.append(f"{label}: Lesson 1-1 has NO foundation block")
        return errors

    terms = foundation.get("terms", [])
    term_ids = [t["term_id"] for t in terms]

    # Check all required terms
    for required in REQUIRED_TERM_IDS:
        if required not in term_ids:
            errors.append(f"{label}: Missing required foundation term: '{required}'")

    # Check for extra unknown terms
    allowed_extra = {"syntax_error"}  # existing term, not in required but OK
    unknown = set(term_ids) - set(REQUIRED_TERM_IDS) - allowed_extra
    if unknown:
        errors.append(f"{label}: Unknown foundation terms: {unknown}")

    # Check glossary_terms exist
    glossary_terms = foundation.get("glossary_terms", [])
    if not glossary_terms:
        errors.append(f"{label}: No glossary_terms in foundation")

    # Check rules exist
    rules = foundation.get("rules", [])
    if len(rules) < 2:
        errors.append(f"{label}: Too few rules ({len(rules)})")

    # Check no consecutive Bagus lines
    post_dialogue = lesson_1.get("post_error_dialogue", [])
    bagus_seen_consecutive = False
    bagus_count = 0
    for i in range(len(post_dialogue) - 1):
        if (post_dialogue[i].get("character") == "bagus" and
            post_dialogue[i + 1].get("character") == "bagus"):
            bagus_seen_consecutive = True
            errors.append(f"{label}: Consecutive Bagus lines at indices {i}, {i+1}")
    for line in post_dialogue:
        if line.get("character") == "bagus":
            bagus_count += 1

    if bagus_count == 0:
        errors.append(f"{label}: No Bagus line in lesson 1-1 (expected 1)")

    return errors


def check_render_order(path: str) -> list[str]:
    """Check that FoundationBlock renders before dialogue in LessonPage."""
    errors = []
    if not os.path.exists(path):
        return [f"LessonPage not found: {path}"]

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check FoundationBlock is imported
    if "import FoundationBlock" not in content:
        errors.append("LessonPage.tsx: Missing FoundationBlock import")

    # Only search within the JSX return section (the actual render order).
    # Skip import lines at the top of the file.
    return_idx = content.find("return (")
    if return_idx == -1:
        errors.append("LessonPage.tsx: Could not find return statement")
        return errors
    render_section = content[return_idx:]

    # Check FoundationBlock is rendered before dialogue
    foundation_idx = render_section.find("FoundationBlock")
    dialogue_idx = render_section.find("pre_topic_dialogue")

    if foundation_idx == -1:
        errors.append("LessonPage.tsx: FoundationBlock not rendered in JSX")
    elif dialogue_idx == -1:
        errors.append("LessonPage.tsx: pre_topic_dialogue not rendered in JSX")
    elif foundation_idx > dialogue_idx:
        errors.append(
            "LessonPage.tsx: FoundationBlock renders AFTER dialogue "
            "(should be before)"
        )

    # Check foundation render is before analogy, practice, mission
    for block in ["analogy", "practice", "mission"]:
        block_idx = render_section.find(block)
        if block_idx != -1 and foundation_idx > block_idx:
            errors.append(
                f"LessonPage.tsx: FoundationBlock renders AFTER {block}"
            )

    return errors


def main() -> int:
    all_errors = []

    print("=" * 60)
    print("Lesson 1-1 Foundation Render Verification")
    print("=" * 60)

    # 1. Check backend data
    print("\n[1/3] Checking backend data file...")
    errors = check_data_file(BACKEND_LESSONS, "backend")
    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        all_errors.extend(errors)
    else:
        print("  PASS")

    # 2. Check API data file (deployed to Vercel)
    print("\n[2/3] Checking API data file...")
    errors = check_data_file(API_LESSONS, "api")
    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        all_errors.extend(errors)
    else:
        print("  PASS")

    # 3. Check render order in LessonPage.tsx
    print("\n[3/3] Checking render order...")
    errors = check_render_order(LESSON_PAGE)
    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        all_errors.extend(errors)
    else:
        print("  PASS")

    # Summary
    print("\n" + "=" * 60)
    if all_errors:
        print(f"VERIFICATION FAILED: {len(all_errors)} issue(s)")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    else:
        print("VERIFICATION PASSED: All checks OK")
        return 0


if __name__ == "__main__":
    sys.exit(main())
