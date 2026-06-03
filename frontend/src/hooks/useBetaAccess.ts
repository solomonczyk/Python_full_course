/**
 * useBetaAccess — Hook for beta staged access information.
 *
 * Fetches current stage for a participant code and exposes
 * helper functions for feedback submission and stage checking.
 */

import { useState, useEffect, useCallback } from 'react'
import type { BetaAccessInfo } from '../types'
import { getStoredParticipantCode } from '../lib/participantIdentity'

const BASE = '/api/beta/access'

export function useBetaAccess() {
  const [betaAccess, setBetaAccess] = useState<BetaAccessInfo | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchAccess = useCallback(async () => {
    const code = getStoredParticipantCode()
    if (!code) {
      setBetaAccess(null)
      return
    }

    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`${BASE}/${encodeURIComponent(code)}`)
      if (!res.ok) throw new Error('Failed to fetch beta access')
      const data = await res.json()
      if (data.ok) {
        setBetaAccess({
          participantCode: data.participant_code,
          currentStage: data.current_stage,
          maxStage: data.max_stage,
          hasFeedback: data.has_feedback,
          feedbackSubmittedAt: data.feedback_submitted_at,
        })
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error')
      setBetaAccess(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchAccess()
  }, [fetchAccess])

  const submitFeedback = useCallback(async (
    feedbackText: string,
    rating?: number,
  ): Promise<{ ok: boolean; error?: string }> => {
    const code = getStoredParticipantCode()
    if (!code) return { ok: false, error: 'No participant code' }

    try {
      const res = await fetch(`${BASE}/${encodeURIComponent(code)}/provide-feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feedback_text: feedbackText, rating }),
      })
      const data = await res.json()
      if (data.ok) {
        await fetchAccess()
        return { ok: true }
      }
      return { ok: false, error: data.detail || 'Failed to submit feedback' }
    } catch (e) {
      return { ok: false, error: e instanceof Error ? e.message : 'Network error' }
    }
  }, [fetchAccess])

  const refreshAccess = fetchAccess

  return {
    betaAccess,
    loading,
    error,
    submitFeedback,
    refreshAccess,
  }
}
