"""
Scenario Quality Audit — checks generated scenario fields for:
- Generic fallback overuse
- Tone mismatch
- Content relevance
- Dialogue naturalness
- Connection to the final game

Output: scenario_quality_audit_report.json + human-readable summary
"""

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PROJECT = _HERE.parent
_LESSONS_PATH = _PROJECT / "api" / "app" / "data" / "lessons.json"

# ── Known generic / fallback patterns ────────────────────────────────────────

# Hard fallback pre-topic dialogues (from get_pre_topic_dialogue fallback)
HARD_DIALOGUE_MARKERS = [
    "Мы переходим к новой теме. Всё, что мы учим, пригодится в финальной игре",
    "Новая тема — новый инструмент для твоей игры. Разберёмся по шагам",
    "Продолжаем собирать инструменты для финального проекта. Это важный шаг",
    "В Башне Алгоритмов каждая деталь важна. Эта тема — часть твоего успеха",
    "Давай разберём новую тему шаг за шагом",
    "Обрати внимание на детали в теме",
]

# Hard fallback post-error dialogues
HARD_POST_ERROR_MARKERS = [
    "Ошибки на этом этапе — нормально. Главное — понять причину и исправить",
    "Хорошая новость: ты уже умеешь находить такие ошибки. Практика решает",
    "Чем сложнее код, тем внимательнее нужно быть к деталям",
    "В финальной игре такие ошибки будут стоить ходов. Учись ловить их сейчас",
    "Ошибка найдена — отлично! Теперь ты знаешь, как её избежать",
    "Исправляй и запоминай. В следующий раз будет легче",
]

# Generic game_relevance part fallbacks
GAME_RELEVANCE_FALLBACK_MARKERS = [
    "Для финальной игры: основа",
    "Для финальной игры: тема",
    "Для финальной игры: «",
    "— это фундамент, на котором строится вся игра",
    "добавляет в игру логику и контроль",
    "— инструмент для работы с данными",
    "— часть игровой механики",
    "— ещё один шаг к созданию",
]

# Generic mini_summary fallback patterns
SUMMARY_FALLBACK_MARKERS = [
    "Ты научился основам:",
    "Ты освоил",
    "— полезный инструмент для работы с данными в игре",
    "— ещё один элемент для финальной сборки игры",
    "Продолжаем изучать",
]

# Generic connection_to_game part fallbacks
CONNECTION_FALLBACK_MARKERS = [
    "В финальной игре навыки из темы",
    "В финальной игре знания из темы",
    "В финальной игре «",
    "— это часть игрового цикла финального проекта",
    "Тема «",
    "пригодится в финальной игре",
]

# Generic story_placement fallback
STORY_PLACEMENT_FALLBACK = "Продолжаем путешествие по миру Python."

# Category-level game_relevance fallbacks (acceptable, not ideal)
CATEGORY_RELEVANCE_MARKERS = [
    "работа с числами — основа расчётов",
    "понимание ссылок и изменяемости помогает избежать ошибок",
    "безопасное копирование данных",
    "ключи сортировки нужны для упорядочивания",
    "распаковка делает код чище",
    "поиск максимума/минимума пригодится для анализа статистики",
    "принципы чат-бота — основа игрового цикла",
    "умение управлять задачами пригодится",
    "контроль ввода защищает игру",
    "состояния объектов (флаги, статусы) определяют",
    "чистый и понятный код важнее короткого",
]


def is_generic_fallback(text: str, markers: list[str]) -> bool:
    """Check if text matches any known fallback marker."""
    if not text:
        return True
    return any(m in text for m in markers)


def analyze_field(lessons: list[dict], field: str, markers: list[str]) -> dict:
    """Analyze a single field across all lessons."""
    results = []
    generic_count = 0
    empty_count = 0
    short_count = 0  # < 30 chars
    for l in lessons:
        value = l.get(field)
        lid = l["id"]
        title = l["title"]
        entry = {"id": lid, "title": title}

        if value is None:
            entry["status"] = "MISSING"
            empty_count += 1
            generic_count += 1
            results.append(entry)
            continue

        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        entry["length"] = len(text)

        if len(text) < 30:
            entry["status"] = "TOO_SHORT"
            short_count += 1
        elif is_generic_fallback(text, markers):
            entry["status"] = "GENERIC_FALLBACK"
            generic_count += 1
        else:
            entry["status"] = "OK"

        results.append(entry)

    return {
        "field": field,
        "total": len(lessons),
        "ok": sum(1 for r in results if r.get("status") == "OK"),
        "generic_fallback": generic_count,
        "too_short": short_count,
        "empty": empty_count,
        "details": results,
    }


