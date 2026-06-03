# Synthetic Beta E2E Journey Plan

## Goal
Verify the beta journey technically before real student testing.

## What This Test Can Prove
- Route works
- CTA works
- Mission submit flow works
- Fail/pass analytics works
- Hint analytics works
- Lesson completion analytics works
- Local analytics export works
- Analytics debug API is available and functional
- No external analytics requests are made
- No personal data is collected in analytics payload

## What This Test Cannot Prove
- Real children understand the course
- Real students enjoy the product
- Real users want to continue
- Product-market fit
- Readiness for mass paid launch
- Real student comprehension or motivation
- Parent value perception

## Synthetic Personas

| ID | Type | Purpose |
|---|---|---|
| SYN-001 | fast_success | Happy path: beta → demo → correct answer → complete |
| SYN-002 | one_error_then_success | Error recovery: wrong → feedback → correct |
| SYN-003 | multiple_errors_then_success | Progressive hints: 3+ errors → hints → success |
| SYN-004 | multiple_errors_then_abandon | Session abandon after repeated failures |
| SYN-005 | landing_open_no_demo | Landing page view without CTA click |
| SYN-006 | demo_open_no_mission_attempt | Lesson view without code submission |
| SYN-007 | hint_after_first_fail | Hint fires on first mission failure |
| SYN-008 | never_uses_hint | No hint when mission passed first try |
| SYN-009 | refresh_mid_lesson | Analytics persists after page refresh |
| SYN-010 | mobile_small_screen_path | Mobile viewport renders correctly |

## E2E Scenarios

1. **Fast success** (SYN-001): `/beta` → click CTA → `/lesson/1-1` → submit correct answer → complete
2. **Error recovery** (SYN-002): `/beta` → demo → lesson → wrong answer → hint → correct answer
3. **Multiple failures** (SYN-003): lesson → 3 wrong answers → analytics counts verified
4. **Landing abandon** (SYN-005): open `/beta`, do not click CTA → only `landing_opened` event
5. **Demo open no attempt** (SYN-006): `/beta` → demo → lesson → no submit → no `mission_attempted`
6. **Mobile path** (SYN-010): 375×667 viewport → beta readable → CTA tappable → lesson accessible
7. **Analytics debug API** (all): verify `window.__PYTHON_QUEST_ANALYTICS__` exists and returns events
8. **No external analytics** (all): intercept network requests → fail on analytics domains
9. **No personal data** (all): inspect all payload fields → fail on name/email/phone/age/IP

## Analytics Validation

Required events for a full journey:
- `landing_opened` — fired on `/beta` page mount
- `demo_started` — fired on CTA click
- `lesson_started` — fired on lesson page mount
- `mission_attempted` — fired on mission submit button click
- `mission_failed` — fired on incorrect mission result
- `mission_passed` — fired on correct mission result
- `hint_used` — fired when adaptive feedback shows error hints
- `lesson_completed` — fired on mission success via `onComplete` callback

Event payload fields allowed:
- `event`, `anonymous_session_id`, `timestamp`
- `lesson_id`, `mission_id`, `attempt_count`, `result`, `hint_id`, `source`, `route`

## Safety Validation
- No personal data fields (name, email, phone, age, city, IP, etc.)
- No external analytics domains (google-analytics, yandex, facebook, posthog, etc.)
- No payment system
- No child profiles
- No login/registration

## Acceptance Criteria
- All E2E tests pass
- Required analytics events are present for each scenario
- No forbidden payload fields detected
- No external analytics requests detected
- Analytics debug API is functional
- localStorage persistence works correctly
- Events survive page refresh

## Test Setup
- E2E framework: Playwright with Chromium
- App server: Vite dev server (started automatically by Playwright webServer config)
- Mission API: mocked via `page.route()` to avoid backend dependency
- Config file: `frontend/playwright.config.ts`
- Test file: `tests/e2e/synthetic_beta_journey.spec.ts`
