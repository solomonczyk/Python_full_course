#!/usr/bin/env python3
"""
Comprehensive audit script for Python Full Course lessons.

Reads backend/app/data/lessons.json, checks every lesson for issues,
and outputs a report to scripts/audit_report.json.

Categories checked:
  A. Dialogues (pre_topic_dialogue, post_error_dialogue)
  B. what_outputs (Predict Output)
  C. find_bug
  D. quiz
  E. mission
  F. practice_subtasks
"""

import json
import os
import sys
import re


def load_lessons(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

TOPIC_KEYWORDS = {
    "print": ["print", "вывод", "печать", "вывес"],
    "строки": ["строк", "кавычк", "текст", "str"],
    "переменные": ["перемен", "присваив", "="],
    "input": ["input", "ввод", "введ"],
    "int(input": ["int", "преобраз", "числ"],
    "арифметик": ["арифмет", "+", "-", "*", "/", "сложен", "вычитан"],
    "сравнения": [">", "<", "==", "!=", "сравн"],
    "if": ["if", "услови", "ветвлен"],
    "elif": ["elif", "else if", "множествен"],
    "логические": ["and", "or", "not", "логическ"],
    "random.randint": ["random", "randint", "случайн"],
    "простая": ["угадай", "игр", "randint"],
    "первое": ["for", "цикл", "повторен"],
    "for": ["for", "range", "повтор"],
    "range": ["range", "for"],
    "списки": ["спис", "list", "индекс"],
    "методы": ["метод", ".append", ".pop", ".sort"],
    "break": ["break", "прерыв"],
    "continue": ["continue", "пропуск"],
    "while": ["while", "пока"],
}

CHARACTER_PROFILES = {
    "novice": {
        "traits": ["curious", "beginner", "simplifies", "asks questions"],
        "keywords": ["понял", "значит", "то есть", "как", "почему"],
    },
    "ksyu": {
        "traits": ["gentle", "patient", "uses metaphors", "encouraging"],
        "keywords": ["представ", "как", "коробк", "сундук"],
    },
    "va": {
        "traits": ["logical", "direct", "technical", "precise"],
        "keywords": ["типичная", "ошибка", "правиль"],
    },
    "da": {
        "traits": ["practical", "action-oriented", "mission-focused"],
        "keywords": ["давай", "сделай", "напиши"],
    },
}


def flatten_text(dialogue_list):
    """Extract all text from a list of dialogue dicts."""
    texts = []
    for d in dialogue_list:
        if isinstance(d, dict) and "text" in d:
            texts.append(d["text"])
    return texts


def count_words(text):
    return len(text.split())


def is_overly_long(text, max_words=70):
    """Check if a dialogue line is too long / info-dense."""
    return count_words(text) > max_words


def extract_code_string(code):
    """Normalize a code string for analysis (remove comments, strip)."""
    lines = []
    for line in code.split("\n"):
        # Remove single-line comments
        clean = line.split("#")[0].strip()
        if clean:
            lines.append(clean)
    return "\n".join(lines)


def contains_function(code, keywords):
    """Check if code contains any of the given keywords."""
    code_lower = code.lower()
    return any(kw.lower() in code_lower for kw in keywords)


def safe_run(code_snippet):
    """
    Attempt to evaluate/execute a snippet to validate determinism.
    Returns (output, error) tuple.
    """
    import subprocess
    import tempfile

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            # Add a print wrapper for expressions
            if "\n" not in code_snippet.strip() and not any(
                kw in code_snippet for kw in ["\n", "if ", "for ", "while ", "import "]
            ):
                full_code = f"print({code_snippet})"
            else:
                full_code = code_snippet
            f.write(full_code)
            f.flush()
            result = subprocess.run(
                [sys.executable, f.name],
                capture_output=True,
                text=True,
                timeout=5,
                input="",
            )
        os.unlink(f.name)
        if result.returncode != 0:
            return None, result.stderr.strip()
        return result.stdout.strip(), None
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def check_dialogues(lesson, lesson_id, title):
    """Check pre_topic_dialogue and post_error_dialogue."""
    issues = []

    for block_name in ("pre_topic_dialogue", "post_error_dialogue"):
        dialogue = lesson.get(block_name, [])
        if not dialogue:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": block_name,
                "issue": f"{block_name} is missing or empty",
                "detail": "No dialogue found",
            })
            continue

        characters_seen = set()
        for turn in dialogue:
            if not isinstance(turn, dict):
                continue
            char = turn.get("character", "")
            text = turn.get("text", "")
            characters_seen.add(char)

            # Check for overly long lines
            if is_overly_long(text):
                issues.append({
                    "id": lesson_id,
                    "title": title,
                    "severity": "info",
                    "block": f"{block_name}.{char}",
                    "issue": f"Dialogue line is too long ({count_words(text)} words)",
                    "detail": text[:100] + ("..." if len(text) > 100 else ""),
                })

            # Check character stays in character
            if char == "novice":
                # Novice should sound like a beginner discovering things
                if any(phrase in text.lower() for phrase in ["типичная ошибка", "это стандартный", "используй", "должен"]):
                    issues.append({
                        "id": lesson_id,
                        "title": title,
                        "severity": "warning",
                        "block": f"{block_name}.novice",
                        "issue": "Novice sounds too expert (giving advice, not asking)",
                        "detail": text[:100],
                    })
            elif char == "va":
                # VA should be logical/technical, not too metaphorical
                metaphor_words = ["представ", "сказк", "волшебн", "сундук"]
                if sum(1 for m in metaphor_words if m in text.lower()) >= 2:
                    issues.append({
                        "id": lesson_id,
                        "title": title,
                        "severity": "info",
                        "block": f"{block_name}.va",
                        "issue": "VA using too many metaphors (VA should be logical/technical)",
                        "detail": text[:100],
                    })

        # Check that at least novice and one teacher appear in pre_topic
        if block_name == "pre_topic_dialogue":
            if "novice" not in characters_seen:
                issues.append({
                    "id": lesson_id,
                    "title": title,
                    "severity": "warning",
                    "block": block_name,
                    "issue": "Novice character missing from pre_topic_dialogue",
                    "detail": f"Characters present: {characters_seen}",
                })
            if not characters_seen.intersection({"ksyu", "va", "da"}):
                issues.append({
                    "id": lesson_id,
                    "title": title,
                    "severity": "warning",
                    "block": block_name,
                    "issue": "No teacher character (ksyu/va/da) in pre_topic_dialogue",
                    "detail": f"Characters present: {characters_seen}",
                })

    return issues


