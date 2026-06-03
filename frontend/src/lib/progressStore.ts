/**
 * Python Quest — Beta Progress Store
 *
 * Enhanced progress persistence bound to participant code.
 * Coexists with the existing `python-quest-progress` localStorage key.
 * - Stores rich mission stats (attempts, fails, hints)
 * - Tracks lesson status (started / completed)
 * - Preserves existing progress via migration
 * - Never collects personal data
 */

import type { BetaProgressData, BetaMissionStats, BetaLessonStatus } from '../types'
import { getStoredParticipantCode, generateParticipantCode, getOrCreateParticipantCode } from './participantIdentity'

// ── Constants ───────────────────────────────────────────────────────────────

const BETA_PROGRESS_KEY = 'pq_beta_progress'
const LEGACY_PROGRESS_KEY = 'python-quest-progress'

// ── Defaults ────────────────────────────────────────────────────────────────

function createDefaultProgress(participantCode: string): BetaProgressData {
  return {
    participantCode,
    currentLessonId: '1-1',
    completedLessons: [],
    lessonStatus: {},
    missionStats: {},
    lastActiveAt: new Date().toISOString(),
    createdAt: new Date().toISOString(),
  }
}

// ── Legacy migration ────────────────────────────────────────────────────────

interface LegacyRecord {
  lesson_id: string
  completed: boolean
  quiz_passed: boolean
  mission_done: boolean
  score: number | null
  updated_at: string
}

