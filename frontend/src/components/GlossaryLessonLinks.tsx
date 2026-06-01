import { useEffect, useState } from 'react'
import type { GlossaryTermSummary } from '../types'

const BASE = '/api'

interface Props {
  termIds: string[]
}

export default function GlossaryLessonLinks({ termIds }: Props) {
  const [terms, setTerms] = useState<GlossaryTermSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!termIds || termIds.length === 0) {
      setLoading(false)
      return
    }
    fetch(`${BASE}/glossary`)
      .then((r) => r.json())
      .then((data: GlossaryTermSummary[]) => {
        if (Array.isArray(data)) {
          const filtered = data.filter((t) => termIds.includes(t.id))
          setTerms(filtered)
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [termIds])

  if (loading || terms.length === 0) return null

  return (
    <div
      className="rounded-xl p-4 mb-6"
      style={{
        background: 'rgba(0,212,170,0.06)',
        border: '1px solid rgba(0,212,170,0.15)',
      }}
    >
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-sm" style={{ color: '#00d4aa' }}>
          book
        </span>
        <h4 className="text-[10px] font-bold uppercase tracking-wider" style={{ color: '#00d4aa' }}>
          Термины урока
        </h4>
      </div>
      <div className="flex flex-wrap gap-2">
        {terms.map((t) => (
          <a
            key={t.id}
            href={`/glossary#${t.id}`}
            className="text-xs px-2.5 py-1 rounded-full no-underline transition-all hover:opacity-80"
            style={{
              background: 'rgba(0,212,170,0.1)',
              border: '1px solid rgba(0,212,170,0.2)',
              color: '#7ee8d4',
            }}
          >
            {t.term}
          </a>
        ))}
      </div>
    </div>
  )
}