def check_what_outputs(lesson, lesson_id, title):
    """Check the what_outputs block."""
    issues = []
    wo = lesson.get("what_outputs")
    if not wo:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "what_outputs",
            "issue": "what_outputs block is missing",
            "detail": "No what_outputs found",
        })
        return issues

    code = wo.get("code", "")
    options = wo.get("options", [])
    correct = wo.get("correct", "")

    if not code:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "what_outputs",
            "issue": "what_outputs code is empty",
            "detail": "No code provided",
        })
        return issues

    if not options:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "what_outputs",
            "issue": "what_outputs options are empty",
            "detail": "No options provided",
        })

    if not correct:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "what_outputs",
            "issue": "what_outputs correct answer is empty",
            "detail": "No correct answer provided",
        })
        return issues

    # Check if correct answer is actually in options
    if correct not in options:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "what_outputs",
            "issue": "Correct answer not in options list",
            "detail": f"Correct: '{correct}', Options: {options}",
        })

    # Check for duplicate options
    if len(options) != len(set(options)):
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "what_outputs",
            "issue": "Duplicate options in what_outputs",
            "detail": f"Options: {options}",
        })

    # Check if code uses input() - if so, it's non-deterministic / can't predict
    if "input()" in code:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "what_outputs",
            "issue": "Code uses input() making output non-deterministic without stdin",
            "detail": f"Code: {code[:100]}",
        })

    # Check if code uses random - then output is non-deterministic
    if "random." in code or "randint" in code:
        # Check if the correct answer depends on random
        # If it's always True (e.g., checking bounds), it's fine
        # If it's a specific number, it's non-deterministic
        if not any(
            marker in correct.lower() for marker in ["true", "false", "ошибк"]
        ):
            # Check if it's a logic expression that always returns same
            # Let's flag it as info
            pass  # We'll just flag the random usage lightly

    # Try to execute the code and see if it matches the correct answer
    try:
        output, error = safe_run(code)
        if error:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "warning",
                "block": "what_outputs",
                "issue": f"Code execution error: {error[:100]}",
                "detail": f"Code: {code[:150]}",
            })
        elif output is not None and output != correct:
            # If output doesn't match correct, check if it's a random-based lesson
            if "random" not in code:
                issues.append({
                    "id": lesson_id,
                    "title": title,
                    "severity": "error",
                    "block": "what_outputs",
                    "issue": f"Actual output '{output}' doesn't match expected correct '{correct}'",
                    "detail": f"Code: {code[:150]}",
                })
    except Exception as e:
        pass

    # Check distractor plausibility
    if len(options) >= 2:
        # Check if "None" is always an option - might indicate lazy distractor
        none_count = sum(1 for o in options if o.strip() in ("None",))
        # This is sometimes fine, so just info
        if none_count > 0 and len(options) >= 3:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "info",
                "block": "what_outputs",
                "issue": "None appears as an option (may be a lazy distractor)",
                "detail": f"Options: {options}",
            })

    # Check topic relevance
    topic = lesson.get("topic", "").lower()
    topic_kws = []
    for t_key, kws in TOPIC_KEYWORDS.items():
        if t_key in topic or any(kw in topic for kw in kws):
            topic_kws.extend(kws)
    if topic_kws:
        if not contains_function(code, topic_kws):
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "info",
                "block": "what_outputs",
                "issue": "Code may not use the topic's key concept",
                "detail": f"Topic: '{topic}', Code: {code[:100]}",
            })

    return issues


