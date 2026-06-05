# First Staged Beta Batch 5–10

## Goal

Run the first controlled beta group with 5–10 real participants using the verified production infrastructure (Turso persistence, staged access, OPERATOR_KEY gate). Prove that the first real beta batch can be operated safely, manually, and without collecting child personal data.

## Batch Size

| Dimension | Value |
|---|---|
| Minimum participants | 5 |
| Maximum participants | 10 |
| Target | 7–8 |

## Participant Labels

Use participant labels only — no personal identifiers.

| Label | Optional? | Notes |
|---|---|---|
| STU-001 | Required | First participant |
| STU-002 | Required | Second participant |
| STU-003 | Required | Third participant |
| STU-004 | Required | Fourth participant |
| STU-005 | Required | Fifth participant (minimum reached) |
| STU-006 | Optional | Expand as needed |
| STU-007 | Optional | Expand as needed |
| STU-008 | Optional | Expand as needed |
| STU-009 | Optional | Expand as needed |
| STU-010 | Optional | Batch maximum |

## Data Policy

### Allowed (tracked per participant)

- Participant label (e.g., STU-001)
- Beta code reference (not the secret — a hash or reference)
- Current stage (1–5)
- Part progress (started/not started, completed lessons count)
- Feedback received (yes/no)
- Unlock decision (approved/held/stopped)
- Browser/device type (optional, anonymous)
- Parent/operator feedback text (submitted via feedback form)
- Issues reported (blocker/major/minor/polish)

### Forbidden (never collect)

- Child full name
- Child email address
- Child phone number
- Precise age or birthdate
- Home address
- School name or class
- Photo, audio, or video of the child
- Personal identification numbers

### Allowed from parent (optional, manual, outside the product)

- Parent contact info (only what they choose to share)
- Parent name (only for communication, never stored in the product)

## Access Model

The course has 5 parts. Staged access means not all parts are open at once:

| Stage | Content Parts | Opens When |
|---|---|---|
| 1 | Part 1 | Immediately with a valid beta code |
| 2 | Parts 1–2 | After feedback + operator unlock |
| 3 | Parts 1–3 | After feedback + operator unlock |
| 4 | Parts 1–4 | After feedback + operator unlock |
| 5 | Parts 1–5 | After feedback + operator unlock |

### Locked Lesson Behavior

When a lesson is locked:
- The lesson is marked as `locked: true` in the lessons data
- The frontend should show the lesson as inaccessible
- Direct URL access to a locked lesson should be blocked
- The API returns the lesson data but the frontend enforces access control based on the participant's current stage

## Participant Lifecycle

```
Screening → Invitation → Beta Code Issued → Part 1 Started
  → Part 1 Completed → Feedback Requested → Feedback Received
  → Operator Review → Unlock Decision → Part 2+ Opened
```

## Success Criteria

| Criterion | Target | Minimum |
|---|---|---|
| Participants recruited | 7–8 | 5 |
| Participants started Part 1 | 7 | 5 |
| Part 1 completed | 5 | 3 |
| Feedback received | 5 | 3 |
| Part 2 unlocked | 3 | 2 |
| No critical blockers | 0 | 0 |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Participants don't complete Part 1 | Medium | Low | Focus on engaged families, check in after 3 days |
| Technical blockers found | Medium | Medium | Have fix + redeploy plan ready (1–2 day turnaround) |
| Beta codes shared publicly | Low | High | Issue codes privately, monitor for abuse |
| Parents misunderstand beta scope | Medium | Medium | Clear screening, staged access explanation in invitation |
| Vercel auth blocks participant | Low | High | Test access before issuing codes; use Protection Bypass if needed |

## Operator Safety Rules

1. **Never commit OPERATOR_KEY** — The key is set via environment variable. Never paste it into code, config files, or version control.
2. **Never use default dev key in production** — The default `op-python-quest-dev-2026` is for local development only. Production must have a unique `OPERATOR_KEY` set.
3. **Never collect child personal data** — Do not ask for or store child name, email, phone, precise age, address, or school.
4. **Never unlock without feedback** — Feedback is required before any stage unlock.
5. **Never promise full product** — Participants are in a beta. Do not promise certificates, complete courses, or future paid features.
6. **Never call this mass paid launch** — This is a controlled staged beta with 5–10 participants.
