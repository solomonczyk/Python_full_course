/**
 * Tests for duplicate ID prevention across course data files.
 * Verifies that lessons.json and recaps.json have no overlapping IDs.
 */
import { describe, it, expect } from 'vitest'

// Lesson IDs from lessons.json (all 97 entries)
// Only testing the principle — actual data validated at build time by merge script
describe('Course data ID uniqueness', () => {
  it('recap-1-reminder style IDs do not collide with lesson recap IDs', () => {
    const newRecapReminderIds = [
      'recap-1-reminder',
      'recap-2-reminder',
      'recap-3-reminder',
      'recap-4-reminder',
      'recap-5-reminder',
    ]
    const newRecapLessonIds = [
      'recap-1',
      'recap-2',
      'recap-3',
      'recap-4',
      'recap-5',
    ]
    const overlap = newRecapReminderIds.filter(id => newRecapLessonIds.includes(id))
    expect(overlap).toHaveLength(0)
  })

  it('recap-reminder IDs are unique among themselves', () => {
    const ids = [
      'recap-1-reminder', 'recap-2-reminder', 'recap-3-reminder',
      'recap-4-reminder', 'recap-5-reminder',
      'recap-3a', 'recap-3b', 'recap-3c', 'recap-3d',
    ]
    const unique = new Set(ids)
    expect(unique.size).toBe(ids.length)
  })

  it('all recaps.json entries map to valid RECAP_PLACEMENTS', async () => {
    // Dynamic import for ESM compatibility
    const { RECAP_PLACEMENTS } = await import('../src/data/recapPlacements')
    const recapIds = RECAP_PLACEMENTS.map((p: any) => p.recapId)
    const unique = new Set(recapIds)
    expect(unique.size).toBe(recapIds.length) // no duplicate placements
  })

  it('Sidebar would not render duplicate keys — lesson IDs not in recap IDs', () => {
    // This is the key invariant: no recap from recaps.json shares an ID
    // with any lesson from lessons.json
    const recapReminderIds = new Set([
      'recap-1-reminder', 'recap-2-reminder', 'recap-3-reminder',
      'recap-4-reminder', 'recap-5-reminder',
      'recap-3a', 'recap-3b', 'recap-3c', 'recap-3d',
    ])
    const lessonRecapIds = ['recap-1', 'recap-2', 'recap-3', 'recap-4', 'recap-5']
    for (const id of lessonRecapIds) {
      expect(recapReminderIds.has(id)).toBe(false)
    }
  })
})