def check_find_bug(lesson, lesson_id, title):
    """Check the find_bug block."""
    issues = []
    fb = lesson.get("find_bug")
    if not fb:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "find_bug",
            "issue": "find_bug block is missing",
            "detail": "No find_bug found",
        })
        return issues

    code = fb.get("code", "")
    hint = fb.get("hint", "")
    correct = fb.get("correct", "")
    description = fb.get("description", "")

    if not code:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "find_bug",
            "issue": "find_bug code is empty",
            "detail": "No buggy code provided",
        })

    if not hint:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "find_bug",
            "issue": "find_bug hint is missing",
            "detail": "No hint provided",
        })

    if not correct:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "find_bug",
            "issue": "find_bug correct answer is missing",
            "detail": "No correct code provided",
        })

    if code and correct:
        # Check if correct is actually the fixed version
        if code == correct:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "find_bug",
                "issue": "Buggy code and correct code are identical — no bug to find",
                "detail": f"Code: {code[:100]}",
            })

    if hint:
        # Check if hint gives away the answer too directly
        hint_lower = hint.lower()
        giveaways = [
            "добавь кавычки", "добавь отступ", "используй int",
            "замени на", "убери кавычки",
        ]
        for g in giveaways:
            if g in hint_lower:
                # Only flag if hint literally says what to change
                if any(
                    exact in hint_lower
                    for exact in ["добавь кавычки", "замени на", "убери кавычки"]
                ):
                    issues.append({
                        "id": lesson_id,
                        "title": title,
                        "severity": "info",
                        "block": "find_bug",
                        "issue": f"Hint may give away the answer: '{g}'",
                        "detail": f"Hint: {hint[:150]}",
                    })
                break

    # Check if the bug relates to the topic
    topic = lesson.get("topic", "").lower()
    # Try to see if code error relates to topic
    if topic and code:
        topic_related_errors = {
            "print": ["кавычк", "print"],
            "строк": ["кавычк", "строк"],
            "перемен": ["перемен", "="],
            "input": ["input", "скобк"],
            "int": ["int", "строк", "числ"],
            "арифмет": ["кавычк", "оператор"],
            "сравнен": ["=", "=="],
            "if": ["двоеточи", "отступ", "if"],
            "elif": ["elif", "if"],
            "for": ["for", "двоеточи", "отступ", "range"],
            "while": ["while", "бесконечн", "отступ"],
        }
        for topic_word, error_kws in topic_related_errors.items():
            if topic_word in topic:
                if not any(kw in code.lower() for kw in error_kws):
                    issues.append({
                        "id": lesson_id,
                        "title": title,
                        "severity": "info",
                        "block": "find_bug",
                        "issue": "Bug may not clearly relate to the topic's key concept",
                        "detail": f"Topic: '{topic}', Code: {code[:100]}",
                    })
                break

    return issues


