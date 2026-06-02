#!/usr/bin/env python3
"""
Course Data Dialogue Integrity Audit

Checks all course data sources for malformed entries that could crash the frontend:
  - Dialogue steps (pre_topic_dialogue, post_error_dialogue, code_watch.dialogue, etc.)
    missing 'text' or 'character'/'speaker'
  - code_watch blocks missing required fields
  - analogy blocks missing required fields
  - Empty/null strings where UI expects content
  - Malformed character values
  - WalkthroughStep missing optional-but-common fields

Usage: python scripts/audit_dialogue_integrity.py
Output: audit results printed to stdout, summary at end
"""

import json
import sys
import os
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_PATH = os.path.join(BASE, "backend", "app", "data", "lessons.json")
RECAPS_PATH = os.path.join(BASE, "backend", "app", "data", "recaps.json")
QUESTS_PATH = os.path.join(BASE, "backend", "app", "data", "quests.json")
CHAPTER_QUESTS_PATH = os.path.join(BASE, "backend", "app", "data", "chapter_quests.json")
REVIEW_SCHEDULE_PATH = os.path.join(BASE, "api", "app", "data", "review_schedule.json")
DIALOGUES_PART2_PATH = os.path.join(BASE, "api", "app", "data", "dialogues_part2.json")

VALID_CHARACTERS = {"ksyu", "va", "da", "bagus", "novice"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_nonempty_str(val: Any) -> bool:
    """True if val is a str with at least one non-whitespace char."""
    return isinstance(val, str) and len(val.strip()) > 0


def is_valid_character(val: Any) -> bool:
    return isinstance(val, str) and val in VALID_CHARACTERS


def fmt_loc(lesson_id: str, block: str, idx: int | None = None) -> str:
    parts = [f"lesson={lesson_id}", f"block={block}"]
    if idx is not None:
        parts.append(f"idx={idx}")
    return "[" + " ".join(parts) + "]"


# ---------------------------------------------------------------------------
# Findings collector
# ---------------------------------------------------------------------------

class Findings:
    def __init__(self):
        self.errors: list[str] = []       # Must-fix issues (will break render)
        self.warnings: list[str] = []     # Should-fix (bad practice, risky)
        self.info: list[str] = []         # Observations

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def note(self, msg: str):
        self.info.append(msg)

    def print_report(self):
        print(f"\n{'='*70}")
        print(f"COURSE DATA DIALOGUE INTEGRITY AUDIT REPORT")
        print(f"{'='*70}")
        if self.errors:
            print(f"\n  ERRORS ({len(self.errors)}):")
            for e in self.errors:
                print(f"    [ERROR]  {e}")
        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"    [WARN]   {w}")
        if self.info:
            print(f"\n  INFO ({len(self.info)}):")
            for i in self.info:
                print(f"    [INFO]   {i}")
        print(f"\n  Summary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info items")


# ===================================================================
# Check: dialogue step list
# ===================================================================

def check_dialogue_list(
    steps: list[Any],
    loc_label: str,
    findings: Findings,
    *,
    text_field: str = "text",
    speaker_field: str = "character",
):
    """Validate a list of DialogueLine-like objects."""
    if not isinstance(steps, list):
        findings.error(f"{loc_label}: expected a list, got {type(steps).__name__}")
        return
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            findings.error(f"{loc_label}[{i}]: step is not a dict (got {type(step).__name__})")
            continue

        # Check speaker/character
        speaker = step.get(speaker_field)
        if not is_valid_character(speaker):
            findings.error(
                f"{loc_label}[{i}]: missing or invalid {speaker_field}="
                f"{repr(speaker)}"
            )

        # Check text
        text = step.get(text_field)
        if not is_nonempty_str(text):
            if text_field not in step:
                findings.error(
                    f"{loc_label}[{i}]: missing '{text_field}' field "
                    f"(keys={list(step.keys())})"
                )
            else:
                findings.error(
                    f"{loc_label}[{i}]: '{text_field}' is empty or not a string "
                    f"(type={type(text).__name__}, value={repr(text)[:80]})"
                )


# ===================================================================
# Check: WalkthroughStep (code_watch dialogue)
# ===================================================================

