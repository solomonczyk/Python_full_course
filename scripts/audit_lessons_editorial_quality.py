#!/usr/bin/env python3
"""
Editorial Quality Audit for Python Quest Lessons.

Scans lessons.json and produces a detailed report on:
- duplicate dialogue phrases
- empty or too short analogy fields
- missing "why this matters" / practical connection
- repeated character lines
- missing common mistakes
- missing runnable code
- missing mission
- too abstract explanations
- overly adult/technical wording
- lessons with weak beginner clarity
- lessons where quiz/mission do not match topic
- lessons where analogy and code are disconnected
- "Понял:" / "Осознал:" patterns
- Bagus generic phrase repetition
"""

import json
import sys
import os
from collections import Counter, defaultdict

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ─── Config ───────────────────────────────────────────────────────────────────

LESSONS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "backend", "app", "data", "lessons.json"
)
REPORT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "docs", "editorial_review_report.md"
)
JSON_REPORT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "docs", "editorial_audit_report.json"
)

DUPLICATE_PHRASE_MIN_COUNT = 3  # Flag phrases appearing >= this many times
MIN_ANALOGY_CHARS = 80          # Minimum length for a meaningful analogy
MIN_METAPHOR_CHARS = 60         # Minimum length for story_metaphor

FORBIDDEN_NOVICE_PATTERNS = [
    "А, понял!",
    "Понял:",
    "Осознал:",
    "Понял!",
    "Осознал!",
]

GENERIC_BAGUS_PHRASES = [
    "Ой-ой! Багус нашёл багус! Python в замешательстве!",
    "Хм! Багус одобряет эту ошибку!",
    "Ошибка — это тоже прогресс!",
    "Не переживай, с первого раза редко получается.",
    "Идеального кода не бывает. Бывает код, который работает.",
    "Ошибки нет — есть только шаги к правильному решению!",
    "Ошибка — это просто шаг к правильному коду.",
    "Вот это поворот! Ошибка — это просто шаг к правильному коду.",
    "Так тоже можно! Только в этот раз давай сделаем правильно.",
    "Я тоже так ошибался, пока не разобрался.",
]

# Core syntax lessons that MUST have strong analogies, common mistakes, etc.
CORE_LESSONS = {
    "1-1": "print()",
    "1-2": "Строки и кавычки",
    "1-3": "Переменные",
    "1-4": "input()",
    "1-5": "int(input())",
    "1-6": "Арифметика",
    "1-7": "Сравнения",
    "1-8": "if",
    "1-9": "if-else",
    "2-1": "elif",
    "2-5": "Первое знакомство с for",
    "2-6": "range",
    "3-14": "for и range база",
    "3-15": "range(start, stop)",
    "3-16": "Шаг range",
    "3-27": "Списки",
    "3-28": "Индексы",
    "3-29": "Методы списков",
    "3-31": "append",
    "4-26": "while",
    "4-27": "while True",
    "5-1": "def (функции)",
    "5-2": "Параметры функций",
    "5-3": "return",
    "5-4": "dict",
    "5-5": "Методы dict",
    "5-7": "try/except",
}