def check_quiz(lesson, lesson_id, title):
    """Check the quiz block."""
    issues = []
    quiz = lesson.get("quiz")
    if not quiz:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "quiz",
            "issue": "quiz block is missing",
            "detail": "No quiz found",
        })
        return issues

    question = quiz.get("question", "")
    options = quiz.get("options", [])

    if not question:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "quiz",
            "issue": "Quiz question is empty",
            "detail": "No question text",
        })

    if not options or len(options) < 2:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "quiz",
            "issue": "Quiz has fewer than 2 options",
            "detail": f"Options count: {len(options)}",
        })

    # Check for exactly one correct answer
    correct_count = sum(1 for o in options if o.get("correct", False))
    if correct_count == 0:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "quiz",
            "issue": "No correct answer marked in quiz options",
            "detail": "No option has correct=true",
        })
    elif correct_count > 1:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "quiz",
            "issue": f"Multiple correct answers ({correct_count}) in quiz",
            "detail": "More than one option marked correct",
        })

    # Check for duplicate option text
    option_texts = [o.get("text", "") for o in options]
    if len(option_texts) != len(set(option_texts)):
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "quiz",
            "issue": "Duplicate option texts in quiz",
            "detail": f"Options: {option_texts}",
        })

    # Check plausibility of distractors
    for opt in options:
        text = opt.get("text", "")
        if not text:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "warning",
                "block": "quiz",
                "issue": "Quiz option with empty text",
                "detail": f"Option id: {opt.get('id', '?')}",
            })

    # Check if question relates to topic
    topic = lesson.get("topic", "").lower()
    if topic and question:
        topic_parts = topic.split()
        if not any(tp.lower() in question.lower() for tp in topic_parts if len(tp) > 3):
            pass  # Not always required, skip

    return issues


def check_mission(lesson, lesson_id, title):
    """Check the mission block."""
    issues = []
    mission = lesson.get("mission")
    if not mission:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "mission",
            "issue": "mission block is missing",
            "detail": "No mission found",
        })
        return issues

    expected_output = mission.get("expected_output", "")
    task = mission.get("task", "")
    description = mission.get("description", "")
    mission_title = mission.get("title", "")

    if not expected_output:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "mission",
            "issue": "expected_output is empty",
            "detail": "No expected output defined",
        })

    if not task:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "mission",
            "issue": "Mission task is empty",
            "detail": "No task description",
        })

    # Check if expected_output is a DESCRIPTION rather than actual program output
    description_patterns = [
        r"(?:выведет|напишет|покажет|будет)\s",
        r"(?:результат|значение|число|текст|строк)",
        r"^[а-яА-Яa-zA-Z].*\s+\d",  # "слово число" pattern
        r"\b(?:переменная|функция|команда)\b",
    ]
    for pat in description_patterns:
        if re.search(pat, expected_output, re.IGNORECASE) and len(expected_output) > 60:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "warning",
                "block": "mission",
                "issue": "expected_output looks like a description, not program output",
                "detail": f"expected_output: '{expected_output[:100]}'",
            })
            break

    # Check if mission requires input() (no stdin available in validation)
    if task and "input()" in task:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "mission",
            "issue": "Task requires input() but mission validation has no stdin",
            "detail": f"task: {task[:150]}",
        })

    # Check if expected_output contains Markdown or code formatting (should be raw output)
    if any(marker in expected_output for marker in ["```", "**", "__", "# "]):
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "mission",
            "issue": "expected_output contains Markdown formatting",
            "detail": f"expected_output: '{expected_output[:100]}'",
        })

    # Check if expected_output is very long (unlikely to be a simple output)
    if len(expected_output) > 200:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "warning",
            "block": "mission",
            "issue": f"expected_output is very long ({len(expected_output)} chars)",
            "detail": f"expected_output: '{expected_output[:150]}'",
        })

    # Check that mission has a character assigned
    character = mission.get("character", "")
    if not character:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "info",
            "block": "mission",
            "issue": "Mission has no character assigned",
            "detail": "Missing 'character' field in mission",
        })

    return issues


