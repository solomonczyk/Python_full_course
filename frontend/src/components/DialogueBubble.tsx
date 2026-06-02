import type { Character } from '../types'
import CharacterAvatar from './CharacterAvatar'

const BORDER_COLORS: Record<Character, string> = {
  ksyu:  '#74B9FF',
  va:    '#A29BFE',
  da:    '#28A745',
  bagus: '#FF7675',
  novice: '#9b98a8',
}

const NAMES: Record<Character, string> = {
  ksyu:  'Ксю',
  va:    'Ва',
  da:    'Да',
  bagus: 'Багус',
  novice: 'Новичок',
}

const NAME_COLORS: Record<Character, string> = {
  ksyu:  '#74B9FF',
  va:    '#A29BFE',
  da:    '#28A745',
  bagus: '#FF7675',
  novice: '#9b98a8',
}

function renderText(text?: string | null) {
  if (!text) return null
  const parts = text.split(/(`[^`]+`)/)
  return parts.map((part, i) =>
    part.startsWith('`') && part.endsWith('`')
      ? <code key={i} style={{ background: 'rgba(0,212,170,0.15)', color: '#00d4aa', padding: '2px 6px', borderRadius: '4px', fontFamily: "'JetBrains Mono', monospace", fontSize: '13px' }}>{part.slice(1, -1)}</code>
      : <span key={i}>{part}</span>
  )
}

export default function DialogueBubble({ character, text }: { character: Character; text?: string | null }) {
  if (!text) return null
  return (
    <section className="flex gap-4 items-start">
      <CharacterAvatar character={character} />
      <div
        className="relative rounded-xl p-4 flex-1"
        style={{
          background: '#1a1924',
          border: `2px solid ${BORDER_COLORS[character]}66`,
        }}
      >
        <div
          className="absolute -left-2 top-6 w-4 h-4 rotate-45 rounded-sm"
          style={{
            background: '#1a1924',
            borderLeft: '2px solid',
            borderBottom: '2px solid',
            borderColor: BORDER_COLORS[character],
          }}
        />
        <p className="text-xs font-bold mb-1" style={{ color: NAME_COLORS[character] }}>
          {NAMES[character]}
        </p>
        <p className="text-xs leading-relaxed" style={{ color: '#e8e6f0' }}>
          {renderText(text)}
        </p>
      </div>
    </section>
  )
}
