import { useState } from 'react'
import type { Lesson } from '../types'

interface Props {
  findBug: Lesson['find_bug']
}

export default function FindBugBlock({ findBug }: Props) {
  const [code, setCode] = useState(findBug?.code ?? '')
  const [status, setStatus] = useState<'idle' | 'correct' | 'wrong' | 'hint'>('idle')

  if (!findBug) return null

  const handleCheck = () => {
    if (!findBug.correct) {
      setStatus('hint')
      return
    }
    // Normalize: trim, collapse spaces, unify quotes (both ' and " are valid Python)
    const normalize = (s: string) =>
      s.trim().replace(/\s+/g, ' ').replace(/'/g, '"')
    const normalizedCode = normalize(code)
    const normalizedCorrect = normalize(findBug.correct)
    setStatus(normalizedCode === normalizedCorrect ? 'correct' : 'wrong')
  }

  const handleReset = () => {
    setCode(findBug.code)
    setStatus('idle')
  }

  return (
    <section className="bg-error-container/20 rounded-2xl p-6 border border-error-bagus/30 relative overflow-hidden">
      <div className="flex items-center gap-3 mb-5">
        <div className="w-10 h-10 bg-error/10 rounded-xl flex items-center justify-center text-error">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>bug_report</span>
        </div>
        <h3 className="font-display text-[20px] leading-7 font-bold text-on-surface">Найди ошибку</h3>
      </div>

      <p className="text-[15px] leading-[22px] text-on-surface-variant mb-4">{findBug.description}</p>

      {/* Editable code field */}
      <div className="relative">
        <textarea
          value={code}
          onChange={(e) => { setCode(e.target.value); setStatus('idle') }}
          className={`w-full p-5 rounded-xl font-mono text-[14px] leading-6 border-2 bg-white resize-y min-h-[80px]
            ${status === 'correct'
              ? 'border-action-da bg-green-50'
              : status === 'wrong'
                ? 'border-error bg-red-50'
                : 'border-outline-variant focus:border-secondary focus:bg-blue-50/30'
            }
            transition-colors outline-none`}
          spellCheck={false}
          placeholder="Исправь код здесь..."
        />
        <span className="absolute top-2 right-2 text-[11px] text-outline font-sans flex items-center gap-1 pointer-events-none">
          <span className="material-symbols-outlined text-[14px]" style={{ fontVariationSettings: "'FILL' 0" }}>edit</span>
          редактируй
        </span>
      </div>

      {/* Buttons */}
      <div className="flex gap-3 mt-4">
        <button
          onClick={handleCheck}
          disabled={status === 'correct'}
          className="flex-1 py-3 bg-error-bagus text-white font-sans text-[13px] font-bold rounded-xl
                     hover:opacity-90 active:scale-[0.98] transition-all
                     disabled:opacity-50 disabled:cursor-default"
        >
          {findBug.correct ? 'Проверить' : 'Показать подсказку'}
        </button>
        <button
          onClick={handleReset}
          className="py-3 px-5 bg-white text-on-surface-variant font-sans text-[13px] font-bold rounded-xl
                     border-2 border-outline-variant hover:border-secondary active:scale-[0.98] transition-all"
        >
          Сбросить
        </button>
      </div>

      {/* Feedback */}
      {status === 'correct' && (
        <div className="mt-4 p-4 bg-green-50 rounded-xl border border-action-da">
          <p className="font-sans text-[14px] font-bold text-action-da">✅ Верно! Ошибка исправлена.</p>
        </div>
      )}
      {status === 'wrong' && (
        <div className="mt-4 p-4 bg-red-50 rounded-xl border border-error">
          <p className="font-sans text-[14px] font-bold text-error mb-2">❌ Ещё не так. Попробуй ещё раз.</p>
          {findBug.hint && (
            <p className="text-sm text-on-surface"><span className="font-bold">💡 Подсказка:</span> {findBug.hint}</p>
          )}
        </div>
      )}
      {status === 'hint' && findBug.hint && (
        <div className="mt-4 p-4 bg-white/80 rounded-xl border border-error-bagus/30">
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
