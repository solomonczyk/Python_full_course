# First Batch Tracker

## Overview

Participant tracker for the first staged beta batch (5–10 participants). This table uses **participant labels only** — no child personal data is stored here.

## Tracker Table

| Participant Label | Beta Code Ref | Source | Stage | Started | Part 1 Progress | Feedback Received | Unlock Decision | Issues | Status |
|---|---|---|---|---|---|---|---|---|---|
| STU-001 | — | — | 1 | — | — | — | — | — | pending |
| STU-002 | — | — | 1 | — | — | — | — | — | pending |
| STU-003 | — | — | 1 | — | — | — | — | — | pending |
| STU-004 | — | — | 1 | — | — | — | — | — | pending |
| STU-005 | — | — | 1 | — | — | — | — | — | pending |
| STU-006 | — | — | 1 | — | — | — | — | — | pending |
| STU-007 | — | — | 1 | — | — | — | — | — | pending |
| STU-008 | — | — | 1 | — | — | — | — | — | pending |
| STU-009 | — | — | 1 | — | — | — | — | — | pending |
| STU-010 | — | — | 1 | — | — | — | — | — | pending |

## Column Definitions

| Column | Description | Values |
|---|---|---|
| **Participant Label** | Anonymous identifier for the participant | STU-001 through STU-010 |
| **Beta Code Ref** | Reference to the beta code (not the code itself) | E.g., BETA-A3K8M2, or link to private tracker |
| **Source** | How the participant was recruited | Warm network, Teacher referral, Community, etc. |
| **Stage** | Current access stage (1–5) | 1, 2, 3, 4, 5 |
| **Started** | Has the participant started Part 1? | Y / N / Date |
| **Part 1 Progress** | How far has the participant progressed in Part 1? | Not started / In progress (lesson X-Y) / Completed |
| **Feedback Received** | Has feedback been submitted? | Y / N / Date received |
| **Unlock Decision** | Operator's decision on stage unlock | pending / unlocked / held / stopped / withdrawn |
| **Issues** | Any issues reported by this participant | List of issue references, or — |
| **Status** | Current participant status | active / paused / completed / withdrawn / revoked |

## Forbidden Columns

The following columns must **never** appear in this tracker:

- ❌ Child full name
- ❌ Child email address
- ❌ Child phone number
- ❌ Precise age or birthdate
- ❌ School name or class
- ❌ Home address
- ❌ Photo, audio, or video links
- ❌ Any personal identification number

## Status Definitions

| Status | Meaning |
|---|---|
| **pending** | Participant label created, awaiting invitation |
| **invited** | Invitation sent, awaiting response |
| **active** | Participant has started using the course |
| **paused** | Participant temporarily stopped, may return |
| **completed** | Participant has completed all available stages |
| **withdrawn** | Participant/parent voluntarily withdrew |
| **revoked** | Access revoked by operator |

## Usage Notes

- The operator maintains the canonical version of this tracker outside of Git (e.g., in a private spreadsheet or note).
- This document is a template/snapshot — the live tracker is not version-controlled.
- Update the tracker whenever a participant changes stage, submits feedback, or an unlock decision is made.
- Never fill in real beta codes in a Git-tracked version of this file.
