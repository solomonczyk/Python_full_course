import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { useProgress, type ProgressRecord } from './useApi'
import type { LessonSummary } from '../types'
import { getStoredParticipantCode } from '../lib/participantIdentity'

interface ProgressContextValue {
  progress: Record<string, ProgressRecord>
  markComplete: (lesson_id: string, score?: number) => Promise<void>
  isLessonUnlocked: (lessonId: string, lessons: LessonSummary[]) => boolean
  betaStage: number | undefined
}

const ProgressContext = createContext<ProgressContextValue | null>(null)

export function isLessonUnlocked(
  lessonId: string,
  lessons: LessonSummary[],
  progress: Record<string, ProgressRecord>,
  betaStage?: number,
): boolean {
  const idx = lessons.findIndex(l => l.id === lessonId)
  if (idx <= 0) return true  // first lesson always open

  const lesson = lessons[idx]

  // Beta stage check: block parts beyond current stage
  if (betaStage !== undefined && lesson.part > betaStage) return false

  // Beta stage: if participant's stage covers this part, bypass sequential unlock
  if (betaStage !== undefined && lesson.part <= betaStage) return true

  if (!lesson.locked) return true  // explicitly unlocked in data

  // Unlock if previous lesson is completed
  const prev = lessons[idx - 1]
  return Boolean(progress[prev.id]?.completed)
}

export function ProgressProvider({ children }: { children: ReactNode }) {
  const { progress, markComplete } = useProgress()
  const [betaStage, setBetaStage] = useState<number | undefined>(undefined)

  // Fetch beta stage on mount if participant code exists
  useEffect(() => {
    const code = getStoredParticipantCode()
    if (code) {
      fetch(`/api/beta/access/${encodeURIComponent(code)}`)
        .then(r => r.json())
        .then(data => {
          if (data.ok) setBetaStage(data.current_stage)
        })
        .catch(() => {
          // No beta access available — behavior unchanged
          setBetaStage(undefined)
        })
    }
  }, [])

  const value: ProgressContextValue = {
    progress,
    markComplete,
    betaStage,
    isLessonUnlocked: (lessonId, lessons) =>
      isLessonUnlocked(lessonId, lessons, progress, betaStage),
  }

  return (
    <ProgressContext.Provider value={value}>
      {children}
    </ProgressContext.Provider>
  )
}

export function useProgressContext(): ProgressContextValue {
  const ctx = useContext(ProgressContext)
  if (!ctx) throw new Error('useProgressContext must be used within ProgressProvider')
  return ctx
}
