import { useState, useEffect, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useGlossary } from '../hooks/useApi'
import { usePageMeta } from '../hooks/usePageMeta'
import type { GlossaryTermSummary } from '../types'

const CATEGORIES: { key: string; label: string }[] = [
  { key: '', label: 'Все' },
  { key: 'basics', label: 'Основы' },
  { key: 'strings', label: 'Строки' },
  { key: 'variables', label: 'Переменные' },
  { key: 'numbers', label: 'Числа' },
  { key: 'conditions', label: 'Условия' },
  { key: 'loops', label: 'Циклы' },
  { key: 'functions', label: 'Функции' },
  { key: 'lists', label: 'Списки' },
  { key: 'errors', label: 'Ошибки' },
  { key: 'style', label: 'Стиль кода' },
]

export default function GlossaryPage() {
  usePageMeta({
    title: 'Глоссарий',
    description: 'Словарь терминов Python для начинающих. Простые определения, аналогии и примеры кода.',
  })

  const { terms, loading } = useGlossary()
  const [search, setSearch] = useState('')
  const [activeCategory, setActiveCategory] = useState('')
  const [expandedTerm, setExpandedTerm] = useState<string | null>(null)
  const [termDetail, setTermDetail] = useState<Record<string, any>>({})
  const [loadingDetail, setLoadingDetail] = useState<string | null>(null)

  // Handle hash anchor on initial load
  useEffect(() => {
    const hash = window.location.hash.replace('#', '')
    if (hash) {
      setExpandedTerm(hash)
      setTimeout(() => {
        const el = document.getElementById(`term-${hash}`)
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 300)
    }
  }, [terms])

  const filteredTerms = useMemo(() => {
    let result = terms
    if (activeCategory) {
      result = result.filter((t) => t.category === activeCategory)
    }
    if (search.trim()) {
      const q = search.toLowerCase().trim()
      result = result.filter(
        (t) =>
          t.term.toLowerCase().includes(q) ||
          t.id.toLowerCase().includes(q) ||
          t.python_name.toLowerCase().includes(q)
      )
    }
    return result
  }, [terms, activeCategory, search])

  const toggleExpand = async (termId: string) => {
    if (expandedTerm === termId) {
      setExpandedTerm(null)
      return
    }
    setExpandedTerm(termId)

    if (!termDetail[termId]) {
      setLoadingDetail(termId)
      try {
        const res = await fetch(`/api/glossary/${termId}`)
        if (res.ok) {
          const data = await res.json()
          setTermDetail((prev) => ({ ...prev, [termId]: data }))
        }
      } catch {
        // silently fail
      }
      setLoadingDetail(null)
    }
  }

  return (
    <div className="py-6">
      {/* Header */}
      <div
        className="rounded-xl p-5 mb-6"
        style={{
          background: 'linear-gradient(135deg, rgba(0,212,170,0.1), rgba(0,212,170,0.02))',
          border: '1px solid rgba(0,212,170,0.2)',
        }}
      >
        <div className="flex items-center gap-2 mb-2">
          <span className="material-symbols-outlined text-2xl" style={{ color: '#00d4aa' }}>
            menu_book
          </span>
          <h1 className="text-lg font-bold" style={{ color: '#e8e6f0' }}>📘 Глоссарий</h1>
        </div>
        <p className="text-xs" style={{ color: '#9b98a8' }}>
          Словарь терминов Python с простыми определениями, аналогиями и примерами.
          Нажми на термин, чтобы увидеть подробности.
        </p>
      </div>

      {/* Search */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="🔍 Поиск терминов..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-2.5 rounded-lg text-xs border-none outline-none"
          style={{
            background: '#1a1924',
            border: '1px solid rgba(201,162,39,0.15)',
            color: '#e8e6f0',
          }}
        />
      </div>

      {/* Category filters */}
      <div className="flex flex-wrap gap-2 mb-5">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.key}
            onClick={() => setActiveCategory(cat.key)}
            className="text-xs px-3 py-1.5 rounded-full border-none cursor-pointer transition-all"
            style={{
              background: activeCategory === cat.key ? 'rgba(0,212,170,0.2)' : 'rgba(255,255,255,0.05)',
              border: `1px solid ${activeCategory === cat.key ? 'rgba(0,212,170,0.4)' : 'rgba(255,255,255,0.1)'}`,
              color: activeCategory === cat.key ? '#00d4aa' : '#9b98a8',
            }}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Loading state */}
      {loading && (
        <div className="text-center py-8">
          <div className="animate-spin w-6 h-6 border-2 border-emerald-400 border-t-transparent rounded-full mx-auto mb-2" />
          <p className="text-xs" style={{ color: '#9b98a8' }}>Загрузка глоссария...</p>
        </div>
      )}

      {/* Empty state */}
      {!loading && filteredTerms.length === 0 && (
        <div className="text-center py-8">
          <p className="text-sm" style={{ color: '#9b98a8' }}>
            {search ? 'Ничего не найдено. Попробуй другой запрос.' : 'Нет терминов в этой категории.'}
          </p>
        </div>
      )}

      {/* Terms list */}
      {!loading && (
        <div className="space-y-2">
          {filteredTerms.map((term) => {
            const isExpanded = expandedTerm === term.id
            const detail = termDetail[term.id]
            const isLoading = loadingDetail === term.id

            return (
              <div
                key={term.id}
                id={`term-${term.id}`}
                className="rounded-xl overflow-hidden transition-all"
                style={{
                  border: `1px solid ${isExpanded ? 'rgba(0,212,170,0.3)' : 'rgba(201,162,39,0.1)'}`,
                  background: isExpanded ? 'rgba(0,212,170,0.04)' : 'rgba(15,14,23,0.6)',
                }}
              >
                {/* Term header (clickable) */}
                <button
                  onClick={() => toggleExpand(term.id)}
                  className="w-full flex items-center justify-between px-4 py-3 cursor-pointer border-none text-left"
                  style={{ background: 'transparent' }}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span
                      className="text-[10px] font-bold px-2 py-0.5 rounded shrink-0"
                      style={{
                        background: 'rgba(201,162,39,0.15)',
                        color: '#c9a227',
                      }}
                    >
                      {term.category}
                    </span>
                    <div className="min-w-0">
                      <span className="text-sm font-semibold block truncate" style={{ color: '#e8e6f0' }}>
                        {term.term}
                      </span>
                      {term.python_name && (
                        <span className="text-[10px]" style={{ color: '#9b98a8' }}>
                          {term.python_name}
                        </span>
                      )}
                    </div>
                  </div>
                  <span
                    className="material-symbols-outlined text-sm shrink-0 ml-2 transition-transform"
                    style={{
                      color: '#9b98a8',
                      transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)',
                    }}
                  >
                    expand_more
                  </span>
                </button>

                {/* Expanded detail */}
                {isExpanded && (
                  <div className="px-4 pb-4 pt-0 border-t border-transparent">
                    {isLoading ? (
                      <div className="flex items-center gap-2 py-3">
                        <div className="animate-spin w-4 h-4 border-2 border-emerald-400 border-t-transparent rounded-full" />
                        <span className="text-xs" style={{ color: '#9b98a8' }}>Загрузка...</span>
                      </div>
                    ) : detail ? (
                      <div className="space-y-3 pt-3">
                        {/* Definition */}
                        <div>
                          <h4 className="text-[10px] font-bold uppercase tracking-wider mb-1" style={{ color: '#9b98a8' }}>
                            Определение
                          </h4>
                          <p className="text-xs leading-relaxed" style={{ color: '#c4c2d0' }}>
                            {detail.simple_definition}
                          </p>
                        </div>

                        {/* Analogy */}
                        {detail.analogy && (
                          <div
                            className="rounded-lg p-3"
                            style={{ background: 'rgba(201,162,39,0.06)', border: '1px solid rgba(201,162,39,0.1)' }}
                          >
                            <h4 className="text-[10px] font-bold uppercase tracking-wider mb-1" style={{ color: '#c9a227' }}>
                              🧠 Аналогия
                            </h4>
                            <p className="text-xs leading-relaxed" style={{ color: '#c4c2d0' }}>
                              {detail.analogy}
                            </p>
                          </div>
                        )}

                        {/* Code example */}
                        {detail.code_example && (
                          <div>
                            <h4 className="text-[10px] font-bold uppercase tracking-wider mb-1" style={{ color: '#9b98a8' }}>
                              Пример кода
                            </h4>
                            <pre
                              className="text-xs p-3 rounded-lg overflow-x-auto"
                              style={{
                                background: '#0a0910',
                                border: '1px solid rgba(0,212,170,0.1)',
                                color: '#7ee8d4',
                                fontFamily: "'JetBrains Mono', monospace",
                              }}
                            >
                              {detail.code_example}
                            </pre>
                          </div>
                        )}

                        {/* Common mistake */}
                        {detail.common_mistake && (
                          <div
                            className="rounded-lg p-3"
                            style={{ background: 'rgba(255,107,107,0.06)', border: '1px solid rgba(255,107,107,0.15)' }}
                          >
                            <h4 className="text-[10px] font-bold uppercase tracking-wider mb-1" style={{ color: '#ff6b6b' }}>
                              ⚠️ Частая ошибка
                            </h4>
                            <p className="text-xs leading-relaxed mb-1" style={{ color: '#ffb3b3' }}>
                              {detail.common_mistake}
                            </p>
                            {detail.mistake_explanation && (
                              <p className="text-xs leading-relaxed" style={{ color: '#c4c2d0' }}>
                                {detail.mistake_explanation}
                              </p>
                            )}
                          </div>
                        )}

                        {/* Related lessons */}
                        {detail.related_lessons && detail.related_lessons.length > 0 && (
                          <div>
                            <h4 className="text-[10px] font-bold uppercase tracking-wider mb-1.5" style={{ color: '#9b98a8' }}>
                              Связанные уроки
                            </h4>
                            <div className="flex flex-wrap gap-1.5">
                              {detail.related_lessons.map((lid: string) => (
                                <Link
                                  key={lid}
                                  to={`/lesson/${lid}`}
                                  className="text-[10px] px-2 py-0.5 rounded no-underline transition-all hover:opacity-80"
                                  style={{
                                    background: 'rgba(0,212,170,0.1)',
                                    border: '1px solid rgba(0,212,170,0.2)',
                                    color: '#00d4aa',
                                  }}
                                >
                                  Урок {lid}
                                </Link>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    ) : null}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}

      {/* Count footer */}
      {!loading && (
        <p className="text-center text-[10px] mt-6" style={{ color: '#9b98a8' }}>
          Всего терминов: {terms.length} · Показано: {filteredTerms.length}
        </p>
      )}
    </div>
  )
}
