# Mission Checker v2 — Structure & Safety Validation

## Overview

The v2 checker adds **AST-based static analysis** on top of the legacy output comparison.  Every student submission is first analysed without execution to verify:

- **Required constructs** are present (variables, `if`, `for`, `while`, `input()`, etc.)
- **Hardcoded output** is detected (a literal `print("10")` when the lesson expects `coins = 10; print(coins)`)
- **Forbidden imports** and dangerous calls (`exec`, `eval`, `os.system`, etc.) are rejected
- **Infinite loop risk** is flagged

Only after all structural and safety checks pass does the checker optionally run the code for output validation — and in `PUBLIC_MODE` even that step is skipped.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  POST /mission/check                                    │
│                                                          │
│  1. Load lesson & validation metadata                    │
│  2. AST analysis (no execution)                          │
│     ├─ Parse code → syntax check                         │
│     ├─ Detect constructs (variable, if, for, …)          │
│     ├─ Detect forbidden imports & dangerous calls        │
│     └─ Detect hardcoded output & infinite loops          │
│                                                          │
│  3. Safety check                                         │
│     ├─ Forbidden import?  → reject                       │
│     ├─ Dangerous pattern? → reject                       │
│     └─ Syntax error?     → reject                        │
│                                                          │
│  4. Structure check                                      │
│     ├─ All required constructs present?                  │
│     ├─ Hardcoded output detected?                        │
│     └─ → hints: missing_variable, expected_if, ...       │
│                                                          │
│  5. Output check (only if structure & safety pass)       │
│     ├─ PUBLIC_MODE=1  → AST-only comparison             │
│     ├─ ast_only=True   → trust structure                 │
│     └─ otherwise       → subprocess with test_cases      │
│                                                          │
│  6. Return rich response                                 │
└──────────────────────────────────────────────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `backend/app/ast_checker.py` | Core AST analysis engine — no execution, pure static analysis |
| `backend/app/validation_metadata.py` | Per-lesson validation rules (required constructs, test cases) |
| `backend/app/routers/mission.py` | FastAPI endpoint — wires AST checker + validation + optional execution |
| `frontend/src/types/index.ts` | TypeScript types including new MissionResult fields |
| `frontend/src/components/MissionCard.tsx` | UI — shows hints, detailed error breakdown |
| `backend/tests/test_mission_checker_v2.py` | Unit + integration tests for AST checker |
| `backend/tests/test_mission_security.py` | Security-focused tests |
| `scripts/audit_lesson_validation_metadata.py` | Audit script to review all lesson validation rules |

---

## AST Checker (`ast_checker.py`)

### `analyze_code(code: str) → AnalysisResult`

Parses and walks the AST, returning:

| Field | Type | Description |
|-------|------|-------------|
| `constructs` | `set[str]` | Detected constructs: `variable`, `print`, `input`, `int_call`, `float_call`, `if`, `elif`, `else`, `for`, `while`, `range`, `function_def`, `return`, `list`, `dict`, `tuple`, `modulo`, `len_call`, `str_call`, `random_import`, `math_import` |
| `errors` | `list[str]` | Human-readable error messages |
| `hardcoded_outputs` | `list[str]` | String literals passed to `print()` |
| `print_has_variable` | `bool` | True if any `print()` call contains a non-literal argument |
| `has_dangerous_patterns` | `bool` | True if `exec`/`eval`/`open`/etc. detected |
| `has_infinite_loop_risk` | `bool` | True for `while True:` / `while 1:` |
| `has_forbidden_import` | `bool` | True if a blocked module is imported |
| `forbidden_import_name` | `str \| None` | Which module triggered the block |
| `is_syntactically_valid` | `bool` | False if parsing failed |
| `syntax_error_detail` | `str \| None` | Russian-friendly syntax error message |

### `check_required_constructs(detected, required) → (passed, hint_key)`

Returns whether all required constructs are present, and a hint key for the first missing one.

### `check_hardcoded_output(result, expected_output, required_constructs) → bool`

Returns `True` if the code merely prints the expected output as a literal string without using the required constructs.

### `make_validation_hints(result, required_constructs, expected_output) → list[str]`

Builds a list of human-readable (Russian) hint messages. Covers:

