import { useState } from 'react'
import type { Lesson } from '../types'

interface Props {
  mission: Lesson['mission']
  lessonId: string
  onComplete?: (score: number) => void
}

export default function MissionCard({ mission, lessonId, onComplete }: Props) {
  const [code, setCode] = useState('')
  const [result, setResult] = useState<'idle' | 'success' | 'error'>('idle')
  const [bagusVisible, setBagusVisible] = useState(false)

  const handleRun = () => {
    const trimmed = code.trim()
    const expected = mission.expected_output.trim()
    if (!trimmed) {
      setBagusVisible(true)
      setResult('error')
      return
    }

    const isCorrect =
      trimmed === `print("${expected}")` ||
      trimmed === `print('${expected}')` ||
      trimmed.includes(expected)

    if (isCorrect) {
      setResult('success')
      setBagusVisible(false)
      onComplete?.(100)
    } else {
      setResult('error')
      setBagusVisible(true)
    }
  }

  return (
    <section className="bg-white rounded-3xl shadow-xl border-t-8 border-action-da overflow-hidden">
      <div className="p-8">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-12 h-12 bg-action-da rounded-2xl flex items-center justify-center text-white shadow-lg shrink-0">
            <span className="material-symbols-outlined text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>task_alt</span>
          </div>
          <div>
            <h3 className="font-display text-[24px] leading-tight font-bold text-on-surface">{mission.title}</h3>
            <p className="text-on-surface-variant font-medium">{mission.description}</p>
          </div>
        </div>

        <div className="bg-surface-container p-6 rounded-2xl mb-8">
          <div className="flex items-start gap-3">
            <span className="material-symbols-outlined text-secondary shrink-0" style={{ fontVariationSettings: "'FILL' 0" }}>info</span>
            <div className="text-[16px] leading-6 text-on-surface-variant space-y-2">
              <p>{mission.task}</p>
              <div className="bg-white p-3 rounded-lg border border-outline-variant font-mono text-on-surface text-sm">
                {mission.expected_output}
              </div>
            </div>
          </div>
        </div>

        {/* Code editor */}
        <div className="bg-[#1e1e1e] rounded-xl overflow-hidden mb-6">
          <div className="bg-[#333] px-4 py-2 flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
            <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
            <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
            <span className="ml-auto text-[11px] text-gray-400 font-mono uppercase tracking-widest">mission-{lessonId}.py</span>
          </div>
          <div className="p-6 font-mono">
            <div className="flex gap-4">
              <span className="text-gray-600 select-none pt-1">1</span>
              <div className="relative w-full">
                {!code && (
                  <span className="text-white opacity-20 pointer-events-none absolute top-0 left-0 font-mono text-[14px]">
                    # Напиши свой код здесь
                  </span>
                )}
                <textarea
                  value={code}
                  onChange={(e) => { setCode(e.target.value); setResult('idle'); setBagusVisible(false) }}
                  className="bg-transparent border-none p-0 focus:ring-0 text-white w-full outline-none resize-none font-mono text-[14px] leading-5 min-h-[80px]"
                  spellCheck={false}
                  autoFocus
                />
              </div>
            </div>
          </div>
          {result === 'success' && (
            <div className="border-t border-white/10 px-4 py-3 bg-green-900/30 flex items-center gap-2">
              <span className="material-symbols-outlined text-green-400 text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
              <span className="text-green-400 text-xs font-mono">{mission.expected_output}</span>
            </div>
          )}
        </div>

        <div className="flex items-center justify-between">
          <div className="flex gap-2 items-center">
            {result === 'idle' && (
              <>
                <span className="w-3 h-3 rounded-full bg-secondary-container animate-pulse" />
                <span className="text-xs text-on-surface-variant font-sans font-bold tracking-wider">ОЖИДАНИЕ ВВОДА...</span>
              </>
            )}
            {result === 'success' && (
              <span className="text-sm font-bold text-action-da">🎉 Миссия выполнена!</span>
            )}
          </div>
          <button
            onClick={handleRun}
            className="bg-action-da text-white font-display text-[20px] leading-7 font-semibold px-10 py-3 rounded-2xl shadow-lg hover:scale-105 active:scale-95 transition-all flex items-center gap-2"
          >
            <span>Запустить миссию</span>
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>rocket_launch</span>
          </button>
        </div>
      </div>

      {bagusVisible && (
        <div className="mx-8 mb-8 bg-error-container text-on-error-container p-4 rounded-xl border-2 border-error-bagus flex gap-4 items-center animate-bounce">
          <div className="shrink-0 w-12 h-12 bg-white rounded-full flex items-center justify-center text-2xl">🐛</div>
          <div>
            <p className="font-sans font-bold text-[13px]">ОЙ! Багус нашёл ошибку!</p>
            <p className="text-sm">
              Ожидалось: <code className="font-mono bg-white/40 px-1 rounded">{mission.expected_output}</code>. Попробуй ещё раз!
            </p>
          </div>
        </div>
      )}
    </section>
  )
}
