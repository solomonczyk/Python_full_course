# Course Flow Review

## Summary

| Metric | Value |
|--------|-------|
| Lessons reviewed | 92 |
| Parts reviewed | 5 |
| Course-flow issues found | 4 structural + 2 confirmed carryover |
| Must fix now | 0 |
| Can fix in course flow corrective pass | 2 (lesson 2-5, lesson 4-30) |
| Requires quest/recap architecture correction | 1 (missing quest system) |
| Non-blocking polish | 6 (missing foundation blocks) |
| Recommended next action | `course_flow_corrective_pass` |

---

## Method

### Documents Reviewed

1. `docs/remaining_deferred_issue_triage.md` — 8 remaining issues classified; 2 deferred to course flow review
2. `docs/proof_remaining_deferred_issue_triage.json` — confirms classification with lesson-level detail
3. `docs/operator_human_lesson_review_10_lessons.md` — human review of 10 representative lessons (7 PASS, 3 NEEDS_FIX)
4. `docs/content_corrective_pass_report.md` — 7 fixes applied across 3 NEEDS_FIX lessons; 8 remaining issues documented
5. `docs/operator_recheck_corrected_lessons.md` — production verification of 4 corrected lessons; carryover observations
6. `backend/app/data/lessons.json` — full course data: 92 lessons with structure, mission, practice, foundation
7. `api/app/data/lessons.json` — identical to backend (hash verified); data sync confirmed

### Review Method

This review builds a **course structure map** from the full lesson data, then analyzes difficulty curves at three levels:

- **Micro level**: individual lesson practice → mission gap (e.g., 2-5)
- **Meso level**: chapter flow — how difficulty changes within a chapter
- **Macro level**: part-to-part transitions — how the course grows across parts

---

## Course Complexity Model

Defined difficulty levels 1–5 for this analysis:

| Level | Label | Description | Example |
|-------|-------|-------------|---------|
| 1 | Recognition / copy | Copy a simple code pattern; single concept, one line | `print("Hello")`, `name = "Alice"` |
| 2 | Single concept application | Apply one concept in a straightforward way | `for i in range(5): print(i)`, `if x > 0:` |
| 3 | Combine 2 related concepts | Use two concepts together where one is natural extension | `int(input())`, `for` with `range(1,6)` |
| 4 | Multi-step / multi-concept | Several steps using different concepts from recent lessons | Nested loops, list comprehensions, formatted output inside loop |
| 5 | Quest / recap / mixed challenge | Must select and combine skills from multiple chapters | Full game with while + random + conditions + input |

### Difficulty Distribution Per Part

| Part | L1 | L2 | L3 | L4 | L5 | Total |
|------|----|----|----|----|----|-------|
| Part 1: Foundation | 8 | 1 | 0 | 0 | 0 | 9 |
| Part 2: Conditionals & Loops | 4 | 2 | 0 | 0 | 0 | 6 |
| Part 3: Data Types & Collections | 12 | 27 | 1 | 1 | 0 | 41 |
| Part 4: Advanced Topics & Recap | 4 | 23 | 3 | 1 | 0 | 31 |
| Part 5: Functions & Dicts | 0 | 5 | 0 | 0 | 0 | 5 |
| **Total** | **28** | **58** | **4** | **2** | **0** | **92** |

**Key observation**: 86 of 92 lessons are Level 1–2. Only 6 lessons reach Level 3–4. Zero lessons reach Level 5 (quest/recap/mixed challenge) — this is a structural gap.

---

## Chapter Flow Map

### Part 1: Foundation (9 lessons, chapters 1–2)

| Metric | Assessment |
|--------|-----------|
| **Learning goal** | Learn to output text, store values, receive input, and make simple decisions |
| **New skills introduced** | `print()`, strings, variables, `input()`, `int()`, arithmetic, comparisons, `if`, `if/else` |
| **Practice pattern** | 2 practice subtasks per lesson; simple single-concept tasks |
| **Foundation blocks** | Present in lessons 1-1, 1-2, 1-3, 1-5; missing from 1-4, 1-6, 1-7, 1-8, 1-9 |
| **Recap strength** | **None** — no recap lesson in Part 1 |
| **Quest strength** | **None** — no quest lesson in Part 1 |
| **Difficulty curve** | **smooth** — L1 (8 lessons) → L2 (1 lesson: 1-9 if/else). Gradual, appropriate |
| **Main risks** | No recap before transitioning to Part 2; missing foundation blocks in 5/9 lessons |
| **Recommended action** | Add foundation blocks during consistency pass; no urgent changes |

