/**
 * Python Quest — Beta Participant Identity
 *
 * Lightweight beta identity layer using participant codes.
 * - Generates human-readable BETA-XXXXXX codes
 * - Stores locally (no personal data)
 * - Provides hash for analytics binding
 * - No login, no email, no password, no personal data
 */

// ── Constants ───────────────────────────────────────────────────────────────

const PARTICIPANT_CODE_KEY = 'pq_beta_participant_code'
const PARTICIPANT_CREATED_KEY = 'pq_beta_created_at'

/** Characters safe from confusion (no 0/O, 1/I/L) */
const CODE_CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
const CODE_LENGTH = 6
const CODE_PATTERN = /^BETA-[A-Z0-9]{6}$/

// ── Generation ──────────────────────────────────────────────────────────────

/**
 * Generate a random BETA-XXXXXX participant code.
 * The code contains no personal information.
 */
export function generateParticipantCode(): string {
  let code = ''
  for (let i = 0; i < CODE_LENGTH; i++) {
    code += CODE_CHARS[Math.floor(Math.random() * CODE_CHARS.length)]
  }
  return `BETA-${code}`
}

// ── Storage ─────────────────────────────────────────────────────────────────

/**
 * Get stored participant code or create a new one.
 * Safe to call anywhere — never throws.
 */
export function getOrCreateParticipantCode(): string {
  const stored = getStoredParticipantCode()
  if (stored) return stored

  const code = generateParticipantCode()
  try {
    localStorage.setItem(PARTICIPANT_CODE_KEY, code)
    localStorage.setItem(PARTICIPANT_CREATED_KEY, new Date().toISOString())
  } catch {
    // localStorage unavailable — return code anyway (memory-only session)
  }
  return code
}

/**
 * Get stored participant code without creating one.
 * Returns null if no code exists.
 */
export function getStoredParticipantCode(): string | null {
  try {
    return localStorage.getItem(PARTICIPANT_CODE_KEY)
  } catch {
    return null
  }
}

/**
 * Get the creation timestamp of the participant identity.
 */
export function getParticipantCreatedAt(): string | null {
  try {
    return localStorage.getItem(PARTICIPANT_CREATED_KEY)
  } catch {
    return null
  }
}

/**
 * Store a participant code entered by a returning user.
 * Validates format before storing.
 * Returns true if code was accepted.
 */
export function storeParticipantCode(code: string): boolean {
  const trimmed = code.trim().toUpperCase()
  if (!CODE_PATTERN.test(trimmed)) return false

  try {
    localStorage.setItem(PARTICIPANT_CODE_KEY, trimmed)
    // Preserve original created_at if already set
    if (!localStorage.getItem(PARTICIPANT_CREATED_KEY)) {
      localStorage.setItem(PARTICIPANT_CREATED_KEY, new Date().toISOString())
    }
  } catch {
    return false
  }
  return true
}

/**
 * Clear the participant identity from local storage.
 */
export function clearParticipantIdentity(): void {
  try {
    localStorage.removeItem(PARTICIPANT_CODE_KEY)
    localStorage.removeItem(PARTICIPANT_CREATED_KEY)
  } catch {
    // best-effort
  }
}

// ── Hashing for analytics ───────────────────────────────────────────────────

/**
 * Create a deterministic pseudonymous hash of a participant code.
 * This is NOT personal data and cannot be reversed to the original code.
 * Used for analytics binding without exposing the raw code.
 */
export function hashParticipantCode(code: string): string {
  let hash = 0
  for (let i = 0; i < code.length; i++) {
    const char = code.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32bit integer
  }
  return 'p_' + Math.abs(hash >>> 0).toString(36)
}

/**
 * Get the pseudonymous participant ID for analytics payload.
 * Returns null if no participant code is stored.
 */
export function getParticipantId(): string | null {
  const code = getStoredParticipantCode()
  if (!code) return null
  return hashParticipantCode(code)
}

// ── Format validation ───────────────────────────────────────────────────────

/**
 * Check if a string looks like a valid participant code format.
 */
export function isValidCodeFormat(code: string): boolean {
  return CODE_PATTERN.test(code.trim().toUpperCase())
}