| Category | Hint example |
|----------|-------------|
| Syntax error | `❗ Синтаксическая ошибка: строка 1: неверный синтаксис` |
| Forbidden import | `⛔ Использование модуля 'os' запрещено` |
| Dangerous code | `⛔ Код содержит запрещённые операции` |
| Missing variable | `🔧 Нужно создать переменную. Пример: name = 'Андрей'` |
| Missing input | `🔧 Нужно использовать input() для ввода данных` |
| Missing if | `🔧 Нужно использовать if для проверки условия` |
| Missing for | `🔧 Нужно использовать цикл for для повторения` |
| Missing while | `🔧 Нужно использовать цикл while` |
| Hardcoded output | `🔧 Просто вывести правильный ответ — не достаточно. Используй переменные / ввод / условия из урока` |
| Infinite loop | `⚠️ Похоже на бесконечный цикл (while True без break)` |

---

## Validation Metadata (`validation_metadata.py`)

Each lesson that makes structural demands gets a `LessonValidation` record:

| Field | Type | Description |
|-------|------|-------------|
| `lesson_id` | `str` | e.g. `"1-3"` |
| `title` | `str` | Lesson title |
| `required_constructs` | `list[str]` | e.g. `["variable", "print"]` |
| `reject_hardcoded` | `bool` | Default `True` for non-trivial lessons |
| `forbidden_patterns` | `list[str]` | Additional string patterns to reject |
| `test_cases` | `list[dict]` | `[{"input": "7", "expected_output": "odd"}]` |
| `ast_only` | `bool` | Skip output check entirely (for random/indeterminate missions) |

Lessons *not* listed use an auto-detected default (usually `["print"]` only) for backward compatibility.

---

## Response Format

### Legacy fields (unchanged)

```json
{
  "correct": true,
  "actual_output": "10",
  "expected_output": "10",
  "error": null
}
```

### New v2 fields

```json
{
  "output_correct": true,
  "structure_correct": true,
  "safety_passed": true,
  "finally_correct": true,
  "hints": ["🔧 Нужно создать переменную. Пример: name = 'Андрей'"],
  "details": {
    "constructs_found": ["print", "variable"],
    "required_constructs": ["variable", "print"],
    "missing_constructs": ["input"]
  }
}
```

| Field | Type | Meaning |
|-------|------|---------|
| `output_correct` | `bool \| null` | Output matches expected (or `null` if not checked) |
| `structure_correct` | `bool` | All required constructs present |
| `safety_passed` | `bool` | No forbidden imports, no dangerous patterns |
| `finally_correct` | `bool` | Overall pass (== `correct` for backward compat) |
| `hints` | `string[]` | Human-readable hint messages |
| `details` | `object` | Debug info: constructs found, required, missing |

---

## PUBLIC_MODE

Set `PUBLIC_MODE=1` (or `true`, `yes`) in the environment to **disable all subprocess execution**.  In this mode:

- AST analysis still runs (constructs, safety, hardcode detection)
- For deterministic output (`print("literal")`) a static comparison is made
- For variable/expression-based output `output_correct` is set to `null`
- The hint "Код структурно верен. Запусти локально для проверки вывода." is shown

This is intended for production deployment where running arbitrary student code is unsafe.

---

## Test Cases

Lessons that depend on `input()` can define multiple test cases:

```python
LessonValidation(
    "1-9",
    required_constructs=["input", "int_call", "if", "else", "modulo", "print"],
    test_cases=[
        {"input": "7", "expected_output": "odd"},
        {"input": "4", "expected_output": "even"},
    ],
)
```

All test cases must pass for the output to be considered correct.

---

## Security Properties

1. **No raw subprocess in PUBLIC_MODE** — `os.environ["PUBLIC_MODE"]` gates execution
2. **AST pre-check always runs** — dangerous code is rejected before any execution
3. **Forbidden imports blocked** — `os`, `sys`, `subprocess`, `socket`, `shutil`, `pathlib`, `requests`, `ctypes`, `signal`, `multiprocessing`, `threading`, `pickle`, `shelve`, `sqlite3`, `http`, `urllib`, `webbrowser`, `importlib`, `builtins`, `compile`, `dis`, `inspect`
4. **Dangerous calls blocked** — `exec()`, `eval()`, `compile()`, `__import__()`, `open()`, `breakpoint()`, `exit()`, `quit()`
5. **Infinite loop timeout** — subprocess execution has a 5-second timeout

---

## Running Tests

```bash
cd backend
pytest tests/test_mission_checker_v2.py -v
pytest tests/test_mission_security.py -v

# All tests
pytest tests/ -v

# Ruff linting
ruff check app tests
```

---

## Legacy Compatibility

- The old `correct`, `actual_output`, `expected_output`, `error` fields remain unchanged
- `correct` always equals `finally_correct`
- Existing frontend code that reads only `correct` continues to work
- New fields are additive — no breaking changes to the API contract
