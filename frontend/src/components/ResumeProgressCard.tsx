/**
 * ResumeProgressCard — Shows restored progress for returning participant
 *
 * Displays the participant's progress summary after entering a valid beta code.
 * Shows current lesson and provides a button to continue.
 */

import type { BetaProgressData } from '../types'

interface Props {
  progress: BetaProgressData
  onContinue: (lessonId: string) => void
  onStartFresh: () => void
}

export default function ResumeProgressCard({ progress, onContinue, onStartFresh }: Props) {
  const completedCount = progress.completedLessons.length

  return (
    <div
      className="rounded-xl p-6 sm:p-8 space-y-5"
      style={{
        background: '#1a1924',
        border: '2px solid rgba(0,212,170,0.3)',
        boxShadow: '0 0 30px rgba(0,212,170,0.08)',
      }}
    >
      {/* Icon */}
      <div className="flex items-center gap-3">
        <div
          className="w-12 h-12 rounded-full flex items-center justify-center shrink-0"
          style={{ background: 'rgba(0,212,170,0.15)' }}
        >
          <span className="text-xl">📚</span>
        </div>
        <div>
          <h3 className="text-base font-bold" style={{ color: '#e8e6f0' }}>
            Ваш прогресс найден
          </h3>
          <p className="text-xs" style={{ color: '#00d4aa' }}>
            Код подтверждён · {completedCount} уроков пройдено
          </p>
        </div>
      </div>

      {/* Progress bar */}
      <div>
        <div className="flex justify-between text-[10px] mb-1.5">
          <span style={{ color: '#9b98a8' }}>Прогресс по курсу</span>
          <span style={{ color: '#00d4aa' }}>{completedCount} / 87 уроков</span>
        </div>
        <div
          className="h-2 rounded-full overflow-hidden"
          style={{ background: 'rgba(0,212,170,0.1)' }}
        >
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{
              width: `${Math.min((completedCount / 87) * 100, 100)}%`,
              background: 'linear-gradient(90deg, #00d4aa, #c9a227)',
            }}
          />
        </div>
      </div>

      {/* Current lesson info */}
      <div>
        <p className="text-xs mb-2" style={{ color: '#9b98a8' }}>
          Продолжить с урока:
        </p>
        <div
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg"
          style={{
            background: 'rgba(201,162,39,0.1)',
            border: '1px solid rgba(201,162,39,0.2)',
          }}
        >
          <span className="material-symbols-outlined text-sm" style={{ color: '#c9a227', fontVariationSettings: "'FILL' 0" }}>
            play_circle
          </span>
          <span className="text-sm font-bold" style={{ color: '#e8e6f0' }}>
            Урок {progress.currentLessonId}
          </span>
        </div>
      </div>

      {/* Mission stats summary */}
      {Object.keys(progress.missionStats).length > 0 && (
        <div className="flex gap-4 text-center">
          <div className="flex-1 rounded-lg p-2.5" style={{ background: 'rgba(15,14,23,0.6)' }}>
            <div className="text-lg font-bold" style={{ color: '#c9a227' }}>
              {Object.values(progress.missionStats).reduce((sum, s) => sum + s.attempts, 0)}
            </div>
            <div className="text-[10px]" style={{ color: '#9b98a8' }}>Всего попыток</div>
          </div>
          <div className="flex-1 rounded-lg p-2.5" style={{ background: 'rgba(15,14,23,0.6)' }}>
            <div className="text-lg font-bold" style={{ color: '#00d4aa' }}>
              {Object.values(progress.missionStats).filter(s => s.passed).length}
            </div>
            <div className="text-[10px]" style={{ color: '#9b98a8' }}>Миссий пройдено</div>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-1">
        <button
          onClick={onStartFresh}
          className="px-5 py-2.5 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:opacity-80"
          style={{
            background: 'transparent',
            border: '1px solid rgba(201,162,39,0.3)',
            color: '#9b98a8',
          }}
        >
          Начать заново
        </button>

        <button
          onClick={() => onContinue(progress.currentLessonId)}
          className="px-6 py-2.5 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:opacity-90 active:scale-[0.97]"
          style={{
            background: 'linear-gradient(135deg, #00d4aa, #00b894)',
            color: '#0f0e17',
          }}
        >
          Продолжить урок {progress.currentLessonId} →
        </button>
      </div>
    </div>
  )
}