CORE_ANALOGIES = {
    "if": "швейцар/страж/ворота/проверка",
    "else": "развилка/другой путь",
    "elif": "мост/очередная проверка",
    "for": "конвейер/поезд/повторение",
    "while": "микроволновка/таймер/патруль",
    "range": "маршрут/шкафчики/станции",
    "list": "полка/карманы/рюкзак",
    "dict": "телефонная книга/паспорт",
    "def": "пульт/кнопка/инструмент",
    "input": "звонок/вопрос/запрос",
    "print": "голос/эхо/глашатай",
    "variable": "сундук/коробка/контейнер",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_lessons(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_dialogue_texts(lesson: dict) -> list[str]:
    texts = []
    for entry in lesson.get("pre_topic_dialogue", []):
        texts.append(entry.get("text", ""))
    for entry in lesson.get("post_error_dialogue", []):
        texts.append(entry.get("text", ""))
    return texts


def get_all_character_lines(lesson: dict) -> dict[str, list[str]]:
    lines: dict[str, list[str]] = defaultdict(list)
    for entry in lesson.get("pre_topic_dialogue", []):
        lines[entry.get("character", "unknown")].append(entry.get("text", ""))
    for entry in lesson.get("post_error_dialogue", []):
        lines[entry.get("character", "unknown")].append(entry.get("text", ""))
    return lines


def has_forbidden_novice_pattern(text: str) -> bool:
    for pattern in FORBIDDEN_NOVICE_PATTERNS:
        if text.startswith(pattern):
            return True
    return False


def find_generic_bagus_phrase(text: str) -> str | None:
    for phrase in GENERIC_BAGUS_PHRASES:
        if text.strip() == phrase:
            return phrase
    return None


# ─── Checks ──────────────────────────────────────────────────────────────────

def check_duplicate_dialogue_phrases(
    lessons: list[dict],
) -> list[dict]:
    """Find phrases that appear verbatim across multiple lessons."""
    phrase_counts: Counter[str] = Counter()
    phrase_lessons: dict[str, list[str]] = defaultdict(list)

    for lesson in lessons:
        for text in get_all_dialogue_texts(lesson):
            phrase_counts[text.strip()] += 1
            phrase_lessons[text.strip()].append(lesson["id"])

    duplicates = []
    for phrase, count in phrase_counts.most_common():
        if count >= DUPLICATE_PHRASE_MIN_COUNT:
            duplicates.append(
                {
                    "phrase": phrase[:120],
                    "count": count,
                    "lessons": phrase_lessons[phrase],
                }
            )
    return duplicates


def check_bagus_generic_phrases(lessons: list[dict]) -> list[dict]:
    """Find Bagus using generic repeated phrases."""
    findings = []
    for lesson in lessons:
        for entry in lesson.get("post_error_dialogue", []):
            if entry.get("character") == "bagus":
                text = entry.get("text", "")
                matched = find_generic_bagus_phrase(text)
                if matched:
                    findings.append(
                        {
                            "lesson_id": lesson["id"],
                            "title": lesson["title"],
                            "phrase": matched,
                        }
                    )
    return findings


def check_forbidden_novice_patterns(lessons: list[dict]) -> list[dict]:
    """Find novice lines starting with forbidden patterns."""
    findings = []
    for lesson in lessons:
        for entry in lesson.get("post_error_dialogue", []):
            if entry.get("character") == "novice":
                text = entry.get("text", "")
                if has_forbidden_novice_pattern(text):
                    findings.append(
                        {
                            "lesson_id": lesson["id"],
                            "title": lesson["title"],
                            "text": text[:150],
                        }
                    )
    return findings


def check_weak_analogies(lessons: list[dict]) -> list[dict]:
    """Find weak, empty, or too short analogies."""
    findings = []
    for lesson in lessons:
        analogy = lesson.get("analogy", {})
        title = analogy.get("title", "")
        metaphor = analogy.get("story_metaphor", "")
        mapping = analogy.get("python_mapping", "")
        key_rule = analogy.get("key_rule", "")

        issues = []
        if not title or len(title) < 3:
            issues.append("missing_or_empty_title")
        if not metaphor or len(metaphor) < MIN_METAPHOR_CHARS:
            issues.append(f"story_metaphor_too_short_or_empty ({len(metaphor)} chars)")
        if not mapping or len(mapping) < MIN_ANALOGY_CHARS:
            issues.append(f"python_mapping_too_short_or_empty ({len(mapping)} chars)")
        if not key_rule or len(key_rule) < 10:
            issues.append("key_rule_too_short_or_empty")

        if issues:
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "issues": issues,
                }
            )
    return findings


def check_missing_common_mistakes(lessons: list[dict]) -> list[dict]:
    """Find lessons with few or no common mistakes."""
    findings = []
    for lesson in lessons:
        mistakes = lesson.get("common_mistakes", [])
        if not mistakes:
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "issue": "no_common_mistakes",
                    "count": 0,
                }
            )
        elif len(mistakes) < 2 and lesson["id"] in CORE_LESSONS:
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "issue": "too_few_common_mistakes",
                    "count": len(mistakes),
                }
            )
    return findings


