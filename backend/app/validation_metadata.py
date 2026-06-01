"""Validation metadata for Python Quest lessons.

Maps lesson IDs to their required constructs, forbidden patterns, and
optional test cases for output validation.

This module is the single source of truth for what each lesson's mission
expects from the student beyond raw output matching.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LessonValidation:
    """Validation rules for a single lesson's mission."""

    lesson_id: str
    title: str = ""

    # Constructs the student's code MUST contain to be considered structurally
    # correct (e.g. ``["variable", "print"]``).
    required_constructs: list[str] = field(default_factory=list)

    # If True, a student who simply prints the expected literal string
    # without using the required constructs will get a hardcode hint.
    reject_hardcoded: bool = True

    # Extra string patterns that should raise an error.
    forbidden_patterns: list[str] = field(default_factory=list)

    # Test cases for output validation: each dict has "input" (stdin) and/or
    # "expected_output".  When empty, only the top-level expected_output is
    # compared.
    test_cases: list[dict[str, str]] = field(default_factory=list)

    # Whether to skip subprocess execution even in non-public mode.
    # AST-only check still runs.
    ast_only: bool = False


# NOTE: Lessons NOT listed here default to requiring only ``["print"]``
# and reject_hardcoded=False (i.e. just print the right thing).

_VALIDATION: dict[str, LessonValidation] = {
    # ── Part 1 — Basics ──────────────────────────────────────────────────
    "1-1": LessonValidation(
        "1-1",
        title="print()",
        required_constructs=["print"],
        reject_hardcoded=False,
    ),
    "1-2": LessonValidation(
        "1-2",
        title="Строки и кавычки",
        required_constructs=["variable", "print"],
        test_cases=[{"input": "Багус", "expected_output": "Багус"}],
    ),
    "1-3": LessonValidation(
        "1-3",
        title="Переменные",
        required_constructs=["variable", "print"],
    ),
    "1-4": LessonValidation(
        "1-4",
        title="input()",
        required_constructs=["input", "print"],
        test_cases=[{"input": "Андрей", "expected_output": "Андрей"}],
    ),
    "1-5": LessonValidation(
        "1-5",
        title="int(input())",
        required_constructs=["input", "int_call", "print"],
        test_cases=[{"input": "8", "expected_output": "9"}],
    ),
    "1-6": LessonValidation(
        "1-6",
        title="Арифметика",
        required_constructs=["print"],
        reject_hardcoded=False,
    ),
    "1-7": LessonValidation(
        "1-7",
        title="Сравнения",
        required_constructs=["print"],
        reject_hardcoded=False,
    ),
    "1-8": LessonValidation(
        "1-8",
        title="if",
        required_constructs=["if", "print"],
    ),
    "1-9": LessonValidation(
        "1-9",
        title="if else",
        required_constructs=["input", "int_call", "if", "else", "modulo", "print"],
        test_cases=[
            {"input": "7", "expected_output": "odd"},
            {"input": "4", "expected_output": "even"},
        ],
    ),
    # ── Part 2 — Conditions & Random ─────────────────────────────────────
    "2-1": LessonValidation(
        "2-1",
        title="elif",
        required_constructs=["if", "elif", "print"],
    ),
    "2-2": LessonValidation(
        "2-2",
        title="Логические цепочки",
        required_constructs=["if", "elif", "else", "print"],
    ),
    "2-3": LessonValidation(
        "2-3",
        title="random.randint",
        required_constructs=["random_import", "variable", "print"],
        # Random output — only check construct, not output
        ast_only=True,
    ),
    "2-4": LessonValidation(
        "2-4",
        title="Простая игра с random",
        required_constructs=["random_import", "variable", "print"],
        ast_only=True,
    ),
    "2-5": LessonValidation(
        "2-5",
        title="Первое знакомство с for",
        required_constructs=["for", "range", "print"],
    ),
    "2-6": LessonValidation(
        "2-6",
        title="range",
        required_constructs=["range", "print"],
    ),
    # ── Part 3 — Types, Conditions, Loops ────────────────────────────────
    "3-1": LessonValidation(
        "3-1",
        title="Float и типы данных",
        required_constructs=["print"],
        reject_hardcoded=False,
    ),
    "3-2": LessonValidation(
        "3-2",
        title="Обычное деление /",
        required_constructs=["print"],
        reject_hardcoded=False,
    ),
    "3-3": LessonValidation(
        "3-3",
        title="Целочисленное деление //",
        required_constructs=["print"],
        reject_hardcoded=False,
    ),
    "3-4": LessonValidation(
        "3-4",
        title="Остаток от деления %",
        required_constructs=["modulo", "print"],
    ),
    "3-5": LessonValidation(
        "3-5",
        title="Определение на чётность",
        required_constructs=["input", "int_call", "if", "else", "modulo", "print"],
        test_cases=[
            {"input": "8", "expected_output": "yes"},
            {"input": "7", "expected_output": "no"},
        ],
    ),
    "3-6": LessonValidation(
        "3-6",
        title="Bool",
        required_constructs=["variable", "print"],
    ),
    "3-7": LessonValidation(
        "3-7",
        title="Состояния объектов",
        required_constructs=["variable", "if", "print"],
    ),
    "3-8": LessonValidation(
        "3-8",
        title="Короткая запись условий",
        required_constructs=["if", "print"],
    ),
    # Input-based conditions — test cases with multi-line input
    "3-9": LessonValidation(
        "3-9",
        title="and",
        required_constructs=["input", "int_call", "if", "print"],
        test_cases=[
            {"input": "17\nнет", "expected_output": "locked"},
        ],
    ),
    "3-10": LessonValidation(
        "3-10",
        title="or",
        required_constructs=["input", "if", "print"],
        test_cases=[
            {"input": "сб", "expected_output": "weekend"},
        ],
    ),
    "3-11": LessonValidation(
        "3-11",
        title="not",
        required_constructs=["input", "if", "print"],
        test_cases=[
            {"input": "дом", "expected_output": "no a"},
        ],
    ),
    "3-12": LessonValidation(
        "3-12",
        title="Оптимизация if",
        required_constructs=["input", "if", "print"],
        test_cases=[
            {"input": "Анна\n123", "expected_output": "accepted"},
        ],
    ),
    "3-13": LessonValidation(
        "3-13",
        title="Вложенные if",
        required_constructs=["input", "if", "print"],
        test_cases=[
            {"input": "1234\n999", "expected_output": "ok"},
        ],
    ),
    "3-14": LessonValidation(
        "3-14",
        title="For и range база",
        required_constructs=["for", "range", "print"],
    ),
    "3-15": LessonValidation(
        "3-15",
        title="Диапазон range(start, stop)",
        required_constructs=["range", "print"],
    ),
    "3-16": LessonValidation(
        "3-16",
        title="Шаг range",
        required_constructs=["range", "print"],
    ),
    "3-17": LessonValidation(
        "3-17",
        title="Обратный ход",
        required_constructs=["range", "print"],
    ),
    "3-18": LessonValidation(
        "3-18",
        title="Переменные в циклах",
        required_constructs=["for", "range", "variable", "print"],
    ),
    "3-22": LessonValidation(
        "3-22",
        title="F-строка",
        required_constructs=["variable", "print"],
    ),
    "3-24": LessonValidation(
        "3-24",
        title="Индексы",
        required_constructs=["print"],
        reject_hardcoded=False,
    ),
    "3-26": LessonValidation(
        "3-26",
        title="Перебор строки",
        required_constructs=["for", "print"],
    ),
    "3-27": LessonValidation(
        "3-27",
        title="Списки база",
        required_constructs=["list", "print"],
    ),
    # ── Part 4 — Advanced topics ─────────────────────────────────────────
    "4-1": LessonValidation(
        "4-1",
        title="Флаги",
        required_constructs=["for", "if", "variable", "print"],
    ),
    "4-2": LessonValidation(
        "4-2",
        title="break",
        required_constructs=["for", "break", "print"],
    ),
    "4-14": LessonValidation(
        "4-14",
        title="map",
        required_constructs=["map", "sum_call", "print"],
    ),
    "4-26": LessonValidation(
        "4-26",
        title="while",
        required_constructs=["while", "print"],
    ),
    "4-28": LessonValidation(
        "4-28",
        title="До правильного ввода",
        required_constructs=["while", "input", "if", "print"],
        test_cases=[
            {"input": "нет\nнет\nда", "expected_output": "accepted"},
        ],
    ),
    "4-31": LessonValidation(
        "4-31",
        title="random + while игра",
        required_constructs=["random_import", "while", "input", "int_call", "if", "print"],
        # Random game — construct check only
        ast_only=True,
    ),
    # ── Part 5 — Functions ───────────────────────────────────────────────
    "5-1": LessonValidation(
        "5-1",
        title="Кнопка на пульте",
        required_constructs=["function_def", "print"],
    ),
    "5-2": LessonValidation(
        "5-2",
        title="Кофемашина с настройками",
        required_constructs=["function_def", "print"],
    ),
    "5-3": LessonValidation(
        "5-3",
        title="Завод с конвейером",
        required_constructs=["function_def", "return", "print"],
    ),
    "5-7": LessonValidation(
        "5-7",
        title="Страховка альпиниста",
        required_constructs=["input", "int_call", "if", "print"],
        test_cases=[
            {"input": "abc", "expected_output": "Не число"},
        ],
    ),
}


