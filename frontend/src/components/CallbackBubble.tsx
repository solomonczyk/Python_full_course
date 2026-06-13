import type { Callback } from '../types'
import CharacterAvatar from './CharacterAvatar'

interface Props {
  callback: Callback
}

const CHARACTER_NAMES: Record<string, string> = {
  ksyu: 'Ксю',
  va: 'Ва',
  da: 'Да',
  bagus: 'Багус',
  novice: 'Новичок',
}

export default function CallbackBubble({ callback }: Props) {
  const { references_lesson, character, text } = callback
  const charName = CHARACTER_NAMES[character] ?? character

  return (
    <div className="mb-4 animate-fade-in">
      <div
        className="rounded-xl px-4 py-3 flex items-start gap-3"
        style={{
          background: '#1a1924',
          borderLeft: '3px solid rgba(108, 92, 231, 0.4)',
        }}
      >
        {/* Small avatar */}
        <div className="shrink-0">
          <CharacterAvatar character={character as any} size="sm" />
        </div>

        {/* Content */}
        <div className="min-w-0">
          {/* Header row: character name + reference badge */}
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span
              className="text-xs font-semibold"
              style={{ color: '#e8e6f0' }}
            >
              {charName}
            </span>
            <span
              className="text-[10px] px-1.5 py-0.5 rounded font-medium"
              style={{
                background: 'rgba(108, 92, 231, 0.15)',
                color: '#a29bfe',
              }}
            >
              Урок {references_lesson}
            </span>
          </div>

          {/* Callback text */}
          <p
            className="text-xs leading-relaxed m-0"
            style={{ color: '#b8b6c4' }}
          >
            {text}
          </p>
        </div>
      </div>
    </div>
  )
}
