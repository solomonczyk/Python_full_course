import type { Character } from '../types'

const AVATARS: Record<Character, { emoji: string; color: string; label: string }> = {
  ksyu: { emoji: '🤖', color: 'border-mentor-ksyu bg-blue-50', label: 'Ксю' },
  va:   { emoji: '🧙', color: 'border-logic-va bg-purple-50', label: 'Ва' },
  da:   { emoji: '⚔️', color: 'border-action-da bg-green-50', label: 'Да' },
  bagus:{ emoji: '🐛', color: 'border-error-bagus bg-red-50', label: 'Багус' },
}

export default function CharacterAvatar({ character, size = 'md' }: { character: Character; size?: 'sm' | 'md' | 'lg' }) {
  const { emoji, color, label } = AVATARS[character]
  const dim = size === 'sm' ? 'w-8 h-8 text-lg' : size === 'lg' ? 'w-16 h-16 text-3xl' : 'w-14 h-14 text-2xl'
  return (
    <div
      className={`${dim} rounded-full border-2 ${color} flex items-center justify-center shadow-sm shrink-0`}
      title={label}
    >
      {emoji}
    </div>
  )
}
