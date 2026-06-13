import type { StoryEvent } from '../types'

interface Props {
  storyEvent: StoryEvent
}

export default function StoryEventPanel({ storyEvent }: Props) {
  const { location, text, bagus_presence } = storyEvent

  return (
    <div
      className="mb-6 rounded-xl border animate-fade-in"
      style={{
        background: '#14121e',
        borderColor: 'rgba(201, 162, 39, 0.15)',
      }}
    >
      {/* Location label */}
      <div
        className="flex items-center gap-1.5 px-4 pt-3 pb-0"
        style={{ color: '#00d4aa' }}
      >
        <span className="material-symbols-outlined text-sm">location_on</span>
        <span className="text-[11px] uppercase tracking-widest font-medium opacity-80">
          {location}
        </span>
      </div>

      {/* Story text */}
      <div className="px-4 py-2">
        <p
          className="text-sm leading-relaxed italic m-0"
          style={{ color: '#b8b6c4' }}
        >
          {text}
        </p>
      </div>

      {/* Bagus presence */}
      {bagus_presence && (
        <div
          className="mx-4 mb-3 mt-0 px-3 py-2 rounded-lg flex items-start gap-2"
          style={{
            background: 'rgba(255, 107, 107, 0.08)',
            borderLeft: '2px solid rgba(255, 107, 107, 0.4)',
          }}
        >
          <span
            className="text-xs font-bold shrink-0 mt-0.5"
            style={{ color: '#ff6b6b' }}
          >
            Багус
          </span>
          <span
            className="text-xs leading-relaxed"
            style={{ color: '#d4a0a0' }}
          >
            {bagus_presence}
          </span>
        </div>
      )}
    </div>
  )
}
