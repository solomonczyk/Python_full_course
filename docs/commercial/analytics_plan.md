# Python Quest Analytics Plan

## Purpose
Track product engagement, learning flow, and friction points during beta testing — without collecting personal data.

## Design Principles
- **Anonymous by design:** No personal identifiable information (PII) is stored or transmitted.
- **Minimal payload:** Only event name, anonymous session ID, and relevant lesson/mission IDs.
- **No tracking of children outside the product:** No cookies for advertising, no cross-site tracking, no social media pixels.
- **Opt-out not required during beta:** Since no personal data is collected, no consent popup is needed. (If personal data collection is added later, a separate privacy/legal layer is required.)

## Event Map

### Event: `landing_opened`
- **Trigger:** User loads the landing page.
- **Why it matters:** Measures landing page reach — how many potential students/parents discover the product.
- **Data payload:**
  ```json
  {
    "event": "landing_opened",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "referrer": "direct|search|social|unknown"
  }
  ```
- **Product question answered:** Are we driving traffic to the landing page?

### Event: `demo_started`
- **Trigger:** User clicks "Start Quest" / "See How It Works" / demo CTA.
- **Why it matters:** Conversion from landing visitor to active trial. Low rate → CTA or value proposition needs improvement.
- **Data payload:**
  ```json
  {
    "event": "demo_started",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE"
  }
  ```
- **Product question answered:** Does the landing page persuade visitors to try the product?

### Event: `quest_started`
- **Trigger:** User opens a quest (enters lesson grid for a quest).
- **Why it matters:** Indicates commitment — the student decided to begin a learning block.
- **Data payload:**
  ```json
  {
    "event": "quest_started",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "quest_id": "quest_1"
  }
  ```
- **Product question answered:** Which quests are started most/least?

### Event: `lesson_started`
- **Trigger:** User opens a lesson within a quest.
- **Why it matters:** Shows lesson-level engagement.
- **Data payload:**
  ```json
  {
    "event": "lesson_started",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "lesson_id": "1-1"
  }
  ```
- **Product question answered:** Are students starting lessons? Where do they drop off?

### Event: `mission_attempted`
- **Trigger:** User clicks "Run" or "Check" on a mission (submits code).
- **Why it matters:** Core interaction — shows the student is actively trying to write code.
- **Data payload:**
  ```json
  {
    "event": "mission_attempted",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "mission_id": "mission_1",
    "attempt_count": 1
  }
  ```
- **Product question answered:** Do students attempt missions? How many attempts per mission on average?

### Event: `mission_failed`
- **Trigger:** Mission Checker returns error / not-passed status.
- **Why it matters:** Identifies hard missions or unclear instructions.
- **Data payload:**
  ```json
  {
    "event": "mission_failed",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "mission_id": "mission_1",
    "attempt_count": 2,
    "error_type": "syntax_error|logic_error|type_error|unknown"
  }
  ```
- **Product question answered:** Which missions have the highest failure rate? Do failures cluster by concept?

### Event: `mission_passed`
- **Trigger:** Mission Checker returns success.
- **Why it matters:** Core success signal — the student understood the concept.
- **Data payload:**
  ```json
  {
    "event": "mission_passed",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "mission_id": "mission_1",
    "attempt_count": 3
  }
  ```
- **Product question answered:** What is the pass rate per mission? Average attempts-to-pass?

### Event: `hint_used`
- **Trigger:** User clicks "Hint" button during a mission.
- **Why it matters:** High hint usage on a mission suggests the concept was not explained clearly enough.
- **Data payload:**
  ```json
  {
    "event": "hint_used",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "mission_id": "mission_5",
    "hint_level": 1
  }
  ```
- **Product question answered:** Which missions require excessive hints? Are hints helpful enough?

### Event: `lesson_completed`
- **Trigger:** User completes the final mission of a lesson and sees the success screen.
- **Why it matters:** Full lesson completion is the strongest short-term engagement signal.
- **Data payload:**
  ```json
  {
    "event": "lesson_completed",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "lesson_id": "1-1"
  }
  ```
- **Product question answered:** What is the lesson completion rate? Where do students stop?

### Event: `quest_completed`
- **Trigger:** User completes all lessons in a quest.
- **Why it matters:** Major milestone — full quest completion shows sustained motivation.
- **Data payload:**
  ```json
  {
    "event": "quest_completed",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "quest_id": "quest_1"
  }
  ```
- **Product question answered:** What is the quest completion rate? Which quest is hardest to finish?

### Event: `student_stuck`
- **Trigger:** User has failed a mission 5+ times consecutively, OR spends >10 minutes on one mission without passing.
- **Why it matters:** Flags content that is genuinely blocking progress — beyond normal difficulty.
- **Data payload:**
  ```json
  {
    "event": "student_stuck",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "mission_id": "mission_7",
    "total_attempts": 7,
    "time_spent_minutes": 12
  }
  ```
- **Product question answered:** Where is the course broken for some students?

### Event: `session_abandoned`
- **Trigger:** No user activity for 15+ minutes after a lesson_started or mission_attempted (not caused by normal lesson content consumption).
- **Why it matters:** Measures where students lose motivation or get interrupted.
- **Data payload:**
  ```json
  {
    "event": "session_abandoned",
    "anonymous_session_id": "generated_id",
    "timestamp": "ISO_DATE",
    "last_lesson_id": "2-5",
    "last_mission_id": "mission_14",
    "session_duration_minutes": 18
  }
  ```
- **Product question answered:** Where in the course do students abandon sessions most often?

## Implementation Priority

| Event | Priority for beta | Implementation |
|-------|-------------------|----------------|
| `lesson_started` | P0 — must have | Frontend event on lesson mount |
| `mission_attempted` | P0 — must have | Frontend event on mission submit |
| `mission_passed` | P0 — must have | Frontend event on mission success |
| `mission_failed` | P0 — must have | Frontend event on mission failure |
| `lesson_completed` | P0 — must have | Frontend event on lesson completion |
| `quest_started` | P1 — important | Frontend event on quest open |
| `quest_completed` | P1 — important | Frontend event on quest completion |
| `landing_opened` | P1 — important | Frontend event on landing page load |
| `demo_started` | P1 — important | Frontend event on demo CTA click |
| `hint_used` | P1 — important | Frontend event on hint button click |
| `student_stuck` | P2 — nice to have | Frontend check after 5 failures or 10 min |
| `session_abandoned` | P2 — nice to have | Backend/heartbeat check or frontend idle timer |

## Data Collection Method

During beta, events can be collected via:
1. **Simple POST to a beta analytics endpoint** (in-memory or log-file storage, no database required).
2. **Console-log based recording** for manually observed test sessions.
3. **Spreadsheet recording** for in-person beta tests with observer notes.

No third-party analytics SDK is required at beta stage.

## Forbidden Payloads
The following must never be included in analytics events without a separate privacy/legal layer:
```json
{
  "child_full_name": "...",
  "email": "...",
  "phone": "...",
  "precise_age": "...",
  "ip_address": "...",
  "cookie_id": "..."
}
```

## Missing Items (Future Layers)
- User account linking (requires privacy/legal layer).
- Cross-session student progress persistence (requires accounts).
- Funnel analysis with cohort tracking (requires accounts).
- A/B test event tracking (requires full platform).