### Part 2: Conditionals & Random & Loops (6 lessons, chapters 3–5)

| Metric | Assessment |
|--------|-----------|
| **Learning goal** | Extend conditionals to multiple branches, add randomness, introduce iteration |
| **New skills introduced** | `elif`, logical chains, `random.randint()`, `for`, `range()` |
| **Practice pattern** | 2 practice subtasks; single-concept tasks |
| **Foundation blocks** | None in any of the 6 lessons |
| **Recap strength** | **None** — no recap before Part 3's 41-lesson marathon |
| **Quest strength** | **None** — no quest lesson |
| **Difficulty curve** | **smooth but truncated** — L1 (4) → L2 (2). Stays at low difficulty |
| **Main risks** | **Part 2 is extremely short (6 lessons) relative to Part 3 (41 lessons).** The chapter-to-chapter jump from Part 2 (6 lessons) to Part 3 (41 lessons) is a 7× volume increase. No bridge prepares the learner for the density of Part 3. Mission 2-5 has a real difficulty jump (see Issue 2-5 below). |
| **Recommended action** | Shorten jump by adding bridge lesson before 2-5 or splitting 2-5 mission; add recap before Part 3 |

### Part 3: Data Types & Collections (41 lessons, chapters 6–11, 18)

| Metric | Assessment |
|--------|-----------|
| **Learning goal** | Master numeric types, boolean logic, string manipulation, list operations |
| **New skills introduced** | `float`, division types, modulo, `bool`, `and`/`or`/`not`, nested `if`, `range(start,stop,step)`, strings indexing, slicing, f-strings, list methods (pop/remove/append/index/count/insert/extend), `random.choice`/`shuffle` |
| **Practice pattern** | 2 practice subtasks; mostly single-concept |
| **Foundation blocks** | None in any of the 41 lessons |
| **Recap strength** | **None** — 41 lessons without any recap or quest |
| **Quest strength** | 3-41 is boss-level but positioned as an indentation/formatting task, not a skill-integration quest |
| **Difficulty curve** | **uneven** — L1 (12) → L2 (27) → L3 (1) → L4 (1). Features a "wall" of medium lessons (chapters 7–11). No break or consolidation point until lesson 26 (lists). The 10-lesson chapter 10 (list methods) is monotonous: all medium difficulty, same pattern (new method → practice → mission). |
| **Main risks** | **No recap in 41 lessons** — the longest stretch of any part. After Part 2's gentle 6 lessons, learners hit 27 medium lessons in a row without consolidation. The locked lesson system (required from 2-2 onward) means learners cannot skip ahead. |
| **Recommended action** | Insert at least one recap/quest lesson mid-Part 3 (e.g., after chapter 9 or chapter 10) |

### Part 4: Advanced Topics & Recap (31 lessons, chapters 12–17)

| Metric | Assessment |
|--------|-----------|
| **Learning goal** | Understand `while` loops, string processing, sorting, nested data, references, and build integrated programs |
| **New skills introduced** | `while`, `while True`, `break`, `None`, `join`/`split`, `map`, `sort`/`sorted`/`key`, nested lists, list comprehensions, references, `is`, `copy`/`deepcopy` |
| **Practice pattern** | 2 practice subtasks; some multi-step tasks |
| **Foundation blocks** | None in any of the 31 lessons |
| **Recap strength** | **weak** — Chapter 17 (3 lessons) serves as recap area with 4-29 (chat-bot) and 4-30 (task manager), but neither adequately integrates skills from the full part |
| **Quest strength** | 4-31 (boss) is the strongest, requiring random + while + conditions. However, 4-29 and 4-30 missions are at Level 1–2, which is too low for recap/quest lessons |
| **Difficulty curve** | **uneven** — L1 (4) → L2 (23) → L3 (3) → L4 (1). Chapter 15 is the hardest stretch (3 hard lessons). Then Chapter 17's recap is weaker than the material it should recap |
| **Main risks** | 4-30 mission is too simple (see Issue 4-30). Missing quest architecture means lessons labelled as recap don't actually test multi-skill integration. |
| **Recommended action** | Upgrade 4-30 to multi-skill recap; consider quest architecture for Chapter 17 |

