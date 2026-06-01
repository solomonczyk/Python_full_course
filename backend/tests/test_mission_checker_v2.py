"""Tests for the mission checker v2 — AST static analysis.

Tests cover:
- Correct solutions pass all checks
- Hardcoded print is rejected when a construct is required
- Forbidden imports are rejected
- Missing constructs are detected
- Infinite loop risk detection
- Backward-compatible response shape
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ast_checker import (
    analyze_code,
    check_required_constructs,
    check_hardcoded_output,
    make_validation_hints,
)

# ── AST analysis tests ──────────────────────────────────────────────────────


class TestAnalyzeCode:
    """Unit tests for the core ``analyze_code`` function."""

    def test_empty_code(self):
        r = analyze_code("")
        assert r.is_syntactically_valid
        assert r.constructs == set()

    def test_print_literal(self):
        r = analyze_code('print("Привет")')
        assert "print" in r.constructs
        assert "Привет" in r.hardcoded_outputs
        assert not r.print_has_variable

    def test_variable_assignment(self):
        r = analyze_code("x = 10\nprint(x)")
        assert "variable" in r.constructs
        assert "print" in r.constructs
        assert r.print_has_variable  # x is a variable, not literal
        assert r.hardcoded_outputs == []  # no string literal in print

    def test_augmented_assignment(self):
        r = analyze_code("x = 5\nx += 3\nprint(x)")
        assert "variable" in r.constructs

    def test_input_detection(self):
        r = analyze_code('name = input("Name: ")\nprint(name)')
        assert "input" in r.constructs
        assert "variable" in r.constructs
        assert "print" in r.constructs

    def test_int_call(self):
        r = analyze_code('n = int(input())\nprint(n)')
        assert "int_call" in r.constructs
        assert "input" in r.constructs
        assert "variable" in r.constructs

    def test_float_call(self):
        r = analyze_code('f = float("3.14")\nprint(f)')
        assert "float_call" in r.constructs

    def test_if_statement(self):
        r = analyze_code("x = 10\nif x > 0:\n    print('ok')")
        assert "if" in r.constructs
        assert "variable" in r.constructs
        assert "print" in r.constructs
        assert "else" not in r.constructs

    def test_if_else(self):
        r = analyze_code("if x > 0:\n    print('pos')\nelse:\n    print('neg')")
        assert "if" in r.constructs
        assert "else" in r.constructs

    def test_if_elif(self):
        r = analyze_code(
            "if x > 0:\n    print('pos')\nelif x < 0:\n    print('neg')"
        )
        assert "if" in r.constructs
        assert "elif" in r.constructs

    def test_for_loop(self):
        r = analyze_code("for i in range(5):\n    print(i)")
        assert "for" in r.constructs
        assert "range" in r.constructs
        assert "print" in r.constructs

    def test_while_loop(self):
        r = analyze_code("i = 0\nwhile i < 3:\n    print(i)\n    i += 1")
        assert "while" in r.constructs
        assert "variable" in r.constructs

    def test_infinite_while_detection(self):
        r = analyze_code("while True:\n    print('forever')")
        assert r.has_infinite_loop_risk
        assert "while" in r.constructs

    def test_function_def(self):
        r = analyze_code("def greet():\n    print('hello')\ngreet()")
        assert "function_def" in r.constructs
        assert "print" in r.constructs

    def test_return_detection(self):
        r = analyze_code("def add(a, b):\n    return a + b\nprint(add(1, 2))")
        assert "function_def" in r.constructs
        assert "return" in r.constructs

    def test_list_detection(self):
        r = analyze_code("items = [1, 2, 3]\nprint(items)")
        assert "list" in r.constructs
        assert "variable" in r.constructs

    def test_dict_detection(self):
        r = analyze_code("d = {'a': 1}\nprint(d)")
        assert "dict" in r.constructs

    def test_modulo_detection(self):
        r = analyze_code("print(10 % 3)")
        assert "modulo" in r.constructs
        assert "print" in r.constructs

    def test_syntax_error(self):
        r = analyze_code("print('hello")
        assert not r.is_syntactically_valid
        assert r.syntax_error_detail is not None
        assert len(r.errors) > 0

    def test_forbidden_import(self):
        r = analyze_code("import os\nprint('test')")
        assert r.has_forbidden_import
        assert r.has_dangerous_patterns
        assert r.forbidden_import_name == "os"

        r2 = analyze_code("import subprocess\nprint('test')")
        assert r2.has_forbidden_import
        assert r2.forbidden_import_name == "subprocess"

        r3 = analyze_code("import requests\nprint('test')")
        assert r3.has_forbidden_import
        assert r3.forbidden_import_name == "requests"

    def test_dangerous_call(self):
        r = analyze_code("exec('print(1)')")
        assert r.has_dangerous_patterns

        r2 = analyze_code("eval('1+1')")
        assert r2.has_dangerous_patterns

    def test_random_import(self):
        r = analyze_code("import random\nprint(random.randint(1, 6))")
        assert "random_import" in r.constructs
        assert not r.has_forbidden_import
        assert "print" in r.constructs

    def test_print_with_variable_and_literal(self):
        r = analyze_code("x = 10\nprint('Result:', x)")
        assert r.print_has_variable  # x is not literal
        assert "Result:" in r.hardcoded_outputs

    def test_forbidden_import_from(self):
        r = analyze_code("from os import system\nsystem('ls')")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "os"


# ── Required constructs checking ────────────────────────────────────────────


class TestCheckRequiredConstructs:
    def test_all_present(self):
        passed, hint = check_required_constructs(
            {"print", "variable", "input"}, ["print", "variable", "input"]
        )
        assert passed
        assert hint is None

    def test_missing_variable(self):
        passed, hint = check_required_constructs(
            {"print", "input"}, ["print", "input", "variable"]
        )
        assert not passed
        assert hint == "missing_variable"

    def test_missing_input(self):
        passed, hint = check_required_constructs(
            {"print", "variable"}, ["print", "variable", "input"]
        )
        assert not passed
        assert hint == "missing_input"

    def test_missing_if(self):
        passed, hint = check_required_constructs(
            {"print"}, ["if", "print"]
        )
        assert not passed
        assert hint == "expected_if"

    def test_no_requirements(self):
        passed, hint = check_required_constructs({"print"}, None)
        assert passed
        assert hint is None

    def test_empty_list(self):
        passed, hint = check_required_constructs({"print"}, [])
        assert passed
        assert hint is None


# ── Hardcoded output detection ──────────────────────────────────────────────


class TestCheckHardcodedOutput:
    def test_hardcoded_string_literal(self):
        """print('10') when variable is required should be flagged."""
        r = analyze_code("print('10')")
        assert check_hardcoded_output(r, "10", ["variable"]), \
            "Should detect hardcoded output when variable is required"

    def test_variable_not_hardcoded(self):
        """print(x) with x = 10 should NOT be flagged."""
        r = analyze_code("x = 10\nprint(x)")
        assert not check_hardcoded_output(r, "10", ["variable"]), \
            "Code using variables should not be hardcoded"

    def test_print_literal_but_has_construct(self):
        """print('ok') with if should NOT be flagged if if is present."""
        r = analyze_code("x = 10\nif x > 0:\n    print('ok')")
        assert not check_hardcoded_output(r, "ok", ["if", "print"]), \
            "Hardcode check should not flag when required construct is present"

    def test_no_required_constructs(self):
        """When no constructs required, literal print is fine."""
        r = analyze_code("print('Hello')")
        assert not check_hardcoded_output(r, "Hello", []), \
            "No required constructs = not hardcoded"

    def test_hardcoded_even_odd(self):
        """print('odd') without if/else and input should be flagged."""
        r = analyze_code("print('odd')")
        assert check_hardcoded_output(r, "odd", ["input", "if", "print"])

    def test_expression_not_hardcoded(self):
        """print(5 + 5) should not count as hardcoded string."""
        r = analyze_code("print(5 + 5)")
        # hardcoded_outputs is empty (only string literals), so not flagged
        assert not check_hardcoded_output(r, "10", ["print"])


# ── Validation hints ────────────────────────────────────────────────────────


class TestMakeValidationHints:
    def test_syntax_error_hint(self):
        r = analyze_code("print('unclosed")
        hints = make_validation_hints(r, ["print"], "hello")
        assert any("Синтаксическая" in h for h in hints)

    def test_forbidden_import_hint(self):
        r = analyze_code("import os")
        hints = make_validation_hints(r, ["print"], "test")
        assert any("запрещено" in h for h in hints)

    def test_missing_variable_hint(self):
        r = analyze_code("print('10')")
        hints = make_validation_hints(r, ["variable", "print"], "10")
        assert any("переменную" in h for h in hints), \
            f"Expected hint about variable, got: {hints}"

    def test_missing_input_hint(self):
        r = analyze_code("print('Андрей')")
        hints = make_validation_hints(r, ["input", "print"], "Андрей")
        assert any("input" in h for h in hints)

    def test_missing_if_hint(self):
        r = analyze_code("print('Плюс')")
        hints = make_validation_hints(r, ["if", "print"], "Плюс")
        assert any("if" in h for h in hints), f"Expected if hint, got: {hints}"

    def test_missing_for_hint(self):
        r = analyze_code("print('test')")
        hints = make_validation_hints(r, ["for", "range", "print"], "test")
        assert any("for" in h for h in hints)

    def test_hardcode_hint(self):
        r = analyze_code("print('10')")
        hints = make_validation_hints(r, ["variable", "print"], "10")
        assert any("просто вывести" in h.lower() for h in hints), \
            f"Expected hardcode hint, got: {hints}"

    def test_infinite_loop_hint(self):
        r = analyze_code("while True:\n    print('loop')")
        hints = make_validation_hints(r, ["while", "print"], "loop")
        assert any("бесконечный" in h for h in hints)

    def test_all_correct_no_hints(self):
        r = analyze_code("x = 10\nprint(x)")
        hints = make_validation_hints(r, ["variable", "print"], "10")
        # Should be no error/hardcode hints (constructs present)
        error_hints = [h for h in hints if h.startswith(("🔧", "❗", "⛔", "⚠️"))]
        assert len(error_hints) == 0, f"Expected no error hints, got: {hints}"


# ── End‐to‐end scenario tests via the API ────────────────────────────────────


class TestMissionCheckAPIV2:
    """Integration tests hitting the /mission/check endpoint."""

    def _setup(self):
        """Import & configure test client lazily."""
        from fastapi.testclient import TestClient
        from app.main import app
        return TestClient(app)

    def test_correct_variable_solution(self):
        """1-3: coins = 10; print(coins) — correct solution."""
        client = self._setup()
        r = client.post("/mission/check", json={
            "lesson_id": "1-3",
            "code": "coins = 10\nprint(coins)",
        })
        data = r.json()
        assert data["finally_correct"] is True, f"Expected correct, got: {data}"
        assert data["structure_correct"] is True
        assert data["safety_passed"] is True

    def test_hardcoded_variable_rejected(self):
        """1-3: print('10') without variable should be rejected."""
        client = self._setup()
        r = client.post("/mission/check", json={
            "lesson_id": "1-3",
            "code": "print('10')",
        })
        data = r.json()
        assert data["finally_correct"] is False, \
            f"Hardcode should be rejected, got: {data}"
        assert data["structure_correct"] is False
        # Should have a hint about variable
        hints = data.get("hints", [])
        assert any("переменную" in h for h in hints), f"Expected variable hint, got: {hints}"

    def test_correct_print_solution(self):
        """1-1: print('...') — correct."""
        client = self._setup()
        r = client.post("/mission/check", json={
            "lesson_id": "1-1",
            "code": "print('Я начинаю путь Python')",
        })
        data = r.json()
        assert data["finally_correct"] is True, f"Expected correct, got: {data}"

    def test_forbidden_import_rejected(self):
        """Using 'import os' should be rejected."""
        client = self._setup()
        r = client.post("/mission/check", json={
            "lesson_id": "1-1",
            "code": "import os\nprint('test')",
        })
        data = r.json()
        assert data["finally_correct"] is False
        assert data["safety_passed"] is False
        assert data["structure_correct"] is False
        error = data.get("error", "")
        assert "запрещено" in error.lower(), f"Expected forbidden message, got: {error}"

    def test_missing_if_rejected(self):
        """1-8: print('Плюс') without if should be rejected."""
        client = self._setup()
        r = client.post("/mission/check", json={
            "lesson_id": "1-8",
            "code": "print('Плюс')",
        })
        data = r.json()
        assert data["finally_correct"] is False
        assert data["structure_correct"] is False
        hints = data.get("hints", [])
        assert any("if" in h for h in hints), f"Expected if hint, got: {hints}"

    def test_correct_if_solution_accepted(self):
        """1-8: x = 10; if x > 0: print('Плюс') — correct."""
        client = self._setup()
        r = client.post("/mission/check", json={
            "lesson_id": "1-8",
            "code": "x = 10\nif x > 0:\n    print('Плюс')",
        })
        data = r.json()
        assert data["finally_correct"] is True, f"Expected correct, got: {data}"
        assert data["structure_correct"] is True

    def test_backward_compatible_response_shape(self):
        """Legacy fields (correct, actual_output, expected_output, error)
        should still be present and correct."""
        client = self._setup()
        r = client.post("/mission/check", json={
            "lesson_id": "1-1",
            "code": "print('Я начинаю путь Python')",
        })
        data = r.json()
        # Legacy fields
        assert "correct" in data
        assert "actual_output" in data
        assert "expected_output" in data
        assert "error" in data
        # New fields
        assert "output_correct" in data
        assert "structure_correct" in data
        assert "safety_passed" in data
        assert "finally_correct" in data
        assert "hints" in data
        assert "details" in data
        # Legacy correct matches new finally_correct
        assert data["correct"] == data["finally_correct"]

    def test_hint_classification_carryover(self):
        """Regression: constructive hints (🔧) should not leak into errors.
        Only safety (⛔) and syntax (❗) should be in the error field.
        """
        client = self._setup()

        # Case: missing variable — hints should contain 🔧 but errors should NOT
        r = client.post("/mission/check", json={
            "lesson_id": "1-3",
            "code": "print('10')",
        })
        data = r.json()
        hints = data.get("hints", [])
        error = data.get("error") or ""
        has_constructive_hint = any("переменную" in h or "просто вывести" in h for h in hints)
        assert has_constructive_hint, \
            f"Expected constructive hint about variable, got: {hints}"
        # The error field should not contain the constructive hint text
        assert "переменную" not in error.lower(), \
            f"Constructive hint leaked into error: {error}"
        assert "просто вывести" not in error.lower(), \
            f"Constructive hint leaked into error: {error}"

    def test_safety_hints_are_errors(self):
        """Regression: safety violations (⛔) MUST appear in both hints AND errors."""
        client = self._setup()
        r = client.post("/mission/check", json={
            "lesson_id": "1-1",
            "code": "import os\nprint('test')",
        })
        data = r.json()
        error = data.get("error") or ""
        assert "запрещен" in error.lower(), \
            f"Safety violation should be in error, got: {error}"
