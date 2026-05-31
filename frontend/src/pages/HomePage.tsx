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
  5: { label: 'Constructs', icon: '🧱' },
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
      {/* 1. Hero Banner — чистое изображение + DOM overlays */}
      <section className="rounded-[20px] overflow-hidden relative" style={{ border: '1px solid rgba(201,162,39,0.3)' }}>
        <div className="relative">
          {/* Фоновое изображение — без встроенных кнопок */}
          <img
            src="/herro_section/ChatGPT Image May 31, 2026, 04_51_53 PM.webp"
            alt="Python Quest — Башня Алгоритмов"
            className="w-full h-auto object-contain"
            style={{ display: 'block', pointerEvents: 'none' }}
          />

          {/* Кнопки — нижняя левая зона, поверх изображения */}
          <div
            className="absolute flex gap-3 sm:gap-4 z-10"
            style={{ bottom: '12%', left: '8%' }}
          >
            <button
              onClick={() => { const next = lessons.find(l => !progress[l.id]?.completed && isLessonUnlocked(l.id, lessons)); if (next) navigate(`/lesson/${next.id}`) }}
              className="px-5 sm:px-8 py-2 sm:py-3 rounded-lg text-xs sm:text-sm font-bold cursor-pointer border-none transition-all hover:scale-105 hover:brightness-110 focus:outline-2 focus:outline-[#00d4aa] active:scale-95"
              style={{ background: '#00d4aa', color: '#0f0e17' }}
            >
              🎮 Продолжить квест
            </button>
            <button
              onClick={() => navigate('/lesson/1-1')}
              className="px-4 sm:px-6 py-2 sm:py-3 rounded-lg text-xs sm:text-sm font-bold cursor-pointer border-none transition-all hover:scale-105 hover:brightness-110 focus:outline-2 focus:outline-[#c9a227] active:scale-95"
              style={{ background: 'rgba(15,14,23,0.75)', border: '1px solid #c9a227', color: '#ffd700' }}
            >
              📜 Начать с начала
            </button>
          </div>

          {/* Progress banner — glass panel, нижняя правая зона */}
          <div
            className="absolute z-10 hidden sm:block"
            style={{ bottom: '13%', right: '5%' }}
          >
            <div
              className="rounded-xl px-4 py-3 backdrop-blur-sm"
              style={{
                background: 'rgba(26,25,36,0.7)',
                border: '1px solid rgba(201,162,39,0.2)',
              }}
            >
              <div className="text-[10px] font-bold mb-2 uppercase tracking-wider" style={{ color: '#9b98a8' }}>
                ПРОГРЕСС
              </div>
              <div className="flex items-center gap-3">
                <div>
                  <div className="text-xs font-bold" style={{ color: '#e8e6f0' }}>
                    {done} <span style={{ color: '#6b7280' }}>/</span> {total}
                  </div>
                </div>
                <div className="w-16 h-1.5 rounded-full" style={{ background: 'rgba(0,212,170,0.15)' }}>
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{ width: total > 0 ? `${(done / total) * 100}%` : '0%', background: '#00d4aa' }}
                  />
                </div>
                <div className="text-[10px] font-medium" style={{ color: '#c9a227' }}>
                  {done >= 80 ? 'Архимаг' : done >= 50 ? 'Плетущий код' : done >= 20 ? 'Адепт' : 'Новичок'}
                </div>
              </div>
            </div>
          </div>

          {/* Mobile: progress под изображением */}
          <div className="sm:hidden px-4 py-3" style={{ background: 'rgba(26,25,36,0.9)' }}>
            <div className="flex items-center justify-between">
              <div className="text-[10px] font-bold uppercase tracking-wider" style={{ color: '#9b98a8' }}>
                ПРОГРЕСС
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold" style={{ color: '#e8e6f0' }}>{done}/{total}</span>
                <div className="w-12 h-1.5 rounded-full" style={{ background: 'rgba(0,212,170,0.15)' }}>
                  <div className="h-full rounded-full" style={{ width: total > 0 ? `${(done / total) * 100}%` : '0%', background: '#00d4aa' }} />
                </div>
                <span className="text-[10px]" style={{ color: '#c9a227' }}>
                  {done >= 80 ? 'Архимаг' : done >= 50 ? 'Плетущий код' : done >= 20 ? 'Адепт' : 'Новичок'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Character Introduction */}
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