def check_practice_subtasks(lesson, lesson_id, title):
    """Check the practice_subtasks block."""
    issues = []
    subtasks = lesson.get("practice_subtasks", [])

    if not subtasks:
        # Not all lessons have subtasks, only flag if lesson is harder
        difficulty = lesson.get("difficulty", "")
        if difficulty in ("medium", "hard", "boss"):
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "info",
                "block": "practice_subtasks",
                "issue": "Harder lesson has no practice subtasks",
                "detail": f"Difficulty: {difficulty}",
            })
        return issues

    for i, subtask in enumerate(subtasks):
        sub_title = subtask.get("title", f"subtask_{i}")
        sub_task = subtask.get("task", "")
        sub_expected = subtask.get("expected_output", "")
        sub_hint = subtask.get("hint", "")

        if not sub_task:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "warning",
                "block": f"practice_subtasks[{i}]",
                "issue": f"Subtask '{sub_title}' has no task description",
                "detail": "Missing 'task' field",
            })

        if not sub_expected:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": f"practice_subtasks[{i}]",
                "issue": f"Subtask '{sub_title}' has no expected_output",
                "detail": "Missing 'expected_output' field",
            })

        if not sub_hint:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "info",
                "block": f"practice_subtasks[{i}]",
                "issue": f"Subtask '{sub_title}' has no hint",
                "detail": "Missing 'hint' field",
            })

        # Check if subtask requires input()
        if sub_task and "input()" in sub_task:
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "warning",
                "block": f"practice_subtasks[{i}]",
                "issue": f"Subtask '{sub_title}' requires input() — check validation approach",
                "detail": f"task: {sub_task[:150]}",
            })

        # Check if expected_output is a description not actual output
        if sub_expected and len(sub_expected) > 80 and not any(
            c in sub_expected for c in ["\n", "True", "False", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        ):
            # Long text without numbers or newlines might be a description
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "info",
                "block": f"practice_subtasks[{i}]",
                "issue": f"Subtask '{sub_title}' expected_output may be a description",
                "detail": f"expected_output: '{sub_expected[:100]}'",
            })

    return issues


def check_metadata(lesson, lesson_id, title):
    """Check basic metadata completeness."""
    issues = []

    required_fields = ["part", "chapter", "lesson", "slug", "title", "difficulty", "topic"]
    for field in required_fields:
        if lesson.get(field) is None or lesson.get(field) == "":
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "metadata",
                "issue": f"Required field '{field}' is missing or empty",
                "detail": f"Field: {field}",
            })

    # Check explanation
    explanation = lesson.get("explanation")
    if not explanation:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "error",
            "block": "explanation",
            "issue": "explanation block is missing",
            "detail": "No explanation found",
        })
    else:
        if not explanation.get("text"):
            issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "warning",
                "block": "explanation",
                "issue": "Explanation text is empty",
                "detail": "Missing explanation text",
            })

    # Check game_relevance
    gr = lesson.get("game_relevance", "")
    if not gr:
        issues.append({
            "id": lesson_id,
            "title": title,
            "severity": "info",
            "block": "game_relevance",
            "issue": "game_relevance is missing or empty",
            "detail": "No game_relevance text",
        })

    return issues


def analyze_dialogue_coverage(lessons):
    """Analyze dialogue patterns across all lessons."""
    issues = []

    # Count character usage
    char_counts = {}

    for lesson in lessons:
        lid = lesson["id"]
        title = lesson["title"]
        for block_name in ("pre_topic_dialogue", "post_error_dialogue"):
            dialogue = lesson.get(block_name, [])
            for turn in dialogue:
                char = turn.get("character", "unknown")
                char_counts[char] = char_counts.get(char, 0) + 1

    return issues


