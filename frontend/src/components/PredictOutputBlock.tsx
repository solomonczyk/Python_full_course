import { useState } from 'react'
import type { Lesson } from '../types'

interface Props {
  whatOutputs: Lesson['what_outputs']
  onAnswer?: (correct: boolean, answer: string) => void
}

export default function PredictOutputBlock({ whatOutputs, onAnswer }: Props) {
  const [selected, setSelected] = useState<string | null>(null)

  if (!whatOutputs) return null

  const handleClick = (opt: string) => {
    if (selected !== null) return // already answered
    setSelected(opt)
    onAnswer?.(opt === whatOutputs.correct, opt)
  }

  return (
    <section className="bg-white rounded-2xl p-6 shadow-sm border border-outline-variant">
      <div className="flex items-center gap-3 mb-5">
        <div className="w-10 h-10 bg-tertiary/10 rounded-xl flex items-center justify-center text-tertiary">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>visibility</span>
        </div>
        <h3 className="font-display text-[20px] leading-7 font-bold text-on-surface">Что выведет код?</h3>
      </div>

      {/* Code display */}
      <div className="bg-[#1e1e1e] rounded-xl overflow-hidden mb-5">
        <div className="bg-[#333] px-4 py-2 flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
          <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
          <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
          <span className="ml-auto text-[11px] text-gray-400 font-mono">predict.py</span>
        </div>
        <div className="p-5 font-mono text-[14px] leading-5 text-green-400 whitespace-pre">{whatOutputs.code}</div>
      </div>

      {/* Answer options */}
      <div className="flex gap-3 flex-wrap">
        {whatOutputs.options.map((opt) => {
          const isSelected = selected === opt
          const isCorrect = opt === whatOutputs.correct
          let borderColor = 'border-outline-variant hover:border-secondary hover:bg-secondary/5'
          if (isSelected) {
            borderColor = isCorrect
              ? 'border-action-da bg-green-50'
              : 'border-error bg-red-50'
          } else if (selected !== null && isCorrect) {
            borderColor = 'border-action-da bg-green-50' // show correct answer after selection
          }

          return (
            <button
              key={opt}
              onClick={() => handleClick(opt)}
              disabled={selected !== null}
              className={`flex-1 min-w-[80px] py-3 px-4 rounded-xl border-2 font-mono text-[14px] font-bold whitespace-pre-wrap text-center transition-all
                ${borderColor}
                ${selected !== null ? 'cursor-default' : 'active:scale-[0.97]'}
                ${isSelected && isCorrect ? 'text-action-da' : isSelected && !isCorrect ? 'text-error' : 'text-on-surface'}
              `}
            >
              {opt}
            </button>
          )
        })}
      </div>

      {/* Result feedback */}
      {selected && (
        <div className={`mt-4 p-3 rounded-xl font-sans text-[14px] font-bold ${
          selected === whatOutputs.correct
            ? 'bg-green-50 text-action-da'
            : 'bg-red-50 text-error'
        }`}>
          {selected === whatOutputs.correct
            ? '✅ Верно!'
            : `❌ Неверно. Правильный вывод:\n${whatOutputs.correct}`
          }
        </div>
      )}
    </section>
  )
}
