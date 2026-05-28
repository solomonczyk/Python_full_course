import type { Character } from '../types'
import { CHARACTER_AVATARS } from '../constants'

const LABELS: Record<Character, string> = {
  ksyu: 'Ксю',
  va: 'Ва',
  da: 'Да',
  bagus: 'Багус',
}

const COLORS: Record<Character, string> = {
  ksyu: 'border-mentor-ksyu',
  va: 'border-logic-va',
  da: 'border-action-da',
  bagus: 'border-error-bagus',
}

interface Props {
  character: Character
  size?: 'sm' | 'md' | 'lg'
  src?: string
}

export default function CharacterAvatar({ character, size = 'md', src }: Props) {
  const dim = size === 'sm' ? 'w-8 h-8' : size === 'lg' ? 'w-16 h-16' : 'w-14 h-14'
  const imgDim = size === 'sm' ? 'w-8 h-8' : size === 'lg' ? 'w-16 h-16' : 'w-14 h-14'
  const imgSrc = src ?? CHARACTER_AVATARS[character]

  return (
    <div
      className={`${dim} rounded-full border-2 ${COLORS[character]} shrink-0 overflow-hidden bg-white shadow-sm`}
      title={LABELS[character]}
    >
      <img
        src={imgSrc}
        alt={LABELS[character]}
        className={`${imgDim} object-cover`}
      />
    </div>
  )
}
