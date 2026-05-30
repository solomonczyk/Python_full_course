import { Link, useLocation } from 'react-router-dom'
import type { LessonSummary, Progress } from '../types'

interface Props {
  lessons: LessonSummary[]
  progress: Record<string, Progress>
  open: boolean
  onClose: () => void
}

const PART_ICONS: Record<number, string> = {
  1: '1',
  2: '2',
  3: '3',
  4: '4',
}

const PART_LABELS: Record<number, string> = {
  1: 'Hello Python',
  2: 'Data Magic',
  3: 'The Logic Gate',
  4: 'Loop Labyrinth',
}

export default function Sidebar({ lessons, progress, open, onClose }: Props) {
  const location = useLocation()
  const match = location.pathname.match(/\/(?:lesson|review)\/([\w-]+)/)
  const activeId = match ? match[1] : undefined
  const activeLesson = activeId ? lessons.find(l => l.id === activeId) : null
  const activePart = activeLesson?.part ?? 0

  const parts = Array.from(new Set(lessons.map((l) => l.part))).sort()

  const completedCount = (part: number) =>
    lessons.filter(l => l.part === part && progress[l.id]?.completed).length

  const totalCount = (part: number) =>
    lessons.filter(l => l.part === part).length

  return (
    <>
      {open && (
        <div className="fixed inset-0 bg-black/60 z-40 md:hidden" onClick={onClose} />
      )}

      <aside
        className={`fixed left-0 top-0 h-full w-[220px] bg-steam-sidebar border-r border-steam-bronze-dim flex flex-col z-50
          transition-transform duration-200
          ${open ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
          overflow-y-auto`}
        style={{ borderRightColor: 'rgba(201,162,39,0.15)' }}
      >
        {/* Logo */}
        <div className="px-5 py-5 border-b border-steam-bronze-dim shrink-0" style={{ borderBottomColor: 'rgba(201,162,39,0.15)' }}>
          <Link to="/" onClick={onClose} className="flex items-center gap-2 no-underline">
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-steam-cyan to-cyan-700 flex items-center justify-center text-[11px] font-extrabold text-steam-bg shrink-0">
              Py
            </div>
            <span className="font-display text-sm font-extrabold text-steam-text-accent">Python Quest</span>
          </Link>
        </div>

        {/* Nav */}
        <nav className="flex-1 py-4">
          {parts.map((part) => {
            const done = completedCount(part)
            const total = totalCount(part)
            const isActive = activePart === part
            return (
              <Link
                key={part}
                to={`#part-${part}`}
                onClick={onClose}
                className={`flex items-center gap-2.5 px-5 py-3 text-xs font-semibold transition-all no-underline
                  ${isActive
                    ? 'bg-steam-cyan-dim text-steam-cyan border-l-2 border-steam-cyan'
                    : 'text-steam-text-secondary hover:bg-steam-cyan-dim hover:text-steam-cyan border-l-2 border-transparent'
                  }`}
                style={{
                  backgroundColor: isActive ? 'rgba(0,212,170,0.08)' : 'transparent',
                  borderLeftColor: isActive ? '#00d4aa' : 'transparent',
                }}
              >
                <span className={`w-5.5 h-5.5 rounded-md flex items-center justify-center text-[10px] font-bold shrink-0
                  ${isActive
                    ? 'bg-steam-cyan text-steam-bg-deep'
                    : 'bg-steam-bronze-dim text-steam-bronze'
                  }`}
                  style={{
                    width: '22px', height: '22px',
                    borderRadius: '6px',
                    backgroundColor: isActive ? '#00d4aa' : 'rgba(201,162,39,0.15)',
                    color: isActive ? '#0f0e17' : '#c9a227',
                  }}
                >
                  {PART_ICONS[part] ?? part}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="text-[12px] font-semibold truncate">
                    Part {part}: {PART_LABELS[part] ?? ''}
                  </div>
                  {!isActive && (
                    <div className="text-[10px] text-steam-text-secondary opacity-70 mt-0.5">
                      {done}/{total} artifacts
                    </div>
                  )}
                </div>
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="px-5 py-4 border-t shrink-0" style={{ borderTopColor: 'rgba(201,162,39,0.15)' }}>
          <button
            onClick={() => {
              const firstIncomplete = lessons.find(l => !progress[l.id]?.completed && !l.locked)
              if (firstIncomplete) window.location.href = `/lesson/${firstIncomplete.id}`
            }}
            className="w-full py-3 rounded-lg text-xs font-bold text-steam-bg-deep cursor-pointer border-none"
            style={{
              background: 'linear-gradient(135deg, #c9a227, #8b7355)',
            }}
          >
            ⚡ Continue Learning
          </button>
        </div>
      </aside>
    </>
  )
}
