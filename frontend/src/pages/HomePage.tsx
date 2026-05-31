import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import type { LessonSummary, Progress, ReviewSummary } from '../types'
import CharacterAvatar from '../components/CharacterAvatar'
import CharacterIntroSection from '../components/CharacterIntroSection'
import { useProgressContext } from '../hooks/ProgressContext'

const BASE = '/api'

interface Props {
  lessons: LessonSummary[]
  progress: Record<string, Progress>
}

const PART_IMAGES: Record<number, string> = {
  1: '/parts/rituals.webp',
  2: '/parts/logic.webp',
  3: '/parts/alchemy.webp',
  4: '/parts/mastery.webp',
  5: '/parts/part5.webp',
}

const PART_LABELS: Record<number, { label: string; icon: string }> = {
  1: { label: 'Rituals', icon: '🔮' },
  2: { label: 'Alchemy', icon: '⚗️' },
  3: { label: 'Logic', icon: '⚙️' },
  4: { label: 'Mastery', icon: '🏰' },
}

export default function HomePage({ lessons, progress }: Props) {
  const navigate = useNavigate()
  const { isLessonUnlocked } = useProgressContext()
  const total = lessons.length
  const done = Object.values(progress).filter((p) => p.completed).length
  const [reviews, setReviews] = useState<ReviewSummary[]>([])

  useEffect(() => {
    fetch(`${BASE}/reviews`)
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data)) setReviews(data)
      })
      .catch(() => {})
  }, [])

  const parts = Array.from(new Set(lessons.map((l) => l.part))).sort()

  const completedCount = (part: number) =>
    lessons.filter(l => l.part === part && progress[l.id]?.completed).length

  const totalCount = (part: number) =>
    lessons.filter(l => l.part === part).length

  const completedLessons = lessons
    .filter(l => progress[l.id]?.completed)
    .slice(-3)
    .reverse()

  return (
    <div className="space-y-6">
      {/* 1. Hero Banner */}
      <section
        className="rounded-[20px] overflow-hidden relative"
        style={{
          background: 'linear-gradient(135deg, #1a2a3a 0%, #2a1a3a 50%, #1a1a2e 100%)',
          border: '1px solid rgba(201,162,39,0.3)',
        }}
      >
        <div className="absolute inset-0" style={{
          background: 'radial-gradient(circle at 80% 50%, rgba(0,212,170,0.1) 0%, transparent 50%), radial-gradient(circle at 20% 80%, rgba(201,162,39,0.08) 0%, transparent 40%)',
        }} />
        <div className="relative z-10 p-7">
          <div className="flex gap-6 items-start">
            <div className="flex-1 min-w-0">
              <div className="inline-block px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider mb-3" style={{ background: 'rgba(0,212,170,0.15)', border: '1px solid #00d4aa', color: '#00d4aa' }}>
                SYSTEM STATUS: RESONANT
              </div>
              <h1 className="text-2xl font-extrabold mb-2" style={{ color: '#e8e6f0' }}>Welcome Back, Adept</h1>
              <p className="text-sm leading-relaxed max-w-[500px]" style={{ color: '#9b98a8' }}>
                The Tower hums with a new frequency today. Your mastery of Variable crystals has stabilized the lower wards. Part 3 awaits with its branching paths of logic.
              </p>
              <div className="flex gap-3 mt-4">
                <button onClick={() => { const next = lessons.find(l => !progress[l.id]?.completed && isLessonUnlocked(l.id, lessons)); if (next) navigate(`/lesson/${next.id}`) }}
                  className="px-5 py-2.5 rounded-lg text-xs font-bold cursor-pointer border-none" style={{ background: '#00d4aa', color: '#0f0e17' }}>
                  Continue Quest
                </button>
                <button className="px-5 py-2.5 rounded-lg text-xs font-bold cursor-pointer" style={{ background: 'transparent', border: '1px solid #c9a227', color: '#ffd700' }}>
                  Consult Lexicon
                </button>
              </div>
            </div>
            <div className="w-[200px] shrink-0 rounded-xl p-4 hidden lg:block" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.15)' }}>
              <h4 className="text-[11px] font-bold uppercase tracking-wider mb-3" style={{ color: '#9b98a8' }}>AETHER</h4>
              <div className="flex justify-between items-center py-2" style={{ borderBottom: '1px solid rgba(201,162,39,0.1)' }}>
                <span className="text-[11px]" style={{ color: '#9b98a8' }}>RESONANCE</span>
                <span className="text-xs font-bold" style={{ color: '#e8e6f0' }}>{done} / {total} XP</span>
              </div>
              <div className="h-1.5 rounded-full my-2" style={{ background: 'rgba(0,212,170,0.1)' }}>
                <div className="h-full rounded-full transition-all duration-700" style={{ width: total > 0 ? `${(done / total) * 100}%` : '0%', background: '#00d4aa' }} />
              </div>
              <div className="flex justify-between items-center py-2" style={{ borderBottom: '1px solid rgba(201,162,39,0.1)' }}>
                <span className="text-[11px]" style={{ color: '#9b98a8' }}>RANK</span>
                <span className="text-xs font-bold" style={{ color: '#e8e6f0' }}>
                  {done >= 80 ? 'Arch-Mage' : done >= 50 ? 'Script-Weaver' : done >= 20 ? 'Code-Adept' : 'Novice'}
                </span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-[11px]" style={{ color: '#9b98a8' }}>STREAKS</span>
                <span className="text-xs font-bold" style={{ color: '#e8e6f0' }}>{Math.floor(done / 3)} Days</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Character Introduction — restored */}
      <CharacterIntroSection />

      {/* 3. The Path of the Python */}
      <section>
        <h3 className="text-sm font-bold mb-1" style={{ color: '#e8e6f0' }}>Путь Python</h3>
        <p className="text-xs mb-4" style={{ color: '#9b98a8' }}>Освой четыре царства фундаментального волшебства.</p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {parts.map((part) => {
            const done = completedCount(part)
            const total = totalCount(part)
            const info = PART_LABELS[part] ?? { label: `Part ${part}`, icon: '📚' }
            const allDone = done === total
            const isCurrent = done > 0 && done < total
            const isLocked = done === 0 && part > 1

            return (
              <div key={part}
                className="rounded-xl overflow-hidden transition-all cursor-pointer"
                style={{
                  background: '#1a1924',
                  border: isCurrent ? '1px solid #00d4aa' : '1px solid rgba(201,162,39,0.15)',
                  boxShadow: isCurrent ? '0 0 20px rgba(0,212,170,0.15)' : 'none',
                  opacity: isLocked ? 0.5 : 1,
                }}
                onClick={() => { if (!isLocked) { const first = lessons.find(l => l.part === part && isLessonUnlocked(l.id, lessons)); if (first) navigate(`/lesson/${first.id}`) } }}
              >
                <div className="h-[130px] relative overflow-hidden">
                  <img
                    src={PART_IMAGES[part] ?? ''}
                    alt={`Part ${part}`}
                    className="w-full h-full object-cover"
                  />
                  {isLocked && (
                    <div className="absolute inset-0 flex items-center justify-center text-3xl" style={{ background: 'rgba(15,14,23,0.7)' }}>
                      🔒
                    </div>
                  )}
                </div>
                <div className="p-3">
                  <h4 className="text-xs font-bold mb-1" style={{ color: '#e8e6f0' }}>Part {part}: {info.label}</h4>
                  <p className="text-[10px]" style={{ color: '#9b98a8' }}>
                    {allDone ? `COMPLETED • ${done}/${total} Artifacts` : isCurrent ? `CURRENT • ${done}/${total} Artifacts` : `Locked • Part ${part - 1} Required`}
                  </p>
                  {isCurrent && <div className="mt-2 h-1 rounded-full" style={{ background: 'rgba(0,212,170,0.1)' }}><div className="h-full rounded-full" style={{ width: `${(done / total) * 100}%`, background: '#00d4aa' }} /></div>}
                </div>
              </div>
            )
          })}
        </div>
      </section>

      {/* 4. Quest History */}
      {completedLessons.length > 0 && (
        <section>
          <h3 className="text-sm font-bold mb-3" style={{ color: '#e8e6f0' }}>Quest History</h3>
          <div className="space-y-2">
            {completedLessons.map((lesson) => (
              <div key={lesson.id}
                className="flex items-center gap-3 p-3 rounded-xl cursor-pointer hover:scale-[1.01] transition-all"
                style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.1)' }}
                onClick={() => navigate(`/lesson/${lesson.id}`)}
              >
                <div className="w-9 h-9 rounded-lg flex items-center justify-center text-xs shrink-0" style={{ background: 'rgba(0,212,170,0.1)', color: '#00d4aa' }}>✓</div>
                <div className="flex-1 min-w-0">
                  <h5 className="text-xs font-semibold" style={{ color: '#e8e6f0' }}>Mastered: {lesson.title}</h5>
                  <p className="text-[10px]" style={{ color: '#9b98a8' }}>{lesson.subtitle}</p>
                </div>
                <div className="text-[11px] font-bold shrink-0" style={{ color: '#c9a227' }}>+50 XP</div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 5. Reviews at the bottom */}
      {reviews.length > 0 && (
        <section>
          <h3 className="text-sm font-bold mb-3 uppercase tracking-wider" style={{ color: '#9b98a8' }}>Review Blocks</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {reviews.map((r) => (
              <button key={r.id}
                onClick={() => navigate(`/review/${r.id}`)}
                className="rounded-xl p-4 text-left cursor-pointer transition-all hover:scale-[1.02] active:scale-[0.98]"
                style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.15)' }}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider" style={{ color: '#00d4aa' }}>
                    {r.type === 'quick_recall' ? 'Quick Recall' : r.type === 'chapter_review' ? 'Chapter' : r.type === 'boss_review' ? 'Boss' : 'Part'}
                  </span>
                  <span className="text-[10px]" style={{ color: '#c9a227' }}>· {r.part}.{r.chapter}</span>
                </div>
                <h4 className="text-sm font-bold" style={{ color: '#ffd700' }}>{r.title}</h4>
                <p className="text-xs mt-1" style={{ color: '#9b98a8' }}>{r.subtitle}</p>
              </button>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
