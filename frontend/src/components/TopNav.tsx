import { useLocation, useNavigate } from 'react-router-dom'
import type { LessonSummary } from '../types'
import { USER_AVATAR } from '../constants'

interface Props {
  lessons: LessonSummary[]
  currentId?: string
  onMenuClick: () => void
}

export default function TopNav({ onMenuClick }: Props) {
  const location = useLocation()
  const navigate = useNavigate()

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
            { label: 'Leaderboard', path: '/leaderboard' },
            { label: 'Sandbox', path: '/sandbox' },
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