### Part 5: Functions & Dicts (5 lessons, chapter 19)

| Metric | Assessment |
|--------|-----------|
| **Learning goal** | Create reusable code blocks with functions; work with dictionaries; handle errors |
| **New skills introduced** | `def`, parameters, `return`, `dict`, `try`/`except` |
| **Practice pattern** | 2 practice subtasks |
| **Foundation blocks** | None in any of the 5 lessons |
| **Recap strength** | **None** — Part 5 ends without recap or quest |
| **Quest strength** | **None** — no boss or quest lesson |
| **Difficulty curve** | **smooth** — all medium (L2). Gradual |
| **Main risks** | Course ends abruptly at lesson 5-7 (try/except) without a final integration quest. No capstone that combines functions + dicts + exceptions + all prior skills. |
| **Recommended action** | Add final quest/capstone lesson at end of Part 5 (or design as separate post-course project) |

### Cross-Part Risks

| Risk | Severity | Evidence |
|------|----------|----------|
| **Part size imbalance** | **high** | Part 2 (6 lessons) → Part 3 (41 lessons) is a 7× volume jump. Part 5 (5 lessons) is also too short. |
| **No mid-course recap** | **high** | 41 lessons in Part 3 without a single recap. Learners go from "elif" to "deepcopy" without consolidation. |
| **Missing quest architecture** | **high** | Zero lessons at Level 5 (quest/recap/mixed challenge). The course format doesn't distinguish recap/quest lessons. |
| **Foundation blocks missing from 88/92 lessons** | **low** (polish) | Only lessons 1-1, 1-2, 1-3, 1-5 have foundation blocks. All other lessons lack preliminary terminology context. |
| **boss lessons not actually integrative** | **medium** | 3-41 (boss) and 4-31 (boss) are harder but still single-concept focused, not multi-skill integration. |

---

## Issue 2-5 Review: Mission Difficulty Jump

### Current Mission

**Mission task**: "Напиши программу, которая выводит таблицу умножения на 3 от 1 до 5. Используй цикл for и range. Формат каждой строки: '3 * ЧИСЛО = РЕЗУЛЬТАТ'. Подсказка: результат = 3 * i."

**Expected output**:
```
3 * 1 = 3
3 * 2 = 6
3 * 3 = 9
3 * 4 = 12
3 * 5 = 15
```

### Required Concepts

1. `for` loop with `range(1, 6)` — taught in lesson body ✅
2. Multiplication `3 * i` — arithmetic is covered in lesson 1-6 ✅ (but now as expression, not standalone)
3. **String formatting** — `${i}` inside f-string or concatenation with `str()` — **NOT taught in any lesson before 2-5**
4. **Multi-line formatted output** — building a string that changes per iteration — **NOT practiced before**

### Previous Preparation

| Lesson | Practice Tasks | Mission |
|--------|---------------|---------|
| 2-3 (random.randint) | Print random number, print 3 roll results | "Бросок: X + Y = Сумма" — already hints at formatted output but doesn't enforce format |
| 2-4 (simple game with random) | if-guess game | Simple text output "Игра готова!" |
| 2-5 (for) — practice | `print(i)` patterns | **Mission uses f-string/concatenation** |
| 2-6 (range) — practice | Print numbers, print list(range) | Simple number output "1" |

### Difficulty Jump Analysis

- **Practice level**: L2 (single concept: for + range, print variable)
- **Mission required level**: L3–L4 (multi-step: for loop + multiplication expression + string formatting or concatenation + line-by-line output)
- **Jump magnitude**: +1.5 to +2 difficulty levels
- **Root cause**: The mission assumes the learner already knows how to produce formatted output (either via f-strings, taught in 3-22, or via string concatenation). Neither skill is taught or practiced before 2-5.

