import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import type { LessonSummary, RecapSummary, PartFlowItem } from '../types'
import { useProgressContext } from '../hooks/ProgressContext'
import {
  RECAP_PLACEMENTS,
  isRecapUnlocked,
  isRecapCompleted,
} from '../data/recapPlacements'
import { parseLessonId } from '../utils/lessonId'

interface Props {
  lessons: LessonSummary[]
}

const PART_LABELS: Record<number, { label: string; icon: string }> = {
  1: { label: 'Rituals', icon: '🔮' },
  2: { label: 'Alchemy', icon: '⚗️' },
  3: { label: 'Logic', icon: '⚙️' },
  4: { label: 'Mastery', icon: '🏰' },
  5: { label: 'Constructs', icon: '🧱' },
}

const PART_IMAGES: Record<number, string> = {
  1: '/parts/rituals.webp',
  2: '/parts/logic.webp',
  3: '/parts/alchemy.webp',
  4: '/parts/mastery.webp',
  5: '/parts/part5.webp',
}

function buildFlowItems(
  partLessons: LessonSummary[],
  allRecaps: RecapSummary[],
  progress: Record<string, { completed?: boolean }>,
): PartFlowItem[] {
  const items: PartFlowItem[] = []
  for (const lesson of partLessons) {
    items.push({ type: 'lesson', id: lesson.id, lesson })

    // Insert any recap placed after this lesson
    const recapsAfter = allRecaps.filter((r) => {
      const placement = RECAP_PLACEMENTS.find((p) => p.recapId === r.id)
      return placement?.afterLesson === lesson.id
    })
    for (const recap of recapsAfter) {
      items.push({
        type: 'recap',
        id: recap.id,
        recap,
        unlocked: isRecapUnlocked(recap.id, progress),
        completed: isRecapCompleted(recap.id, progress),
      })
    }
  }
  return items
}

