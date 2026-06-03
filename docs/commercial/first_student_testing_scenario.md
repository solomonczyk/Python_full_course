# First Student Testing Scenario

## Goal
Validate whether real beginner students (ages 10–16, no coding experience) can:
- Understand the Python Quest onboarding without external help.
- Complete the first mission independently.
- Understand what to do next.
- Express interest in continuing.
- Give actionable feedback on what was confusing, hard, or fun.

## Test Group
- **Size:** 5–10 students.
- **Profile:** Beginner level — no prior programming experience (or minimal experience with Scratch/block-based only).
- **Age:** 10–16 years old.
- **Recruitment:** Personal network of the product team, or parent volunteers from relevant communities.
- **Parent/operator observation preferred:** A parent or operator should sit with the student (not help, just observe) and take notes.

## Test Duration
- **Type:** Single session per student.
- **Recommended length:** 20–40 minutes.
- **Maximum length:** 60 minutes (after that, attention drops and feedback quality degrades).
- **Student may stop earlier if they lose interest** — note the stopping point as key data.

## Pre-Test Setup
1. Open the landing page in a modern browser (Chrome/Firefox/Edge).
2. Ensure the screen is at least 1024×768 (or use a laptop/desktop; tablet is acceptable but not phone).
3. No account creation or login required.
4. Observer has a notebook or the observation template ready.
5. Student starts without any explanation beyond: *"This is Python Quest. Click 'Start Quest' and see what happens. I'm here if you need help with the computer, but try to figure it out yourself first."*

## Test Path

| Step | Action | Expected |
|------|--------|----------|
| 1. Landing | Student sees landing page. Allowed to explore for 10–30 seconds. | Student reads or scans content. May comment on the art or headline. |
| 2. Start Quest | Student clicks "Start Quest" CTA. | Navigation to first quest / lesson grid. |
| 3. Explore grid | Student sees lesson grid with pulsing first lesson. | Student clicks the highlighted first lesson (or clicks around to explore). |
| 4. Lesson 1 character intro | Character dialogue loads. Ва speaks to the student. | Student reads the dialogue (may read aloud or silently). |
| 5. Concept explanation | Variable analogy is shown (variable as a labelled box). | Student reads or listens. May ask a question or nod. |
| 6. First mission | Mission card appears: "Create a variable named `treasure` with the value `42`." | Student attempts to type code in the editor. |
| 7. Mission attempt | Student writes code and clicks Run/Check. | Mission Checker evaluates. |
| 8. (If stuck) Hint | If student fails 2+ times, hint becomes available. | Student clicks hint, reads it, retries. |
| 9. Success | Mission passes. Celebration animation. | Student smiles, says "I did it" or equivalent. |
| 10. Continue | Student sees lesson completion marker and next lesson. | Student either clicks next lesson or stops to look around. |
| 11. Optional: Continue to lesson 1-2 and 1-3 | If engaged, continue to next lessons. | Natural progression. |
| 12. Stop | End session at natural break or time limit. | Observer asks post-test questions. |

## What To Observe

| Observation | What to note |
|-------------|-------------|
| **Where student hesitates** | Did they pause at the landing page? The lesson grid? The code editor? What were they confused about? |
| **Where student asks for help** | Did they ask "What am I supposed to do?" If so, at which step? Was the instruction unclear? |
| **Where student makes repeated mistakes** | Which mission caused 3+ failed attempts? Was the error message understood? Did the hint help? |
| **Where motivation drops** | Did the student sigh, lean back, look away, or say "This is boring"? At what point? |
| **Which character/dialogue helps or distracts** | Did the student read the dialogue or skip it? Did they laugh at Багус? Did they find Ва's explanations helpful or too wordy? |
| **Reading behaviour** | Does the student read text aloud? Do they skip dialogue boxes? Are there too many words per screen? |
| **UI interaction** | Does the student know where to click? Do they use the hint button? Do they notice the lesson grid? |

## Success Metrics

| Metric | Target for beta | How to measure |
|--------|----------------|----------------|
| Student starts without external explanation | ≥ 8/10 students | Observer notes "student clicked Start Quest without prompting" |
| Student completes first mission | ≥ 9/10 students | Mission Checker reports pass |
| Student understands what to do next | ≥ 7/10 students | Observer notes "student clicked next lesson without asking" |
| Student wants to continue | ≥ 6/10 students | Post-test Q: "Would you continue tomorrow?" — "Yes" or "Maybe" |
| Parent understands product value | ≥ 7/10 parents | Post-test Q: "What does this product teach?" — correct answer: Python/coding |

## Blocker Criteria

| Blocker | Severity | Action |
|---------|----------|--------|
| Student cannot understand first task (variable mission) after 5 attempts + hint | HIGH | Pause beta. Rewrite first lesson before next test. |
| Mission Checker blocks a correct answer (false negative) | CRITICAL | Stop testing. Fix Mission Checker before next session. |
| UI prevents progress (button not working, navigation broken) | CRITICAL | Stop testing. Fix UI before next session. |
| Onboarding does not explain product (student says "What am I supposed to do?") | HIGH | Revise landing/onboarding before next session. |
| Parent cannot understand what product does after seeing landing + first mission | HIGH | Revise landing page messaging. |

## Polish Criteria (Non-Blocking)

| Observation | Suggested Improvement |
|-------------|----------------------|
| Text could be shorter | Reduce dialogue length by 20–30% in flagged lessons. |
| CTA could be clearer | Add arrow or pulse animation to "Start Quest" button. |
| More animation would help | Add entrance animations for dialogue, mission cards, success. |
| Better progress visualization needed | Add quest-map breadcrumb or "You are here" indicator. |

## Post-Test Questions (asked by the observer, answered by the student)

1. **What was easy?** — Open-ended. Identifies what is well-explained.
2. **What was confusing?** — Open-ended. Identifies pain points.
3. **Where did you want to stop?** — Open-ended. Identifies motivation drops.
4. **What did you like?** — Open-ended. Identifies strengths to preserve.
5. **Would you continue tomorrow?** — Yes / Maybe / No. Core retention signal.

## Post-Test Questions (parent/operator)

1. **What do you think this product teaches?** — Verifies parent understands the value proposition.
2. **Did your child seem engaged?** — Subjective engagement assessment.
3. **Was there anything concerning?** — Safety, content, or behavioural concerns.
4. **Would you pay for this? What price seems fair?** — Price sensitivity test.
5. **What would need to change for you to recommend it?** — Product improvement ideas from the parent perspective.

## Test Session Log Template

```
Student ID: [anonymous ID]
Age range: [10-12 / 13-14 / 15-16]
Session date: YYYY-MM-DD
Session duration: XX min
Observer: [name]

Start time: HH:MM
Landing visit duration: XX sec
Started quest: Y/N
First lesson started: Y/N — time: HH:MM
First mission attempts: X
First mission passed: Y/N — attempts: X
Hints used: Y/N — level: X
Lesson completed: Y/N
Next lesson started: Y/N
Stopped at: [lesson/mission]
Stop reason: [natural break / lost interest / stuck / time limit]

Observations:
- [free text]
- [free text]

Post-test answers:
- Easy: ...
- Confusing: ...
- Wanted to stop: ...
- Liked: ...
- Continue tomorrow: Yes/Maybe/No
```
