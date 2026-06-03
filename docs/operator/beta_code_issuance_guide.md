# Beta Code Issuance Guide

## Goal
Issue beta codes safely without creating child accounts.

## Before Issuing Code

Verify all of the following with the parent:

- [x] Candidate screened via screening form
- [x] Parent understands this is a beta (not finished product)
- [x] Staged access explained (Part 1 open, Part 2 locked until feedback)
- [x] Feedback requirement explained (unlock requires feedback)
- [x] No child personal data collected (name, email, phone, precise age, address, school)
- [x] Parent agrees to the beta terms

If any item is unchecked, do not issue a code. Have the conversation first.

## Code Naming / Labels

Beta codes use the format: `PART-XXXXXX` where XXXXXX is a random uppercase alphanumeric string (letters and digits).

### Participant Labels

Use sequential participant labels for tracking:

| Label | Format | Example |
|---|---|---|
| First batch | WB-001, WB-002, … | WB-001 = Warm Batch participant 1 |
| Teacher referral | TR-001, TR-002, … | TR-001 = Tutor Referral participant 1 |
| Community | CM-001, CM-002, … | CM-001 = Community participant 1 |

### Tracker Record

For each issued code, record in the candidate tracker:

| Field | Example |
|---|---|
| Candidate ID | CAND-005 |
| Participant Label | WB-003 |
| Beta Code | PART-A3K8M2 |
| Stage | part_1 |
| Status | active |

## Delivery Message

Send the beta code to the parent via private message (not in a group chat).

> Hello [Parent Name],
>
> Your beta code for Python Quest is:
>
> **PART-A3K8M2**
>
> To start:
> 1. Go to: https://python-quest.vercel.app/
> 2. Enter the code in the beta access field
> 3. Click Start and begin Part 1
>
> After your child completes Part 1, please fill out this feedback form:
> [feedback form link]
>
> Once I receive your feedback, I'll review and unlock Part 2.
>
> Important reminders:
> - This code is for your family only — please don't share it publicly
> - The course is in beta — rough edges are expected, your feedback helps!
> - Parent supervision recommended for the first session
>
> Happy coding! 🚀

## Lost Code Handling

If a parent loses their beta code:

1. Verify the participant's identity (confirm parent contact details)
2. Look up the beta code in the tracker
3. Resend the same code via private message
4. If the code was compromised (shared publicly), generate a new code and update the tracker

## Reissue Rules

- **Same code:** OK if code was not compromised and participant is the same
- **New code:** Required if old code was shared publicly or the participant changed
- **Expired code:** Codes do not expire during the beta, but may be revoked if compromised
- **Revoked code:** If a code must be revoked (participant withdrawal, policy violation), mark as revoked in tracker and inform the participant

## What Not To Do

- ❌ **Do not publish beta codes publicly** — in posts, group chats, or public repositories
- ❌ **Do not send many codes into group chat** — one code per family, delivered privately
- ❌ **Do not store child personal data with beta code** — tracker contains only label, code, stage, status
- ❌ **Do not use beta code as password** — the code is not a security measure, it's an access stage identifier
- ❌ **Do not reuse codes across different families** — each participant gets a unique code
- ❌ **Do not commit beta codes to the repository** — codes are generated at runtime or stored in the database, never hardcoded