export default function PartPage({ lessons }: Props) {
  const { partNum } = useParams<{ partNum: string }>()
  const navigate = useNavigate()
  const { progress, isLessonUnlocked } = useProgressContext()
  const [recaps, setRecaps] = useState<RecapSummary[]>([])
  const [loading, setLoading] = useState(true)

  const part = parseInt(partNum ?? '0', 10)
  const info = PART_LABELS[part]
  const partImage = PART_IMAGES[part]

  useEffect(() => {
    fetch('/api/recaps')
      .then((r) => r.json())
      .then((data: RecapSummary[]) => {
        if (Array.isArray(data)) {
          setRecaps(data.filter((r) => r.part === part))
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [part])

  const partLessons = lessons
    .filter((l) => l.part === part)
    .sort((a, b) => {
      const aParsed = parseLessonId(a.id)
      const bParsed = parseLessonId(b.id)
      return (aParsed.index ?? 0) - (bParsed.index ?? 0)
    })

  const total = partLessons.length
  const done = partLessons.filter((l) => progress[l.id]?.completed).length
  const allDone = done === total
  const flowItems = buildFlowItems(partLessons, recaps, progress)

  if (!info) {
    return (
      <div
        className="rounded-xl p-6"
        style={{
          background: '#1a1924',
          border: '1px solid rgba(255,107,107,0.3)',
        }}
      >
        <p style={{ color: '#ff6b6b' }}>
          Part {part} не найдена.{' '}
          <Link to="/" style={{ color: '#c9a227' }}>
            На главную
          </Link>
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        to="/"
        className="text-xs hover:underline inline-block"
        style={{ color: '#9b98a8' }}
      >
        ← На главную
      </Link>

      {/* Part header */}
      <div
        className="rounded-xl overflow-hidden"
        style={{
          border: '1px solid rgba(201,162,39,0.15)',
        }}
      >
        <div className="relative h-[180px]">
          <img
            src={partImage}
            alt={`Part ${part}`}
            className="w-full h-full object-cover"
          />
          <div
            className="absolute inset-0 flex flex-col justify-end p-5"
            style={{
              background:
                'linear-gradient(to top, rgba(15,14,23,0.95) 0%, rgba(15,14,23,0.3) 100%)',
            }}
          >
            <div className="flex items-center gap-2 mb-1">
              <span className="text-lg">{info.icon}</span>
              <span
                className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded"
                style={{
                  background: allDone
                    ? 'rgba(0,212,170,0.2)'
                    : 'rgba(201,162,39,0.15)',
                  color: allDone ? '#00d4aa' : '#c9a227',
                  border: allDone
                    ? '1px solid rgba(0,212,170,0.3)'
                    : '1px solid rgba(201,162,39,0.2)',
                }}
              >
                Part {part}
              </span>
            </div>
            <h1 className="text-lg font-bold" style={{ color: '#e8e6f0' }}>
              {info.label}
            </h1>
            <p className="text-xs mt-1" style={{ color: '#9b98a8' }}>
              {allDone
                ? `Пройдено • ${done}/${total} уроков`
                : `Прогресс • ${done}/${total} уроков`}
            </p>
            <div className="mt-2 h-1.5 rounded-full max-w-[300px]">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{
                  width: `${total > 0 ? (done / total) * 100 : 0}%`,
                  background: allDone ? '#00d4aa' : '#c9a227',
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Flow list */}
      {loading ? (
        <div className="text-xs py-8 text-center" style={{ color: '#9b98a8' }}>
          Загрузка...
        </div>
      ) : (
        <div className="space-y-2">
          {flowItems.map((item) =>
            item.type === 'lesson' ? (
              <LessonCard
                key={item.id}
                lesson={item.lesson}
                isUnlocked={
                  item.lesson.locked
                    ? isLessonUnlocked(item.lesson.id, lessons)
                    : true
                }
                isCompleted={Boolean(progress[item.lesson.id]?.completed)}
                onClick={() => navigate(`/lesson/${item.lesson.id}`)}
              />
            ) : (
              <RecapCard
                key={item.id}
                recap={item.recap}
                unlocked={item.unlocked}
                completed={item.completed}
                onClick={() => navigate(`/recap/${item.recap.id}`)}
              />
            ),
          )}
        </div>
      )}
    </div>
  )
}

// ── Lesson card ──────────────────────────────────────────────────────────────

function LessonCard({
  lesson,
  isUnlocked,
  isCompleted,
  onClick,
}: {
  lesson: LessonSummary
  isUnlocked: boolean
  isCompleted: boolean
  onClick: () => void
}) {
  return (
    <button
      onClick={isUnlocked || isCompleted ? onClick : undefined}
      disabled={!isUnlocked && !isCompleted}
      className="w-full flex items-center gap-3 p-3 rounded-xl text-left cursor-pointer transition-all hover:scale-[1.01] border-none"
      style={{
        background: '#1a1924',
        border: '1px solid rgba(201,162,39,0.1)',
        opacity: !isUnlocked && !isCompleted ? 0.45 : 1,
      }}
    >
      <span
        className="material-symbols-outlined text-lg flex items-center justify-center"
        style={{
          color: isCompleted
            ? '#00d4aa'
            : isUnlocked
              ? '#e8e6f0'
              : 'rgba(155,152,168,0.4)',
          fontVariationSettings: `'FILL' ${isCompleted ? '1' : '0'}`,
        }}
      >
        {!isUnlocked && !isCompleted
          ? 'lock'
          : isCompleted
            ? 'check_circle'
            : 'radio_button_unchecked'}
      </span>
      <div className="flex-1 min-w-0">
        <div
          className="text-xs font-bold truncate"
          style={{ color: isCompleted ? '#9b98a8' : '#e8e6f0' }}
        >
          {lesson.id} {lesson.title}
        </div>
        <div className="text-[10px]" style={{ color: '#9b98a8' }}>
          {lesson.topic}
        </div>
      </div>
    </button>
  )
}

// ── Recap card ───────────────────────────────────────────────────────────────

function RecapCard({
  recap,
  unlocked,
  completed,
  onClick,
}: {
  recap: RecapSummary
  unlocked: boolean
  completed: boolean
  onClick: () => void
}) {
  const isCheckpoint =
    recap.id.startsWith('recap-3') && recap.id !== 'recap-3'
  const accentColor = isCheckpoint ? '#6c5ce7' : '#c9a227'
  const label = isCheckpoint ? 'ЧЕКПОИНТ' : 'ПОВТОРЕНИЕ'
  const isDisabled = !unlocked && !completed

  return (
    <button
      onClick={isDisabled ? undefined : onClick}
      disabled={isDisabled}
      className="w-full flex items-center gap-3 p-3 rounded-xl text-left cursor-pointer transition-all hover:scale-[1.01] border-none"
      style={{
        background: 'rgba(26,25,36,0.7)',
        border: completed
          ? `1px solid rgba(0,212,170,0.3)`
          : unlocked
            ? `1px solid ${accentColor}44`
            : `1px solid rgba(201,162,39,0.08)`,
        opacity: isDisabled ? 0.4 : 1,
      }}
    >
      <span
        className="material-symbols-outlined text-lg flex items-center justify-center"
        style={{
          color: completed
            ? '#00d4aa'
            : unlocked
              ? accentColor
              : 'rgba(155,152,168,0.4)',
          fontVariationSettings: `'FILL' ${completed ? '1' : '0'}`,
        }}
      >
        {isDisabled
          ? 'lock'
          : completed
            ? 'check_circle'
            : isCheckpoint
              ? 'checklist'
              : 'menu_book'}
      </span>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span
            className="text-[10px] font-bold uppercase tracking-wider"
            style={{ color: completed ? '#00d4aa' : accentColor }}
          >
            {completed ? '✓ ' : ''}
            {label}
          </span>
          <span className="text-[10px]" style={{ color: '#9b98a8' }}>
            · Part {recap.part}
          </span>
        </div>
        <div
          className="text-xs font-bold truncate mt-0.5"
          style={{
            color: completed
              ? '#9b98a8'
              : isDisabled
                ? 'rgba(155,152,168,0.6)'
                : '#e8e6f0',
          }}
        >
          {recap.title}
        </div>
      </div>
    </button>
  )
}