function loadLegacyProgress(): Record<string, LegacyRecord> | null {
  try {
    const raw = localStorage.getItem(LEGACY_PROGRESS_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (typeof parsed === 'object' && parsed !== null) return parsed
    return null
  } catch {
    return null
  }
}

function migrateFromLegacy(participantCode: string, legacy: Record<string, LegacyRecord>): BetaProgressData {
  const progress = createDefaultProgress(participantCode)
  const lessonIds = Object.keys(legacy).sort()

  let latestLessonId = '1-1'
  let latestTimestamp = ''

  for (const lessonId of lessonIds) {
    const record = legacy[lessonId]
    if (record.completed) {
      progress.completedLessons.push(lessonId)
      progress.lessonStatus[lessonId] = 'completed'
      progress.missionStats[lessonId] = {
        attempts: 1,
        failed: record.mission_done ? 0 : 1,
        passed: record.mission_done,
        hintsUsed: 0,
      }
    }
    if (record.updated_at && record.updated_at > latestTimestamp) {
      latestTimestamp = record.updated_at
      latestLessonId = lessonId
    }
  }

  if (lessonIds.length > 0) {
    const last = lessonIds[lessonIds.length - 1]
    // If last lesson is not completed, mark as current
    if (!legacy[last]?.completed) {
      progress.currentLessonId = last
      progress.lessonStatus[last] = 'started'
    } else if (latestLessonId !== '1-1') {
      // Find next lesson after the last completed one
      progress.currentLessonId = latestLessonId
    }
  }

  return progress
}

// ── Load / Save ─────────────────────────────────────────────────────────────

/**
 * Load beta progress for a given participant code.
 * Returns null if no progress exists for this code.
 */
export function loadBetaProgress(participantCode: string): BetaProgressData | null {
  try {
    const raw = localStorage.getItem(BETA_PROGRESS_KEY)
    if (!raw) return null
    const data: BetaProgressData = JSON.parse(raw)
    if (data.participantCode !== participantCode) return null
    return data
  } catch {
    return null
  }
}

/**
 * Save beta progress to local storage.
 */
export function saveBetaProgress(data: BetaProgressData): void {
  try {
    data.lastActiveAt = new Date().toISOString()
    localStorage.setItem(BETA_PROGRESS_KEY, JSON.stringify(data))
  } catch {
    // localStorage unavailable or full — best-effort
  }
}

/**
 * Initialize beta progress for a participant code.
 * Migrates from legacy progress if available.
 * Returns existing progress if already initialized.
 */
export function initBetaProgress(participantCode?: string): BetaProgressData {
  const code = participantCode ?? getOrCreateParticipantCode()

  // Return existing if already initialized for this code
  const existing = loadBetaProgress(code)
  if (existing) return existing

  // Try to migrate from legacy progress
  const legacy = loadLegacyProgress()

  if (legacy && Object.keys(legacy).length > 0) {
    const migrated = migrateFromLegacy(code, legacy)
    saveBetaProgress(migrated)
    return migrated
  }

  // Fresh start
  const fresh = createDefaultProgress(code)
  saveBetaProgress(fresh)
  return fresh
}

/**
 * Load the progress for the current participant (from localStorage).
 * Falls back to initialized default if none exists.
 */
export function getCurrentBetaProgress(): BetaProgressData {
  const code = getStoredParticipantCode()
  if (!code) return createDefaultProgress(generateParticipantCode())

  return loadBetaProgress(code) ?? initBetaProgress(code)
}

// ── Trackers ────────────────────────────────────────────────────────────────

/**
 * Track that a lesson was opened/started.
 */
export function trackLessonStarted(lessonId: string): void {
  const code = getStoredParticipantCode()
  if (!code) return

  const progress = loadBetaProgress(code) ?? initBetaProgress(code)
  progress.currentLessonId = lessonId
  if (!progress.lessonStatus[lessonId]) {
    progress.lessonStatus[lessonId] = 'started'
  }
  saveBetaProgress(progress)
}

/**
 * Track that progress was updated (current lesson changed).
 */
export function updateCurrentLesson(lessonId: string): void {
  const code = getStoredParticipantCode()
  if (!code) return

  const progress = loadBetaProgress(code) ?? initBetaProgress(code)
  progress.currentLessonId = lessonId
  saveBetaProgress(progress)
}

/**
 * Track a mission attempt (failed or passed).
 */
export function trackMissionAttempt(lessonId: string, hintUsed: boolean): void {
  const code = getStoredParticipantCode()
  if (!code) return

  const progress = loadBetaProgress(code) ?? initBetaProgress(code)
  if (!progress.missionStats[lessonId]) {
    progress.missionStats[lessonId] = { attempts: 0, failed: 0, passed: false, hintsUsed: 0 }
  }
  progress.missionStats[lessonId].attempts++
  if (hintUsed) {
    progress.missionStats[lessonId].hintsUsed++
  }
  saveBetaProgress(progress)
}

/**
 * Track a mission result (pass/fail).
 */
export function trackMissionResult(lessonId: string, passed: boolean): void {
  const code = getStoredParticipantCode()
  if (!code) return

  const progress = loadBetaProgress(code) ?? initBetaProgress(code)
  if (!progress.missionStats[lessonId]) {
    progress.missionStats[lessonId] = { attempts: 0, failed: 0, passed: false, hintsUsed: 0 }
  }
  if (passed) {
    progress.missionStats[lessonId].passed = true
    if (!progress.completedLessons.includes(lessonId)) {
      progress.completedLessons.push(lessonId)
    }
    progress.lessonStatus[lessonId] = 'completed'
  } else {
    progress.missionStats[lessonId].failed++
  }
  saveBetaProgress(progress)
}

/**
 * Track lesson completion.
 */
export function trackLessonCompleted(lessonId: string): void {
  const code = getStoredParticipantCode()
  if (!code) return

  const progress = loadBetaProgress(code) ?? initBetaProgress(code)
  if (!progress.completedLessons.includes(lessonId)) {
    progress.completedLessons.push(lessonId)
  }
  progress.lessonStatus[lessonId] = 'completed'
  saveBetaProgress(progress)
}

// ── Query helpers ───────────────────────────────────────────────────────────

/**
 * Check if a lesson has been completed in the current beta progress.
 */
export function isBetaLessonCompleted(lessonId: string): boolean {
  const code = getStoredParticipantCode()
  if (!code) return false
  const progress = loadBetaProgress(code)
  if (!progress) return false
  return progress.completedLessons.includes(lessonId)
}

/**
 * Get the current lesson ID from beta progress.
 */
export function getCurrentLessonId(): string {
  const code = getStoredParticipantCode()
  if (!code) return '1-1'
  const progress = loadBetaProgress(code)
  if (!progress) return '1-1'
  return progress.currentLessonId
}

/**
 * Clear all beta progress data (for testing or reset).
 */
export function clearBetaProgress(): void {
  try {
    localStorage.removeItem(BETA_PROGRESS_KEY)
  } catch {
    // best-effort
  }
}
