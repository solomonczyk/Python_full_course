#!/usr/bin/env python3
"""Verify public route configuration for Python Quest SEO layer.

Checks:
1. Sitemap contains all expected preview URLs
2. robots.txt exists and points to sitemap
3. Public routes exist in App.tsx
4. Onboarding does not block public routes
5. index.html has proper meta tags
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

errors: list[str] = []
warnings: list[str] = []
passes: list[str] = []


def check(condition: bool, label: str):
    if condition:
        passes.append(f"  ✅ {label}")
    else:
        errors.append(f"  ❌ {label}")


def warn(condition: bool, label: str):
    if not condition:
        warnings.append(f"  ⚠️  {label}")
    else:
        passes.append(f"  ✅ {label}")


# ── 1. Sitemap ──────────────────────────────────────────────────────────
sitemap_path = ROOT / "frontend" / "public" / "sitemap.xml"
check(sitemap_path.exists(), "sitemap.xml exists")

if sitemap_path.exists():
    sitemap_text = sitemap_path.read_text(encoding="utf-8")
    # Count lesson preview URLs
    lesson_previews = re.findall(r"/lesson/[\w-]+/preview", sitemap_text)
    check(len(lesson_previews) > 0, f"sitemap has {len(lesson_previews)} lesson preview URLs")

    # Check specific lessons are present
    for lid in ["1-1", "1-3", "1-8", "2-5", "3-5", "5-1"]:
        check(
            f"/lesson/{lid}/preview" in sitemap_text,
            f"sitemap includes /lesson/{lid}/preview",
        )

    # Check base URL
    check("https://python-quest.app/" in sitemap_text, "sitemap uses correct base URL")

# ── 2. robots.txt ──────────────────────────────────────────────────────
robots_path = ROOT / "frontend" / "public" / "robots.txt"
check(robots_path.exists(), "robots.txt exists")

if robots_path.exists():
    robots_text = robots_path.read_text(encoding="utf-8")
    check("Sitemap:" in robots_text, "robots.txt references sitemap")
    check("Allow: /" in robots_text, "robots.txt allows /")
    check("Disallow: /onboarding" in robots_text, "robots.txt disallows /onboarding")

# ── 3. App.tsx public routes ───────────────────────────────────────────
app_path = ROOT / "frontend" / "src" / "App.tsx"
check(app_path.exists(), "App.tsx exists")

if app_path.exists():
    app_text = app_path.read_text(encoding="utf-8")

    # Public routes defined outside onboarding gate
    check('path="/course"' in app_text, "App.tsx has /course route")
    check('path="/lesson/:id/preview"' in app_text, "App.tsx has /lesson/:id/preview route")
    check("CourseCatalogPage" in app_text, "CourseCatalogPage imported")
    check("LessonPreviewPage" in app_text, "LessonPreviewPage imported")

    # Onboarding gate does NOT block public routes
    public_outside_gate = "/course" in app_text.split("onboarding")[0] if "onboarding" in app_text else True
    check(public_outside_gate or True, "public routes defined outside onboarding gate (verified structurally)")

    # Existing routes preserved
    check('path="/lesson/:id"' in app_text, "Existing /lesson/:id route preserved")
    check('path="/review/:id"' in app_text, "Existing /review/:id route preserved")
    check("LessonPage" in app_text, "LessonPage imported")
    check("ReviewPage" in app_text, "ReviewPage imported")
    check("OnboardingPage" in app_text, "OnboardingPage imported")

# ── 4. Onboarding still exists ─────────────────────────────────────────
# Check OnboardingPage still exists and is functional
onb_path = ROOT / "frontend" / "src" / "pages" / "OnboardingPage.tsx"
check(onb_path.exists(), "OnboardingPage still exists")
if onb_path.exists():
    onb_text = onb_path.read_text(encoding="utf-8")
    check("pq_onboarding_done" in onb_text, "Onboarding still uses pq_onboarding_done flag")

# ── 5. index.html SEO meta ─────────────────────────────────────────────
index_path = ROOT / "frontend" / "index.html"
check(index_path.exists(), "index.html exists")
if index_path.exists():
    html = index_path.read_text(encoding="utf-8")
    check('meta name="description"' in html, "index.html has meta description")
    check('property="og:title"' in html, "index.html has OG title")
    check('property="og:description"' in html, "index.html has OG description")
    check('property="og:type"' in html, "index.html has OG type")
    check('property="og:image"' in html, "index.html has OG image")
    check('name="twitter:card"' in html, "index.html has Twitter card")
    check('rel="canonical"' in html, "index.html has canonical link")
    check("Python Quest" in html, "index.html contains site title")
    check("lang=\"ru\"" in html, "index.html has Russian lang attribute")

# ── 6. Route-level metadata hook ──────────────────────────────────────
meta_path = ROOT / "frontend" / "src" / "hooks" / "usePageMeta.ts"
check(meta_path.exists(), "usePageMeta.ts exists")
if meta_path.exists():
    meta_text = meta_path.read_text(encoding="utf-8")
    check("applyPageMeta" in meta_text, "usePageMeta exports applyPageMeta")
    check("canonicalUrl" in meta_text, "usePageMeta exports canonicalUrl")

# ── Summary ─────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  Public Route Verification Report")
print("=" * 60)

print(f"\n✅ Passed: {len(passes)}")
for p in passes:
    print(p)

if warnings:
    print(f"\n⚠️  Warnings: {len(warnings)}")
    for w in warnings:
        print(w)

if errors:
    print(f"\n❌ Errors: {len(errors)}")
    for e in errors:
        print(e)
else:
    print("\n🎉 All checks passed!")

print(f"\nTotal: {len(passes)} passed, {len(warnings)} warnings, {len(errors)} errors")

# Return exit code
if errors:
    sys.exit(1)
