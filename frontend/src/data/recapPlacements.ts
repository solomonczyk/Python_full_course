export interface RecapPlacement {
  recapId: string
  afterLesson: string
  placementType: 'end-of-part' | 'mid-part-checkpoint'
}

/**
 * Placement mapping: which recap should appear after which lesson.
 * Determines when a recap unlocks and where it shows in the part flow.
 */
export const RECAP_PLACEMENTS: RecapPlacement[] = [
  // Part 1
  { recapId: 'recap-1-reminder', afterLesson: '1-9', placementType: 'end-of-part' },

  // Part 2
  { recapId: 'recap-2-reminder', afterLesson: '2-6', placementType: 'end-of-part' },

  // Part 3 — mid-part checkpoints at chapter boundaries + full recap
  { recapId: 'recap-3a', afterLesson: '3-18', placementType: 'mid-part-checkpoint' },
  { recapId: 'recap-3b', afterLesson: '3-25', placementType: 'mid-part-checkpoint' },
  { recapId: 'recap-3c', afterLesson: '3-35', placementType: 'mid-part-checkpoint' },
  { recapId: 'recap-3d', afterLesson: '3-40', placementType: 'mid-part-checkpoint' },
  { recapId: 'recap-3-reminder', afterLesson: '3-41', placementType: 'end-of-part' },

  // Part 4
  { recapId: 'recap-4-reminder', afterLesson: '4-31', placementType: 'end-of-part' },

  // Part 5
  { recapId: 'recap-5-reminder', afterLesson: '5-7', placementType: 'end-of-part' },
]

/**
 * Check if a recap's prerequisite lesson is completed, OR if beta stage covers the recap's part.
 *
 * The part is derived from afterLesson: "5-7" → part 5.
 */
export function isRecapUnlocked(
  recapId: string,
  progress: Record<string, { completed?: boolean }>,
  betaStage?: number,
): boolean {
  const placement = RECAP_PLACEMENTS.find((p) => p.recapId === recapId)
  if (!placement) return false

  // Beta stage check: if participant's stage covers the recap's part, unlock
  const recapPart = parseInt(placement.afterLesson.split('-')[0], 10)
  if (betaStage !== undefined && betaStage >= recapPart) return true

  return Boolean(progress[placement.afterLesson]?.completed)
}

/**
 * Check if a recap itself has been completed.
 * Handles both the correct key (recap-1) and the legacy buggy key (recap-recap-1)
 * for backward compatibility with existing progress data.
 */
export function isRecapCompleted(
  recapId: string,
  progress: Record<string, { completed?: boolean }>,
): boolean {
  return Boolean(
    progress[recapId]?.completed || progress[`recap-${recapId}`]?.completed,
  )
}

/**
 * Get all recaps for a given part that have a placement mapping.
 */
export function getRecapsForPart(
  partNum: number,
  allRecaps: { id: string; part: number; title: string }[],
): { id: string; part: number; title: string }[] {
  const mappedIds = new Set(
    RECAP_PLACEMENTS.filter((p) => {
      const recap = allRecaps.find((r) => r.id === p.recapId)
      return recap?.part === partNum
    }).map((p) => p.recapId),
  )
  return allRecaps.filter((r) => r.part === partNum && mappedIds.has(r.id))
}
