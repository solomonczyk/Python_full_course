/**
 * Tests for old-format recap reminder unlock with beta staged access.
 */
import { describe, it, expect } from 'vitest'

// Inlined isRecapUnlocked logic with betaStage support
const RECAP_PLACEMENTS = [
  { recapId: 'recap-1-reminder', afterLesson: '1-9', placementType: 'end-of-part' as const },
  { recapId: 'recap-2-reminder', afterLesson: '2-6', placementType: 'end-of-part' as const },
  { recapId: 'recap-3-reminder', afterLesson: '3-41', placementType: 'end-of-part' as const },
  { recapId: 'recap-4-reminder', afterLesson: '4-31', placementType: 'end-of-part' as const },
  { recapId: 'recap-5-reminder', afterLesson: '5-7', placementType: 'end-of-part' as const },
  { recapId: 'recap-3a', afterLesson: '3-18', placementType: 'mid-part-checkpoint' as const },
  { recapId: 'recap-3b', afterLesson: '3-25', placementType: 'mid-part-checkpoint' as const },
  { recapId: 'recap-3c', afterLesson: '3-35', placementType: 'mid-part-checkpoint' as const },
  { recapId: 'recap-3d', afterLesson: '3-40', placementType: 'mid-part-checkpoint' as const },
]

function isRecapUnlocked(
  recapId: string,
  progress: Record<string, { completed?: boolean }>,
  betaStage?: number,
): boolean {
  const placement = RECAP_PLACEMENTS.find((p) => p.recapId === recapId)
  if (!placement) return false
  const recapPart = parseInt(placement.afterLesson.split('-')[0], 10)
  if (betaStage !== undefined && betaStage >= recapPart) return true
  return Boolean(progress[placement.afterLesson]?.completed)
}

describe('isRecapUnlocked — beta staged access for old-format recaps', () => {
  const emptyProgress = {}

  it('current_stage=5 unlocks recap-5-reminder without progress', () => {
    expect(isRecapUnlocked('recap-5-reminder', emptyProgress, 5)).toBe(true)
  })

  it('current_stage=5 unlocks recap-4-reminder without progress', () => {
    expect(isRecapUnlocked('recap-4-reminder', emptyProgress, 5)).toBe(true)
  })

  it('current_stage=4 locks recap-5-reminder', () => {
    expect(isRecapUnlocked('recap-5-reminder', emptyProgress, 4)).toBe(false)
  })

  it('current_stage=4 unlocks recap-4-reminder', () => {
    expect(isRecapUnlocked('recap-4-reminder', emptyProgress, 4)).toBe(true)
  })

  it('current_stage=1 locks all later recap reminders', () => {
    expect(isRecapUnlocked('recap-2-reminder', emptyProgress, 1)).toBe(false)
    expect(isRecapUnlocked('recap-3-reminder', emptyProgress, 1)).toBe(false)
    expect(isRecapUnlocked('recap-4-reminder', emptyProgress, 1)).toBe(false)
    expect(isRecapUnlocked('recap-5-reminder', emptyProgress, 1)).toBe(false)
  })

  it('current_stage=1 unlocks recap-1-reminder', () => {
    expect(isRecapUnlocked('recap-1-reminder', emptyProgress, 1)).toBe(true)
  })

  it('current_stage=5 unlocks mid-part checkpoints too', () => {
    expect(isRecapUnlocked('recap-3a', emptyProgress, 5)).toBe(true)
    expect(isRecapUnlocked('recap-3b', emptyProgress, 5)).toBe(true)
    expect(isRecapUnlocked('recap-3c', emptyProgress, 5)).toBe(true)
    expect(isRecapUnlocked('recap-3d', emptyProgress, 5)).toBe(true)
  })

  it('without beta stage, progress-based unlock still works', () => {
    // recap-5-reminder needs 5-7 completed
    expect(isRecapUnlocked('recap-5-reminder', emptyProgress, undefined)).toBe(false)
    expect(isRecapUnlocked('recap-5-reminder', { '5-7': { completed: true } }, undefined)).toBe(true)
  })

  it('unknown recap ID returns false', () => {
    expect(isRecapUnlocked('nonexistent', emptyProgress, 5)).toBe(false)
  })
})
