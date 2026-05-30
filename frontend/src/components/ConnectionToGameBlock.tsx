interface Props {
  text: string
}

export default function ConnectionToGameBlock({ text }: Props) {
  return (
    <div
      className="rounded-xl p-4"
      style={{
        background: 'rgba(0,212,170,0.08)',
        border: '1px solid rgba(0,212,170,0.2)',
      }}
    >
      <div className="flex items-center gap-2 mb-2">
        <span className="material-symbols-outlined text-sm" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>flag</span>
        <h3 className="text-xs font-bold" style={{ color: '#00d4aa' }}>В финальной игре</h3>
      </div>
      <p className="text-xs leading-relaxed font-medium" style={{ color: '#e8e6f0' }}>
        {text}
      </p>
    </div>
  )
}
