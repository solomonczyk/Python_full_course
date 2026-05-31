import type { CommonMistake } from '../types'
import CharacterAvatar from './CharacterAvatar'

interface Props {
  mistakes: CommonMistake[]
}

export default function CommonMistakesBlock({ mistakes }: Props) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 pb-2" style={{ borderBottom: '1px solid rgba(255,107,107,0.2)' }}>
        <CharacterAvatar character="bagus" size="sm" />
        <div>
          <h3 className="text-xs font-bold" style={{ color: '#ff6b6b' }}>Багус предупреждает</h3>
          <p className="text-[10px]" style={{ color: '#9b98a8' }}>
            Типичные ошибки новичков — учись на чужих шишках!
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {mistakes.map((m, i) => (
          <div
            key={i}
            className="rounded-lg p-3"
            style={{ background: '#0f0e17', border: '1px solid rgba(201,162,39,0.1)' }}
          >
            <p className="text-xs font-bold mb-2" style={{ color: '#e8e6f0' }}>
              {i + 1}. {m.title}
            </p>

            <div className="mb-2">
              <div className="text-[10px] font-bold mb-1" style={{ color: '#ff6b6b' }}>❌ Неправильно:</div>
              <div
                className="rounded-lg overflow-hidden"
                style={{ border: '1px solid rgba(255,107,107,0.2)' }}
              >
                <div
                  className="px-3 py-1 text-[10px] font-mono"
                  style={{ background: 'rgba(255,107,107,0.08)', color: '#ff6b6b' }}
                >
                  {m.wrong}
                </div>
              </div>
            </div>

            <div className="mb-2">
              <div className="text-[10px] font-bold mb-1" style={{ color: '#00d4aa' }}>✅ Правильно:</div>
              <div
                className="rounded-lg overflow-hidden"
                style={{ border: '1px solid rgba(0,212,170,0.2)' }}
              >
                <div
                  className="px-3 py-1 text-[10px] font-mono"
                  style={{ background: 'rgba(0,212,170,0.08)', color: '#00d4aa' }}
                >
                  {m.right}
                </div>
              </div>
            </div>

            {m.note && (
              <p className="text-[11px] leading-relaxed" style={{ color: '#9b98a8' }}>
                {m.note}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
