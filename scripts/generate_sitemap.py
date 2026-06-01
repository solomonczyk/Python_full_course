#!/usr/bin/env python3
"""Generate sitemap.xml for Python Quest.

Since the app is a client-side SPA (Vite + React), search engines that do
not execute JS will not discover routes via crawling.  This script produces
a static sitemap.xml with all public routes and lesson preview pages.

Usage:
    python scripts/generate_sitemap.py

Output:
    frontend/public/sitemap.xml
"""

import json
import sys
from datetime import date
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Add backend to path so we can load lesson data
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

BASE_URL = "https://python-quest.app"

# Lessons JSON path
LESSONS_PATH = (
    Path(__file__).resolve().parent.parent
    / "backend" / "app" / "data" / "lessons.json"
)

# Static public routes (not requiring onboarding)
STATIC_ROUTES = [
    {"path": "/", "changefreq": "weekly", "priority": "1.0"},
    {"path": "/course", "changefreq": "daily", "priority": "0.9"},
]


def load_lessons() -> list[dict]:
    """Load lesson summaries from the backend data file."""
    with open(LESSONS_PATH, encoding="utf-8") as f:
        lessons = json.load(f)
    return lessons


def build_sitemap(lessons: list[dict]) -> str:
    """Generate a sitemap XML string."""
    today = date.today().isoformat()

    urlset = Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    def add_url(path: str, changefreq: str = "monthly", priority: str = "0.5"):
        url = SubElement(urlset, "url")
        loc = SubElement(url, "loc")
        loc.text = f"{BASE_URL}{path}"
        lastmod = SubElement(url, "lastmod")
        lastmod.text = today
        cf = SubElement(url, "changefreq")
        cf.text = changefreq
        pri = SubElement(url, "priority")
        pri.text = priority

    # Static routes
    for route in STATIC_ROUTES:
        add_url(route["path"], route["changefreq"], route["priority"])

    # Lesson preview pages
    for lesson in lessons:
        lesson_id = lesson.get("id", "")
        if not lesson_id or not lesson.get("mission"):
            continue  # only lessons with a mission get preview pages
        add_url(
            f"/lesson/{lesson_id}/preview",
            changefreq="monthly",
            priority="0.7",
        )

    # Pretty-print XML
    rough = tostring(urlset, encoding="unicode")
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ")


def main():
    lessons = load_lessons()
    xml = build_sitemap(lessons)

    # Count lesson preview URLs
    lesson_count = sum(
        1 for item in lessons if item.get("id") and item.get("mission")
    )
    total_urls = len(STATIC_ROUTES) + lesson_count

    out_path = (
        Path(__file__).resolve().parent.parent
        / "frontend" / "public" / "sitemap.xml"
    )
    out_path.write_text(xml, encoding="utf-8")

    print(f"✅ Sitemap generated: {out_path}")
    print(f"   Static routes: {len(STATIC_ROUTES)}")
    print(f"   Lesson previews: {lesson_count}")
    print(f"   Total URLs: {total_urls}")


if __name__ == "__main__":
    main()
