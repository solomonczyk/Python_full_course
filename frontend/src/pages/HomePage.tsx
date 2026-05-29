import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import type { LessonSummary, Progress, ReviewSummary } from '../types'
import CharacterAvatar from '../components/CharacterAvatar'
import CharacterIntroSection from '../components/CharacterIntroSection'

const BASE = '/api'

interface Props {
  lessons: LessonSummary[]
  progress: Record<string, Progress>
}

const PART_LABELS: Record<number, string> = {
  1: 'Вход в Python',
  2: 'Условия и циклы',
  3: 'Уверенная база Python',
  4: 'Башня алгоритмов',
}

export default function HomePage({ lessons, progress }: Props) {
  const navigate = useNavigate()
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

  return (
    <div className="w-full max-w-[800px]">
      {/* Reviews section */}
      {reviews.length > 0 && (
        <section className="mb-10">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center text-purple-600">
              <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>repeat</span>
            </div>
            <h2 className="font-display text-[24px] leading-8 font-bold text-on-surface">Повторение</h2>
            <span className="bg-purple-100 text-purple-600 text-[12px] font-bold px-2 py-0.5 rounded-full">{reviews.length}</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {reviews.map((r) => (
              <button
                key={r.id}
                onClick={() => navigate(`/review/${r.id}`)}
                className="text-left p-5 rounded-2xl border-2 border-purple-200 bg-purple-50/50 hover:shadow-md hover:border-purple-400 transition-all active:scale-[0.99]"
              >
                <div className="flex items-center gap-2 text-purple-600 mb-2 font-sans text-[13px] font-bold">
                  <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>repeat</span>
                  <span>{r.type === 'quick_recall' ? 'Быстрое' : r.type === 'chapter_review' ? 'Глава' : r.type === 'boss_review' ? 'Мини-игра' : 'Часть'}</span>
                  <span className="mx-1">·</span>
                  <span className="text-on-surface-variant">{r.part}.{r.chapter}</span>
                </div>
                <h3 className="font-display text-[20px] leading-7 font-semibold text-on-surface">{r.title}</h3>
                <p className="font-sans text-[15px] text-on-surface-variant mt-1">{r.subtitle}</p>
              </button>
            ))}
          </div>
        </section>
      )}

      {/* Hero */}
      <section className="mb-12">
        <div className="flex items-center gap-4 mb-6">
          <CharacterAvatar character="ksyu" size="lg" />
          <div>
            <div className="flex items-center gap-2 text-secondary mb-1 font-sans text-[13px] font-bold">
              <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>auto_awesome</span>
              <span>ИНТЕРАКТИВНЫЙ КУРС</span>
            </div>
            <h1 className="font-display font-extrabold text-[36px] leading-[44px] tracking-tight text-on-surface">
              Python Quest
            </h1>
          </div>
        </div>
        <p className="font-sans text-[16px] leading-6 text-on-surface-variant max-w-[600px]">
          Начни путь в Python как <strong>Новичок</strong>: сначала ты разберёшься с первыми командами, ошибками и условиями, а затем шаг за шагом соберёшь свою первую консольную игру — <strong>«Побег из Башни Багуса»</strong>.
        </p>
        <p className="font-sans text-[14px] leading-5 text-on-surface-variant mt-3 max-w-[600px]">
          Ксю, Ва и Да будут объяснять, поддерживать и тренировать тебя, а Багус — ломать код, прятать ошибки и проверять, действительно ли ты понял тему.
        </p>

        {/* Progress bar */}
        <div className="mt-6 bg-surface-container-high rounded-full h-3 overflow-hidden">
          <div
            className="bg-action-da h-full rounded-full transition-all duration-700"
            style={{ width: total > 0 ? `${(done / total) * 100}%` : '0%' }}
          />
        </div>
        <p className="mt-2 text-[13px] text-on-surface-variant font-sans">
          {done} / {total} уроков завершено
        </p>
      </section>

      {/* Character intro */}
      <CharacterIntroSection />

      {/* Lessons by part */}
      {parts.map((part) => {
        const partLessons = lessons.filter((l) => l.part === part)
        return (
          <section key={part} className="mb-10">
            <h2 className="font-display text-[24px] leading-8 font-bold text-on-surface mb-4">
              Часть {part}: {PART_LABELS[part] ?? ''}
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {partLessons.map((lesson) => {
                const isDone = progress[lesson.id]?.completed
                return (
                  <button
                    key={lesson.id}
                    onClick={() => !lesson.locked && navigate(`/lesson/${lesson.id}`)}
                    disabled={lesson.locked}
                    className={`text-left p-5 rounded-2xl border-2 transition-all group
                      ${lesson.locked
                        ? 'opacity-50 cursor-not-allowed border-outline-variant bg-surface-container-low'
                        : isDone
                          ? 'border-action-da bg-green-50 hover:shadow-md'
                          : 'border-outline-variant bg-white hover:border-secondary hover:shadow-md active:scale-[0.99]'
                      }`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <span className={`font-sans text-[13px] font-bold ${isDone ? 'text-action-da' : 'text-on-surface-variant'}`}>
                        УРОК {lesson.id}
                      </span>
                      <span
                        className={`material-symbols-outlined text-[20px]
                          ${lesson.locked ? 'text-outline' :
                            isDone ? 'text-action-da' : 'text-outline group-hover:text-secondary'}`}
                        style={{ fontVariationSettings: `'FILL' ${isDone ? '1' : '0'}` }}
                      >
                        {lesson.locked ? 'lock' : isDone ? 'check_circle' : 'radio_button_unchecked'}
                      </span>
                    </div>
                    <h3 className="font-display text-[20px] leading-7 font-semibold text-on-surface mb-1">
                      {lesson.title}
                    </h3>
                    <p className="font-sans text-[15px] leading-[22px] text-on-surface-variant">
                      {lesson.subtitle}
                    </p>
                    <div className="mt-3 inline-block bg-surface-container px-2 py-0.5 rounded-full font-mono text-[12px] text-on-surface-variant">
                      {lesson.topic}
                    </div>
                  </button>
                )
              })}
            </div>
          </section>
        )
      })}
    </div>
  )
}
