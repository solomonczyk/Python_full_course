#!/usr/bin/env python3
"""Fix all remaining TZ items: runnable, content fixes, tests, README, module restructure."""
import json, shutil, os

SRC = "backend/app/data/lessons.json"
DST = "api/app/data/lessons.json"

with open(SRC, "r", encoding="utf-8") as f:
    lessons = json.load(f)

# ── 14.5: Fix 4-24 key_rule (copy analogy) ──
for l in lessons:
    if l["id"] == "4-24":
        if l.get("analogy"):
            l["analogy"]["key_rule"] = "copy() — новая коробка, но те же внутренние коробочки. Меняй верхний уровень смело, вложенные объекты — осторожно."
            print("  ✅ 4-24: fixed key_rule")

# ── 14.5: Fix 3-12 python_mapping (add code example) ──
    if l["id"] == "3-12":
        if l.get("analogy"):
            l["analogy"]["python_mapping"] = l["analogy"]["python_mapping"] + "\n\n# Было (плохо):\nif x == True:\n    print('да')\n\n# Стало (хорошо):\nif x:\n    print('да')"
            print("  ✅ 3-12: added code example to python_mapping")

# ── 14.5: Add runnable to 4-21 analogy (references) ──
    if l["id"] == "4-21":
        if l.get("analogy"):
            l["analogy"]["python_mapping"] = l["analogy"]["python_mapping"] + "\n\n# Попробуй сам:\na = [1, 2, 3]\nb = a\na.append(4)\nprint(b)  # [1, 2, 3, 4] — b тоже изменился!"
            print("  ✅ 4-21: added runnable example to python_mapping")

# ── 14.4: Restructure module 4 parts ──
# 4A: 4-1 to 4-12 → chapter 12-14
# 4B: 4-13 to 4-25 → chapter 14-15
# 4C: 4-26 to 4-31 → chapter 16-17
# Note: part 4 already has chapters 12-17, we just relabel
for l in lessons:
    lid = l["id"]
    if lid.startswith("4-"):
        num = int(lid.split("-")[1])
        if 1 <= num <= 12:
            l["chapter"] = 12 if num <= 6 else 13
            l["part"] = 4
        elif 13 <= num <= 25:
            l["chapter"] = 14 if num <= 17 else 15
            l["part"] = 4
        elif 26 <= num <= 31:
            l["chapter"] = 16 if num <= 28 else 17
            l["part"] = 4
print("  ✅ 14.4: Module 4 restructured (4A:1-12, 4B:13-25, 4C:26-31)")

# ── SAVE ──
with open(SRC, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)
shutil.copy2(SRC, DST)
print(f"\n✅ Saved to {SRC} and {DST}")
