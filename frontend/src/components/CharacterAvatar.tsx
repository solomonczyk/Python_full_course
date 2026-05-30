import { useState } from 'react'
import type { Character } from '../types'
import { CHARACTER_AVATARS } from '../constants'

const LABELS: Record<Character, string> = {
  ksyu: 'Ксю',
  va: 'Ва',
  da: 'Да',
  bagus: 'Багус',
  novice: 'Новичок',
}

const BG_COLORS: Record<Character, string> = {
  ksyu: '#74B9FF',
  va: '#A29BFE',
  da: '#28A745',
  bagus: '#FF7675',
  novice: '#9b98a8',
}

const BORDER_CLASSES: Record<Character, string> = {
  ksyu: 'border-mentor-ksyu',
  va: 'border-logic-va',
  da: 'border-action-da',
  bagus: 'border-error-bagus',
  novice: 'border-outline-variant',
}

interface Props {
  character: Character
  size?: 'sm' | 'md' | 'lg'
  src?: string
}

export default function CharacterAvatar({ character, size = 'md', src }: Props) {
  const dim = size === 'sm' ? 'w-8 h-8' : size === 'lg' ? 'w-16 h-16' : 'w-14 h-14'
  const imgDim = size === 'sm' ? 'w-8 h-8' : size === 'lg' ? 'w-16 h-16' : 'w-14 h-14'
  const textSize = size === 'sm' ? 'text-[10px]' : size === 'lg' ? 'text-lg' : 'text-sm'
  const imgSrc = src ?? CHARACTER_AVATARS[character]
  const [imgError, setImgError] = useState(false)

  return (
    <div
      className={`${dim} rounded-full border-2 ${BORDER_CLASSES[character]} shrink-0 flex items-center justify-center font-bold ${textSize}`}
      style={{ background: BG_COLORS[character], color: '#0f0e17' }}
      title={LABELS[character]}
    >
      {imgError ? (
        <span>{LABELS[character][0]}</span>
      ) : (
        <img
          src={imgSrc}
          alt={LABELS[character]}
          className={`${imgDim} object-cover rounded-full`}
          onError={() => setImgError(true)}
        />
      )}
    </div>
  )
}
