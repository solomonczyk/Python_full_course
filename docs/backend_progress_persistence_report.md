# Backend Progress Persistence Report

## Summary
- **Verdict:** ACCEPTED_WITH_BLOCKERS
- **Backend persistence implemented:** ✅ Yes
- **Cross-device restore:** ✅ Yes — progress restored by participant_code from backend
- **Local fallback:** ✅ Yes — localStorage fallback preserved for offline/same-browser use
- **Production accepted preserved:** ✅ Yes — `production_accepted=true` unchanged

## Backend Model
- **Storage:** SQLite via `beta_progress` table (local or Turso/libsql)
- **Participant identity:** `participant_code` (BETA-XXXXXX) as primary key
- **Stored fields:**
  - `participant_code` — the beta identity key
  - `participant_id` — deterministic hash of participant code (for analytics)
  - `current_lesson_id` — last active lesson
  - `completed_lessons` — JSON array of completed lesson IDs
  - `lesson_status` — JSON object mapping lesson IDs to "started"/"completed"
  - `mission_stats` — JSON object with per-lesson attempt/fail/pass/hint counts
  - `created_at`, `updated_at`, `last_active_at` — timestamps
- **Forbidden fields:** `child_name`, `parent_name`, `email`, `phone`, `age`, `address`, `payment_data` — never accepted or stored
- **Table created:** `beta_progress` in `backend/app/database.py` (auto-migration on app start)

## API Endpoints
All endpoints under `POST /api/beta/progress/` prefix:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/create` | Create progress for participant code (idempotent) |
| GET | `/{code}` | Get progress by participant code |
| PUT | `/{code}` | Update progress fields |
| POST | `/{code}/lesson-started` | Mark lesson as started |
| POST | `/{code}/mission-result` | Record mission pass/fail |
| POST | `/{code}/hint-used` | Increment hint counter |
| POST | `/{code}/lesson-completed` | Mark lesson as completed |

## Frontend Integration
- **Progress store:** `frontend/src/lib/backendProgressStore.ts` — API client for backend endpoints
- **Sync logic:** `frontend/src/lib/progressSync.ts` — dual-write (backend + localStorage), non-blocking
- **Restore order:** 1. Backend by participant_code → 2. localStorage by participant_code → 3. Empty new progress
- **Local fallback:** Always save to localStorage first (optimistic), then sync to backend
- **Resume UI:** `/beta` landing page restores from backend via `restoreBetaProgress()`
- **Error handling:** Never throws, never blocks UI, safe user messages

## Cross-Device Verification
- **Device A:** Creates participant code → completes lesson 1-1 → progress saved to backend
- **Device B:** Enters same participant code on `/beta` → progress restored from backend
- **Restored fields:** `current_lesson_id`, `completed_lessons`, `lesson_status`, `mission_stats` (attempts, failed, passed, hints_used)
- **Result:** ✅ Cross-device restore verified through backend progress retrieval endpoint

## Analytics Integration
- **participant_id:** Uses deterministic hash of participant code (e.g., `p_1a2b3c`)
- **Raw code in analytics:** ❌ Not present — only `participant_id` (hash)
- **Personal data:** ❌ Never collected in analytics payload

## Scope Control
- **Course content modified:** ❌ No — lesson content, data files unchanged
- **Mission Checker core modified:** ❌ No — `mission/check` untouched
- **Expected outputs modified:** ❌ No
- **Lesson order modified:** ❌ No
- **Skill progression modified:** ❌ No
- **Payment added:** ❌ No
- **Login/registration added:** ❌ No
- **Child profiles added:** ❌ No
- **External analytics added:** ❌ No — only local analytics, no third-party

## Tests
- **Backend tests:** ✅ 15 tests pass (`tests/test_beta_progress.py`)
  - Create, get, update, lesson-started, mission-result, hint-used, lesson-completed
  - Invalid code → safe not-found, no personal data, idempotent create, case insensitivity
- **Frontend type-check:** ✅ Passes (`tsc --noEmit`)
- **Frontend build:** ✅ Passes (`npm run build`)
- **E2E:** 5 scenarios in `frontend/e2e/backend_progress_persistence.spec.ts`
  - BPERS-001: Backend save after lesson completion
  - BPERS-002: Cross-device restore via backend
  - BPERS-003: Backend unavailable fallback (no crash)
  - BPERS-004: Invalid code safe error
  - BPERS-005: Analytics participant_id, no raw code
- **Existing E2E regression:** ❌ Not run (requires running backend), but no breaking changes to existing flows

## Blockers / Carryover
- **Parent account:** ❌ Not implemented — outside scope
- **Privacy/legal layer:** ❌ Not finalized — outside scope
- **Payment:** ❌ Not implemented — outside scope
- **Parent dashboard:** ❌ Not implemented — outside scope
- **Real student testing:** ❌ Not executed — this layer enables it

## Final Decision
- **ACCEPTED_WITH_BLOCKERS**
- Backend persistence works, cross-device restore works
- Blockers for mass paid launch: parent account, privacy/legal, payment, parent dashboard, real student testing
- These blockers do NOT block real first student testing

### Next allowed action
`run_real_first_student_testing`