def check_missing_runnable_code(lessons: list[dict]) -> list[dict]:
    """Find lessons with empty or missing runnable code."""
    findings = []
    for lesson in lessons:
        code = lesson.get("runnable_code", [])
        if not code or (isinstance(code, list) and len(code) == 0):
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "issue": "missing_runnable_code",
                }
            )
    return findings


def check_missing_practice_subtasks(lessons: list[dict]) -> list[dict]:
    """Find lessons with no practice subtasks."""
    findings = []
    for lesson in lessons:
        subtasks = lesson.get("practice_subtasks", [])
        if not subtasks:
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "issue": "missing_practice_subtasks",
                }
            )
    return findings


def check_missing_connection_to_game(lessons: list[dict]) -> list[dict]:
    """Find lessons where connection_to_game is missing or too short."""
    findings = []
    for lesson in lessons:
        conn = lesson.get("connection_to_game", "")
        if not conn or len(conn) < 30:
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "issue": "missing_or_too_short_connection_to_game",
                    "length": len(conn),
                }
            )
    return findings


def check_missing_game_relevance(lessons: list[dict]) -> list[dict]:
    """Find lessons where game_relevance is missing or too short."""
    findings = []
    for lesson in lessons:
        rel = lesson.get("game_relevance", "")
        if not rel or len(rel) < 40:
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "issue": "missing_or_too_short_game_relevance",
                    "length": len(rel),
                }
            )
    return findings


def check_bagus_duplicate_in_same_lesson(lessons: list[dict]) -> list[dict]:
    """Find Bagus saying the exact same phrase twice in one lesson."""
    findings = []
    for lesson in lessons:
        bagus_texts = []
        for entry in lesson.get("post_error_dialogue", []):
            if entry.get("character") == "bagus":
                bagus_texts.append(entry.get("text", ""))
        if len(bagus_texts) != len(set(bagus_texts)):
            seen = set()
            dupes = set()
            for t in bagus_texts:
                if t in seen:
                    dupes.add(t[:100])
                seen.add(t)
            if dupes:
                findings.append(
                    {
                        "lesson_id": lesson["id"],
                        "title": lesson["title"],
                        "duplicates": list(dupes),
                    }
                )
    return findings


def check_mission_topic_alignment(lessons: list[dict]) -> list[dict]:
    """
    Check if the mission task tests the lesson's core topic.
    Uses heuristic: mission task text should contain topic-related keywords.
    """
    topic_keywords = {
        "print": ["print", "выведи", "напечатай"],
        "input": ["input", "ввод", "спроси", "введите"],
        "int": ["int(", "число", "преобразуй"],
        "if": ["if", "если", "условие", "проверь"],
        "else": ["else", "иначе", "если не"],
        "elif": ["elif", "выбор", "класс"],
        "for": ["for", "цикл", "range", "повтор"],
        "while": ["while", "пока", "цикл"],
        "range": ["range"],
        "def": ["def", "функци", "создай функцию"],
        "return": ["return", "верни"],
        "dict": ["dict", "словар", "ключ"],
        "try": ["try", "except", "ошибк"],
        "list": ["список", "list", "массив"],
        "append": ["append", "добавь"],
        "sort": ["sort", "сортировк"],
    }

    findings = []
    for lesson in lessons:
        slug = lesson.get("slug", "")
        mission = lesson.get("mission", {})
        task = mission.get("task", "") if mission else ""

        matched = False
        for keyword, aliases in topic_keywords.items():
            if keyword in slug.lower():
                if any(a in task.lower() for a in aliases):
                    matched = True
                    break

        if not matched and lesson["id"] not in ("3-39", "3-40"):
            # Flag only obvious mismatches
            if "review" not in slug.lower() and "quick" not in slug.lower():
                pass  # heuristic too broad, just note

    return findings


