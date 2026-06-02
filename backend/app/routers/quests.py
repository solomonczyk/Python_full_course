import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/quests", tags=["quests"])

_DATA_FILE = Path(__file__).parent.parent / "data" / "quests.json"
_cache: list[dict[str, Any]] | None = None


def _load_quests() -> list[dict[str, Any]]:
    global _cache
    if _cache is None:
        with open(_DATA_FILE, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def invalidate_cache() -> None:
    global _cache
    _cache = None


class QuestCheckRequest(BaseModel):
    code: str


_FORBIDDEN_IMPORTS = [
    "import os", "import sys", "import subprocess",
    "import socket", "__import__", "exec(", "eval(",
    "import shutil", "import pathlib", "import requests",
]


@router.get("")
def list_quests() -> list[dict[str, Any]]:
    """Return all quests (summary fields)."""
    quests = _load_quests()
    SUMMARY_FIELDS = ("id", "part", "title")
    return [
        {k: quest[k] for k in SUMMARY_FIELDS if k in quest}
        | ({"is_capstone": True} if quest.get("is_capstone") else {})
        for quest in quests
    ]


@router.get("/{quest_id}")
def get_quest(quest_id: str) -> dict[str, Any]:
    """Return a single quest by ID."""
    quests = _load_quests()
    for quest in quests:
        if quest["id"] == quest_id:
            return quest
    raise HTTPException(status_code=404, detail=f"Quest '{quest_id}' not found")


@router.post("/{quest_id}/check")
def check_quest(quest_id: str, body: QuestCheckRequest) -> dict[str, Any]:
    """Run submitted code against all test cases for a quest."""
    quests = _load_quests()
    quest = next((q for q in quests if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quest '{quest_id}' not found")

    test_cases = quest.get("test_cases", [])
    if not test_cases:
        raise HTTPException(status_code=400, detail="No test cases for this quest")

    code_lower = body.code.lower()
    for forbidden in _FORBIDDEN_IMPORTS:
        if forbidden in code_lower:
            return {
                "quest_id": quest_id,
                "results": [],
                "all_passed": False,
                "error": "Использование запрещённых модулей не допускается",
            }

    results = []
    all_passed = True

    for tc in test_cases:
        tc_input = tc.get("input", "")
        expected = tc.get("expected_contains", [])

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as f:
                f.write(body.code)
                tmp_path = f.name

            py_cmd = "python3"
            try:
                subprocess.run(["python", "--version"], capture_output=True, timeout=2)
                py_cmd = "python"
            except Exception:
                pass

            proc = subprocess.run(
                [py_cmd, tmp_path],
                input=tc_input,
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )

            actual = proc.stdout
            stderr = proc.stderr.strip()

            missing = [e for e in expected if e not in actual]
            passed = len(missing) == 0 and not stderr
            if not passed:
                all_passed = False

            results.append({
                "passed": passed,
                "input": tc_input.strip()[:100],
                "actual_output": actual.strip()[:300] if actual else "",
                "missing_contains": missing,
                "error": stderr[:200] if stderr else None,
            })

        except subprocess.TimeoutExpired:
            all_passed = False
            results.append({
                "passed": False,
                "input": tc_input.strip()[:100],
                "actual_output": "",
                "missing_contains": expected,
                "error": "Превышено время выполнения (5 сек)",
            })
        except Exception as e:
            all_passed = False
            results.append({
                "passed": False,
                "input": tc_input.strip()[:100],
                "actual_output": "",
                "missing_contains": expected,
                "error": str(e)[:200],
            })
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    return {
        "quest_id": quest_id,
        "results": results,
        "all_passed": all_passed,
    }
