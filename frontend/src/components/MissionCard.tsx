import { useState, useRef } from 'react'
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
  const [expanded, setExpanded] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const lineCount = code.split('\n').length
  const collapsedHeight = Math.min(lineCount * 28 + 40, 160)

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
    <div
      className="rounded-xl overflow-hidden"
      style={{
        background: '#1a1924',
        border: '1px solid rgba(201,162,39,0.15)',
        borderTop: '8px solid #28A745',
      }}
    >
      <div className="p-6">
        <div className="flex items-center gap-2 mb-1">
          <span className="material-symbols-outlined text-sm" style={{ color: '#28A745', fontVariationSettings: "'FILL' 0" }}>code</span>
          <span className="text-[11px] font-bold tracking-wider" style={{ color: '#28A745' }}>ПРАКТИЧЕСКАЯ ЗАДАЧА</span>
        </div>
        <div className="flex items-center gap-3 mb-5">
          <div
            className="w-10 h-10 rounded-lg flex items-center justify-center text-base shrink-0"
            style={{ background: '#28A745', color: '#0f0e17' }}
          >
            🎯
          </div>
          <div>
            <h3 className="text-sm font-bold" style={{ color: '#e8e6f0' }}>{mission.title}</h3>
            <p className="text-[11px]" style={{ color: '#9b98a8' }}>{mission.description}</p>
          </div>
        </div>

        {/* Task info with clear input/output display */}
        <div
          className="rounded-lg p-4 mb-5"
          style={{ background: '#0f0e17', border: '1px solid rgba(201,162,39,0.15)' }}
        >
          <div className="flex items-start gap-3">
            <span className="material-symbols-outlined text-sm shrink-0 mt-0.5" style={{ color: '#c9a227', fontVariationSettings: "'FILL' 0" }}>info</span>
            <div className="text-xs leading-relaxed space-y-3" style={{ color: '#9b98a8' }}>
              <p style={{ color: '#e8e6f0' }}>{mission.task}</p>
              <div>
                <div className="text-[10px] font-bold mb-1 uppercase tracking-wider" style={{ color: '#c9a227' }}>Ожидаемый результат:</div>
                <div
                  className="p-2.5 rounded-lg font-mono text-xs"
                  style={{
                    background: '#0d0c14',
                    border: '1px solid rgba(0,212,170,0.2)',
                    color: '#00d4aa',
                  }}
                >
                  {mission.expected_output}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Code editor with expand */}
        <div
          className="rounded-lg overflow-hidden mb-5"
          style={{
            background: '#0d0c14',
            border: result === 'success' ? '1px solid #00d4aa' : '1px solid rgba(0,212,170,0.2)',
          }}
        >
          {/* Terminal header */}
          <div
            className="flex items-center justify-between px-3 py-1.5"
            style={{
              background: 'rgba(0,212,170,0.05)',
              borderBottom: '1px solid rgba(0,212,170,0.1)',
            }}
          >
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ff5f56' }} />
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ffbd2e' }} />
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#27c93f' }} />
              </div>
              <span className="text-[10px]" style={{ color: '#9b98a8' }}>mission-{lessonId}.py</span>
            </div>
            <button
              onClick={() => setExpanded(!expanded)}
              className="flex items-center gap-1 text-[10px] cursor-pointer transition-all hover:opacity-80"
              style={{ color: '#9b98a8', background: 'none', border: 'none' }}
              title={expanded ? 'Свернуть' : 'Развернуть'}
            >
              <span className="material-symbols-outlined text-[14px]" style={{ fontVariationSettings: "'FILL' 0" }}>
                {expanded ? 'fullscreen_exit' : 'fullscreen'}
              </span>
              {expanded ? 'Свернуть' : 'На весь экран'}
            </button>
          </div>

          {/* Code area */}
          <div className="relative">
            <div className="flex" style={{ minHeight: expanded ? '400px' : `${collapsedHeight}px` }}>
              <div className="p-3 pr-2 text-right font-mono text-xs leading-7 select-none shrink-0" style={{ color: '#6b7280', minWidth: '32px' }}>
                {code.split('\n').map((_, i) => (
                  <div key={i}>{i + 1}</div>
                ))}
                {!code && <div>1</div>}
              </div>
              <textarea
                ref={textareaRef}
                value={code}
                onChange={(e) => { setCode(e.target.value); setResult('idle'); setBagusVisible(false); setErrorMessage(null) }}
                className="w-full p-3 pl-2 font-mono text-xs leading-7 resize-none outline-none"
                style={{
                  minHeight: expanded ? '400px' : `${collapsedHeight}px`,
                  background: '#0d0c14',
                  color: '#e8e6f0',
                  border: 'none',
                }}
                spellCheck={false}
                placeholder="# Напиши свой код здесь"
              />
            </div>

            {/* Scroll indicator */}
            {!expanded && lineCount > 6 && (
              <div
                className="absolute bottom-0 left-0 right-0 h-8 pointer-events-none flex items-end justify-center pb-1"
                style={{ background: 'linear-gradient(transparent, rgba(13,12,20,0.9))' }}
              >
                <span className="text-[10px] animate-pulse" style={{ color: '#9b98a8' }}>
                  ⋮ скроль или разверни
                </span>
              </div>
            )}
          </div>

          {/* Success output */}
          {result === 'success' && (
            <div className="px-3 py-2 flex items-center gap-2" style={{ background: 'rgba(0,212,170,0.1)', borderTop: '1px solid rgba(0,212,170,0.2)' }}>
              <span className="material-symbols-outlined text-xs" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>check_circle</span>
              <span className="text-xs font-mono" style={{ color: '#00d4aa' }}>{actualOutput ?? mission.expected_output}</span>
            </div>
          )}
        </div>

        {/* Buttons */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {result === 'idle' && (
              <>
                <span className="w-2 h-2 rounded-full animate-pulse" style={{ background: '#c9a227' }} />
                <span className="text-[10px] font-bold tracking-wider" style={{ color: '#9b98a8' }}>ОЖИДАНИЕ ВВОДА...</span>
              </>
            )}
            {result === 'checking' && (
              <>
                <span className="material-symbols-outlined text-sm animate-spin" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 0" }}>progress_activity</span>
                <span className="text-[10px] font-bold tracking-wider" style={{ color: '#00d4aa' }}>ПРОВЕРКА...</span>
              </>
            )}
            {result === 'success' && (
              <span className="text-xs font-bold" style={{ color: '#00d4aa' }}>🎉 Миссия выполнена!</span>
            )}
          </div>
          <button
            onClick={handleRun}
            disabled={result === 'checking'}
            className="flex items-center gap-2 px-6 py-2.5 rounded-lg text-xs font-bold cursor-pointer transition-all hover:scale-105 active:scale-95 border-none disabled:opacity-60 disabled:hover:scale-100"
            style={{
              background: result === 'success' ? '#00d4aa' : 'linear-gradient(135deg, #c9a227, #8b7355)',
              color: '#0f0e17',
            }}
          >
            <span>{result === 'checking' ? 'Проверяю...' : 'Запустить миссию'}</span>
            <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>
              {result === 'checking' ? 'hourglass_top' : 'rocket_launch'}
            </span>
          </button>
        </div>
      </div>

      {/* Bagus error feedback */}
      {bagusVisible && (
        <div
          className="mx-6 mb-6 p-4 rounded-xl flex gap-4 items-start animate-bounce"
          style={{
            background: 'rgba(255,107,107,0.1)',
            border: '2px solid #ff6b6b',
          }}
        >
          <div className="shrink-0 w-10 h-10 rounded-full overflow-hidden" style={{ border: '2px solid #ff6b6b' }}>
            <img src={CHARACTER_AVATARS.bagus} alt="Багус" className="w-full h-full object-cover" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-bold" style={{ color: '#ff6b6b' }}>ОЙ! Багус нашёл ошибку!</p>
            <p className="text-[11px] mt-1" style={{ color: '#e8e6f0' }}>
              Ожидалось: <code className="font-mono px-1 rounded" style={{ background: 'rgba(255,107,107,0.2)', color: '#ff6b6b' }}>{mission.expected_output}</code>
              {actualOutput !== null && (
                <> · Получилось: <code className="font-mono px-1 rounded" style={{ background: 'rgba(255,107,107,0.2)', color: '#ff6b6b' }}>{actualOutput}</code></>
              )}
            </p>
            {errorMessage && (
              <p className="text-[11px] mt-2 p-2 rounded font-mono" style={{ background: 'rgba(255,107,107,0.05)', color: '#ff6b6b' }}>
                {errorMessage}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
