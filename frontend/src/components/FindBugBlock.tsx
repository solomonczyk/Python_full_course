import { useState, useRef } from 'react'
import type { Lesson } from '../types'
import { CHARACTER_AVATARS } from '../constants'

interface Props {
  findBug: Lesson['find_bug']
}

export default function FindBugBlock({ findBug }: Props) {
  const [code, setCode] = useState(findBug?.code ?? '')
  const [status, setStatus] = useState<'idle' | 'correct' | 'wrong' | 'hint'>('idle')
  const [expanded, setExpanded] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  if (!findBug) return null

  const handleCheck = () => {
    if (!findBug.correct) {
      setStatus('hint')
      return
    }
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

  const lineCount = code.split('\n').length
  const collapsedHeight = Math.min(lineCount * 28 + 40, 180)
  const expandedHeight = Math.max(collapsedHeight, 400)

  return (
    <div
      className="rounded-xl p-4 relative overflow-hidden"
      style={{
        background: 'rgba(255,107,107,0.05)',
        border: '1px solid rgba(255,107,107,0.25)',
      }}
    >
      {/* Header */}
      <div className="flex items-center gap-2.5 mb-3">
        <div
          className="w-9 h-9 rounded-full overflow-hidden shrink-0"
          style={{ border: '2px solid #ff6b6b' }}
        >
          <img
            src={CHARACTER_AVATARS.bagus}
            alt="Bagus"
            className="w-full h-full object-cover"
          />
        </div>
        <div>
          <h3 className="text-xs font-bold" style={{ color: '#ff6b6b' }}>Glitch's Trap!</h3>
          <p className="text-[10px]" style={{ color: '#9b98a8' }}>A chaotic error has appeared...</p>
        </div>
      </div>

      <p className="text-xs leading-relaxed mb-3" style={{ color: '#9b98a8' }}>
        {findBug.description}
      </p>

      {/* Code terminal */}
      <div
        className="rounded-lg overflow-hidden"
        style={{
          background: '#0d0c14',
          border: `1px solid ${status === 'correct' ? '#00d4aa' : status === 'wrong' ? '#ff6b6b' : 'rgba(255,107,107,0.2)'}`,
        }}
      >
        {/* Terminal header */}
        <div
          className="flex items-center justify-between px-3 py-1.5"
          style={{
            background: 'rgba(255,107,107,0.08)',
            borderBottom: '1px solid rgba(255,107,107,0.15)',
          }}
        >
          <div className="flex items-center gap-2">
            <div className="flex gap-1">
              <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ff5f56' }} />
              <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ffbd2e' }} />
              <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#27c93f' }} />
            </div>
            <span className="text-[10px]" style={{ color: '#9b98a8' }}>bug_report.py — /tmp</span>
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
          <textarea
            ref={textareaRef}
            value={code}
            onChange={(e) => { setCode(e.target.value); setStatus('idle') }}
            className="w-full p-3 font-mono text-xs leading-7 resize-none outline-none"
            style={{
              minHeight: expanded ? '400px' : `${collapsedHeight}px`,
              background: '#0d0c14',
              color: '#e8e6f0',
              border: 'none',
            }}
            spellCheck={false}
            placeholder="Fix the code here..."
          />

          {/* Scroll indicator (only visible when not expanded and content overflows) */}
          {!expanded && lineCount > 6 && (
            <div
              className="absolute bottom-0 left-0 right-0 h-8 pointer-events-none flex items-end justify-center pb-1"
              style={{
                background: 'linear-gradient(transparent, rgba(13,12,20,0.9))',
              }}
            >
              <span className="text-[10px] animate-pulse" style={{ color: '#9b98a8' }}>
                ⋮ ещё {lineCount - 5} строк · скроль или разверни
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Buttons */}
      <div className="flex gap-2 mt-3">
        <button
          onClick={handleCheck}
          disabled={status === 'correct'}
          className="flex-1 py-2.5 rounded-lg text-xs font-bold cursor-pointer transition-all hover:opacity-90 border-none disabled:opacity-50 disabled:cursor-default"
          style={{
            background: '#ff6b6b',
            color: '#0f0e17',
          }}
        >
          {findBug.correct ? '🔍 Проверить' : '💡 Подсказка'}
        </button>
        <button
          onClick={handleReset}
          className="py-2.5 px-4 rounded-lg text-xs font-bold cursor-pointer transition-all hover:opacity-80"
          style={{
            background: 'transparent',
            border: '1px solid rgba(255,107,107,0.3)',
            color: '#ff6b6b',
          }}
        >
          ↻ Сбросить
        </button>
      </div>

      {/* Feedback */}
      {status === 'correct' && (
        <div className="mt-3 p-3 rounded-lg text-xs font-bold" style={{ background: 'rgba(0,212,170,0.15)', border: '1px solid #00d4aa', color: '#00d4aa' }}>
          ✅ Верно! Ошибка исправлена.
        </div>
      )}
      {status === 'wrong' && (
        <div className="mt-3 p-3 rounded-lg" style={{ background: 'rgba(255,107,107,0.1)', border: '1px solid #ff6b6b' }}>
          <p className="text-xs font-bold mb-1" style={{ color: '#ff6b6b' }}>❌ Ещё не так. Попробуй ещё раз.</p>
          {findBug.hint && (
            <p className="text-[11px] leading-relaxed" style={{ color: '#e8e6f0' }}>
              <span className="font-bold" style={{ color: '#ffd700' }}>💡 Подсказка:</span> {findBug.hint}
            </p>
          )}
        </div>
      )}
      {status === 'hint' && findBug.hint && (
        <div className="mt-3 p-3 rounded-lg" style={{ background: 'rgba(201,162,39,0.1)', border: '1px solid rgba(201,162,39,0.3)' }}>
          <p className="text-[11px] leading-relaxed" style={{ color: '#e8e6f0' }}>
            <span className="font-bold" style={{ color: '#ffd700' }}>💡 Подсказка:</span> {findBug.hint}
          </p>
        </div>
      )}

      {/* Scrollable indicator in footer */}
      {!expanded && lineCount > 6 && (
        <div className="flex justify-center mt-2">
          <button
            onClick={() => setExpanded(true)}
            className="text-[10px] cursor-pointer transition-all hover:opacity-80"
            style={{ color: '#ff6b6b', background: 'none', border: 'none', textDecoration: 'underline dotted' }}
          >
            ⬇ Показать все {lineCount} строк
          </button>
        </div>
      )}
    </div>
  )
}
