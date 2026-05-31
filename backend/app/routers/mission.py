import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/mission", tags=["mission"])

_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "lessons.json"


def _load_lessons() -> list[dict[str, Any]]:
    with open(_DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


class MissionSubmit(BaseModel):
    lesson_id: str
    code: str


_FORBIDDEN_IMPORTS = [
    "import os", "import sys", "import subprocess",
    "import socket", "__import__", "exec(", "eval(",
    "import shutil", "import pathlib", "import requests",
]


@router.post("/check")
def check_mission(body: MissionSubmit) -> dict[str, Any]:
    lessons = _load_lessons()
    lesson = next((x for x in lessons if x["id"] == body.lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    mission = lesson.get("mission")
    if not mission:
        raise HTTPException(status_code=400, detail="No mission in this lesson")

    expected = mission["expected_output"].strip()

    code_lower = body.code.lower()
    for forbidden in _FORBIDDEN_IMPORTS:
        if forbidden in code_lower:
            return {
                "correct": False,
                "actual_output": None,
                "expected_output": expected,
                "error": "Использование запрещённых модулей не допускается",
            }

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(body.code)
            tmp_path = f.name

        # Try python first, fall back to python3
        py_cmd = "python3"
        try:
            subprocess.run(["python", "--version"], capture_output=True, timeout=2)
            py_cmd = "python"
        except Exception:
            pass

        result = subprocess.run(
            [py_cmd, tmp_path],
            capture_output=True,
            text=True,
            timeout=5,
        )

        actual = result.stdout.strip()
        stderr = result.stderr.strip()
        first_line = actual.split("\n")[0] if actual else ""
        correct = first_line == expected or actual == expected

        return {
            "correct": correct,
            "actual_output": actual,
            "expected_output": expected,
            "error": stderr if not correct and stderr else None,
        }
    except subprocess.TimeoutExpired:
        return {
            "correct": False,
            "actual_output": None,
            "expected_output": expected,
            "error": "Превышено время выполнения (5 сек). Проверь, нет ли бесконечного цикла",
        }
    except Exception as e:
        return {
            "correct": False,
            "actual_output": None,
            "expected_output": expected,
            "error": str(e),
        }
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
