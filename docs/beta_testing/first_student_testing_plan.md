# First Student Testing Plan

## Goal

Проверить, может ли первый ученик понять Python Quest, начать demo, пройти первый lesson/mission и продолжить без постоянной помощи взрослого.

## Status

> **PREPARED_NOT_EXECUTED** — план готов, но тестирование не проведено. Реальные ученики пока не доступны. Артефакты подготовлены для запуска теста, когда ученики появятся.

## Test Group

- **Target count:** 5–10 students
- **Level:** complete beginners / early beginners
- **Age group:** broad child/beginner range, without collecting precise age
- **Parent/operator presence:** allowed for observation, not for solving tasks

## Test Entry Point

- **Landing:** /beta
- **Demo CTA:** /lesson/1-1
- **Analytics:** local anonymous analytics only (`window.__PYTHON_QUEST_ANALYTICS__`)

## Test Path

1. Open /beta
2. Read hero/product explanation
3. Click "Начать демо"
4. Start lesson 1-1
5. Complete first mission
6. Continue until first friction point or agreed stop time

## Session Duration

- **Recommended:** 20–30 minutes
- **Maximum:** 45 minutes
- **Stop early if:** student is frustrated or blocked

## What To Observe

- Does student understand what Python Quest is?
- Does student know where to click?
- Does student understand first explanation?
- Does student understand first mission?
- Does student submit answer?
- Does student use hint?
- Does student recover after mistake?
- Does student want to continue?

## Success Criteria

- Student starts demo without external instruction
- Student opens first lesson
- Student attempts first mission
- Student can recover after at least one mistake
- Student understands what to do next
- Parent/operator understands product value

## Blocker Criteria

- Student cannot understand landing
- CTA path unclear
- First lesson unclear
- Mission checker rejects correct answer
- Student cannot continue due to UI
- Analytics events missing or unusable

## Polish Criteria

- Text too long
- Button wording could be clearer
- More visual guidance needed
- Character explanation could be better
- Hint timing could be improved

## Data Collection Rules

- ❌ No child name collected
- ❌ No child email/phone collected
- ❌ No precise age collected
- ❌ No child profiles created
- ❌ No external analytics connected
- ✅ Anonymous session ID only
- ✅ Events stored in localStorage only
- ✅ Operator observation notes only

## Analytics Events Available

| Event | Trigger |
|---|---|
| `landing_opened` | User opens `/beta` |
| `demo_started` | User clicks "Начать демо" CTA |
| `lesson_started` | User opens lesson `/lesson/1-1` |
| `mission_attempted` | User submits a mission answer |
| `mission_failed` | Mission checker rejects answer |
| `mission_passed` | Mission checker accepts answer |
| `hint_used` | User opens hint |
| `lesson_completed` | User finishes all lesson tasks |

## Console Debug API

```javascript
// View all events for current session
window.__PYTHON_QUEST_ANALYTICS__.getEvents()

// Clear stored events
window.__PYTHON_QUEST_ANALYTICS__.clearEvents()
```

## Artifacts to Produce Per Session

1. Observation template (markdown) — operator notes
2. Analytics export (JSON) — via `getEvents()` after session
3. Combined into session result record

## Post-Test Questions (ask student)

1. Что было понятно?
2. Что было непонятно?
3. Где хотелось остановиться?
4. Что понравилось?
5. Что было сложно?
6. Хотелось бы продолжить завтра?

## Observer Debrief Questions

1. Was the landing clear without explanation?
2. Did student navigate independently?
3. Where did student hesitate most?
4. Were hints helpful?
5. Did checker behave correctly?
6. Would you let your child use this unsupervised?
