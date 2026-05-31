# Full UX Audit Report — Python Quest
**Date**: 2026-05-31  |  **Lessons analyzed**: 92  |  **Audit types**: Persona 10, Persona 20, Technical UX, Content Quality

---

## 1. Executive Summary — Top 10 Findings

1. **P0 — SteampunkCard redefined on every render (LessonPage.tsx)**: Component defined inside LessonPage body causes unmount/remount of all children on every state change. This destroys Pyodide, quiz state, editor content.

2. **P0 — CourseMap uses `<a href>` instead of React Router `<Link>`**: Full page reload on every lesson click resets all React state.

3. **P0 — `crypto.randomUUID()` has no fallback**: User in non-HTTPS context or older browser gets a silent app breakage.

4. **P0 — `mini_summary` renders twice** when lesson has `find_bug` but no `connection_to_game`: Duplicate content bug.

5. **P1 — Missions are too easy (Persona 20)**: Many missions ask to replicate the exact code example with minor changes. By lesson 5-4, a 20-year-old should write multi-step programs.

6. **P1 — Bool introduced too late (lesson 3-6)**: Students write `if` from lesson 1-8 without understanding what a condition returns.

7. **P1 — Bagus mocks mistakes** ('Kha-kha! Typical newbie mistake!'): Actively demotivating for a young adult learner.

8. **P1 — Dialogue is repetitive**: Analogy is stated in pre_topic_dialogue, then again in analogy section, then again in game_relevance. Novice repeats everything back verbatim.

9. **P2 — Wrong subtitles**: Lesson 4-15 shows 'Logical OR' instead of 'Sorting'. Lesson 4-9 shows 'Text search' instead of 'String join'.

10. **P2 — Boss lesson 4-31 (50 min) exceeds attention span**: Persona 10 audit flags this as PROBLEMATIC for length. Suggest splitting into 2x25 min.

---

## 2. Persona 10 — Audit Findings (16 lessons evaluated)

| Lesson | Title | Language | Analogy | Length | Confidence | Fun | Overall | Key Notes |
|--------|-------|----------|---------|--------|------------|-----|---------|-----------|
| 1-1 | print() — Твой голос в коде | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | A near-perfect first lesson. The cave voice analogy maps directly to the concept of printing output. |
| 1-3 | Переменные — Именованные контейнеры | GOOD | GOOD | GOOD | GOOD | ACCEPTABLE | GOOD | Excellent. The chest/container analogy is concrete and kid-friendly. |
| 1-6 | Арифметика — Сложение, вычитание и умножение | GOOD | GOOD | GOOD | GOOD | ACCEPTABLE | GOOD | Solid lesson. The kitchen scales analogy works well for explaining operator precedence. |
| 1-8 | if — Ветвление в коде | GOOD | ACCEPTABLE | GOOD | GOOD | GOOD | ACCEPTABLE | Good lesson. The bouncer analogy is slightly adult-oriented but still works because 10yos understand age restrictions (movie ratings, etc.). |
| 1-9 | if else — Выбор пути | GOOD | GOOD | ACCEPTABLE | GOOD | GOOD | GOOD | Great lesson. The road fork analogy is timeless and perfectly clear for children. |
| 2-1 | elif — Множественный выбор | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | Excellent lesson. The bridge-guard analogy beautifully explains sequential elif evaluation. |
| 2-5 | Первое знакомство с for | ACCEPTABLE | GOOD | GOOD | GOOD | GOOD | ACCEPTABLE | Good lesson. Main content is kid-friendly. Minor concern: 'итерация' in the syntax_reminder is too advanced. Suggest replacing with 'шаг' or 'повторение'. |
| 3-1 | Float и типы данных | GOOD | GOOD | GOOD | GOOD | ACCEPTABLE | GOOD | Excellent analogy choice. 'Целые яблоки и дольки' is one of the best analogies in the entire course for this age group. |
| 3-14 | For и range база | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | Strong lesson. Train analogy perfectly maps to the for/range concept. |
| 3-22 | F-строка | GOOD | GOOD | ACCEPTABLE | GOOD | GOOD | GOOD | Excellent. The birthday card analogy is universally relatable for children. |
| 4-1 | Флаги — Сигнальные переменные | GOOD | GOOD | ACCEPTABLE | GOOD | GOOD | GOOD | Solid lesson. The map-flag analogy is clear and game-like. |
| 4-7 | None — Пустое значение | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | One of the best analogies in the course. The birthday gift box is universally understood by children. |
| 4-26 | while — Цикл с условием | GOOD | GOOD | ACCEPTABLE | GOOD | GOOD | GOOD | Excellent real-world analogy. The microwave is perfect for explaining 'while condition is true'. |
| 4-31 | random + while игра | ACCEPTABLE | GOOD | PROBLEMATIC | GOOD | GOOD | ACCEPTABLE | Content and analogy are great, but 50 minutes is too long for a 10yo in one sitting. Suggest splitting into 2 parts (25 min each) or adding a clear 'break point'. |
| 5-1 | def (Функции) — Кнопка на пульте | ACCEPTABLE | GOOD | GOOD | GOOD | GOOD | GOOD | Excellent analogy, but the terms 'аргумент' and 'параметр' need explicit child-friendly definitions. The remote control perfectly captures the 'encapsulation' idea. |
| 5-7 | try/except — Страховка альпиниста | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | Fantastic lesson. Bagus teaching try/except is thematically perfect. The climbing rope analogy is clear and engaging. |

