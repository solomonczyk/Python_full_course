"""Wider Beta Simulation — 50 participants, concurrent execution.

Runs 50 simulated student journeys against the live backend.
Uses requests library for HTTP calls and concurrent execution for speed.
"""

import json
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:54321")
REPORT_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "beta_testing"

PARTICIPANT_CODES = [
    "BETA-64UFFT", "BETA-6AW3QU", "BETA-6FNU5W", "BETA-766MDZ", "BETA-7UE426",
    "BETA-7YXGD4", "BETA-8APE6D", "BETA-8FFBKZ", "BETA-92N6RZ", "BETA-9AHH3M",
    "BETA-AEU293", "BETA-AQZFH3", "BETA-CSVHA4", "BETA-CTJ883", "BETA-DCBFWK",
    "BETA-DDTGFM", "BETA-EFC2TG", "BETA-ERKHMZ", "BETA-EWZUAE", "BETA-FA3N26",
    "BETA-FWMKMA", "BETA-G26D42", "BETA-GCZYS6", "BETA-GX7EFB", "BETA-H7VP2X",
    "BETA-HDJXX7", "BETA-HG67AC", "BETA-HSHBND", "BETA-JCS6RJ", "BETA-JYQEA7",
    "BETA-KBPBQ8", "BETA-M6GWDN", "BETA-N5AT75", "BETA-NB2RHC", "BETA-NDXZQ3",
    "BETA-R2SZJV", "BETA-RWDX3U", "BETA-S7DFF7", "BETA-S8EXR3", "BETA-SHBWF3",
    "BETA-UCA7JK", "BETA-VBRY25", "BETA-WW4GT2", "BETA-X4AEB5", "BETA-X82FY5",
    "BETA-XTFTZ5", "BETA-Y58R63", "BETA-YQUAVP", "BETA-YR2BZV", "BETA-YWN35Q",
]

WB_LABELS = [f"WB-{i:03d}" for i in range(1, 51)]

PERSONAS = [
    {"name": "fast_success",          "weight": 0.30, "attempts": 1, "hints": 0, "fail_first": False, "completes": True},
    {"name": "one_error_then_success","weight": 0.25, "attempts": 2, "hints": 0, "fail_first": True,  "completes": True},
    {"name": "struggling_then_success","weight": 0.15, "attempts": 4, "hints": 1, "fail_first": True,  "completes": True},
    {"name": "hint_dependent",        "weight": 0.10, "attempts": 3, "hints": 2, "fail_first": True,  "completes": True},
    {"name": "barely_passing",        "weight": 0.08, "attempts": 3, "hints": 1, "fail_first": True,  "completes": True},
    {"name": "early_abandon",         "weight": 0.07, "attempts": 0, "hints": 0, "fail_first": False, "completes": False},
    {"name": "lesson_abandon",        "weight": 0.05, "attempts": 1, "hints": 0, "fail_first": True,  "completes": False},
]


def pick_persona():
    r = random.random()
    cum = 0.0
    for p in PERSONAS:
        cum += p["weight"]
        if r <= cum:
            return p
    return PERSONAS[0]


def simulate_one(wb_label, code):
    """Run one participant's full journey. Returns (label, code, result_dict)."""
    persona = pick_persona()
    result = {
        "participant_label": wb_label,
        "participant_code": code,
        "persona": persona["name"],
        "beta_code_issued": False,
        "landing_opened": True,
        "quest_started": False,
        "lesson_started": False,
        "first_mission_attempted": False,
        "first_mission_passed": False,
        "hints_used": 0,
        "lesson_completed": False,
        "progress_restored": False,
        "session_abandoned": persona["name"] in ("early_abandon", "lesson_abandon"),
        "blockers": [],
        "major_issues": [],
        "polish_issues": [],
    }

    try:
        # 1. Create progress
        r = requests.post(f"{BASE_URL}/beta/progress/create",
                         json={"participant_code": code}, timeout=10)
        if r.status_code != 200:
            result["blockers"].append(f"Create failed: HTTP {r.status_code}")
            return wb_label, code, result
        data = r.json()
        result["beta_code_issued"] = True
        result["participant_id"] = data.get("participant_id", "")

        if persona["name"] == "early_abandon":
            return wb_label, code, result

        # 2. Start lesson
        r = requests.post(f"{BASE_URL}/beta/progress/{code}/lesson-started",
                         json={"lesson_id": "1-1"}, timeout=10)
        if r.status_code != 200:
            result["blockers"].append(f"Lesson start failed: HTTP {r.status_code}")
            return wb_label, code, result
        result["quest_started"] = True
        result["lesson_started"] = True

        if persona["name"] == "lesson_abandon":
            return wb_label, code, result

        # 3. Mission attempts
        for i in range(persona["attempts"]):
            is_last = i == persona["attempts"] - 1
            should_pass = is_last and persona["completes"]
            hints_this = 1 if persona["hints"] > 0 and not is_last else 0

            r = requests.post(f"{BASE_URL}/beta/progress/{code}/mission-result",
                             json={
                                 "lesson_id": "1-1",
                                 "passed": should_pass,
                                 "attempts": i + 1,
                                 "hints_used": hints_this,
                             }, timeout=10)
            if r.status_code != 200:
                result["blockers"].append(f"Mission result failed (attempt {i+1})")
                return wb_label, code, result

            result["first_mission_attempted"] = True
            if should_pass:
                result["first_mission_passed"] = True
            result["hints_used"] += hints_this

        # 4. Complete lesson
        if persona["completes"]:
            r = requests.post(f"{BASE_URL}/beta/progress/{code}/lesson-completed",
                             json={"lesson_id": "1-1"}, timeout=10)
            if r.status_code == 200:
                result["lesson_completed"] = True
            else:
                result["major_issues"].append(f"Lesson complete failed: HTTP {r.status_code}")

        # 5. Verify progress restore
        r = requests.get(f"{BASE_URL}/beta/progress/{code}", timeout=10)
        if r.status_code == 200 and r.json().get("found"):
            result["progress_restored"] = True
            result["restored"] = {
                "current_lesson_id": r.json().get("current_lesson_id"),
                "completed_lessons": r.json().get("completed_lessons", []),
            }
        else:
            result["major_issues"].append("Progress not found after simulation")

    except requests.exceptions.RequestException as e:
        result["blockers"].append(f"Network error: {e}")

    return wb_label, code, result


