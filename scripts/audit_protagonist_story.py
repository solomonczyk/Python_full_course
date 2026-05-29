"""
Audit Новичок protagonist integration.

Required:
- story_placement mentions Новичок 86/86
- pre_topic_dialogue has ≥2 Новичок lines 86/86
- post_error_dialogue has ≥2 Новичок lines 86/86
- No mentor-only dialogues (0 non-novice consecutive blocks > 3)
- No lecture-card dialogues
"""

import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent
_LESSONS_PATH = _PROJECT / "api" / "app" / "data" / "lessons.json"

NOVICE = "novice"
NOVICE_NAME = "Новичок"


def main() -> int:
    with open(_LESSONS_PATH, encoding="utf-8") as f:
        lessons = json.load(f)

    total = len(lessons)
    issues = []
    passed = []

    sp_ok = 0
    pre_2plus = 0
    post_2plus = 0
    mentor_only = 0
    lecture_card = 0

    for l in lessons:
        lid = l["id"]

        # ── story_placement ──
        sp = l.get("story_placement", "") or ""
        if NOVICE_NAME in sp:
            sp_ok += 1
        else:
            issues.append(f"{lid}: story_placement lacks {NOVICE_NAME}")

        # ── pre_topic_dialogue ──
        pre = l.get("pre_topic_dialogue") or []
        pre_novice = [d for d in pre if d.get("character") == NOVICE]
        if len(pre_novice) >= 2:
            pre_2plus += 1
        else:
            issues.append(f"{lid}: pre_topic has {len(pre_novice)} {NOVICE_NAME} lines (need ≥2)")

        # ── post_error_dialogue ──
        post = l.get("post_error_dialogue") or []
        post_novice = [d for d in post if d.get("character") == NOVICE]
        if len(post_novice) >= 2:
            post_2plus += 1
        else:
            issues.append(f"{lid}: post_error has {len(post_novice)} {NOVICE_NAME} lines (need ≥2)")

        # ── mentor-only dialogue check (3+ non-novice consecutive lines) ──
        for dlg_name, dlg in [("pre", pre), ("post", post)]:
            non_novice_run = 0
            for d in dlg:
                if d.get("character") != NOVICE and d.get("character") != "novice":
                    non_novice_run += 1
                    if non_novice_run >= 3:
                        mentor_only += 1
                        issues.append(f"{lid}: {dlg_name}_topic has {non_novice_run}+ mentor-only consecutive lines")
                        break
                else:
                    non_novice_run = 0

        # ── lecture-card check (no Новичок at all in dialogue) ──
        if not pre_novice and not post_novice:
            lecture_card += 1
            issues.append(f"{lid}: lecture-card dialogue (no {NOVICE_NAME} in either dialogue)")

    # Count total dialogue-bearing lessons
    pre_1plus = sum(1 for l in lessons if l.get("pre_topic_dialogue"))
    post_1plus = sum(1 for l in lessons if l.get("post_error_dialogue"))

    report = {
        "total_lessons": total,
        "checks": {
            "story_placement_with_protagonist": f"{sp_ok}/{total}",
            "pre_topic_dialogues_with_protagonist_2plus": f"{pre_2plus}/{total}",
            "post_error_dialogues_with_protagonist_2plus": f"{post_2plus}/{total}",
            "mentor_only_dialogues": mentor_only,
            "lecture_card_dialogues": lecture_card,
        },
        "canonical_protagonist": NOVICE_NAME,
        "issues": issues,
        "summary": {
            "story_placement_with_protagonist": sp_ok,
            "pre_topic_with_2plus_novice": pre_2plus,
            "post_error_with_2plus_novice": post_2plus,
            "mentor_only_violations": mentor_only,
            "lecture_card_violations": lecture_card,
        },
        "verdict": "ACCEPTED" if (sp_ok == total and pre_2plus == total and post_2plus == total and mentor_only == 0 and lecture_card == 0) else "NEEDS_FIXES",
    }

    print(f"\n{'='*50}")
    print(f"  Новичок Protagonist Story Audit")
    print(f"{'='*50}")
    print(f"  canonical_protagonist={NOVICE_NAME}")
    print(f"  story_placement_with_protagonist={sp_ok}/{total}")
    print(f"  pre_topic_dialogues_with_protagonist={pre_2plus}/{total}")
    print(f"  post_error_dialogues_with_protagonist={post_2plus}/{total}")
    print(f"  mentor_only_dialogues={mentor_only}")
    print(f"  lecture_card_dialogues={lecture_card}")
    print()
    for iss in issues[:10]:
        print(f"  ❌ {iss}")
    if len(issues) > 10:
        print(f"  ... and {len(issues) - 10} more issues")
    if not issues:
        print(f"  ✅ All checks passed!")
    print(f"\n  Verdict: {report['verdict']}")
    print(f"{'='*50}\n")

    report_path = _PROJECT / "protagonist_story_audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Report saved to {report_path.resolve()}\n")

    return 0 if report["verdict"] == "ACCEPTED" else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