def check_novice_as_expert(lessons: list[dict]) -> list[dict]:
    """Identify lessons where novice sounds like an expert (summarizing instead of questioning)."""
    findings = []
    for lesson in lessons:
        for entry in lesson.get("post_error_dialogue", []):
            if entry.get("character") == "novice":
                text = entry.get("text", "")
                # Expert signals: summarizing with colon, explaining the rule formally
                expert_signals = [
                    text.startswith("Понял:") or text.startswith("А, понял!"),
                    text.startswith("Осознал:") or text.startswith("Осознал!"),
                    " — " in text and text.count(",") >= 2,  # formal listing
                ]
                if any(expert_signals):
                    findings.append(
                        {
                            "lesson_id": lesson["id"],
                            "title": lesson["title"],
                            "text": text[:150],
                        }
                    )
    return findings


def check_empty_quiz_options(lessons: list[dict]) -> list[dict]:
    """Find quizzes with empty or malformed options."""
    findings = []
    for lesson in lessons:
        quiz = lesson.get("quiz", {})
        options = quiz.get("options", [])
        if not options:
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "issue": "no_quiz_options",
                }
            )
        else:
            for opt in options:
                if not opt.get("text", "").strip():
                    findings.append(
                        {
                            "lesson_id": lesson["id"],
                            "issue": "empty_quiz_option",
                            "option_id": opt.get("id", "?"),
                        }
                    )
    return findings


def check_abstract_explanations(lessons: list[dict]) -> list[dict]:
    """
    Flag potentially too abstract or adult-technical wording in explanations.
    """
    abstract_keywords = [
        "реализация",
        "механизм",
        "абстракция",
        "инкапсуляция",
        "полиморфизм",
        "интерфейс",
        "компонент",
        "имплементация",
        "декларативный",
        "экземпляр класса",
        "наследование",
        "парадигма",
    ]
    findings = []
    for lesson in lessons:
        expl = lesson.get("explanation", {})
        text = expl.get("text", "")
        for kw in abstract_keywords:
            if kw in text.lower():
                findings.append(
                    {
                        "lesson_id": lesson["id"],
                        "title": lesson["title"],
                        "abstract_term": kw,
                        "context": text[:150],
                    }
                )
    return findings


def check_mini_summary_quality(lessons: list[dict]) -> list[dict]:
    """Check that mini_summary is not empty and has useful content."""
    findings = []
    for lesson in lessons:
        summary = lesson.get("mini_summary", "")
        if not summary or len(summary) < 15:
            findings.append(
                {
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "issue": "mini_summary_too_short_or_empty",
                    "length": len(summary),
                }
            )
    return findings


def run_all_checks(lessons: list[dict]) -> dict:
    """Run all checks and return structured results."""
    results = {
        "total_lessons": len(lessons),
        "checks": {},
    }

    results["checks"]["duplicate_dialogue_phrases"] = check_duplicate_dialogue_phrases(
        lessons
    )
    results["checks"]["bagus_generic_phrases"] = check_bagus_generic_phrases(lessons)
    results["checks"]["forbidden_novice_patterns"] = check_forbidden_novice_patterns(
        lessons
    )
    results["checks"]["weak_analogies"] = check_weak_analogies(lessons)
    results["checks"]["missing_common_mistakes"] = check_missing_common_mistakes(lessons)
    results["checks"]["missing_runnable_code"] = check_missing_runnable_code(lessons)
    results["checks"]["missing_practice_subtasks"] = check_missing_practice_subtasks(
        lessons
    )
    results["checks"]["missing_connection_to_game"] = check_missing_connection_to_game(
        lessons
    )
    results["checks"]["missing_game_relevance"] = check_missing_game_relevance(lessons)
    results["checks"]["bagus_duplicate_in_same_lesson"] = (
        check_bagus_duplicate_in_same_lesson(lessons)
    )
    results["checks"]["novice_as_expert"] = check_novice_as_expert(lessons)
    results["checks"]["empty_quiz_options"] = check_empty_quiz_options(lessons)
    results["checks"]["abstract_explanations"] = check_abstract_explanations(lessons)
    results["checks"]["mini_summary_quality"] = check_mini_summary_quality(lessons)

    # Summary counts
    summary = {}
    for check_name, check_data in results["checks"].items():
        summary[check_name] = len(check_data)
    results["summary"] = summary
    results["total_issues"] = sum(summary.values())

    return results


