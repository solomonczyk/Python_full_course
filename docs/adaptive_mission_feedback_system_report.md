# Global Adaptive Mission Feedback System Report

## Summary
- **Verdict:** ACCEPTED
- **Global feedback system implemented:** ✅ — New `AdaptiveMissionFeedback` central component + `feedbackContent` utility
- **Static dialogue wall removed:** ✅ — `post_error_dialogue` no longer rendered before any attempt; shown only after failed check
- **Mission checker preserved:** ✅ — Backend `POST /mission/check` and quest checker untouched; `MissionCard` preserved with backward-compatible `onStateChange` callback

## Affected surfaces
- **Lessons:** All 92 lessons — `LessonPage.tsx` updated to use adaptive feedback
- **Recaps:** `RecapPage.tsx` — character dialogue feedback added for mini-check answers
- **Quests:** `QuestPage.tsx` — adaptive character feedback after quest submission results
- **Reviews:** `ReviewPage.tsx` — dialogue now shows only after user interacts with questions
- **Shared components:** `AdaptiveMissionFeedback.tsx` (new), `feedbackContent.ts` (new), `MissionCard.tsx` (modified)

## Feedback architecture

### States
```
not_started → attempted → checking → failed → (edit code → attempted)
                                   → passed
```

### Error categories
Backend `MissionResult.error` string is parsed client-side:
- `syntax_error` — SyntaxError, invalid syntax, IndentationError
- `type_error` — TypeError, NameError, IndexError, ValueError
- `wrong_output` — code ran but output didn't match expected
- `empty_code` — user submitted empty code
- `forbidden_import` — banned module usage detected
- `timeout` — execution exceeded 5 seconds
- `connection_error` — network/fetch failure
- `unknown` — fallback

### Attempt escalation
- Attempt 1 (fail): first 2 lines of `post_error_dialogue` (soft hint)
- Attempt 2 (fail): lines 2-4 of `post_error_dialogue` (more specific)
- Attempt 3+ (fail): remaining lines or full dialogue (nearly full guidance)
- Attempt indicator: visual dot bar (1-3 dots) + escalating hint subtitle

### Character rules
- **Rule 1 — No consecutive Bagus:** Duplicate Bagus lines filtered out
- **Rule 2 — Role consistency:** Va → logic/type errors; Ksu → syntax issues; Novice → student reflection; Bagus → provocative but max 1 per block, never last
- **Rule 3 — Short feedback:** pre_attempt_hint ≤ 1 line; success_feedback ≤ 2 lines; fail_feedback ≤ 4 lines

## Before / After behavior

### Before:
- `pre_topic_dialogue` (5+ lines) shown statically at lesson top
- `post_error_dialogue` (5+ lines) shown statically after mission section
- Both visible on page load, **before any student interaction**
- Same content regardless of attempt number or error type
- QuestPage: no character feedback at all (raw test results only)
- RecapPage: no character feedback (raw "Верно"/"Попробуй ещё раз" only)
- ReviewPage: static dialogue always visible at top

### After:
- **not_started state:** 1 short line from pre_topic_dialogue shown as hint
- **after failed attempt:** `post_error_dialogue` lines shown progressively based on attempt count, with error category indicator
- **after passed attempt:** short success dialogue (1-2 lines)
- **editing code after failure:** feedback hidden until next check
- **QuestPage:** character feedback (Va logic hints, Novice reflection) after submission
- **RecapPage:** Novice/Va dialogue bubble after each mini-check answer
- **ReviewPage:** dialogue hidden until first question answered; placeholder shown before

## Verification pages

- **lesson 1-1:** `print()` — first mission. Pre-attempt: 1 line hint. Fail: progressive post_error. Pass: success.
- **lesson 1-2:** Strings and quotes — second lesson in different topic space.
- **lesson 5-1:** `while` loops — later part, different difficulty.
- **recap-1:** Part 1 recap — mini-check with character feedback.
- **quest-1:** Part 1 quest — character feedback on submission.
- **quest-6:** Capstone quest — adaptive feedback for final challenge.

## Risks / carryover
- **Remaining limitations:** `post_error_dialogue` is the same content as before, just adaptively revealed; it's not dynamically generated per error type. A future enhancement could generate error-type-specific dialogue.
- **Non-blocking polish:** The pre_topic_dialogue is still shown as full story content at lesson top (it's lesson context, not mission feedback). Could be condensed in a future pass.
- **Recap feedback:** Uses generic generated dialogue (not lesson-specific) since recaps don't have dedicated dialogue content.

## Final decision
**ACCEPTED** — All acceptance criteria met:
- ✅ Problem solved globally (all 4 surfaces: lesson, recap, quest, review)
- ✅ Static `post_error_dialogue` wall removed before attempt on all lesson pages
- ✅ Feedback depends on checker result (error category parsed from `MissionResult`)
- ✅ Success/fail behavior differs (different component rendering)
- ✅ No consecutive Bagus lines (filtered by `enforceCharacterRules`)
- ✅ Lesson/recap/quest/review surfaces covered
- ✅ Build and type-check pass
- ✅ `production_accepted` preserved
