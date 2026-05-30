import { useState } from 'react'
import type { PracticeSubtask as PracticeSubtaskType } from '../types'

interface Props {
  subtasks: PracticeSubtaskType[]
}

export default function PracticeSubtasks({ subtasks }: Props) {
  const [openIndex, setOpenIndex] = useState<number | null>(null)
  const [completed, setCompleted] = useState<Set<number>>(new Set())

  if (!subtasks || subtasks.length === 0) return null

  const toggleOpen = (i: number) => {
    setOpenIndex(openIndex === i ? null : i)
  }

  return (
    <div
      className="rounded-xl p-4"
      style={{
        background: 'rgba(0,212,170,0.05)',
        border: '1px solid rgba(0,212,170,0.15)',
      }}
    >
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-sm" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>exercise</span>
        <h3 className="text-xs font-bold" style={{ color: '#00d4aa' }}>Дополнительные задания</h3>
        <span className="text-[10px] px-1.5 py-0.5 rounded-full" style={{ background: 'rgba(0,212,170,0.15)', color: '#00d4aa' }}>
          {completed.size}/{subtasks.length}
        </span>
      </div>

      <div className="space-y-2">
        {subtasks.map((task, i) => (
          <div
            key={i}
            className="rounded-lg overflow-hidden"
            style={{
              background: completed.has(i) ? 'rgba(0,212,170,0.08)' : '#0f0e17',
              border: `1px solid ${
                completed.has(i) ? 'rgba(0,212,170,0.3)' : 'rgba(201,162,39,0.15)'
              }`,
            }}
          >
            {/* Header */}
            <button
              onClick={() => toggleOpen(i)}
              className="w-full flex items-center justify-between p-3 text-left cursor-pointer border-none"
              style={{ background: 'transparent' }}
            >
              <div className="flex items-center gap-2">
                <span
                  className="material-symbols-outlined text-sm"
                  style={{
                    color: completed.has(i) ? '#00d4aa' : '#9b98a8',
                    fontVariationSettings: `'FILL' ${completed.has(i) ? '1' : '0'}`,
                  }}
                >
                  {completed.has(i) ? 'check_circle' : 'radio_button_unchecked'}
                </span>
                <span className="text-xs font-medium" style={{ color: completed.has(i) ? '#00d4aa' : '#e8e6f0' }}>
                  {task.title}
                </span>
              </div>
              <span className="text-[10px]" style={{ color: '#9b98a8' }}>
                {openIndex === i ? '▾' : '▸'}
              </span>
            </button>

            {/* Expanded content */}
            {openIndex === i && (
              <div className="px-3 pb-3 space-y-2">
                <p className="text-[11px] leading-relaxed" style={{ color: '#9b98a8' }}>
                  {task.task}
                </p>
                {task.hint && (
                  <div
                    className="p-2 rounded text-[10px]"
                    style={{
                      background: 'rgba(201,162,39,0.1)',
                      border: '1px solid rgba(201,162,39,0.2)',
                      color: '#c9a227',
                    }}
                  >
                    💡 {task.hint}
                  </div>
                )}
                <div
                  className="p-2 rounded font-mono text-[11px]"
                  style={{
                    background: '#0d0c14',
                    border: '1px solid rgba(0,212,170,0.2)',
                    color: '#00d4aa',
                  }}
                >
                  Ожидаемый вывод: {task.expected_output}
                </div>
                <button
                  onClick={() => {
                    setCompleted((prev) => new Set(prev).add(i))
                  }}
                  className="text-[10px] font-semibold cursor-pointer px-3 py-1.5 rounded-lg transition-all hover:scale-105 border-none"
                  style={{
                    background: completed.has(i) ? '#00d4aa' : 'rgba(0,212,170,0.15)',
                    color: completed.has(i) ? '#0f0e17' : '#00d4aa',
                  }}
                >
                  {completed.has(i) ? '✅ Готово' : '✓ Отметить выполненным'}
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
