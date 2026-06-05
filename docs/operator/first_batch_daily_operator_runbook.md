# First Batch Daily Operator Runbook

## Overview

Daily runbook for the operator managing the first staged beta batch (5–10 participants). Follow these steps each day the beta is active.

## Prerequisites

- Vercel CLI installed and authenticated
- `OPERATOR_KEY` available as environment variable (never hardcoded)
- Access to participant tracker (private, not in Git)
- Access to feedback form results

## Daily Flow

### 1. Check Production Health

Verify the production API is running and healthy.

```bash
# Check root endpoint
vercel curl https://python-full-course-andy-s-projects26.vercel.app/api/health

# Expected: {"status":"healthy"}

# Check persistence backend
vercel curl https://python-full-course-andy-s-projects26.vercel.app/api/health/persistence

# Expected: {"backend":"turso","environment":"production",...,"safe_for_beta_progress":true}
```

If either check fails:
- **health endpoint fails**: Check Vercel deployment status (`vercel list`), check GitHub Actions for recent failed deployments
- **turso not available**: Check Turso database status, check TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are set in Vercel env

### 2. Check Pending Feedback

List participants who have submitted feedback and are waiting for unlock.

```bash
vercel curl -H "X-Operator-Key: $OPERATOR_KEY" \
  https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/operator/pending-feedback
```

Expected response:
```json
{
  "ok": true,
  "pending": [
    {
      "participant_code": "BETA-XXXXXX",
      "current_stage": 1,
      "feedback_text": "...",
      "feedback_rating": 4,
      "feedback_submitted_at": "2026-06-05T12:00:00"
    }
  ]
}
```

If no pending feedback:
- Check if any participants have recently completed Part 1
- Send feedback form to those who completed Part 1 but haven't submitted feedback

### 3. Check Participant Progress

Check each active participant's current stage and progress.

```bash
# For each active participant:
vercel curl https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/BETA-CODE
vercel curl https://python-full-course-andy-s-projects26.vercel.app/api/beta/progress/BETA-CODE
```

Look for:
- Participants who haven't started (created but no progress)
- Participants making steady progress
- Participants who stopped mid-Part 1
- Participants who completed Part 1

### 4. Review Reported Issues

Check the issue registry for any new issues reported by participants.

Review areas:
- Any critical or major blockers reported?
- Are issues systemic (affecting multiple participants) or isolated?
- Does any issue block unlock decisions?

### 5. Decide Unlock / Hold / Stop

For each participant with pending feedback:

1. Read the feedback text carefully
2. Check unlock criteria:
   - [ ] Part 1 completed or attempted enough
   - [ ] Feedback received
   - [ ] No critical blocker
   - [ ] Parent agrees to continue
   - [ ] Student wants to continue
3. Make decision:

| Decision | Action |
|---|---|
| **unlock** | Execute unlock API, notify parent |
| **hold** | Do not unlock yet, explain why to parent, set conditions |
| **pause** | Pause participation, check back later |
| **stop** | End participation, document reason |

### 6. Record Decision

Record each decision in the operator tracker (outside the product):

```json
{
  "timestamp": "2026-06-05",
  "operator": "manual",
  "participant_label": "STU-001",
  "current_stage": 1,
  "decision": "unlock_to_stage_2",
  "reason": "Completed Part 1, positive feedback, no blockers",
  "issues_found": []
}
```

## Quick Reference: API Endpoints

| Action | Command |
|---|---|
| Check health | `vercel curl https://python-full-course-andy-s-projects26.vercel.app/api/health` |
| Check persistence | `vercel curl https://python-full-course-andy-s-projects26.vercel.app/api/health/persistence` |
| Check participant stage | `vercel curl https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/BETA_CODE` |
| Check participant progress | `vercel curl https://python-full-course-andy-s-projects26.vercel.app/api/beta/progress/BETA_CODE` |
| List pending feedback | `vercel curl -H "X-Operator-Key: $OPERATOR_KEY" https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/operator/pending-feedback` |
| Unlock next stage | `vercel curl -X POST -H "X-Operator-Key: $OPERATOR_KEY" https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/BETA_CODE/operator-unlock` |
| Submit feedback (test) | `curl -X POST -H "Content-Type: application/json" -d '{"feedback_text":"Test feedback","rating":4}' https://python-full-course-andy-s-projects26.vercel.app/api/beta/access/BETA_CODE/provide-feedback` (use vercel curl for production) |

## Safety Rules

1. **Never expose OPERATOR_KEY** — not in docs, not in code, not in logs, not in screenshots
2. **Never collect child personal data** — labels only, no names/emails/phones/ages
3. **Never unlock without feedback** — feedback is required before any stage unlock
4. **Never bypass staged access** — don't manually set stages in the database
5. **Never promise full course access** — this is a staged beta
6. **Use BETA_CODE_PLACEHOLDER** in any shared examples, never real codes

## Incident Response

| Incident | Immediate Action | Follow-up |
|---|---|---|
| Production down | Check Vercel dashboard, redeploy if needed | Investigate root cause |
| Participant can't access | Confirm code is correct, check browser | Verify in logs |
| Locked lesson accessible | **Critical blocker** — stop beta, fix access control | Redeploy, verify fix |
| Mission checker wrong | Log as product blocker, do not unlock | Fix code, redeploy |
| Data breach suspicion | Pause beta, investigate | Report if confirmed |
| Parent complaint | Listen, clarify, escalate if needed | Document outcome |
