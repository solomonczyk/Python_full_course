"""
Verify the review schedule for quality and coverage.

Checks:
- max_gap_without_review <= 3
- All 4 review types present
- Mixed topics (2+ topics per review)
- Outputs proof JSON
"""

import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent
_LESSONS_PATH = _PROJECT / "api" / "app" / "data" / "lessons.json"
_REVIEW_PATH = _PROJECT / "api" / "app" / "data" / "review_schedule.json"


def main() -> int:
    if not _REVIEW_PATH.exists():
        print(f"ERROR: review_schedule.json not found at {_REVIEW_PATH}")
        return 1

    with open(_LESSONS_PATH, encoding="utf-8") as f:
        lessons = json.load(f)

    with open(_REVIEW_PATH, encoding="utf-8") as f:
        data = json.load(f)

    reviews = data.get("reviews", [])
    total_reviews = len(reviews)
    print(f"Review schedule: {total_reviews} review blocks for {len(lessons)} lessons\n")

    # ── Check: max gap without review ──
    lesson_ids = [l["id"] for l in lessons]
    review_positions = set(r["position_after"] for r in reviews)
    max_gap = 0
    current_gap = 0
    for lid in lesson_ids:
        current_gap += 1
        if lid in review_positions:
            max_gap = max(max_gap, current_gap)
            current_gap = 0
    max_gap = max(max_gap, current_gap)  # tail
    max_gap_ok = max_gap <= 3

    # ── Check: all 4 types present ──
    type_counts: dict[str, int] = {}
    for r in reviews:
        type_counts[r["type"]] = type_counts.get(r["type"], 0) + 1
    all_types = ["quick_recall", "chapter_review", "boss_review", "part_review"]
    types_present = all(t in type_counts for t in all_types)

    # ── Check: mixed topics (2+ topics per review) ──
    mixed_reviews = sum(1 for r in reviews if len(r.get("topics", [])) >= 2)
    total_with_topics = sum(1 for r in reviews if r.get("topics"))
    mixed_ok = mixed_reviews >= total_with_topics * 0.8

    # ── Check: content completeness ──
    has_questions = sum(1 for r in reviews if r.get("questions") and len(r["questions"]) > 0)
    has_what_outputs = sum(1 for r in reviews if r.get("what_outputs"))
    has_find_bug = sum(1 for r in reviews if r.get("find_bug"))
    has_task = sum(1 for r in reviews if r.get("task"))
    has_dialogue = sum(1 for r in reviews if r.get("dialogue") and len(r["dialogue"]) > 0)

    # ── Results ──
    results = {
        "total_reviews": total_reviews,
        "total_lessons": len(lessons),
        "checks": {
            "max_gap_without_review": {
                "value": max_gap,
                "required": "<= 3",
                "passed": max_gap_ok,
            },
            "all_review_types_present": {
                "value": list(type_counts.keys()),
                "required": all_types,
                "passed": types_present,
            },
            "mixed_reviews": {
                "value": f"{mixed_reviews}/{total_with_topics} have ≥2 topics",
                "required": "≥80%",
                "passed": mixed_ok,
            },
            "content_completeness": {
                "with_questions": f"{has_questions}/{total_reviews}",
                "with_what_outputs": f"{has_what_outputs}/{total_reviews}",
                "with_find_bug": f"{has_find_bug}/{total_reviews}",
                "with_task": f"{has_task}/{total_reviews}",
                "with_dialogue": f"{has_dialogue}/{total_reviews}",
            },
        },
        "type_counts": type_counts,
        "proof": {
            "max_gap_without_review": max_gap,
            "mixed_reviews_present": mixed_ok,
            "chapter_reviews_present": "chapter_review" in type_counts,
            "boss_reviews_present": "boss_review" in type_counts,
            "part_reviews_present": "part_review" in type_counts,
        },
        "verdict": "PASSED" if (max_gap_ok and types_present and mixed_ok) else "FAILED",
    }

    # ── Print summary ──
    print(f"{'='*50}")
    print(f"  Review Schedule Verification")
    print(f"{'='*50}")
    print(f"  Max gap without review: {max_gap}{' ✅' if max_gap_ok else ' ❌'}")
    print(f"  All review types present: {'✅' if types_present else '❌'}")
    print(f"  Mixed reviews (>=2 topics): {mixed_reviews}/{total_with_topics}{' ✅' if mixed_ok else ' ❌'}")
    print()
    print(f"  Type counts:")
    for t in all_types:
        print(f"    {t}: {type_counts.get(t, 0)}")
    print()
    print(f"  Content:")
    print(f"    Questions:  {has_questions}/{total_reviews}")
    print(f"    What outputs: {has_what_outputs}/{total_reviews}")
    print(f"    Find bug:   {has_find_bug}/{total_reviews}")
    print(f"    Task:       {has_task}/{total_reviews}")
    print(f"    Dialogue:   {has_dialogue}/{total_reviews}")
    print()
    print(f"  Verdict: {results['verdict']}")
    print(f"{'='*50}\n")

    # ── Save report ──
    report_path = _PROJECT / "review_schedule_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  Report saved to {report_path.resolve()}")
    print()

    return 0 if results["verdict"] == "PASSED" else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
