import { useState } from 'react'
import type { TaskPresentation } from '../types'
import CodePanel from './CodePanel'

interface Props {
  presentation: TaskPresentation
}

export default function TaskPresentationBlock({ presentation }: Props) {
  const [showWhatIf, setShowWhatIf] = useState(false)
  const [showSolutions, setShowSolutions] = useState(false)

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center gap-2 pb-2" style={{ borderBottom: '1px solid rgba(255,118,117,0.2)' }}>
        <span className="material-symbols-outlined text-sm" style={{ color: '#ff6b6b', fontVariationSettings: "'FILL' 1" }}>assignment</span>
        <h3 className="text-xs font-bold" style={{ color: '#ff6b6b' }}>{presentation.title}</h3>
      </div>

      {/* Description */}
      <p className="text-xs leading-relaxed" style={{ color: '#9b98a8' }}>
        {presentation.description}
      </p>

      {/* Initial code */}
      <div>
        <div className="text-[10px] font-bold mb-1" style={{ color: '#9b98a8' }}>Начальный код:</div>
        <CodePanel code={presentation.initial_code} filename="task.py" />
      </div>

      {/* Expected output */}
      <div
        className="rounded-lg p-3"
        style={{
          background: 'rgba(0,212,170,0.05)',
          border: '1px solid rgba(0,212,170,0.15)',
        }}
      >
        <span className="text-[10px] font-bold" style={{ color: '#00d4aa' }}>Ожидаемый результат:</span>
        <div className="mt-1 font-mono text-xs" style={{ color: '#00d4aa' }}>
          {presentation.expected_output}
        </div>
      </div>

      {/* What-if scenarios */}
      {presentation.what_if && presentation.what_if.length > 0 && (
        <div
          className="rounded-xl overflow-hidden"
          style={{ background: 'rgba(162,155,254,0.05)', border: '1px solid rgba(162,155,254,0.15)' }}
        >
          <button
            onClick={() => setShowWhatIf(!showWhatIf)}
            className="w-full flex items-center justify-between p-3 cursor-pointer border-none"
            style={{ background: 'transparent' }}
          >
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-sm" style={{ color: '#a29bfe', fontVariationSettings: "'FILL' 0" }}>psychiatry_alt</span>
              <span className="text-xs font-bold" style={{ color: '#a29bfe' }}>А что если?</span>
            </div>
            <span className="text-[10px]" style={{ color: '#9b98a8' }}>
              {showWhatIf ? '▾ Скрыть' : '▸ Показать сценарии'}
            </span>
          </button>
          {showWhatIf && (
            <div className="px-3 pb-3 space-y-3">
              {presentation.what_if.map((scenario, i) => (
                <div key={i} className="rounded-lg p-3" style={{ background: '#0f0e17', border: '1px solid rgba(162,155,254,0.1)' }}>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded" style={{ background: 'rgba(162,155,254,0.15)', color: '#a29bfe' }}>
                      {scenario.description}
                    </span>
                  </div>
                  <CodePanel code={scenario.code} filename="task.py" />
                  <div className="mt-1 px-3 py-1.5 rounded-lg font-mono text-xs" style={{
                    background: scenario.output.includes('Error') ? 'rgba(255,107,107,0.1)' : 'rgba(0,212,170,0.08)',
                    border: `1px solid ${scenario.output.includes('Error') ? 'rgba(255,107,107,0.2)' : 'rgba(0,212,170,0.2)'}`,
                    color: scenario.output.includes('Error') ? '#ff6b6b' : '#00d4aa',
                  }}>
                    <span className="text-[10px] font-bold block mb-0.5" style={{ color: '#9b98a8' }}>Вывод:</span>
                    {scenario.output}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Solutions */}
      {presentation.solutions && presentation.solutions.length > 0 && (
        <div className="rounded-xl overflow-hidden" style={{ background: 'rgba(0,212,170,0.05)', border: '1px solid rgba(0,212,170,0.15)' }}>
          <button
            onClick={() => setShowSolutions(!showSolutions)}
            className="w-full flex items-center justify-between p-3 cursor-pointer border-none"
            style={{ background: 'transparent' }}
          >
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-sm" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>lightbulb</span>
              <span className="text-xs font-bold" style={{ color: '#00d4aa' }}>Варианты решений</span>
            </div>
            <span className="text-[10px]" style={{ color: '#9b98a8' }}>
              {showSolutions ? '▾ Скрыть' : '▸ Показать решения'}
            </span>
          </button>
          {showSolutions && (
            <div className="px-3 pb-3 space-y-3">
              {presentation.solutions.map((solution, i) => (
                <div key={i} className="rounded-lg p-3" style={{ background: '#0f0e17', border: '1px solid rgba(0,212,170,0.1)' }}>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="material-symbols-outlined text-[14px]" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>check_circle</span>
                    <span className="text-xs font-bold" style={{ color: '#00d4aa' }}>{solution.title}</span>
                  </div>
                  <p className="text-[11px] mb-2" style={{ color: '#9b98a8' }}>{solution.description}</p>
                  <CodePanel code={solution.code} filename="solution.py" />
                  {solution.output && (
                    <div className="mt-1 px-3 py-1.5 rounded-lg font-mono text-xs" style={{ background: 'rgba(0,212,170,0.08)', border: '1px solid rgba(0,212,170,0.2)', color: '#00d4aa' }}>
                      <span className="text-[10px] font-bold block mb-0.5" style={{ color: '#9b98a8' }}>Вывод:</span>
                      {solution.output}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
