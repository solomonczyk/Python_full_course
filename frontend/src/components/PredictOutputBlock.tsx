import type { Lesson } from '../types'

interface Props {
  whatOutputs: Lesson['what_outputs']
  onAnswer?: (correct: boolean, answer: string) => void
}

export default function PredictOutputBlock({ whatOutputs, onAnswer }: Props) {
  if (!whatOutputs) return null

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
        {whatOutputs.options.map((opt) => (
          <button
            key={opt}
            onClick={() => onAnswer?.(opt === whatOutputs.correct, opt)}
            className="flex-1 min-w-[80px] py-3 px-4 rounded-xl border-2 border-outline-variant
                       font-sans text-[14px] font-bold text-on-surface
                       hover:border-secondary hover:bg-secondary/5
                       active:scale-[0.97] transition-all"
          >
            {opt}
          </button>
        ))}
      </div>
    </section>
  )
}
