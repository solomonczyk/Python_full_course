import { Link, useParams } from 'react-router-dom'
import type { LessonSummary, Progress } from '../types'

interface Props {
  lessons: LessonSummary[]
  progress: Record<string, Progress>
  open: boolean
  onClose: () => void
}

export default function Sidebar({ lessons, progress, open, onClose }: Props) {
  const { id } = useParams()

  const parts = Array.from(new Set(lessons.map((l) => l.part))).sort()

  return (
    <>
      {/* Overlay (mobile) */}
      {open && (
        <div
          className="fixed inset-0 bg-black/30 z-40 md:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed left-0 top-16 h-[calc(100vh-64px)] w-[280px] bg-surface-container-low shadow-sm flex flex-col py-6 px-4 z-50 overflow-y-auto
          transition-transform duration-200
          ${open ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}
      >
        <div className="mb-8 px-2">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-full bg-mentor-ksyu flex items-center justify-center text-xl">🤖</div>
            <div>
              <h2 className="font-sans text-[13px] font-bold text-on-surface">Ксю — наставник</h2>
              <p className="text-[11px] text-on-surface-variant">Python Quest</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 space-y-4">
          {parts.map((part) => {
            const partLessons = lessons.filter((l) => l.part === part)
            return (
              <div key={part}>
                <p className="px-3 mb-1 font-sans text-[11px] font-bold text-on-surface-variant tracking-widest uppercase">
                  Часть {part}
                </p>
                <div className="space-y-1">
                  {partLessons.map((lesson) => {
                    const isActive = lesson.id === id
                    const isDone = progress[lesson.id]?.completed
                    return (
                      <Link
                        key={lesson.id}
                        to={lesson.locked ? '#' : `/lesson/${lesson.id}`}
                        onClick={onClose}
                        className={`flex items-center gap-3 px-3 py-2.5 rounded-lg font-sans text-[13px] font-bold transition-all
                          ${lesson.locked ? 'opacity-50 cursor-not-allowed' : ''}
                          ${isActive
                            ? 'bg-secondary-container text-on-secondary-container'
                            : 'text-on-surface-variant hover:bg-surface-container-high'
                          }`}
                      >
                        <span className="material-symbols-outlined text-[18px] shrink-0" style={{ fontVariationSettings: `'FILL' ${isDone ? '1' : '0'}` }}>
                          {lesson.locked ? 'lock' : isDone ? 'check_circle' : 'radio_button_unchecked'}
                        </span>
                        <span className={isDone ? 'text-action-da' : ''}>{lesson.id} {lesson.title}</span>
                      </Link>
                    )
                  })}
                </div>
              </div>
            )
          })}
        </nav>

        <div className="mt-auto pt-6 border-t border-outline-variant space-y-1">
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-container-high rounded-lg font-sans text-[13px] font-bold">
            <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 0" }}>settings</span>
            Настройки
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-container-high rounded-lg font-sans text-[13px] font-bold">
            <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 0" }}>help</span>
            Помощь
          </a>
        </div>
      </aside>
    </>
  )
}