### Verdict

**Issue confirmed.** The mission is 1.5–2 difficulty levels above the practice. The formatting skill (`3 * 1 = 3`) is not prepared in any previous lesson.

### Recommended Correction

**Recommended option: B (split 2-5 mission into two stages) + C (add guided hints/scaffold)**

| Option | Description | Rationale |
|--------|-------------|-----------|
| ~~A: Add bridge before 2-5~~ | Add new lesson between 2-4 and 2-5 | Overkill — the concept gap is small enough to fix in-place |
| **B: Split mission** | Stage 1: print multiplication results only (numbers). Stage 2: format as table | Lets learner master the arithmetic first, then the formatting |
| **C: Add scaffold/hints** | Provide string concatenation template in hints or split mission description | Low-cost fix that teaches the missing formatting skill |
| ~~D: Move harder part to chapter quest~~ | Not viable — no quest architecture exists | Would require larger architectural change |

**Specific recommendation**: Rewrite the mission to two sequential tasks:
1. First: "Выведи результат умножения 3 на каждое число от 1 до 5. Используй цикл for: print(3 * i)" (expected: 3 6 9 12 15 each on separate line)
2. Second (bonus/challenge): "А теперь выведи таблицу умножения в формате '3 * число = результат'. Используй конкатенацию строк: print(str(3) + " * " + str(i) + " = " + str(3 * i))" OR provide template

This keeps the original challenge available but adds a scaffolded entry point.

---

## Issue 4-30 Review: Mission Too Simple for Recap

### Current Mission

**Mission task**: "Создай пустой список задач. Добавь задачу 'learn python' через append и выведи список."

**Expected output**: `['learn python']`

### Expected Recap/Role

Lesson 4-30 is positioned as a multi-skill integration lesson:
- Title: "Таск-менеджер" (Task Manager)
- Topic: "таск-менеджер" (task manager)
- Part of Chapter 17: "Recap/Quest" area of Part 4
- Lesson body covers: lists, while loop concept, conditionals, input handling (per human review)

### Actual Difficulty

- **Mission level**: L1 (recognition — create list, call append once, print)
- **What it actually tests**: Only `list.append()` — one micro-skill
- **Skills NOT tested**: `while` loop, conditionals, `input()`, menu system, multi-step logic

### Missing Skill Checks

| Skill | Where taught | Tested in practice? | Tested in mission? |
|-------|-------------|-------------------|-------------------|
| `list.append()` | 3-31 | ✅ | ✅ (the only skill) |
| `while` loop | 4-26, 4-27 | ✅ | ❌ |
| `while True` with `break` | 4-27 | ✅ | ❌ |
| `if`/`elif`/`else` | 1-8, 1-9, 2-1 | ✅ | ❌ |
| `input()` with `int()` | 1-4, 1-5 | ✅ | ❌ |
| Multi-skill integration | None | ❌ | ❌ |

### Verdict

**Issue confirmed.** The mission only tests L1 single-concept skill, while the lesson body teaches L3–L4 multi-skill integration. The lesson body describes a full task manager (while loop with menu, add/remove/view tasks), but the mission only asks for an empty list with one item appended.

### Root Cause

The mission format (single `mission` object with single `task`, `expected_output`, no multi-part missions) constrains what can be tested. The actual task manager requires multiple inputs, a while loop, and conditional branching — none of which fit the current mission model.

### Recommended Correction

**Recommended option: C (convert 4-30 into guided recap with staged tasks) — within current format constraints**

| Option | Description | Rationale |
|--------|-------------|-----------|
| A: Upgrade to multi-skill recap mission | Rewrite mission to test at least 2 skills together | Best outcome but limited by mission format |
| ~~B: Keep simple but add separate quest~~ | Adds separate quest lesson | Better long-term but deferred to architecture change |
| **C: Guided recap with staged tasks** | Multi-line expected output: append → show list → show count | Works within current mission constraints; bumps difficulty to L3 |
| D: Defer to quest architecture update | Do nothing now, fix later | Acceptable only if architecture correction follows |

