import type { DialogueLine, MissionResult, ErrorCategory, Character } from '../types'

// ── Error categorization ─────────────────────────────────────────────────

const ERROR_PATTERNS: [RegExp, ErrorCategory][] = [
  [/SyntaxError|invalid syntax|unexpected (token|character|eof)/i, 'syntax_error'],
  [/TypeError|can only concatenate|must be (str|int|float|list)|unsupported operand/i, 'type_error'],
  [/NameError|is not defined/i, 'type_error'],
  [/IndexError|list index out of range/i, 'type_error'],
  [/ValueError|invalid literal/i, 'type_error'],
  [/IndentationError|unexpected indent/i, 'syntax_error'],
  [/запрещённых модулей|forbidden.*import/i, 'forbidden_import'],
  [/Превышено время|timeout/i, 'timeout'],
]

/**
 * Classify a mission check error into a category for adaptive feedback.
 */
export function categorizeError(result: MissionResult, caught?: boolean): ErrorCategory {
  if (caught) return 'connection_error'

  const error = result.error ?? ''

  if (!result.correct && result.actual_output !== null && !error) {
    return 'wrong_output'
  }

  for (const [pattern, category] of ERROR_PATTERNS) {
    if (pattern.test(error)) return category
  }

  if (error) return 'unknown'

  return 'wrong_output'
}

// ── Error display metadata ────────────────────────────────────────────────

interface ErrorMeta {
  icon: string
  label: string
  primaryCharacter: Character
}

export const ERROR_META: Record<ErrorCategory, ErrorMeta> = {
  syntax_error: {
    icon: 'syntax_error',
    label: 'Синтаксическая ошибка',
    primaryCharacter: 'ksyu',
  },
  type_error: {
    icon: 'data_alert',
    label: 'Ошибка типов',
    primaryCharacter: 'va',
  },
  wrong_output: {
    icon: 'output',
    label: 'Неверный вывод',
    primaryCharacter: 'va',
  },
  missing_output: {
    icon: 'output',
    label: 'Нет вывода',
    primaryCharacter: 'va',
  },
  empty_code: {
    icon: 'edit_note',
    label: 'Код пуст',
    primaryCharacter: 'bagus',
  },
  forbidden_import: {
    icon: 'block',
    label: 'Запрещённый импорт',
    primaryCharacter: 'bagus',
  },
  timeout: {
    icon: 'timer_off',
    label: 'Превышено время',
    primaryCharacter: 'bagus',
  },
  connection_error: {
    icon: 'wifi_off',
    label: 'Ошибка соединения',
    primaryCharacter: 'novice',
  },
  unknown: {
    icon: 'error',
    label: 'Ошибка',
    primaryCharacter: 'va',
  },
}

// ── Progressive hint selection ────────────────────────────────────────────

/**
 * Select dialogue lines from post_error_dialogue based on attempt count.
 * Attempt 1: first 2 lines (soft hint)
 * Attempt 2: next 2 lines (more specific)
 * Attempt 3+: remaining lines (nearly full guidance)
 */
export function selectProgressiveHints(
  failDialogue: DialogueLine[],
  attemptCount: number,
): DialogueLine[] {
  if (!failDialogue.length) return []

  if (attemptCount <= 1) {
    // Attempt 1: first 2 lines
    return failDialogue.slice(0, 2)
  } else if (attemptCount === 2) {
    // Attempt 2: lines 2-4 (or 3-4 if available)
    const start = Math.min(2, failDialogue.length - 1)
    return failDialogue.slice(start, start + 2)
  } else {
    // Attempt 3+: show all remaining after the first 4, or full dialogue
    if (failDialogue.length <= 4) return failDialogue
    return failDialogue.slice(4)
  }
}

// ── Character rule enforcement ────────────────────────────────────────────

/**
 * Enforce character dialogue rules:
 * Rule 1 — No consecutive Bagus lines
 * Rule 2 — Bagus max 1 per block, never the last line
 * Rule 3 — Short feedback (truncate to maxLines if set)
 */
