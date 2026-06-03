# Beta Candidate Tracker

**Important:** This tracker is for manual operator use only. Do not store child personal data in any column. All references are by candidate ID and participant label.

## Table

| Candidate ID | Source | Parent Contact Ref | Fit | Invited | Beta Code Issued | Stage | Feedback Received | Unlock Decision | Status |
|---|---|---|---|---|---|---|---|---|---|
| CAND-001 | warm | manual | yes | yes | yes | part_1 | no | none | active |
| CAND-002 | group | manual | maybe | no | no | none | no | none | screening |
| CAND-003 | tutor | manual | yes | yes | yes | part_1_done | no | pending | awaiting_feedback |
| CAND-004 | group | manual | no | no | no | none | no | none | rejected |
| CAND-005 | warm | manual | yes | yes | yes | part_1_done | yes | unlock_part_2 | unlocked |
| CAND-006 | group | manual | yes | yes | yes | part_2 | no | none | active |

## Column Guide

| Column | Values | Description |
|---|---|---|
| **Candidate ID** | CAND-001, CAND-002, … | Unique candidate identifier |
| **Source** | warm / contact / group / tutor / homeschool / other | Where this candidate came from |
| **Parent Contact Ref** | manual | Contact stored externally (operator's phone/messenger) — never in this file |
| **Fit** | yes / no / maybe | Does the candidate fit the target profile |
| **Invited** | yes / no | Invitation sent |
| **Beta Code Issued** | yes / no | Unique beta code generated and delivered |
| **Stage** | none / part_1 / part_1_done / part_2 / part_2_done / part_3 / completed | Current stage in the course |
| **Feedback Received** | yes / no | Feedback form submitted |
| **Unlock Decision** | none / unlock_part_2 / keep_part_1 / pause / needs_support / product_blocker | Operator decision |
| **Status** | screening / invited / active / awaiting_feedback / unlocked / paused / completed / rejected | Current status |

## Status Flow

```
screening → invited → active → awaiting_feedback → unlocked → active (next part) → completed
                                                       → paused
                                                       → rejected
                          → rejected (during screening/invitation)
```

## Forbidden Columns

The following columns **must not** appear in this tracker:

- ❌ Child name
- ❌ Child email
- ❌ Precise age or date of birth (approximate range is fine)
- ❌ Address
- ❌ School name
- ❌ Phone number (from child)
