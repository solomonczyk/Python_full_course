/**
 * Unit tests for isLessonUnlocked — beta staged access lock logic.
 */
import { describe, it, expect } from 'vitest'
import { isLessonUnlocked } from '../src/hooks/ProgressContext'
import type { LessonSummary } from '../src/types'

function makeLesson(id: string, part: number, locked = true): LessonSummary {
  return {
    id,
    part,
    chapter: 1,
    lesson: parseInt(id.split('-')[1] || '1'),
    slug: id,
    title: `Lesson ${id}`,
    subtitle: '',
    topic: 'test',
    locked,
    difficulty: 'easy',
    estimated_time_min: 10,
  }
}

describe('isLessonUnlocked — beta staged access', () => {
  const lessons: LessonSummary[] = [
    makeLesson('1-1', 1),  // idx 0, first lesson
    makeLesson('4-30', 4),
    makeLesson('4-31', 4),
    makeLesson('5-1', 5),
    makeLesson('5-2', 5),
    makeLesson('5-7', 5),
  ]

  const emptyProgress = {}

  it('first lesson always unlocked regardless of beta stage', () => {
    expect(isLessonUnlocked('1-1', lessons, emptyProgress, 1)).toBe(true)
    expect(isLessonUnlocked('1-1', lessons, emptyProgress, 5)).toBe(true)
    expect(isLessonUnlocked('1-1', lessons, emptyProgress, undefined)).toBe(true)
  })

  it('current_stage=5 unlocks Part 5 lessons without prior progress', () => {
    expect(isLessonUnlocked('5-1', lessons, emptyProgress, 5)).toBe(true)
    expect(isLessonUnlocked('5-2', lessons, emptyProgress, 5)).toBe(true)
    expect(isLessonUnlocked('5-7', lessons, emptyProgress, 5)).toBe(true)
  })

  it('current_stage=5 unlocks Part 4 lessons without prior progress', () => {
    expect(isLessonUnlocked('4-30', lessons, emptyProgress, 5)).toBe(true)
    expect(isLessonUnlocked('4-31', lessons, emptyProgress, 5)).toBe(true)
  })

  it('current_stage=1 locks Part 5 lessons', () => {
    expect(isLessonUnlocked('5-1', lessons, emptyProgress, 1)).toBe(false)
    expect(isLessonUnlocked('5-7', lessons, emptyProgress, 1)).toBe(false)
  })

  it('current_stage=4 locks Part 5 but unlocks Part 4', () => {
    expect(isLessonUnlocked('4-30', lessons, emptyProgress, 4)).toBe(true)
    expect(isLessonUnlocked('5-1', lessons, emptyProgress, 4)).toBe(false)
  })

  it('fresh participant (current_stage=1) sees Part 5 locked', () => {
    expect(isLessonUnlocked('5-1', lessons, emptyProgress, 1)).toBe(false)
  })

  it('without beta stage, sequential progress still applies', () => {
    // No beta stage, 5-1 is not first lesson and prev (4-31) not completed → locked
    expect(isLessonUnlocked('5-1', lessons, emptyProgress, undefined)).toBe(false)
    expect(isLessonUnlocked('5-2', lessons, emptyProgress, undefined)).toBe(false)
  })

  it('without beta stage, explicitly unlocked lessons are open', () => {
    const unlockedLessons = [
      ...lessons.slice(0, -1),
      makeLesson('5-7', 5, false),  // explicitly unlocked
    ]
    expect(isLessonUnlocked('5-7', unlockedLessons, emptyProgress, undefined)).toBe(true)
  })

  it('operator unlock of stage 5 reflects immediately on all parts', () => {
    // Simulate: participant had stage=1, now operator unlocks to stage=5
    // After refresh, betaStage becomes 5
    for (const part of [1, 2, 3, 4, 5]) {
      const partLessons = [
        makeLesson(`${part}-1`, part),
        makeLesson(`${part}-5`, part),
        makeLesson(`${part}-9`, part),
      ]
      const allLessons = [makeLesson('1-1', 1), ...partLessons]
      for (const l of partLessons) {
        expect(isLessonUnlocked(l.id, allLessons, emptyProgress, 5)).toBe(true)
      }
    }
  })
})