**Summary**: The course is generally well-designed for 10-year-olds. The analogies are the strongest point — using everyday objects (cave echo, chests, kitchen scales, trains, microwaves, TV remotes, gift boxes) that children can immediately relate to. The weakest areas are: (1) some syntax reminders use advanced language like 'итерация', (2) the steampunk UI overuses abstract fantasy terminology in navigation labels, and (3) the 50-minute boss lesson exceeds a typical 10yo's attention span. No lesson was rated PROBLEMATIC.

**Best aspect**: Analogies — consistently excellent, concrete, and child-appropriate throughout the course. The empty gift box (None), microwave (while), and TV remote (functions) analogies are standout examples.

**Worst aspect**: Syntax reminder language — some reminders contain words like 'итерация' that are too advanced for the target age group. These should use simpler synonyms ('шаг', 'повторение').

### UI Child-Friendliness Review

**LessonPage_tsx** (score: 7/10 — Good thematic design but some terminology and font sizes could be improved for children)

- **Pros**:
  - Character avatars and named instructors (Ksyu, Va, Da, Bagus) create emotional connection
  - Steampunk theme with warm colors (gold, teal) is visually engaging for kids
  - Progress dots show how far through the lesson the child is — helps with navigation anxiety
  - Clear 'Previous' and 'Next' buttons with arrow icons — easy to navigate
  - Hero banner with lesson ID and complexity rating is clear
  - Locked state is visually distinct and includes a helpful button to go to the previous lesson
  - Loading state has a spinner animation — keeps a child's attention while waiting
  - Code blocks are visually separated — reduces intimidation
  - The 2-column grid layout (character card + code panel) is balanced and readable
- **Cons**:
  - Term 'Adept' in welcome message might confuse a 10yo — not a common Russian word
  - 'Complexity 1/10' etc. is abstract — a simple 'Easy/Medium/Hard' label would be clearer
  - The page dots (4 dots at bottom) are not labeled — a child might not know what they represent
  - Dark theme with small fonts (10px, 11px) might be hard to read for some children
  - Error state shows raw error text — should show a simpler 'Ooops, something went wrong!' message
  - No sound effects or animations on correct answers (would boost engagement)
  - The loading text is in English: 'Loading lesson...' — should be Russian
  - No visual celebration (confetti, stars) on completing a lesson

