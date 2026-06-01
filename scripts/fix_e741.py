"""Fix E741 ambiguous variable name 'l' in Python files."""
import re

FILES = [
    "backend/tests/test_learning_support_system.py",
    "scripts/audit_learning_support_system.py",
]

for filepath in FILES:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Fix list comprehensions: [l for l in ...] -> [item for item in ...]
    # and next(l for l in ...) -> next(item for item in ...)
    # and {l["id"] for l in ...} -> {item["id"] for item in ...}

    # Replace patterns with 'l' as iteration variable in comprehensions
    # Pattern: for l in (variable_name)
    # Replace 'l' in comprehension with 'item' when 'l' is the loop variable
    content = re.sub(
        r'(\[|\(|\{)\s*l\s+for\s+l\s+in\s+',
        lambda m: m.group(1) + ' item for item in ',
        content,
    )
    content = re.sub(
        r'for\s+l\s+in\s+(\w+)\s+if\s+l\[',
        'for item in \\1 if item[',
        content,
    )
    content = re.sub(
        r'\bl\b(?=\[["\'](?:id|part))',
        'item',
        content,
    )
    # Replace remaining 'l' in list comps that refer to iteration
    # Fix specific: {l["id"] for l in lessons}
    content = re.sub(
        r'\{\s*l\s*\[',
        '{ item[',
        content,
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed: {filepath}")
