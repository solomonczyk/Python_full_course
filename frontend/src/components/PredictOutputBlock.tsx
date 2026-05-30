import { useState, useMemo } from 'react'
import type { Lesson } from '../types'

interface Props {
  whatOutputs: Lesson['what_outputs']
  onAnswer?: (correct: boolean, answer: string) => void
}

/** Fisher-Yates shuffle */
function shuffle<T>(arr: T[]): T[] {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

export default function PredictOutputBlock({ whatOutputs, onAnswer }: Props) {
  const [selected, setSelected] = useState<string | null>(null)
  const [attempt, setAttempt] = useState(0)

  // Shuffle options on mount and on each retry, keyed by attempt
  const shuffledOptions = useMemo(
    () => shuffle(whatOutputs?.options ?? []),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [whatOutputs?.code, attempt]
  )

  if (!whatOutputs) return null

  const handleClick = (opt: string) => {
    if (selected !== null) return
    setSelected(opt)
    onAnswer?.(opt === whatOutputs.correct, opt)
  }

  const handleRetry = () => {
    setSelected(null)
    setAttempt((a) => a + 1)
  }

  return (
    <div
      className="rounded-xl p-4"
      style={{
        background: 'rgba(0,0,0,0.15)',
        border: '1px solid rgba(201,162,39,0.15)',
      }}
    >
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-sm" style={{ color: '#c9a227', fontVariationSettings: "'FILL' 0" }}>visibility</span>
        <h3 className="text-xs font-bold" style={{ color: '#c9a227' }}>Что выведет код?</h3>
      </div>

      {/* Code display */}
      <div
        className="rounded-lg overflow-hidden mb-4"
        style={{ background: '#0d0c14', border: '1px solid rgba(0,212,170,0.2)' }}
      >
        <div
          className="flex items-center gap-1.5 px-3 py-1.5"
          style={{ background: 'rgba(0,212,170,0.05)', borderBottom: '1px solid rgba(0,212,170,0.1)' }}
        >
          <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ff5f56' }} />
          <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ffbd2e' }} />
          <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#27c93f' }} />
          <span className="ml-auto text-[10px]" style={{ color: '#9b98a8' }}>predict.py</span>
        </div>
        <div className="p-4 font-mono text-xs leading-5 whitespace-pre" style={{ color: '#4ade80' }}>
          {whatOutputs.code}
        </div>
      </div>

      {/* Answer options — shuffled */}
      <div className="flex gap-2 flex-wrap">
        {shuffledOptions.map((opt) => {
          const isSelected = selected === opt
          const isCorrect = opt === whatOutputs.correct

          return (
            <button
              key={opt + String(attempt)}
              onClick={() => handleClick(opt)}
              disabled={selected !== null}
              className="flex-1 min-w-[80px] py-2.5 px-3 rounded-lg font-mono text-xs font-bold whitespace-pre-wrap text-center transition-all border-2"
              style={{
                borderColor: isSelected
                  ? isCorrect ? '#00d4aa' : '#ff6b6b'
                  : selected !== null && isCorrect
                    ? '#00d4aa'
                    : 'rgba(201,162,39,0.2)',
                background: isSelected
                  ? isCorrect ? 'rgba(0,212,170,0.15)' : 'rgba(255,107,107,0.15)'
                  : selected !== null && isCorrect
                    ? 'rgba(0,212,170,0.1)'
                    : 'transparent',
                color: isSelected
                  ? isCorrect ? '#00d4aa' : '#ff6b6b'
                  : selected !== null && isCorrect
                    ? '#00d4aa'
                    : '#e8e6f0',
                cursor: selected !== null ? 'default' : 'pointer',
              }}
            >
              {opt}
            </button>
          )
        })}
      </div>

      {/* Result feedback */}
      {selected && (
        <div className="flex items-center justify-between mt-4">
          <div
            className="text-xs font-bold"
            style={{
              color: selected === whatOutputs.correct ? '#00d4aa' : '#ff6b6b',
            }}
          >
            {selected === whatOutputs.correct
              ? '✅ Верно!'
              : `❌ Неверно. Правильный вывод: ${whatOutputs.correct}`
            }
          </div>
          <button
            onClick={handleRetry}
            className="text-xs font-bold cursor-pointer transition-all hover:scale-105 active:scale-95"
            style={{
              color: '#0f0e17',
              background: '#c9a227',
              border: 'none',
              borderRadius: '8px',
              padding: '6px 14px',
            }}
          >
            ↻ Ещё попытка
          </button>
        </div>
      )}
    </div>
  )
}
