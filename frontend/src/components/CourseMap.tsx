import { Link } from 'react-router-dom'
import type { LessonSummary } from '../types'
import { useProgress } from '../hooks/useProgress'

interface Props {
  lessons: LessonSummary[]
}

export default function CourseMap({ lessons }: Props) {
  const { progress, totalLessons, completedCount } = useProgress()
  const total = lessons.length || totalLessons
  const pct = total > 0 ? Math.round((completedCount / total) * 100) : 0

  // Group by part
  const parts: Record<number, LessonSummary[]> = {}
  for (const l of lessons) {
    const p = l.part || 1
    if (!parts[p]) parts[p] = []
    parts[p].push(l)
  }

  const getStatus = (lessonId: string) => {
    const p = progress[lessonId]
    if (!p) return 'locked'
    if (p.completed) return 'done'
    return 'in-progress'
  }

  const statusStyles: Record<string, { bg: string; border: string; text: string; label: string }> = {
    done: { bg: 'rgba(0,212,170,0.12)', border: '#00d4aa', text: '#00d4aa', label: '✓' },
    'in-progress': { bg: 'rgba(201,162,39,0.1)', border: '#c9a227', text: '#c9a227', label: '↻' },
    locked: { bg: '#0f0e17', border: 'rgba(201,162,39,0.1)', text: '#6b7280', label: '🔒' },
  }

  return (
    <div className="space-y-6">
      {/* Progress header */}
      <div className="flex items-center gap-4 p-4 rounded-xl" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.15)' }}>
        <div className="flex-1">
          <div className="flex justify-between mb-1">
            <span className="text-xs font-bold" style={{ color: '#e8e6f0' }}>Прогресс курса</span>
            <span className="text-xs" style={{ color: '#9b98a8' }}>{completedCount}/{total} уроков</span>
          </div>
          <div className="h-2 rounded-full overflow-hidden" style={{ background: '#0f0e17' }}>
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{ width: `${pct}%`, background: 'linear-gradient(90deg, #00d4aa, #c9a227)' }}
            />
          </div>
        </div>
        <div
          className="text-lg font-bold px-3 py-1 rounded-lg"
          style={{ color: '#00d4aa', background: 'rgba(0,212,170,0.1)' }}
        >
          {pct}%
        </div>
      </div>

      {/* Course parts */}
      {Object.entries(parts).map(([partNum, partLessons]) => (
        <div key={partNum}>
          <h3 className="text-sm font-bold mb-2" style={{ color: '#e8e6f0' }}>
            Часть {partNum}
          </h3>
          <div className="flex flex-wrap gap-2">
            {partLessons.map((lesson) => {
              const st = getStatus(lesson.id)
              const style = statusStyles[st]
              return (
                <Link
                  key={lesson.id}
                  to={`/lesson/${lesson.id}`}
                  className="rounded-lg px-3 py-2 text-xs transition-all hover:scale-105"
                  style={{
                    background: style.bg,
                    border: `1px solid ${style.border}`,
                    color: style.text,
                    textDecoration: 'none',
                    minWidth: '70px',
                    textAlign: 'center',
                  }}
                  title={lesson.title}
                >
                  <div className="font-mono text-[10px] opacity-60">{lesson.id}</div>
                  <div className="font-medium truncate max-w-[90px]">{lesson.title.split(' ')[0]}</div>
                </Link>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}
