# Python Quest — Execution Model

## Overview

Python Quest uses a **dual execution model**: student code runs in two distinct environments depending on context.

---

## 1. Frontend: Pyodide (in-browser Python)

**Where**: CodePlayground component (`frontend/src/components/CodePlayground.tsx`)

**How it works**:
- On page load, Pyodide v0.25.1 is loaded from CDN (`https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js`).
- Python code executes entirely in the user's browser via WebAssembly.
- No network requests are made during code execution.
- stdout is captured via `io.StringIO` redirection and displayed in the playground output area.

**Capabilities**:
- Standard Python syntax (variables, loops, conditionals, functions)
- Built-in functions (`print`, `len`, `range`, `input`, etc.)
- Common standard library modules (limited by Pyodide's WebAssembly runtime)

**Limitations**:
- No filesystem access (`open()` writes to a virtual in-memory filesystem, not real disk)
- Some C-extension modules are unavailable
- Network requests (`import urllib`, `import requests`) are restricted by browser security
- Execution is single-threaded

**Used for**:
- Interactive code playground in lesson pages
- Student experimentation and exploration

---

## 2. Backend: subprocess.run (server-side execution)

**Where**: API routes `POST /mission/check` and `POST /quests/{quest_id}/check` in `api/index.py`

**How it works**:
- Student code is written to a temporary `.py` file on the Vercel server filesystem.
- The file is executed via `subprocess.run([python, tmp_path], ...)` with a 5-second timeout.
- stdout and stderr are captured and returned as API responses.

**Safety constraints**:
- **Forbidden imports**: `os`, `sys`, `subprocess`, `socket`, `shutil`, `pathlib`, `requests`, and dangerous patterns like `__import__`, `exec(`, `eval(` are blocked by string matching before execution.
- **Timeout**: All executions are hard-capped at 5 seconds via `subprocess.TimeoutExpired`.
- **Ephemeral**: Temp files are deleted in a `finally` block after execution.
- **Encoding**: `PYTHONIOENCODING=utf-8` is set in the subprocess environment.

**Used for**:
- Mission output checking (`POST /mission/check`)
- Quest test case verification (`POST /quests/{quest_id}/check`)

---

## Summary

| Aspect | Frontend (CodePlayground) | Backend (Mission/Quest check) |
|--------|--------------------------|-------------------------------|
| Runtime | Pyodide (WebAssembly) | CPython via subprocess |
| Location | Browser (client-side) | Vercel serverless function |
| Network required for run? | No (after initial CDN load) | Yes (API call) |
| Timeout | None (browser tab context) | 5 seconds |
| Forbidden imports | Pyodide-inherent restrictions | Blocklist + timeout |
| Persistence | None (in-memory only) | None (temp file cleaned up) |
| Used in | Lesson playground | Mission/quest grading |

## False Claims

The README accurately describes Pyodide as the interpreter for the code playground ("Интерпретатор | Pyodide (WebAssembly — Python в браузере)"). No false browser-execution claims exist in the codebase. The backend subprocess execution is documented here for clarity; it is a separate path used only for automated grading, not for student-facing code execution.
