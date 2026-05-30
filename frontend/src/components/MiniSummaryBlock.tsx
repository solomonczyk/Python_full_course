interface Props {
  text: string
}

export default function MiniSummaryBlock({ text }: Props) {
  return (
    <div
      className="rounded-xl px-4 py-3 flex items-start gap-3"
      style={{
        background: 'rgba(201,162,39,0.1)',
        border: '1px solid rgba(201,162,39,0.2)',
      }}
    >
      <span className="material-symbols-outlined text-sm shrink-0 mt-0.5" style={{ color: '#ffd700', fontVariationSettings: "'FILL' 1" }}>lightbulb</span>
      <div>
        <span className="text-[11px] font-bold tracking-wider" style={{ color: '#ffd700' }}>МИНИ-ИТОГ</span>
        <p className="text-xs leading-relaxed font-medium mt-1" style={{ color: '#e8e6f0' }}>{text}</p>
      </div>
    </div>
  )
}
