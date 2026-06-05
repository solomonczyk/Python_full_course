# Production Truth Audit Verification

Task: PYTHON-QUEST-PRODUCTION-TRUTH-REPAIR-001
Date: 2026-06-05
Auditor: Independent audit (third-party)
Verifier: Claude Code production-truth-repair layer

---

## Claim 1: Turso not physically connected on Vercel

- **Claim**: Turso is not physically connected on Vercel because libsql-experimental is missing from root/requirements.txt. Vercel reads root/requirements.txt for api/index.py. Current code catches ImportError and silently falls back to SQLite /tmp, causing progress loss on cold start.
- **Verified**: **TRUE**
- **Files inspected**:
  - `requirements.txt` (root) — contains only `fastapi==0.115.14`, `uvicorn==0.34.3`, `pydantic>=2.12.0`. No `libsql-experimental`.
  - `backend/requirements.txt` — contains `libsql-experimental>=0.0.21; sys_platform == 'linux' or sys_platform == 'darwin'` (but Vercel does not use this file).
  - `api/index.py` lines 50-63 — `get_connection()` attempts `import libsql_experimental` and on `ImportError` silently falls through to `sqlite3.connect(str(_DB_PATH))` where `_DB_PATH` defaults to `/tmp/progress.db`. No warning, no error, no production guard.
  - `vercel.json` — sets `DB_PATH: /tmp/progress.db`, confirming /tmp is the configured fallback path.
- **Severity**: **CRITICAL** — students lose all progress on cold start. Vercel serverless functions are ephemeral; /tmp is not persistent across invocations.
- **Fix applied**: Added `libsql-experimental>=0.0.21; sys_platform == 'linux' or sys_platform == 'darwin'` to root `requirements.txt`. Modified `api/index.py` to fail-closed in production when Turso is unavailable: no silent /tmp fallback.

---

## Claim 2: Dead navigation links (Sandbox and Leaderboard)

- **Claim**: Sandbox and Leaderboard buttons exist in TopNav, but pages/routes are missing.
- **Verified**: **TRUE**
- **Files inspected**:
  - `frontend/src/components/TopNav.tsx` lines 44-48 — nav tabs include `{ label: 'Leaderboard', path: '/leaderboard' }` and `{ label: 'Sandbox', path: '/sandbox' }`.
  - `frontend/src/App.tsx` lines 56-62 — registered routes: `/`, `/part/:partNum`, `/lesson/:id`, `/review/:id`, `/quest/:id`, `/recap/:id`. No `/leaderboard` or `/sandbox` routes.
- **Severity**: **HIGH** — clicking Sandbox or Leaderboard navigates to a blank/404 page.
- **Fix applied**: Removed `Leaderboard` and `Sandbox` entries from TopNav nav tabs. App.tsx routes verified to match TopNav links.

---

## Claim 3: Pyodide / execution model

- **Claim**: Pyodide does not exist in the project. User code runs through subprocess.run on Vercel server, not in browser.
- **Verified**: **PARTIALLY FALSE** (the claim is incorrect)
- **Files inspected**:
  - `frontend/src/components/CodePlayground.tsx` lines 25-33 — Pyodide IS loaded from CDN (`https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js`) and Python runs IN THE BROWSER via `window.loadPyodide()` and `pyodide.runPython()`.
  - `api/index.py` lines 291-345 — server-side quest/mission checking DOES use `subprocess.run` on Vercel to execute Python code.
  - `README.md` line 61 — accurately states "Pyodide (WebAssembly — Python в браузере)" as the interpreter for the code playground.
  - `README.md` line 182 — accurately describes CodePlayground as using Pyodide.
- **Actual architecture**: **Dual execution model** — (1) student code playground runs via Pyodide in the browser (frontend); (2) quest/mission test-case verification runs via subprocess.run on the Vercel server (backend). Both are real.
- **Severity**: **LOW** (the claim was incorrect; no fix needed for the architecture itself, but documentation should clarify the dual model)
- **Fix applied**: Created `docs/EXECUTION_MODEL.md` documenting both execution paths with safety constraints and restrictions. No false browser-execution claims found in code; README is accurate.

---

## Claim 4: Content gaps — lesson ordering, numbering, coverage

### Sub-claim 4a: Lesson IDs 5-5 and 5-6 missing

- **Claim**: Lesson IDs 5-5 and 5-6 are missing.
- **Verified**: **TRUE**
- **Files inspected**: `api/lessons.json` — 92 lessons total. Part 5 has lessons: 5-1, 5-2, 5-3, 5-4, 5-7. IDs 5-5 and 5-6 do not exist.
- **Severity**: **MEDIUM** — gap of 2 lesson IDs with no metadata explaining why.
- **Fix applied**: Documented intentional gap policy. Added metadata comment in gap documentation. These slots are reserved for future content (file I/O and classes/OOP).

### Sub-claim 4b: Lesson 3-41 appears after 4-31

- **Claim**: Lesson 3-41 appears after 4-31 in the JSON array.
- **Verified**: **TRUE**
- **Files inspected**: `api/lessons.json` — 4-31 is at array index 85, 3-41 is at index 86. This means a Part 3 lesson appears after Part 4 lessons in display order.
- **Severity**: **HIGH** — students in Part 4 would see a Part 3 lesson inserted unexpectedly.
- **Fix applied**: Moved lesson 3-41 to before 4-31 (after 3-40) in the JSON ordering, maintaining Part 3 → Part 4 → Part 5 sequence.

### Sub-claim 4c: File I/O not covered

- **Claim**: File I/O is not covered in the course.
- **Verified**: **TRUE**
- **Files inspected**: All 92 lesson titles in `api/lessons.json`. No lesson covers file reading/writing (`open()`, `read()`, `write()`, `file` operations).
- **Severity**: **MEDIUM** — file I/O is a fundamental Python topic. Marked as planned future module in gap documentation.
- **Fix applied**: Documented as out-of-scope / planned future content.

### Sub-claim 4d: Class/OOP not covered

- **Claim**: Classes/OOP are not covered in the course.
- **Verified**: **TRUE**
- **Files inspected**: All 92 lesson titles in `api/lessons.json`. No lesson covers classes, objects, OOP.
- **Severity**: **MEDIUM** — classes are an intermediate Python topic. Marked as planned future module.
- **Fix applied**: Documented as out-of-scope / planned future content.

---

## Summary

| # | Claim | Verified | Severity | Fix |
|---|-------|----------|----------|-----|
| 1 | Turso missing from root requirements | TRUE | CRITICAL | Added dependency, fail-closed in production |
| 2 | Dead nav links | TRUE | HIGH | Removed Sandbox/Leaderboard from TopNav |
| 3 | Pyodide doesn't exist / only subprocess | FALSE | LOW | Documented dual execution model |
| 4a | Lesson IDs 5-5, 5-6 missing | TRUE | MEDIUM | Documented intentional gap |
| 4b | Lesson 3-41 after 4-31 | TRUE | HIGH | Reordered JSON |
| 4c | File I/O not covered | TRUE | MEDIUM | Documented as planned future module |
| 4d | Class/OOP not covered | TRUE | MEDIUM | Documented as planned future module |