def check_tone_progression(lessons: list[dict]) -> dict:
    """Check that tone complexity progresses across parts 1-4."""
    part_lessons: dict[int, list[dict]] = {1: [], 2: [], 3: [], 4: []}
    for l in lessons:
        p = l["part"]
        if p in part_lessons:
            part_lessons[p].append(l)

    # Average length per part as a proxy for complexity
    avg_lengths = {}
    for p in [1, 2, 3, 4]:
        pl = part_lessons[p]
        if not pl:
            avg_lengths[p] = 0
            continue
        totals = {"game_relevance": 0, "story_placement": 0, "mini_summary": 0, "connection_to_game": 0}
        for l in pl:
            for f in totals:
                v = l.get(f, "")
                if isinstance(v, str):
                    totals[f] += len(v)
        avg_lengths[p] = {f: round(totals[f] / len(pl), 1) for f in totals}

    return {
        "avg_field_lengths_by_part": avg_lengths,
        "note": "Length should increase from Part 1→4 (more complex topics need more explanation)",
    }


def check_game_connection_quality(lessons: list[dict]) -> dict:
    """Check connection_to_game and game_relevance for quality."""
    game_keywords = ["игр", "башн", "bagus", "багус", "финальн", "проект", "побег", "герой", "комнат", "инвентар", "здоровь", "очк", "команд"]
    weak = []
    for l in lessons:
        conn = l.get("connection_to_game", "") or ""
        relev = l.get("game_relevance", "") or ""
        lid = l["id"]

        # Check if connection mentions anything game-specific
        if isinstance(conn, str) and not any(kw in conn.lower() for kw in game_keywords):
            weak.append({"id": lid, "field": "connection_to_game", "text": conn[:80]})
        if isinstance(relev, str) and not any(kw in relev.lower() for kw in game_keywords):
            weak.append({"id": lid, "field": "game_relevance", "text": relev[:80]})

    return {
        "lessons_with_weak_game_connection": len(weak),
        "weak_entries": weak,
    }


def check_dialogue_quality(lessons: list[dict]) -> dict:
    """Check dialogue fields for quality issues."""
    issues = []
    for l in lessons:
        lid = l["id"]
        for field in ["pre_topic_dialogue", "post_error_dialogue"]:
            lines = l.get(field)
            if not lines:
                continue
            if isinstance(lines, list):
                # Check for very short dialogues (1 line)
                if len(lines) <= 1:
                    issues.append({"id": lid, "field": field, "issue": "too_few_lines", "count": len(lines)})
                # Check if character field is present in all lines
                for i, line in enumerate(lines):
                    if not isinstance(line, dict) or "character" not in line or "text" not in line:
                        issues.append({"id": lid, "field": field, "issue": f"malformed_line_{i}"})
                    elif len(line.get("text", "")) < 10:
                        issues.append({"id": lid, "field": field, "issue": f"line_{i}_too_short", "text": line["text"]})

    return {"total_issues": len(issues), "issues": issues}


def check_story_placement_quality(lessons: list[dict]) -> dict:
    """Check story_placement for relevance."""
    generic_story = []
    for l in lessons:
        sp = l.get("story_placement", "") or ""
        if isinstance(sp, str) and sp == STORY_PLACEMENT_FALLBACK:
            generic_story.append({"id": l["id"], "title": l["title"]})
    return {"generic_story_placements": len(generic_story), "items": generic_story}


