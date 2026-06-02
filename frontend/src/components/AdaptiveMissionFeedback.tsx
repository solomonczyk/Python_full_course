import type {
  FeedbackState,
  AdaptiveFeedbackConfig,
  MissionResult,
  DialogueLine,
  ErrorCategory,
} from '../types'
import DialogueScene from './DialogueScene'
import {
  categorizeError,
  ERROR_META,
  selectProgressiveHints,
  enforceCharacterRules,
  getSuccessFeedback,
  getFailFallback,
} from '../utils/feedbackContent'

interface Props {
  config: AdaptiveFeedbackConfig
  state: FeedbackState
  attemptCount: number
  result?: MissionResult | null
  /** If true, the component was used for quest/recap (no input changes to reset) */
  standalone?: boolean
}

const STATE_LABELS: Record<FeedbackState, { icon: string; text: string; color: string } | null> = {
  not_started: null,
  attempted: null,
  checking: { icon: 'progress_activity', text: 'Проверка...', color: '#00d4aa' },
  failed: null,
  passed: null,
}

/**
 * AdaptiveMissionFeedback — центральный компонент адаптивной обратной связи.
 *
 * Отображает диалоги персонажей в зависимости от состояния проверки:
 * - not_started: краткая подсказка (1 строка из preAttemptHint)
 * - attempted: ничего (пользователь печатает)
 * - checking: индикатор загрузки
 * - failed: прогрессивные подсказки из post_error_dialogue + категория ошибки
 * - passed: короткое поздравление
 */
export default function AdaptiveMissionFeedback({
  config,
  state,
  attemptCount,
  result,
}: Props) {
  // 1. Checking state: show spinner
  if (state === 'checking') {
    const label = STATE_LABELS.checking!
    return (
      <div
        className="rounded-xl p-4 flex items-center gap-3"
        style={{
          background: 'rgba(0,212,170,0.05)',
          border: '1px solid rgba(0,212,170,0.2)',
        }}
      >
        <span
          className="material-symbols-outlined text-sm animate-spin"
          style={{ color: label.color, fontVariationSettings: "'FILL' 0" }}
        >
          {label.icon}
        </span>
        <span className="text-xs font-bold" style={{ color: label.color }}>
          {label.text}
        </span>
      </div>
    )
  }

  // 2. Not started: show 1 short hint line
  if (state === 'not_started') {
    const hintLines = config.preAttemptHint ?? []
    if (hintLines.length === 0) return null

    const safeLines = enforceCharacterRules(hintLines.slice(0, 1), 1)
    if (safeLines.length === 0) return null

    return (
      <div
        className="rounded-xl overflow-hidden"
        style={{
          background: '#1a1924',
          border: '1px solid rgba(201,162,39,0.15)',
        }}
      >
        <DialogueScene lines={safeLines} />
      </div>
    )
  }

  // 3. Attempted: no feedback while typing
  if (state === 'attempted') return null

  // 4. Passed: short success dialogue
  if (state === 'passed') {
    const lines = getSuccessFeedback(config.successDialogue)
    if (lines.length === 0) return null

    return (
      <div
        className="rounded-xl overflow-hidden"
        style={{
          background: 'rgba(0,212,170,0.05)',
          border: '1px solid rgba(0,212,170,0.3)',
        }}
      >
        <div
          className="px-4 pt-3 pb-1 flex items-center gap-2"
          style={{ borderBottom: '1px solid rgba(0,212,170,0.1)' }}
        >
          <span
            className="material-symbols-outlined text-sm"
            style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}
          >
            check_circle
          </span>
          <span className="text-[10px] font-bold uppercase tracking-wider" style={{ color: '#00d4aa' }}>
            Миссия выполнена!
          </span>
        </div>
        <DialogueScene lines={lines} />
      </div>
    )
  }

  // 5. Failed: progressive hints + error category
  if (state === 'failed') {
    const errorCategory: ErrorCategory = result
      ? categorizeError(result)
      : 'unknown'

    const errorMeta = ERROR_META[errorCategory]

    // Select progressive hints from post_error_dialogue
    let feedbackLines: DialogueLine[] = []
    if (config.failDialogue && config.failDialogue.length > 0) {
      feedbackLines = selectProgressiveHints(config.failDialogue, attemptCount)
    } else {
      feedbackLines = getFailFallback()
    }

    // Enforce character rules
    const safeLines = enforceCharacterRules(feedbackLines)

    // Attempt count label
    const attemptLabel =
      attemptCount === 1
        ? 'Первая попытка'
        : attemptCount === 2
          ? 'Вторая попытка'
          : `Попытка ${attemptCount}`

    return (
      <div
        className="rounded-xl overflow-hidden"
        style={{
          background: '#1a1924',
          border: '2px solid rgba(255,107,107,0.3)',
        }}
      >
        {/* Error header with category */}
        <div
          className="px-4 py-2 flex items-center gap-2"
          style={{
            background: 'rgba(255,107,107,0.08)',
            borderBottom: '1px solid rgba(255,107,107,0.15)',
          }}
        >
          <span
            className="material-symbols-outlined text-sm"
            style={{ color: '#ff6b6b', fontVariationSettings: "'FILL' 0" }}
          >
            {errorMeta.icon}
          </span>
          <span className="text-xs font-bold" style={{ color: '#ff6b6b' }}>
            {errorMeta.label}
          </span>
          <span className="text-[10px] ml-auto" style={{ color: '#9b98a8' }}>
            {attemptLabel}
          </span>
        </div>

        {/* Attempt counter bar (visual) */}
        <div
          className="px-4 py-1.5 flex items-center gap-2"
          style={{ background: 'rgba(255,107,107,0.03)' }}
        >
          <div className="flex gap-1">
            {[1, 2, 3].map(i => (
              <div
                key={i}
                className="w-2 h-2 rounded-full"
                style={{
                  background: i <= attemptCount ? '#ff6b6b' : 'rgba(255,107,107,0.2)',
                  opacity: i <= attemptCount ? 1 : 0.4,
                }}
              />
            ))}
          </div>
          <span className="text-[10px]" style={{ color: '#9b98a8' }}>
            {attemptCount <= 1
              ? 'Подсказка: проверь внимательно'
              : attemptCount <= 2
                ? 'Подсказка: обрати внимание на детали'
                : 'Подсказка: почти готовое решение'}
          </span>
        </div>

        {/* Dialogue lines */}
        {safeLines.length > 0 && <DialogueScene lines={safeLines} />}
      </div>
    )
  }

  return null
}
