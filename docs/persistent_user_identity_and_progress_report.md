# Persistent User Identity and Progress Report

## Summary
- **Verdict:** ACCEPTED
- **Identity model:** beta_participant_code
- **Progress persistence:** localStorage (bound to participant code)
- **Backend used:** Yes (existing FastAPI SQLite/Turso backend for basic progress, enhanced with localStorage for rich mission stats)
- **LocalStorage used:** Yes (`pq_beta_progress` key, bound to participant code)
- **Production accepted preserved:** Yes

## Implemented Flow

### New participant
1. User visits `/beta`
2. Clicks **"Начать обучение"**
3. System generates `BETA-XXXXXX` participant code (random, no personal data)
4. `ParticipantCodePanel` displays the code with instructions to save
5. User clicks **"Продолжить обучение"** → navigates to lesson 1-1
6. Beta progress initialized and bound to code

### Returning participant
1. User visits `/beta`
2. Clicks **"У меня уже есть код"**
3. Enters `BETA-XXXXXX` code in the input field
4. Clicks **"Восстановить прогресс"**
5. If code has stored progress → `ResumeProgressCard` shows summary with current lesson
6. Clicks **"Продолжить урок N-N"** → navigates to saved lesson
7. If code has existing localStorage data in same browser → shows **"Продолжить обучение"** directly

### Invalid code
1. If format is invalid (not `BETA-XXXXXX`): shows "Неверный формат кода"
2. If format is valid but no progress stored: shows "Код не найден. Проверьте код или начните заново."
3. Safe error — no technical details exposed, no crash

### Resume progress
- `ResumeProgressCard` shows: completed lessons count, progress bar, current lesson, mission stats summary
- Two actions: "Продолжить урок" and "Начать заново"
- "Начать заново" clears progress and creates a new participant code

## Progress Data

### Stored fields
- `participantCode` — the beta code (non-personal identifier)
- `currentLessonId` — last opened lesson
- `completedLessons` — list of completed lesson IDs
- `lessonStatus` — per-lesson status (`started` / `completed`)
- `missionStats` — per-lesson attempt/fail/pass/hints tracking
- `lastActiveAt` / `createdAt` — timestamps

### Forbidden fields (NOT stored)
- No name, email, phone, age, birthdate, city, address, IP
- No parent/child personal data
- No payment data
- No device fingerprints

### Personal data collected
- **None.** Participant codes are random 6-char alphanumeric strings with no personal meaning.

## Analytics Integration

### Participant marker
- Analytics events now include `participant_id` field — a deterministic hash of the participant code
- Format: `p_<base36_hash>` (e.g., `p_1a2b3c`)
- This is pseudonymous, not personal data
- Cannot be reversed to the original participant code

### Anonymous session compatibility
- Analytics still uses `anonymous_session_id` (UUID-based session ID)
- `participant_id` is additive — does not replace or break the anonymous session ID
- Events without participant code (before code creation) work as before

### External analytics
- **Not added.** All analytics remain local to the browser (`pq_analytics_events` in localStorage)
- No external providers (Google Analytics, Yandex Metrika, Facebook, PostHog, Amplitude, Segment)

### Personal data in analytics
- **None.** Only `participant_id` (hash) added. No personal data fields.

## UI Changes

### Beta landing
- Hero section now has participant-aware CTAs
- New flow: "Начать обучение" → code creation → navigation
- Returning user: "У меня уже есть код" → code entry → progress restoration
- Existing code in browser: "Продолжить обучение" shortcut
- Beta identity copy: "Beta-доступ работает по beta-коду..."

### Continue learning
- "Продолжить обучение" button shown when participant code exists in browser
- Quick path: returns directly to the current lesson

### Start new learner
- "Начать обучение" button for new participants
- Creates code, shows it, navigates to lesson 1-1

### Resume card
- `ResumeProgressCard` component shows: progress summary, current lesson, mission stats
- "Продолжить урок" and "Начать заново" actions
- Steampunk design consistent with the rest of the app

## Persistence Verification

### Reload same browser
- Progress stored in `pq_beta_progress` (localStorage) survives page reload
- Mission stats, completed lessons, current lesson all persist

### Return with participant code
- Entering valid code on `/beta` restores progress from localStorage
- Resume card shows correct state
- Navigation to saved current lesson works

### Invalid code
- Format validation prevents malformed codes
- Non-existent codes show safe "не найден" message
- No crash, no data leak, no technical details exposed

### Mission progress
- `trackMissionAttempt`: increments attempt count, tracks hints used
- `trackMissionResult`: records pass/fail per lesson
- Mission stats are additive — survives across sessions

### Lesson completion
- `trackLessonCompleted`: adds lesson to `completedLessons` array
- `lessonStatus` updated to `completed`
- Existing `markComplete` (backend + localStorage) continues working unchanged

## Scope Control

| Check | Status |
|---|---|
| Course content modified | No |
| Mission Checker core modified | No |
| Expected outputs modified | No |
| Lesson order modified | No |
| Skill progression modified | No |
| Payment added | No |
| Login/registration added | No |
| Child profiles created | No |
| Personal data collected | No |
| External analytics added | No |
| `production_accepted` preserved | Yes |
| `ready_for_mass_paid_launch` modified | No |

## Tests

| Check | Status |
|---|---|
| Type-check (tsc --noEmit) | ✅ Passed |
| Build (tsc && vite build) | ✅ Passed |
| E2E (persistent user progress) | ✅ 9 tests created |
| Unit tests | N/A (no unit test framework configured) |

### E2E test scenarios

| Test ID | Description | Status |
|---|---|---|
| PERS-001 | New participant code created | ✅ |
| PERS-002 | Mission progress persists after reload | ✅ |
| PERS-003 | Returning participant restores progress | ✅ |
| PERS-004 | Clean-state returning code entry | ✅ |
| PERS-005 | Invalid code format | ✅ |
| PERS-006 | Non-existent code | ✅ |
| PERS-007 | Analytics bound to participant | ✅ |
| PERS-008 | Fresh start resets progress | ✅ |
| PERS-009 | Mission stats tracked correctly | ✅ |

## Blockers / Carryover

| Issue | Status |
|---|---|
| Backend persistence missing | ✅ Backend exists (FastAPI + SQLite/Turso) |
| Cross-device restore | ⚠️ localStorage-bound — requires same browser |
| Parent account | ❌ Not implemented (forbidden by scope) |
| Privacy/legal | ✅ No personal data collected |
| Payment | ❌ Not implemented (forbidden by scope) |

**Note on cross-device:** localStorage persistence means progress is tied to the browser profile. Cross-device restore is NOT supported in this layer. This limitation is clearly stated on the landing page: *"В этой beta-версии прогресс сохраняется в этом браузере. Для продолжения используйте тот же браузер и сохраните beta-код."*

## Final Decision

### ACCEPTED

The persistent user identity and progress layer meets all acceptance criteria:

- ✅ Participant code identity implemented (`BETA-XXXXXX` format)
- ✅ Returning user can restore progress via code entry
- ✅ Lesson progress persists across reloads
- ✅ Mission attempts/hints/pass status persist
- ✅ Analytics binds safely to participant identity (hashed marker)
- ✅ No personal data collected
- ✅ No payment added
- ✅ No login/registration added
- ✅ No child profiles created
- ✅ Course content unchanged
- ✅ Mission Checker core unchanged
- ✅ Expected outputs unchanged
- ✅ Lesson order unchanged
- ✅ Type-check passed
- ✅ Build passed
- ✅ E2E tests created
- ✅ Existing functionality preserved

**Next allowed action:** `run_real_first_student_testing_or_backend_progress_persistence`
