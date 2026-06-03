import { useState, useEffect } from 'react'
import type { Lesson, LessonSummary, ReviewBlock, ReviewSummary, QuestSummary, Quest, RecapSummary, Recap, QuestCheckResult, StagedAccessError } from '../types'
import { getUserId } from '../utils/userId'
import { getStoredParticipantCode } from '../lib/participantIdentity'

const BASE = '/api'

function authHeaders(): Record<string, string> {
  return {
    'Content-Type': 'application/json',
    'X-User-Id': getUserId(),
  }
}

function betaHeaders(): Record<string, string> {
  const code = getStoredParticipantCode()
  if (code) {
    return { 'X-Participant-Code': code }
  }
  return {}
}

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
  const [stagedAccess, setStagedAccess] = useState<StagedAccessError | null>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    setError(null)
    setStagedAccess(null)

    const headers = { ...betaHeaders() }

    fetch(`${BASE}/lessons/${id}`, { headers })
      .then(async (r) => {
        if (r.status === 403) {
          const data = await r.json()
          const detail = data?.detail
          if (detail?.reason === 'staged_access') {
            setStagedAccess({
              reason: 'staged_access',
              currentStage: detail.current_stage,
              maxStage: detail.max_stage,
              lessonPart: detail.lesson_part,
              message: detail.message,
            })
            return null
          }
          throw new Error(data?.detail ?? `Lesson ${id} not found`)
        }
        if (!r.ok) throw new Error(`Lesson ${id} not found`)
        return r.json()
      })
      .then((data) => {
        if (data) setLesson(data)
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  return { lesson, loading, error, stagedAccess }
}

const STORAGE_KEY = 'python-quest-progress'

export interface ProgressRecord {
  lesson_id: string
  completed: boolean
  quiz_passed: boolean
  mission_done: boolean
  score: number | null
  updated_at: string
}

export function useProgress() {
  const [progress, setProgress] = useState<Record<string, ProgressRecord>>({})

  useEffect(() => {
    fetch(`${BASE}/progress`, { headers: authHeaders() })
      .then((r) => {
        if (!r.ok) throw new Error('Failed to load progress')
        return r.json()
      })
      .then((data: ProgressRecord[] | null) => {
        const map: Record<string, ProgressRecord> = {}
        if (Array.isArray(data)) {
          data.forEach((p) => {
            if (p && p.lesson_id) map[p.lesson_id] = p
          })
        }
        // Merge with localStorage so offline/Vercel ephemeral state survives
        const saved = localStorage.getItem(STORAGE_KEY)
        if (saved) {
          try {
            const local: Record<string, ProgressRecord> = JSON.parse(saved)
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

  const persist = (map: Record<string, ProgressRecord>) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(map))
  }

  const markComplete = async (lesson_id: string, score?: number) => {
    try {
      const res = await fetch(`${BASE}/progress`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ lesson_id, completed: true, score }),
      })
      const updated: ProgressRecord = await res.json()
      setProgress((prev) => {
        const next = { ...prev, [lesson_id]: updated }
        persist(next)
        return next
      })
    } catch (e) {
      // If API fails (Vercel ephemeral), save to localStorage only
      const updated: ProgressRecord = {
        lesson_id,
        completed: true,
        quiz_passed: false,
        mission_done: false,
        score: score ?? null,
        updated_at: new Date().toISOString(),
      }
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
    headers: authHeaders(),
    body: JSON.stringify({ lesson_id, answer_id }),
  })
  if (!res.ok) throw new Error('Failed to check quiz answer')
  return res.json()
}

export async function checkWhatOutputs(lesson_id: string, answer_id: string) {
  const res = await fetch(`${BASE}/quiz/what-outputs`, {
    method: 'POST',
    headers: authHeaders(),
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

// ── Quest hooks ────────────────────────────────────────────────────────────

export function useQuests() {
  const [quests, setQuests] = useState<QuestSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${BASE}/quests`)
      .then((r) => {
        if (!r.ok) throw new Error('Failed to load quests')
        return r.json()
      })
      .then((data) => {
        if (!Array.isArray(data)) {
          console.warn('Quests data is not an array:', data)
          setQuests([])
          return
        }
        setQuests(data)
      })
      .catch((e) => console.error('Error loading quests:', e))
      .finally(() => setLoading(false))
  }, [])

  return { quests, loading }
}

export function useQuest(id: string) {
  const [quest, setQuest] = useState<Quest | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetch(`${BASE}/quests/${id}`)
      .then((r) => {
        if (!r.ok) throw new Error(`Quest ${id} not found`)
        return r.json()
      })
      .then(setQuest)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  return { quest, loading, error }
}

export async function checkQuest(quest_id: string, code: string): Promise<QuestCheckResult> {
  const res = await fetch(`${BASE}/quests/${quest_id}/check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code }),
  })
  if (!res.ok) throw new Error('Failed to check quest')
  return res.json()
}

// ── Recap hooks ────────────────────────────────────────────────────────────

export function useRecaps() {
  const [recaps, setRecaps] = useState<RecapSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${BASE}/recaps`)
      .then((r) => {
        if (!r.ok) throw new Error('Failed to load recaps')
        return r.json()
      })
      .then((data) => {
        if (!Array.isArray(data)) {
          console.warn('Recaps data is not an array:', data)
          setRecaps([])
          return
        }
        setRecaps(data)
      })
      .catch((e) => console.error('Error loading recaps:', e))
      .finally(() => setLoading(false))
  }, [])

  return { recaps, loading }
}

export function useRecap(id: string) {
  const [recap, setRecap] = useState<Recap | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetch(`${BASE}/recaps/${id}`)
      .then((r) => {
        if (!r.ok) throw new Error(`Recap ${id} not found`)
        return r.json()
      })
      .then(setRecap)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  return { recap, loading, error }
}
