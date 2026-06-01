import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useRecap } from '../hooks/useApi'
import { usePageMeta } from '../hooks/usePageMeta'

const PART_QUESTS: Record<number, string> = {
  1: 'quest-1',
  2: 'quest-2',
  3: 'quest-3',
  4: 'quest-4',
  5: 'quest-5',
}

const PART_LABELS: Record<number, string> = {
  1: 'Hello Python',
  2: 'Data Magic',
  3: 'The Logic Gate',
  4: 'Loop Labyrinth',
  5: 'Constructs',
}

export default function RecapPage() {
  const { id } = useParams<{ id: string }>()
  const { recap, loading, error } = useRecap(id || '')

  usePageMeta({
    title: recap ? `${recap.title}` : 'Повторение',
    description: recap ? recap.story_summary.slice(0, 160) : 'Повторение пройденного материала',
  })

  const [showAnswers, setShowAnswers] = useState<Record<number, boolean>>({})

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin w-6 h-6 border-2 border-emerald-400 border-t-transparent rounded-full" />
      </div>
    )
  }

  if (error || !recap) {
    return (
      <div className="text-center py-20">
        <p className="text-sm" style={{ color: '#ff6b6b' }}>Напоминалка не найдена</p>
        <Link to="/" className="text-xs mt-3 inline-block" style={{ color: '#00d4aa' }}>
          ← Вернуться на главную
        </Link>
      </div>
    )
  }

  const questId = PART_QUESTS[recap.part]

  return (
    <div className="py-6">
      {/* Header */}
      <div
        className="rounded-xl p-5 mb-6"
        style={{
          background: 'linear-gradient(135deg, rgba(201,162,39,0.12), rgba(201,162,39,0.04))',
          border: '1px solid rgba(201,162,39,0.25)',
        }}
      >
        <div className="flex items-center gap-2 mb-1">
          <span className="material-symbols-outlined text-xl" style={{ color: '#ffd700' }}>
            history_edu
          </span>
          <span className="text-[10px] font-bold uppercase tracking-wider" style={{ color: '#ffd700' }}>
            RECAP · Part {recap.part}: {PART_LABELS[recap.part] ?? ''}
          </span>
        </div>
        <h1 className="text-lg font-bold mt-1" style={{ color: '#e8e6f0' }}>{recap.title}</h1>
      </div>

      {/* Story summary */}
      <div
        className="rounded-xl p-4 mb-5"
        style={{
          background: 'rgba(15,14,23,0.6)',
          border: '1px solid rgba(201,162,39,0.1)',
        }}
      >
        <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#9b98a8' }}>
          📖 Что было пройдено
        </h3>
        <p className="text-xs leading-relaxed" style={{ color: '#c4c2d0' }}>
          {recap.story_summary}
        </p>
      </div>

      {/* Learned terms */}
      {recap.learned_terms && recap.learned_terms.length > 0 && (
        <div className="mb-5">
          <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#9b98a8' }}>
            📚 Термины раздела
          </h3>
          <div className="flex flex-wrap gap-1.5">
            {recap.learned_terms.map((termId) => (
              <a
                key={termId}
                href={`/glossary#${termId}`}
                className="text-[10px] px-2 py-0.5 rounded-full no-underline transition-all hover:opacity-80"
                style={{
                  background: 'rgba(0,212,170,0.1)',
                  border: '1px solid rgba(0,212,170,0.2)',
                  color: '#7ee8d4',
                }}
              >
                {termId}
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Hero skills */}
      {recap.hero_skills && recap.hero_skills.length > 0 && (
        <div className="mb-5">
          <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#9b98a8' }}>
            ⚡ Навыки героя
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {recap.hero_skills.map((skill, i) => (
              <div
                key={i}
                className="rounded-lg p-3"
                style={{ background: 'rgba(0,212,170,0.04)', border: '1px solid rgba(0,212,170,0.1)' }}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded" style={{ background: 'rgba(0,212,170,0.15)', color: '#00d4aa' }}>
                    {skill.python}
                  </span>
                </div>
                <p className="text-xs font-semibold mb-0.5" style={{ color: '#e8e6f0' }}>{skill.name}</p>
                <p className="text-[10px]" style={{ color: '#9b98a8' }}>{skill.meaning}</p>
                {skill.analogy && (
                  <p className="text-[10px] italic mt-1" style={{ color: '#7b78a0' }}>🧠 {skill.analogy}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key rules */}
      {recap.key_rules && recap.key_rules.length > 0 && (
        <div
          className="rounded-xl p-4 mb-5"
          style={{
            background: 'rgba(201,162,39,0.04)',
            border: '1px solid rgba(201,162,39,0.1)',
          }}
        >
          <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#c9a227' }}>
            📋 Ключевые правила
          </h3>
          <ul className="space-y-1.5">
            {recap.key_rules.map((rule, i) => (
              <li key={i} className="flex items-start gap-2 text-xs" style={{ color: '#c4c2d0' }}>
                <span style={{ color: '#ffd700' }}>▸</span>
                <span>{rule}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Mini-check */}
      {recap.mini_check && recap.mini_check.length > 0 && (
        <div
          className="rounded-xl p-4 mb-5"
          style={{
            background: 'rgba(0,150,255,0.04)',
            border: '1px solid rgba(0,150,255,0.15)',
          }}
        >
          <h3 className="text-[10px] font-bold uppercase tracking-wider mb-3" style={{ color: '#5b9aff' }}>
            ❓ Проверь себя
          </h3>
          <div className="space-y-3">
            {recap.mini_check.map((check, i) => (
              <div key={i}>
                <p className="text-xs font-semibold mb-1.5" style={{ color: '#e8e6f0' }}>
                  {i + 1}. {check.question}
                </p>
                {showAnswers[i] ? (
                  <div
                    className="rounded-lg p-2.5 text-xs"
                    style={{ background: 'rgba(0,212,170,0.1)', border: '1px solid rgba(0,212,170,0.2)', color: '#7ee8d4' }}
                  >
                    {check.answer}
                  </div>
                ) : (
                  <button
                    onClick={() => setShowAnswers((prev) => ({ ...prev, [i]: true }))}
                    className="text-xs px-3 py-1.5 rounded-lg cursor-pointer border-none transition-all"
                    style={{
                      background: 'rgba(0,212,170,0.1)',
                      border: '1px solid rgba(0,212,170,0.2)',
                      color: '#00d4aa',
                    }}
                  >
                    Показать ответ
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* CTA buttons */}
      <div className="flex flex-wrap gap-3 mt-6">
        {questId && (
          <Link
            to={`/quest/${questId}`}
            className="text-xs px-4 py-2.5 rounded-lg font-bold no-underline transition-all hover:opacity-90"
            style={{
              background: 'linear-gradient(135deg, #ffd700, #c9a227)',
              color: '#0f0e17',
            }}
          >
            ⚔️ Перейти к финальному квесту
          </Link>
        )}
        <Link
          to="/"
          className="text-xs px-4 py-2.5 rounded-lg font-bold no-underline transition-all hover:opacity-90"
          style={{
            background: 'rgba(255,255,255,0.05)',
            border: '1px solid rgba(255,255,255,0.1)',
            color: '#e8e6f0',
          }}
        >
          ← Вернуться к урокам
        </Link>
      </div>
    </div>
  )
}