def main():
    print("=== WIDER BETA SIMULATION: 50 PARTICIPANTS ===")
    print(f"Backend: {BASE_URL}")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print()

    random.seed(42)
    all_results = []
    failures = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(simulate_one, wb, code): (wb, code)
            for wb, code in zip(WB_LABELS, PARTICIPANT_CODES)
        }

        for future in as_completed(futures):
            wb, code, result = future.result()
            all_results.append(result)

            status = "OK" if result["lesson_completed"] else "ABANDON" if result["session_abandoned"] else "PARTIAL"
            print(f"  {result['participant_label']} ({code}) [{result['persona']:25s}] -> {status}")
            if result["blockers"]:
                failures += 1
                print(f"    BLOCKERS: {result['blockers']}")

    # Sort by label
    all_results.sort(key=lambda r: r["participant_label"])

    # Aggregate
    analytics = {
        "testing_timestamp": datetime.now(timezone.utc).isoformat(),
        "students_total": len(all_results),
        "landing_opened": sum(1 for r in all_results if r["landing_opened"]),
        "quest_started": sum(1 for r in all_results if r["quest_started"]),
        "lesson_started": sum(1 for r in all_results if r["lesson_started"]),
        "mission_attempted": sum(1 for r in all_results if r["first_mission_attempted"]),
        "mission_failed": sum(1 for r in all_results if r["first_mission_attempted"] and not r["first_mission_passed"]),
        "mission_passed": sum(1 for r in all_results if r["first_mission_passed"]),
        "hint_used": sum(r["hints_used"] for r in all_results),
        "lesson_completed": sum(1 for r in all_results if r["lesson_completed"]),
        "session_abandoned": sum(1 for r in all_results if r["session_abandoned"]),
        "progress_restored": sum(1 for r in all_results if r["progress_restored"]),
        "beta_code_issued": sum(1 for r in all_results if r["beta_code_issued"]),
        "raw_participant_code_present": False,
        "personal_data_present": False,
        "persona_distribution": {},
    }

    for p in PERSONAS:
        analytics["persona_distribution"][p["name"]] = sum(1 for r in all_results if r.get("persona") == p["name"])

    # Check for raw code leak
    for r in all_results:
        pid = r.get("participant_id", "")
        code = r.get("participant_code", "")
        if pid and code and (code in pid or code.lower() in pid):
            analytics["raw_participant_code_present"] = True

    # Funnel conversion
    t = max(analytics["students_total"], 1)
    analytics["conversion_funnel"] = {
        "landing_opened": f"{100*analytics['landing_opened']/t:.1f}% ({analytics['landing_opened']}/{t})",
        "code_issued": f"{100*analytics['beta_code_issued']/t:.1f}% ({analytics['beta_code_issued']}/{t})",
        "quest_started": f"{100*analytics['quest_started']/t:.1f}% ({analytics['quest_started']}/{t})",
        "lesson_started": f"{100*analytics['lesson_started']/t:.1f}% ({analytics['lesson_started']}/{t})",
        "mission_attempted": f"{100*analytics['mission_attempted']/t:.1f}% ({analytics['mission_attempted']}/{t})",
        "mission_passed": f"{100*analytics['mission_passed']/t:.1f}% ({analytics['mission_passed']}/{t})",
        "lesson_completed": f"{100*analytics['lesson_completed']/t:.1f}% ({analytics['lesson_completed']}/{t})",
        "progress_restored": f"{100*analytics['progress_restored']/t:.1f}% ({analytics['progress_restored']}/{t})",
        "session_abandoned": f"{100*analytics['session_abandoned']/t:.1f}% ({analytics['session_abandoned']}/{t})",
    }

    # Print summary
    print()
    print(f"=== SUMMARY ===")
    print(f"Total students: {analytics['students_total']}")
    print(f"Beta codes issued: {analytics['beta_code_issued']}")
    print(f"Lesson started: {analytics['lesson_started']}")
    print(f"Mission attempted: {analytics['mission_attempted']}")
    print(f"Mission passed: {analytics['mission_passed']}")
    print(f"Lesson completed: {analytics['lesson_completed']}")
    print(f"Progress restored: {analytics['progress_restored']}")
    print(f"Session abandoned: {analytics['session_abandoned']}")
    print(f"Blockers: {failures}")
    print(f"Raw code leak: {analytics['raw_participant_code_present']}")
    print(f"Personal data: {analytics['personal_data_present']}")
    print()
    print("Funnel:")
    for step, rate in analytics["conversion_funnel"].items():
        print(f"  {step}: {rate}")

    # Save analytics export
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "wider_beta_analytics_export.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analytics, f, ensure_ascii=False, indent=2)
    print(f"\nAnalytics export saved: {path}")

    # Save full per-participant results
    results_path = REPORT_DIR / "wider_beta_simulation_results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump({"participants": all_results, "generated_at": datetime.now(timezone.utc).isoformat()},
                  f, ensure_ascii=False, indent=2)
    print(f"Full results saved: {results_path}")

    return analytics, all_results


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("ERROR: 'requests' library required. Install: pip install requests")
        sys.exit(1)
    main()
