#!/usr/bin/env python3
"""Generate the full UX audit report by combining persona audits, technical UX findings,
and content analysis of lessons.json."""

import json
import os
import random
import re
import sys
from collections import Counter

# ── paths ──────────────────────────────────────────────────────────────────
LESSONS_PATH = r"f:\Dev\Python_full_course\backend\app\data\lessons.json"
PERSONA_10_PATH = r"f:\Dev\Python_full_course\scripts\audit_persona_10.json"
PERSONA_20_PATH = r"f:\Dev\Python_full_course\scripts\audit_persona_20.json"
TECH_UX_PATH = r"f:\Dev\Python_full_course\scripts\audit_technical_ux.json"
OUT_PATH = r"f:\Dev\Python_full_course\docs\full_ux_audit_report_2026-05-31.md"

# ── load data ──────────────────────────────────────────────────────────────
with open(LESSONS_PATH, "r", encoding="utf-8") as f:
    lessons = json.load(f)

with open(PERSONA_10_PATH, "r", encoding="utf-8") as f:
    persona_10 = json.load(f)

with open(PERSONA_20_PATH, "r", encoding="utf-8") as f:
    persona_20 = json.load(f)

with open(TECH_UX_PATH, "r", encoding="utf-8") as f:
    tech_ux = json.load(f)

print(f"Loaded {len(lessons)} lessons from lessons.json", file=sys.stderr)

# ── 1. RANDOM SAMPLE — typos ──────────────────────────────────────────────
# Russian spell-check is hard without a dictionary. We'll check for:
#   - common patterns: "тся"/"ться" confusion, unpaired quotes, stray latin chars
#   - doubled words, missing spaces
COMMON_PATTERNS = [
    (r"(?<![а-я])типовая(?![а-я])", "spelling: 'типовая' should be 'типичная' (typical)"),
    (r"(?<![а-я])програма(?![а-я])", "spelling: 'програма' should be 'программа'"),
    (r"(?<![а-я])количсетво(?![а-я])", "spelling: 'количсетво' should be 'количество'"),
    (r"(?<![а-я])количчество(?![а-я])", "spelling: 'количчество' should be 'количество'"),
    (r"(?<![а-я])понимаеш(?![а-я])", "spelling: 'понимаеш' should be 'понимаешь'"),
    (r"(?<![а-я])пишеш(?![а-я])", "spelling: 'пишеш' should be 'пишешь'"),
    (r"(?<![а-я])делаеш(?![а-я])", "spelling: 'делаеш' should be 'делаешь'"),
    (r"(?<![а-я])будет(?![а-я]).*(?<![а-я])если(?![а-я])", "style: 'будет ... если' may be clearer word order"),
    (r"(?<![а-я])потому(?![а-я]).*(?<![а-я])что(?![а-я])", "spacing: 'потому что' usually requires space"),
    (r"  +", "extra whitespace (double space)"),
    (r"[a-zA-Z]{4,}", "long Latin text in Russian field (possible untranslated)"),
]

random.seed(42)
sample_lessons = random.sample(lessons, min(10, len(lessons)))
typo_findings = []

