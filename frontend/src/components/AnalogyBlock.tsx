import type { Character } from '../types'
import CharacterAvatar from './CharacterAvatar'

/** Renders text with backtick-delimited code highlighted in a different color/size */
function renderCode(text: string, codeColor: string, baseColor: string, codeSize?: string): React.ReactNode[] {
  const parts = text.split(/(`[^`]+`)/)
  return parts.map((part, i) => {
    if (part.startsWith('`') && part.endsWith('`')) {
      const code = part.slice(1, -1)
      return (
        <code
          key={i}
          style={{
            color: codeColor,
            fontSize: codeSize ?? 'inherit',
            fontWeight: 700,
            fontFamily: "'JetBrains Mono', monospace",
          }}
        >
          {code}
        </code>
      )
    }
    return <span key={i} style={{ color: baseColor }}>{part}</span>
  })
}

interface Props {
  analogy: {
    title: string
    story_metaphor: string
    python_mapping: string
    key_rule: string
  }
  character: Character
}

export default function AnalogyBlock({ analogy, character }: Props) {
  return (
    <div className="space-y-3">
      {/* Title */}
      <div className="flex items-center gap-2 pb-2" style={{ borderBottom: '1px solid rgba(201,162,39,0.2)' }}>
        <span className="text-lg" style={{ color: '#ffd700' }}>💡</span>
        <span className="text-sm font-bold" style={{ color: '#ffd700' }}>{analogy.title}</span>
      </div>

      {/* Story metaphor — character delivers the analogy */}
      <div className="flex gap-3 items-start">
        <CharacterAvatar character={character} size="sm" />
        <p className="text-xs leading-relaxed">
          {renderCode(analogy.story_metaphor, '#00d4aa', '#e8e6f0')}
        </p>
      </div>

      {/* Python mapping */}
      <div
        className="rounded-lg p-3 text-xs leading-relaxed"
        style={{
          background: 'rgba(0,212,170,0.08)',
          border: '1px solid rgba(0,212,170,0.2)',
          color: '#00d4aa',
        }}
      >
        <span className="font-bold">🐍 В Python: </span>
        {renderCode(analogy.python_mapping, '#c084fc', '#00d4aa')}
      </div>

      {/* Key rule — highlight box with emphasized keywords */}
      <div
        className="rounded-lg p-3 leading-relaxed text-center"
        style={{
          background: 'rgba(201,162,39,0.1)',
          border: '1px solid rgba(201,162,39,0.3)',
        }}
      >
        <span className="text-xs font-semibold" style={{ color: '#ffd700' }}>
          ⚡{' '}
          {renderCode(analogy.key_rule, '#ff6b6b', '#ffd700', '13px')}
        </span>
      </div>
    </div>
  )
}
