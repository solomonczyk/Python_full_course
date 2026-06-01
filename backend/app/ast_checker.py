"""AST-based static checker for beginner Python code.

Provides safe, non-executing analysis of Python code to:
- Detect which constructs are used (variables, if/for/while, input, etc.)
- Detect forbidden imports and patterns
- Detect hardcoded output (print("literal") when a construct is required)
- Classify code for safety (infinite loops, dangerous calls)
"""

import ast
from dataclasses import dataclass, field

# ── Result types ────────────────────────────────────────────────────────────


@dataclass
class AnalysisResult:
    """Result of static AST analysis on a piece of student code."""

    constructs: set[str] = field(default_factory=set)
    """Set of detected constructs, e.g. {'variable', 'print', 'if', 'input'}."""

    errors: list[str] = field(default_factory=list)
    """Human-readable error messages (syntax errors, forbidden patterns)."""

    hardcoded_outputs: list[str] = field(default_factory=list)
    """String literals found in print() calls (for hardcode detection)."""

    has_dangerous_patterns: bool = False
    """True if the code uses exec/eval/import os/subprocess etc."""

    has_infinite_loop_risk: bool = False
    """True if a while loop has a constant True condition or no bound check."""

    has_forbidden_import: bool = False
    """True if code imports a forbidden module."""

    forbidden_import_name: str | None = None
    """Name of the first forbidden import found."""

    print_has_variable: bool = False
    """True if any print() call contains a non-literal (variable/expression)."""

    is_syntactically_valid: bool = True
    """False if the code cannot be parsed."""

    syntax_error_detail: str | None = None
    """Details of syntax error if parsing failed."""


# ── Forbidden imports ───────────────────────────────────────────────────────

# These are checked both via AST (static) and string-match (belt-and-suspenders)
_FORBIDDEN_IMPORT_PATTERNS: list[str] = [
    "os",
    "sys",
    "subprocess",
    "socket",
    "shutil",
    "pathlib",
    "requests",
    "ctypes",
    "signal",
    "multiprocessing",
    "threading",
    "pickle",
    "shelve",
    "sqlite3",
    "http",
    "urllib",
    "webbrowser",
    "importlib",
    "builtins",
    "compile",
    "dis",
    "inspect",
]

# These function/statement patterns are always forbidden in student code
_FORBIDDEN_CALLS: set[str] = {
    "exec",
    "eval",
    "compile",
    "__import__",
    "open",
    "breakpoint",
    "exit",
    "quit",
    "help",
}


# ── AST‐based construct detector ────────────────────────────────────────────


