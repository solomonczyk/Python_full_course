# Feedback Review And Unlock Rules

## Unlock Philosophy
Part 2 unlock is **not automatic**. It requires feedback submission and operator decision. The staged access model exists to ensure quality control — each part must work well before the next opens.

**Key principle:** The unlock is a reward for participation AND a quality gate. If Part 1 has critical issues, those must be fixed before more participants encounter them.

## Unlock Part 2 If

All of the following must be true:

- [x] Part 1 completed (student reached the end of Part 1 content)
- [x] Feedback submitted (feedback form received with meaningful content)
- [x] No unresolved blocker (any critical or major issue is acknowledged and either fixed or has a workaround)
- [x] Student wants to continue (from feedback: "eager to continue" or "yes, but needed a break")
- [x] Parent/operator understands beta (no confusion about beta scope or staged access)

## Do Not Unlock If

Any of the following is true:

- ❌ No feedback submitted — feedback is required before any unlock
- ❌ Student could not start — technical issues prevented the student from beginning Part 1
- ❌ Mission checker blocked correct answer — student wrote correct code but checker rejected it (product blocker)
- ❌ Parent expects finished product — parent believes the course is complete and has unmet expectations
- ❌ Child needs excessive adult help — student could not proceed through lessons without constant adult assistance
- ❌ Privacy concern unresolved — parent expressed privacy concerns that were not addressed
- ❌ Critical blocker found — any issue that prevents progression (blank page, crash, broken checker)
- ❌ Beta code compromised — code was shared publicly, needs reissue before continuing

## Decision Types

| Decision | Meaning | Next Action |
|---|---|---|
| **unlock_part_2** | Participant is cleared for Part 2 | Execute operator-unlock API, notify parent |
| **keep_part_1** | Keep at Part 1, do not unlock yet | Explain reason to parent, set conditions for unlock |
| **pause_participant** | Pause participation temporarily | Notify parent, preserve beta code, check back later |
| **needs_support** | Participant needs technical help or re-explanation | Provide support, check again, then decide unlock/pause |
| **product_blocker** | A product issue prevents safe unlock | Create GitHub issue, do not unlock until fixed and redeployed |

## Decision Record Format

Record each decision in the operator notes (outside the product).

```json
{
  "participant_label": "WB-001",
  "current_stage": "part_1",
  "feedback_received": true,
  "part_1_completed": true,
  "issues": [],
  "operator_decision": "unlock_part_2",
  "reason": "Participant completed Part 1, submitted positive feedback, student eager to continue. No blockers."
}
```

```json
{
  "participant_label": "WB-002",
  "current_stage": "part_1",
  "feedback_received": true,
  "part_1_completed": true,
  "issues": [
    {
      "severity": "major",
      "description": "Mission 3 checker rejects correct answer when string contains Cyrillic characters"
    }
  ],
  "operator_decision": "product_blocker",
  "reason": "Mission checker fails on correct Unicode input. Fix required before unlock."
}
```

## Escalation Path

If unsure about a decision:

1. Re-read the feedback form carefully
2. Check if other participants reported the same issue
3. If product blocker: fix → redeploy → verify fix → unlock
4. If parent confusion: have another conversation → confirm understanding → decide
5. If escalation needed: pause, do not unlock, seek advice

## After Unlock

After unlocking Part 2:

1. Notify the parent via their preferred channel
2. Confirm they can see Part 2 content
3. Reset the feedback requirement for the next unlock (Part 3)
4. Update the candidate tracker
