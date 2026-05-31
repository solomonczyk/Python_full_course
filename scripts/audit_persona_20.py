#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit lessons from a 20-year-old young adult perspective.
Simulate: 20yo, modern Russian, learning Python for real.
"""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

with open('backend/app/data/lessons.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ids_to_check = ['1-1','1-3','1-8','2-1','2-3','2-5','3-6','3-8','3-22','3-35',
                '4-9','4-14','4-15','4-21','4-24','4-31','5-1','5-4']
lessons = {l['id']: l for l in data if l['id'] in ids_to_check}

def rate(lesson_id, pacing, depth, theme, relevance, challenge, language,
         overall, note=""):
    return {
        "id": lesson_id,
        "title": lessons[lesson_id]['title'],
        "ratings": {
            "pacing": pacing,
            "depth": depth,
            "theme": theme,
            "relevance": relevance,
            "challenge": challenge,
            "language": language
        },
        "overall": overall,
        "note": note
    }

results = []

# ---- 1-1: print() ----
results.append(rate("1-1",
    "ACCEPTABLE",  # First lesson, slow is OK, but "cave echo" analogy repeated 3x in dialogue+analogy+game_relevance
    "GOOD",        # Appropriate depth for lesson 1
    "GOOD",        # "Глашатай на площади" fits steampunk, fine for 20yo
    "GOOD",        # print is literally the first thing you learn, relevance is clear
    "ACCEPTABLE",  # Mission: print one line. Trivial but OK for absolute zero. Practice tasks add slight challenge.
    "GOOD",        # Modern Russian, informal ты, clear. Bagus laughing ("Ха-ха!") is mildly annoying but not a big deal.
    "ACCEPTABLE",
    "Strong start, but the 'cave echo' metaphor is overused (dialogue + analogy + relevance all repeat it). Novice character seems unnecessarily clueless — a 20yo would get it faster. Bagus mocks mistakes which feels bad."
))

# ---- 1-3: Переменные ----
results.append(rate("1-3",
    "ACCEPTABLE",  # Chest analogy is fine but repeated across every section
    "ACCEPTABLE",  # Covers assignment, printing, and the name/string trap. But doesn't touch reassignment or dynamic typing.
    "GOOD",        # "Волшебный сундук" fits the RPG theme
    "GOOD",        # Variables = core concept, connection to game storage is clear
    "ACCEPTABLE",  # Basic mission but the swap-values subtask is genuinely good
    "GOOD",
    "ACCEPTABLE",
    "Solid lesson. Swap-values subtask is a highlight — actually makes you think. But Novice asking 'is that like a chest?' after Ksyu already explained the chest is too much handholding."
))

# ---- 1-8: if ----
results.append(rate("1-8",
    "GOOD",        # "Bouncer at club" is a tight analogy, doesn't overstay
    "ACCEPTABLE",  # Covers if condition, indentation, comparison. No mention of truthy/falsy yet.
    "GOOD",        # Bouncer = relatable social scenario for 20yo
    "GOOD",        # if is universal, game connection (check HP, items) is natural
    "ACCEPTABLE",  # Mission: if x > 0 -> Плюс. Very easy.
    "GOOD",
    "ACCEPTABLE",
    "The 'bouncer at club' analogy actually works well for 20-year-olds. Indentation bug (find_bug) is excellent. But Novice's dialogue responses are too obvious — real 20yo would connect faster."
))

# ---- 2-1: elif ----
results.append(rate("2-1",
    "GOOD",
    "GOOD",        # Multiple conditions, the if/elif/else chain, real decision trees
    "GOOD",        # "Three bridges with guards" is creative and RPG-appropriate
    "GOOD",        # Clear: class selection, command processing in game
    "GOOD",        # Mission: hero class branching — decent. Practice: grade by score is real-world.
    "GOOD",
    "GOOD",
    "One of the better lessons. Three bridges analogy maps cleanly to elif chain. Find_bug with if/if instead of if/elif is a real-world bug beginners actually make. Mission is reasonably challenging."
))

# ---- 2-3: random.randint ----
results.append(rate("2-3",
    "GOOD",        # Magic bag analogy is concise
    "ACCEPTABLE",  # Covers import, call, range. But doesn't explain modules meaningfully.
    "GOOD",        # Dice rolling fits RPG perfectly
    "GOOD",        # Randomness is game-critical. 'import random' is a key concept.
    "PROBLEMATIC", # Mission: just print "Бросок сделан!" — doesn't even require using the random value. Expected output is a static string. That's too easy for lesson 2-3.
    "GOOD",
    "ACCEPTABLE",
    "Good concept execution but the mission is a miss: expected output is literally 'Бросок сделан!' — no random value needed. A 20yo would find this trivial. The find_bug (missing import) is great though."
))

# ---- 2-5: for loop ----
results.append(rate("2-5",
    "ACCEPTABLE",  # Factory conveyor is fine but over-explained
    "ACCEPTABLE",  # Covers only range(N) with for. No range(start, stop) or iterating over lists yet.
    "GOOD",        # Steampunk factory theme works
    "GOOD",        # Loops = bread and butter of programming
    "PROBLEMATIC", # Mission: print 'Python' 3 times. Expected output is just 'Python\n' — but mission says 3 times. Wait, expected_output='Python' — that's wrong? Shows 3 lines in code example but expected is single. Inconsistency.
    "GOOD",
    "PROBLEMATIC",
    "Mission expected_output='Python' (single) contradicts the task (print 3 times). This inconsistency would confuse a learner. The practice subtasks (print numbers 1-5) are better but still basic. Missing list iteration."
))

# ---- 3-6: Bool ----
results.append(rate("3-6",
    "ACCEPTABLE",  # Light switch analogy is clear but stretched
    "PROBLEMATIC", # Bool is introduced in LESSON 6 of CHAPTER 3. That's extremely late for such a fundamental type. Comparisons, conditions, and if statements were already used in lessons 1-8 through 2-5 without explaining bool.
    "GOOD",        # "Выключатель" fits steampunk well
    "ACCEPTABLE",  # Bool is essential but the timing is off
    "PROBLEMATIC", # Mission: create True, print True. Zero challenge for lesson 3-6. Should by now use bool in real conditions.
    "GOOD",
    "PROBLEMATIC",
    "Bool introduced way too late (lesson 3-6). Students have been writing if statements since lesson 1-8 without understanding what a condition actually returns. This should be right after or along with if. Mission is trivial."
))

# ---- 3-8: Короткая запись условий ----
results.append(rate("3-8",
    "PROBLEMATIC", # The lesson is confused — tries to cover both `if found:` shorthand AND ternary operator, but doesn't clearly separate them
    "PROBLEMATIC", # Explanation text is about checking bool directly (`if is_ready:`). Analogy is about ternary. Practice subtasks are about ternary. Mission is about `if found:`. No coherent scope.
    "ACCEPTABLE",  # Speed lane analogy for ternary is fine
    "ACCEPTABLE",  # Both concepts are useful but muddled presentation
    "ACCEPTABLE",  # Individually the tasks are fine
    "GOOD",
    "PROBLEMATIC",
    "Scope confusion: title says 'short condition notation', explanation covers `if found:` shorthand, analogy covers ternary, practice covers ternary, mission covers `if found:`. These are two different concepts. Pick one or clearly separate them."
))

# ---- 3-22: F-строка ----
results.append(rate("3-22",
    "GOOD",        # Birthday card with blanks — concise, memorable
    "GOOD",        # Covers f-string syntax, variable insertion, expression evaluation. Appropriate depth.
    "GOOD",        # Трафарет/printing press fits steampunk
    "GOOD",        # f-strings are daily drivers in Python
    "GOOD",        # Mission: compose "Герой Андрей: 5" from two variables. Multi-step, reasonable.
    "GOOD",
    "GOOD",
    "Clean lesson. Great analogy (birthday card with blanks), good progression, mission is appropriately challenging for medium difficulty. One of the best structured lessons."
))

# ---- 3-35: Фильтрация списка ----
results.append(rate("3-35",
    "GOOD",        # Colored balls analogy is simple and clear
    "GOOD",        # Covers both loop+if pattern and list comprehension. Good depth.
    "GOOD",        # Sorting factory/gears fits well
    "GOOD",        # Filtering is a core pattern in any language
    "GOOD",        # Filter odds from [1,3,5,2,4] — good multi-step. Practice tasks (even numbers, short words) are solid.
    "GOOD",
    "GOOD",
    "Solid medium-difficulty lesson. The find_bug (using n without defining it/loop) is excellent. List comprehension is introduced naturally. Good balance of theory and practice."
))

# ---- 4-9: join ----
results.append(rate("4-9",
    "GOOD",        # "Beads on string" is intuitive, not over-explained
    "GOOD",        # Covers separator, list of strings requirement, generator expression for int conversion
    "GOOD",        # Beads/string crafting fits theme
    "GOOD",        # join is used everywhere in real Python
    "ACCEPTABLE",  # Mission: join ['a','b','c'] with space. Simple but find_bug with int list adds challenge.
    "GOOD",
    "GOOD",
    "Effective lesson. The find_bug (join with int list) is a genuinely useful trap. Clean explanation, good analogy. The subtitle says 'Поиск в тексте' (text search) which doesn't match join — cosmetic bug."
))

# ---- 4-14: map ----
results.append(rate("4-14",
    "GOOD",        # Factory stamp analogy is tight
    "ACCEPTABLE",  # Covers map() application but doesn't discuss map objects (lazy evaluation) or when to use list(map(...))
    "GOOD",        # Factory/assembly line fits steampunk
    "GOOD",        # Transforming collections is fundamental
    "GOOD",        # Mission: split string, map(int), sum — multi-step, builds real skill
    "GOOD",
    "GOOD",
    "Good lesson with a practical multi-step mission. The pipeline (split -> map -> sum) is a realistic pattern. Find_bug (sum of strings) is perfect. Could mention that map returns an iterator."
))

# ---- 4-15: sort ----
results.append(rate("4-15",
    "GOOD",        # Bookshelf analogy is clean
    "ACCEPTABLE",  # Covers sort() in-place, reverse parameter. Doesn't cover sorted() — which is arguably more useful and safer.
    "GOOD",        # Bookshelf is universal
    "GOOD",        # Sorting is practical
    "GOOD",        # Mission: straightforward. Find_bug with sort() returning None is ESSENTIAL — excellent.
    "GOOD",
    "GOOD",
    "Well-focused lesson. The find_bug (sort() returns None) is the absolute highlight — this confuses every beginner. Would benefit from also mentioning sorted() for immutable sorting. The subtitle says 'Логическое ИЛИ' (logical OR) which is completely wrong — should be 'Сортировка'."
))

# ---- 4-21: Ссылки ----
results.append(rate("4-21",
    "GOOD",        # Two remotes, one TV — immediately understood by 20yo
    "GOOD",        # References are conceptually deep, explained well with mutation example
    "GOOD",        # Two pulleys/remotes fits adequately
    "GOOD",        # Reference semantics is critical Python knowledge
    "GOOD",        # Mission: a=[], b=a, b.append(3), print(a). Tests understanding perfectly. Find_bug with b.append(2) return value is excellent.
    "GOOD",
    "GOOD",
    "One of the best lessons. Two-remotes analogy is perfect for 20-year-olds. The reference vs copy distinction is one of the hardest concepts for beginners, and this lesson nails it. Great find_bug and practice tasks."
))

# ---- 4-24: copy ----
results.append(rate("4-24",
    "GOOD",        # Xerox cover analogy for shallow copy is clear
    "GOOD",        # Covers shallow copy and nested list behavior
    "GOOD",        # Book xerox fits the theme
    "GOOD",        # Copy vs reference is essential
    "GOOD",        # Mission tests understanding cleanly. Practice task with nested lists is excellent.
    "GOOD",
    "GOOD",
    "Excellent follow-up to lesson 4-21. The nested list mutation practice task is the highlight — it shows exactly why shallow copy isn't always enough. Good progression from reference -> copy -> deep copy awareness."
))

# ---- 4-31: random + while игра ----
results.append(rate("4-31",
    "ACCEPTABLE",  # Packing a backpack analogy tries to cover too many concepts at once
    "GOOD",        # Boss-level lesson combining while, random, break, conditions — appropriately comprehensive
    "GOOD",        # "Великое приключение" fits the RPG theme
    "GOOD",        # Building a complete game is the culmination
    "PROBLEMATIC", # Mission is confusing: secret=2, always wins with guess=2, but expected_output=2 (remaining attempts after wrong guess?). The code example and task description don't align.
    "GOOD",
    "PROBLEMATIC",
    "Great concept (boss lesson combining everything) but flawed execution. The code example has guess=secret always succeeding, but the task asks for 'remaining attempts after first wrong guess'. Inconsistent. 50min difficulty is appropriate but the mission design needs rework."
))

# ---- 5-1: Кнопка на пульте ----
results.append(rate("5-1",
    "GOOD",        # TV remote button — universal, immediate understanding
    "ACCEPTABLE",  # Covers def, call, indentation. Doesn't cover parameters or return values yet.
    "GOOD",        # Remote control fits steampunk well
    "GOOD",        # Functions are THE organizing principle of code
    "ACCEPTABLE",  # Mission: define greet() and call it. Appropriate for intro. Practice: three bells is slightly repetitive.
    "GOOD",
    "GOOD",
    "Remote control is the perfect analogy for functions — a 20yo has never thought about how a TV button works, which is exactly the point. Good intro but needs parameters and return in follow-up lessons to feel complete."
))

# ---- 5-4: Телефонная книга ----
results.append(rate("5-4",
    "ACCEPTABLE",  # Phonebook analogy is slightly dated (young adults use contacts, not yellow pages) but still understandable
    "ACCEPTABLE",  # Covers dict creation, key access, KeyError. Doesn't cover dict methods (.get, .keys, .items) which are essential.
    "ACCEPTABLE",  # Phonebook is a bit mundane for steampunk RPG but works
    "GOOD",        # Dicts are fundamental for game state
    "PROBLEMATIC", # Mission: create dict with one key, print it. Pathetically easy for lesson 5-4 (penultimate lesson).
    "GOOD",
    "ACCEPTABLE",
    "Content is correct but the mission is far too easy for a lesson this late (5-4). By lesson ~60, a 20yo should be building small multi-step programs, not 'create one key-value pair'. The telephone book subtitle is 'Храним данные по ключам' which is accurate, but the chapter 5 placement means students should handle more complex tasks."
))

# General observations
general = {
    "general_observations": {
        "positive": [
            "Analogy quality is generally high — 'two remotes one TV' (4-21), 'bouncer at club' (1-8), 'birthday card' (3-22) are genuinely good",
            "Find_bug exercises are consistently excellent across all lessons — real-world mistakes, not contrived",
            "Practice subtasks add meaningful reinforcement beyond the main mission",
            "F-strings, join, map, references, copy, sort, filter — the chapter 3-4 lessons are very strong",
            "Russian language is natural, modern, avoids both overly formal and cringey slang",
            "Steampunk RPG theme is consistent and creates a coherent identity"
        ],
        "issues": [
            "MISSIONS are often too easy: many ask to replicate the exact code example with minor changes. By lesson 5-4, a 20yo should write multi-step programs",
            "DIALOGUE repetition: analogy is stated in pre_topic_dialogue, then again in analogy section, then again in game_relevance. Novice character always repeats the analogy back verbatim — patronizing for 20yo",
            "BAGUS character mocks mistakes ('Ха-ха! Типичная ошибка новичка!') — this is actively demotivating for a young adult learner",
            "BOOL introduced too late (3-6) — students use conditions from 1-8 without understanding what a boolean is",
            "Lesson 3-8 mixes two unrelated concepts (if-found shorthand AND ternary operator) with no clear separation",
            "Lesson 4-31 (boss) has mission/code example inconsistency — code always wins but task expects wrong guess handling",
            "Several subtitles are wrong: 4-15 shows 'Логическое ИЛИ' instead of 'Сортировка', 4-9 shows 'Поиск в тексте' instead of 'Объединение строк'",
            "CompletionPage.tsx has no progressive roadmap — just redirects to lesson 1-1 if incomplete. No 'you are here' milestone visualization"
        ],
        "for_20yo_summary": (
            "The course is ACCEPTABLE for a 20-year-old but has clear marks of being designed for a younger audience. "
            "The steampunk RPG theme is not a problem — it's well-executed and consistent. The real issues are: "
            "(1) missions lack bite — most replicate examples, "
            "(2) dialogue is too repetitive with the Novice character being overly slow on the uptake, "
            "(3) Bagus laughing at mistakes would annoy any self-respecting 20yo, "
            "(4) the late bool introduction and confused 3-8 lesson show structural curriculum issues. "
            "The strongest part is the chapter 4 sequence (join, map, sort, references, copy) which is genuinely well-structured. "
            "With harder missions, less patronizing dialogue, and curriculum reordering, this could be excellent for young adults."
        )
    }
}

output = {
    "meta": {
        "audit_type": "persona_20",
        "persona": "20-year-old young adult, modern Russian speaker, beginner programmer, steampunk/RPG fan",
        "criteria": ["pacing", "depth", "theme", "relevance", "challenge", "language"],
        "date": "2026-05-31"
    },
    "lessons": results,
    **general,
    "completion_page_review": {
        "file": "frontend/src/pages/CompletionPage.tsx",
        "useful_as_roadmap": False,
        "note": (
            "CompletionPage is a finish-line screen, not a roadmap. It has no 'you are here' indicator, "
            "no milestone tracking, no part/chapter progression visualization. The skills checklist (7 items) is "
            "reasonable for the course scope. The next-steps links (FastAPI, pandas, selenium, LeetCode) are useful "
            "post-course suggestions. But a true roadmap would show lesson parts, completion percentage per part, "
            "and the student's current position in the broader curriculum — none of which exist here."
        )
    }
}

with open('scripts/audit_persona_20.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Written {len(results)} lesson audits to scripts/audit_persona_20.json")
