#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('backend/app/data/lessons.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ids_to_check = {'1-1','1-3','1-8','2-1','2-3','2-5','3-6','3-8','3-22','3-35','4-9','4-14','4-15','4-21','4-24','4-31','5-1','5-4'}
lessons = [l for l in data if l['id'] in ids_to_check]

for l in lessons:
    lid = l['id']
    print(f"\n{'='*80}")
    print(f"LESSON {lid}: {l['title']} ({l['subtitle']})")
    print(f"Difficulty: {l['difficulty']}, Time: {l['estimated_time_min']}min")

    # Explanation
    if 'explanation' in l:
        e = l['explanation']
        print(f"\n--- EXPLANATION ---")
        print(f"Text: {e.get('text','')}")
        if 'code_example' in e:
            print(f"Code: {e['code_example']}")
        if 'output' in e:
            print(f"Output: {e['output']}")

    # Analogy
    if 'analogy' in l:
        a = l['analogy']
        print(f"\n--- ANALOGY ---")
        print(f"Title: {a.get('title','')}")
        print(f"Metaphor: {a.get('story_metaphor','')[:200]}")
        print(f"Mapping: {a.get('python_mapping','')[:200]}")
        print(f"Rule: {a.get('key_rule','')[:200]}")

    # Quiz
    if 'quiz' in l:
        q = l['quiz']
        print(f"\n--- QUIZ ---")
        print(f"Q: {q.get('question','')}")
        for opt in q.get('options', []):
            mark = "✓" if opt.get('correct') else " "
            print(f"  [{mark}] {opt.get('text','')}")

    # Mission
    if 'mission' in l:
        m = l['mission']
        print(f"\n--- MISSION ---")
        print(f"Title: {m.get('title','')}")
        print(f"Task: {m.get('task','')[:200]}")
        print(f"Expected: {m.get('expected_output','')[:100]}")

    # Find Bug
    if 'find_bug' in l:
        fb = l['find_bug']
        print(f"\n--- FIND BUG ---")
        print(f"Bug code: {fb.get('code','')}")
        print(f"Hint: {fb.get('hint','')[:150]}")
        print(f"Correct: {fb.get('correct','')}")

    # Practice subtasks
    if 'practice_subtasks' in l and l['practice_subtasks']:
        print(f"\n--- PRACTICE SUBTASKS ({len(l['practice_subtasks'])}) ---")
        for i, pt in enumerate(l['practice_subtasks']):
            print(f"  {i+1}. {pt.get('title','')}: {pt.get('task','')[:150]}")

    # Game relevance
    if 'game_relevance' in l:
        print(f"\n--- GAME RELEVANCE ---")
        print(f"{l['game_relevance'][:200]}")

    # Connection to game
    if 'connection_to_game' in l:
        print(f"\n--- CONNECTION TO GAME ---")
        print(f"{l['connection_to_game'][:200]}")

    # Dialogue samples
    if 'pre_topic_dialogue' in l and l['pre_topic_dialogue']:
        print(f"\n--- PRE-TOPIC DIALOGUE (first 3) ---")
        for d in l['pre_topic_dialogue'][:3]:
            print(f"  [{d.get('character','')}] {d.get('text','')[:150]}")

    print(f"\n{'='*80}")