**Specific recommendation**: Rewrite mission to require at least 2 steps:

Original: `Создай пустой список задач. Добавь задачу 'learn python' через append и выведи список.` → `['learn python']`

Revised: `Создай список задач tasks = ['купить хлеб']. Добавь 'выучить Python' через append. Выведи длину списка через len() и сам список.`

Expected: `2\n['купить хлеб', 'выучить Python']`

This tests: list creation, append, len() — combining 2-3 list skills. Still not a full recap, but meaningful improvement within format constraints. A full task manager mission requires quest architecture change.

---

## Global Flow Risks

| # | Risk | Parts Affected | Severity | Action Needed |
|---|------|----------------|----------|---------------|
| 1 | **7× volume jump** from Part 2 (6) to Part 3 (41) | 2 → 3 | high | Add recap/bridge at end of Part 2 |
| 2 | **No recap in 41-lesson Part 3** | 3 | high | Insert recap lesson mid-Part 3 |
| 3 | **Missing quest architecture** — no Level 5 lessons exist | All | high | Define quest format; convert 3-41, 4-30, 4-31 to quests |
| 4 | **Part 5 ends without capstone** | 5 | medium | Add final integration project/quest |
| 5 | **88/92 lessons without foundation blocks** | All | low (polish) | Add in editorial consistency pass |
| 6 | **Mission format constraints** limit recap/quest potential | 4 | medium | Design multi-part or staged mission format |

---

## Target Course Complexity Model

### Per-Chapter Target Levels

| Chapter | Part | Target Start | Target End | Bridge Needed | Recap | Quest | Acceptable Jump | Forbidden Jump |
|---------|------|-------------|-----------|---------------|-------|-------|-----------------|----------------|
| 1. Print & Strings | 1 | 1 | 1 | No | No | No | +0 | +1 |
| 2. Conditions | 1 | 1 | 2 | No | Yes | No | +1 | +2 |
| 3. Elif & Chains | 2 | 2 | 2 | Yes (from Part 1) | Yes | No | +1 | +2 |
| 4. Random | 2 | 2 | 2 | No | No | No | +1 | +2 |
| 5. For & Range | 2 | 2 | 2 | No | No | No | +1 | **+2 (current 2-5 violates)** |
| 6. Float & Division | 3 | 2 | 2 | No | No | No | +1 | +2 |
| 7. Boolean & Logic | 3 | 2 | 3 | No | No | No | +1 | +2 |
| 8. For with Range | 3 | 2 | 3 | No | No | No | +1 | +2 |
| 9. Strings & Methods | 3 | 2 | 3 | No | **Yes** | No | +1 | +2 |
| 10. List Basics | 3 | 2 | 3 | No | No | No | +1 | +2 |
| 11. List Advanced | 3 | 3 | 3 | No | No | No | +1 | +2 |
| 12. While & Break | 4 | 3 | 3 | No | No | No | +1 | +2 |
| 13. String Processing | 4 | 3 | 3 | No | No | No | +1 | +2 |
| 14. Sort & Map | 4 | 3 | 3 | No | No | No | +1 | +2 |
| 15. Nested & References | 4 | 3 | 4 | Yes | No | No | +1 | +2 |
| 16. While Advanced | 4 | 3 | 3 | No | No | No | +1 | +2 |
| **17. Recap/Quest** | **4** | **3** | **4** | **No** | **Yes** | **Yes** | **+1** | **+2** |
| 18. Boss | 3 | 2 | 3 | No | Yes | Yes | +1 | +2 |
| 19. Functions & Dicts | 5 | 3 | 3 | Yes (from Part 4) | **Yes** | **Yes** | +1 | +2 |

### Target Model Summary

- **Stage 1** (Lessons 1-1 to 1-5): Recognize → Copy → Understand syntax
- **Stage 2** (Lessons 1-6 to 2-4): Use variable → Change value → See different result
- **Stage 3** (Lessons 2-5 to 3-20): Combine 2 topics → Simple loop → String operations
- **Stage 4** (Lessons 3-21 to 4-25): Multi-step tasks → List manipulation → Sorting → References
- **Stage 5** (Lessons 4-26 to 5-7): While loops → Integrated programs → Functions → Capstone