def main() -> int:
    if not _LESSONS_PATH.exists():
        print(f"ERROR: lessons.json not found at {_LESSONS_PATH}")
        return 1

    with open(_LESSONS_PATH, encoding="utf-8") as f:
        lessons = json.load(f)

    print(f"Loaded {len(lessons)} lessons. Running quality audit...\n")

    # ── Audit each field ──
    report = {
        "total_lessons": len(lessons),
        "summary": {},
        "field_analyses": {},
        "tone_progression": check_tone_progression(lessons),
        "game_connection_quality": check_game_connection_quality(lessons),
        "dialogue_quality": check_dialogue_quality(lessons),
        "story_placement_quality": check_story_placement_quality(lessons),
        "targeted_fixes": [],
        "verdict": "PENDING",
    }

    field_configs = [
        ("story_placement", STORY_PLACEMENT_FALLBACK),
        ("pre_topic_dialogue", HARD_DIALOGUE_MARKERS),
        ("post_error_dialogue", HARD_POST_ERROR_MARKERS),
        ("game_relevance", GAME_RELEVANCE_FALLBACK_MARKERS + CATEGORY_RELEVANCE_MARKERS),
        ("mini_summary", SUMMARY_FALLBACK_MARKERS),
        ("connection_to_game", CONNECTION_FALLBACK_MARKERS),
    ]

    for field, markers in field_configs:
        analysis = analyze_field(lessons, field, markers if isinstance(markers, list) else [markers])
        report["field_analyses"][field] = analysis
        report["summary"][field] = {
            "ok": analysis["ok"],
            "generic_fallback": analysis["generic_fallback"],
            "too_short": analysis["too_short"],
        }

    # ── Determine verdict ──
    critical = report["dialogue_quality"]["total_issues"]
    weak_conn = report["game_connection_quality"]["lessons_with_weak_game_connection"]
    generic_total = sum(s["generic_fallback"] for s in report["summary"].values())
    total_checks = len(lessons) * 6

    print(f"  Generic fallback occurrences: {generic_total}/{total_checks}")
    print(f"  Dialogue quality issues: {critical}")
    print(f"  Weak game connections: {weak_conn}")

    has_critical = critical > 0 or weak_conn > 4 or (generic_total / total_checks) > 0.3
    report["verdict"] = "NEEDS_FIXES" if has_critical else "ACCEPTED"
    print(f"  Verdict: {report['verdict']}")

    # ── Generate targeted fixes ──
    fixes = []

    # Fix 1: Pre-topic hard fallbacks → more specific
    hard_dialogue_ids = [
        r["id"] for r in report["field_analyses"]["pre_topic_dialogue"]["details"]
        if r.get("status") == "GENERIC_FALLBACK"
    ]
    if hard_dialogue_ids:
        fixes.append({
            "issue": f"{len(hard_dialogue_ids)} lessons with hard fallback pre_topic_dialogue",
            "affected_ids": hard_dialogue_ids,
            "fix": "Add specific dialogue entries to PRE_TOPIC_DIALOGUE_MAP for these topics",
        })

    # Fix 2: Post-error hard fallbacks
    hard_post_ids = [
        r["id"] for r in report["field_analyses"]["post_error_dialogue"]["details"]
        if r.get("status") == "GENERIC_FALLBACK"
    ]
    if hard_post_ids:
        fixes.append({
            "issue": f"{len(hard_post_ids)} lessons with hard fallback post_error_dialogue",
            "affected_ids": hard_post_ids,
            "fix": "Add specific post-error dialogue entries to POST_ERROR_DIALOGUE_MAP",
        })

    # Fix 3: Weak game connections
    weak_conn_ids = [w["id"] for w in report["game_connection_quality"]["weak_entries"]]
    if weak_conn_ids:
        fixes.append({
            "issue": f"{len(weak_conn_ids)} lessons with weak game connection (no game-specific keywords)",
            "affected_ids": weak_conn_ids,
            "fix": "Improve connection_to_game or game_relevance to mention game concepts",
        })

    # Fix 4: Generic game_relevance
    generic_relevance_ids = [
        r["id"] for r in report["field_analyses"]["game_relevance"]["details"]
        if r.get("status") == "GENERIC_FALLBACK"
    ]
    if generic_relevance_ids:
        fixes.append({
            "issue": f"{len(generic_relevance_ids)} lessons with generic game_relevance fallback",
            "affected_ids": generic_relevance_ids,
            "fix": "Add specific game_relevance entries to GAME_RELEVANCE_MAP or CATEGORY-level entries",
        })

    # Fix 5: Generic mini_summary
    generic_summary_ids = [
        r["id"] for r in report["field_analyses"]["mini_summary"]["details"]
        if r.get("status") == "GENERIC_FALLBACK"
    ]
    if generic_summary_ids:
        fixes.append({
            "issue": f"{len(generic_summary_ids)} lessons with generic mini_summary fallback",
            "affected_ids": generic_summary_ids,
            "fix": "Add specific MINI_SUMMARY_MAP entries for these topics",
        })

    # Fix 6: Generic connection_to_game
    generic_conn_ids = [
        r["id"] for r in report["field_analyses"]["connection_to_game"]["details"]
        if r.get("status") == "GENERIC_FALLBACK"
    ]
    if generic_conn_ids:
        fixes.append({
            "issue": f"{len(generic_conn_ids)} lessons with generic connection_to_game fallback",
            "affected_ids": generic_conn_ids,
            "fix": "Add specific CONNECTION_TO_GAME_MAP entries for these topics",
        })

    # Fix 7: Generic story_placement
    generic_story_ids = [s["id"] for s in report["story_placement_quality"]["items"]]
    if generic_story_ids:
        fixes.append({
            "issue": f"{len(generic_story_ids)} lessons with generic story_placement",
            "affected_ids": generic_story_ids,
            "fix": "Add specific STORY_PLACEMENT_MAP entries for these topics",
        })

    report["targeted_fixes"] = fixes

    # ── Short summary ──
    print(f"\n{'='*50}")
    print("  FIELD SUMMARY")
    print(f"{'='*50}")
    for field, markers in field_configs:
        a = report["field_analyses"][field]
        bar_ok = "█" * (a["ok"] // 2)
        bar_fb = "▓" * (a["generic_fallback"] // 2)
        print(f"  {field:<25s} OK:{a['ok']:>3d}  FB:{a['generic_fallback']:>3d}  SHORT:{a['too_short']:>2d}  {bar_ok}{'░' if a['generic_fallback'] > 0 else ''}{bar_fb}")

    print(f"\n  Dialogue quality issues: {report['dialogue_quality']['total_issues']}")
    print(f"  Weak game connections: {report['game_connection_quality']['lessons_with_weak_game_connection']}")
    print(f"  Generic story placements: {report['story_placement_quality']['generic_story_placements']}")
    print(f"\n  TARGETED FIXES: {len(fixes)}")
    for f in fixes:
        print(f"    - {f['issue']}")
    print(f"\n  VERDICT: {report['verdict']}")
    print(f"{'='*50}\n")

    # ── Save report ──
    report_path = _PROJECT / "scenario_quality_audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"  Full report saved to {report_path.resolve()}")
    print()

    return 0 if report["verdict"] == "ACCEPTED" else 1


if __name__ == "__main__":
    sys.exit(main())
