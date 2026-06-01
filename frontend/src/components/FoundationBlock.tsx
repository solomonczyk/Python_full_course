import type { FoundationBlock as FoundationBlockType } from '../types'

interface Props {
  foundation: FoundationBlockType
}

export default function FoundationBlock({ foundation }: Props) {
  return (
    <div
      className="rounded-xl p-5 mb-6"
      style={{
        background: 'linear-gradient(135deg, rgba(201,162,39,0.12), rgba(201,162,39,0.04))',
        border: '1px solid rgba(201,162,39,0.25)',
      }}
    >
      <div className="flex items-center gap-2 mb-4">
        <span className="material-symbols-outlined text-lg" style={{ color: '#ffd700' }}>
          construction
        </span>
        <h3 className="text-sm font-bold uppercase tracking-wider" style={{ color: '#ffd700' }}>
          {foundation.title || 'Перед стартом'}
        </h3>
      </div>

      {/* Terms with definitions */}
      {foundation.terms && foundation.terms.length > 0 && (
        <div className="space-y-3 mb-4">
          {foundation.terms.map((term, i) => (
            <div
              key={i}
              className="rounded-lg p-3"
              style={{ background: 'rgba(15,14,23,0.6)', border: '1px solid rgba(201,162,39,0.1)' }}
            >
              <div className="flex items-start gap-2">
                <span
                  className="text-xs font-bold rounded px-1.5 py-0.5 shrink-0 mt-0.5"
                  style={{ background: 'rgba(201,162,39,0.2)', color: '#ffd700' }}
                >
                  {term.label}
                </span>
                <span className="text-xs leading-relaxed" style={{ color: '#c4c2d0' }}>
                  {term.definition}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Glossary links (lightweight mode) */}
      {(!foundation.terms || foundation.terms.length === 0) && foundation.glossary_terms && foundation.glossary_terms.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          <span className="text-[10px] font-bold uppercase tracking-wider self-center" style={{ color: '#9b98a8' }}>
            Термины:
          </span>
          {foundation.glossary_terms.map((termId, i) => (
            <a
              key={i}
              href={`/glossary#${termId}`}
              className="text-xs px-2 py-1 rounded-md no-underline transition-all hover:opacity-80"
              style={{
                background: 'rgba(0,212,170,0.1)',
                border: '1px solid rgba(0,212,170,0.2)',
                color: '#00d4aa',
              }}
            >
              {termId}
            </a>
          ))}
        </div>
      )}

      {/* Rules */}
      {foundation.rules && foundation.rules.length > 0 && (
        <div>
          <h4 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#9b98a8' }}>
            Правила:
          </h4>
          <ul className="space-y-1.5">
            {foundation.rules.map((rule, i) => (
              <li key={i} className="flex items-start gap-2 text-xs" style={{ color: '#c4c2d0' }}>
                <span className="text-emerald-400 shrink-0 mt-0.5">✓</span>
                <span>{rule}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
