/**
 * Python Quest — Anonymous Local Analytics
 *
 * Safe, local-only analytics for beta diagnostics.
 * - No external network requests
 * - No personal data collection
 * - localStorage with in-memory fallback
 * - Never throws / never blocks UI
 */

// ── Types ─────────────────────────────────────────────────────────────────

export type AnalyticsEventName =
  | 'landing_opened'
  | 'demo_started'
  | 'lesson_started'
  | 'mission_attempted'
  | 'mission_failed'
  | 'mission_passed'
  | 'hint_used'
  | 'lesson_completed'
  | 'quest_started'
  | 'quest_completed'
  | 'student_stuck'
  | 'session_abandoned'
  | 'beta_entry_clicked'

/** Payload fields safe for anonymous local storage */
export interface AnalyticsEventPayload {
  lesson_id?: string
  mission_id?: string
  attempt_count?: number
  result?: string
  hint_id?: string
  source?: string
  route?: string
}

export interface AnalyticsEvent {
  event: AnalyticsEventName
  anonymous_session_id: string
  /** Pseudonymous participant code hash (no personal data) */
  participant_id?: string
  timestamp: string
  lesson_id?: string
  mission_id?: string
  attempt_count?: number
  result?: string
  hint_id?: string
  source?: string
  route?: string
}

// ── Constants ─────────────────────────────────────────────────────────────

const STORAGE_KEY = 'pq_analytics_events'
const SESSION_KEY = 'pq_anonymous_session_id'
const MAX_STORED_EVENTS = 500

// ── Session ID — anonymous, random, local-only ────────────────────────────

function generateSessionId(): string {
  const ts = Date.now().toString(36)
  const rand = Math.random().toString(36).slice(2, 10)
  return `pq_session_${ts}_${rand}`
}

let cachedSessionId: string | null = null

function getOrCreateSessionId(): string {
  if (cachedSessionId) return cachedSessionId

  try {
    const stored = localStorage.getItem(SESSION_KEY)
    if (stored) {
      cachedSessionId = stored
      return stored
    }
  } catch {
    // localStorage unavailable — use memory-only
  }

  const fresh = generateSessionId()
  cachedSessionId = fresh
  try {
    localStorage.setItem(SESSION_KEY, fresh)
  } catch {
    // localStorage full or unavailable — memory-only is fine
  }
  return fresh
}

// ── Storage — localStorage with memory fallback ────────────────────────────

let memoryBuffer: AnalyticsEvent[] = []

function readEvents(): AnalyticsEvent[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed: AnalyticsEvent[] = JSON.parse(raw)
      if (Array.isArray(parsed)) return parsed
    }
  } catch {
    // Corrupt data or localStorage unavailable — fall through to memory
  }
  return memoryBuffer
}

function writeEvents(events: AnalyticsEvent[]): void {
  // Always keep memory buffer in sync
  memoryBuffer = events

  try {
    const trimmed = events.slice(-MAX_STORED_EVENTS)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmed))
  } catch {
    // localStorage quota exceeded or unavailable — memory buffer is fine
  }
}

function appendEvent(event: AnalyticsEvent): void {
  const events = readEvents()
  events.push(event)
  writeEvents(events)
}

// ── Imports for participant identity binding ──────────────────────────────

import { getParticipantId } from './participantIdentity'

// ── Public API ────────────────────────────────────────────────────────────

/**
 * Track an analytics event.
 *
 * Safe to call anywhere — never throws, never blocks UI.
 * If localStorage is unavailable, falls back to in-memory buffer.
 */
export function trackEvent(
  name: AnalyticsEventName,
  payload?: AnalyticsEventPayload,
): void {
  try {
    const event: AnalyticsEvent = {
      event: name,
      anonymous_session_id: getOrCreateSessionId(),
      timestamp: new Date().toISOString(),
      ...payload,
    }

    // Bind to beta participant identity if available
    // Uses a deterministic hash of the participant code — no personal data
    const pid = getParticipantId()
    if (pid) {
      event.participant_id = pid
    }

    appendEvent(event)
  } catch {
    // Analytics failure MUST never break the app
    // Silently ignore — the app continues unaffected
  }
}

/**
 * Get all stored analytics events.
 * Useful for debug/export during beta testing.
 */
export function getStoredAnalyticsEvents(): AnalyticsEvent[] {
  try {
    return readEvents()
  } catch {
    return []
  }
}

/**
 * Clear all stored analytics events.
 */
export function clearStoredAnalyticsEvents(): void {
  try {
    memoryBuffer = []
    localStorage.removeItem(STORAGE_KEY)
  } catch {
    // Best-effort
  }
}

// ── Debug API (exposed for operator inspection) ───────────────────────────

if (typeof window !== 'undefined') {
  try {
    ;(window as any).__PYTHON_QUEST_ANALYTICS__ = {
      getEvents: getStoredAnalyticsEvents,
      clearEvents: clearStoredAnalyticsEvents,
    }
  } catch {
    // Non-browser environment — skip
  }
}
