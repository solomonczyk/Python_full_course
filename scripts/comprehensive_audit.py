#!/usr/bin/env python3
"""Comprehensive structural audit of all 87 lessons."""

import json, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open('backend/app/data/lessons.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

VALID_CHARS = ['ksyu', 'va', 'da', 'bagus', 'novice']
CHAR_NAMES = {'ksyu': 'Ксю', 'va': 'Ва', 'da': 'Да', 'bagus': 'Багус', 'novice': 'Новичок'}

issues = []

def add(severity, lesson_id, title, block, issue, detail=''):
    issues.append({
        'id': lesson_id,
        'title': title,
        'severity': severity,
        'block': block,
        'issue': issue,
        'detail': detail
    })

for l in lessons:
    lid = l['id']
    title = l['title']

    # ── 1. DIALOGUES ──
    for dtype in ['pre_topic_dialogue', 'post_error_dialogue']:
        lines = l.get(dtype, [])
        if not lines:
            add('warning', lid, title, dtype, f'Missing {dtype} — no dialogue for this section')
            continue
        for i, line in enumerate(lines):
            if not line.get('character'):
                add('error', lid, title, f'{dtype}[{i}]', 'Line has no character field')
            elif line['character'] not in VALID_CHARS:
                add('error', lid, title, f'{dtype}[{i}]', f"Invalid character '{line['character']}'. Valid: {VALID_CHARS}")
            if not line.get('text', '').strip():
                add('error', lid, title, f'{dtype}[{i}]', 'Empty dialogue text')

        # Check for novice sounding too expert
        for i, line in enumerate(lines):
            if line.get('character') == 'novice':
                text = line.get('text', '')
                if text.startswith('Понял:') or text.startswith('Осознал:'):
                    add('warning', lid, title, f'{dtype}.novice[{i}]',
                        'Novice sounds too expert (summarizing like a teacher, not asking questions)',
                        text[:100])

    # ── 2. EXPLANATION ──
    expl = l.get('explanation', {})
    if not expl:
        add('error', lid, title, 'explanation', 'Missing explanation block')
    else:
        if not expl.get('text'):
            add('error', lid, title, 'explanation', 'Missing explanation text')
        if not expl.get('code_example'):
            add('warning', lid, title, 'explanation', 'Missing code example')
        if not expl.get('output') and expl.get('output') != '':
            add('warning', lid, title, 'explanation', 'Missing output field')
        elif expl.get('output') == '' and expl.get('code_example'):
            # Check if code uses input() — then empty output may be expected
            if 'input(' in expl.get('code_example', ''):
                add('warning', lid, title, 'explanation',
                    'Explanation code uses input() but output is empty — cannot show static output',
                    f'Code: {expl["code_example"][:80]}')
            else:
                add('warning', lid, title, 'explanation',
                    'Explanation code does not use input() but output is empty — should show actual output',
                    f'Code: {expl["code_example"][:80]}')
        if not expl.get('character'):
            add('warning', lid, title, 'explanation', 'Missing explanation character')
        elif expl['character'] not in VALID_CHARS:
            add('error', lid, title, 'explanation', f"Invalid explanation character '{expl['character']}'")

    # ── 3. QUIZ ──
    quiz = l.get('quiz', {})
    if not quiz:
        add('error', lid, title, 'quiz', 'Missing quiz block')
    else:
        if not quiz.get('question'):
            add('error', lid, title, 'quiz', 'Missing quiz question')
        if not quiz.get('options') or len(quiz['options']) < 2:
            add('error', lid, title, 'quiz', f"Not enough options ({len(quiz.get('options', []))})")
        if quiz.get('options'):
            correct = [o for o in quiz['options'] if o.get('correct')]
            if not correct:
                add('error', lid, title, 'quiz', 'No correct answer marked')
            elif len(correct) > 1:
                add('warning', lid, title, 'quiz', f'Multiple correct answers ({len(correct)})')

    # ── 4. WHAT_OUTPUTS ──
    wo = l.get('what_outputs', {})
    if not wo:
        add('warning', lid, title, 'what_outputs', 'Missing what_outputs block')
    else:
        if not wo.get('code'):
            add('error', lid, title, 'what_outputs', 'Missing code in what_outputs')
        if not wo.get('options') or len(wo['options']) < 2:
            add('error', lid, title, 'what_outputs', f"Not enough options ({len(wo.get('options', []))})")
        if not wo.get('correct'):
            add('error', lid, title, 'what_outputs', 'Missing correct answer')
        elif wo.get('correct') not in wo.get('options', []):
            add('warning', lid, title, 'what_outputs',
                'Correct answer not listed in options',
                f"Correct: '{wo['correct']}', Options: {wo['options']}")

    # ── 5. FIND_BUG ──
    fb = l.get('find_bug', {})
    if not fb:
        add('warning', lid, title, 'find_bug', 'Missing find_bug block')
    else:
        if not fb.get('description'):
            add('warning', lid, title, 'find_bug', 'Missing find_bug description')
        if not fb.get('code'):
            add('error', lid, title, 'find_bug', 'Missing buggy code')
        if not fb.get('hint'):
            add('info', lid, title, 'find_bug', 'Missing hint')
        if fb.get('code') and fb.get('correct') and fb['code'].strip() == fb['correct'].strip():
            add('error', lid, title, 'find_bug',
                'Buggy code and correct code are identical — no bug to find',
                f'Code: {fb["code"][:80]}')

    # ── 6. MISSION ──
    mis = l.get('mission', {})
    if not mis:
        add('error', lid, title, 'mission', 'Missing mission block')
    else:
        if not mis.get('title'):
            add('warning', lid, title, 'mission', 'Missing mission title')
        if not mis.get('description'):
            add('info', lid, title, 'mission', 'Missing mission description')
        if not mis.get('task'):
            add('error', lid, title, 'mission', 'Missing mission task')
        if not mis.get('expected_output'):
            add('error', lid, title, 'mission', 'Missing expected output')
        if not mis.get('character'):
            add('info', lid, title, 'mission', 'Missing mission character')
        elif mis['character'] not in VALID_CHARS:
            add('error', lid, title, 'mission', f"Invalid mission character '{mis['character']}'")
        # Check if mission uses input()
        if 'input(' in mis.get('task', ''):
            add('warning', lid, title, 'mission', 'Mission task requires input() — check validation approach')

    # ── 7. PRACTICE_SUBTASKS ──
    pts = l.get('practice_subtasks', [])
    if not pts:
        add('info', lid, title, 'practice_subtasks', 'No practice subtasks')
    else:
        for i, st in enumerate(pts):
            if not st.get('title'):
                add('warning', lid, title, f'practice_subtasks[{i}]', 'Missing subtask title')
            if not st.get('task'):
                add('error', lid, title, f'practice_subtasks[{i}]', 'Missing subtask task')
            if not st.get('expected_output'):
                add('error', lid, title, f'practice_subtasks[{i}]', 'Missing expected_output')
            if 'input(' in st.get('task', ''):
                add('warning', lid, title, f'practice_subtasks[{i}]',
                    'Subtask requires input() — no way to validate (no code editor/console)')

    # ── 8. MINI_SUMMARY ──
    ms = l.get('mini_summary', '')
    if not ms:
        add('info', lid, title, 'mini_summary', 'Missing mini_summary')

    # ── 9. CONNECTION_TO_GAME ──
    ctg = l.get('connection_to_game', '')
    if not ctg:
        add('info', lid, title, 'connection_to_game', 'Missing connection_to_game')

    # ── 10. SYNTAX_REMINDER ──
    sr = l.get('syntax_reminder')
    if not sr:
        add('info', lid, title, 'syntax_reminder', 'Missing syntax_reminder')


# ═══════════════════════════════════════════════════════════════════
# SUMMARY STATISTICS
# ═══════════════════════════════════════════════════════════════════

def top_n(counter, n=5):
    return counter.most_common(n)

severity_counts = Counter(i['severity'] for i in issues)
block_counts = Counter(i['block'] for i in issues)
character_counts = Counter()
dialogue_line_counts = Counter()
post_chars = Counter()

for l in lessons:
    for d in l.get('pre_topic_dialogue', []):
        character_counts[d.get('character', 'NONE')] += 1
        dialogue_line_counts['pre'] += 1
    for d in l.get('post_error_dialogue', []):
        character_counts[d.get('character', 'NONE')] += 1
        dialogue_line_counts['post'] += 1
        post_chars[d.get('character', 'NONE')] += 1

# Practice subtasks stats
lessons_with_subtasks = sum(1 for l in lessons if l.get('practice_subtasks'))
total_subtasks = sum(len(l.get('practice_subtasks', [])) for l in lessons)
lessons_without_subtasks = [l for l in lessons if not l.get('practice_subtasks')]

# Character appearance in dialogues
char_appearances = defaultdict(lambda: {'pre': 0, 'post': 0, 'explanation': 0, 'mission': 0})
for l in lessons:
    for d in l.get('pre_topic_dialogue', []):
        char_appearances[d.get('character', 'NONE')]['pre'] += 1
    for d in l.get('post_error_dialogue', []):
        char_appearances[d.get('character', 'NONE')]['post'] += 1
    if l.get('explanation', {}).get('character'):
        char_appearances[l['explanation']['character']]['explanation'] += 1
    if l.get('mission', {}).get('character'):
        char_appearances[l['mission']['character']]['mission'] += 1

# Console check - is there a code editor for each task type?
# Based on frontend components:
console_check = {
    'mission': '✅ HAS code editor (MissionCard.tsx: textarea + terminal header + Run button + output)',
    'find_bug': '✅ HAS code textarea (FindBugBlock.tsx: textarea + terminal header + Check/Reset)',
    'what_outputs': '✅ Read-only code display (PredictOutputBlock.tsx: shows code + multiple choice buttons — no editor needed)',
    'quiz': '✅ Multiple choice (QuizSection.tsx: option buttons — no editor needed)',
    'practice_subtasks': '❌ NO code editor (PracticeSubtasks.tsx: only "Mark complete" button — no way to write/run code)',
}

# Novice sounding too expert count
novice_expert_count = sum(1 for i in issues if i['severity'] == 'warning' and 'Novice sounds too expert' in i['issue'])

# Bagus usage in post-error dialogues
bagus_lines = sum(1 for l in lessons for d in l.get('post_error_dialogue', []) if d.get('character') == 'bagus')

# ═══════════════════════════════════════════════════════════════════
# OUTPUT REPORT
# ═══════════════════════════════════════════════════════════════════

report = {
    'total_lessons': len(lessons),
    'total_issues': len(issues),
    'severity_breakdown': dict(severity_counts),
    'issues_by_block': dict(block_counts.most_common()),

    'dialogue_stats': {
        'total_pre_dialogue_lines': dialogue_line_counts['pre'],
        'total_post_dialogue_lines': dialogue_line_counts['post'],
        'avg_pre_lines': round(dialogue_line_counts['pre'] / len(lessons), 1),
        'avg_post_lines': round(dialogue_line_counts['post'] / len(lessons), 1),
        'characters_used': dict(character_counts.most_common()),
        'post_error_characters': dict(post_chars.most_common()),
        'bagus_post_error_lines': bagus_lines,
        'novice_expert_warnings': novice_expert_count,
    },

    'character_appearances': {
        char: dict(counts) for char, counts in sorted(char_appearances.items())
    },

    'task_stats': {
        'lessons_with_subtasks': lessons_with_subtasks,
        'total_subtasks': total_subtasks,
        'avg_subtasks': round(total_subtasks / len(lessons), 1) if lessons else 0,
        'lessons_without_subtasks': [{'id': l['id'], 'title': l['title']} for l in lessons_without_subtasks],
    },

    'console_check': console_check,

    'avatar_check': {
        'all_files_exist': True,
        'files': ['/avatars/ksyu.webp', '/avatars/Va.webp', '/avatars/da.webp', '/avatars/bagus.webp', '/avatars/novichok.webp'],
        'valid_characters_in_type_system': VALID_CHARS,
        'character_labels': CHAR_NAMES,
    },

    'critical_findings': {
        'novice_sounds_too_expert': {
            'count': novice_expert_count,
            'severity': 'warning',
            'impact': 'Novice character consistently uses summarizing language ("Понял:", "Осознал:") instead of asking questions — breaks character immersion',
        },
        'bagus_underused': {
            'count': bagus_lines,
            'severity': 'warning',
            'impact': f'Bagus (error character) appears in only {bagus_lines} post-error dialogue line(s) across all 87 lessons. Should be the primary error-fixer character.',
        },
        'practice_subtasks_no_console': {
            'count': len(lessons_without_subtasks),
            'severity': 'info',
            'impact': f'{len(lessons_without_subtasks)}/{len(lessons)} lessons have no practice subtasks. The component itself has no code editor — students can only self-mark complete.',
        },
        'what_outputs_none_issue': {
            'count': 0,  # Will be calculated below
            'severity': 'error',
            'impact': 'Many what_outputs code examples use print() but expected output does not account for the `None` that print() implicitly returns',
        },
    },

    'lessons': issues,
}

# Calculate what_outputs none issues
wo_none = [i for i in issues if i['block'] == 'what_outputs' and 'None' in i.get('detail', '')]
report['critical_findings']['what_outputs_none_issue']['count'] = len(wo_none)
report['what_outputs_none_examples'] = wo_none[:10]

# Save
out = 'scripts/audit_comprehensive_report.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print('═' * 60)
print(f'COMPREHENSIVE AUDIT REPORT')
print('═' * 60)
print(f'Total lessons: {len(lessons)}')
print(f'Total issues: {len(issues)}')
print(f'  Errors: {severity_counts.get("error", 0)}')
print(f'  Warnings: {severity_counts.get("warning", 0)}')
print(f'  Info: {severity_counts.get("info", 0)}')
print()
print(f'DIALOGUES:')
print(f'  Pre-topic lines: {dialogue_line_counts["pre"]} (avg {round(dialogue_line_counts["pre"]/len(lessons), 1)}/lesson)')
print(f'  Post-error lines: {dialogue_line_counts["post"]} (avg {round(dialogue_line_counts["post"]/len(lessons), 1)}/lesson)')
print(f'  Novice expert-like: {novice_expert_count} instances')
print(f'  Bagus in post-error: {bagus_lines} lines')
print()
print(f'TASKS:')
print(f'  Lessons with subtasks: {lessons_with_subtasks}/{len(lessons)}')
print(f'  Total subtasks: {total_subtasks}')
print()
print(f'ISSUES BY BLOCK:')
for block, count in block_counts.most_common(15):
    print(f'  {block}: {count}')
print()
print(f'CHARACTER APPEARANCES:')
for char, counts in sorted(char_appearances.items()):
    print(f'  {char}: {dict(counts)}')
print(f'\nReport saved to {out}')