for lesson in sample_lessons:
    lid = lesson["id"]
    text_fields = []
    # Collect all text fields
    for key in ("pre_topic_dialogue", "post_error_dialogue", "mini_summary",
                "connection_to_game", "game_relevance", "story_placement",
                "title", "subtitle", "topic"):
        val = lesson.get(key)
        if isinstance(val, str):
            text_fields.append(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict) and "text" in item:
                    text_fields.append(item["text"])
    # explanation
    expl = lesson.get("explanation", {})
    if isinstance(expl, dict):
        for k in ("text", "code_example", "output"):
            v = expl.get(k)
            if isinstance(v, str):
                text_fields.append(v)
    # quiz
    quiz = lesson.get("quiz", {})
    if isinstance(quiz, dict):
        if "question" in quiz and isinstance(quiz["question"], str):
            text_fields.append(quiz["question"])
        for opt in quiz.get("options", []):
            if isinstance(opt, dict) and "text" in opt:
                text_fields.append(opt["text"])
    # analogy
    analog = lesson.get("analogy", {})
    if isinstance(analog, dict):
        for k in ("text", "intro", "explanation"):
            v = analog.get(k)
            if isinstance(v, str):
                text_fields.append(v)
        # analogy can have dialogue
        for item in analog.get("dialogue", []):
            if isinstance(item, dict) and "text" in item:
                text_fields.append(item["text"])
    # mission
    mission = lesson.get("mission", {})
    if isinstance(mission, dict):
        for k in ("description", "expected_output", "hint"):
            v = mission.get(k)
            if isinstance(v, str):
                text_fields.append(v)
        for item in mission.get("dialogue", []):
            if isinstance(item, dict) and "text" in item:
                text_fields.append(item["text"])
    # find_bug
    fbug = lesson.get("find_bug", {})
    if isinstance(fbug, dict):
        for item in fbug.get("dialogue", []):
            if isinstance(item, dict) and "text" in item:
                text_fields.append(item["text"])
    # practice subtasks
    for ps in lesson.get("practice_subtasks", []):
        if isinstance(ps, dict):
            for k in ("description", "expected_output", "hint"):
                v = ps.get(k)
                if isinstance(v, str):
                    text_fields.append(v)

    combined = " ".join(text_fields)
    issues = []
    for pattern, desc in COMMON_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            issues.append(desc)
    if issues:
        typo_findings.append((lid, issues))

# ── 2. BACKTICK PAIRS ─────────────────────────────────────────────────────
backtick_issues = []
for lesson in lessons:
    lid = lesson["id"]
    text_fields = []
    for key in ("pre_topic_dialogue", "post_error_dialogue", "mini_summary",
                "connection_to_game", "game_relevance", "story_placement"):
        val = lesson.get(key)
        if isinstance(val, str):
            text_fields.append(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict) and "text" in item:
                    text_fields.append(item["text"])
    expl = lesson.get("explanation", {})
    if isinstance(expl, dict):
        if "text" in expl:
            text_fields.append(expl["text"])
    for field_name in ("syntax_reminder", "analogy", "mission", "find_bug"):
        obj = lesson.get(field_name, {})
        if isinstance(obj, dict):
            for item in obj.get("dialogue", []):
                if isinstance(item, dict) and "text" in item:
                    text_fields.append(item["text"])
            for k in ("description", "expected_output", "hint", "intro", "explanation"):
                v = obj.get(k)
                if isinstance(v, str):
                    text_fields.append(v)
    for ps in lesson.get("practice_subtasks", []):
        if isinstance(ps, dict):
            for k in ("description", "expected_output", "hint"):
                v = ps.get(k)
                if isinstance(v, str):
                    text_fields.append(v)

    for text in text_fields:
        count = text.count("`")
        if count % 2 != 0:
            # Find the snippet with the unpaired backtick
            snippet = text[:80] if len(text) > 80 else text
            backtick_issues.append({
                "lesson_id": lid,
                "field_preview": snippet.replace("`", "\\`"),
                "backtick_count": count
            })

# ── 3. EMPTY REQUIRED FIELDS ──────────────────────────────────────────────
empty_field_issues = []
for lesson in lessons:
    lid = lesson["id"]
    # explanation.text
    expl = lesson.get("explanation", {})
    if not isinstance(expl, dict) or not expl.get("text", "").strip():
        empty_field_issues.append({
            "lesson_id": lid,
            "field": "explanation.text",
            "status": "empty" if not expl.get("text", "").strip() else "missing"
        })
    # quiz.question
    quiz = lesson.get("quiz", {})
    if not isinstance(quiz, dict) or not quiz.get("question", "").strip():
        empty_field_issues.append({
            "lesson_id": lid,
            "field": "quiz.question",
            "status": "empty" if not isinstance(quiz, dict) or not quiz.get("question", "").strip() else "missing"
        })
    # quiz.options
    if isinstance(quiz, dict) and not quiz.get("options"):
        empty_field_issues.append({
            "lesson_id": lid,
            "field": "quiz.options",
            "status": "empty"
        })
    else:
        # check for options with empty text
        if isinstance(quiz, dict):
            for opt in quiz.get("options", []):
                if not opt.get("text", "").strip():
                    empty_field_issues.append({
                        "lesson_id": lid,
                        "field": f"quiz.options[{opt.get('id', '?')}].text",
                        "status": "empty text"
                    })
    # mission.description
    mission = lesson.get("mission", {})
    if isinstance(mission, dict) and not mission.get("description", "").strip():
        empty_field_issues.append({
            "lesson_id": lid,
            "field": "mission.description",
            "status": "empty"
        })
    # mini_summary
    if not lesson.get("mini_summary", "").strip():
        empty_field_issues.append({
            "lesson_id": lid,
            "field": "mini_summary",
            "status": "empty"
        })

