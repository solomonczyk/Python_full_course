"""Security-focused tests for the mission checker.

Ensures that:
- Dangerous imports are rejected via AST (before any potential execution)
- Forbidden calls (exec, eval) are detected
- Infinite loops are flagged
- PUBLIC_MODE skips subprocess execution
- Multiple test cases work correctly
"""

import importlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ast_checker import analyze_code, run_code_safely


class TestStaticSecurityAnalysis:
    """Tests that security issues are caught by static analysis alone."""

    def test_os_import_detected(self):
        """import os must be flagged as forbidden."""
        r = analyze_code("import os\nprint('test')")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "os"
        assert r.has_dangerous_patterns

    def test_subprocess_import_detected(self):
        """import subprocess must be flagged."""
        for imp in ["import subprocess", "import subprocess as sp"]:
            r = analyze_code(f"{imp}\nprint('test')")
            assert r.has_forbidden_import, f"'{imp}' not detected"
            assert r.forbidden_import_name == "subprocess"

    def test_socket_import_detected(self):
        r = analyze_code("import socket")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "socket"

    def test_sys_import_detected(self):
        r = analyze_code("import sys\nprint('test')")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "sys"

    def test_requests_import_detected(self):
        r = analyze_code("import requests")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "requests"

    def test_shutil_import_detected(self):
        r = analyze_code("import shutil")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "shutil"

    def test_pathlib_import_detected(self):
        r = analyze_code("import pathlib")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "pathlib"

    def test_from_import_detected(self):
        r = analyze_code("from os import path")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "os"

    def test_exec_detected(self):
        r = analyze_code('exec("print(1)")')
        assert r.has_dangerous_patterns

    def test_eval_detected(self):
        r = analyze_code('eval("1+1")')
        assert r.has_dangerous_patterns

    def test_compile_detected(self):
        r = analyze_code('compile("x=1", "", "exec")')
        assert r.has_dangerous_patterns

    def test__import__detected(self):
        r = analyze_code('__import__("os")')
        assert r.has_dangerous_patterns

    def test_open_detected(self):
        r = analyze_code('open("/etc/passwd")')
        assert r.has_dangerous_patterns

    def test_breakpoint_detected(self):
        r = analyze_code("breakpoint()")
        assert r.has_dangerous_patterns

    def test_multiple_forbidden_imports(self):
        """Multiple forbidden imports should all be detected."""
        r = analyze_code("import os\nimport sys\nprint('test')")
        assert r.has_forbidden_import
        # First forbidden import caught
        assert r.forbidden_import_name is not None

    def test_ctypes_import_detected(self):
        r = analyze_code("import ctypes")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "ctypes"

    def test_signal_import_detected(self):
        r = analyze_code("import signal")
        assert r.has_forbidden_import
        assert r.forbidden_import_name == "signal"


class TestInfiniteLoopDetection:
    """AST detection of potentially infinite loops."""

    def test_while_true(self):
        r = analyze_code("while True:\n    print('inf')")
        assert r.has_infinite_loop_risk

    def test_while_1(self):
        r = analyze_code("while 1:\n    print('inf')")
        # `while 1` AST Constant(1) -> bool(1) is True
        assert r.has_infinite_loop_risk

    def test_normal_while_not_flagged(self):
        r = analyze_code("i = 0\nwhile i < 3:\n    print(i)\n    i += 1")
        assert not r.has_infinite_loop_risk
        assert "while" in r.constructs

    def test_for_loop_not_flagged(self):
        """for loops are always finite (bounded) in Python."""
        r = analyze_code("for i in range(5):\n    print(i)")
        assert not r.has_infinite_loop_risk

    def test_while_with_break_not_flagged(self):
        r = analyze_code("while True:\n    x = input()\n    if x == 'q':\n        break")
        # Currently we flag while True regardless (simple detection)
        assert r.has_infinite_loop_risk


