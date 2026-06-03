/**
 * Python Quest — Backend Beta Progress Store
 *
 * API client for server-side beta progress persistence.
 * Communicates with the backend /api/beta/progress/* endpoints.
 *
 * - Never throws — all methods return clean results
 * - Never collects personal data
 * - Falls back gracefully on network error
 */

import type { BetaProgressData, BetaMissionStats } from '../types'

// ── Types ───────────────────────────────────────────────────────────────────

export interface BackendBetaProgress {
  ok: boolean
  found?: boolean
  participant_code?: string
  participant_id?: string
  current_lesson_id?: string
  completed_lessons?: string[]
  lesson_status?: Record<string, string>
  mission_stats?: Record<string, {
    attempts: number
    failed: number
    passed: boolean
    hints_used: number
  }>
  created_at?: string
  updated_at?: string
  last_active_at?: string
  message?: string
}

export interface BackendResult {
  ok: boolean
  /** Whether the backend was reachable at all */
  reachable: boolean
  data: BackendBetaProgress | null
  error?: string
}

// ── Constants ───────────────────────────────────────────────────────────────

const BASE = '/api/beta/progress'

// ── Helpers ─────────────────────────────────────────────────────────────────

function convertBackendToBetaProgress(backend: BackendBetaProgress): BetaProgressData | null {
  if (!backend.participant_code) return null

  // Convert snake_case mission_stats to camelCase for BetaProgressData
  const missionStats: Record<string, BetaMissionStats> = {}
  if (backend.mission_stats) {
    for (const [lessonId, stats] of Object.entries(backend.mission_stats)) {
      missionStats[lessonId] = {
        attempts: stats.attempts ?? 0,
        failed: stats.failed ?? 0,
        passed: stats.passed ?? false,
        hintsUsed: stats.hints_used ?? 0,
      }
    }
  }

  // Convert lesson_status to BetaLessonStatus format
  const lessonStatus: Record<string, 'completed' | 'started'> = {}
  if (backend.lesson_status) {
    for (const [lessonId, status] of Object.entries(backend.lesson_status)) {
      if (status === 'completed' || status === 'started') {
        lessonStatus[lessonId] = status
      }
    }
  }

  return {
    participantCode: backend.participant_code,
    currentLessonId: backend.current_lesson_id ?? '1-1',
    completedLessons: backend.completed_lessons ?? [],
    lessonStatus,
    missionStats,
    lastActiveAt: backend.last_active_at ?? new Date().toISOString(),
    createdAt: backend.created_at ?? new Date().toISOString(),
  }
}

async function apiCall<T>(
  url: string,
  options: RequestInit = {},
): Promise<{ ok: boolean; data: T | null; error?: string }> {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers as Record<string, string> ?? {}),
      },
      ...options,
    })
    if (!response.ok) {
      const text = await response.text()
      return { ok: false, data: null, error: `HTTP ${response.status}: ${text.slice(0, 200)}` }
    }
    const data = await response.json()
    return { ok: true, data }
  } catch (err) {
    return {
      ok: false,
      data: null,
      error: err instanceof Error ? err.message : 'Network error',
    }
  }
}

// ── Public API ──────────────────────────────────────────────────────────────

/**
 * Create beta progress for a participant code.
 * Idempotent — safe to call if already exists.
 */
export async function createBackendProgress(participantCode: string): Promise<BackendResult> {
  const result = await apiCall<BackendBetaProgress>(`${BASE}/create`, {
    method: 'POST',
    body: JSON.stringify({ participant_code: participantCode }),
  })

  return {
    ok: result.ok,
    reachable: result.ok || (result.error?.includes('Network error') === false),
    data: result.data ?? null,
    error: result.error,
  }
}

/**
 * Get beta progress from backend by participant code.
 */
export async function getBackendProgress(participantCode: string): Promise<BackendResult> {
  const result = await apiCall<BackendBetaProgress>(`${BASE}/${encodeURIComponent(participantCode)}`)

  if (!result.ok) {
    return {
      ok: false,
      reachable: false,
      data: null,
      error: result.error,
    }
  }

  // Backend returns found=false for missing codes — still a valid response
  const data = result.data
  if (data && !data.found) {
    return {
      ok: true,
      reachable: true,
      data: data,
    }
  }

  return {
    ok: true,
    reachable: true,
    data: result.data,
  }
}

