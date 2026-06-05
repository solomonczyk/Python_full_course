# First Batch Beta Code Issuance

## Overview

This document describes how beta codes are prepared, issued, and tracked for the first staged beta batch (5–10 participants). All codes are **operator-controlled** — creation and delivery are manual, not automated.

## How Many Codes Are Prepared

| Batch Phase | Codes Prepared | Status |
|---|---|---|
| Minimum batch (5 participants) | 5 | Ready for operator |
| Target batch (7–8 participants) | 8 | Ready for operator |
| Maximum batch (10 participants) | 10 | Ready for operator |

Codes beyond the initial 5 are issued only when the operator confirms additional participants are ready.

## Code Format

Beta codes follow the format `BETA-XXXXXX` where `XXXXXX` is a random uppercase alphanumeric string (letters and digits).

Example: `BETA-K7M3A9`

## Mapping: Code → Participant Label

Each issued code is mapped to a participant label. The mapping is stored in the operator's private tracker (outside the product). No mapping is stored in the database.

| Participant Label | Beta Code | Notes |
|---|---|---|
| STU-001 | BETA-XXXXXX | Issued first |
| STU-002 | BETA-XXXXXX | Issued second |
| STU-003 | BETA-XXXXXX | Issued third |
| ... | ... | ... |

## Where NOT to Store Secrets

- ❌ **Do not store beta codes in the repository** — never commit codes to Git
- ❌ **Do not store beta codes in the database** — codes are runtime values, not persistence secrets
- ❌ **Do not log beta codes** — avoid printing codes to console or logging systems
- ❌ **Do not share codes in group chats** — deliver privately per participant
- ✅ **Store mapping in operator's private tracker** (outside the product, not version-controlled)

## How to Deliver Code Manually

1. Generate a random code (or use the system's beta code creation endpoint if available)
2. Record the code → participant mapping in the private tracker
3. Send the code to the **parent** via private message (not in a group chat)
4. Verify the participant can access Part 1 with the code

### Delivery Message Template

```
Hello [Parent Name],

Your beta code for Python Quest is:

  BETA-K7M3A9

To start:
1. Go to: https://python-full-course-andy-s-projects26.vercel.app/
2. Enter the code in the beta access field
3. Click Start and begin Part 1

After your child completes Part 1, please fill out the feedback form:
[feedback form URL — TBD]

Once I receive your feedback, I'll review and unlock Part 2.

Important reminders:
- This code is for your family only — please don't share it publicly
- The course is in beta — rough edges are expected, your feedback helps!
- Parent supervision recommended for the first session

Happy coding! 🚀
```

## What to Do If Code Is Lost

1. Verify the participant's identity (confirm with parent via trusted contact channel)
2. Look up the existing beta code in the private tracker
3. Resend the **same code** via private message
4. If the code was compromised (shared publicly), **generate a new code** and update the tracker

## How to Revoke or Stop Participant

If a participant must be stopped or removed:

1. Mark the participant's label as `revoked` in the operator tracker
2. The existing beta code remains in the database but is no longer valid for new progress
3. The participant's existing progress data is preserved for analysis
4. Inform the parent that access has been ended (explain why: policy violation, withdrawal, etc.)
5. Do not delete the participant's data — mark as revoked, preserve for audit

### Revocation Reasons

| Reason | Action |
|---|---|
| Parent withdrawal (voluntary) | Mark as withdrawn, preserve data |
| Policy violation (code sharing, abuse) | Mark as revoked, preserve data for review |
| Technical blocker (unfixable) | Mark as paused, re-evaluate after fix |
| Duplicate code issuance | Reissue new code, revoke old one |

## Beta Code Creation Endpoint

The system has a `POST /api/beta/progress/create` endpoint that creates a beta progress record. However, for this first batch, **code issuance is manually controlled by the operator**:

- Codes are generated externally (operator creates them)
- The endpoint can be used to create a progress record if needed, but the code itself is delivered manually
- No automated code generation is required for this batch
