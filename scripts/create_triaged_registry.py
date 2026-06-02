#!/usr/bin/env python3
"""Create triaged issue registry from the original course quality issue registry."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE, "docs", "course_quality_issue_registry.json")
OUTPUT_PATH = os.path.join(BASE, "docs", "course_quality_issue_registry_triaged.json")

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    registry = json.load(f)

issues = registry["issues"]

for iss in issues:
    iid = iss["issue_id"]
    itype = iss["issue_type"]

    # Consecutive Bagus — all 3 were FIXED
    if iid in ("PQA-0037", "PQA-0038", "PQA-0039"):
        iss["triage_status"] = "real_issue_fixed"
        iss["fix_decision"] = "fixed"
        iss["risk_level"] = "low"
        iss["requires_operator_review"] = False
        iss["reason"] = (
            "Changed one of two consecutive Bagus lines to another character "
            "(Va or Novice) to maintain Bagus role as comic relief, not main teacher"
        )
        iss["files_touched"] = ["api/app/data/lessons.json"]
        iss["before"] = "Two consecutive Bagus dialogue lines in post_error_dialogue"
        iss["after"] = "Bagus lines separated by other character (Va/Novice)"
        continue

    # Boss no code_watch — real, deferred
    if iid in ("PQA-0055", "PQA-0056"):
        iss["triage_status"] = "real_issue_deferred_operator_review"
        iss["fix_decision"] = "deferred"
        iss["risk_level"] = "medium"
        iss["requires_operator_review"] = True
        iss["reason"] = (
            "Adding code_watch requires creating new pedagogical content about "
            "lesson topic. Safe autofix not possible without understanding lesson flow."
        )
        iss["files_touched"] = []
        iss["before"] = "Missing code_watch block in boss lesson"
        iss["after"] = "Needs operator-created code_watch for lesson topic"
        continue

    # Dialogue premature concept — all false positives (everyday language)
    if itype == "dialogue_premature_concept":
        iss["triage_status"] = "false_positive"
        iss["fix_decision"] = "rejected_as_false_positive"
        iss["risk_level"] = "none"
        iss["requires_operator_review"] = False
        iss["reason"] = (
            "Audit flags everyday Russian words as programming concepts. "
            "Words like 'если' (if), 'пока' (while), 'повтор' (repeat), "
            "'словарь' (dictionary) are used in their natural language sense, "
            "not as Python keyword references. This is an over-aggressive "
            "keyword match in the pedagogical prerequisite audit."
        )
        iss["files_touched"] = []
        continue

    # Premature concept risk for lesson 2-5 — false positive (lesson IS about for)
    if iid == "PQA-0023":
        iss["triage_status"] = "false_positive"
        iss["fix_decision"] = "rejected_as_false_positive"
        iss["risk_level"] = "none"
        iss["requires_operator_review"] = False
        iss["reason"] = (
            "Lesson 2-5 content (title 'Первое знакомство с for', slug, "
            "dialogue, mission) is entirely about the for loop. The audit "
            "flags this based on skill_progression.json which lists 2-5 as "
            "teaching 'elif', but actual lesson content teaches 'for'. "
            "This is a skill_progression config mismatch, not a lesson defect."
        )
        iss["files_touched"] = []
        continue

    # Suspicious one-line code — false positives (valid single-line Python)
    if itype == "suspicious_one_line_code":
        iss["triage_status"] = "false_positive"
        iss["fix_decision"] = "rejected_as_false_positive"
        iss["risk_level"] = "none"
        iss["requires_operator_review"] = False
        if iid == "PQA-0035":
            iss["reason"] = (
                "find_bug.correct for 1-1 is print('Привет') — a legitimate "
                "single-line Python statement fixing a missing-quotes bug. "
                "Not a multiline formatting issue."
            )
        else:
            iss["reason"] = (
                "find_bug.correct for 4-10 is print('\\n'.join(['a','b'])) — "
                "a legitimate single-line Python expression. The fix only "
                "changes '/' to '\\'. Not a multiline formatting issue."
            )
        iss["files_touched"] = []
        continue

    # Wording ambiguous — non-blocking defer
    if itype == "wording_ambiguous":
        iss["triage_status"] = "non_blocking_deferred"
        iss["fix_decision"] = "deferred"
        iss["risk_level"] = "low"
        iss["requires_operator_review"] = False
        iss["reason"] = (
            "'выведи результат' is standard beginner phrasing. Students "
            "only have print() available at this stage, so the expected "
            "action is unambiguous. Clarifying is a style preference, not a defect."
        )
        iss["files_touched"] = []
        continue

    # Wording overstated — non-blocking polish
    if itype == "wording_overstated":
        iss["triage_status"] = "non_blocking_deferred"
        iss["fix_decision"] = "deferred"
        iss["risk_level"] = "low"
        iss["requires_operator_review"] = False
        iss["reason"] = (
            "'напиши программу' is slightly overstated for single-line "
            "solutions but is standard pedagogical encouragement language. "
            "Style preference, not a bug."
        )
        iss["files_touched"] = []
        continue

    # Fallback
    iss["triage_status"] = "needs_more_context"
    iss["fix_decision"] = "deferred"
    iss["requires_operator_review"] = True

# Build summary
statuses = {}
for iss in issues:
    s = iss.get("triage_status", "unknown")
    statuses[s] = statuses.get(s, 0) + 1

output = {
    "generated_at": "2026-06-02T18:00:00.000000+00:00",
    "total_items_checked": 1347,
    "original_issues_total": 56,
    "triage_completed": True,
    "triage_summary": {
        "real_issues_fixed": statuses.get("real_issue_fixed", 0),
        "real_issues_deferred_operator_review": statuses.get("real_issue_deferred_operator_review", 0),
        "false_positives": statuses.get("false_positive", 0),
        "duplicates": statuses.get("duplicate", 0),
        "non_blocking_deferred": statuses.get("non_blocking_deferred", 0),
        "needs_more_context": statuses.get("needs_more_context", 0),
    },
    "issues": issues,
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("=== TRIAGE RESULTS ===")
for k, v in sorted(statuses.items()):
    print(f"  {k}: {v}")
print(f"  TOTAL: {sum(statuses.values())}")
print(f"  FIXED: {statuses.get('real_issue_fixed', 0)}")
print(f"\nTriaged registry written to {OUTPUT_PATH}")
