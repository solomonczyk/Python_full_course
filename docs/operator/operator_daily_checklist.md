# Operator Daily Checklist

## Morning

- [ ] **Check new candidates** — Review any new messages from parents, tutors, or community posts. Reply to inquiries.
- [ ] **Reply to interested parents** — Respond to all pending parent messages within 24 hours.
- [ ] **Check pending feedback** — Run the pending feedback API:
  ```bash
  curl -H "X-Operator-Key: $OPERATOR_KEY" \
    https://python-quest.vercel.app/api/beta/access/operator/pending-feedback
  ```
  Review any new feedback submissions.
- [ ] **Check stuck participants** — Are there participants who started Part 1 but haven't completed it in several days? Check in with parent.
- [ ] **Check GitHub/Vercel status** — Verify:
  - GitHub Actions: green on main branch
  - Vercel: deployment healthy and ready

## During Sessions

- [ ] **Confirm participant can start** — When a participant begins their first session, verify the beta code works and Part 1 loads.
- [ ] **Record blockers** — If the participant encounters a technical issue, record it immediately with details (browser, lesson, error message).
- [ ] **Do not over-help unless necessary** — Beta is about observing real use. Let the child try independently. Only help if they are truly stuck or the product has a bug.
- [ ] **Note where student hesitates** — If you're observing, note which lessons or missions caused hesitation, confusion, or repeated errors.

## After Session

- [ ] **Ask for feedback** — If the participant completed Part 1, send the feedback form link. If they didn't finish, ask about the experience so far.
- [ ] **Record issue if needed** — Log any issues observed during the session:
  | Severity | Description |
  |---|---|
  | Blocker | Cannot proceed |
  | Major | Significant confusion or broken feature |
  | Minor | Small issue with workaround |
  | Polish | Typos, layout, cosmetic |
- [ ] **Decide unlock / pause / support** — For participants who completed Part 1 and submitted feedback, review and decide.
- [ ] **Update tracker** — Update the `beta_candidate_tracker.md` with current status for each active participant.

## End Of Day

- [ ] **Count active participants** — How many participants are actively in Part 1, awaiting feedback, in Part 2?
- [ ] **Count Part 1 completions** — How many participants have completed Part 1 today? Cumulative?
- [ ] **Count feedback received** — How many feedback forms were submitted today? Cumulative?
- [ ] **Count unlocks** — How many participants were unlocked to Part 2 today? Cumulative?
- [ ] **Summarize blockers** — List all blockers found today. Any critical ones? Any pattern across participants?

## Daily Summary Template

```
Date: YYYY-MM-DD

Active participants: X
Part 1 completed today: X (cumulative: X)
Feedback received today: X (cumulative: X)
Unlocks today: X (cumulative: X)

New blockers:
- [description]

New issues:
- Major: X
- Minor: X
- Polish: X

Notes:
- Any incidents or notable observations?
```

## Communication Log

Keep a simple log of parent communications:

| Date | Participant | Channel | Summary | Status |
|---|---|---|---|---|
| 2026-06-03 | WB-001 | Telegram | Sent feedback form | awaiting_response |
| 2026-06-03 | WB-002 | Email | Explained staged access | resolved |
