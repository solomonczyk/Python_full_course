import type { Character } from '../types'
import CharacterAvatar from './CharacterAvatar'

const BORDER: Record<Character, string> = {
  ksyu:  'border-mentor-ksyu/40',
  va:    'border-logic-va/40',
  da:    'border-action-da/40',
  bagus: 'border-error-bagus/40',
}

const NAMES: Record<Character, string> = {
  ksyu:  'Ксю',
  va:    'Ва',
  da:    'Да',
  bagus: 'Багус',
}

const NAME_COLORS: Record<Character, string> = {
  ksyu:  'text-secondary',
  va:    'text-tertiary',
  da:    'text-primary',
  bagus: 'text-error',
}

function renderText(text: string) {
  const parts = text.split(/(`[^`]+`)/)
  return parts.map((part, i) =>
    part.startsWith('`') && part.endsWith('`')
      ? <code key={i} className="bg-surface-container-highest px-1.5 py-0.5 rounded text-primary font-mono text-[13px]">{part.slice(1, -1)}</code>
      : <span key={i}>{part}</span>
  )
}

export default function DialogueBubble({ character, text }: { character: Character; text: string }) {
  return (
    <section className="flex gap-4 items-start">
      <CharacterAvatar character={character} />
      <div className={`relative bg-white border-2 ${BORDER[character]} rounded-2xl p-4 shadow-sm flex-1`}>
        <div className="absolute -left-2 top-6 w-4 h-4 bg-white border-l-2 border-b-2 border-inherit rotate-45 rounded-sm" />
        <p className="text-[13px] font-label-bold mb-1 {NAME_COLORS[character]}">
          <span className={NAME_COLORS[character]}>{NAMES[character]}</span>
        </p>
        <p className="font-sans text-[15px] leading-[22px] font-medium text-on-surface">
          {renderText(text)}
        </p>
      </div>
    </section>
  )
}