def check_walkthrough_steps(
    steps: list[Any],
    loc_label: str,
    findings: Findings,
):
    """Validate a list of WalkthroughStep objects (code_watch dialogue)."""
    if not isinstance(steps, list):
        findings.error(f"{loc_label}.dialogue: expected a list, got {type(steps).__name__}")
        return
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            findings.error(f"{loc_label}.dialogue[{i}]: step is not a dict")
            continue

        # speaker is required
        speaker = step.get("speaker")
        if not is_valid_character(speaker):
            findings.error(
                f"{loc_label}.dialogue[{i}]: missing or invalid speaker="
                f"{repr(speaker)}"
            )

        # text is required
        text = step.get("text")
        if not is_nonempty_str(text):
            if "text" not in step:
                findings.error(
                    f"{loc_label}.dialogue[{i}]: missing 'text' field "
                    f"(keys={list(step.keys())})"
                )
            else:
                findings.error(
                    f"{loc_label}.dialogue[{i}]: 'text' is empty or not a string "
                    f"(type={type(text).__name__}, value={repr(text)[:80]})"
                )

        # code and output are optional but warn if they're set to empty string
        for opt_field in ("code", "output", "caption"):
            val = step.get(opt_field)
            if opt_field in step and val is not None and not is_nonempty_str(val):
                findings.warn(
                    f"{loc_label}.dialogue[{i}]: optional field '{opt_field}' is "
                    f"present but empty (value={repr(val)[:80]})"
                )


# ===================================================================
# Check: code_watch block
# ===================================================================

def check_code_watch_block(
    cw: Any,
    loc_label: str,
    findings: Findings,
):
    """Validate a CodeWalkthrough object."""
    if not isinstance(cw, dict):
        findings.error(f"{loc_label}: code_watch is not a dict")
        return

    # Required fields
    for field in ("title", "main_code", "dialogue"):
        val = cw.get(field)
        if field == "dialogue":
            if not isinstance(val, list):
                findings.error(f"{loc_label}: missing or invalid '{field}'")
                continue
            check_walkthrough_steps(val, loc_label, findings)
        elif not is_nonempty_str(val):
            findings.error(
                f"{loc_label}: missing or empty required field '{field}'"
            )

    # Optional fields
    for opt_field in ("what_if", "solutions"):
        val = cw.get(opt_field)
        if val is not None and not isinstance(val, list):
            findings.warn(
                f"{loc_label}: optional field '{opt_field}' is not a list "
                f"(got {type(val).__name__})"
            )


# ===================================================================
# Check: analogy block
# ===================================================================

def check_analogy_block(
    analogy: Any,
    loc_label: str,
    findings: Findings,
):
    """Validate an analogy block."""
    if not isinstance(analogy, dict):
        findings.error(f"{loc_label}: analogy is not a dict")
        return

    for field in ("title", "story_metaphor", "python_mapping", "key_rule"):
        val = analogy.get(field)
        if not is_nonempty_str(val):
            findings.error(
                f"{loc_label}: missing or empty required field '{field}'"
            )


# ===================================================================
# Check: foundation block
# ===================================================================

def check_foundation_block(
    fb: Any,
    loc_label: str,
    findings: Findings,
):
    """Validate a FoundationBlock."""
    if not isinstance(fb, dict):
        findings.error(f"{loc_label}: foundation is not a dict")
        return
    if not is_nonempty_str(fb.get("title", "")):
        findings.error(f"{loc_label}: foundation missing or empty 'title'")


# ===================================================================
# Check: what_outputs & find_bug blocks
# ===================================================================

def check_lesson_blocks(lesson: dict, findings: Findings):
    """Check what_outputs, find_bug, quiz, mission blocks for required fields."""
    lid = lesson.get("id", "???")

    # what_outputs
    wo = lesson.get("what_outputs", {})
    if isinstance(wo, dict):
        for f in ("code", "options", "correct"):
            if f not in wo:
                findings.error(f"[lesson={lid}] what_outputs: missing '{f}'")
        if isinstance(wo.get("options"), list) and len(wo["options"]) < 2:
            findings.warn(f"[lesson={lid}] what_outputs: fewer than 2 options ({len(wo['options'])})")

    # find_bug
    fb = lesson.get("find_bug", {})
    if isinstance(fb, dict):
        for f in ("description", "code", "hint"):
            if not is_nonempty_str(fb.get(f, "")):
                findings.warn(f"[lesson={lid}] find_bug: missing or empty '{f}'")

    # quiz
    qz = lesson.get("quiz", {})
    if isinstance(qz, dict):
        if not is_nonempty_str(qz.get("question", "")):
            findings.error(f"[lesson={lid}] quiz: missing or empty 'question'")
        options = qz.get("options", [])
        if not isinstance(options, list) or len(options) < 2:
            findings.error(f"[lesson={lid}] quiz: fewer than 2 options")

    # mission
    ms = lesson.get("mission", {})
    if isinstance(ms, dict):
        for f in ("title", "description", "task", "expected_output", "character"):
            if not is_nonempty_str(ms.get(f, "")) and f != "character":
                findings.warn(f"[lesson={lid}] mission: missing or empty '{f}'")
            elif f == "character" and not is_valid_character(ms.get(f)):
                findings.error(f"[lesson={lid}] mission: missing or invalid 'character'")


