import { createContext, useContext, type ReactNode } from 'react'
import { useProgress } from './useApi'
import type { Progress } from '../types'

interface ProgressContextValue {
  progress: Record<string, Progress>
  markComplete: (lesson_id: string, score?: number) => Promise<void>
}

const ProgressContext = createContext<ProgressContextValue | null>(null)

export function ProgressProvider({ children }: { children: ReactNode }) {
  const { progress, markComplete } = useProgress()
  return (
    <ProgressContext.Provider value={{ progress, markComplete }}>
      {children}
    </ProgressContext.Provider>
  )
}

export function useProgressContext(): ProgressContextValue {
  const ctx = useContext(ProgressContext)
  if (!ctx) throw new Error('useProgressContext must be used within ProgressProvider')
  return ctx
}
