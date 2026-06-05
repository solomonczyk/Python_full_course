import { useLocation, useNavigate } from 'react-router-dom'
import type { LessonSummary, Progress } from '../types'
import { USER_AVATAR } from '../constants'

interface Props {
  lessons: LessonSummary[]
  currentId?: string
  progress: Record<string, Progress>
  onMenuClick: () => void
}

export default function TopNav({ lessons, progress, onMenuClick }: Props) {
  const location = useLocation()
  const navigate = useNavigate()

  const completedCount = lessons.filter(l => progress[l.id]?.completed).length
  const totalCount = lessons.length
  const pct = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0

  const currentPath = location.pathname
  const isActive = (path: string) => {
    if (path === '/') return currentPath === '/' || currentPath.startsWith('/lesson') || currentPath.startsWith('/review')
    return currentPath.startsWith(path)
  }

  return (
    <header
      className="h-14 flex items-center justify-between px-6 shrink-0 z-30"
      style={{
        background: '#1a1924',
        borderBottom: '1px solid rgba(201,162,39,0.15)',
      }}
    >
      {/* Left: Hamburger + Nav tabs */}
      <div className="flex items-center gap-6">
        <button
          onClick={onMenuClick}
          className="md:hidden text-steam-text-secondary hover:text-steam-text transition-colors"
          aria-label="Toggle sidebar"
        >
          <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: "'FILL' 0" }}>menu</span>
        </button>
        <nav className="flex items-center gap-6">
          {[
            { label: 'Curriculum', path: '/' },
          ].map((tab) => (
            <button
              key={tab.label}
              onClick={() => navigate(tab.path)}
              className="text-xs font-semibold transition-all pb-1 bg-transparent border-none cursor-pointer"
              style={{
                color: isActive(tab.path) ? '#00d4aa' : '#9b98a8',
                borderBottom: isActive(tab.path) ? '2px solid #00d4aa' : '2px solid transparent',
              }}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        {/* Progress bar — hidden on small screens */}
        <div className="items-center gap-2 hidden sm:flex">
          <div
            className="w-24 h-1.5 rounded-full overflow-hidden"
            style={{ background: 'rgba(155,152,168,0.2)' }}
          >
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{
                width: `${pct}%`,
                background: 'linear-gradient(90deg, #00d4aa, #c9a227)',
              }}
            />
          </div>
          <span className="text-[10px] font-semibold" style={{ color: '#9b98a8' }}>
            {completedCount}/{totalCount}
          </span>
        </div>
      </div>

      {/* Right: Search + Avatar */}
      <div className="flex items-center gap-3">
        <div
          className="rounded-full px-3 py-1.5 text-xs text-steam-text-secondary hidden sm:block"
          style={{
            background: '#0f0e17',
            border: '1px solid rgba(201,162,39,0.2)',
          }}
        >
          <span className="material-symbols-outlined text-[14px] align-middle mr-1" style={{ fontVariationSettings: "'FILL' 0" }}>search</span>
          Search the Archives...
        </div>
        <div
          className="w-8 h-8 rounded-full overflow-hidden flex items-center justify-center text-[10px] font-bold shrink-0"
          style={{
            background: 'linear-gradient(135deg, #c9a227, #8b7355)',
            border: '2px solid #c9a227',
            color: '#1a1a2e',
          }}
        >
          A
        </div>
      </div>
    </header>
  )
}
