import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import type { Lesson } from '../types'
import { usePageMeta, canonicalUrl } from '../hooks/usePageMeta'
import CodeBlock from '../components/CodeBlock'

const BASE = '/api'

const PART_LABELS: Record<number, string> = {
  1: 'Rituals', 2: 'Alchemy', 3: 'Logic', 4: 'Mastery', 5: 'Constructs',
}

const DIFFICULTY_LABELS: Record<string, string> = {
  easy: '🔰 Начальный',
  medium: '⚙️ Средний',
  hard: '🔥 Сложный',
  boss: '👹 Босс',
}

export default function LessonPreviewPage() {
  const { id } = useParams<{ id: string }>()
  const [lesson, setLesson] = useState<Lesson | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // ── Fetch lesson detail ─────────────────────────────────────────────
  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetch(`${BASE}/lessons/${id}`)
      .then(r => {
        if (!r.ok) throw new Error('Урок не найден')
        return r.json()
      })
      .then((data: Lesson) => setLesson(data))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  // ── SEO metadata (dynamic per lesson) ──────────────────────────────
  useEffect(() => {
    if (lesson) {
      const metaTitle = `${lesson.title}: ${lesson.subtitle}`
      usePageMeta({
        title: metaTitle,
        description: `${lesson.topic}: ${lesson.story_placement ?? lesson.mini_summary ?? 'Изучай Python в формате квеста.'}`,
        ogTitle: metaTitle,
        ogDescription: lesson.mini_summary ?? lesson.story_placement ?? 'Изучай Python в формате квеста.',
        ogType: 'article',
        canonical: canonicalUrl(`/lesson/${id}/preview`),
      })
    } else {
      usePageMeta({
        title: 'Загрузка урока...',
        canonical: canonicalUrl(`/lesson/${id}/preview`),
      })
    }
    return () => { /* restore handled by next route */ }
  }, [lesson, id])

  // ── Loading state ──────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-4" style={{ color: '#9b98a8' }}>
          <span className="material-symbols-outlined text-5xl animate-spin" style={{ fontVariationSettings: "'FILL' 0" }}>progress_activity</span>
          <p className="text-sm">Загрузка урока...</p>
        </div>
      </div>
    )
  }

  // ── Error state ────────────────────────────────────────────────────
  if (error || !lesson) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-4">
          <span className="material-symbols-outlined text-5xl block" style={{ color: '#ff6b6b', fontVariationSettings: "'FILL' 0" }}>error</span>
          <p style={{ color: '#ff6b6b' }}>{error ?? 'Урок не найден'}</p>
          <Link
            to="/course"
            className="inline-block px-6 py-2.5 rounded-lg text-xs font-bold"
            style={{
              background: 'linear-gradient(135deg, #c9a227, #8b7355)',
              color: '#0f0e17',
              textDecoration: 'none',
            }}
          >
            ← К каталогу уроков
          </Link>
        </div>
      </div>
    )
  }

  const partLabel = PART_LABELS[lesson.part] ?? `Part ${lesson.part}`
  const diffLabel = DIFFICULTY_LABELS[lesson.difficulty] ?? lesson.difficulty

  // Safe usage — guard against missing fields
  const safeOutput = lesson.explanation?.output ?? ''
  const safeCodeExample = lesson.explanation?.code_example ?? ''
  const safeExplanationText = lesson.explanation?.text ?? ''

  return (
    <div className="max-w-[800px] mx-auto px-4 py-8 space-y-8">
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb">
        <Link
          to="/course"
          className="text-xs font-medium transition-all hover:opacity-80"
          style={{ color: '#c9a227', textDecoration: 'none' }}
        >
          ← Каталог уроков
        </Link>
      </nav>

      {/* Hero section */}
      <header>
        <div className="flex items-center gap-2 mb-3">
          <span
            className="px-2.5 py-0.5 rounded-full text-[10px] font-bold"
            style={{
              background: 'rgba(0,212,170,0.15)',
              color: '#00d4aa',
              border: '1px solid rgba(0,212,170,0.3)',
            }}
          >
            Урок {lesson.id}
          </span>
          <span
            className="px-2.5 py-0.5 rounded-full text-[10px] font-bold"
            style={{
              background: 'rgba(201,162,39,0.1)',
              color: '#c9a227',
            }}
          >
            Часть {lesson.part}: {partLabel}
          </span>
          <span className="text-[10px]" style={{ color: '#9b98a8' }}>
            {diffLabel}
          </span>
        </div>

        <h1 className="text-2xl font-extrabold mb-2" style={{ color: '#e8e6f0' }}>
          {lesson.title}: {lesson.subtitle}
        </h1>

        <p className="text-xs leading-relaxed" style={{ color: '#9b98a8' }}>
          {lesson.story_placement ?? 'Изучай Python в формате квеста.'}
        </p>
      </header>

      {/* Topic card */}
      <div
        className="rounded-xl p-4 flex items-center gap-3"
        style={{
          background: '#1a1924',
          border: '1px solid rgba(201,162,39,0.15)',
        }}
      >
        <span className="text-lg">📖</span>
        <div>
          <p className="text-xs font-bold" style={{ color: '#e8e6f0' }}>Тема урока</p>
          <p className="text-[11px]" style={{ color: '#9b98a8' }}>{lesson.topic}</p>
        </div>
      </div>

      {/* Analogy */}
      {lesson.analogy && (
        <section
          className="rounded-xl p-4 space-y-2"
          style={{
            background: '#1a1924',
            border: '1px solid rgba(162,155,254,0.2)',
          }}
        >
          <h2 className="text-xs font-bold flex items-center gap-2" style={{ color: '#A29BFE' }}>
            <span>💡</span> Аналогия
          </h2>
          {lesson.analogy.story_metaphor && (
            <p className="text-xs leading-relaxed" style={{ color: '#e8e6f0' }}>
              {lesson.analogy.story_metaphor}
            </p>
          )}
          {lesson.analogy.python_mapping && (
            <p className="text-[11px]" style={{ color: '#9b98a8' }}>
              <span style={{ color: '#c9a227' }}>В Python:</span> {lesson.analogy.python_mapping}
            </p>
          )}
          {lesson.analogy.key_rule && (
            <p className="text-[11px] px-2 py-1 rounded" style={{ background: 'rgba(201,162,39,0.1)', color: '#c9a227' }}>
              📌 {lesson.analogy.key_rule}
            </p>
          )}
        </section>
      )}

      {/* Explanation + Code example */}
      <section
        className="rounded-xl p-4 space-y-4"
        style={{
          background: '#1a1924',
          border: '1px solid rgba(0,212,170,0.2)',
        }}
      >
        <h2 className="text-xs font-bold flex items-center gap-2" style={{ color: '#00d4aa' }}>
          <span>📝</span> Объяснение
        </h2>

        {safeExplanationText && (
          <p className="text-xs leading-relaxed" style={{ color: '#e8e6f0' }}>
            {safeExplanationText}
          </p>
        )}

        {safeCodeExample && (
          <div>
            <p className="text-[10px] font-bold mb-1 uppercase tracking-wider" style={{ color: '#9b98a8' }}>
              Пример кода:
            </p>
            <CodeBlock code={safeCodeExample} />
          </div>
        )}

        {safeOutput && (
          <div>
            <p className="text-[10px] font-bold mb-1 uppercase tracking-wider" style={{ color: '#9b98a8' }}>
              Вывод:
            </p>
            <div
              className="p-2.5 rounded-lg font-mono text-xs"
              style={{
                background: '#0d0c14',
                border: '1px solid rgba(0,212,170,0.2)',
                color: '#00d4aa',
              }}
            >
              {safeOutput}
            </div>
          </div>
        )}
      </section>

      {/* Mini summary */}
      {lesson.mini_summary && (
        <section
          className="rounded-xl p-4"
          style={{
            background: '#1a1924',
            border: '1px solid rgba(201,162,39,0.15)',
          }}
        >
          <h2 className="text-xs font-bold mb-2 flex items-center gap-2" style={{ color: '#c9a227' }}>
            <span>📌</span> Кратко
          </h2>
          <p className="text-xs leading-relaxed" style={{ color: '#e8e6f0' }}>
            {lesson.mini_summary}
          </p>
        </section>
      )}

      {/* CTA */}
      <div
        className="rounded-xl p-6 text-center"
        style={{
          background: '#1a1924',
          border: '2px solid rgba(201,162,39,0.3)',
        }}
      >
        <p className="text-sm font-bold mb-1" style={{ color: '#e8e6f0' }}>
          Готов начать обучение?
        </p>
        <p className="text-xs mb-4" style={{ color: '#9b98a8' }}>
          Пройди onboarding и получи полный доступ к курсу с практическими заданиями, тестами и миссиями.
        </p>
        <Link
          to="/onboarding"
          className="inline-block px-8 py-3 rounded-lg text-sm font-bold transition-all hover:scale-105"
          style={{
            background: 'linear-gradient(135deg, #c9a227, #8b7355)',
            color: '#0f0e17',
            textDecoration: 'none',
          }}
        >
          Начать обучение 🚀
        </Link>
        <div className="mt-3">
          <Link
            to="/course"
            className="text-xs font-medium transition-all hover:opacity-80"
            style={{ color: '#9b98a8', textDecoration: 'none' }}
          >
            ← Все уроки
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center py-4">
        <p className="text-[11px]" style={{ color: '#6b7280' }}>
          Python Quest — игровой курс Python для новичков
        </p>
      </footer>
    </div>
  )
}
