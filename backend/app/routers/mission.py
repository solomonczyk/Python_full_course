"""Mission check endpoint — validates student Python code.

Uses AST‐based static analysis as the primary checker, with safe subprocess
execution as a fallback for output validation in non‑public environments.

Architecture:
1. Parse & analyse code with :mod:`app.ast_checker` (no execution).
2. Check for forbidden imports.
3. Validate required constructs and detect hardcoded output.
4. If all structural checks pass, optionally run code in a subprocess for
   output validation (skipped in ``PUBLIC_MODE``).
5. Return a rich response with ``output_correct``, ``structure_correct``,
   ``safety_passed``, ``finally_correct``.
"""

import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any

from app.ast_checker import (
    AnalysisResult,
    analyze_code,
    check_required_constructs,
    make_validation_hints,
    run_code_safely,
)
from app.validation_metadata import get_or_default

router = APIRouter(prefix="/mission", tags=["mission"])

def _is_public_mode() -> bool:
    """Return True when PUBLIC_MODE is set, skipping subprocess execution."""
    return os.environ.get("PUBLIC_MODE", "").lower() in ("1", "true", "yes")

# ── Request / Response models ───────────────────────────────────────────────


class MissionSubmit(BaseModel):
    lesson_id: str
    code: str


# ── Endpoint ────────────────────────────────────────────────────────────────


@router.post("/check")
def check_mission(body: MissionSubmit) -> dict[str, Any]:
    """Check student code for a mission.

    Returns a dict with keys:
      - ``correct`` (legacy, backward-compatible — ``True`` only when all pass)
      - ``output_correct``
      - ``structure_correct``
      - ``safety_passed``
      - ``finally_correct`` (same as ``correct``)
      - ``actual_output``
      - ``expected_output``
      - ``error`` (first error message, or ``None``)
      - ``hints`` (list of human-readable hint strings)
      - ``details`` (constructs found, missing constructs, etc.)
    """
    # 1. Load lesson
    from app.routers.lessons import _load_lessons

    lessons = _load_lessons()
    lesson = next((x for x in lessons if x["id"] == body.lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    mission = lesson.get("mission")
    if not mission:
        raise HTTPException(status_code=400, detail="No mission in this lesson")

    expected = mission["expected_output"].strip()

    # 2. Get validation rules
    val = get_or_default(body.lesson_id, lesson)

    # 3. AST analysis
    analysis: AnalysisResult = analyze_code(body.code)

    # 4. Build response
    hints: list[str] = []
    errors: list[str] = list(analysis.errors)

    # Safety checks
    safety_passed = True
    if analysis.has_forbidden_import:
        safety_passed = False
        err_msg = (
            f"⛔ Использование модуля '{analysis.forbidden_import_name}' запрещено"
        )
        errors.append(err_msg)
        hints.append(err_msg)
    elif analysis.has_dangerous_patterns:
        safety_passed = False
        err_msg = "⛔ Код содержит запрещённые операции"
        errors.append(err_msg)
        hints.append(err_msg)
    elif not analysis.is_syntactically_valid:
        safety_passed = False
        err_msg = f"❗ Синтаксическая ошибка: {analysis.syntax_error_detail}"
        errors.append(err_msg)
        hints.append(err_msg)

    # Structure checks (only if safety passed)
    structure_correct = False
    if safety_passed:
        passed, _ = check_required_constructs(
            analysis.constructs, val.required_constructs,
        )
        structure_correct = passed
        # Add hints from AST analysis
        ast_hints = make_validation_hints(
            analysis, val.required_constructs, expected,
        )
        hints.extend(ast_hints)
        for h in ast_hints:
            # Only safety (⛔) and syntax (❗) hints are real errors
            if h.startswith("⛔") or h.startswith("❗"):
                if h not in errors:
                    errors.append(h)

    # Output check (only if structure is correct and we can safely run)
    output_correct: bool | None = None
    actual_output: str | None = None

    if safety_passed and structure_correct:
        if val.ast_only:
            # Random / non-deterministic missions — skip output check,
            # trust structural correctness
            output_correct = True
        elif _is_public_mode():
            # Public mode: no subprocess. Try static output extraction.
            # If all print() args are constants, we can compare.
            if analysis.hardcoded_outputs and not analysis.print_has_variable:
                combined = "\n".join(analysis.hardcoded_outputs)
                output_correct = combined.strip() == expected
                actual_output = combined
            elif not analysis.hardcoded_outputs and analysis.constructs:
                # Code uses variables but we can't execute — mark as
                # unknown (structurally correct at least)
                output_correct = None
                actual_output = None
                hints.append(
                    "ℹ️  Код структурно верен. Запусти локально для проверки вывода."
                )
            else:
                output_correct = None
                actual_output = None
        else:
            # Non-public mode: safe subprocess execution
            test_cases = val.test_cases if val.test_cases else None
            passed, out, err = run_code_safely(
                body.code, expected, test_cases=test_cases,
            )
            output_correct = passed
            actual_output = out
            if err:
                errors.append(err)
                if err not in hints:
                    hints.append(err)

    # Legacy 'correct' field (backward-compatible)
    finally_correct = bool(
        safety_passed
        and structure_correct
        and (output_correct is True or (output_correct is None and val.ast_only))
    )

    # Determine the primary error message (frontend uses this)
    first_error = next((e for e in errors if e), None)

    # Construct details for debugging / frontend display
    details: dict[str, Any] = {
        "constructs_found": sorted(analysis.constructs) if analysis.is_syntactically_valid else [],
        "required_constructs": val.required_constructs,
    }
    if analysis.is_syntactically_valid and safety_passed:
        missing = [
            c for c in val.required_constructs if c not in analysis.constructs
        ]
        if missing:
            details["missing_constructs"] = missing

    resp: dict[str, Any] = {
        # Legacy fields (backward-compatible)
        "correct": finally_correct,
        "actual_output": actual_output,
        "expected_output": expected,
        "error": first_error,
        # New v2 fields
        "output_correct": output_correct,
        "structure_correct": structure_correct,
        "safety_passed": safety_passed,
        "finally_correct": finally_correct,
        "hints": hints,
        "details": details,
    }

    return resp
