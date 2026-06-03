/**
 * Python Quest — Beta Progress Sync
 *
 * Syncs beta progress between backend and localStorage.
 *
 * Order of operations:
 *   1. Primary: Save to backend
 *   2. Fallback: Save to localStorage (always, for offline resilience)
 *   3. Restore: backend → localStorage → empty
 *
 * Never throws. Never blocks UI. Never collects personal data.
 */

import type { BetaProgressData } from '../types'
import {
  loadBetaProgress,
  saveBetaProgress,
  getCurrentBetaProgress,
} from './progressStore'
import {
  createBackendProgress,
  markLessonStartedBackend,
  saveMissionResultBackend,
  saveHintUsedBackend,
  markLessonCompletedBackend,
  restoreFromBackend,
  checkBackendReachable,
} from './backendProgressStore'
import { getStoredParticipantCode } from './participantIdentity'

// ── Types ───────────────────────────────────────────────────────────────────

export interface SyncState {
  /** Whether backend is currently reachable */
  backendReachable: boolean
  /** Last time backend was checked */
  lastCheckAt: number | null
  /** Pending changes that need to be synced */
  hasPendingSync: boolean
}

let syncState: SyncState = {
  backendReachable: false,
  lastCheckAt: null,
  hasPendingSync: false,
}

// ── Backend reachability check (cached) ─────────────────────────────────────

const CHECK_INTERVAL_MS = 60_000 // Recheck every 60s

/**
 * Check if backend is reachable, with caching.
 */
export async function isBackendReachable(): Promise<boolean> {
  const now = Date.now()
  if (syncState.lastCheckAt && now - syncState.lastCheckAt < CHECK_INTERVAL_MS) {
    return syncState.backendReachable
  }

  syncState.backendReachable = await checkBackendReachable()
  syncState.lastCheckAt = now
  return syncState.backendReachable
}

/**
 * Force recheck of backend reachability.
 */
export async function refreshBackendReachable(): Promise<boolean> {
  syncState.backendReachable = await checkBackendReachable()
  syncState.lastCheckAt = Date.now()
  return syncState.backendReachable
}

// ── Restore progress ────────────────────────────────────────────────────────

/**
 * Restore beta progress with backend support.
 *
 * Order:
 *   1. Backend by participant_code
 *   2. localStorage by participant_code
 *   3. Empty new progress (via progressStore.initBetaProgress)
 *
 * Returns the restored progress and its source.
 */
export async function restoreBetaProgress(
  participantCode: string,
): Promise<{
  source: 'backend' | 'localStorage' | 'empty'
  progress: BetaProgressData | null
}> {
  const localProgress = loadBetaProgress(participantCode)
  console.debug(`[progressSync] restoreBetaProgress: code=${participantCode}, local=${!!localProgress}`)
  const result = await restoreFromBackend(participantCode, localProgress)

  if (result.source === 'backend' && result.progress) {
    // Backend has progress — save it to localStorage for offline resilience
    console.debug(`[progressSync] backend has progress, saving locally. lesson=${result.progress.currentLessonId}`)
    saveBetaProgress(result.progress)
  }

  console.debug(`[progressSync] restore result: source=${result.source}, found=${!!result.progress}`)
  return result
}

// ── Sync single operations ──────────────────────────────────────────────────

/**
 * Sync lesson started event.
 * Always saves to localStorage first (optimistic), then attempts backend sync.
 */
export async function syncLessonStarted(lessonId: string): Promise<void> {
  const code = getStoredParticipantCode()
  if (!code) return

  // Always save locally first (optimistic)
  const { trackLessonStarted } = await import('./progressStore')
  trackLessonStarted(lessonId)

  // Best-effort backend sync
  try {
    if (await isBackendReachable()) {
      await markLessonStartedBackend(code, lessonId)
    } else {
      syncState.hasPendingSync = true
    }
  } catch {
    syncState.hasPendingSync = true
  }
}

