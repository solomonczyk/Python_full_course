"""
Add backticks around Python keywords in dialogue text, but only outside existing code blocks.
Run: python scripts/highlight_keywords.py
"""

import json, sys, io, re, shutil, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PY_KEYWORDS = ['True', 'False', 'None', 'if', 'else', 'elif', 'for', 'while', 'in', 'not',
               'and', 'or', 'def', 'return', 'class', 'import', 'from', 'break', 'continue',
               'pass', 'try', 'except', 'finally', 'raise', 'with', 'as', 'yield', 'global',
               'is', 'lambda', 'del', 'assert', 'nonlocal',
               'print', 'input', 'int', 'str', 'float', 'bool', 'len', 'list', 'range',
               'set', 'dict', 'tuple', 'type', 'sorted', 'map', 'filter', 'zip',
               'append', 'pop', 'remove', 'insert', 'extend', 'index', 'count',
               'split', 'join', 'strip', 'lower', 'upper', 'replace',
               'sort', 'copy', 'deepcopy', 'shuffle', 'choice', 'randint', 'random',
               'sum', 'min', 'max', 'abs', 'round', 'enumerate', 'reversed',
               'ValueError', 'TypeError', 'NameError', 'SyntaxError', 'IndexError',
               'KeyError', 'AttributeError', 'ZeroDivisionError', 'ImportError',
               'StopIteration', 'FileNotFoundError', 'Exception', 'KeyboardInterrupt',
               'SystemExit']

PATH = "api/app/data/lessons.json"
BACKEND_PATH = "backend/app/data/lessons.json"

# Sort by length descending so longer matches (e.g. "append") take priority over shorter ("in")
PY_KEYWORDS.sort(key=len, reverse=True)

with open(PATH, encoding='utf-8') as f:
    lessons = json.load(f)

def add_backticks(text):
    """Add backticks around Python keywords, only outside existing code blocks."""
    parts = re.split(r'(`[^`]*`)', text)
    result = []
    for part in parts:
        if part.startswith('`') and part.endswith('`'):
            result.append(part)  # Already code — leave as-is
        else:
            for kw in PY_KEYWORDS:
                part = re.sub(r'(?<!\w)(' + re.escape(kw) + r')(?!\w)', r'`\1`', part)
            result.append(part)
    return ''.join(result)

changes = 0
for lesson in lessons:
    for d in lesson.get('pre_topic_dialogue', []) + lesson.get('post_error_dialogue', []):
        new_text = add_backticks(d['text'])
        if new_text != d['text']:
            d['text'] = new_text
            changes += 1

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

shutil.copy2(PATH, BACKEND_PATH)

print(f"Added backticks to {changes} keyword occurrences")
print(f"Saved to {PATH} and {BACKEND_PATH}")