### Where Current Course Deviates from Target

| Deviation | Current | Target | Impact |
|-----------|---------|--------|--------|
| 2-5 mission | L3–L4 | L2 | Learner hits wall |
| 4-30 mission | L1 | L3–L4 | Recap doesn't recap |
| Part 2 → Part 3 volume | 6 → 41 lessons | Gradual increase | Learner fatigue |
| Part 3 mid-point recap | None | 1 recap at Ch9 | No consolidation |
| Part 5 capstone | None | 1 final quest | No sense of completion |
| Quests across course | 0 | 3–4 | Missing integration practice |

---

## Recommended Next Layer

### Selected: `course_flow_corrective_pass`

**Rationale:**

1. **Two concrete lesson-level fixes are clearly defined and bounded:**
   - Lesson 2-5: Split mission into staged tasks (add scaffold, keep original as challenge)
   - Lesson 4-30: Upgrade mission to require 2-3 list skills (append + len + list print)

2. **These fixes do not require architecture changes.** Both can be done within the current mission format. The guided recaps and staged tasks work within the existing `mission.task` / `mission.expected_output` constraints.

3. **Architecture correction is deferred but tracked.** The missing quest architecture and missing mid-Part-3 recap are real issues, but they require design decisions beyond content editing:
   - What does a "quest" lesson look like in the current format?
   - Should quests have multi-part missions?
   - Where should the Part 3 recap be inserted?

4. **The corrective pass is a prerequisite for architecture work.** Until basic pacing issues (2-5 jump, 4-30 undershoot) are resolved, the course isn't stable enough to design a quest architecture against.

### What the Corrective Pass Should Do

| Task | Scope | Complexity |
|------|-------|------------|
| Fix 2-5 mission: add staged scaffold (simple print → formatted table) | Single lesson, mission only | Low |
| Fix 4-30 mission: upgrade to multi-step list task | Single lesson, mission only | Low |
| Add foundation blocks for all non-NEEDS_FIX lessons (6 remaining) | 6 lessons, mechanical | Low |
| Verify no regression in practice → mission alignment | All 92 lessons verify | Medium |

### What Should NOT Be in the Corrective Pass

| Task | Reason |
|------|--------|
| Quest architecture design | Requires design decision, not content fix |
| Mid-Part-3 recap lesson | Requires new lesson, not fix |
| Part 5 capstone | Requires new lesson, not fix |
| Part 2 → Part 3 bridge | Requires new lesson, not fix |

### Expected Next Action Sequence

```
course_flow_corrective_pass → quest_recap_architecture_correction → foundation_consistency_polish → production_readiness_review
```

---

## Forbidden Actions Confirmation

| Action | Status |
|--------|--------|
| Infrastructure changed | ✅ Not changed |
| Mission checker changed | ✅ Not changed |
| SEO/routes changed | ✅ Not changed |
| Frontend/backend architecture changed | ✅ Not changed |
| Deployment pipeline changed | ✅ Not changed |
| Course content rewritten (mass) | ✅ Not done — only analysis |
| Lessons.json edited | ✅ Not edited (no fixes applied in this review) |
| New features created | ✅ Not created |
| `production_accepted=true` | ✅ Not set (remains false) |
| Issues dismissed without evidence | ✅ Not done — each issue has evidence and reasoning |
| 2-5 or 4-30 fixed without review | ✅ Not done — only recommended corrections, no edits |
| All issues called non-blocking without proof | ✅ Not done — 4 structural risks identified with evidence |

## Follow-up Status

**2026-06-02**: `course_flow_corrective_pass` completed.

- Lesson 2-5: Mission simplified from formatted multiplication table to simple arithmetic-within-loop (L3-L4 → L2-L3). String formatting requirement removed.
- Lesson 4-30: Mission upgraded from single `list.append()` to multi-step list task (L1 → L3). Tests append, len, and print.
- Structural issues (Part 3 volume, missing recap, missing quest architecture, missing capstone) deferred to next architecture layer.

See `docs/course_flow_corrective_pass_report.md` and `docs/proof_course_flow_corrective_pass.json`.
