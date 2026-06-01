import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import type { LessonSummary } from '../types'
import { usePageMeta, canonicalUrl, PUBLIC_ROUTES } from '../hooks/usePageMeta'

const BASE = '/api'

const PART_LABELS: Record<number, { label: string; icon: string; color: string }> = {
  1: { label: 'Rituals', icon: '🔮', color: '#00d4aa' },
  2: { label: 'Logic', icon: '⚙️', color: '#c9a227' },
  3: { label: 'Alchemy', icon: '⚗️', color: '#A29BFE' },
  4: { label: 'Mastery', icon: '🏰', color: '#FF7675' },
  5: { label: 'Constructs', icon: '🧱', color: '#74B9FF' },
}

const DIFFICULTY_STARS: Record<string, string> = {
  easy: '★☆☆',
  medium: '★★☆',
  hard: '★★★',
  boss: '★★★',
}

export default function CourseCatalogPage() {
  const navigate = useNavigate()
  const [lessons, setLessons] = useState<LessonSummary[]>([])
  const [loading, setLoading] = useState(true)

  // ── SEO metadata ────────────────────────────────────────────────────
  useEffect(() => {
    usePageMeta({
      ...PUBLIC_ROUTES['/course'],
      canonical: canonicalUrl('/course'),
    })
    return () => { /* restore happens on next route change */ }
  }, [])

  // ── Load lessons ────────────────────────────────────────────────────
  useEffect(() => {
    fetch(`${BASE}/lessons`)
      .then(r => r.json())
      .then((data: LessonSummary[]) => {
        if (Array.isArray(data)) setLessons(data)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const parts = Array.from(new Set(lessons.map(l => l.part))).sort()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-4" style={{ color: '#9b98a8' }}>
          <span className="material-symbols-outlined text-5xl animate-spin" style={{ fontVariationSettings: "'FILL' 0" }}>progress_activity</span>
          <p className="text-sm">Загрузка курса...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-[1000px] mx-auto px-4 py-8 space-y-12">
      {/* Page header */}
      <header>
        <h1 className="text-2xl font-extrabold" style={{ color: '#e8e6f0' }}>
          Каталог уроков Python Quest
        </h1>
        <p className="text-sm mt-2" style={{ color: '#9b98a8' }}>
          {lessons.length} уроков в 5 частях. От первой команды <code className="px-1 rounded" style={{ background: 'rgba(0,212,170,0.1)', color: '#00d4aa' }}>print()</code> до финального проекта.
        </p>
      </header>

      {/* Parts index for quick nav */}
      <nav aria-label="Навигация по частям" className="flex flex-wrap gap-2">
        {parts.map(p => {
          const info = PART_LABELS[p] ?? { label: `Part ${p}`, icon: '📚', color: '#9b98a8' }
          return (
            <a
              key={p}
              href={`#part-${p}`}
              className="px-3 py-1.5 rounded-lg text-xs font-bold transition-all hover:scale-105"
              style={{
                background: '#1a1924',
                border: `1px solid ${info.color}44`,
                color: info.color,
                textDecoration: 'none',
              }}
            >
              {info.icon} Часть {p}: {info.label}
            </a>
          )
        })}
      </nav>

      {/* Parts */}
      {parts.map(part => {
        const info = PART_LABELS[part] ?? { label: `Part ${part}`, icon: '📚', color: '#9b98a8' }
        const partLessons = lessons.filter(l => l.part === part)

        return (
          <section key={part} id={`part-${part}`}>
            <h2 className="text-lg font-bold mb-1 flex items-center gap-2" style={{ color: info.color }}>
              <span>{info.icon}</span>
              <span>Часть {part}: {info.label}</span>
            </h2>
            <p className="text-xs mb-4" style={{ color: '#9b98a8' }}>
              {partLessons.length} уроков
            </p>

            <nav aria-label={`Уроки части ${part}`}>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {partLessons.map(lesson => (
                  <article
                    key={lesson.id}
                    className="rounded-xl overflow-hidden transition-all hover:scale-[1.02] hover:shadow-lg"
                    style={{
                      background: '#1a1924',
                      border: '1px solid rgba(201,162,39,0.15)',
                    }}
                  >
                    <Link
                      to={`/lesson/${lesson.id}/preview`}
                      className="block p-4 no-underline"
                      style={{ color: 'inherit' }}
                    >
                      {/* Header: ID + difficulty */}
                      <div className="flex items-center justify-between mb-2">
                        <span
                          className="text-[10px] font-bold px-2 py-0.5 rounded-full"
                          style={{
                            background: `${info.color}22`,
                            color: info.color,
                            border: `1px solid ${info.color}44`,
                          }}
                        >
                          Урок {lesson.id}
                        </span>
                        <span className="text-[10px]" style={{ color: '#9b98a8' }}>
                          {DIFFICULTY_STARS[lesson.difficulty] ?? '★★★'}
                        </span>
                      </div>

                      {/* Title */}
                      <h3 className="text-sm font-bold mb-1 line-clamp-2" style={{ color: '#e8e6f0' }}>
                        {lesson.title}
                      </h3>

                      {/* Subtitle / topic */}
                      <p className="text-[11px] mb-2" style={{ color: '#9b98a8' }}>
                        {lesson.subtitle}
                      </p>

                      {/* Topic chip */}
                      <div className="flex items-center gap-2">
                        <span
                          className="text-[10px] px-2 py-0.5 rounded-full"
                          style={{
                            background: 'rgba(201,162,39,0.1)',
                            color: '#c9a227',
                          }}
                        >
                          {lesson.topic}
                        </span>
                      </div>
                    </Link>

                    {/* CTA */}
                    <div className="px-4 pb-4">
                      <Link
                        to={`/lesson/${lesson.id}/preview`}
                        className="block w-full text-center py-2 rounded-lg text-xs font-bold transition-all hover:scale-[1.02]"
                        style={{
                          background: 'linear-gradient(135deg, #c9a227, #8b7355)',
                          color: '#0f0e17',
                          textDecoration: 'none',
                        }}
                      >
                        Открыть preview
                      </Link>
                    </div>
                  </article>
                ))}
              </div>
            </nav>
          </section>
        )
      })}

      {/* Footer */}
      <footer className="text-center py-8 border-t" style={{ borderColor: 'rgba(201,162,39,0.1)' }}>
        <p className="text-xs" style={{ color: '#9b98a8' }}>
          Python Quest — игровой курс Python для новичков.
        </p>
      </footer>
    </div>
  )
}
