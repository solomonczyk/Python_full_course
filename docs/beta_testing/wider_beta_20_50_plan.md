# Wider Controlled Beta 20–50 Plan

## Goal
Validate Python Quest after first beta stabilization on a larger controlled group of 20–50 real (synthetic) students. Confirm all blocker fixes from FST-0001 through FST-0007 hold at scale, verify analytics export pipeline, and build confidence for commercial beta offer decision.

## Test Group

| Attribute | Value |
|---|---|
| **Target number** | 50 |
| **Minimum acceptable number** | 20 |
| **Beginner level** | True — all participants start at lesson 1-1 with no prior Python knowledge assumed |
| **Parent/operator observation** | Simulated teacher/operator monitors progress via backend analytics export dashboard |
| **Device/browser spread** | Desktop Chrome (primary), Chromium-based browsers (Edge), mobile viewport tested via SYN-010 |

## Test Scope

| Area | Coverage |
|---|---|
| **/beta landing** | Full page load, hero section, CTAs, FAQ, how-it-works, audience targeting |
| **beta-code creation** | Generate unique BETA-XXXXXX code, display with copy button, store in localStorage and backend |
| **returning user restore** | Enter existing beta-code on /beta → restore progress from backend → ResumeProgressCard |
| **lesson 1-1** | Full lesson flow: explanation → quiz → glitch trap → mission → practice task → next lesson navigation |
| **first mission** | Submit Python code → mission checker evaluates → pass/fail result → stats tracked |
| **early learning path** | Lesson 1-1 → lesson 1-2 progression, accumulated progress across lessons |
| **progress restore** | localStorage persistence across refresh, backend restore across devices |
| **analytics export** | All 8 event types captured, analytics export endpoint returns aggregated data, no personal data in payload |

## Success Criteria

| Criterion | Threshold |
|---|---|
| Can start without adult technical help | 80%+ |
| Complete first mission | 70%+ |
| Complete target early path (lesson 1-1) | 60%+ |
| Beta-code creation works | 90%+ |
| Backend progress restore works | 90%+ |
| Critical blockers | 0 |
| Repeated major blockers affecting >20% of users | 0 |

## Blocker Criteria

| Scenario | Blocker? |
|---|---|
| Mission checker rejects correct answer | 🔴 Critical |
| Progress restore fails repeatedly | 🔴 Critical |
| Beta-code flow breaks | 🔴 Critical |
| Onboarding blocks start | 🟠 Major |
| Lesson route/navigation breaks | 🟠 Major |
| Analytics missing core events | 🟡 Minor |

## Decision Criteria

| Outcome | When |
|---|---|
| **ready_for_commercial_beta_offer** | ≥20 students tested, 0 critical blockers, no repeated major blockers, analytics + issue registry created, production_accepted preserved, git clean |
| **needs_corrective_product_pass** | ≥20 students tested, analytics collected, but repeated major issues found that need a corrective pass before commercial beta |
| **needs_course_flow_review** | Issues found in lesson content, mission checker, or learning path that require review before expansion |
| **needs_infrastructure_pass** | Backend persistence, analytics export, or beta-code generation fail at scale |

## Test Execution Protocol

1. Generate 50 unique beta codes (WB-001 through WB-050)
2. For each participant, execute the standard journey:
   - Open `/beta` → verify landing renders
   - Click "Начать обучение" → verify beta-code generated and displayed
   - Click "Продолжить обучение" → navigate to onboarding or lesson
   - Complete onboarding (all 3 steps or skip)
   - Navigate to lesson 1-1
   - Read lesson content, answer quiz, complete glitch trap
   - Submit mission (try correct and incorrect answers)
   - Verify mission result displayed
   - Complete lesson
   - Verify progress persisted (localStorage + backend)
   - Verify returning user can restore progress
3. Export analytics for aggregated view
4. Classify all issues in registry
5. Produce final report with verdict

## Safety / Scope Constraints

| Constraint | Status |
|---|---|
| Course content modified | ❌ No |
| Mission Checker expected outputs modified | ❌ No |
| Lesson order modified | ❌ No |
| Skill progression modified | ❌ No |
| Payment added | ❌ No |
| Login/password added | ❌ No |
| Personal data collected | ❌ No |
| Child profiles created | ❌ No |
| External analytics provider | ❌ No |
