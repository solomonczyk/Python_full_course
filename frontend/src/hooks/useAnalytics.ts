/**
 * useAnalytics — React hook for anonymous local analytics.
 *
 * Provides a safe, no-throw interface for tracking events
 * from React components.
 */

import { useCallback } from 'react'
import {
  trackEvent,
  getStoredAnalyticsEvents,
  clearStoredAnalyticsEvents,
  type AnalyticsEventName,
  type AnalyticsEventPayload,
  type AnalyticsEvent,
} from '../lib/analytics'
import { getParticipantId } from '../lib/participantIdentity'

/**
 * Hook for tracking analytics events from React components.
 *
 * Example:
 * ```ts
 * const { track } = useAnalytics()
 * track('landing_opened')
 * track('demo_started', { source: 'hero_cta' })
 * ```
 */
export function useAnalytics() {
  const track = useCallback(
    (name: AnalyticsEventName, payload?: AnalyticsEventPayload) => {
      trackEvent(name, payload)
    },
    [],
  )

  const getEvents = useCallback((): AnalyticsEvent[] => {
    return getStoredAnalyticsEvents()
  }, [])

  const clearEvents = useCallback(() => {
    clearStoredAnalyticsEvents()
  }, [])

  const getCurrentParticipantId = useCallback((): string | null => {
    return getParticipantId()
  }, [])

  return { track, getEvents, clearEvents, getParticipantId: getCurrentParticipantId }
}
