"""
Add backticks around Python keywords in analogy fields.
Run: python scripts/highlight_analogies.py
"""

import json, sys, io, re, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PATH = "api/app/data/lessons.json"
BACKEND_PATH = "backend/app/data/lessons.json"

PY_KEYWORDS = sorted([
    "True", "False", "None", "if", "else", "elif", "for", "while", "in", "not",
    "and", "or", "def", "return", "class", "import", "from", "break", "continue",
    "pass", "try", "except", "finally", "raise", "with", "as", "yield", "global",
    "is", "lambda", "del", "assert", "nonlocal",
    "print", "input", "int", "str", "float", "bool", "len", "list", "range",
    "set", "dict", "tuple", "type", "sorted", "map", "filter", "zip",
    "append", "pop", "remove", "insert", "extend", "index", "count",
    "split", "join", "strip", "lower", "upper", "replace",
    "sort", "copy", "deepcopy", "shuffle", "choice", "randint", "random",
    "sum", "min", "max", "abs", "round",
    "ValueError", "TypeError", "NameError", "SyntaxError", "IndexError",
    "KeyError", "AttributeError", "ZeroDivisionError", "ImportError",
    "FileNotFoundError", "Exception", "KeyboardInterrupt",
], key=len, reverse=True)

BT = chr(96)  # backtick character

with open(PATH, encoding="utf-8") as f:
    lessons = json.load(f)

def highlight(text):
    """Add backticks around Python keywords outside existing code blocks."""
    parts = re.split(r"(`[^`]*`)", text)
    result = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            result.append(part)  # already code — skip
        else:
            for kw in PY_KEYWORDS:
                part = re.sub(r"(?<!\w)(" + re.escape(kw) + r")(?!\w)", BT + r"\1" + BT, part)
            result.append(part)
    return "".join(result)

changes = 0
for lesson in lessons:
    analogy = lesson.get("analogy", {})
    for field in ["story_metaphor", "python_mapping", "key_rule"]:
        text = analogy.get(field, "")
        if text:
            new_text = highlight(text)
            if new_text != text:
                analogy[field] = new_text
                changes += 1

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

shutil.copy2(PATH, BACKEND_PATH)

print(f"Highlighted {changes} analogy fields with backtick keywords")
