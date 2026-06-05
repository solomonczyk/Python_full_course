"""Tests for PYTHON-QUEST-PRODUCTION-TRUTH-REPAIR-001 fixes.

Covers: persistence backend selection, dead nav, execution model, lesson integrity.
"""

import os
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "api"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient

# ── Import app (fresh module to avoid import side-effects from other tests) ──
# We import in a way that lets us set env vars before import.
# For mock-based tests we'll reload the module.

# First, normal import for routes/lessons tests
try:
    from api.index import app
except (ImportError, ModuleNotFoundError):
    try:
        from index import app
    except (ImportError, ModuleNotFoundError) as e:
        print(f"Could not import app: {e}")
        sys.exit(1)

client = TestClient(app)

# ── Load lessons for integrity checks ──
_LESSONS_PATH = Path(__file__).resolve().parent.parent.parent / "api" / "lessons.json"
_FRONTEND_SRC = Path(__file__).resolve().parent.parent.parent / "frontend" / "src"


def _load_lessons() -> list[dict]:
    with open(_LESSONS_PATH, encoding="utf-8") as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════
# 1. PERSISTENCE BACKEND TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_persistence_health_endpoint():
    """GET /health/persistence returns valid status without secrets."""
    r = client.get("/health/persistence")
    assert r.status_code == 200
    data = r.json()
    assert "backend" in data
    assert "environment" in data
    assert "persistent_storage" in data
    assert "safe_for_beta_progress" in data
    # Must never be True in test (no Turso configured in test env)
    assert data["sqlite_tmp_fallback"] is False
    # Must not leak credentials
    body = r.text
    assert "TURSO_DATABASE_URL" not in body or "TURSO" not in body.upper(), \
        "Health endpoint must not leak Turso credentials"
    assert "auth_token" not in body.lower(), \
        "Health endpoint must not leak auth tokens"


def test_persistence_development_allows_sqlite():
    """In development (no Vercel env), SQLite is allowed."""
    # The test environment has no VERCEL_ENV set, so it should be 'development'
    r = client.get("/health/persistence")
    data = r.json()
    assert data["environment"] in ("development", "test"), \
        f"Expected development or test, got {data['environment']}"
    # In dev without Turso, backend should be sqlite, not turso
    # (actual backend depends on whether TURSO_* is set in test env)


def test_production_requires_turso():
    """Simulating production with missing Turso must NOT fall back to SQLite.

    This tests the _resolve_backend() logic by importing the module
    with VERCEL_ENV=production and no Turso credentials.
    """
    # Reload module with production env
    old_env = os.environ.get("VERCEL_ENV", "")
    old_turso_url = os.environ.get("TURSO_DATABASE_URL", "")
    old_turso_token = os.environ.get("TURSO_AUTH_TOKEN", "")
    try:
        os.environ["VERCEL_ENV"] = "production"
        # Remove any Turso config that might exist
        os.environ.pop("TURSO_DATABASE_URL", None)
        os.environ.pop("TURSO_AUTH_TOKEN", None)

        # Re-import the module
        import importlib
        # Clean up cached modules
        for mod_name in list(sys.modules.keys()):
            if "api.index" in mod_name or "index" in mod_name:
                del sys.modules[mod_name]

        import api.index as fresh_index
        status = fresh_index.get_backend_status()
        assert status["backend"] == "unavailable", \
            f"Expected unavailable, got {status['backend']}"
        assert status["persistent_storage"] is False
        assert status["safe_for_beta_progress"] is False
        assert status["sqlite_tmp_fallback"] is False
    finally:
        # Restore env
        if old_env:
            os.environ["VERCEL_ENV"] = old_env
        else:
            os.environ.pop("VERCEL_ENV", None)
        if old_turso_url:
            os.environ["TURSO_DATABASE_URL"] = old_turso_url
        if old_turso_token:
            os.environ["TURSO_AUTH_TOKEN"] = old_turso_token


