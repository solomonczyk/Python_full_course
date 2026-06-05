# First Batch Feedback and Unlock Flow

## Overview

This document describes the feedback collection and staged unlock process for the first beta batch. Feedback is required before any stage unlock. This ensures quality control and gives the operator the information needed to make safe unlock decisions.

## When Feedback Is Requested

Feedback is requested after the participant completes Part 1 (or reaches the end of currently available content for their stage).

| Trigger | Action |
|---|---|
| Participant completes Part 1 (reaches end of stage 1 content) | Operator sends feedback form link to parent |
| Participant has been active for 5+ days without completing Part 1 | Operator checks in, may still request partial feedback |
| Parent reports that child is done (regardless of progress) | Operator sends feedback form |
| Participant stops using the course for 7+ days | Operator checks in, may request exit feedback |

## Feedback Questions

The feedback form asks the following questions:

1. **Overall rating** — How would you rate your child's experience with Part 1? (1–5 stars)
2. **What went well** — What did your child enjoy? What was clear and easy to follow?
3. **Where did they get stuck?** — Were there any lessons, missions, or concepts that were confusing?
4. **Does your child want to continue?** — (Yes / Yes, but needs a break / Not sure / No)
5. **Any issues or suggestions?** — Free text for anything that broke, could be improved, or general thoughts

### Minimal Feedback Requirements

For a feedback submission to be considered valid, it must:
- Be at least 10 characters of meaningful text
- Include an answer to at least 2 of the 5 questions
- Not be spam, empty, or auto-generated

## Who Reviews Feedback

**The operator** — the person managing the beta batch. No automated unlock decisions are made.

The operator:
- Reads each feedback submission attentively
- Notes any issues, blockers, or concerns
- Checks if the unlock criteria are met
- Makes the final unlock decision

## Unlock Criteria

**All criteria must be met** for a stage unlock:

| # | Criterion | How to Verify |
|---|---|---|
| 1 | Part 1 completed or attempted enough | Check participant's progress data |
| 2 | Feedback received | Check `feedback_submitted` flag in database |
| 3 | No critical blocker | Review feedback and issue registry for any CRITICAL or MAJOR issues |
| 4 | Parent/operator agrees to continue | Parent's feedback indicates willingness to continue |
| 5 | Student wants to continue | Feedback question #4 answered "Yes" or "Yes, but needs a break" |

### Additional Unlock Rules

- The operator may apply discretion if criteria 4–5 are met but the feedback text reveals a concern not captured by the criteria
- If the operator is unsure, they may contact the parent for clarification before unlocking
- If a product blocker was found, it must be fixed and redeployed before any unlock
- Unlock is per-participant — one participant's blocker doesn't block others (unless it's a systemic issue)

## Unlock Decision Flow

```
Feedback received?
├── No → Request feedback from parent
└── Yes →
    Review feedback content
    Check for blockers
    ├── Critical blocker found?
    │   ├── Yes → Do NOT unlock. Fix blocker first.
    │   └── No →
    │       Parent agrees to continue and student wants to continue?
    │       ├── No → Do NOT unlock. Discuss with parent.
    │       └── Yes →
    │           Execute operator-unlock API:
    │           curl -X POST -H "X-Operator-Key: $OPERATOR_KEY" \
    │             https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/CODE/operator-unlock
    │           Record decision
    │           Notify parent
```

## Stop Conditions

The participant's access should be stopped (not unlocked) under these conditions:

| Condition | Action |
|---|---|
| Critical blocker found (systemic) | Stop all unlocks, fix blocker |
| Parent explicitly withdraws | Mark as withdrawn, stop access |
| Code compromised | Issue new code or stop access |
| Violation of beta terms | Stop access, document reason |
| Repeated feedback indicates the product is not ready for this child | Recommend waiting for release |

## Issue Severity Levels

When reviewing feedback, classify any reported issues:

| Severity | Definition | Unlock Impact |
|---|---|---|
| **Blocker / Critical** | Prevents progression — blank page, crash, wrong answer marked correct, locked lesson accessible without unlock | **Must fix** before any unlock |
| **Major** | Serious usability issue but has a workaround — confusing flow, misleading text, broken navigation | Should fix before unlock, may unlock with explicit parent awareness |
| **Minor** | Visual or wording issue — typo, alignment, unclear but not blocking | Note for fix, does not block unlock |
| **Polish** | Nice-to-have improvement — could be better but works fine | Log for later, does not block unlock |

### How to Record Issues

Maintain an issue registry (separate from code tracker) with:

```
- participant_label: STU-001
- severity: major
- description: "Mission 3-5 checker rejects correct answer when input contains Cyrillic characters"
- reported_at: 2026-06-05
- status: open / fixed / won't fix
- unlock_blocked: true / false
```

## Technical Flow for Unlock

### Check participant's current stage

```bash
curl https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/STU-001
```

### View pending feedback (operator only)

```bash
curl -H "X-Operator-Key: $OPERATOR_KEY" \
  https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/operator/pending-feedback
```

### Execute unlock (operator only)

```bash
curl -X POST -H "X-Operator-Key: $OPERATOR_KEY" \
  https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/BETA-CODE/operator-unlock
```

**Never include the real OPERATOR_KEY in this document or any Git-tracked file.**

## Decision Record Format

After each unlock decision, record it in the operator notes (outside the product):

```json
{
  "participant_label": "STU-001",
  "beta_code_ref": "BETA-XXXXXX",
  "current_stage": 1,
  "part_1_completed": true,
  "feedback_received": true,
  "issues": [],
  "operator_decision": "unlock_to_stage_2",
  "decision_reason": "Part 1 completed, positive feedback, student eager to continue. No blockers."
}
```

## After Unlock

1. Notify the parent via their preferred channel
2. Confirm they can see the new content
3. Reset for next unlock cycle (Part 3 unlock requires feedback on Part 2)
4. Update the batch tracker