# ---------------------------------------------------------------------------
# Main audit function
# ---------------------------------------------------------------------------

def main():
    lessons_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "backend", "app", "data", "lessons.json",
    )

    if not os.path.exists(lessons_path):
        print(f"ERROR: lessons.json not found at {lessons_path}", file=sys.stderr)
        sys.exit(1)

    lessons = load_lessons(lessons_path)
    total = len(lessons)
    print(f"Loaded {total} lessons from {lessons_path}")

    all_issues = []

    for lesson in lessons:
        lesson_id = lesson.get("id", "?")
        title = lesson.get("title", "?")

        try:
            all_issues.extend(check_metadata(lesson, lesson_id, title))
        except Exception as e:
            all_issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "metadata",
                "issue": f"Exception during metadata check: {str(e)[:100]}",
                "detail": "",
            })

        try:
            all_issues.extend(check_dialogues(lesson, lesson_id, title))
        except Exception as e:
            all_issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "dialogues",
                "issue": f"Exception during dialogue check: {str(e)[:100]}",
                "detail": "",
            })

        try:
            all_issues.extend(check_what_outputs(lesson, lesson_id, title))
        except Exception as e:
            all_issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "what_outputs",
                "issue": f"Exception during what_outputs check: {str(e)[:100]}",
                "detail": "",
            })

        try:
            all_issues.extend(check_find_bug(lesson, lesson_id, title))
        except Exception as e:
            all_issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "find_bug",
                "issue": f"Exception during find_bug check: {str(e)[:100]}",
                "detail": "",
            })

        try:
            all_issues.extend(check_quiz(lesson, lesson_id, title))
        except Exception as e:
            all_issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "quiz",
                "issue": f"Exception during quiz check: {str(e)[:100]}",
                "detail": "",
            })

        try:
            all_issues.extend(check_mission(lesson, lesson_id, title))
        except Exception as e:
            all_issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "mission",
                "issue": f"Exception during mission check: {str(e)[:100]}",
                "detail": "",
            })

        try:
            all_issues.extend(check_practice_subtasks(lesson, lesson_id, title))
        except Exception as e:
            all_issues.append({
                "id": lesson_id,
                "title": title,
                "severity": "error",
                "block": "practice_subtasks",
                "issue": f"Exception during practice_subtasks check: {str(e)[:100]}",
                "detail": "",
            })

    # Add cross-lesson analysis issues
    analyze_dialogue_coverage(lessons)

    # Sort issues: errors first, then warnings, then info
    severity_order = {"error": 0, "warning": 1, "info": 2}
    all_issues.sort(key=lambda x: (severity_order.get(x["severity"], 99), x["id"], x["block"]))

    # Count stats
    error_count = sum(1 for i in all_issues if i["severity"] == "error")
    warning_count = sum(1 for i in all_issues if i["severity"] == "warning")
    info_count = sum(1 for i in all_issues if i["severity"] == "info")

    report = {
        "total_lessons": total,
        "total_issues": len(all_issues),
        "errors": error_count,
        "warnings": warning_count,
        "info": info_count,
        "issues": all_issues,
        "summary": {
            "lessons_with_errors": len(set(i["id"] for i in all_issues if i["severity"] == "error")),
            "lessons_with_warnings": len(set(i["id"] for i in all_issues if i["severity"] == "warning")),
            "clean_lessons": total - len(set(i["id"] for i in all_issues)),
        },
    }

    # Write report
    report_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "audit_report.json",
    )
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nReport written to {report_path}")
    print(f"Total lessons: {total}")
    print(f"Total issues: {len(all_issues)}")
    print(f"  Errors:   {error_count}")
    print(f"  Warnings: {warning_count}")
    print(f"  Info:     {info_count}")
    print(f"Lessons with errors: {report['summary']['lessons_with_errors']}")
    print(f"Lessons with warnings: {report['summary']['lessons_with_warnings']}")
    print(f"Clean lessons: {report['summary']['clean_lessons']}")

    return report


if __name__ == "__main__":
    main()
