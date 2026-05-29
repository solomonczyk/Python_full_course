import { Link, useNavigate } from 'react-router-dom'
import type { LessonSummary } from '../types'
import { USER_AVATAR } from '../constants'

interface Props {
  lessons: LessonSummary[]
  currentId?: string
  onMenuClick: () => void
}

export default function TopNav({ lessons, currentId, onMenuClick }: Props) {
  const navigate = useNavigate()

  const idx = lessons.findIndex((l) => l.id === currentId)
  const prev = idx > 0 ? lessons[idx - 1] : null
  const next = idx >= 0 && idx < lessons.length - 1 ? lessons[idx + 1] : null

  return (
    <header className="bg-surface-container-lowest shadow-sm flex justify-between items-center w-full px-6 h-16 z-40 fixed top-0">
      <div className="flex items-center gap-3">
        <button onClick={onMenuClick} className="md:hidden mr-2 text-on-surface-variant">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>menu</span>
        </button>
        <Link to="/" className="flex items-center gap-3">
          <span className="material-symbols-outlined text-primary text-3xl" style={{ fontVariationSettings: "'FILL' 0" }}>terminal</span>
          <h1 className="font-display text-[24px] leading-8 font-bold text-primary hover:underline underline-offset-4">Python Quest</h1>
        </Link>
      </div>

      <div className="flex items-center gap-3">
        {prev && (
          <button
            onClick={() => navigate(`/lesson/${prev.id}`)}
            className="font-display text-[20px] leading-7 font-semibold text-on-surface-variant hover:bg-surface-container px-4 py-2 rounded-lg active:scale-95 transition-all"
          >
            ← Назад
          </button>
        )}
        {next && !next.locked && (
          <button
            onClick={() => navigate(`/lesson/${next.id}`)}
            className="bg-primary text-on-primary font-display text-[20px] leading-7 font-semibold px-6 py-2 rounded-lg shadow-sm hover:opacity-90 active:scale-95 transition-all"
          >
            Далее →
          </button>
        )}
        <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-primary-container shrink-0">
          <img src={USER_AVATAR} alt="User" className="w-full h-full object-cover" />
        </div>
      </div>
    </header>
  )
}