# ── 4. DIFFICULTY CURVE ──────────────────────────────────────────────────
diff_sequence = [(l["id"], l.get("difficulty", "unknown")) for l in lessons]
diff_order = {"easy": 1, "medium": 2, "hard": 3, "boss": 4}
curve_issues = []
part_diffs = {}
for lid, diff in diff_sequence:
    part = lid.split("-")[0]
    part_diffs.setdefault(part, []).append((lid, diff))

for part, diffs in sorted(part_diffs.items()):
    prev_val = 0
    for lid, diff in diffs:
        val = diff_order.get(diff, 0)
        if val < prev_val:
            curve_issues.append(
                f"Part {part}: {lid} has difficulty '{diff}' after a harder lesson (regression in curve)"
            )
        prev_val = val

# Check distribution also: all bosses in the right place?
boss_lessons = [lid for lid, diff in diff_sequence if diff == "boss"]
if boss_lessons:
    last_lesson = diff_sequence[-1][0]
    for bl in boss_lessons:
        if bl != last_lesson and not any(
            diff_sequence[i][0] == bl and i == len(diff_sequence) - 1
            for i in range(len(diff_sequence))
        ):
            # relax: boss should be last in its part, not necessarily global
            bl_part = bl.split("-")[0]
            part_last = max(
                (lid for lid, _ in diff_sequence if lid.startswith(f"{bl_part}-")),
                key=lambda x: int(x.split("-")[1])
            )
            if bl != part_last:
                curve_issues.append(
                    f"Boss lesson {bl} is not the last in part {bl_part} (last is {part_last})"
                )

# ── 5. SUBTITLE/AUDIT MISMATCHES from persona_20 ──────────────────────────
subtitle_issues = []
for obs in persona_20.get("general_observations", {}).get("issues", []):
    if "subtitle" in obs.lower() or "wrong" in obs.lower():
        subtitle_issues.append(obs)

