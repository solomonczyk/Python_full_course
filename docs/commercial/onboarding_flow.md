# Python Quest Onboarding Flow

## Goal
Within the first 3 minutes, a new learner should understand:
- What Python Quest is.
- What they need to do.
- That they can succeed (first mission passed).
- That the product is fun and they want to continue.

## Entry Flow
```
landing page → "Start Quest" button → animation/loading → Quest 1 lesson grid → first lesson card → character intro dialogue → first mission → success feedback → lesson complete → next lesson available
```

## First 3 Minutes

| Time | What happens | Student action |
|------|-------------|----------------|
| 0:00–0:10 | Landing page loads with headline "Learn Python. Complete Missions. Save the World." and "Start Quest" CTA | Tap/click Start Quest |
| 0:10–0:20 | Brief animated transition or loading screen with steampunk art | Wait (no action needed) |
| 0:20–0:40 | Lesson grid appears. First lesson card is highlighted and pulsing. Character Ва appears with dialogue: *"Welcome, Новичок. I've been expecting you. The world runs on Python, and someone must learn to control it."* | Click the highlighted lesson card |
| 0:40–1:00 | Lesson 1 loads. Ва explains: *"Before we save anything, let's understand the simplest box — a variable. Think of it like a labelled chest."* | Read/listen to dialogue |
| 1:00–1:30 | First concept explanation with visual analogy (variable as a box with name and value). Новичок asks: *"So I put something in a box and give it a name?"* | Read dialogue |
| 1:30–2:00 | First mission appears: "Create a variable named `treasure` with the value `42`." Code editor is shown with a placeholder. | Type code |
| 2:00–2:30 | Student clicks "Run" or "Check" — Mission Checker evaluates. | See result |
| 2:30–3:00 | **On success:** Confetti/glow effect. Ва says: *"Excellent! You've written your first Python code."* Lesson card marks as complete. Next lesson unlocks. | Student feels success. Clicks next lesson or explores grid. |
| | **On mistake:** Hint appears in-character. Багус runs around the screen: *"Bzzzt! The box needs a name first! Try something like `treasure = 42`"* | Student retries and passes. |

## Character Explanation (Parent/Operator Context)

- **Ва** — The Mentor. Explains concepts through real-world analogies. Voice: calm, wise, slightly eccentric professor.
- **Новичок** — The Learner. Represents the student's perspective. Asks clarification questions, makes mistakes, learns. Voice: curious, honest, sometimes confused.
- **Багус** — The Bug Creature. Shows up when code breaks. Makes error messages friendly and funny. Voice: chaotic, playful, high-energy.

## First Mission Experience

- **How task is introduced:** After the explanation dialogue, a mission card slides in with a clear instruction (e.g., "Create a variable named `treasure` with the value `42`"). The code editor appears below with a starter template.
- **How mistake is handled:** If the student submits incorrect code, a gentle error banner appears. Багус dialogue plays with a concrete hint ("Check the name — it should be `treasure` with an `e` at the end!"). No score is lost. No time pressure.
- **How hint is shown:** After 2 failed attempts, an optional "Hint" button becomes available. Clicking it reveals the next piece of the solution without giving everything away.
- **How success is shown:** Visual celebration — the mission card glows, particles or confetti appear, Ва gives congratulatory dialogue. The lesson card in the grid fills with a completion checkmark.

## Parent/Operator Explanation

- **What parent should understand:** Python Quest is a self-guided course where the child learns real Python programming through an interactive story. No installation or setup is needed — just a browser. The child progresses at their own pace.
- **What progress means:** Each completed lesson fills a card on the quest grid. Complete all lessons in a quest — the quest is marked complete. The skill tree shows which Python concepts the child has mastered.
- **What feedback is useful:** Tell us: Did the child need help? Did they get stuck? Did they enjoy it? Which part made them want to stop? Your observations are more valuable than any automated metric.
