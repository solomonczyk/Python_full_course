#!/usr/bin/env python3
"""Check persistence backend status — run locally or as a diagnostic."""

import json
import os
import sys
from pathlib import Path

# Ensure we can import from api
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE / ".."))

# Simulate environment (import api/index.py sets these from os.environ)
os.environ.setdefault("VERCEL_ENV", "development")
os.environ.setdefault("APP_ENV", "development")

# Force re-import
for mod in list(sys.modules.keys()):
    if "index" in mod or "api.index" in mod:
        del sys.modules[mod]

# Remove cached .pyc
import importlib.util
spec = importlib.util.spec_from_file_location("api.index", str(_HERE / ".." / "api" / "index.py"))
if spec and spec.loader:
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def check():
    """Print persistence backend status."""
    try:
        status = module.get_backend_status()
    except AttributeError as e:
        print(json.dumps({
            "backend": "error",
            "environment": os.environ.get("VERCEL_ENV", "unknown"),
            "persistent_storage": False,
            "sqlite_tmp_fallback": False,
            "safe_for_beta_progress": False,
            "error": f"get_backend_status not available: {e}",
        }, ensure_ascii=False, indent=2))
        return

    print(json.dumps(status, ensure_ascii=False, indent=2))

    # Summary
    if status.get("backend") == "turso":
        print("\n✅ Turso is active — progress is persistent.")
    elif status.get("backend") == "sqlite":
        print("\n⚠️  SQLite is active (development mode) — local progress only.")
    else:
        print(f"\n❌ Backend unavailable: {status.get('error', 'unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    check()
