/**
 * Safe lesson ID parser.
 * Lesson IDs are formatted as "{part}-{index}", e.g. "1-8", "3-12".
 * This utility safely parses such IDs without crashing on undefined/malformed input.
 */

export interface ParsedLessonId {
  part: number | null
  index: number | null
}

/**
 * Safely parse a lesson ID string of the form "{part}-{index}".
 * Returns { part: null, index: null } for any invalid input.
 */
export function parseLessonId(lessonId?: string | null): ParsedLessonId {
  if (!lessonId || typeof lessonId !== 'string') {
    return { part: null, index: null }
  }

  const parts = lessonId.split('-')

  if (parts.length < 2) {
    return { part: null, index: null }
  }

  const part = Number(parts[0])
  const index = Number(parts[1])

  if (!Number.isFinite(part) || !Number.isFinite(index)) {
    return { part: null, index: null }
  }

  return { part, index }
}
