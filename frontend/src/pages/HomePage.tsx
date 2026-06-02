import { useNavigate } from 'react-router-dom'
import type { LessonSummary, Progress } from '../types'
import CharacterIntroSection from '../components/CharacterIntroSection'
import { useProgressContext } from '../hooks/ProgressContext'

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

  const parts = Array.from(new Set(lessons.map((l) => l.part))).sort()

  const completedCount = (part: number) =>
    lessons.filter(l => l.part === part && progress[l.id]?.completed).length

  const totalCount = (part: number) =>
    lessons.filter(l => l.part === part).length

  return (
    <div className="space-y-6">
      {/* 1. Hero Banner — чисте зображення */}
      <section className="rounded-[20px] overflow-hidden relative" style={{ border: '1px solid rgba(201,162,39,0.3)' }}>
        <div className="relative">
          <img
            src="/herro_section/ChatGPT Image May 31, 2026, 04_51_53 PM.webp"
            alt="Python Quest — Башня Алгоритмов"
            className="w-full h-auto object-contain"
            style={{ display: 'block', pointerEvents: 'none' }}
          />

          {/* Progress banner — TOP CENTER */}
          <div className="absolute z-10 hidden sm:block" style={{ top: '10%', left: '50%', transform: 'translateX(-50%)' }}>
            <div
              className="rounded-xl px-5 py-2.5 backdrop-blur-sm inline-flex items-center gap-3"
              style={{
                background: 'rgba(26,25,36,0.7)',
                border: '1px solid rgba(201,162,39,0.2)',
              }}
            >
              <div className="text-[10px] font-bold uppercase tracking-wider" style={{ color: '#9b98a8' }}>
                ПРОГРЕСС
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold" style={{ color: '#e8e6f0' }}>{done} / {total}</span>
                <div className="w-16 h-1.5 rounded-full" style={{ background: 'rgba(0,212,170,0.15)' }}>
                  <div className="h-full rounded-full transition-all duration-500" style={{ width: total > 0 ? `${(done / total) * 100}%` : '0%', background: '#00d4aa' }} />
                </div>
                <span className="text-[10px] font-medium" style={{ color: '#c9a227' }}>
                  {done >= 80 ? 'Архимаг' : done >= 50 ? 'Плетущий код' : done >= 20 ? 'Адепт' : 'Новичок'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Кнопки ПІД хиро-секцією — 3 в одному стилі */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        <button
          onClick={() => { const next = lessons.find(l => !progress[l.id]?.completed && isLessonUnlocked(l.id, lessons)); if (next) navigate(`/lesson/${next.id}`) }}
          className="flex items-center gap-3 px-5 py-3 rounded-xl text-sm font-bold cursor-pointer border-none transition-all hover:scale-[1.02] active:scale-[0.98]"
          style={{ background: 'rgba(15,14,23,0.8)', border: '1px solid #c9a227', color: '#e8e6f0' }}
        >
          <img src="/buttons/prodolgyt_quest.webp" alt="" className="w-8 h-8 object-contain" />
          <span>Продолжить квест</span>
        </button>
        <button
          onClick={() => navigate('/lesson/1-1')}
          className="flex items-center gap-3 px-5 py-3 rounded-xl text-sm font-bold cursor-pointer border-none transition-all hover:scale-[1.02] active:scale-[0.98]"
          style={{ background: 'rgba(15,14,23,0.8)', border: '1px solid #c9a227', color: '#e8e6f0' }}
        >
          <img src="/buttons/nachat_s_nachala.webp" alt="" className="w-8 h-8 object-contain" />
          <span>Начать с начала</span>
        </button>
      </div>

      {/* Mobile: progress під кнопками */}
      <div className="sm:hidden">
        <div className="flex items-center gap-2 text-[10px]" style={{ color: '#9b98a8' }}>
          <span className="font-bold uppercase tracking-wider">ПРОГРЕСС</span>
          <span className="font-bold" style={{ color: '#e8e6f0' }}>{done}/{total}</span>
          <div className="flex-1 h-1 rounded-full" style={{ background: 'rgba(0,212,170,0.15)' }}>
            <div className="h-full rounded-full" style={{ width: total > 0 ? `${(done / total) * 100}%` : '0%', background: '#00d4aa' }} />
          </div>
          <span style={{ color: '#c9a227' }}>
            {done >= 80 ? 'Архимаг' : done >= 50 ? 'Плетущий код' : done >= 20 ? 'Адепт' : 'Новичок'}
          </span>
        </div>
      </div>

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
                onClick={() => { if (!isLocked) navigate(`/part/${part}`) }}
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

      {/* 4. How to continue */}
      <section
        className="rounded-xl p-4"
        style={{
          background: '#1a1924',
          border: '1px solid rgba(201,162,39,0.1)',
        }}
      >
        <div className="flex items-start gap-3">
          <span className="material-symbols-outlined text-lg" style={{ color: '#c9a227' }}>
            info
          </span>
          <div>
            <h4 className="text-xs font-bold mb-1" style={{ color: '#e8e6f0' }}>
              Как продолжить обучение
            </h4>
            <p className="text-[11px] leading-relaxed" style={{ color: '#9b98a8' }}>
              Выбери часть курса на карте выше, чтобы увидеть все уроки и повторения.
              Повторения и чекпоинты открываются после прохождения соответствующих
              уроков — они встроены в учебный маршрут каждой части.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}
