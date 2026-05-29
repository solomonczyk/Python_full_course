"""
Audit difficulty curve across all lessons.

Checks:
- No sharp easy→hard jump without review in between
- Hard lessons have syntax_reminder
- Hard lessons have post_error_dialogue
- After hard lesson, next lesson is review or easier
"""

import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent
_LESSONS_PATH = _PROJECT / "api" / "app" / "data" / "lessons.json"
_REVIEW_PATH = _PROJECT / "api" / "app" / "data" / "review_schedule.json"

DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2, "boss": 3}


def main() -> int:
    with open(_LESSONS_PATH, encoding="utf-8") as f:
        lessons = json.load(f)
    with open(_REVIEW_PATH, encoding="utf-8") as f:
        review_data = json.load(f)
    reviews = review_data.get("reviews", [])
    review_positions = set(r["position_after"] for r in reviews)

    issues: list[str] = []
    passed_checks: list[str] = []

    # ── Check 1: hard lessons have syntax_reminder ──
    hard_lessons = [l for l in lessons if l.get("difficulty") == "hard"]
    missing_reminder = [l["id"] for l in hard_lessons if not l.get("syntax_reminder")]
    if missing_reminder:
        issues.append(f"Hard lessons without syntax_reminder: {', '.join(missing_reminder)}")
    else:
        passed_checks.append(f"All {len(hard_lessons)} hard lessons have syntax_reminder")

    # ── Check 2: hard lessons have post_error_dialogue ──
    missing_post = [l["id"] for l in hard_lessons if not l.get("post_error_dialogue")]
    if missing_post:
        issues.append(f"Hard lessons without post_error_dialogue: {', '.join(missing_post)}")
    else:
        passed_checks.append(f"All {len(hard_lessons)} hard lessons have post_error_dialogue")

    # ── Check 3: no sharp easy→hard jump ──
    for i in range(1, len(lessons)):
        prev = lessons[i - 1]
        curr = lessons[i]
        prev_diff = DIFFICULTY_ORDER.get(prev.get("difficulty", "medium"), 1)
        curr_diff = DIFFICULTY_ORDER.get(curr.get("difficulty", "medium"), 1)
        diff_jump = curr_diff - prev_diff
        if diff_jump >= 2:  # easy→hard or easy→boss
            has_review_between = prev["id"] in review_positions
            if not has_review_between:
                issues.append(f"Sharp difficulty jump: {prev['id']}({prev.get('difficulty')}) → {curr['id']}({curr.get('difficulty')}) without review")

    if not any(i.startswith("Sharp") for i in issues):
        passed_checks.append("No sharp difficulty jumps without in-between review")

    # ── Check 4: after hard lesson → next is review or same/easier ──
    for i in range(len(lessons) - 1):
        curr = lessons[i]
        next_l = lessons[i + 1]
        if curr.get("difficulty") == "hard":
            next_diff = DIFFICULTY_ORDER.get(next_l.get("difficulty", "medium"), 1)
            curr_diff = DIFFICULTY_ORDER.get("hard", 2)
            if next_diff > curr_diff and curr["id"] not in review_positions:
                issues.append(f"Hard→Harder without review: {curr['id']}(hard) → {next_l['id']}({next_l.get('difficulty')})")

    # ── Difficulty distribution ──
    dist: dict[str, int] = {}
    for l in lessons:
        d = l.get("difficulty", "unknown")
        dist[d] = dist.get(d, 0) + 1

    report = {
        "total_lessons": len(lessons),
        "difficulty_distribution": dist,
        "hard_lessons_count": len(hard_lessons),
        "checks": {
            "hard_lessons_have_syntax_reminder": len(missing_reminder) == 0,
            "hard_lessons_have_post_error_dialogue": len(missing_post) == 0,
            "no_sharp_easy_hard_jumps_without_review": True,
            "hard_topics_have_review_support": True,
        },
        "issues": issues,
        "passed_checks": passed_checks,
        "verdict": "PASSED" if not issues else "NEEDS_FIXES",
    }

    # Fix the check flag
    report["checks"]["no_sharp_easy_hard_jumps_without_review"] = not any(
        i.startswith("Sharp") for i in issues
    )
    report["checks"]["hard_topics_have_review_support"] = not any(
        i.startswith("Hard") for i in issues
    )

    print(f"\n{'='*50}")
    print("  Difficulty Curve Audit")
    print(f"{'='*50}")
    print(f"  Lessons: {len(lessons)}")
    print(f"  Difficulty distribution:")
    for d, c in sorted(dist.items()):
        bar = "█" * (c // 2)
        print(f"    {d:<10s} {c:>2d} {bar}")
    print()
    for chk in passed_checks:
        print(f"  ✅ {chk}")
    for iss in issues:
        print(f"  ❌ {iss}")
    print(f"\n  Verdict: {report['verdict']}")
    print(f"{'='*50}\n")

    report_path = _PROJECT / "difficulty_curve_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Report saved to {report_path.resolve()}\n")

    return 0 if report["verdict"] == "PASSED" else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
