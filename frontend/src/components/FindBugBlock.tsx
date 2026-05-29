import { useState } from 'react'
import type { Lesson } from '../types'

interface Props {
  findBug: Lesson['find_bug']
}

export default function FindBugBlock({ findBug }: Props) {
  const [showHint, setShowHint] = useState(false)

  if (!findBug) return null

  return (
    <section className="bg-error-container/20 rounded-2xl p-6 border border-error-bagus/30 relative overflow-hidden">
      <div className="flex items-center gap-3 mb-5">
        <div className="w-10 h-10 bg-error/10 rounded-xl flex items-center justify-center text-error">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>bug_report</span>
        </div>
        <h3 className="font-display text-[20px] leading-7 font-bold text-on-surface">Найди ошибку</h3>
      </div>

      <p className="text-[15px] leading-[22px] text-on-surface-variant mb-4">{findBug.description}</p>

      {/* Code with error marker */}
      <div className="bg-white/80 p-5 rounded-xl font-mono text-[14px] leading-5 border-l-4 border-error text-on-surface mb-4">
        {findBug.code}
      </div>

      {!showHint ? (
        <button
          onClick={() => setShowHint(true)}
          className="w-full py-3 bg-error-bagus/10 text-error font-sans text-[13px] font-bold rounded-xl
                     hover:bg-error-bagus/20 active:scale-[0.98] transition-all"
        >
          Показать подсказку
        </button>
      ) : (
        <div className="p-4 bg-white/80 rounded-xl border border-error-bagus/30">
          <p className="text-sm text-on-surface"><span className="font-bold">💡 Подсказка:</span> {findBug.hint}</p>
        </div>
      )}

      {/* Decorative icon */}
      <div className="absolute -right-4 -bottom-4 w-20 h-20 opacity-[0.06] pointer-events-none">
        <span className="material-symbols-outlined text-7xl text-error">dangerous</span>
      </div>
    </section>
  )
}
