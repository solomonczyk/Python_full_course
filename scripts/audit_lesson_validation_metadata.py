#!/usr/bin/env python3
"""Audit script to review lesson validation metadata.

Usage:
    python scripts/audit_lesson_validation_metadata.py

Output:
    - Lessons with explicit validation metadata
    - Lessons WITHOUT explicit metadata (using auto-detection fallback)
    - Summary statistics
"""

import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.validation_metadata import (
    all_validated_lesson_ids,
    list_validation_metadata,
    get_or_default,
)

DATA_FILE = Path(__file__).resolve().parent.parent / "backend" / "app" / "data" / "lessons.json"

with open(DATA_FILE, encoding="utf-8") as f:
    lessons = json.load(f)

validated_ids = set(all_validated_lesson_ids())
all_ids = set(l["id"] for l in lessons if l.get("mission"))

explicit = sorted(validated_ids & all_ids)
auto_detect = sorted(all_ids - validated_ids)
no_mission = sorted(set(l["id"] for l in lessons) - all_ids)

print("=" * 72)
print("Lesson Validation Metadata Audit")
print("=" * 72)
print(f"\nTotal lessons: {len(lessons)}")
print(f"  With mission:  {len(all_ids)}")
print(f"  No mission:    {len(no_mission)}")
print(f"  Explicit rules: {len(explicit)}")
print(f"  Auto-detect:   {len(auto_detect)}")
print()

print("─" * 72)
print("Lessons WITH explicit validation metadata:")
print("─" * 72)
val_meta = list_validation_metadata()
for v in val_meta:
    if v["lesson_id"] in all_ids:
        tc = f"  ({v['test_case_count']} test cases)" if v["test_case_count"] else ""
        ao = "  [AST only]" if v["ast_only"] else ""
        print(
            f"  {v['lesson_id']:6s}  {v['title']:<30s}"
            f" req={str(v['required_constructs']):40s}"
            f"{tc}{ao}"
        )

print()
print("─" * 72)
print(f"Lessons WITHOUT explicit metadata ({len(auto_detect)} — using auto-detect):")
print("─" * 72)
for lid in auto_detect:
    lesson = next((l for l in lessons if l["id"] == lid), None)
    v = get_or_default(lid, lesson)
    title = lesson.get("title", "") if lesson else ""
    print(
        f"  {lid:6s}  {title:<30s}"
        f" auto-req={str(v.required_constructs):40s}"
    )

print()
print("─" * 72)
print("Hardcode rejection check:")
print("─" * 72)
no_hardcode_reject = []
for lid in all_ids:
    lesson = next((l for l in lessons if l["id"] == lid), None)
    v = get_or_default(lid, lesson)
    if not v.reject_hardcoded:
        no_hardcode_reject.append((lid, lesson.get("title", "") if lesson else ""))
if no_hardcode_reject:
    print(f"  Lessons that do NOT reject hardcoded output ({len(no_hardcode_reject)}):")
    for lid, title in no_hardcode_reject:
        print(f"    {lid:6s}  {title:<30s}")
else:
    print("  All lessons reject hardcoded output (or use auto-detect).")

print()
print("─" * 72)
print("Lessons without missions (ignored):")
print("─" * 72)
for lid in sorted(no_mission):
    print(f"  {lid}")

print()
print("Done.")