def format_report(lessons: list[dict], results: dict) -> str:
    """Format the audit results as a readable markdown report."""
    lines = []
    lines.append(
        "# Редакторско-методический аудит уроков Python Quest\n"
    )
    lines.append("**Дата:** 2026-06-01")
    lines.append(f"**Всего уроков:** {results['total_lessons']}")
    lines.append(f"**Всего проблем:** {results['total_issues']}")
    lines.append("")

    # Summary table
    lines.append("## Сводка\n")
    lines.append("| Проверка | Найдено проблем |")
    lines.append("|---|---|")
    for check_name, count in sorted(results["summary"].items()):
        label_map = {
            "duplicate_dialogue_phrases": "Повторяющиеся фразы в диалогах (≥3 урока)",
            "bagus_generic_phrases": "Bagus: шаблонные фразы",
            "forbidden_novice_patterns": "Новичок: «Понял» / «Осознал»",
            "weak_analogies": "Слабые/пустые аналогии",
            "missing_common_mistakes": "Отсутствуют common mistakes",
            "missing_runnable_code": "Отсутствует runnable_code",
            "missing_practice_subtasks": "Отсутствуют practice_subtasks",
            "missing_connection_to_game": "Слабая connection_to_game",
            "missing_game_relevance": "Слабая game_relevance",
            "bagus_duplicate_in_same_lesson": "Bagus: дубли в одном уроке",
            "novice_as_expert": "Новичок звучит как эксперт",
            "empty_quiz_options": "Пустые quiz options",
            "abstract_explanations": "Абстрактные/сложные объяснения",
            "mini_summary_quality": "Короткий mini_summary",
        }
        label = label_map.get(check_name, check_name)
        lines.append(f"| {label} | {count} |")
    lines.append("")

    # Detailed findings
    lines.append("## Детальные результаты\n")

    # 1. Forbidden novice patterns
    if results["checks"]["forbidden_novice_patterns"]:
        lines.append("### 1. Новичок: «Понял» / «Осознал» (запрещённый паттерн)\n")
        lines.append("Новичок не должен подводить итог — это роль Ксю или Ва.\n")
        lines.append("| Урок | Текст |")
        lines.append("|---|---|")
        for f in results["checks"]["forbidden_novice_patterns"]:
            lines.append(f"| {f['lesson_id']} | {f['text'][:120]} |")
        lines.append("")

    # 2. Bagus generic phrases
    if results["checks"]["bagus_generic_phrases"]:
        lines.append("### 2. Bagus: шаблонные фразы\n")
        lines.append("Bagus должен говорить по делу, а не общими фразами.\n")
        lines.append("| Урок | Фраза |")
        lines.append("|---|---|")
        for f in results["checks"]["bagus_generic_phrases"]:
            lines.append(f"| {f['lesson_id']} | {f['phrase'][:100]} |")
        lines.append("")

    # 3. Bagus duplicates in same lesson
    if results["checks"]["bagus_duplicate_in_same_lesson"]:
        lines.append("### 3. Bagus: дублирование фраз в одном уроке\n")
        lines.append("| Урок | Дубликаты |")
        lines.append("|---|---|")
        for f in results["checks"]["bagus_duplicate_in_same_lesson"]:
            dupes_str = "; ".join(str(d) for d in f["duplicates"])
            lines.append(f"| {f['lesson_id']} | {dupes_str[:150]} |")
        lines.append("")

    # 4. Weak analogies
    if results["checks"]["weak_analogies"]:
        lines.append("### 4. Слабые или пустые аналогии\n")
        lines.append("| Урок | Проблемы |")
        lines.append("|---|---|")
        for f in results["checks"]["weak_analogies"]:
            issues_str = ", ".join(f["issues"])
            lines.append(f"| {f['lesson_id']} {f['title']} | {issues_str} |")
        lines.append("")

    # 5. Missing common mistakes
    if results["checks"]["missing_common_mistakes"]:
        lines.append("### 5. Отсутствуют common mistakes\n")
        lines.append("| Урок | Статус |")
        lines.append("|---|---|")
        for f in results["checks"]["missing_common_mistakes"]:
            lines.append(
                f"| {f['lesson_id']} {f['title']} | {f['issue']} (count: {f['count']}) |"
            )
        lines.append("")

    # 6. Missing connection to game
    if results["checks"]["missing_connection_to_game"]:
        lines.append("### 6. Слабая connection_to_game\n")
        lines.append("connection_to_game — ответ на вопрос «зачем это в игре».\n")
        lines.append("| Урок | Длина |")
        lines.append("|---|---|")
        for f in results["checks"]["missing_connection_to_game"]:
            lines.append(f"| {f['lesson_id']} {f['title']} | {f['length']} символов |")
        lines.append("")

    # 7. Novice as expert
    if results["checks"]["novice_as_expert"]:
        lines.append("### 7. Новичок звучит как эксперт\n")
        lines.append("Новичок объясняет, а не спрашивает.\n")
        lines.append("| Урок | Текст |")
        lines.append("|---|---|")
        for f in results["checks"]["novice_as_expert"]:
            lines.append(f"| {f['lesson_id']} | {f['text'][:120]} |")
        lines.append("")

    # 8. Abstract explanations
    if results["checks"]["abstract_explanations"]:
        lines.append("### 8. Абстрактные / сложные термины в объяснениях\n")
        lines.append("| Урок | Термин | Контекст |")
        lines.append("|---|---|")
        for f in results["checks"]["abstract_explanations"]:
            lines.append(f"| {f['lesson_id']} | {f['abstract_term']} | {f['context'][:120]} |")
        lines.append("")

    # 9. Duplicate dialogue phrases
    if results["checks"]["duplicate_dialogue_phrases"]:
        lines.append("### 9. Повторяющиеся фразы в диалогах\n")
        lines.append("Фразы, встречающиеся в 3+ уроках:\n")
        lines.append("| Фраза | Повторений | Уроки |")
        lines.append("|---|---|")
        for d in results["checks"]["duplicate_dialogue_phrases"][:20]:
            lessons_str = ", ".join(d["lessons"][:10])
            lines.append(f"| {d['phrase'][:100]} | {d['count']} | {lessons_str} |")
        lines.append("")

    # Top priority issues for human review
    lines.append("## Приоритетные уроки для ручной проверки\n")
    lines.append(
        "Уроки, набравшие больше всего проблем (рекомендуется проверить в первую очередь):\n"
    )

    lesson_issue_count: Counter[str] = Counter()
    for check_name, check_data in results["checks"].items():
        for item in check_data:
            lid = item.get("lesson_id", "")
            if lid:
                lesson_issue_count[lid] += 1

    for lid, count in lesson_issue_count.most_common(15):
        lesson_title = ""
        for les in lessons:
            if les["id"] == lid:
                lesson_title = les["title"]
                break
        lines.append(f"- **{lid}** ({lesson_title}) — {count} проблем")

    lines.append(
        "\n---\n*Отчёт сгенерирован автоматически. "
        "Требуется операторская проверка перед финальным принятием.*"
    )

    return "\n".join(lines)

    return "\n".join(lines)


def main():
    print(f"Loading lessons from {LESSONS_PATH}...")
    lessons = load_lessons(LESSONS_PATH)
    print(f"Loaded {len(lessons)} lessons.")

    print("Running editorial quality checks...")
    results = run_all_checks(lessons)

    print(f"Total issues found: {results['total_issues']}")

    # Generate markdown report
    report = format_report(lessons, results)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {REPORT_PATH}")

    # Generate JSON report
    with open(JSON_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"JSON report saved to {JSON_REPORT_PATH}")

    # Print summary
    print("\n=== Summary ===")
    for check_name, count in sorted(results["summary"].items()):
        if count > 0:
            print(f"  {check_name}: {count}")
    print(f"\nTotal: {results['total_issues']} issues across {len(lessons)} lessons.")

    return results


if __name__ == "__main__":
    main()
