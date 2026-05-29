"""
Coverage verification script for Python Quest — Scenario Pack v2.

Usage: python scripts/verify_coverage.py

Checks that all 86 lessons have 100% coverage for all scenario fields,
then outputs a JSON report.
"""

import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent
_LESSONS_PATH = _PROJECT / "api" / "app" / "data" / "lessons.json"
_FRONTEND_PATH = _PROJECT / "frontend"

# All required scenario fields
REQUIRED_FIELDS = [
    "story_placement",
    "pre_topic_dialogue",
    "post_error_dialogue",
    "mini_summary",
    "connection_to_game",
    "game_relevance",
]

OPTIONAL_FIELDS = [
    "syntax_reminder",
]

# Existing structural fields (must all still be present)
STRUCTURAL_FIELDS = [
    "id", "part", "chapter", "lesson", "slug", "title", "subtitle",
    "topic", "locked", "explanation", "quiz", "what_outputs",
    "find_bug", "mission",
]


def check_typescript_build() -> tuple[bool, str]:
    """Run TypeScript type-check. Returns (passed, output)."""
    try:
        result = subprocess.run(
            "npx tsc --noEmit",
            cwd=str(_FRONTEND_PATH),
            capture_output=True,
            text=True,
            timeout=60,
            shell=True,
        )
        passed = result.returncode == 0
        output = result.stdout or result.stderr or ""
        return passed, output.strip()
    except FileNotFoundError:
        return False, "npx/tsc not found"
    except subprocess.TimeoutExpired:
        return False, "TypeScript check timed out"
    except Exception as e:
        return False, str(e)


def main() -> int:
    if not _LESSONS_PATH.exists():
        print(f"ERROR: lessons.json not found at {_LESSONS_PATH}")
        return 1

    with open(_LESSONS_PATH, encoding="utf-8") as f:
        lessons = json.load(f)

    total = len(lessons)
    report = {
        "total_lessons": total,
        "checks": {},
        "field_details": {},
        "ts_build": None,
    }

    all_passed = True

    # ── Check structural fields ──
    for field in STRUCTURAL_FIELDS:
        missing = [l["id"] for l in lessons if field not in l]
        count = total - len(missing)
        report["field_details"][field] = {
            "coverage": f"{count}/{total}",
            "passed": len(missing) == 0,
            "missing": missing if missing else None,
        }
        if missing:
            all_passed = False

    # ── Check scenario fields ──
    for field in REQUIRED_FIELDS:
        missing = [l["id"] for l in lessons if l.get(field) is None]
        count = total - len(missing)
        has_content = bool(lessons[0].get(field))  # quick type check
        field_type = type(lessons[0].get(field)).__name__ if lessons[0].get(field) else "unknown"

        passed = len(missing) == 0
        if not passed:
            all_passed = False

        report["field_details"][field] = {
            "coverage": f"{count}/{total}",
            "type": field_type,
            "passed": passed,
            "missing": missing if missing else None,
            "sample": str(lessons[0].get(field, ""))[:80] if lessons[0].get(field) else None,
        }

    # ── Check optional fields (track but don't require 86/86) ──
    for field in OPTIONAL_FIELDS:
        present = [l for l in lessons if l.get(field) is not None]
        count = len(present)
        sample_val = present[0].get(field) if present else None
        field_type = type(sample_val).__name__ if sample_val else "N/A"
        report["field_details"][field] = {
            "coverage": f"{count}/{total}",
            "type": field_type,
            "passed": True,  # optional fields always pass
            "missing": None,
        }

    # ── Required reminders check ──
    # Lessons with block structures MUST have syntax_reminder
    REQUIRED_REMINDER_IDS = [
        "1-5", "1-8", "1-9", "2-1", "2-5", "2-6",
        "3-1", "3-13", "3-14", "3-24", "3-25", "3-29", "3-30", "3-31", "3-41",
        "4-1", "4-2", "4-18", "4-24", "4-25", "4-26", "4-27", "4-31",
    ]
    missing_reminders = [lid for lid in REQUIRED_REMINDER_IDS
                         if not any(l.get("syntax_reminder") for l in lessons if l["id"] == lid)]
    report["required_reminders_present"] = len(missing_reminders) == 0
    report["missing_reminders"] = missing_reminders if missing_reminders else None
    if missing_reminders:
        print(f"  ❌ Required reminders missing: {', '.join(missing_reminders)}")
        all_passed = False

    # ── Check TypeScript build ──
    ts_ok, ts_output = check_typescript_build()
    report["ts_build"] = {
        "passed": ts_ok,
        "output": ts_output if not ts_ok else None,
    }
    if not ts_ok:
        all_passed = False

    # ── Verdict ──
    report["verdict"] = "ready_for_review" if all_passed else "needs_fixes"

    # ── Print human-readable summary ──
    print(f"\n{'='*50}")
    print(f"  Python Quest — Coverage Report")
    print(f"{'='*50}")
    print(f"  Total lessons: {total}")
    print(f"  Verdict: {report['verdict'].upper()}")
    print()

    for field in STRUCTURAL_FIELDS:
        d = report["field_details"][field]
        icon = "✅" if d["passed"] else "❌"
        print(f"  {icon} {field:<25s} {d['coverage']}")

    print()
    for field in REQUIRED_FIELDS:
        d = report["field_details"][field]
        icon = "✅" if d["passed"] else "❌"
        print(f"  {icon} {field:<25s} {d['coverage']:>8s}  [{d['type']}]")
        if d["missing"]:
            print(f"       Missing: {', '.join(d['missing'][:5])}{'...' if len(d['missing']) > 5 else ''}")

    print()
    for field in OPTIONAL_FIELDS:
        d = report["field_details"][field]
        print(f"  ⬜ {field:<25s} {d['coverage']:>8s}  [{d['type']}] (optional)")

    print()
    ts_icon = "✅" if report["ts_build"]["passed"] else "❌"
    print(f"  {ts_icon} TypeScript build: {'passed' if report['ts_build']['passed'] else 'FAILED'}")
    rr_icon = "✅" if report.get("required_reminders_present") else "❌"
    print(f"  {rr_icon} Required reminders: {'all present' if report.get('required_reminders_present') else 'MISSING'}")

    print()
    verdict_icon = "✅" if all_passed else "❌"
    print(f"  {verdict_icon} Verdict: {report['verdict']}")
    print(f"{'='*50}\n")

    # ── Output JSON report ──
    report_path = _PROJECT / "coverage_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Full report saved to {report_path.resolve()}")
    print()

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
