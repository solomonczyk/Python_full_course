import { useState, useEffect } from 'react'
import type { Lesson, LessonSummary, Progress } from '../types'

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

export function useProgress() {
  const [progress, setProgress] = useState<Record<string, Progress>>({})

  useEffect(() => {
    fetch(`${BASE}/progress`)
      .then((r) => {
        if (!r.ok) throw new Error('Failed to load progress')
        return r.json()
      })
      .then((data: Progress[] | null) => {
        if (!Array.isArray(data)) {
          console.warn('Progress data is not an array:', data)
          return
        }
        const map: Record<string, Progress> = {}
        data.forEach((p) => {
          if (p && p.lesson_id) {
            map[p.lesson_id] = p
          }
        })
        setProgress(map)
      })
      .catch((err) => {
        console.error('Error loading progress:', err)
        setProgress({})
      })
  }, [])

  const markComplete = async (lesson_id: string, score?: number) => {
    const res = await fetch(`${BASE}/progress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lesson_id, completed: true, score }),
    })
    const updated: Progress = await res.json()
    setProgress((prev) => ({ ...prev, [lesson_id]: updated }))
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
