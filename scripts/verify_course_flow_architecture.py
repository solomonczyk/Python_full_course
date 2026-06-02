#!/usr/bin/env python3
"""Verify course flow architecture: quests, recaps, part 3 pacing, preserved fixes."""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ── paths ──────────────────────────────────────────────────────────────────
BACKEND_DATA = REPO / "backend" / "app" / "data"
API_DATA = REPO / "api" / "app" / "data"
LESSONS_FILE = BACKEND_DATA / "lessons.json"
QUESTS_FILE = BACKEND_DATA / "quests.json"
CHAPTER_QUESTS_FILE = BACKEND_DATA / "chapter_quests.json"
RECAPS_FILE = BACKEND_DATA / "recaps.json"

checks = []
errors = []


def check(name: str, condition: bool, detail: str = ""):
    checks.append({"name": name, "passed": condition, "detail": detail})
    if not condition:
        errors.append(f"  FAIL: {name} — {detail}")


# 1. Preserved bounded fixes ────────────────────────────────────────────────
lessons = json.loads(LESSONS_FILE.read_text(encoding="utf-8"))
lesson_2_5 = next((l for l in lessons if l["id"] == "2-5"), None)
lesson_4_30 = next((l for l in lessons if l["id"] == "4-30"), None)

# Lesson 2-5: mission should be arithmetic-only, no string formatting in mission
if lesson_2_5:
    mission = lesson_2_5.get("mission", {})
    task = mission.get("task", "")
    check(
        "lesson_2_5_still_fixed",
        "3 * i" in task and "3 * 1 = 3" not in task,
        f"Task: {task[:80]}...",
    )

# Lesson 4-30: should be multi-step recap, not append-only
if lesson_4_30:
    mission = lesson_4_30.get("mission", {})
    task = mission.get("task", "")
    has_append = "append" in task
    has_len = "len" in task or "len(" in task
    check(
        "lesson_4_30_still_fixed",
        has_append and has_len,
        f"Task: {task[:100]}...",
    )

# 2. Quest architecture ─────────────────────────────────────────────────────
quests = json.loads(QUESTS_FILE.read_text(encoding="utf-8"))

check(
    "level_5_quests_exist",
    len(quests) >= 6,
    f"Found {len(quests)} quests (expected 6+)",
)

level_5_count = sum(1 for q in quests if len(q.get("required_constructs", [])) >= 3)
check(
    "quests_have_multiple_skills",
    level_5_count >= 6,
    f"{level_5_count}/6 quests have 3+ required constructs",
)

quests_with_test_cases = sum(1 for q in quests if len(q.get("test_cases", [])) >= 1)
check(
    "quests_have_test_cases",
    quests_with_test_cases >= 6,
    f"{quests_with_test_cases}/6 quests have test cases",
)

quests_with_prior_skills = sum(1 for q in quests if len(q.get("required_lessons", [])) >= 1)
check(
    "quests_have_required_prior_skills",
    quests_with_prior_skills >= 6,
    f"{quests_with_prior_skills}/6 quests have required_lessons",
)

# Capstone check
capstone = next((q for q in quests if q.get("is_capstone")), None)
check(
    "part_5_capstone_exists",
    capstone is not None,
    f"Capstone: {capstone['title'] if capstone else 'NOT FOUND'}",
)
if capstone:
    constructs = capstone.get("required_constructs", [])
    check(
        "capstone_integrates_multiple_skills",
        len(constructs) >= 6,
        f"Capstone integrates {len(constructs)} constructs: {constructs}",
    )

# 3. Part 3 pacing ──────────────────────────────────────────────────────────
recaps = json.loads(RECAPS_FILE.read_text(encoding="utf-8"))

part_3_recaps = [r for r in recaps if r["part"] == 3]
sub_recap_ids = ["recap-3a", "recap-3b", "recap-3c", "recap-3d"]
existing_sub_recaps = [r["id"] for r in part_3_recaps if r["id"] in sub_recap_ids]

check(
    "part_3_has_recap_checkpoints",
    len(existing_sub_recaps) >= 4,
    f"Part 3 sub-recaps: {existing_sub_recaps}",
)

# Each sub-recap should have mini_check with questions
for rid in sub_recap_ids:
    recap = next((r for r in recaps if r["id"] == rid), None)
    if recap:
        check(
            f"recap_{rid}_has_mini_check",
            len(recap.get("mini_check", [])) >= 3,
            f"{rid}: {len(recap.get('mini_check', []))} mini-check questions",
        )
        check(
            f"recap_{rid}_has_key_rules",
            len(recap.get("key_rules", [])) >= 5,
            f"{rid}: {len(recap.get('key_rules', []))} key rules",
        )

# 4. 92 lessons preserved ────────────────────────────────────────────────────
check(
    "all_92_lessons_preserved",
    len(lessons) == 92,
    f"Found {len(lessons)} lessons (expected 92)",
)

# 5. Backend/API data synced ─────────────────────────────────────────────────
def files_match(a: Path, b: Path) -> bool:
    if not a.exists() or not b.exists():
        return False
    return a.read_bytes() == b.read_bytes()


check(
    "backend_api_quests_synced",
    files_match(BACKEND_DATA / "quests.json", API_DATA / "quests.json"),
    "quests.json backend vs api differ",
)
check(
    "backend_api_recaps_synced",
    files_match(BACKEND_DATA / "recaps.json", API_DATA / "recaps.json"),
    "recaps.json backend vs api differ",
)

# 6. Legacy chapter_quests.json unchanged ────────────────────────────────────
if CHAPTER_QUESTS_FILE.exists():
    orig = json.loads(CHAPTER_QUESTS_FILE.read_text(encoding="utf-8"))
    check(
        "chapter_quests_unchanged",
        len(orig) == 5,
        f"chapter_quests.json has {len(orig)} entries (expected 5)",
    )

# ── summary ────────────────────────────────────────────────────────────────
passed = sum(1 for c in checks if c["passed"])
total = len(checks)
print(f"\n{'='*60}")
print(f" Course Flow Architecture Verification")
print(f"{'='*60}")
print(f"  {passed}/{total} checks passed\n")
for c in checks:
    status = "[PASS]" if c["passed"] else "[FAIL]"
    print(f"  {status} {c['name']}")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for e in errors:
        print(e)

print(f"\nVerdict: {'PASS' if passed == total else 'NEEDS_FIX'}")
sys.exit(0 if passed == total else 1)
