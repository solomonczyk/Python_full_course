import { useState, useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import type { LessonSummary, Progress } from '../types'
import { CHARACTER_AVATARS } from '../constants'
import { useProgressContext } from '../hooks/ProgressContext'

interface Props {
  lessons: LessonSummary[]
  progress: Record<string, Progress>
  open: boolean
  onClose: () => void
}

const PART_LABELS: Record<number, string> = {
  1: 'Hello Python',
  2: 'Data Magic',
  3: 'The Logic Gate',
  4: 'Loop Labyrinth',
}

export default function Sidebar({ lessons, progress, open, onClose }: Props) {
  const location = useLocation()
  const navigate = useNavigate()
  const { isLessonUnlocked } = useProgressContext()
  const match = location.pathname.match(/\/(?:lesson|review)\/([\w-]+)/)
  const activeId = match ? match[1] : undefined
  const activeLesson = activeId ? lessons.find(l => l.id === activeId) : null
  const activePart = activeLesson?.part ?? 0

  const parts = Array.from(new Set(lessons.map((l) => l.part))).sort()

  const [expandedPart, setExpandedPart] = useState<number | null>(activePart)

  // Auto-expand active part when navigating
  useEffect(() => {
    if (activePart) setExpandedPart(activePart)
  }, [activePart])

  const completedCount = (part: number) =>
    lessons.filter(l => l.part === part && progress[l.id]?.completed).length

  const totalCount = (part: number) =>
    lessons.filter(l => l.part === part).length

  const togglePart = (part: number) => {
    setExpandedPart(expandedPart === part ? null : part)
  }

  const navToLesson = (lessonId: string) => {
    onClose()
    navigate(`/lesson/${lessonId}`)
  }

  const goToContinue = () => {
    const firstIncomplete = lessons.find(l => !progress[l.id]?.completed && isLessonUnlocked(l.id, lessons))
    if (firstIncomplete) {
      onClose()
      navigate(`/lesson/${firstIncomplete.id}`)
    }
  }

  return (
    <>
      {open && (
        <div className="fixed inset-0 bg-black/60 z-40 md:hidden" onClick={onClose} />
      )}

      <aside
        className={`fixed left-0 top-0 h-full w-[240px] flex flex-col z-50
          transition-transform duration-200
          ${open ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
          overflow-y-auto`}
        style={{
          background: '#16151f',
          borderRight: '1px solid rgba(201,162,39,0.15)',
        }}
      >
        {/* Logo */}
        <div className="px-5 py-5 shrink-0" style={{ borderBottom: '1px solid rgba(201,162,39,0.15)' }}>
          <Link to="/" onClick={onClose} className="flex items-center gap-2 no-underline">
            <img src="/logo/logo.webp" alt="Python Quest" className="w-full max-w-[180px] h-auto object-contain" />
          </Link>
        </div>

        {/* Nav with collapsible parts */}
        <nav className="flex-1 py-3 overflow-y-auto">
          {parts.map((part) => {
            const done = completedCount(part)
            const total = totalCount(part)
            const isActive = activePart === part
            const isExpanded = expandedPart === part
            const partLessons = lessons.filter(l => l.part === part)

            return (
             <div key={part}>
                {/* Part header — clickable to toggle */}
                <button
                  onClick={() => togglePart(part)}
                  className="w-full flex items-center gap-2.5 px-4 py-2.5 text-xs font-semibold transition-all cursor-pointer border-none text-left"
                  style={{
                    background: done === total ? 'rgba(0,212,170,0.08)' : 'transparent',
                    borderLeft: `2px solid ${done === total ? '#00d4aa' : 'transparent'}`,
                    color: done === total ? '#00d4aa' : '#9b98a8',
                  }}
                >
                  <span
                    className="flex items-center justify-center text-[10px] font-bold shrink-0"
                    style={{
                      width: '22px', height: '22px',
                      borderRadius: '6px',
                      background: done === total ? '#00d4aa' : 'rgba(201,162,39,0.15)',
                      color: done === total ? '#0f0e17' : '#c9a227',
                    }}
                  >
                    {done === total ? '✓' : part}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="text-[12px] font-semibold truncate" style={{ color: done === total ? '#00d4aa' : '#e8e6f0' }}>
                      {done === total ? '✓ ' : ''}Part {part}: {PART_LABELS[part] ?? ''}
                    </div>
                    <div className="text-[10px] opacity-70 mt-0.5" style={{ color: '#9b98a8' }}>
                      {done === total ? 'COMPLETED' : `${done}/${total} artifacts`}
                      {isExpanded ? ' ▾' : ' ▸'}
                    </div>
                  </div>
                </button>

                {/* Lessons list (collapsible) */}
                {isExpanded && (
                  <div className="ml-3 pl-3" style={{ borderLeft: '1px solid rgba(201,162,39,0.15)' }}>
                    {partLessons.map((lesson) => {
                      const isLessonActive = lesson.id === activeId
                      const isDone = progress[lesson.id]?.completed
                      const isLocked = lesson.locked && !progress[lesson.id]?.completed

                      return (
                        <button
                          key={lesson.id}
                          onClick={() => !isLocked && navToLesson(lesson.id)}
                          disabled={isLocked}
                          className="w-full flex items-center gap-2 px-3 py-1.5 text-[11px] font-medium transition-all cursor-pointer text-left border-none rounded-sm"
                          style={{
                            color: isLessonActive ? '#00d4aa' : isDone ? '#9b98a8' : isLocked ? 'rgba(155,152,168,0.4)' : '#e8e6f0',
                            background: isLessonActive ? 'rgba(0,212,170,0.1)' : 'transparent',
                          }}
                        >
                          <span className="material-symbols-outlined text-[14px]" style={{ fontVariationSettings: `'FILL' ${isDone ? '1' : '0'}` }}>
                            {isLocked ? 'lock' : isDone ? 'check_circle' : 'radio_button_unchecked'}
                          </span>
                          <span className="truncate">{lesson.id} {lesson.title}</span>
                        </button>
                      )
                    })}
                  </div>
                )}
              </div>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="px-4 py-4 shrink-0" style={{ borderTop: '1px solid rgba(201,162,39,0.15)' }}>
          <button
            onClick={goToContinue}
            className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:opacity-90"
            style={{
              background: 'rgba(15,14,23,0.8)',
              border: '1px solid #c9a227',
              color: '#e8e6f0',
            }}
          >
            <img src="/buttons/continue_learning.webp" alt="" className="w-6 h-6 object-contain" />
            Continue Learning
          </button>
        </div>
      </aside>
    </>
  )
}
