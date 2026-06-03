# Staged Beta Operator Runbook

## Goal
Run the first staged beta group manually and safely.

## Daily Operator Flow
1. **Check candidates** — Review new candidate inquiries from outreach channels
2. **Invite selected participants** — Send invitation to screened and approved candidates
3. **Issue beta code** — Generate unique code, deliver to parent, confirm access works
4. **Confirm Part 1 access** — Verify participant can open the course and see Part 1
5. **Monitor progress** — Check which participants have started/completed lessons
6. **Collect feedback** — Request feedback form after Part 1 completion
7. **Review unlock criteria** — Evaluate feedback against unlock rules
8. **Unlock Part 2 if allowed** — Execute operator-unlock API call
9. **Record decision** — Update candidate tracker and decision log

## API Endpoints

All endpoints are prefixed with `/beta/access`.

### Check participant stage
```bash
curl https://python-quest.vercel.app/api/beta/access/PART-XXXXXX
```

Response:
```json
{
  "ok": true,
  "participant_code": "PART-XXXXXX",
  "current_stage": 1,
  "max_stage": 5,
  "has_feedback": false,
  "feedback_submitted_at": null
}
```

### Submit feedback (parent action, also usable by operator)
```bash
curl -X POST https://python-quest.vercel.app/api/beta/access/PART-XXXXXX/provide-feedback \
  -H "Content-Type: application/json" \
  -d '{"feedback_text": "Child enjoyed it, got stuck on loops", "rating": 4}'
```

### List pending feedback
```bash
curl -H "X-Operator-Key: $OPERATOR_KEY" \
  https://python-quest.vercel.app/api/beta/access/operator/pending-feedback
```

Response:
```json
{
  "ok": true,
  "pending": [
    {
      "participant_code": "PART-XXXXXX",
      "current_stage": 1,
      "feedback_text": "...",
      "feedback_rating": 4,
      "feedback_submitted_at": "2026-06-03T12:00:00"
    }
  ]
}
```

### Unlock next stage
```bash
curl -X POST -H "X-Operator-Key: $OPERATOR_KEY" \
  https://python-quest.vercel.app/api/beta/access/PART-XXXXXX/operator-unlock
```

Response:
```json
{
  "ok": true,
  "previous_stage": 1,
  "current_stage": 2,
  "message": "Stage unlocked to 2"
}
```

### Get current beta access info
```bash
curl https://python-quest.vercel.app/api/beta/access/PART-XXXXXX
```

## Quick Reference: Participant Lifecycle

| Phase | Operator Action | API Call |
|---|---|---|
| Screening complete, ready to invite | Send invitation + beta code | (manual) |
| Part 1 started | Monitor | `GET /beta/access/CODE` |
| Part 1 completed | Ask for feedback | (manual) |
| Feedback received | Review | `GET /beta/access/operator/pending-feedback` |
| Feedback approved, unlock ready | Unlock Part 2 | `POST /beta/access/CODE/operator-unlock` |
| Part 2 in progress | Monitor | `GET /beta/access/CODE` |

## Operator Safety Rules

1. **Never commit OPERATOR_KEY** — The key is set via environment variable. Never paste it into code, config files, or version control.
2. **Never use default dev key in production** — The default `op-python-quest-dev-2026` is for local development only. Production must have a unique `OPERATOR_KEY` set.
3. **Never collect child personal data** — Do not ask for or store child name, email, phone, precise age, address, or school.
4. **Never unlock without feedback** — Feedback is required before any stage unlock.
5. **Never promise full product** — Participants are in a beta. Do not promise certificates, complete courses, or future paid features.
6. **Never call this mass paid launch** — This is a controlled staged beta with 5–10 participants.

## Incident Handling

| Incident | Response |
|---|---|
| **Beta code does not work** | Check code spelling (must be uppercase). Verify participant exists in DB. If not, reissue code. |
| **Locked lesson opens incorrectly** | Check that `get_current_stage()` returns correct value. If bypass is possible, create GitHub issue as critical blocker. |
| **Direct URL bypass works** | **Critical blocker.** Stop beta, fix access control, redeploy. |
| **Feedback form missing** | Send the feedback form URL directly. If endpoint is down, check backend logs. |
| **Parent complains about locked content** | Explain staged access. Check if feedback was submitted. If feedback is submitted, process unlock. |
| **Mission checker fails** | Verify the student's code is correct. If checker is wrong, log as product_blocker, fix, redeploy. |
| **Page crashes or blank screen** | Ask for browser console logs. Check Vercel deployment status. Create GitHub issue. |
| **Parent loses beta code** | Reissue same code (if not leaked) or generate new code. Update tracker. |