export function enforceCharacterRules(
  lines: DialogueLine[],
  maxLines?: number,
): DialogueLine[] {
  let result: DialogueLine[] = [...lines]

  // Rule 1: Remove consecutive Bagus
  result = result.filter((line, i, arr) => {
    if (i === 0) return true
    return !(line.character === 'bagus' && arr[i - 1].character === 'bagus')
  })

  // Rule 2: Bagus never last, max 1 per block
  const bagusIndices = result
    .map((l, i) => (l.character === 'bagus' ? i : -1))
    .filter(i => i >= 0)

  if (bagusIndices.length > 1) {
    // Remove all but the first Bagus
    const firstBagus = bagusIndices[0]
    result = result.filter((_, i) => i === firstBagus || result[i].character !== 'bagus')
  }

  // Bagus never last
  if (result.length > 0 && result[result.length - 1].character === 'bagus') {
    // Swap with the previous non-Bagus line if possible
    for (let i = result.length - 2; i >= 0; i--) {
      if (result[i].character !== 'bagus') {
        // Move Bagus before this line
        const bagusLine = result[result.length - 1]
        const swapLine = result[i]
        result[result.length - 1] = swapLine
        result[i] = bagusLine
        break
      }
    }
  }

  // Rule 3: Truncate to maxLines
  if (maxLines && result.length > maxLines) {
    result = result.slice(0, maxLines)
  }

  return result
}

// ── Success/generic feedback generators ───────────────────────────────────

const SUCCESS_MESSAGES: DialogueLine[] = [
  { character: 'va', text: 'Верное решение! Ты правильно применил конструкцию.' },
  { character: 'novice', text: 'Отлично, я понял! Работает как надо.' },
]

const FAIL_FALLBACK: DialogueLine[] = [
  { character: 'novice', text: 'Что-то не так... Давай разберёмся.' },
  { character: 'va', text: 'Проверь внимательно: возможно, ошибка в логике или синтаксисе.' },
]

/**
 * Generate a short success dialogue (1-2 lines).
 * Uses any provided successDialogue or falls back to generic messages.
 */
export function getSuccessFeedback(successDialogue?: DialogueLine[]): DialogueLine[] {
  if (successDialogue && successDialogue.length > 0) {
    return enforceCharacterRules(successDialogue.slice(0, 2), 2)
  }
  return enforceCharacterRules(SUCCESS_MESSAGES.slice(0, 1), 1)
}

/**
 * Generate fallback failure feedback when no post_error_dialogue exists.
 */
export function getFailFallback(): DialogueLine[] {
  return enforceCharacterRules(FAIL_FALLBACK)
}

// ── Quest feedback generators ─────────────────────────────────────────────

export function getQuestFailFeedback(attemptCount: number): DialogueLine[] {
  if (attemptCount <= 2) {
    return enforceCharacterRules([
      { character: 'novice', text: 'Хм, не все тесты прошли. Надо подумать...' },
      { character: 'ksyu', text: 'Проверь краевые случаи: что будет при необычном вводе?' },
    ])
  }
  return enforceCharacterRules([
    { character: 'va', text: 'Давай по шагам: проверь каждое условие и тип данных.' },
    { character: 'ksyu', text: 'Обрати внимание на то, что ожидается в каждом тесте.' },
  ])
}

export function getQuestPassFeedback(): DialogueLine[] {
  return enforceCharacterRules([
    { character: 'va', text: 'Все тесты пройдены! Решение корректно.' },
  ])
}

// ── Recap feedback generators ─────────────────────────────────────────────

export function getRecapCorrectFeedback(): DialogueLine[] {
  return [
    { character: 'novice', text: 'Верно! Я это запомнил.' },
  ]
}

export function getRecapIncorrectFeedback(): DialogueLine[] {
  return [
    { character: 'va', text: 'Не совсем. Попробуй ещё раз — подумай, что мы проходили в этой части.' },
  ]
}