class _ConstructDetector(ast.NodeVisitor):
    """Walks an AST and records what constructs it finds."""

    def __init__(self) -> None:
        self.constructs: set[str] = set()
        self.hardcoded_outputs: list[str] = []
        self.print_has_variable: bool = False
        self.has_dangerous: bool = False
        self.has_infinite_loop: bool = False
        self.has_forbidden_import: bool = False
        self.forbidden_import_name: str | None = None

    # ── Variable assignment ──────────────────────────────────────────────

    def visit_Assign(self, node: ast.Assign) -> None:
        self.constructs.add("variable")
        self.generic_visit(node)

    visit_AnnAssign = visit_Assign  # type: ignore  # `x: int = 5`

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.constructs.add("variable")
        self.generic_visit(node)

    # ── Function calls (print, input, int, float, range) ─────────────────

    def visit_Call(self, node: ast.Call) -> None:
        fn = self._resolve_func_name(node)
        if fn == "print":
            self.constructs.add("print")
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    self.hardcoded_outputs.append(arg.value)
                else:
                    self.print_has_variable = True
        elif fn == "input":
            self.constructs.add("input")
        elif fn == "int":
            self.constructs.add("int_call")
        elif fn == "float":
            self.constructs.add("float_call")
        elif fn == "str":
            self.constructs.add("str_call")
        elif fn == "range":
            self.constructs.add("range")
        elif fn == "len":
            self.constructs.add("len_call")
        elif fn == "sum":
            self.constructs.add("sum_call")
        elif fn == "list":
            self.constructs.add("list_call")
        elif fn == "dict":
            self.constructs.add("dict_call")
        elif fn in _FORBIDDEN_CALLS:
            self.has_dangerous = True

        self.generic_visit(node)

    def _resolve_func_name(self, node: ast.Call) -> str | None:
        if isinstance(node.func, ast.Name):
            return node.func.id
        # Handle obj.method() — we only care about simple names
        if isinstance(node.func, ast.Attribute):
            # e.g. random.randint → check only for dangerous attr access
            attr = node.func.attr
            if attr in ("run", "call", "system", "popen", "fork", "exec"):
                self.has_dangerous = True
            return attr
        return None

    # ── Control flow ─────────────────────────────────────────────────────

    def visit_If(self, node: ast.If) -> None:
        self.constructs.add("if")
        if node.orelse:
            # an elif clause is just an If inside orelse
            if isinstance(node.orelse[0], ast.If):
                self.constructs.add("elif")
            else:
                self.constructs.add("else")
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.constructs.add("for")
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.constructs.add("while")
        # Detect likely-infinite loops: while True, while 1, etc.
        if isinstance(node.test, ast.Constant) and bool(node.test.value) is True:
            self.has_infinite_loop = True
        self.generic_visit(node)

    # ── Functions ────────────────────────────────────────────────────────

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.constructs.add("function_def")
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        self.constructs.add("return")
        self.generic_visit(node)

    # ── Data structures ──────────────────────────────────────────────────

    def visit_List(self, node: ast.List) -> None:
        self.constructs.add("list")
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        self.constructs.add("dict")
        self.generic_visit(node)

    def visit_Tuple(self, node: ast.Tuple) -> None:
        self.constructs.add("tuple")
        self.generic_visit(node)

    # ── Operators (modulo, comparison, boolean) ──────────────────────────

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if isinstance(node.op, ast.Mod):
            self.constructs.add("modulo")
        self.generic_visit(node)

    # ── Imports ──────────────────────────────────────────────────────────

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self._check_import_name(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self._check_import_name(node.module.split(".")[0])
        self.generic_visit(node)

    def _check_import_name(self, name: str) -> None:
        root = name.split(".")[0]
        if root in _FORBIDDEN_IMPORT_PATTERNS:
            self.has_forbidden_import = True
            self.forbidden_import_name = root
            self.has_dangerous = True
        elif root == "random":
            self.constructs.add("random_import")
        elif root == "math":
            self.constructs.add("math_import")


# ── Public API ──────────────────────────────────────────────────────────────


def analyze_code(code: str) -> AnalysisResult:
    """Parse and analyse student Python code safely (no execution).

    Returns an ``AnalysisResult`` with all detected constructs, errors, and
    safety flags.  This is the main entry-point for the module.
    """
    result = AnalysisResult()

    # 1. Try to parse
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        result.is_syntactically_valid = False
        result.syntax_error_detail = _format_syntax_error(exc)
        result.errors.append(f"SyntaxError: {result.syntax_error_detail}")
        return result

    # 2. Walk the AST
    detector = _ConstructDetector()
    detector.visit(tree)

    # 3. Populate result
    result.constructs = detector.constructs
    result.hardcoded_outputs = detector.hardcoded_outputs
    result.print_has_variable = detector.print_has_variable
    result.has_dangerous_patterns = detector.has_dangerous
    result.has_infinite_loop_risk = detector.has_infinite_loop
    result.has_forbidden_import = detector.has_forbidden_import
    result.forbidden_import_name = detector.forbidden_import_name

    # 4. Extra string-based forbidden-import catch (belt-and-suspenders
    #    for dynamically constructed imports AST can't catch easily)
    code_lower = code.lower()
    if not result.has_forbidden_import:
        for pat in ("__import__", "exec(", "eval("):
            if pat in code_lower:
                result.has_dangerous_patterns = True
                result.errors.append(f"Использование {pat} запрещено")
                break

    return result


def check_required_constructs(
    detected: set[str],
    required: list[str] | None,
    lesson_title: str = "",
) -> tuple[bool, str | None]:
    """Check that every construct in *required* is present in *detected*.

    Returns ``(passed: bool, hint_key: str | None)``.
    The *hint_key* is a short string the frontend can map to a localised
    message (e.g. ``"missing_variable"``, ``"missing_input"``).
    """
    if not required:
        return True, None

    missing = [c for c in required if c not in detected]
    if not missing:
        return True, None

    # Map the first missing construct to a hint key
    hint_map: dict[str, str] = {
        "variable": "missing_variable",
        "print": "missing_print",
        "input": "missing_input",
        "int_call": "missing_int",
        "float_call": "missing_float",
        "if": "expected_if",
        "else": "expected_else",
        "elif": "expected_elif",
        "for": "expected_for",
        "range": "expected_range",
        "while": "expected_while",
        "modulo": "expected_modulo",
        "function_def": "expected_function",
        "return": "expected_return",
        "list": "expected_list",
        "dict": "expected_dict",
        "random_import": "expected_random",
        "tuple": "expected_tuple",
    }
    hint_key = hint_map.get(missing[0], f"missing_{missing[0]}")
    return False, hint_key


def check_hardcoded_output(
    result: AnalysisResult,
    expected_output: str,
    required_constructs: list[str] | None = None,
) -> bool:
    """Return True if the output appears to be hardcoded (just a literal
    print) when a non-trivial construct was expected.

    This detects cheats like  ``print("10")``  when the lesson expects
    ``coins = 10; print(coins)``.
    """
    if not result.hardcoded_outputs:
        return False
    # If at least one print() has a variable/expression, it's not pure hardcode
    if result.print_has_variable:
        return False

    # No constructs required = simple print lesson = not hardcoded
    if not required_constructs:
        return False

    # If we're told a construct is required and it's missing, check whether
    # the user just printed the expected string verbatim
    has_required = all(
        c in result.constructs for c in required_constructs
    )
    if not has_required:
        # The user is missing the construct AND only printing literals
        for out in result.hardcoded_outputs:
            if out.strip() == expected_output.strip():
                return True

    return False


def make_validation_hints(
    result: AnalysisResult,
    required_constructs: list[str] | None,
    expected_output: str,
) -> list[str]:
    """Build a list of human-readable hint messages based on analysis.

    These are short Russian strings displayed to the student.
    """
    hints: list[str] = []

    if not result.is_syntactically_valid:
        hints.append(f"❗ Синтаксическая ошибка: {result.syntax_error_detail}")
        return hints

    if result.has_forbidden_import:
        hints.append(
            f"⛔ Использование модуля '{result.forbidden_import_name}' запрещено"
        )
        return hints

    if result.has_dangerous_patterns:
        hints.append("⛔ Код содержит запрещённые операции")
        return hints

    if result.has_infinite_loop_risk:
        hints.append("⚠️ Похоже на бесконечный цикл (while True без break)")

    # Check required constructs
    if required_constructs:
        passed, hint_key = check_required_constructs(
            result.constructs, required_constructs,
        )
        if not passed:
            hint_texts = {
                "missing_variable": (
                    "🔧 Нужно создать переменную. "
                    "Пример: name = 'Андрей'"
                ),
                "missing_print": (
                    "🔧 Нужно использовать print() для вывода"
                ),
                "missing_input": (
                    "🔧 Нужно использовать input() для ввода данных"
                ),
                "missing_int": (
                    "🔧 Нужно преобразовать ввод в число: int(input())"
                ),
                "missing_float": (
                    "🔧 Нужно преобразовать ввод в float: float(input())"
                ),
                "expected_if": (
                    "🔧 Нужно использовать if для проверки условия"
                ),
                "expected_else": (
                    "🔧 Нужно добавить else для второго случая"
                ),
                "expected_elif": (
                    "🔧 Нужно использовать elif для дополнительных условий"
                ),
                "expected_for": (
                    "🔧 Нужно использовать цикл for для повторения"
                ),
                "expected_range": (
                    "🔧 Нужно использовать range() для задания диапазона"
                ),
                "expected_while": (
                    "🔧 Нужно использовать цикл while"
                ),
                "expected_modulo": (
                    "🔧 Нужно использовать оператор % (остаток от деления)"
                ),
                "expected_function": (
                    "🔧 Нужно определить функцию через def"
                ),
                "expected_return": (
                    "🔧 Нужно использовать return в функции"
                ),
                "expected_list": (
                    "🔧 Нужно создать список [...]"
                ),
                "expected_dict": (
                    "🔧 Нужно создать словарь {\"key\": value}"
                ),
                "expected_random": (
                    "🔧 Нужно импортировать random: import random"
                ),
                "expected_tuple": (
                    "🔧 Нужно использовать кортеж (tuple)"
                ),
            }
            hints.append(hint_texts.get(hint_key or "", f"Не хватает: {hint_key}"))

    # Check for hardcoded output
    if check_hardcoded_output(result, expected_output, required_constructs):
        hints.append(
            "🔧 Просто вывести правильный ответ — не достаточно. "
            "Используй переменные / ввод / условия из урока"
        )

    return hints


# ── Helpers ─────────────────────────────────────────────────────────────────


def _format_syntax_error(exc: SyntaxError) -> str:
    """Produce a beginner-friendly syntax error message."""
    parts = []
    if exc.lineno:
        parts.append(f"строка {exc.lineno}")
    if exc.msg:
        msg = exc.msg
        # Simplify some common CPython messages
        replacements = {
            "invalid syntax": "неверный синтаксис",
            "unterminated": "не завершена строка",
            "unexpected indent": "неожиданный отступ",
            "unexpected character": "неожиданный символ",
        }
        for eng, rus in replacements.items():
            if msg.startswith(eng):
                msg = msg.replace(eng, rus, 1)
                break
        parts.append(msg)
    return ": ".join(parts)


# ── Safe code runner (non‐public mode) ──────────────────────────────────────


def run_code_safely(
    code: str,
    expected_output: str,
    test_cases: list[dict[str, str]] | None = None,
    timeout: int = 5,
) -> tuple[bool, str | None, str | None]:
    """Execute student code in a subprocess and validate output.

    **Not safe for public/production use** — this is the escape hatch for
    local development and CI where subprocess execution is acceptable.

    Args:
        code: Student Python source.
        expected_output: Expected stdout output (stripped).
        test_cases: Optional list of ``{"input": ..., "expected_output": ...}``
                    dicts.  If provided, *all* must pass.
        timeout: Per‐execution timeout in seconds.

    Returns:
        ``(all_passed: bool, actual_output: str | None, error: str | None)``
    """
    import os
    import subprocess  # noqa: S404 — only used in non‑public mode
    import tempfile

    def _run(input_data: str | None = None) -> tuple[str, str]:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8",
        ) as f:
            f.write(code)
            tmp = f.name
        try:
            # Try python first, fallback to python3
            py = "python3"
            try:
                subprocess.run(
                    ["python", "--version"],
                    capture_output=True, timeout=2,
                )
                py = "python"
            except Exception:
                pass

            # Ensure UTF-8 encoding for subprocess (critical on Windows
            # for Cyrillic / non-ASCII output)
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"

            proc = subprocess.run(  # noqa: S603
                [py, tmp],
                capture_output=True, text=True, timeout=timeout,
                input=input_data or None,  # stdin for input()
                env=env,
            )
            return proc.stdout.strip(), proc.stderr.strip()
        finally:
            try:
                os.unlink(tmp)
            except Exception:
                pass

    # If we have test_cases, run once per case
    if test_cases:
        for tc in test_cases:
            inp = tc.get("input", "")
            exp = tc.get("expected_output", "")
            try:
                actual, stderr = _run(inp)
                if stderr:
                    return False, actual, stderr
                if actual.strip() != exp.strip():
                    return False, actual, f"Получено: {actual}, ожидалось: {exp}"
            except subprocess.TimeoutExpired:
                return (
                    False,
                    None,
                    "Превышено время выполнения (5 сек). Проверь, нет ли бесконечного цикла",
                )
            except Exception as e:
                return False, None, str(e)
        return True, None, None

    # Single run with no test case
    try:
        actual, stderr = _run()
        if stderr:
            return False, actual, stderr
        passed = actual.strip() == expected_output.strip()
        return passed, actual, None
    except subprocess.TimeoutExpired:
        return (
            False,
            None,
            "Превышено время выполнения (5 сек). Проверь, нет ли бесконечного цикла",
        )
    except Exception as e:
        return False, None, str(e)
