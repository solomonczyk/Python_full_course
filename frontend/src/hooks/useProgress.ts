import { useState, useEffect, useCallback } from 'react'
import { getUserId } from '../utils/userId'

const BASE = '/api'
const STORAGE_KEY = 'python-quest-progress'

export interface ProgressRecord {
  lesson_id: string
  completed: boolean
  quiz_passed: boolean
  mission_done: boolean
  updated_at: string
}

function loadLocal(): Record<string, ProgressRecord> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

function saveLocal(map: Record<string, ProgressRecord>) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(map))
}

export function useProgress() {
  const [progress, setProgress] = useState<Record<string, ProgressRecord>>(loadLocal)
  const [loading, setLoading] = useState(true)

  // Load from server on mount
  useEffect(() => {
    const headers = {
      'Content-Type': 'application/json',
      'X-User-Id': getUserId(),
    }
    fetch(`${BASE}/progress`, { headers })
      .then((r) => {
        if (!r.ok) throw new Error('Failed to load progress from server')
        return r.json()
      })
      .then((data: ProgressRecord[]) => {
        if (Array.isArray(data)) {
          const map: Record<string, ProgressRecord> = {}
          data.forEach((p) => {
            if (p?.lesson_id) map[p.lesson_id] = p
          })
          // Merge: server wins, local fills gaps
          const local = loadLocal()
          const merged = { ...local, ...map }
          setProgress(merged)
          saveLocal(merged)
        }
      })
      .catch((err) => {
        console.warn('Progress API unavailable, using localStorage:', err.message)
        setProgress(loadLocal())
      })
      .finally(() => setLoading(false))
  }, [])

  const updateProgress = useCallback(
    async (lesson_id: string, update: Partial<ProgressRecord>) => {
      const headers = {
        'Content-Type': 'application/json',
        'X-User-Id': getUserId(),
      }
      const payload = {
        lesson_id,
        completed: update.completed ?? false,
        quiz_passed: update.quiz_passed ?? false,
        mission_done: update.mission_done ?? false,
      }

      // Optimistic update
      setProgress((prev) => {
        const existing = prev[lesson_id]
        const next: ProgressRecord = {
          lesson_id,
          completed: update.completed ?? existing?.completed ?? false,
          quiz_passed: update.quiz_passed ?? existing?.quiz_passed ?? false,
          mission_done: update.mission_done ?? existing?.mission_done ?? false,
          updated_at: new Date().toISOString(),
        }
        const merged = { ...prev, [lesson_id]: next }
        saveLocal(merged)
        return merged
      })

      // Sync to server
      try {
        await fetch(`${BASE}/progress`, {
          method: 'POST',
          headers,
          body: JSON.stringify(payload),
        })
      } catch (err) {
        console.warn('Failed to sync progress to server:', err)
      }
    },
    [],
  )

  const completedCount = Object.values(progress).filter((p) => p.completed).length
  const totalLessons = 87

  return { progress, updateProgress, completedCount, totalLessons, loading }
}
