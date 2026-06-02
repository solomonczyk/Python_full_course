# Course Flow Corrective Pass

## Summary
- **Lessons changed**: 2-5, 4-30
- **Issues fixed**:
  - Lesson 2-5: Mission difficulty jump (L3-L4 → L2-L3) — removed unexplained string formatting requirement, simplified to multiplication-within-loop scaffolded task
  - Lesson 4-30: Mission too simple for recap (L1 → L3) — upgraded from single `list.append()` check to multi-step task testing list creation, append, len(), and print
- **Structural issues deferred**: 4 (Part 2→3 volume jump, missing Part 3 recap, missing quest architecture, missing Part 5 capstone)
- **Production accepted**: `false`

---

## Lesson 2-5 Fix

### Before
**Mission task**: "Напиши программу, которая выводит таблицу умножения на 3 от 1 до 5. Используй цикл for и range. Формат каждой строки: '3 * ЧИСЛО = РЕЗУЛЬТАТ'. Подсказка: результат = 3 * i."

**Expected output**:
```
3 * 1 = 3
3 * 2 = 6
3 * 3 = 9
3 * 4 = 12
3 * 5 = 15
```

### Problem
The mission required string formatting (concatenation or f-strings) which is NOT taught before lesson 2-5. F-strings are introduced in lesson 3-22. String concatenation is not formally taught in any prior lesson. This creates a 1.5–2 level difficulty jump from practice (L2: `print(i)`) to mission (L3–L4: formatted table output).

### Correction
**Option C — simplified table**: Rewrote the mission to require only loop + simple arithmetic + print, without any string formatting.

**New mission task**: "Выведи результаты умножения числа 3 на каждое число от 1 до 5. Используй цикл for и range(1, 6). Внутри цикла вычисли результат = 3 * i и выведи его. Каждое число на новой строке."

**New expected output**:
```
3
6
9
12
15
```

### Difficulty before
L3–L4 (multi-step: for loop + arithmetic + string formatting/concatenation + line-by-line formatted output)

### Difficulty after
L2–L3 (single-step extension: for loop + simple arithmetic inside loop + print result)

### Why this is now beginner-appropriate
- `for` and `range(1, 6)` are taught in the lesson body (L2)
- `*` (multiplication) was taught in lesson 1-6 (prior knowledge)
- `print(result)` outputting a number is identical in form to the practice subtask `print(i)`
- No string formatting, f-strings, concatenation, or `str()` conversion required

### Remaining risk
- The multiplication `3 * i` is used inside a loop context which is a very small step beyond practice. This is appropriate but should be monitored during operator recheck.

---

## Lesson 4-30 Fix

### Before
**Mission task**: "Создай пустой список задач. Добавь задачу 'learn python' через append и выведи список."

**Expected output**:
```
['learn python']
```

### Problem
The mission only tested `list.append()` — a single L1 micro-skill. The lesson body teaches multi-skill integration: lists + while loop concept + conditionals + input handling. As a recap/quest-positioned lesson, it should test at least 2–3 skills from the chapter.

### Correction
**Option B — staged list recap**: Upgraded to a multi-step task requiring list creation, append (called twice), `len()`, and print — all within the current single-mission format.

**New mission task**: "Создай пустой список tasks. Добавь задачу 'купить хлеб' через append. Добавь задачу 'выучить Python' через append. Выведи количество задач (len(tasks)), а затем сам список tasks. Каждое значение на отдельной строке."

**New expected output**:
```
2
['купить хлеб', 'выучить Python']
```

### Difficulty before
L1 (recognition — single operation: create list, call append once, print)

### Difficulty after
L3 (multi-step combination: list creation + append ×2 + len() + print, orchestrated in correct sequence)

### Why this now works as recap
- Tests multiple list skills from the chapter: `list.append()`, `len()`, `print(list)`
- Requires sequencing 4 operations in correct order (create → append → append → len → print)
- Stays within the current single-mission format — no architecture changes needed
- Difficulty matches the lesson body's multi-skill integration theme

### Remaining risk
- The mission still doesn't test `while` loops or conditional branching (the lesson body mentions a full menu-driven task manager). A complete recap would require quest architecture changes beyond this bounded corrective pass scope.
- Mission now expects both `len` and list output; mission checker must validate multi-line output (already supported — existing lessons use `\n` in expected_output)

---

## Deferred Architecture Issues

The following structural issues are explicitly deferred to the next architecture layer:

| Issue | Severity | Recommended Layer | Details |
|-------|----------|-------------------|---------|
| 7× volume jump from Part 2 (6 lessons) to Part 3 (41 lessons) | **high** | `part_3_recap_and_pacing_architecture` | No bridge prepares the learner for Part 3's density |
| No recap in 41-lesson Part 3 | **high** | `part_3_recap_and_pacing_architecture` | Longest stretch of the course without a consolidation point |
| Missing quest architecture / 0 lessons at Level 5 | **high** | `quest_architecture_correction` | No lesson requires multi-skill integration across chapters |
| Missing Part 5 capstone | **medium** | `part_5_capstone_layer` | Course ends abruptly without final integration project |

**These issues are not addressed in this corrective pass.** They require architectural design decisions beyond content editing (quest format design, lesson insertion points, multi-part mission support). They remain tracked in the course flow review and must be resolved before `production_accepted=true`.

---

## Verification

- **Backend/api data sync**: ✅ MD5 hashes match (`a5e5db16...`)
- **All 92 lessons preserved**: ✅ (verified via `json.load` — 92 objects)
- **Tests**:
  - Editorial audit: 23 passed, 3 xfailed (pre-existing)
  - Full backend test suite: passed
- **Production/API check**: pending (requires deploy)
- **Git**: committed and pushed

---

## Next Actions

1. `operator_recheck_course_flow_fixes_or_quest_architecture_correction` — verify 2-5 and 4-30 in production
2. `quest_architecture_correction` — design quest format, add missing recap/quest lessons
3. `part_5_capstone_layer` — add final integration project