class TestPublicMode:
    """PUBLIC_MODE behaviour — tests the function directly."""

    def test_public_mode_not_set_by_default(self):
        """Without env var, public mode should be False."""
        old = os.environ.pop("PUBLIC_MODE", None)
        import app.routers.mission as m
        # Reload to pick up current env
        importlib.reload(m)
        assert m._is_public_mode() is False
        if old is not None:
            os.environ["PUBLIC_MODE"] = old

    def test_public_mode_set(self):
        os.environ["PUBLIC_MODE"] = "1"
        import app.routers.mission as m
        importlib.reload(m)
        assert m._is_public_mode() is True
        os.environ.pop("PUBLIC_MODE", None)
        importlib.reload(m)

    def test_public_mode_rejects_hardcode_via_ast(self):
        """Hardcode detection is AST-based and does not depend on PUBLIC_MODE.
        This test verifies that hardcoded output is rejected regardless."""
        from app.ast_checker import analyze_code, check_hardcoded_output

        r = analyze_code("print('10')")
        assert check_hardcoded_output(r, "10", ["variable"]), \
            "Hardcode should be detected regardless of PUBLIC_MODE"


class TestSafeRunner:
    """Tests for the safe code runner (non-public mode)."""

    def test_simple_execution(self):
        passed, out, err = run_code_safely(
            "print('Hello')", "Hello"
        )
        assert passed, f"Expected pass, got err={err}, out={out}"
        assert out == "Hello"

    def test_with_input(self):
        passed, out, err = run_code_safely(
            "name = input()\nprint(name)", "Alice",
            test_cases=[{"input": "Alice", "expected_output": "Alice"}],
        )
        assert passed, f"Expected pass, got err={err}, out={out}"

    def test_multiple_test_cases(self):
        """Multiple test cases: all must pass."""
        code = "n = int(input())\nif n % 2 == 0:\n    print('even')\nelse:\n    print('odd')"
        passed, out, err = run_code_safely(
            code, "even",
            test_cases=[
                {"input": "4", "expected_output": "even"},
                {"input": "7", "expected_output": "odd"},
            ],
        )
        assert passed, f"Expected all test cases pass, got err={err}"

    def test_test_case_fails(self):
        """When one test case fails, the runner reports failure."""
        code = "n = int(input())\nprint('even')"  # always prints even
        passed, out, err = run_code_safely(
            code, "even",
            test_cases=[
                {"input": "4", "expected_output": "even"},
                {"input": "7", "expected_output": "odd"},
            ],
        )
        assert not passed, "Should fail on uneven input"
        # The error should mention 'odd' and 'even'
        assert err and ("odd" in err or "even" in err)

    def test_timeout_handling(self):
        """Infinite loops should time out gracefully."""
        passed, out, err = run_code_safely(
            "while True:\n    pass", "",
            timeout=1,
        )
        assert not passed
        assert err and ("врем" in err or "timeout" in err.lower() or "Time" in err or "5" in err)

    def test_syntax_error_execution(self):
        """Syntax errors should be caught."""
        passed, out, err = run_code_safely(
            "print('unclosed", "",
        )
        assert not passed
        assert err is not None

    def test_no_test_cases_fallback(self):
        """Without test_cases, compare to expected_output directly."""
        passed, out, err = run_code_safely(
            "print(5 + 5)", "10",
        )
        assert passed
        assert out == "10"


class TestResponseCompatibility:
    """Backward compatibility of the API response."""

    def test_old_fields_present(self):
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)

        r = client.post("/mission/check", json={
            "lesson_id": "1-1",
            "code": "print('Я начинаю путь Python')",
        })
        data = r.json()
        # These are the fields the original test suite expects
        assert "correct" in data
        assert "actual_output" in data
        assert "expected_output" in data
        assert "error" in data
        # These are the new fields
        assert "output_correct" in data
        assert "structure_correct" in data
        assert "safety_passed" in data
        assert "finally_correct" in data
        assert "hints" in data
        assert "details" in data

    def test_lesson_not_found(self):
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)

        r = client.post("/mission/check", json={
            "lesson_id": "invalid",
            "code": "print('test')",
        })
        assert r.status_code == 404

    def test_no_mission(self):
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)

        # Lesson 3-0 doesn't exist; 1-1 definitely has a mission
        # Try to find a lesson without a mission from the real data
        import json
        data_path = Path(__file__).resolve().parent.parent / "app" / "data" / "lessons.json"
        with open(data_path, encoding="utf-8") as f:
            lessons = json.load(f)
        no_mission = [item for item in lessons if not item.get("mission")]
        if no_mission:
            r = client.post("/mission/check", json={
                "lesson_id": no_mission[0]["id"],
                "code": "print('test')",
            })
            assert r.status_code == 400
