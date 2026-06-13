import type { CharacterGrowth } from '../types'

interface Props {
  characterGrowth: CharacterGrowth
}

export default function CharacterGrowthCard({ characterGrowth }: Props) {
  const { internal } = characterGrowth

  return (
    <div
      className="mt-6 mb-6 rounded-xl border animate-fade-in"
      style={{
        background: 'rgba(201, 162, 39, 0.04)',
        borderColor: 'rgba(201, 162, 39, 0.2)',
      }}
    >
      {/* Header */}
      <div
        className="flex items-center gap-2 px-5 pt-4 pb-0"
        style={{ color: '#c9a227' }}
      >
        <span className="material-symbols-outlined text-base">psychology</span>
        <span className="text-xs uppercase tracking-wider font-medium opacity-90">
          Малёк размышляет
        </span>
      </div>

      {/* Internal monologue */}
      <div className="px-5 py-3">
        <p
          className="text-sm leading-relaxed italic m-0"
          style={{ color: '#e8e6f0' }}
        >
          «{internal}»
        </p>
      </div>
    </div>
  )
}
