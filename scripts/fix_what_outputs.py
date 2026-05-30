"""
Fix what_outputs blocks that have multiple sequential print() calls
but single-line options. The user can't tell which output is being asked.

Fix: combine into a single print() or use multi-line options.
"""

import json, sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = "api/app/data/lessons.json"
BACKUP = PATH + ".wo_backup"

shutil.copy2(PATH, BACKUP)
print(f"Backup saved to {BACKUP}")

with open(PATH, encoding="utf-8") as f:
    lessons = json.load(f)

fixes = {
    # 1-7: Two comparisons → single print with boolean
    "1-7": {
        "code": "x = 10 == 10\ny = 2 > 5\nprint(x, y)",
        "options": ["True False", "False True", "Ошибка"],
        "correct": "True False",
    },
    # 3-6: Two prints → single comparison (keep bool topic)
    "3-6": {
        "code": "print(5 > 2)",
        "options": ["True", "False", "Ошибка"],
        "correct": "True",
    },
    # 3-9: Two prints of and → single print with expression
    "3-9": {
        "code": "print(True and False)",
        "options": ["False", "True", "Ошибка"],
        "correct": "False",
    },
    # 3-10: Two prints of or → single print
    "3-10": {
        "code": "print(False or True)",
        "options": ["True", "False", "Ошибка"],
        "correct": "True",
    },
    # 3-11: Two prints of not → single print
    "3-11": {
        "code": "print(not True)",
        "options": ["False", "True", "Ошибка"],
        "correct": "False",
    },
    # 3-29: Two prints (pop and list) → single print showing both
    "3-29": {
        "code": "a = [1, 2, 3]\nprint(a.pop(), a)",
        "options": ["3 [1, 2]", "3 [1, 2, 3]", "Ошибка"],
        "correct": "3 [1, 2]",
    },
    # 4-16: Two prints → single focused on sorted behavior
    "4-16": {
        "code": "a = [2, 1]\nb = sorted(a)\nprint(a, b)",
        "options": ["[2, 1] [1, 2]", "[1, 2] [2, 1]", "Ошибка"],
        "correct": "[2, 1] [1, 2]",
    },
    # 4-23: Two prints (== and is) → single showing the key insight
    "4-23": {
        "code": "a = [1]\nb = [1]\nprint(a == b, a is b)",
        "options": ["True False", "False True", "Ошибка"],
        "correct": "True False",
    },
    # ── For-loop fixes: multi-line → single clear value ──
    # 2-5: for i in range(3): print(i) → show range as list
    "2-5": {
        "code": "print(list(range(3)))",
        "options": ["[0, 1, 2]", "[1, 2, 3]", "Ошибка"],
        "correct": "[0, 1, 2]",
    },
    # 2-6: range(2, 5) → show as list
    "2-6": {
        "code": "print(list(range(2, 5)))",
        "options": ["[2, 3, 4]", "[2, 3, 4, 5]", "Ошибка"],
        "correct": "[2, 3, 4]",
    },
    # 3-14: for i in range(2): → range as list
    "3-14": {
        "code": "print(list(range(2)))",
        "options": ["[0, 1]", "[1, 2]", "Ошибка"],
        "correct": "[0, 1]",
    },
    # 3-15: range(3, 6)
    "3-15": {
        "code": "print(list(range(3, 6)))",
        "options": ["[3, 4, 5]", "[3, 4, 5, 6]", "Ошибка"],
        "correct": "[3, 4, 5]",
    },
    # 3-16: range(1, 6, 2)
    "3-16": {
        "code": "print(list(range(1, 6, 2)))",
        "options": ["[1, 3, 5]", "[1, 2, 3, 4, 5]", "Ошибка"],
        "correct": "[1, 3, 5]",
    },
    # 3-17: range(3, 0, -1)
    "3-17": {
        "code": "print(list(range(3, 0, -1)))",
        "options": ["[3, 2, 1]", "[3, 2, 1, 0]", "Ошибка"],
        "correct": "[3, 2, 1]",
    },
    # 3-26: for ch in "hi": print(ch) → show list of chars
    "3-26": {
        "code": "print(list('hi'))",
        "options": ["['h', 'i']", "['hi']", "Ошибка"],
        "correct": "['h', 'i']",
    },
    # 3-35: list comprehension filter
    "3-35": {
        "code": "print([n for n in [1, 2, 3] if n > 1])",
        "options": ["[2, 3]", "[1, 2, 3]", "Ошибка"],
        "correct": "[2, 3]",
    },
    # 4-2: break → show loop behavior with single print
    "4-2": {
        "code": "for x in [1, 2, 3]:\n    print(x)\n    break",
        "options": ["1", "1\n2", "1\n2\n3"],
        "correct": "1",
    },
    # 4-6: negative index
    "4-6": {
        "code": "a = [10, 20]\nprint(a[-1])",
        "options": ["20", "10", "Ошибка"],
        "correct": "20",
    },
    # 4-10: \\n in string — show what user sees (two lines)
    "4-10": {
        "code": "print(\"a\\nb\")",
        "options": ["a\nb", "ab", "a\\nb"],
        "correct": "a\nb",
    },
    # 4-26: while loop — single iteration to show concept
    "4-26": {
        "code": "x = 1\nwhile x < 2:\n    print(x)\n    x += 1",
        "options": ["1", "1\n2", "0"],
        "correct": "1",
    },
    # 4-31: while with condition
    "4-31": {
        "code": "x = 2\nwhile x > 1:\n    print(x)\n    x -= 1",
        "options": ["2", "2\n1", "Ошибка"],
        "correct": "2",
    },
}

fixed = 0
for lid, new_wo in fixes.items():
    lesson = next((l for l in lessons if l["id"] == lid), None)
    if lesson:
        lesson["what_outputs"] = new_wo
        fixed += 1
        print(f"  ✓ {lid}: replaced with single-output code")
    else:
        print(f"  ✗ {lid}: not found")

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

print(f"\nFixed {fixed} what_outputs blocks")
print(f"Total lessons: {len(lessons)}")

# Verify: no more what_outputs with 2+ prints and single-line options
still_bad = []
for l in lessons:
    wo = l.get("what_outputs", {})
    if not wo or not wo.get("code"): continue
    prints = [ln for ln in wo["code"].split("\n") if ln.strip().startswith("print(")]
    if len(prints) > 1:
        has_multiline = any("\\n" in opt for opt in wo.get("options", []))
        if not has_multiline and len(wo.get("options", [])) == 3:
            still_bad.append(l["id"])

if still_bad:
    print(f"\n⚠ Still problematic: {still_bad}")
else:
    print(f"\n✅ All good — no more multi-print with single-line options")
