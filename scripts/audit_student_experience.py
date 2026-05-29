"""
Audit student experience integration.

Verifies:
- difficulty labels on all lessons
- time estimates on all lessons
- all 4 difficulty types used
- hard topics have review coverage
- student experience principles exist
- final game motivation in opening lesson
- environment guard in opening lesson
"""

import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent
_LESSONS_PATH = _PROJECT / "api" / "app" / "data" / "lessons.json"
_REVIEW_PATH = _PROJECT / "api" / "app" / "data" / "review_schedule.json"
_PRINCIPLES_PATH = _PROJECT / "docs" / "student_experience_principles.md"


def main() -> int:
    checks = {}
    issues = []

    with open(_LESSONS_PATH, encoding="utf-8") as f:
        lessons = json.load(f)
    with open(_REVIEW_PATH, encoding="utf-8") as f:
        review_data = json.load(f)
    reviews = review_data.get("reviews", [])

    # ── Difficulty labels ──
    missing_diff = [l["id"] for l in lessons if not l.get("difficulty")]
    checks["difficulty_labels_on_all_lessons"] = len(missing_diff) == 0
    if missing_diff:
        issues.append(f"Missing difficulty: {', '.join(missing_diff)}")

    # ── Time estimates ──
    missing_time = [l["id"] for l in lessons if not l.get("estimated_time_min")]
    checks["time_estimates_on_all_lessons"] = len(missing_time) == 0
    if missing_time:
        issues.append(f"Missing time estimate: {', '.join(missing_time)}")

    # ── All 4 difficulty types used ──
    used_diffs = set(l.get("difficulty") for l in lessons)
    required_diffs = {"easy", "medium", "hard", "boss"}
    checks["all_4_difficulty_types_used"] = required_diffs.issubset(used_diffs)
    missing_diffs = required_diffs - used_diffs
    if missing_diffs:
        issues.append(f"Missing difficulty types: {', '.join(missing_diffs)}")

    # ── Hard topics in reviews ──
    hard_topic_ids = [l["id"] for l in lessons if l.get("difficulty") == "hard"]
    review_topic_ids = set()
    for r in reviews:
        for t in r.get("topics", []):
            # topics are lesson titles — find matching lesson
            for l in lessons:
                if l["title"] in t or t in l["title"]:
                    review_topic_ids.add(l["id"])
    hard_in_reviews = [hid for hid in hard_topic_ids if hid in review_topic_ids]
    checks["hard_topics_appear_in_reviews"] = len(hard_in_reviews) >= len(hard_topic_ids) * 0.7

    # ── Principles doc exists ──
    checks["student_experience_principles_exist"] = _PRINCIPLES_PATH.exists()

    # ── Opening lesson has motivation + environment guard ──
    lesson_1 = [l for l in lessons if l["id"] == "1-1"][0]
    pre_dialogue = lesson_1.get("pre_topic_dialogue", [])
    dialogue_text = " ".join(d.get("text", "") for d in pre_dialogue).lower()
    checks["project_based_motivation_in_opening"] = "игр" in dialogue_text and "башн" in dialogue_text
    checks["beginner_environment_guard_in_opening"] = "браузер" in dialogue_text or "online" in dialogue_text
    checks["honest_difficulty_warning"] = "сложн" in dialogue_text
    checks["normalizing_errors"] = "ошибк" in dialogue_text

    # ── Each review has mixed topics ──
    mixed = sum(1 for r in reviews if len(r.get("topics", [])) >= 2)
    checks["mixed_topics_in_reviews"] = mixed >= len(reviews) * 0.8

    # ── Proof JSON ──
    report = {
        "total_lessons": len(lessons),
        "total_reviews": len(reviews),
        "checks": checks,
        "issues": issues,
        "proof": {
            "student_experience_principles_added": checks["student_experience_principles_exist"],
            "project_based_motivation": checks["project_based_motivation_in_opening"],
            "beginner_environment_guard": checks["beginner_environment_guard_in_opening"],
            "difficulty_labels_added": checks["difficulty_labels_on_all_lessons"],
            "time_expectations_added": checks["time_estimates_on_all_lessons"],
            "hard_lessons_have_review_or_relief": checks["hard_topics_appear_in_reviews"],
            "honest_difficulty_warning": checks["honest_difficulty_warning"],
            "normalizing_errors": checks["normalizing_errors"],
            "all_4_difficulty_types_used": checks["all_4_difficulty_types_used"],
        },
        "verdict": "PASSED" if all(checks.values()) else "NEEDS_FIXES",
    }

    print(f"\n{'='*50}")
    print("  Student Experience Audit")
    print(f"{'='*50}")
    for chk, val in checks.items():
        print(f"  {'✅' if val else '❌'} {chk}")
    for iss in issues:
        print(f"     Issue: {iss}")
    print(f"\n  Verdict: {report['verdict']}")
    print(f"{'='*50}\n")

    report_path = _PROJECT / "student_experience_audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Report saved to {report_path.resolve()}\n")

    return 0 if report["verdict"] == "PASSED" else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
