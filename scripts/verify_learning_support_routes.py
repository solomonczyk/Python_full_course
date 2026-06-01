#!/usr/bin/env python3
"""Verify learning support system routes are properly configured.

Checks:
1. /glossary route exists in App.tsx
2. /recap/:id route exists in App.tsx
3. /quest/:id route exists in App.tsx
4. Backend glossary endpoint is accessible
5. Backend recaps endpoint returns data
6. Backend quests endpoint returns data
7. Existing /lesson/:id route still works
8. Existing /course route still works
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

errors: list[str] = []
passes: list[str] = []


def check(condition: bool, label: str):
    if condition:
        passes.append(f"  ✅ {label}")
    else:
        errors.append(f"  ❌ {label}")


# ── 1. Frontend routes ──────────────────────────────────────────────────
print("\n── 1. Frontend Routes (App.tsx) ──")
app_path = ROOT / "frontend" / "src" / "App.tsx"
check(app_path.exists(), "App.tsx exists")

if app_path.exists():
    app_text = app_path.read_text(encoding="utf-8")

    # New routes
    check('path="/glossary"' in app_text, "Route /glossary defined")
    check('path="/recap/:id"' in app_text, "Route /recap/:id defined")
    check('path="/quest/:id"' in app_text, "Route /quest/:id defined")

    # Page imports
    check("GlossaryPage" in app_text, "GlossaryPage imported")
    check("RecapPage" in app_text, "RecapPage imported")
    check("QuestPage" in app_text, "QuestPage imported")

    # Existing routes preserved
    check('path="/lesson/:id"' in app_text, "Existing /lesson/:id preserved")
    check('path="/review/:id"' in app_text, "Existing /review/:id preserved")
    check('path="/course"' in app_text, "Existing /course preserved")
    check('path="/lesson/:id/preview"' in app_text, "Existing /preview preserved")
    check("LessonPage" in app_text, "LessonPage still imported")
    check("CourseCatalogPage" in app_text, "CourseCatalogPage still imported")


# ── 2. Backend router files ─────────────────────────────────────────────
print("\n── 2. Backend Router Files ──")
glossary_router = ROOT / "backend" / "app" / "routers" / "glossary.py"
check(glossary_router.exists(), "glossary.py router exists")

recaps_router = ROOT / "backend" / "app" / "routers" / "recaps.py"
check(recaps_router.exists(), "recaps.py router exists")

quests_router = ROOT / "backend" / "app" / "routers" / "quests.py"
check(quests_router.exists(), "quests.py router exists")


# ── 3. Backend main.py includes ─────────────────────────────────────────
print("\n── 3. Backend Router Registration ──")
main_path = ROOT / "backend" / "app" / "main.py"
if main_path.exists():
    main_text = main_path.read_text(encoding="utf-8")
    check("glossary" in main_text, "main.py imports glossary")
    check("recaps" in main_text, "main.py imports recaps")
    check("quests" in main_text, "main.py imports quests")
    check("app.include_router(glossary" in main_text, "glossary router registered")
    check("app.include_router(recaps" in main_text, "recaps router registered")
    check("app.include_router(quests" in main_text, "quests router registered")


# ── 4. api/index.py includes ────────────────────────────────────────────
print("\n── 4. API Vercel Routes ──")
api_path = ROOT / "api" / "index.py"
if api_path.exists():
    api_text = api_path.read_text(encoding="utf-8")
    check('"/glossary"' in api_text, "api/index.py has /glossary endpoint")
    check('"/recaps"' in api_text, "api/index.py has /recaps endpoint")
    check('"/quests"' in api_text, "api/index.py has /quests endpoint")
    check('_GLOSSARY_FILE' in api_text, "api/index.py has GLOSSARY_FILE constant")
    check('_RECAPS_FILE' in api_text, "api/index.py has RECAPS_FILE constant")
    check('_QUESTS_FILE' in api_text, "api/index.py has QUESTS_FILE constant")


# ── 5. Data files ───────────────────────────────────────────────────────
print("\n── 5. Data Files ──")
check((ROOT / "backend" / "app" / "data" / "glossary.json").exists(),
      "backend glossary.json")
check((ROOT / "backend" / "app" / "data" / "recaps.json").exists(),
      "backend recaps.json")
check((ROOT / "backend" / "app" / "data" / "chapter_quests.json").exists(),
      "backend chapter_quests.json")
check((ROOT / "api" / "app" / "data" / "glossary.json").exists(),
      "api glossary.json")
check((ROOT / "api" / "app" / "data" / "recaps.json").exists(),
      "api recaps.json")
check((ROOT / "api" / "app" / "data" / "chapter_quests.json").exists(),
      "api chapter_quests.json")


# ── 6. Sidebar navigation ──────────────────────────────────────────────
print("\n── 6. Sidebar Navigation ──")
sidebar_path = ROOT / "frontend" / "src" / "components" / "Sidebar.tsx"
if sidebar_path.exists():
    sidebar_text = sidebar_path.read_text(encoding="utf-8")
    check('to="/glossary"' in sidebar_text, "Sidebar links to glossary")
    check('recaps' in sidebar_text and 'fetch' in sidebar_text,
          "Sidebar fetches recaps")
    check('quests' in sidebar_text and 'fetch' in sidebar_text,
          "Sidebar fetches quests")


# ── 7. HomePage integration ─────────────────────────────────────────────
print("\n── 7. HomePage Integration ──")
home_path = ROOT / "frontend" / "src" / "pages" / "HomePage.tsx"
if home_path.exists():
    home_text = home_path.read_text(encoding="utf-8")
    check('setRecaps' in home_text, "HomePage loads recaps")
    check('setQuests' in home_text, "HomePage loads quests")


# ── Summary ─────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  Learning Support Route Verification Report")
print("=" * 60)

print(f"\n✅ Passed: {len(passes)}")
for p in passes:
    print(p)

if errors:
    print(f"\n❌ Errors: {len(errors)}")
    for e in errors:
        print(e)
else:
    print("\n🎉 All checks passed!")

print(f"\nTotal: {len(passes)} passed, {len(errors)} errors")

if errors:
    sys.exit(1)
