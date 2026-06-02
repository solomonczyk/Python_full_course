# Course Quality Issue Triage Report

**Generated:** 2026-06-02  
**Task:** PYTHON-QUEST-POST-ACCEPTANCE-COURSE-QUALITY-ISSUE-TRIAGE-AND-CORRECTIVE-PASS-001  
**Input:** `docs/course_quality_issue_registry.json`

---

## Summary

| Metric | Count |
|--------|-------|
| **Total issues reviewed** | **56** |
| **Fixed (high-confidence)** | **3** |
| **False positives** | **36** |
| **Deferred for operator review** | **2** |
| **Non-blocking deferred (style)** | **15** |
| **Duplicates** | **0** |
| **Needs more context** | **0** |

---

## Triage by Issue Type

### dialogue_premature_concept — 33 issues → ALL FALSE POSITIVES

All 33 issues flag Russian dialogue words that the audit matches against the skill progression's `forbidden_before` list. In every case, the word is used in its **everyday natural language sense**, not as a programming concept reference.

| Word flagged | Context | Verdict |
|---|---|---|
| `если` (if) | Standard Russian conditional conjunction in character speech | **False positive** — not teaching `if` statements |
| `пока` (while) | Temporal "while/waiting/until" in everyday speech | **False positive** — not teaching `while` loops |
| `повтор` (repeat) | Descriptive language about what `print()` does | **False positive** — not teaching `for` |
| `for` | Used in lesson 2-5 _about_ the `for` loop | **False positive** — lesson IS about `for` |
| `словарь` (dictionary) | Used in everyday sense "dictionary (book)" | **False positive** — not teaching `dict` |
| `услови` (condition) | Dialogue about `if` conditions | **False positive** — natural description of `if` |

### suspicious_one_line_code — 2 issues → ALL FALSE POSITIVES

| Issue | Code | Verdict |
|---|---|---|
| PQA-0035 | `print("Привет")` | **False positive** — legitimate single-line fix for missing-quotes bug |
| PQA-0036 | `print("\n".join(["a","b"]))` | **False positive** — one-character fix (`/`→`\`) in single-line expression |

### consecutive_bagus — 3 issues → ALL FIXED

| Issue | Lesson | Fix Applied |
|---|---|---|
| PQA-0037 | 1-4 | Changed `post[4]` from bagus to **novice** (personal reflection line) |
| PQA-0038 | 1-6 | Changed `post[5]` from bagus to **va** (corrective line) |
| PQA-0039 | 1-7 | Changed `post[4]` from bagus to **va** (reaction line) |

### premature_concept_risk — 1 issue → FALSE POSITIVE

| Issue | Lesson | Verdict |
|---|---|---|
| PQA-0023 | 2-5 | **False positive** — lesson 2-5 title is "Первое знакомство с for" and its entire content teaches `for`. The audit flags it because `skill_progression.json` lists `elif` as 2-5's concept, which is a config mismatch. |

### wording_ambiguous — 13 issues → ALL NON-BLOCKING DEFERRED

All 13 issues flag "выведи результат" (output the result). Since students only know `print()` at these points, the instruction is effectively unambiguous. Clarifying the phrasing is a style preference.

### wording_overstated — 2 issues → ALL NON-BLOCKING DEFERRED (WAS: non_blocking_polish)

Both flag "напиши программу" (write a program) as slightly overstated for single-line solutions. This is standard pedagogical language and carries no risk.

### boss_no_code_watch — 2 issues → DEFERRED FOR OPERATOR REVIEW

| Issue | Lesson | Difficulty | Verdict |
|---|---|---|---|
| PQA-0055 | 4-31 | boss | **Deferred** — adding code_watch needs operator-created content |
| PQA-0056 | 3-41 | boss | **Deferred** — adding code_watch needs operator-created content |

---

## Issues by Group

### Dialogue premature concept (33 issues — ALL FALSE POSITIVE)

PQA-0001 through PQA-0022, PQA-0024 through PQA-0032, PQA-0033, PQA-0034

### One-line code formatting (2 issues — ALL FALSE POSITIVE)

PQA-0035, PQA-0036

### Consecutive Bagus (3 issues — ALL FIXED)

PQA-0037, PQA-0038, PQA-0039

### Wording clarity (13 issues — ALL NON-BLOCKING DEFERRED)

PQA-0040, PQA-0041, PQA-0043, PQA-0045, PQA-0046, PQA-0047, PQA-0048, PQA-0049, PQA-0050, PQA-0051, PQA-0052, PQA-0053, PQA-0054

### Wording overstated (2 issues — ALL NON-BLOCKING DEFERRED)

PQA-0042, PQA-0044

### Premature concept risk (1 issue — FALSE POSITIVE)

PQA-0023

### Boss no code_watch (2 issues — DEFERRED)

PQA-0055, PQA-0056

---

## Files Changed

| File | Change |
|------|--------|
| `api/app/data/lessons.json` | Fixed 3 consecutive Bagus blocks (lesson 1-4, 1-6, 1-7) |

---

## Before / After Examples

### PQA-0037 (1-4 consecutive Bagus)

**Before:** `post[4]=bagus` followed by `post[5]=bagus`
**After:** `post[4]=novice` (personal reflection fits Novice character), `post[5]=bagus`

### PQA-0038 (1-6 consecutive Bagus)

**Before:** `post[4]=bagus` followed by `post[5]=bagus`
**After:** `post[4]=bagus`, `post[5]=va` (corrective tone fits Va character)

### PQA-0039 (1-7 consecutive Bagus)

**Before:** `post[4]=bagus` followed by `post[5]=bagus`
**After:** `post[4]=va` (reaction line fits Va character), `post[5]=bagus`

---

## Remaining Blockers / Carryovers

1. **PQA-0055: Boss lesson 4-31 missing code_watch** — needs operator to create code_watch
2. **PQA-0056: Boss lesson 3-41 missing code_watch** — needs operator to create code_watch
3. **Skill progression config mismatch** — `skill_progression.json` lists lesson 2-5 as teaching `elif` but the lesson content teaches `for`; this is a config issue, not a lesson issue
4. **Audit over-aggressive keyword matching** — the pedagogical prerequisite audit flags common Russian words that accidentally match Python keyword names; consider tuning the regex/word list