# ===================================================================
# Main audit
# ===================================================================

def main():
    findings = Findings()

    # ---- Lessons ----
    print("Checking lessons.json ...", end=" ", flush=True)
    try:
        with open(LESSONS_PATH, encoding="utf-8") as f:
            lessons = json.load(f)
    except Exception as e:
        findings.error(f"Cannot read lessons.json: {e}")
        lessons = []
    print(f"{len(lessons)} lessons loaded.")

    for lesson in lessons:
        lid = lesson.get("id", "???") or lesson.get("slug", "???")
        if not isinstance(lesson, dict):
            findings.error(f"[lesson={lid}]: lesson is not a dict")
            continue

        # --- Dialogue blocks ---
        for block_name in ("pre_topic_dialogue", "post_error_dialogue"):
            dialogue = lesson.get(block_name)
            if dialogue is not None:
                loc = f"[lesson={lid}] {block_name}"
                check_dialogue_list(dialogue, loc, findings)

        # --- code_watch block (lessons 1-8, 1-9, 2-1) ---
        cw = lesson.get("code_watch")
        if cw is not None:
            check_code_watch_block(cw, f"[lesson={lid}] code_watch", findings)

        # --- analogy block ---
        analogy = lesson.get("analogy")
        if analogy is not None:
            check_analogy_block(analogy, f"[lesson={lid}] analogy", findings)

        # --- foundation block ---
        fb = lesson.get("foundation")
        if fb is not None:
            check_foundation_block(fb, f"[lesson={lid}] foundation", findings)

        # --- what_outputs / find_bug / quiz / mission ---
        check_lesson_blocks(lesson, findings)

        # --- connection_to_game / mini_summary (optional but should not be empty if present) ---
        for opt_field in ("connection_to_game", "mini_summary", "story_placement", "game_relevance"):
            val = lesson.get(opt_field)
            if val is not None and not is_nonempty_str(val):
                findings.warn(
                    f"[lesson={lid}] {opt_field}: present but empty"
                )

        # --- Lesson metadata sanity ---
        for meta_field in ("part", "chapter", "lesson", "slug", "title", "topic", "difficulty"):
            if meta_field not in lesson:
                findings.error(f"[lesson={lid}]: missing metadata field '{meta_field}'")

    # ---- Recaps ----
    print("Checking recaps.json ...", end=" ", flush=True)
    try:
        with open(RECAPS_PATH, encoding="utf-8") as f:
            recaps = json.load(f)
    except Exception as e:
        findings.error(f"Cannot read recaps.json: {e}")
        recaps = []
    print(f"{len(recaps)} recaps loaded.")

    for recap in recaps:
        rid = recap.get("id", "???")
        if not isinstance(recap, dict):
            findings.error(f"[recap={rid}]: not a dict")
            continue

        # Recaps don't have dialogue blocks directly, but check story_summary and title
        if not is_nonempty_str(recap.get("title", "")):
            findings.error(f"[recap={rid}]: missing or empty 'title'")
        if not is_nonempty_str(recap.get("story_summary", "")):
            findings.error(f"[recap={rid}]: missing or empty 'story_summary'")

        # Check hero_skills
        hs = recap.get("hero_skills", [])
        if isinstance(hs, list):
            for i, skill in enumerate(hs):
                if not isinstance(skill, dict):
                    findings.error(f"[recap={rid}] hero_skills[{i}]: not a dict")
                    continue
                for f in ("name", "python", "meaning", "analogy"):
                    if not is_nonempty_str(skill.get(f, "")):
                        findings.warn(f"[recap={rid}] hero_skills[{i}]: missing or empty '{f}'")
        else:
            findings.warn(f"[recap={rid}]: hero_skills is not a list")

    # ---- Quests ----
    print("Checking quests.json ...", end=" ", flush=True)
    try:
        with open(QUESTS_PATH, encoding="utf-8") as f:
            quests = json.load(f)
    except Exception as e:
        findings.error(f"Cannot read quests.json: {e}")
        quests = []
    print(f"{len(quests)} quests loaded.")

    for quest in quests:
        qid = quest.get("id", "???")
        if not isinstance(quest, dict):
            findings.error(f"[quest={qid}]: not a dict")
            continue
        for f in ("title", "story", "task", "starter_code"):
            if not is_nonempty_str(quest.get(f, "")):
                findings.warn(f"[quest={qid}]: missing or empty '{f}'")

        # Check test_cases
        tcs = quest.get("test_cases", [])
        if isinstance(tcs, list):
            for i, tc in enumerate(tcs):
                if not isinstance(tc, dict):
                    continue
                has_input = is_nonempty_str(tc.get("input", ""))
                has_expected = isinstance(tc.get("expected_contains"), list) and len(tc["expected_contains"]) > 0
                if not has_input and not has_expected:
                    findings.warn(f"[quest={qid}] test_cases[{i}]: both 'input' and 'expected_contains' are empty")

    # ---- Chapter Quests ----
    print("Checking chapter_quests.json ...", end=" ", flush=True)
    try:
        with open(CHAPTER_QUESTS_PATH, encoding="utf-8") as f:
            cquests = json.load(f)
    except Exception as e:
        findings.error(f"Cannot read chapter_quests.json: {e}")
        cquests = []
    print(f"{len(cquests)} chapter quests loaded.")
    # Same structure as quests
    for quest in cquests:
        qid = quest.get("id", "???")
        if not isinstance(quest, dict):
            findings.error(f"[chapter_quest={qid}]: not a dict")
            continue
        for f in ("title", "story", "task", "starter_code"):
            if not is_nonempty_str(quest.get(f, "")):
                findings.warn(f"[chapter_quest={qid}]: missing or empty '{f}'")

    # ---- Review Schedule ----
    print("Checking review_schedule.json ...", end=" ", flush=True)
    try:
        with open(REVIEW_SCHEDULE_PATH, encoding="utf-8") as f:
            review_data = json.load(f)
    except Exception as e:
        findings.error(f"Cannot read review_schedule.json: {e}")
        review_data = {}
    # review_schedule.json wraps reviews in { total_reviews, max_gap_without_review, type_counts, reviews: [...] }
    reviews_list = review_data.get("reviews", []) if isinstance(review_data, dict) else []
    print(f"{len(reviews_list)} reviews loaded.")
    if not isinstance(review_data, dict):
        findings.error("review_schedule.json: top-level is not a dict")

    for review_idx, review in enumerate(reviews_list):
        if not isinstance(review, dict):
            findings.error(f"[review idx={review_idx}]: not a dict (got {type(review).__name__})")
            continue
        rid = review.get("id", f"idx={review_idx}")

        # Dialogue in reviews is optional, but if present, check it
        dialogue = review.get("dialogue")
        if dialogue is not None:
            loc = f"[review={rid}] dialogue"
            check_dialogue_list(dialogue, loc, findings)

    # ---- Dialogues Part 2 ----
    print("Checking dialogues_part2.json ...", end=" ", flush=True)
    try:
        with open(DIALOGUES_PART2_PATH, encoding="utf-8") as f:
            d2 = json.load(f)
    except Exception as e:
        findings.error(f"Cannot read dialogues_part2.json: {e}")
        d2 = {}
    if isinstance(d2, dict):
        print(f"{len(d2)} lesson entries loaded.")
        for lesson_key, dialogue_list in d2.items():
            loc = f"[dialogues_part2] {lesson_key}"
            check_dialogue_list(dialogue_list, loc, findings)
    else:
        print("not a dict.")

    # ---- Summary ----
    findings.print_report()

    # ---- Export machine-readable ----
    result = {
        "errors_count": len(findings.errors),
        "warnings_count": len(findings.warnings),
        "info_count": len(findings.info),
        "errors": findings.errors,
        "warnings": findings.warnings,
        "info": findings.info,
    }
    out_path = os.path.join(BASE, "scripts", "audit_dialogue_integrity_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nMachine-readable results written to {out_path}")

    return len(findings.errors)


if __name__ == "__main__":
    sys.exit(main())
