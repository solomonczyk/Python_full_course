import { createContext, useContext, type ReactNode } from 'react'
import { useProgress } from './useApi'
import type { LessonSummary, Progress } from '../types'

interface ProgressContextValue {
  progress: Record<string, Progress>
  markComplete: (lesson_id: string, score?: number) => Promise<void>
  isLessonUnlocked: (lessonId: string, lessons: LessonSummary[]) => boolean
}

const ProgressContext = createContext<ProgressContextValue | null>(null)

export function isLessonUnlocked(
  lessonId: string,
  lessons: LessonSummary[],
  progress: Record<string, Progress>
): boolean {
  const idx = lessons.findIndex(l => l.id === lessonId)
  if (idx <= 0) return true  // first lesson always open

  const lesson = lessons[idx]
  if (!lesson.locked) return true  // explicitly unlocked in data

  // Unlock if previous lesson is completed
  const prev = lessons[idx - 1]
  return Boolean(progress[prev.id]?.completed)
}

export function ProgressProvider({ children }: { children: ReactNode }) {
  const { progress, markComplete } = useProgress()

  const value: ProgressContextValue = {
    progress,
    markComplete,
    isLessonUnlocked: (lessonId, lessons) =>
      isLessonUnlocked(lessonId, lessons, progress),
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