/**
 * Update current lesson on the backend.
 */
export async function updateBackendCurrentLesson(
  participantCode: string,
  lessonId: string,
): Promise<BackendResult> {
  const result = await apiCall<BackendBetaProgress>(`${BASE}/${encodeURIComponent(participantCode)}`, {
    method: 'PUT',
    body: JSON.stringify({ current_lesson_id: lessonId }),
  })

  return {
    ok: result.ok,
    reachable: result.ok || (result.error?.includes('Network error') === false),
    data: result.data ?? null,
    error: result.error,
  }
}

/**
 * Mark a lesson as started on the backend.
 */
export async function markLessonStartedBackend(
  participantCode: string,
  lessonId: string,
): Promise<BackendResult> {
  const result = await apiCall<BackendBetaProgress>(
    `${BASE}/${encodeURIComponent(participantCode)}/lesson-started`,
    {
      method: 'POST',
      body: JSON.stringify({ lesson_id: lessonId }),
    },
  )

  return {
    ok: result.ok,
    reachable: result.ok || (result.error?.includes('Network error') === false),
    data: result.data ?? null,
    error: result.error,
  }
}

/**
 * Record a mission result (pass/fail) on the backend.
 */
export async function saveMissionResultBackend(
  participantCode: string,
  lessonId: string,
  passed: boolean,
  attempts: number,
  hintsUsed: number,
): Promise<BackendResult> {
  const result = await apiCall<BackendBetaProgress>(
    `${BASE}/${encodeURIComponent(participantCode)}/mission-result`,
    {
      method: 'POST',
      body: JSON.stringify({
        lesson_id: lessonId,
        passed,
        attempts,
        hints_used: hintsUsed,
      }),
    },
  )

  return {
    ok: result.ok,
    reachable: result.ok || (result.error?.includes('Network error') === false),
    data: result.data ?? null,
    error: result.error,
  }
}

/**
 * Record a hint used on the backend.
 */
export async function saveHintUsedBackend(
  participantCode: string,
  lessonId: string,
): Promise<BackendResult> {
  const result = await apiCall<BackendBetaProgress>(
    `${BASE}/${encodeURIComponent(participantCode)}/hint-used`,
    {
      method: 'POST',
      body: JSON.stringify({ lesson_id: lessonId }),
    },
  )

  return {
    ok: result.ok,
    reachable: result.ok || (result.error?.includes('Network error') === false),
    data: result.data ?? null,
    error: result.error,
  }
}

/**
 * Mark a lesson as completed on the backend.
 */
export async function markLessonCompletedBackend(
  participantCode: string,
  lessonId: string,
): Promise<BackendResult> {
  const result = await apiCall<BackendBetaProgress>(
    `${BASE}/${encodeURIComponent(participantCode)}/lesson-completed`,
    {
      method: 'POST',
      body: JSON.stringify({ lesson_id: lessonId }),
    },
  )

  return {
    ok: result.ok,
    reachable: result.ok || (result.error?.includes('Network error') === false),
    data: result.data ?? null,
    error: result.error,
  }
}

/**
 * Restore beta progress from backend, falling back to localStorage.
 *
 * Restore order:
 *   1. Backend by participant_code
 *   2. localStorage by participant_code
 *   3. Empty new progress
 *
 * Returns { source, progress } indicating where progress came from.
 */
export async function restoreFromBackend(
  participantCode: string,
  localStorageProgress: BetaProgressData | null,
): Promise<{
  source: 'backend' | 'localStorage' | 'empty'
  progress: BetaProgressData | null
}> {
  // Try backend first
  const backendResult = await getBackendProgress(participantCode)
  if (backendResult.ok && backendResult.data?.found) {
    const converted = convertBackendToBetaProgress(backendResult.data)
    if (converted) {
      return { source: 'backend', progress: converted }
    }
  }

  // Fall back to localStorage
  if (localStorageProgress) {
    return { source: 'localStorage', progress: localStorageProgress }
  }

  // Empty
  return { source: 'empty', progress: null }
}

/**
 * Check if the backend is reachable.
 */
export async function checkBackendReachable(): Promise<boolean> {
  try {
    const response = await fetch('/api/health', { method: 'GET', signal: AbortSignal.timeout(5000) })
    return response.ok
  } catch {
    return false
  }
}