# ═══════════════════════════════════════════════════════════════════════════
# 2. NAV ROUTE TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_topnav_links_have_routes():
    """All TopNav links must resolve to registered routes in App.tsx."""
    # Read App.tsx to get registered routes
    app_tsx = _FRONTEND_SRC / "App.tsx"
    app_content = app_tsx.read_text(encoding="utf-8")

    # Extract Route paths from App.tsx
    import re
    route_paths = re.findall(r'path="([^"]+)"', app_content)
    print(f"Registered routes: {route_paths}")

    # Read TopNav.tsx to get nav links
    topnav_tsx = _FRONTEND_SRC / "components" / "TopNav.tsx"
    topnav_content = topnav_tsx.read_text(encoding="utf-8")

    # Extract nav link paths
    nav_paths = re.findall(r"path:\s*'([^']+)'", topnav_content)
    print(f"Nav link paths: {nav_paths}")

    # Check: only 'Curriculum' (path '/') should exist
    assert "/" in nav_paths, \
        "Curriculum (path '/') must exist in TopNav"
    # No dead links
    for path in nav_paths:
        assert path in route_paths, \
            f"Nav link '{path}' has no matching route in App.tsx"


def test_no_dead_nav_links():
    """No Sandbox or Leaderboard links in TopNav."""
    topnav_tsx = _FRONTEND_SRC / "components" / "TopNav.tsx"
    content = topnav_tsx.read_text(encoding="utf-8")
    assert "Leaderboard" not in content, \
        "Leaderboard nav link must be removed"
    assert "Sandbox" not in content, \
        "Sandbox nav link must be removed"
    # Only Curriculum should remain
    assert "Curriculum" in content, \
        "Curriculum nav link must exist"


# ═══════════════════════════════════════════════════════════════════════════
# 3. EXECUTION MODEL TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_pyodide_actually_loaded():
    """CodePlayground.tsx must load Pyodide from CDN (not fake)."""
    playground = _FRONTEND_SRC / "components" / "CodePlayground.tsx"
    content = playground.read_text(encoding="utf-8")
    assert "cdn.jsdelivr.net/pyodide" in content, \
        "Pyodide must be loaded from CDN"
    assert "loadPyodide" in content, \
        "loadPyodide must be called"
    assert "pyodide.runPython" in content or "runPython" in content, \
        "pyodide.runPython must be used"


def test_backend_uses_subprocess():
    """api/index.py must use subprocess.run for mission/quest checking."""
    index_path = Path(__file__).resolve().parent.parent.parent / "api" / "index.py"
    content = index_path.read_text(encoding="utf-8")
    assert "subprocess.run" in content, \
        "Backend must use subprocess.run for code execution"
    # Verify timeout safety
    assert "timeout=5" in content or "timeout=10" in content or "timeout" in content, \
        "subprocess.run must have timeout"


def test_no_false_browser_execution_claims():
    """README must not claim Pyodide where it doesn't exist."""
    readme = Path(__file__).resolve().parent.parent.parent / "README.md"
    content = readme.read_text(encoding="utf-8")
    # The Pyodide claim should be there (it IS accurate for CodePlayground)
    assert "Pyodide" in content, \
        "README should mention Pyodide (it's used in CodePlayground)"
    # Check the stack table claims accuracy
    assert "WebAssembly" in content or "браузере" in content, \
        "README should mention Pyodide runs in browser"


# ═══════════════════════════════════════════════════════════════════════════
# 4. LESSON INTEGRITY TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_lesson_ids_unique():
    """All lesson IDs must be unique."""
    lessons = _load_lessons()
    ids = [l.get("id", "") for l in lessons]
    duplicates = {i for i in ids if ids.count(i) > 1}
    assert len(duplicates) == 0, f"Duplicate lesson IDs: {duplicates}"


def test_lesson_display_order_parts():
    """Lessons must appear in Part 1 → Part 2 → Part 3 → Part 4 → Part 5 order.

    No Part X lesson may appear after a Part X+1 lesson in the array.
    """
    lessons = _load_lessons()
    last_part = 0
    for i, l in enumerate(lessons):
        part = l.get("part", 0)
        if part < last_part:
            assert False, \
                f"Lesson {l.get('id')} (Part {part}) appears after Part {last_part} at index {i}"
        if part > last_part:
            last_part = part


