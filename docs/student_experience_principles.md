# Python Quest — Student Experience Principles

## 1. Learning by Doing

Каждый урок содержит практическое задание: квиз, predict-output, find-bug, миссию. Теория даётся ровно в том объёме, чтобы ученик мог сразу применить. Мы не объясняем Python абстрактно — мы показываем, как каждая тема работает в коде и в финальной игре.

## 2. Project-Based Motivation

Финальная цель курса — написать свою консольную игру «Побег из Башни Багуса». Каждая тема явно связана с этой целью через `game_relevance` и `connection_to_game`. Ученик не просто учит синтаксис — он собирает деталь для своей игры.

```
Ксю: Каждая новая команда — это будущая деталь твоей игры.
```

## 3. Gradual Difficulty

Сложность растёт постепенно. После каждых 3 уроков — quick_recall-review. После каждой главы — chapter_review. После каждой части — part_review. Hard-темы (if, for, while, вложенные структуры, списки, map, sort) имеют:
- syntax_reminder с визуальным предупреждением
- post_error_dialogue после секции find_bug
- обязательное повторение в следующих review

## 4. No Fake Easy Promises

Мы честно говорим ученику:
- Python не всегда простой
- Ошибки — нормальная часть процесса
- Если не понял с первого раза — это не провал
- Скорость не главное, главное — понимание

Курс не содержит фраз «Python за 2 дня» или «стань программистом за месяц».

## 5. Beginner-Friendly Environment

Первые уроки рекомендуют:
- Онлайн-среду (online-python.com) для первых шагов
- Python Tutor (pythontutor.com) для визуализации кода
- VS Code — только после базовой уверенности
- Если застрял на запуске — это не значит, что ты не понимаешь Python

## 6. Error Location Before Solution

Подсказки в find_bug и review используют 4-уровневую лестницу:

| Уровень | Формат |
|---------|--------|
| 1 (hint_location) | «Проверь строку с if.» |
| 2 (hint_concept) | «Условие сравнивает строку с числом.» |
| 3 (minimal_correction) | «Нужен int(input()).» |
| 4 (full_solution) | Полный исправленный код |

## 7. Spaced Repetition

Каждые ≤3 уроков — quick_recall. Hard-темы появляются минимум в 2 review. Review-блоки содержат смесь из последних и старых тем (mixed review).

## 8. Realistic Time Expectations

Каждый урок имеет:
- `difficulty` (easy / medium / hard / boss)
- `estimated_time_min` (реалистичная оценка в минутах)

| Difficulty | Estimated time | Expected retries |
|---|---|---|
| easy | 10-15 min | 0-1 |
| medium | 20-30 min | 1-3 |
| hard | 35-50 min | 2-5 |
| boss | 45-60 min | 3+ |

## 9. Emotional Support Without Patronizing

Курс поддерживает ученика, но не сюсюкает. Диалоги персонажей:
- **Ксю** объясняет спокойно и поддерживает
- **Ва** проверяет логику и не даёт угадывать
- **Да** мотивирует через проектные шаги
- **Багус** показывает ошибки без осуждения

## 10. Mistake Is a Signal, Not Failure

Каждая ошибка в find_bug, predict_output и review — это сигнал к повторению, а не провал. Post-error dialogue нормализует ошибку:
> «Ошибки на этом этапе — нормально. Главное — понять причину и исправить.»

## 11. Environment-Agnostic Learning

Курс не требует установки IDE. Всё можно проходить в браузере. VS Code — опция для тех, кто хочет пойти глубже.

## 12. Practice Density

Каждый урок содержит минимум 3 практических задания:
- predict_output (Что выведет код?)
- find_bug (Найди ошибку)
- mission (Практическая задача)
- quiz (Мини-квиз)

## 13. Review as Learning Reset

Review-блоки — это не просто повторение, а learning reset. После hard-темы review помогает:
- Закрепить материал через questions / predict-output / find-bug
- Связать тему с финальной игрой
- Снизить когнитивную нагрузку перед следующим hard