def get_validation(lesson_id: str) -> LessonValidation | None:
    """Return the validation rules for *lesson_id*, or ``None`` if not found."""
    return _VALIDATION.get(lesson_id)


def get_or_default(lesson_id: str, lesson: dict | None = None) -> LessonValidation:
    """Return validation rules, or a sensible default.

    The default requires ``["print"]`` and does not reject hardcoded output.
    """
    v = _VALIDATION.get(lesson_id)
    if v is not None:
        return v

    # Auto-detect based on lesson metadata (if provided)
    if lesson:
        mission = lesson.get("mission", {}) or {}
        task = (mission.get("task", "") or "").lower()

        constructs: list[str] = ["print"]
        needs_input = any(kw in task for kw in ["input()", "считай", "ввод"])
        needs_int = any(
            kw in task for kw in ["int(input())", "преобразуй"]
        )
        needs_if = any(
            kw in task for kw in ["если", "if", "проверь", "условие"]
        )
        needs_else = any(
            kw in task for kw in ["иначе", "else", "нечётное", "нечёт"]
        )
        needs_for = any(
            kw in task for kw in ["for", "цикл", "range"]
        )
        needs_while = "while" in task
        needs_variable = any(
            kw in task for kw in ["переменн", "сохран"]
        )

        if needs_input:
            constructs.append("input")
        if needs_int:
            constructs.append("int_call")
        if needs_if:
            constructs.append("if")
        if needs_else:
            constructs.append("else")
        if needs_for:
            constructs.append("for")
            constructs.append("range")
        if needs_while:
            constructs.append("while")
        if needs_variable:
            constructs.append("variable")

        return LessonValidation(
            lesson_id=lesson_id,
            title=lesson.get("title", ""),
            required_constructs=constructs,
            reject_hardcoded=bool(needs_input or needs_if or needs_variable),
        )

    return LessonValidation(
        lesson_id=lesson_id,
        required_constructs=["print"],
        reject_hardcoded=False,
    )


def all_validated_lesson_ids() -> list[str]:
    """Return a sorted list of lesson IDs that have explicit validation rules."""
    return sorted(_VALIDATION.keys())


def list_validation_metadata() -> list[dict[str, Any]]:
    """Return a human-readable summary of all validation rules."""
    out: list[dict[str, Any]] = []
    for vid in sorted(_VALIDATION.keys()):
        v = _VALIDATION[vid]
        out.append({
            "lesson_id": v.lesson_id,
            "title": v.title,
            "required_constructs": v.required_constructs,
            "reject_hardcoded": v.reject_hardcoded,
            "test_case_count": len(v.test_cases),
            "ast_only": v.ast_only,
        })
    return out
