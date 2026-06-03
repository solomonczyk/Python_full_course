/**
 * ParticipantCodePanel — Displays the participant's beta code
 *
 * Shows the generated BETA-XXXXXX code with instructions to save it.
 * No personal data displayed.
 */

import { useState } from 'react'

interface Props {
  participantCode: string
  onContinue: () => void
}

export default function ParticipantCodePanel({ participantCode, onContinue }: Props) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(participantCode)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // Clipboard API not available — fallback: select the text
    }
  }

  return (
    <div
      className="rounded-xl p-6 sm:p-8 text-center space-y-5"
      style={{
        background: '#1a1924',
        border: '2px solid rgba(201,162,39,0.3)',
        boxShadow: '0 0 30px rgba(201,162,39,0.08)',
      }}
    >
      {/* Icon */}
      <div
        className="w-14 h-14 rounded-full flex items-center justify-center mx-auto"
        style={{ background: 'rgba(201,162,39,0.15)' }}
      >
        <span className="text-2xl">🔑</span>
      </div>

      {/* Title */}
      <div>
        <h3 className="text-base font-bold mb-1" style={{ color: '#e8e6f0' }}>
          Ваш beta-код создан!
        </h3>
        <p className="text-xs" style={{ color: '#9b98a8' }}>
          Сохраните этот код, чтобы продолжить обучение позже.
        </p>
      </div>

      {/* Code display */}
      <div
        className="inline-block px-6 py-3 rounded-lg font-mono text-xl font-bold tracking-widest select-all"
        style={{
          background: '#0f0e17',
          border: '1px solid rgba(201,162,39,0.4)',
          color: '#c9a227',
          letterSpacing: '0.15em',
        }}
      >
        {participantCode}
      </div>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
        <button
          onClick={handleCopy}
          className="px-5 py-2.5 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:opacity-80"
          style={{
            background: 'transparent',
            border: '1px solid rgba(201,162,39,0.3)',
            color: '#c9a227',
          }}
        >
          {copied ? '✓ Скопировано!' : 'Копировать код'}
        </button>

        <button
          onClick={onContinue}
          className="px-6 py-2.5 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:opacity-90 active:scale-[0.97]"
          style={{
            background: 'linear-gradient(135deg, #c9a227, #b8922a)',
            color: '#0f0e17',
          }}
        >
          Продолжить обучение →
        </button>
      </div>

      {/* Warning */}
      <p className="text-[11px] leading-relaxed" style={{ color: '#6b7280' }}>
        ⚠️ В этой beta-версии прогресс сохраняется в этом браузере.
        Для продолжения используйте тот же браузер и сохраните beta-код.
      </p>
    </div>
  )
}