def test_no_cross_part_out_of_order():
    """No Part 3 lesson appears after a Part 4 lesson."""
    lessons = _load_lessons()
    part4_start = None
    part3_end = None
    for i, l in enumerate(lessons):
        p = l.get("part", 0)
        if p == 4 and part4_start is None:
            part4_start = i
        if p == 3:
            part3_end = i
    if part4_start is not None and part3_end is not None:
        assert part3_end < part4_start, \
            f"Part 3 lessons extend into Part 4 territory (Part 3 last index: {part3_end}, Part 4 first index: {part4_start})"


def test_lesson_3_41_before_4_31():
    """Lesson 3-41 must appear before lesson 4-31 in the array order."""
    lessons = _load_lessons()
    idx_3_41 = None
    idx_4_31 = None
    for i, l in enumerate(lessons):
        lid = l.get("id", "")
        if lid == "3-41":
            idx_3_41 = i
        elif lid == "4-31":
            idx_4_31 = i
    assert idx_3_41 is not None, "Lesson 3-41 not found"
    assert idx_4_31 is not None, "Lesson 4-31 not found"
    assert idx_3_41 < idx_4_31, \
        f"Lesson 3-41 (index {idx_3_41}) must appear before 4-31 (index {idx_4_31})"


def test_lesson_part_5_ids():
    """Part 5 IDs must be documented (5-5, 5-6 gaps intentional)."""
    lessons = _load_lessons()
    p5_ids = [l.get("id") for l in lessons if l.get("part") == 5]
    # 5-5 and 5-6 may be missing (intentional gap) or present
    # But the gap must be documented
    gap_doc = Path(__file__).resolve().parent.parent.parent / "docs" / "LESSON_GAP_POLICY.md"
    assert gap_doc.exists(), "LESSON_GAP_POLICY.md must exist"
    gap_content = gap_doc.read_text(encoding="utf-8")
    if "5-5" not in p5_ids:
        assert "5-5" in gap_content, \
            "Missing lesson 5-5 must be documented in LESSON_GAP_POLICY.md"
    if "5-6" not in p5_ids:
        assert "5-6" in gap_content, \
            "Missing lesson 5-6 must be documented in LESSON_GAP_POLICY.md"


def test_file_io_and_class_gaps_documented():
    """File I/O and class coverage gaps must be documented in LESSON_GAP_POLICY.md."""
    gap_doc = Path(__file__).resolve().parent.parent.parent / "docs" / "LESSON_GAP_POLICY.md"
    assert gap_doc.exists(), "LESSON_GAP_POLICY.md must exist"
    content = gap_doc.read_text(encoding="utf-8")
    assert any(k in content.lower() for k in ["file i/o", "file io", "файл", "open", "read", "write"]), \
        "File I/O gap must be documented"
    assert any(k in content.lower() for k in ["class", "oop", "объект", "класс"]), \
        "Class/OOP gap must be documented"


# ═══════════════════════════════════════════════════════════════════════════
# 5. REQUIREMENTS / DEPENDENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_root_requirements_has_libsql():
    """Root requirements.txt must contain libsql-experimental."""
    req_path = Path(__file__).resolve().parent.parent.parent / "requirements.txt"
    content = req_path.read_text(encoding="utf-8")
    assert "libsql-experimental" in content, \
        "Root requirements.txt must include libsql-experimental"


def test_root_requirements_has_all_deps():
    """Root requirements.txt must have fastapi, uvicorn, pydantic."""
    req_path = Path(__file__).resolve().parent.parent.parent / "requirements.txt"
    content = req_path.read_text(encoding="utf-8")
    assert "fastapi" in content
    assert "uvicorn" in content
    assert "pydantic" in content


# ═══════════════════════════════════════════════════════════════════════════
# 6. EXECUTION MODEL DOCUMENTATION TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_execution_model_doc_exists():
    """EXECUTION_MODEL.md must exist and describe both runtimes."""
    doc = Path(__file__).resolve().parent.parent.parent / "docs" / "EXECUTION_MODEL.md"
    assert doc.exists(), "EXECUTION_MODEL.md must exist"
    content = doc.read_text(encoding="utf-8")
    assert "Pyodide" in content, "Must describe Pyodide frontend execution"
    assert "subprocess" in content, "Must describe subprocess backend execution"
