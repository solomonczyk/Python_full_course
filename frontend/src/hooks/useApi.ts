import { useState, useEffect } from 'react'
import type { Lesson, LessonSummary, Progress, ReviewBlock, ReviewSummary } from '../types'

const BASE = '/api'

export function useLessons() {
  const [lessons, setLessons] = useState<LessonSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch(`${BASE}/lessons`)
      .then((r) => {
        if (!r.ok) throw new Error('Failed to load lessons')
        return r.json()
      })
      .then((data) => {
        if (!Array.isArray(data)) {
          console.warn('Lessons data is not an array:', data)
          setLessons([])
          return
        }
        setLessons(data)
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  return { lessons, loading, error }
}

export function useLesson(id: string) {
  const [lesson, setLesson] = useState<Lesson | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetch(`${BASE}/lessons/${id}`)
      .then((r) => {
        if (!r.ok) throw new Error(`Lesson ${id} not found`)
        return r.json()
      })
      .then(setLesson)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  return { lesson, loading, error }
}

const STORAGE_KEY = 'python-quest-progress'

export function useProgress() {
  const [progress, setProgress] = useState<Record<string, Progress>>({})

  useEffect(() => {
    fetch(`${BASE}/progress`)
      .then((r) => {
        if (!r.ok) throw new Error('Failed to load progress')
        return r.json()
      })
      .then((data: Progress[] | null) => {
        const map: Record<string, Progress> = {}
        if (Array.isArray(data)) {
          data.forEach((p) => {
            if (p && p.lesson_id) map[p.lesson_id] = p
          })
        }
        // Merge with localStorage so offline/Vercel ephemeral state survives
        const saved = localStorage.getItem(STORAGE_KEY)
        if (saved) {
          try {
            const local: Record<string, Progress> = JSON.parse(saved)
            Object.assign(map, local)
          } catch { /* ignore corrupt localStorage */ }
        }
        setProgress(map)
      })
      .catch((err) => {
        console.error('Error loading progress:', err)
        // Fallback to localStorage when API fails
        const saved = localStorage.getItem(STORAGE_KEY)
        if (saved) {
          try {
            setProgress(JSON.parse(saved))
          } catch {
            setProgress({})
          }
        } else {
          setProgress({})
        }
      })
  }, [])

  const persist = (map: Record<string, Progress>) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(map))
  }

  const markComplete = async (lesson_id: string, score?: number) => {
    try {
      const res = await fetch(`${BASE}/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lesson_id, completed: true, score }),
      })
      const updated: Progress = await res.json()
      setProgress((prev) => {
        const next = { ...prev, [lesson_id]: updated }
        persist(next)
        return next
      })
    } catch (e) {
      // If API fails (Vercel ephemeral), save to localStorage only
      const updated: Progress = { lesson_id, completed: true, score: score ?? null, updated_at: new Date().toISOString() }
      setProgress((prev) => {
        const next = { ...prev, [lesson_id]: updated }
        persist(next)
        return next
      })
    }
  }

  return { progress, markComplete }
}

export async function checkQuizAnswer(lesson_id: string, answer_id: string) {
  const res = await fetch(`${BASE}/quiz/check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lesson_id, answer_id }),
  })
  if (!res.ok) throw new Error('Failed to check quiz answer')
  return res.json()
}

export async function checkWhatOutputs(lesson_id: string, answer_id: string) {
  const res = await fetch(`${BASE}/quiz/what-outputs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lesson_id, answer_id }),
  })
  if (!res.ok) throw new Error('Failed to check what-outputs')
  return res.json()
}

// ── Review hooks ──────────────────────────────────────────────────────────

export function useReviews() {
  const [reviews, setReviews] = useState<ReviewSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${BASE}/reviews`)
      .then((r) => {
        if (!r.ok) throw new Error('Failed to load reviews')
        return r.json()
      })
      .then((data) => {
        if (!Array.isArray(data)) {
          console.warn('Reviews data is not an array:', data)
          setReviews([])
          return
        }
        setReviews(data)
      })
      .catch((e) => console.error('Error loading reviews:', e))
      .finally(() => setLoading(false))
  }, [])

  return { reviews, loading }
}

export function useReview(id: string) {
  const [review, setReview] = useState<ReviewBlock | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetch(`${BASE}/reviews/${id}`)
      .then((r) => {
        if (!r.ok) throw new Error(`Review ${id} not found`)
        return r.json()
      })
      .then(setReview)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  return { review, loading, error }
}
