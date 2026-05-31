import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('backend/app/data/lessons.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def create_runnable_code(code_example):
    """Create a self-contained version of code that doesn't use input()."""
    if 'input(' not in code_example:
        return code_example

    lines = code_example.strip().split('\n')
    new_lines = []

    for line in lines:
        # Replace input() calls with hardcoded values
        # Common patterns:
        # input("prompt") -> hardcoded string
        # int(input("prompt")) -> hardcoded int
        # float(input("prompt")) -> hardcoded float

        if 'input()' in line or 'input(' in line:
            # Try to detect the variable name from context for meaningful values
            # name = input("...") -> name = "Ксю"
            # age = int(input("...")) -> age = 10
            # number = float(input("...")) -> number = 3.14

            # Check if it's wrapped in int()
            if 'int(input(' in line:
                # variable = int(input("prompt"))
                # -> variable = 10
                import re
                match = re.match(r'(\s*)(\w+)\s*=\s*int\(input\(.*?\)\)\s*', line)
                if match:
                    indent = match.group(1)
                    var_name = match.group(2)
                    new_lines.append(f'{indent}{var_name} = 10')
                    continue
                # Just remove the int() and keep input -> but we replace anyway
                # Actually let's handle generic case
                match = re.match(r'(\s*)(\w+)\s*=\s*int\(input\(.*?\)\)\s*$', line)
                if not match:
                    # Maybe there's more complex expression
                    # Just replace the whole input with a value
                    new_line = line.replace('int(input())', '10')
                    new_line = new_line.replace('int(input(', '10  # ')
                    # Clean up any remaining input()
                    new_line = new_line.replace('input()', '"default"')
                    import re
                    new_line = re.sub(r'int\(input\([^)]*\)\)', '10', new_line)
                    new_line = re.sub(r'input\([^)]*\)', '"default"', new_line)
                    new_lines.append(new_line)
                    continue

            elif 'float(input(' in line:
                import re
                match = re.match(r'(\s*)(\w+)\s*=\s*float\(input\(.*?\)\)\s*', line)
                if match:
                    indent = match.group(1)
                    var_name = match.group(2)
                    new_lines.append(f'{indent}{var_name} = 3.14')
                    continue
                new_line = re.sub(r'float\(input\([^)]*\)\)', '3.14', line)
                new_line = re.sub(r'input\([^)]*\)', '"default"', new_line)
                new_lines.append(new_line)
                continue

            else:
                # Plain input()
                import re
                match = re.match(r'(\s*)(\w+)\s*=\s*input\(.*?\)\s*', line)
                if match:
                    indent = match.group(1)
                    var_name = match.group(2)
                    # Try to find a meaningful default based on context
                    var_lower = var_name.lower()
                    if any(x in var_lower for x in ['name', 'имя', 'username', 'nick']):
                        new_lines.append(f'{indent}{var_name} = "Ксю"')
                    elif any(x in var_lower for x in ['age', 'возраст', 'year', 'old', 'years']):
                        new_lines.append(f'{indent}{var_name} = 10')
                    elif any(x in var_lower for x in ['number', 'число', 'count', 'num', 'amount', 'quantity']):
                        new_lines.append(f'{indent}{var_name} = 7')
                    elif any(x in var_lower for x in ['city', 'город', 'place', 'location', 'country']):
                        new_lines.append(f'{indent}{var_name} = "Москва"')
                    elif any(x in var_lower for x in ['color', 'цвет', 'colour']):
                        new_lines.append(f'{indent}{var_name} = "синий"')
                    elif any(x in var_lower for x in ['answer', 'ответ', 'reply', 'response', 'decision']):
                        new_lines.append(f'{indent}{var_name} = "да"')
                    elif any(x in var_lower for x in ['fruit', 'фрукт', 'food', 'еда', 'dish']):
                        new_lines.append(f'{indent}{var_name} = "яблоко"')
                    elif any(x in var_lower for x in ['password', 'пароль', 'secret']):
                        new_lines.append(f'{indent}{var_name} = "qwerty"')
                    elif any(x in var_lower for x in ['email', 'почта']):
                        new_lines.append(f'{indent}{var_name} = "test@example.com"')
                    elif any(x in var_lower for x in ['action', 'действие', 'choice', 'выбор', 'command', 'cmd']):
                        new_lines.append(f'{indent}{var_name} = "1"')
                    else:
                        new_lines.append(f'{indent}{var_name} = "Python"')
                    continue

                # Generic fallback
                new_line = re.sub(r'input\([^)]*\)', '"Python"', line)
                new_lines.append(new_line)
        else:
            new_lines.append(line)

    return '\n'.join(new_lines)


lessons_updated = 0
lessons_input = 0
lessons_no_input = 0
lessons_skipped_no_code = 0

for lesson in data:
    explanation = lesson.get('explanation')
    if not explanation:
        lessons_skipped_no_code += 1
        continue

    code_example = explanation.get('code_example')
    if not code_example:
        lessons_skipped_no_code += 1
        continue

    if 'input(' in code_example:
        lesson['runnable_code'] = create_runnable_code(code_example)
        lessons_input += 1
        lessons_updated += 1
    else:
        lesson['runnable_code'] = code_example
        lessons_no_input += 1
        lessons_updated += 1

print(f'Total lessons: {len(data)}')
print(f'Lessons with code_example (no input): {lessons_no_input}')
print(f'Lessons with code_example (with input): {lessons_input}')
print(f'Lessons without code_example: {lessons_skipped_no_code}')
print(f'Total runnable_code added: {lessons_updated}')

# Show some examples
for lesson in data:
    if 'runnable_code' in lesson:
        rid = lesson['id']
        orig = lesson['explanation']['code_example']
        runnable = lesson['runnable_code']
        if orig != runnable:
            print(f'\n--- {rid} ---')
            print(f'  Original: {repr(orig)}')
            print(f'  Runnable: {repr(runnable)}')

with open('backend/app/data/lessons.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('\nDone! File saved.')