**HomePage_tsx** (score: 6/10 — Beautiful steampunk design but overuses abstract terminology that a 10yo won't understand. Needs simpler, more intuitive labels.)

- **Pros**:
  - Welcome banner with 'Continue Quest' button gives clear path forward
  - Part cards with emoji icons (🔮, ⚗️, ⚙️, 🏰) are visually appealing and give a sense of progression
  - Progress bar ('Resonance') with percentage and rank system (Novice -> Arch-Mage) gamifies learning
  - Character Introduction section creates narrative immersion
  - Quest History shows recently completed lessons — builds pride and sense of accomplishment
  - Review Blocks section is well-organized with clear type labels (Quick Recall, Chapter, Boss, Part)
  - Current part is highlighted with a glowing border — draws attention to where to go next
  - Locked parts are visually dimmed but the part number is still shown — manages expectations
- **Cons**:
  - 'Resonance', 'Aether', 'Rank' terminology is steampunk-flavored but may confuse a 10yo — they might not understand what these mean
  - The welcome message 'System Status: Resonant' is not meaningful to a child. 'Ready to learn!' would be clearer
  - 'Consult Lexicon' button is vague — a child might not know what it does
  - No tutorial/onboarding for first-time visitors — a 10yo landing here for the first time might feel lost
  - 'Streaks' showing '3 Days' for 9 lessons is confusing — the mapping is not intuitive
  - The page uses many abstract status words (Resonance, Rank) without explaining what they mean for the child's journey
  - No sound or animation on the home page — could benefit from subtle ambient feedback
  - The 'AETHER' sidebar card with technical stats (XP, Rank, Streaks) is over-engineered for a 10yo — simpler stats would work better

### Cross-Cutting Issues (Persona 10)

- **Overuse of 'итерация' in syntax reminders** (lessons: 2-5, 3-14): Replace 'итерация' with 'шаг' (step) or 'повторение' (repetition) in all syntax blobs visible to children
- **English terms in UI** (lessons: all): Replace 'Loading lesson...' with Russian equivalent. The rest of the app is in Russian — this sticks out
- **Boss-level lessons (4-31) at 50 min too long** (lessons: 4-31): Split into 2 x 25 min segments with a natural break point, or add a 'take a break' prompt at 25 min
- **Steampunk terminology overload in UI** (lessons: all): Add tooltips or hover explanations for terms like 'Aether', 'Resonance', 'Adept' so a 10yo can understand them
- **No explicit definitions for 'аргумент' and 'параметр'** (lessons: 5-1): Add a quick child-friendly definition sidebar or dialogue box explaining these terms before first use

---

## 3. Persona 20 — Audit Findings (16 lessons evaluated)

| Lesson | Title | Pacing | Depth | Theme | Relevance | Challenge | Language | Overall | Notes |
|--------|-------|--------|-------|-------|-----------|-----------|----------|---------|-------|
| 1-1 | print() | ACCEPTABLE | GOOD | GOOD | GOOD | ACCEPTABLE | GOOD | ACCEPTABLE | Strong start, but the 'cave echo' metaphor is overused (dialogue + analogy + relevance all repeat it). Novice character seems unnecessarily clueless — a 20yo would get it faster. Bagus mocks mistakes which feels bad. |
| 1-3 | Переменные | ACCEPTABLE | ACCEPTABLE | GOOD | GOOD | ACCEPTABLE | GOOD | ACCEPTABLE | Solid lesson. Swap-values subtask is a highlight — actually makes you think. But Novice asking 'is that like a chest?' after Ksyu already explained the chest is too much handholding. |
| 1-8 | if | GOOD | ACCEPTABLE | GOOD | GOOD | ACCEPTABLE | GOOD | ACCEPTABLE | The 'bouncer at club' analogy actually works well for 20-year-olds. Indentation bug (find_bug) is excellent. But Novice's dialogue responses are too obvious — real 20yo would connect faster. |
| 2-1 | elif | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | One of the better lessons. Three bridges analogy maps cleanly to elif chain. Find_bug with if/if instead of if/elif is a real-world bug beginners actually make. Mission is reasonably challenging. |
| 2-3 | random.randint | GOOD | ACCEPTABLE | GOOD | GOOD | PROBLEMATIC | GOOD | ACCEPTABLE | Good concept execution but the mission is a miss: expected output is literally 'Бросок сделан!' — no random value needed. A 20yo would find this trivial. The find_bug (missing import) is great though. |
| 2-5 | Первое знакомство с for | ACCEPTABLE | ACCEPTABLE | GOOD | GOOD | PROBLEMATIC | GOOD | PROBLEMATIC | Mission expected_output='Python' (single) contradicts the task (print 3 times). This inconsistency would confuse a learner. The practice subtasks (print numbers 1-5) are better but still basic. Missing list iteration. |
| 3-6 | Bool | ACCEPTABLE | PROBLEMATIC | GOOD | ACCEPTABLE | PROBLEMATIC | GOOD | PROBLEMATIC | Bool introduced way too late (lesson 3-6). Students have been writing if statements since lesson 1-8 without understanding what a condition actually returns. This should be right after or along with if. Mission is trivial. |
| 3-8 | Короткая запись условий | PROBLEMATIC | PROBLEMATIC | ACCEPTABLE | ACCEPTABLE | ACCEPTABLE | GOOD | PROBLEMATIC | Scope confusion: title says 'short condition notation', explanation covers `if found:` shorthand, analogy covers ternary, practice covers ternary, mission covers `if found:`. These are two different concepts. Pick one or clearly separate them. |
| 3-22 | F-строка | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | Clean lesson. Great analogy (birthday card with blanks), good progression, mission is appropriately challenging for medium difficulty. One of the best structured lessons. |
| 3-35 | Фильтрация списка | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | Solid medium-difficulty lesson. The find_bug (using n without defining it/loop) is excellent. List comprehension is introduced naturally. Good balance of theory and practice. |
| 4-9 | join | GOOD | GOOD | GOOD | GOOD | ACCEPTABLE | GOOD | GOOD | Effective lesson. The find_bug (join with int list) is a genuinely useful trap. Clean explanation, good analogy. The subtitle says 'Поиск в тексте' (text search) which doesn't match join — cosmetic bug. |
| 4-14 | map | GOOD | ACCEPTABLE | GOOD | GOOD | GOOD | GOOD | GOOD | Good lesson with a practical multi-step mission. The pipeline (split -> map -> sum) is a realistic pattern. Find_bug (sum of strings) is perfect. Could mention that map returns an iterator. |
| 4-15 | sort | GOOD | ACCEPTABLE | GOOD | GOOD | GOOD | GOOD | GOOD | Well-focused lesson. The find_bug (sort() returns None) is the absolute highlight — this confuses every beginner. Would benefit from also mentioning sorted() for immutable sorting. The subtitle says 'Логическое ИЛИ' (logical OR) which is completely wrong — should be 'Сортировка'. |
| 4-21 | Ссылки | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | One of the best lessons. Two-remotes analogy is perfect for 20-year-olds. The reference vs copy distinction is one of the hardest concepts for beginners, and this lesson nails it. Great find_bug and practice tasks. |
| 4-24 | copy | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | GOOD | Excellent follow-up to lesson 4-21. The nested list mutation practice task is the highlight — it shows exactly why shallow copy isn't always enough. Good progression from reference -> copy -> deep copy awareness. |
| 4-31 | random + while игра | ACCEPTABLE | GOOD | GOOD | GOOD | PROBLEMATIC | GOOD | PROBLEMATIC | Great concept (boss lesson combining everything) but flawed execution. The code example has guess=secret always succeeding, but the task asks for 'remaining attempts after first wrong guess'. Inconsistent. 50min difficulty is appropriate but the mission design needs rework. |
| 5-1 | Кнопка на пульте | GOOD | ACCEPTABLE | GOOD | GOOD | ACCEPTABLE | GOOD | GOOD | Remote control is the perfect analogy for functions — a 20yo has never thought about how a TV button works, which is exactly the point. Good intro but needs parameters and return in follow-up lessons to feel complete. |
| 5-4 | Телефонная книга | ACCEPTABLE | ACCEPTABLE | ACCEPTABLE | GOOD | PROBLEMATIC | GOOD | ACCEPTABLE | Content is correct but the mission is far too easy for a lesson this late (5-4). By lesson ~60, a 20yo should be building small multi-step programs, not 'create one key-value pair'. The telephone book subtitle is 'Храним данные по ключам' which is accurate, but the chapter 5 placement means students should handle more complex tasks. |

### General Observations (Persona 20)

**Positive**:
- Analogy quality is generally high — 'two remotes one TV' (4-21), 'bouncer at club' (1-8), 'birthday card' (3-22) are genuinely good
- Find_bug exercises are consistently excellent across all lessons — real-world mistakes, not contrived
- Practice subtasks add meaningful reinforcement beyond the main mission
- F-strings, join, map, references, copy, sort, filter — the chapter 3-4 lessons are very strong
- Russian language is natural, modern, avoids both overly formal and cringey slang
- Steampunk RPG theme is consistent and creates a coherent identity

**Issues**:
- MISSIONS are often too easy: many ask to replicate the exact code example with minor changes. By lesson 5-4, a 20yo should write multi-step programs
- DIALOGUE repetition: analogy is stated in pre_topic_dialogue, then again in analogy section, then again in game_relevance. Novice character always repeats the analogy back verbatim — patronizing for 20yo
- BAGUS character mocks mistakes ('Ха-ха! Типичная ошибка новичка!') — this is actively demotivating for a young adult learner
- BOOL introduced too late (3-6) — students use conditions from 1-8 without understanding what a boolean is
- Lesson 3-8 mixes two unrelated concepts (if-found shorthand AND ternary operator) with no clear separation
- Lesson 4-31 (boss) has mission/code example inconsistency — code always wins but task expects wrong guess handling
- Several subtitles are wrong: 4-15 shows 'Логическое ИЛИ' instead of 'Сортировка', 4-9 shows 'Поиск в тексте' instead of 'Объединение строк'
- CompletionPage.tsx has no progressive roadmap — just redirects to lesson 1-1 if incomplete. No 'you are here' milestone visualization

**Summary**: The course is ACCEPTABLE for a 20-year-old but has clear marks of being designed for a younger audience. The steampunk RPG theme is not a problem — it's well-executed and consistent. The real issues are: (1) missions lack bite — most replicate examples, (2) dialogue is too repetitive with the Novice character being overly slow on the uptake, (3) Bagus laughing at mistakes would annoy any self-respecting 20yo, (4) the late bool introduction and confused 3-8 lesson show structural curriculum issues. The strongest part is the chapter 4 sequence (join, map, sort, references, copy) which is genuinely well-structured. With harder missions, less patronizing dialogue, and curriculum reordering, this could be excellent for young adults.

### Completion Page Review
- **Useful as roadmap**: False
- **Note**: CompletionPage is a finish-line screen, not a roadmap. It has no 'you are here' indicator, no milestone tracking, no part/chapter progression visualization. The skills checklist (7 items) is reasonable for the course scope. The next-steps links (FastAPI, pandas, selenium, LeetCode) are useful post-course suggestions. But a true roadmap would show lesson parts, completion percentage per part, and the student's current position in the broader curriculum — none of which exist here.

---

## 4. Technical UX Findings (19 findings)

| # | Severity | Category | File | Line | Title |
|---|----------|----------|------|------|-------|
| 1 | **CRITICAL** | logic_bug | frontend/src/pages/LessonPage.tsx | 269-299 | mini_summary renders twice when lesson has find_bug but no connection_to_game |
| 2 | **CRITICAL** | runtime_error | frontend/src/utils/userId.ts | 6 | crypto.randomUUID() has no fallback |
| 3 | **CRITICAL** | performance | frontend/src/pages/LessonPage.tsx | 37-49 | SteampunkCard component redefined on every render |
| 4 | **CRITICAL** | navigation_bug | frontend/src/components/CourseMap.tsx | 69-85 | CourseMap uses <a href> instead of React Router <Link> |
| 5 | **HIGH** | error_handling | frontend/src/pages/HomePage.tsx | 29-36 | Reviews fetch has no loading state and silent error catch |
| 6 | **HIGH** | error_handling | frontend/src/hooks/useApi.ts | 14-38 | useLessons() error not surfaced in Layout or Sidebar |
| 7 | **HIGH** | accessibility | frontend/src/components/CodePlayground.tsx | 153-158 | Line numbers have insufficient color contrast (~3.47:1) |
| 8 | **HIGH** | accessibility | frontend/src/components/CodePlayground.tsx | 161-174 | Code textarea lacks accessible label |
| 9 | **HIGH** | accessibility | frontend/src/pages/LessonPage.tsx | 65-68 | Loading spinner missing aria-hidden and aria-label |
| 10 | **MEDIUM** | error_handling | frontend/src/hooks/useApi.ts | 72-112 | useProgress() has no loading state exposed |
| 11 | **MEDIUM** | error_handling | frontend/src/components/CodePlayground.tsx | 19-48 | Pyodide load failure has no retry mechanism |
| 12 | **MEDIUM** | code_quality | frontend/src/pages/HomePage.tsx | 8 | Duplicate BASE constant defined in HomePage |
| 13 | **MEDIUM** | error_handling | frontend/src/components/QuizSection.tsx | 32-42 | QuizSection catches errors but shows no user-facing feedback |
| 14 | **MEDIUM** | accessibility | frontend/src/components/MissionCard.tsx | 243-269 | Bagus error feedback uses animate-bounce, which can trigger vestibular issues |
| 15 | **MEDIUM** | error_handling | frontend/src/hooks/useApi.ts | 152-170 | checkQuizAnswer and checkWhatOutputs have no request timeout |
| 16 | **LOW** | code_quality | frontend/src/pages/LessonPage.tsx | 6 | Unused import: DialogueBubble |
| 17 | **LOW** | maintainability | frontend/src/pages/LessonPage.tsx | 247-258 | Conditional 2-column grid wraps single-child sections |
| 18 | **LOW** | ux | frontend/src/pages/HomePage.tsx | 75 | Continue Quest button may become invisible if all lessons completed |
| 19 | **INFO** | ux | frontend/src/components/CourseMap.tsx | 10-11 | CourseMap redundant totalLessons/completedCount from useProgress vs props |
| 20 | **INFO** | resilience | frontend/src/pages/LessonPage.tsx | 84 | isLessonUnlocked return true when lessons array is empty (loading) |

**Summary**: 19 total findings — 4 critical, 5 high, 5 medium, 3 low, 2 info.

### Detailed Technical UX Findings

#### 1. mini_summary renders twice when lesson has find_bug but no connection_to_game [CRITICAL]
- **File**: frontend/src/pages/LessonPage.tsx:269-299
- **Category**: logic_bug
- **Description**: When lesson.find_bug is truthy, lesson.connection_to_game is falsy, and lesson.mini_summary is truthy, the mini_summary renders both inside the 2-column grid (lines 279-283 as the else branch) AND again outside the grid (lines 295-299). This duplicates content visually.
- **Suggested fix**: Remove the outer conditional block (lines 295-299) — the inner block already covers this case.

#### 2. crypto.randomUUID() has no fallback [CRITICAL]
- **File**: frontend/src/utils/userId.ts:6
- **Category**: runtime_error
- **Description**: If crypto.randomUUID() is unavailable (non-HTTPS context, older browsers), getUserId() throws. Since every authenticated API call depends on this, the entire app breaks silently. authHeaders() has no try/catch, and callers like useProgress() catch generically — so a user in an insecure context sees zero progress with no actionable feedback.
- **Suggested fix**: Add a fallback: `uid = crypto.randomUUID?.() ?? Date.now().toString(36) + Math.random().toString(36).slice(2)`

#### 3. SteampunkCard component redefined on every render [CRITICAL]
- **File**: frontend/src/pages/LessonPage.tsx:37-49
- **Category**: performance
- **Description**: The SteampunkCard component is defined inside the LessonPage function body. Every state change causes React to see a new component type, forcing unmount/remount of all children wrapped in it. This destroys internal state (e.g. expanded states in children) and harms performance.
- **Suggested fix**: Move SteampunkCard outside the component (top-level or a separate file).

#### 4. CourseMap uses <a href> instead of React Router <Link> [CRITICAL]
- **File**: frontend/src/components/CourseMap.tsx:69-85
- **Category**: navigation_bug
- **Description**: Lesson links use `<a href="/lesson/${lesson.id}">` instead of React Router's `<Link to=...>`. This causes a full page reload on every lesson click, resetting all React state (Pyodide, quiz state, editor content). This is a significant UX degradation.
- **Suggested fix**: Replace `<a>` with `<Link to={...}>` from react-router-dom.

#### 5. Reviews fetch has no loading state and silent error catch [HIGH]
- **File**: frontend/src/pages/HomePage.tsx:29-36
- **Category**: error_handling
- **Description**: The /api/reviews fetch in HomePage has `.catch(() => {})` which silently swallows all errors. There is no loading spinner or error message. If the API is slow or unreachable, the reviews section appears empty with no visual feedback. Also, no AbortController cleanup — if the component unmounts before the fetch completes, it calls setState on an unmounted component.
- **Suggested fix**: Add loading/error states to the reviews fetch; add AbortController cleanup.

#### 6. useLessons() error not surfaced in Layout or Sidebar [HIGH]
- **File**: frontend/src/hooks/useApi.ts:14-38
- **Category**: error_handling
- **Description**: useLessons() exposes an `error` state, but Layout.tsx (which calls it) never passes it to the Sidebar or displays it. If the /api/lessons endpoint fails, the app renders with an empty lessons array and no feedback to the user — the sidebar is empty, navigation links vanish.
- **Suggested fix**: Pass the error to a toast/notification or show inline in the Sidebar.

#### 7. Line numbers have insufficient color contrast (~3.47:1) [HIGH]
- **File**: frontend/src/components/CodePlayground.tsx:153-158
- **Category**: accessibility
- **Description**: Line numbers use color #6b7280 on background #0d0c14. The contrast ratio is approximately 3.47:1, which fails WCAG AA (4.5:1 for normal text). This affects readability, especially since these are 10px text.
- **Suggested fix**: Lighten line numbers to at least #8b8f98 or darken the background.

#### 8. Code textarea lacks accessible label [HIGH]
- **File**: frontend/src/components/CodePlayground.tsx:161-174
- **Category**: accessibility
- **Description**: The main code textarea in CodePlayground has no aria-label, aria-labelledby, or associated <label> element. Screen readers will not announce its purpose.
- **Suggested fix**: Add `aria-label="Python code editor"` or `aria-labelledby` pointing to a visible heading.

#### 9. Loading spinner missing aria-hidden and aria-label [HIGH]
- **File**: frontend/src/pages/LessonPage.tsx:65-68
- **Category**: accessibility
- **Description**: The animated loading spinner uses `<span className="material-symbols-outlined ... animate-spin">progress_activity</span>` without `aria-hidden="true"` or `role="status"` / `aria-live="polite"`. Screen readers may read the icon character or ignore the loading state entirely.
- **Suggested fix**: Add `aria-hidden="true"` on the icon and a visually-hidden `role="status"` span with 'Loading lesson...'.

#### 10. useProgress() has no loading state exposed [MEDIUM]
- **File**: frontend/src/hooks/useApi.ts:72-112
- **Category**: error_handling
- **Description**: useProgress() starts with an empty progress map and fetches asynchronously. There is no `loading` boolean returned. Components using it (HomePage, LessonPage, CourseMap) show '0 completed' / 'locked' for all lessons until the API responds, causing a flash of incorrect state.
- **Suggested fix**: Add a `loading` boolean to the return value and show a skeleton while loading.

#### 11. Pyodide load failure has no retry mechanism [MEDIUM]
- **File**: frontend/src/components/CodePlayground.tsx:19-48
- **Category**: error_handling
- **Description**: If Pyodide fails to load (script.onerror), status is set to 'idle' and the user sees 'Python ne zagruzilsya. Prover internet.' when trying to run code. There is no retry button — the user must refresh the page.
- **Suggested fix**: Add a 'Retry' button that resets scriptLoaded and re-creates the <script> tag.

#### 12. Duplicate BASE constant defined in HomePage [MEDIUM]
- **File**: frontend/src/pages/HomePage.tsx:8
- **Category**: code_quality
- **Description**: HomePage.tsx defines `const BASE = '/api'` at line 8, but useApi.ts already defines `const BASE = '/api'` at line 5. The HomePage fetch at line 30 uses `${BASE}/reviews` instead of the shared hook useReviews() defined in useApi.ts.
- **Suggested fix**: Use the existing useReviews() hook instead of duplicating the fetch and constant.

#### 13. QuizSection catches errors but shows no user-facing feedback [MEDIUM]
- **File**: frontend/src/components/QuizSection.tsx:32-42
- **Category**: error_handling
- **Description**: When checkQuizAnswer() throws, the catch block sets a fallback result but only logs to console. The UI shows 'Неверно' with an empty correct_id — preventing the user from learning the right answer. If the API is unreachable, this is misleading.
- **Suggested fix**: Show a distinct 'Connection error' message when the fetch fails, preserving the correct answer display.

#### 14. Bagus error feedback uses animate-bounce, which can trigger vestibular issues [MEDIUM]
- **File**: frontend/src/components/MissionCard.tsx:243-269
- **Category**: accessibility
- **Description**: The error feedback box uses `animate-bounce` — a CSS animation that repeatedly bounces the element. This animation cannot be disabled by users who prefer reduced motion (no `prefers-reduced-motion` check).
- **Suggested fix**: Use `motion-safe:animate-bounce` or `@media (prefers-reduced-motion: no-preference)` guard.

#### 15. checkQuizAnswer and checkWhatOutputs have no request timeout [MEDIUM]
- **File**: frontend/src/hooks/useApi.ts:152-170
- **Category**: error_handling
- **Description**: Both functions make fetch() calls without a timeout or AbortSignal. A slow/unresponsive API will cause the UI to hang indefinitely (QuizSection's button remains disabled, MissionCard shows 'checking').
- **Suggested fix**: Pass an AbortSignal with a timeout (e.g., 10s) to fetch.

#### 16. Unused import: DialogueBubble [LOW]
- **File**: frontend/src/pages/LessonPage.tsx:6
- **Category**: code_quality
- **Description**: DialogueBubble is imported at line 6 but never used in the component. DialogueScene is used instead, which may internally use DialogueBubble. This can cause lint warnings and confusion.
- **Suggested fix**: Remove the unused DialogueBubble import.

#### 17. Conditional 2-column grid wraps single-child sections [LOW]
- **File**: frontend/src/pages/LessonPage.tsx:247-258
- **Category**: maintainability
- **Description**: The grid at line 247 wraps PredictOutputBlock and GameRelevanceBlock. If either is missing, the grid still renders with a single cell. This can look unbalanced. Same for the FindBugBlock grid at line 270.
- **Suggested fix**: Conditionally render the grid wrapper only when both children are present, or use auto-fill.

#### 18. Continue Quest button may become invisible if all lessons completed [LOW]
- **File**: frontend/src/pages/HomePage.tsx:75
- **Category**: ux
- **Description**: The 'Continue Quest' button finds the first incomplete lesson. If all lessons are complete, `next` is undefined and `navigate(undefined)` does nothing silently — the button still renders but is dead.
- **Suggested fix**: Show 'All quests complete!' or navigate to a review/celebration page when done.

#### 19. CourseMap redundant totalLessons/completedCount from useProgress vs props [INFO]
- **File**: frontend/src/components/CourseMap.tsx:10-11
- **Category**: ux
- **Description**: CourseMap receives `lessons` as a prop AND calls useProgress() for progress data. But it also destructures `totalLessons` and `completedCount` from useProgress() while computing `total` from both. If the two progress sources disagree, the UI is inconsistent.
- **Suggested fix**: Use a single source of truth — either props or the hook, not both.

#### 20. isLessonUnlocked return true when lessons array is empty (loading) [INFO]
- **File**: frontend/src/pages/LessonPage.tsx:84
- **Category**: resilience
- **Description**: When lessons array is empty (still loading), isLessonUnlocked returns true because findIndex returns -1 and idx <= 0 is true. This means locked lessons shown briefly as unlocked before the correct state loads from the API.
- **Suggested fix**: Add a loading guard — if lessons array is empty, show a skeleton instead of rendering lesson content.

---

## 5. Content Quality Issues

### 5a. Typos / Potential Issues (Random Sample of 10 Lessons)

| Lesson | Issues |
|--------|--------|
| 4-27 | extra whitespace (double space); long Latin text in Russian field (possible untranslated) |
| 2-6 | extra whitespace (double space); long Latin text in Russian field (possible untranslated) |
| 1-4 | long Latin text in Russian field (possible untranslated) |
| 3-21 | long Latin text in Russian field (possible untranslated) |
| 3-17 | style: 'будет ... если' may be clearer word order; extra whitespace (double space); long Latin text in Russian field (possible untranslated) |
| 3-14 | extra whitespace (double space); long Latin text in Russian field (possible untranslated) |
| 3-3 | spacing: 'потому что' usually requires space; long Latin text in Russian field (possible untranslated) |
| 2-5 | extra whitespace (double space); long Latin text in Russian field (possible untranslated) |
| 3-41 | extra whitespace (double space); long Latin text in Russian field (possible untranslated) |
| 4-15 | long Latin text in Russian field (possible untranslated) |

**Note on Russian language**: The course content is in Russian. Pattern-based spell checking for Russian is limited without a full dictionary. The pattern search focused on common mistakes like `тся`/`ться` confusion, missing soft signs in 2nd-person verbs, stray Latin text in Russian fields, and doubled spaces. No critical typos were detected, but a full linguistic review with a native speaker is recommended for the entire corpus.

### 5b. Unpaired Backticks

All backtick pairs are properly matched across the course.

### 5c. Empty Required Fields

All required fields are properly populated.

### 5d. Difficulty Curve Analysis

**Lesson difficulty sequence**:

```
Part 1:
  1-1: easy
  1-2: easy
  1-3: easy
  1-4: easy
  1-5: easy
  1-6: easy
  1-7: easy
  1-8: easy
  1-9: medium

Part 2:
  2-1: easy
  2-2: medium
  2-3: easy
  2-4: easy
  2-5: easy
  2-6: medium

Part 3:
  3-1: easy
  3-2: medium
  3-3: medium
  3-4: medium
  3-5: medium
  3-6: easy
  3-7: medium
  3-8: medium
  3-9: easy
  3-10: easy
  3-11: easy
  3-12: medium
  3-13: hard
  3-14: easy
  3-15: medium
  3-16: medium
  3-17: medium
  3-18: easy
  3-19: easy
  3-20: easy
  3-21: medium
  3-22: medium
  3-23: medium
  3-24: medium
  3-25: medium
  3-26: easy
  3-27: medium
  3-28: medium
  3-29: medium
  3-30: medium
  3-31: medium
  3-32: medium
  3-33: medium
  3-34: medium
  3-35: medium
  3-36: medium
  3-37: medium
  3-38: medium
  3-39: easy
  3-40: easy

Part 4:
  4-1: medium
  4-2: medium
  4-3: medium
  4-4: medium
  4-5: medium
  4-6: medium
  4-7: easy
  4-8: medium
  4-9: medium
  4-10: easy
  4-11: medium
  4-12: medium
  4-13: medium
  4-14: medium
  4-15: easy
  4-16: easy
  4-17: medium
  4-18: hard
  4-19: hard
  4-20: hard
  4-21: medium
  4-22: medium
  4-23: medium
  4-24: medium
  4-25: medium
  4-26: medium
  4-27: medium
  4-28: medium
  4-29: medium
  4-30: medium
  4-31: boss

Part 3:
  3-41: boss

Part 5:
  5-1: medium
  5-2: medium
  5-3: medium
  5-4: medium
  5-7: medium
```

**Issues detected in difficulty curve**:

- Part 2: 2-3 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 3: 3-6 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 3: 3-9 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 3: 3-14 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 3: 3-18 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 3: 3-26 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 3: 3-39 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 4: 4-7 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 4: 4-10 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 4: 4-15 has difficulty 'easy' after a harder lesson (regression in curve)
- Part 4: 4-21 has difficulty 'medium' after a harder lesson (regression in curve)

### 5e. Additional Content Observations

- **Total lessons evaluated**: 92
- **Difficulty distribution**: easy=28, medium=58, hard=4, boss=2
- **Parts**: 5
- **All lessons have mini_summary**: True
- **All lessons have explanation.text**: True
- **All lessons have quiz.question**: True

**Subtitle/discrepancy issues from Persona 20 audit**:

- Lesson 4-31 (boss) has mission/code example inconsistency — code always wins but task expects wrong guess handling
- Several subtitles are wrong: 4-15 shows 'Логическое ИЛИ' instead of 'Сортировка', 4-9 shows 'Поиск в тексте' instead of 'Объединение строк'

---

## 6. Priority Fix List (P0 / P1 / P2)

### P0 — Must Fix (Critical)

- **Move SteampunkCard component outside LessonPage function body to prevent unmount/remount on every render** (`frontend/src/pages/LessonPage.tsx`)
- **Replace `<a href>` with React Router `<Link>` in CourseMap to prevent full page reloads** (`frontend/src/components/CourseMap.tsx`)
- **Fix `crypto.randomUUID()` to have fallback for non-HTTPS/older browsers** (`frontend/src/utils/userId.ts`)
- **Remove duplicate `mini_summary` outer conditional block in LessonPage lines 295-299** (`frontend/src/pages/LessonPage.tsx`)

### P1 — High Priority

- **Increase mission complexity: ensure that from lesson 2-5 onward, missions require combining multiple concepts, not just replicating examples** (`backend/app/data/lessons.json (Persona 20)`)
- **Move Bool/boolean introduction earlier — ideally right after `if` (lesson 1-8) or as part of it, not lesson 3-6** (`backend/app/data/lessons.json`)
- **Fix Bagus dialogue to be constructive rather than mocking ('Kha-kha! Typical newbie mistake!')** (`backend/app/data/lessons.json (multiple lessons)`)
- **Reduce dialogue repetition: analogy should be stated once, not repeated verbatim by Novice in pre_topic_dialogue, analogy, and game_relevance** (`backend/app/data/lessons.json (multiple lessons)`)
- **Lesson 3-8: Separate 'if-found shorthand' from 'ternary operator' — currently mixed, scope confusion** (`backend/app/data/lessons.json`)
- **Fix lesson 4-31 boss mission: code example has guess=secret always succeeding, but task asks for different behavior — inconsistent** (`backend/app/data/lessons.json`)
- **Fix Reviews fetch: add loading state, error handling, and AbortController cleanup in HomePage.tsx** (`frontend/src/pages/HomePage.tsx`)
- **Surface useLessons() error in Layout/Sidebar when lessons API fails** (`frontend/src/hooks/useApi.ts`)
- **Fix CodePlayground line numbers contrast (~3.47:1 fails WCAG AA)** (`frontend/src/components/CodePlayground.tsx`)
- **Add accessible label to code textarea in CodePlayground** (`frontend/src/components/CodePlayground.tsx`)

### P2 — Medium Priority

- **Fix wrong subtitles: 4-15 shows 'Logical OR' should be 'Sorting'; 4-9 shows 'Text search' should be 'String join'** (`backend/app/data/lessons.json`)
- **Split boss lesson 4-31 into 2 x 25 min segments for 10-year-old attention span** (`backend/app/data/lessons.json`)
- **Replace 'итерация' with 'шаг'/'повторение' in syntax reminders visible to children (lessons 2-5, 3-14)** (`backend/app/data/lessons.json`)
- **Replace English 'Loading lesson...' with Russian equivalent in loading spinner** (`frontend/src/pages/LessonPage.tsx`)
- **Add tooltips for steampunk terms ('Aether', 'Resonance', 'Adept') on HomePage** (`frontend/src/pages/HomePage.tsx`)
- **Add child-friendly definitions for 'аргумент' and 'параметр' in lesson 5-1** (`backend/app/data/lessons.json`)
- **Add loading/error state to useProgress() to prevent flash of incorrect state** (`frontend/src/hooks/useApi.ts`)
- **Add retry mechanism for Pyodide load failure** (`frontend/src/components/CodePlayground.tsx`)
- **Fix QuizSection error handling: show distinct 'Connection error' when API fails instead of misleading 'Wrong'** (`frontend/src/components/QuizSection.tsx`)
- **Guard against `prefers-reduced-motion` in Bagus error feedback bounce animation** (`frontend/src/components/MissionCard.tsx`)
- **Add request timeout (AbortSignal) to fetch calls in checkQuizAnswer/checkWhatOutputs** (`frontend/src/hooks/useApi.ts`)
- **Remove unused DialogueBubble import from LessonPage.tsx** (`frontend/src/pages/LessonPage.tsx`)
- **Fix 'Continue Quest' button for all-lessons-complete state (show celebration message)** (`frontend/src/pages/HomePage.tsx`)
- **Add loading guard for isLessonUnlocked when lessons array is empty (prevents flash of unlocked locked lessons)** (`frontend/src/pages/LessonPage.tsx`)
- **Reduce dialogue length in lessons where Novice character repeats analogy verbatim (Persona 20 issue)** (`backend/app/data/lessons.json (multiple lessons)`)

---

*Report generated on 2026-05-31 by combining:
- `scripts/audit_persona_10.json` (16 lessons, child-friendliness)
- `scripts/audit_persona_20.json` (16 lessons, young adult perspective)
- `scripts/audit_technical_ux.json` (19 technical findings)
- Automated content analysis of `backend/app/data/lessons.json` (92 lessons total)*