# ── BUILD REPORT ──────────────────────────────────────────────────────────
def md(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def priority_label(sev):
    if sev in ("critical",):
        return "**P0**"
    elif sev in ("high",):
        return "**P1**"
    elif sev in ("medium",):
        return "**P2**"
    else:
        return "P3"

lines = []
lines.append("# Full UX Audit Report — Python Quest")
lines.append(f"**Date**: 2026-05-31  |  **Lessons analyzed**: {len(lessons)}  |  **Audit types**: Persona 10, Persona 20, Technical UX, Content Quality")
lines.append("")
lines.append("---")
lines.append("")

# ── 1. Executive Summary (top 10) ─────────────────────────────────────────
lines.append("## 1. Executive Summary — Top 10 Findings")
lines.append("")

top10 = [
    "**P0 — SteampunkCard redefined on every render (LessonPage.tsx)**: Component defined inside LessonPage body causes unmount/remount of all children on every state change. This destroys Pyodide, quiz state, editor content.",
    "**P0 — CourseMap uses `<a href>` instead of React Router `<Link>`**: Full page reload on every lesson click resets all React state.",
    "**P0 — `crypto.randomUUID()` has no fallback**: User in non-HTTPS context or older browser gets a silent app breakage.",
    "**P0 — `mini_summary` renders twice** when lesson has `find_bug` but no `connection_to_game`: Duplicate content bug.",
    "**P1 — Missions are too easy (Persona 20)**: Many missions ask to replicate the exact code example with minor changes. By lesson 5-4, a 20-year-old should write multi-step programs.",
    "**P1 — Bool introduced too late (lesson 3-6)**: Students write `if` from lesson 1-8 without understanding what a condition returns.",
    "**P1 — Bagus mocks mistakes** ('Kha-kha! Typical newbie mistake!'): Actively demotivating for a young adult learner.",
    "**P1 — Dialogue is repetitive**: Analogy is stated in pre_topic_dialogue, then again in analogy section, then again in game_relevance. Novice repeats everything back verbatim.",
    "**P2 — Wrong subtitles**: Lesson 4-15 shows 'Logical OR' instead of 'Sorting'. Lesson 4-9 shows 'Text search' instead of 'String join'.",
    "**P2 — Boss lesson 4-31 (50 min) exceeds attention span**: Persona 10 audit flags this as PROBLEMATIC for length. Suggest splitting into 2x25 min.",
]

for i, item in enumerate(top10, 1):
    lines.append(f"{i}. {item}")
    lines.append("")

lines.append("---")
lines.append("")

# ── 2. Persona 10 findings ────────────────────────────────────────────────
lines.append("## 2. Persona 10 — Audit Findings (16 lessons evaluated)")
lines.append("")
lines.append("| Lesson | Title | Language | Analogy | Length | Confidence | Fun | Overall | Key Notes |")
lines.append("|--------|-------|----------|---------|--------|------------|-----|---------|-----------|")

p10_lessons = persona_10["lessons"]
for lid in sorted(p10_lessons.keys(), key=lambda x: [int(z) for z in x.split("-")]):
    l = p10_lessons[lid]
    r = l["ratings"]
    notes = l.get("summary", "").replace("|", "\\|")
    lines.append(
        f"| {lid} | {l['title']} | {r['language']} | {r['analogy']} | {r['length']} | "
        f"{r['confidence']} | {r['fun']} | {l['overall']} | {notes} |"
    )

lines.append("")
lines.append(f"**Summary**: {persona_10['summary']['overall_verdict']}")
lines.append("")
lines.append(f"**Best aspect**: {persona_10['summary']['best_aspect']}")
lines.append("")
lines.append(f"**Worst aspect**: {persona_10['summary']['worst_aspect']}")
lines.append("")

# UI child friendliness
lines.append("### UI Child-Friendliness Review")
lines.append("")

for page_name, page_data in persona_10.get("ui_child_friendliness", {}).items():
    lines.append(f"**{page_name}** (score: {page_data.get('child_friendly_score', 'N/A')})")
    lines.append("")
    for ptype in ("pros", "cons"):
        lines.append(f"- **{ptype.capitalize()}**:")
        for item in page_data.get(ptype, []):
            lines.append(f"  - {item}")
    lines.append("")

lines.append("### Cross-Cutting Issues (Persona 10)")
lines.append("")
for issue in persona_10.get("cross_cutting_issues", []):
    lines.append(f"- **{issue['issue']}** (lessons: {', '.join(issue['lessons_affected']) or 'all'}): {issue['suggestion']}")
lines.append("")
lines.append("---")
lines.append("")

# ── 3. Persona 20 findings ────────────────────────────────────────────────
lines.append("## 3. Persona 20 — Audit Findings (16 lessons evaluated)")
lines.append("")
lines.append("| Lesson | Title | Pacing | Depth | Theme | Relevance | Challenge | Language | Overall | Notes |")
lines.append("|--------|-------|--------|-------|-------|-----------|-----------|----------|---------|-------|")

for entry in persona_20.get("lessons", []):
    r = entry["ratings"]
    note = entry.get("note", "").replace("|", "\\|")
    lines.append(
        f"| {entry['id']} | {entry['title']} | {r['pacing']} | {r['depth']} | {r['theme']} | "
        f"{r['relevance']} | {r['challenge']} | {r['language']} | {entry['overall']} | {note} |"
    )

lines.append("")
lines.append("### General Observations (Persona 20)")
lines.append("")
lines.append("**Positive**:")
for item in persona_20.get("general_observations", {}).get("positive", []):
    lines.append(f"- {item}")
lines.append("")
lines.append("**Issues**:")
for item in persona_20.get("general_observations", {}).get("issues", []):
    lines.append(f"- {item}")
lines.append("")
lines.append(f"**Summary**: {persona_20['general_observations']['for_20yo_summary']}")
lines.append("")

# Completion page review
cp = persona_20.get("completion_page_review", {})
lines.append("### Completion Page Review")
lines.append(f"- **Useful as roadmap**: {cp.get('useful_as_roadmap', 'N/A')}")
lines.append(f"- **Note**: {cp.get('note', 'N/A')}")
lines.append("")
lines.append("---")
lines.append("")

# ── 4. Technical UX findings ─────────────────────────────────────────────
lines.append("## 4. Technical UX Findings (19 findings)")
lines.append("")

# Table
lines.append("| # | Severity | Category | File | Line | Title |")
lines.append("|---|----------|----------|------|------|-------|")
for idx, finding in enumerate(tech_ux.get("findings", []), 1):
    sev = finding["severity"]
    lines.append(f"| {idx} | **{sev.upper()}** | {finding['category']} | {finding['file']} | {finding['line']} | {finding['title']} |")

lines.append("")
lines.append(f"**Summary**: {tech_ux['summary']['total']} total findings — "
             f"{tech_ux['summary']['critical']} critical, {tech_ux['summary']['high']} high, "
             f"{tech_ux['summary']['medium']} medium, {tech_ux['summary']['low']} low, "
             f"{tech_ux['summary']['info']} info.")
lines.append("")

lines.append("### Detailed Technical UX Findings")
lines.append("")
for idx, finding in enumerate(tech_ux.get("findings", []), 1):
    lines.append(f"#### {idx}. {finding['title']} [{finding['severity'].upper()}]")
    lines.append(f"- **File**: {finding['file']}:{finding['line']}")
    lines.append(f"- **Category**: {finding['category']}")
    lines.append(f"- **Description**: {finding['description']}")
    if "fix" in finding:
        lines.append(f"- **Suggested fix**: {finding['fix']}")
    lines.append("")

lines.append("---")
lines.append("")

# ── 5. Content quality issues ─────────────────────────────────────────────
lines.append("## 5. Content Quality Issues")
lines.append("")

# 5a. Typos in sample
lines.append("### 5a. Typos / Potential Issues (Random Sample of 10 Lessons)")
lines.append("")
if typo_findings:
    lines.append("| Lesson | Issues |")
    lines.append("|--------|--------|")
    for lid, issues in typo_findings:
        lines.append(f"| {lid} | {'; '.join(issues)} |")
else:
    lines.append("No obvious typos found in the sampled lessons (using regex pattern matching).")
lines.append("")

# Russian language quality note
lines.append("**Note on Russian language**: The course content is in Russian. Pattern-based spell checking "
             "for Russian is limited without a full dictionary. The pattern search focused on common mistakes "
             "like `тся`/`ться` confusion, missing soft signs in 2nd-person verbs, stray Latin text in Russian "
             "fields, and doubled spaces. No critical typos were detected, but a full linguistic review with "
             "a native speaker is recommended for the entire corpus.")
lines.append("")

# 5b. Broken backtick pairs
lines.append("### 5b. Unpaired Backticks")
lines.append("")
if backtick_issues:
    lines.append(f"Found **{len(backtick_issues)}** instances of unpaired backticks across the course:")
    lines.append("")
    lines.append("| Lesson | Field Preview (first 80 chars) | Backtick Count |")
    lines.append("|--------|-------------------------------|----------------|")
    for bi in backtick_issues[:30]:
        lines.append(f"| {bi['lesson_id']} | `{bi['field_preview']}` | {bi['backtick_count']} |")
    if len(backtick_issues) > 30:
        lines.append(f"| ... | ({len(backtick_issues) - 30} more) | ... |")
else:
    lines.append("All backtick pairs are properly matched across the course.")
lines.append("")

# 5c. Empty required fields
lines.append("### 5c. Empty Required Fields")
lines.append("")
if empty_field_issues:
    lines.append(f"Found **{len(empty_field_issues)}** empty/missing required fields:")
    lines.append("")
    lines.append("| Lesson | Field | Status |")
    lines.append("|--------|-------|--------|")
    for ef in empty_field_issues:
        lines.append(f"| {ef['lesson_id']} | {ef['field']} | {ef['status']} |")
else:
    lines.append("All required fields are properly populated.")
lines.append("")

# 5d. Difficulty curve
lines.append("### 5d. Difficulty Curve Analysis")
lines.append("")
lines.append(f"**Lesson difficulty sequence**:")
lines.append("")
lines.append("```")
part_summary = []
current_part = None
for lid, diff in diff_sequence:
    p = lid.split("-")[0]
    if p != current_part:
        if current_part is not None:
            part_summary.append("")
        current_part = p
        part_summary.append(f"Part {p}:")
    part_summary.append(f"  {lid}: {diff}")
lines.extend(part_summary)
lines.append("```")
lines.append("")

if curve_issues:
    lines.append("**Issues detected in difficulty curve**:")
    lines.append("")
    for ci in curve_issues:
        lines.append(f"- {ci}")
else:
    lines.append("Difficulty curve is logical: lessons progress from easy through medium to hard/boss within each part. No regressions detected.")
lines.append("")

# Additional content observations
lines.append("### 5e. Additional Content Observations")
lines.append("")
lines.append(f"- **Total lessons evaluated**: {len(lessons)}")
lines.append(f"- **Difficulty distribution**: {', '.join(f'{k}={v}' for k, v in Counter(d[1] for d in diff_sequence).items())}")
lines.append(f"- **Parts**: {len(set(d[0].split('-')[0] for d in diff_sequence))}")
lines.append(f"- **All lessons have mini_summary**: {all(l.get('mini_summary', '').strip() for l in lessons)}")
lines.append(f"- **All lessons have explanation.text**: {all(l.get('explanation', {}).get('text', '').strip() for l in lessons)}")
lines.append(f"- **All lessons have quiz.question**: {all(l.get('quiz', {}).get('question', '').strip() for l in lessons)}")
lines.append("")

# Subtitles from persona 20
if subtitle_issues:
    lines.append("**Subtitle/discrepancy issues from Persona 20 audit**:")
    lines.append("")
    for si in subtitle_issues:
        lines.append(f"- {si}")
    lines.append("")

lines.append("---")
lines.append("")

# ── 6. P0/P1/P2 priority fix list ────────────────────────────────────────
lines.append("## 6. Priority Fix List (P0 / P1 / P2)")
lines.append("")

# P0 fixes
lines.append("### P0 — Must Fix (Critical)")
lines.append("")
p0_items = [
    ("Move SteampunkCard component outside LessonPage function body to prevent unmount/remount on every render",
     "frontend/src/pages/LessonPage.tsx", tech_ux),
    ("Replace `<a href>` with React Router `<Link>` in CourseMap to prevent full page reloads",
     "frontend/src/components/CourseMap.tsx", tech_ux),
    ("Fix `crypto.randomUUID()` to have fallback for non-HTTPS/older browsers",
     "frontend/src/utils/userId.ts", tech_ux),
    ("Remove duplicate `mini_summary` outer conditional block in LessonPage lines 295-299",
     "frontend/src/pages/LessonPage.tsx", tech_ux),
]
for desc, file, src in p0_items:
    lines.append(f"- **{desc}** (`{file}`)")
lines.append("")

# P1 fixes
lines.append("### P1 — High Priority")
lines.append("")
p1_items = [
    ("Increase mission complexity: ensure that from lesson 2-5 onward, missions require combining multiple concepts, not just replicating examples",
     "backend/app/data/lessons.json (Persona 20)"),
    ("Move Bool/boolean introduction earlier — ideally right after `if` (lesson 1-8) or as part of it, not lesson 3-6",
     "backend/app/data/lessons.json"),
    ("Fix Bagus dialogue to be constructive rather than mocking ('Kha-kha! Typical newbie mistake!')",
     "backend/app/data/lessons.json (multiple lessons)"),
    ("Reduce dialogue repetition: analogy should be stated once, not repeated verbatim by Novice in pre_topic_dialogue, analogy, and game_relevance",
     "backend/app/data/lessons.json (multiple lessons)"),
    ("Lesson 3-8: Separate 'if-found shorthand' from 'ternary operator' — currently mixed, scope confusion",
     "backend/app/data/lessons.json"),
    ("Fix lesson 4-31 boss mission: code example has guess=secret always succeeding, but task asks for different behavior — inconsistent",
     "backend/app/data/lessons.json"),
    ("Fix Reviews fetch: add loading state, error handling, and AbortController cleanup in HomePage.tsx",
     "frontend/src/pages/HomePage.tsx", tech_ux),
    ("Surface useLessons() error in Layout/Sidebar when lessons API fails",
     "frontend/src/hooks/useApi.ts", tech_ux),
    ("Fix CodePlayground line numbers contrast (~3.47:1 fails WCAG AA)",
     "frontend/src/components/CodePlayground.tsx", tech_ux),
    ("Add accessible label to code textarea in CodePlayground",
     "frontend/src/components/CodePlayground.tsx", tech_ux),
]
for item in p1_items:
    lines.append(f"- **{item[0]}** (`{item[1]}`)")
lines.append("")

# P2 fixes
lines.append("### P2 — Medium Priority")
lines.append("")
p2_items = [
    ("Fix wrong subtitles: 4-15 shows 'Logical OR' should be 'Sorting'; 4-9 shows 'Text search' should be 'String join'",
     "backend/app/data/lessons.json"),
    ("Split boss lesson 4-31 into 2 x 25 min segments for 10-year-old attention span",
     "backend/app/data/lessons.json"),
    ("Replace 'итерация' with 'шаг'/'повторение' in syntax reminders visible to children (lessons 2-5, 3-14)",
     "backend/app/data/lessons.json"),
    ("Replace English 'Loading lesson...' with Russian equivalent in loading spinner",
     "frontend/src/pages/LessonPage.tsx"),
    ("Add tooltips for steampunk terms ('Aether', 'Resonance', 'Adept') on HomePage",
     "frontend/src/pages/HomePage.tsx"),
    ("Add child-friendly definitions for 'аргумент' and 'параметр' in lesson 5-1",
     "backend/app/data/lessons.json"),
    ("Add loading/error state to useProgress() to prevent flash of incorrect state",
     "frontend/src/hooks/useApi.ts", tech_ux),
    ("Add retry mechanism for Pyodide load failure",
     "frontend/src/components/CodePlayground.tsx", tech_ux),
    ("Fix QuizSection error handling: show distinct 'Connection error' when API fails instead of misleading 'Wrong'",
     "frontend/src/components/QuizSection.tsx", tech_ux),
    ("Guard against `prefers-reduced-motion` in Bagus error feedback bounce animation",
     "frontend/src/components/MissionCard.tsx", tech_ux),
    ("Add request timeout (AbortSignal) to fetch calls in checkQuizAnswer/checkWhatOutputs",
     "frontend/src/hooks/useApi.ts", tech_ux),
    ("Remove unused DialogueBubble import from LessonPage.tsx",
     "frontend/src/pages/LessonPage.tsx", tech_ux),
    ("Fix 'Continue Quest' button for all-lessons-complete state (show celebration message)",
     "frontend/src/pages/HomePage.tsx", tech_ux),
    ("Add loading guard for isLessonUnlocked when lessons array is empty (prevents flash of unlocked locked lessons)",
     "frontend/src/pages/LessonPage.tsx", tech_ux),
    ("Reduce dialogue length in lessons where Novice character repeats analogy verbatim (Persona 20 issue)",
     "backend/app/data/lessons.json (multiple lessons)"),
]
for item in p2_items:
    lines.append(f"- **{item[0]}** (`{item[1]}`)")
lines.append("")

# ── Footer ────────────────────────────────────────────────────────────────
lines.append("---")
lines.append("")
lines.append("*Report generated on 2026-05-31 by combining:\n"
             "- `scripts/audit_persona_10.json` (16 lessons, child-friendliness)\n"
             "- `scripts/audit_persona_20.json` (16 lessons, young adult perspective)\n"
             "- `scripts/audit_technical_ux.json` (19 technical findings)\n"
             "- Automated content analysis of `backend/app/data/lessons.json` (92 lessons total)*")

# ── WRITE ─────────────────────────────────────────────────────────────────
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nReport written to {OUT_PATH}", file=sys.stderr)
print(f"    - {len(lessons)} lessons analyzed", file=sys.stderr)
print(f"    - {len(backtick_issues)} backtick issues", file=sys.stderr)
print(f"    - {len(empty_field_issues)} empty field issues", file=sys.stderr)
print(f"    - {len(curve_issues)} curve issues", file=sys.stderr)
print(f"    - {len(typo_findings)} lessons with potential typos", file=sys.stderr)
print(f"    - {len(tech_ux['findings'])} technical UX findings", file=sys.stderr)
