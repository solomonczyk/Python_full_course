import { useState } from 'react'
import type { Lesson, MissionResult } from '../types'
import { CHARACTER_AVATARS } from '../constants'

interface Props {
  mission: Lesson['mission']
  lessonId: string
  onComplete?: (score: number) => void
}

const BASE = '/api'

export default function MissionCard({ mission, lessonId, onComplete }: Props) {
  const [code, setCode] = useState('')
  const [result, setResult] = useState<'idle' | 'checking' | 'success' | 'error'>('idle')
  const [bagusVisible, setBagusVisible] = useState(false)
  const [actualOutput, setActualOutput] = useState<string | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const handleRun = async () => {
    const trimmed = code.trim()
    if (!trimmed) {
      setBagusVisible(true)
      setResult('error')
      setErrorMessage('Напиши код перед запуском')
      return
    }

    setResult('checking')
    setBagusVisible(false)
    setErrorMessage(null)
    setActualOutput(null)

    try {
      const res = await fetch(`${BASE}/mission/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lesson_id: lessonId, code: trimmed }),
      })
      const data: MissionResult = await res.json()

      if (data.correct) {
        setResult('success')
        setBagusVisible(false)
        setActualOutput(data.actual_output)
        onComplete?.(100)
      } else {
        setResult('error')
        setBagusVisible(true)
        setActualOutput(data.actual_output)
        setErrorMessage(data.error ?? null)
      }
    } catch (e) {
      setResult('error')
      setBagusVisible(true)
      setErrorMessage('Ошибка соединения с сервером')
    }
  }

  return (
    <section className="bg-white rounded-3xl shadow-xl border-t-8 border-action-da overflow-hidden">
      <div className="p-8">
        <div className="flex items-center gap-2 mb-1">
          <span className="material-symbols-outlined text-sm text-action-da" style={{ fontVariationSettings: "'FILL' 0" }}>code</span>
          <span className="font-sans text-[13px] font-bold text-action-da tracking-wider">ПРАКТИЧЕСКАЯ ЗАДАЧА</span>
        </div>
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
                  onChange={(e) => { setCode(e.target.value); setResult('idle'); setBagusVisible(false); setErrorMessage(null) }}
                  className="bg-transparent border-none p-0 focus:ring-0 text-white w-full outline-none resize-none font-mono text-[14px] leading-5"
                  style={{ minHeight: '120px', maxHeight: '50vh' }}
                  spellCheck={false}
                  autoFocus
                  onInput={(e) => {
                    const el = e.currentTarget
                    el.style.height = 'auto'
                    el.style.height = Math.min(el.scrollHeight, window.innerHeight * 0.5) + 'px'
                  }}
                />
              </div>
            </div>
          </div>
          {result === 'success' && (
            <div className="border-t border-white/10 px-4 py-3 bg-green-900/30 flex items-center gap-2">
              <span className="material-symbols-outlined text-green-400 text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
              <span className="text-green-400 text-xs font-mono">{actualOutput ?? mission.expected_output}</span>
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
            {result === 'checking' && (
              <>
                <span className="material-symbols-outlined text-secondary text-sm animate-spin" style={{ fontVariationSettings: "'FILL' 0" }}>progress_activity</span>
                <span className="text-xs text-secondary font-sans font-bold tracking-wider">ПРОВЕРКА...</span>
              </>
            )}
            {result === 'success' && (
              <span className="text-sm font-bold text-action-da">🎉 Миссия выполнена!</span>
            )}
          </div>
          <button
            onClick={handleRun}
            disabled={result === 'checking'}
            className="bg-action-da text-white font-display text-[20px] leading-7 font-semibold px-10 py-3 rounded-2xl shadow-lg hover:scale-105 active:scale-95 transition-all flex items-center gap-2 disabled:opacity-60 disabled:hover:scale-100"
          >
            <span>{result === 'checking' ? 'Проверяю...' : 'Запустить миссию'}</span>
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>
              {result === 'checking' ? 'hourglass_top' : 'rocket_launch'}
            </span>
          </button>
        </div>
      </div>

      {bagusVisible && (
        <div className="mx-8 mb-8 bg-error-container text-on-error-container p-4 rounded-xl border-2 border-error-bagus flex gap-4 items-start animate-bounce">
          <div className="shrink-0 w-12 h-12 bg-white rounded-full overflow-hidden border-2 border-error-bagus">
            <img src={CHARACTER_AVATARS.bagus} alt="Багус" className="w-full h-full object-cover" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-sans font-bold text-[13px]">ОЙ! Багус нашёл ошибку!</p>
            <p className="text-sm">
              Ожидалось: <code className="font-mono bg-white/40 px-1 rounded">{mission.expected_output}</code>
              {actualOutput !== null && (
                <> · Получилось: <code className="font-mono bg-white/40 px-1 rounded">{actualOutput}</code></>
              )}
            </p>
            {errorMessage && (
              <p className="text-sm mt-2 bg-error/10 p-2 rounded font-mono text-[12px] leading-4">
                {errorMessage}
              </p>
            )}
          </div>
        </div>
      )}
    </section>
  )
}