/**
 * Sync mission result.
 *
 * Always saves locally first, then syncs accumulated stats to backend.
 * Uses localStorage values to ensure accumulated attempts/hints are correct.
 */
export async function syncMissionResult(
  lessonId: string,
  passed: boolean,
  _attempts: number,
  _hintsUsed: number,
): Promise<void> {
  const code = getStoredParticipantCode()
  if (!code) return

  // Always save locally first
  const { trackMissionResult, trackMissionAttempt, loadBetaProgress } = await import('./progressStore')
  trackMissionAttempt(lessonId, _hintsUsed > 0)
  trackMissionResult(lessonId, passed)

  // Read back accumulated stats from localStorage
  const localProgress = loadBetaProgress(code)
  const stats = localProgress?.missionStats?.[lessonId]

  // Best-effort backend sync
  try {
    if (await isBackendReachable()) {
      await saveMissionResultBackend(
        code,
        lessonId,
        passed,
        stats?.attempts ?? _attempts,
        stats?.hintsUsed ?? _hintsUsed,
      )
    } else {
      syncState.hasPendingSync = true
    }
  } catch {
    syncState.hasPendingSync = true
  }
}

/**
 * Sync hint used event.
 */
export async function syncHintUsed(lessonId: string): Promise<void> {
  const code = getStoredParticipantCode()
  if (!code) return

  try {
    if (await isBackendReachable()) {
      await saveHintUsedBackend(code, lessonId)
    } else {
      syncState.hasPendingSync = true
    }
  } catch {
    syncState.hasPendingSync = true
  }
}

/**
 * Sync lesson completed event.
 */
export async function syncLessonCompleted(lessonId: string): Promise<void> {
  const code = getStoredParticipantCode()
  if (!code) return

  // Always save locally first
  const { trackLessonCompleted } = await import('./progressStore')
  trackLessonCompleted(lessonId)

  // Best-effort backend sync
  try {
    if (await isBackendReachable()) {
      await markLessonCompletedBackend(code, lessonId)
    } else {
      syncState.hasPendingSync = true
    }
  } catch {
    syncState.hasPendingSync = true
  }
}

/**
 * Try to flush any pending syncs.
 * Called on app startup or when backend becomes reachable again.
 */
export async function flushPendingSync(): Promise<void> {
  if (!syncState.hasPendingSync) return

  const reachable = await refreshBackendReachable()
  if (!reachable) return

  // Create/update progress on backend based on current localStorage state
  const code = getStoredParticipantCode()
  if (!code) return

  try {
    const currentProgress = getCurrentBetaProgress()
    await createBackendProgress(code)

    // Sync each completed lesson
    for (const lessonId of currentProgress.completedLessons) {
      await markLessonCompletedBackend(code, lessonId)
    }

    // Sync each lesson's mission stats
    for (const [lessonId, stats] of Object.entries(currentProgress.missionStats)) {
      await saveMissionResultBackend(
        code,
        lessonId,
        stats.passed,
        stats.attempts,
        stats.hintsUsed,
      )
      // Sync hint counts
      if (stats.hintsUsed > 0) {
        for (let i = 0; i < stats.hintsUsed; i++) {
          await saveHintUsedBackend(code, lessonId)
        }
      }
    }

    // Sync lesson statuses
    for (const [lessonId, status] of Object.entries(currentProgress.lessonStatus)) {
      if (status === 'started') {
        await markLessonStartedBackend(code, lessonId)
      }
    }

    syncState.hasPendingSync = false
  } catch {
    // Backend sync will be retried later
  }
}

/**
 * Get the current sync state.
 */
export function getSyncState(): SyncState {
  return { ...syncState }
}

/**
 * Reset sync state (for testing).
 */
export function resetSyncState(): void {
  syncState = {
    backendReachable: false,
    lastCheckAt: null,
    hasPendingSync: false,
  }
}
