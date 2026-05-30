export interface VariableBox {
  name: string
  value: string
  valueType?: 'str' | 'int' | 'bool' | 'list'
  /** If true, renders a simple arrow between boxes */
  arrow?: boolean
}

interface Props {
  boxes: VariableBox[][]
  title?: string
}

const TYPE_COLORS: Record<string, { box: string; label: string }> = {
  str:  { box: 'border-mentor-ksyu/40',  label: 'str' },
  int:  { box: 'border-action-da/40',    label: 'int' },
  bool: { box: 'border-logic-va/40',     label: 'bool' },
  list: { box: 'border-error-bagus/40',  label: 'list' },
}

function VariableBoxArrow() {
  return (
    <div className="flex items-center justify-center w-8 h-24">
      <span className="material-symbols-outlined text-2xl text-outline" style={{ fontVariationSettings: "'FILL' 0, 'wght' 300" }}>
        arrow_forward
      </span>
    </div>
  )
}

function VariableBoxCard({ v }: { v: VariableBox }) {
  if (v.arrow) {
    return <VariableBoxArrow />
  }

  const colors = v.valueType ? TYPE_COLORS[v.valueType] : TYPE_COLORS['str']
  const displayVal = v.value

  return (
    <div className="flex flex-col items-center gap-1">
      {/* Variable name label — like a sticky note */}
      <div className={`font-mono text-[13px] font-bold px-3 py-1 rounded-lg bg-white border-2 ${colors.box} shadow-sm`}>
        {v.name}
      </div>
      {/* The "box" */}
      <div className={`w-28 h-24 rounded-xl bg-white border-2 ${colors.box} shadow-sm flex flex-col items-center justify-center gap-1 relative`}>
        {/* Value inside the box */}
        <span className="font-mono text-[15px] font-bold text-on-surface">{displayVal}</span>
        {/* Type badge */}
        {v.valueType && (
          <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded-full ${v.valueType === 'str' ? 'bg-mentor-ksyu/10 text-secondary' : v.valueType === 'int' ? 'bg-action-da/10 text-primary' : v.valueType === 'bool' ? 'bg-logic-va/10 text-tertiary' : 'bg-error-bagus/10 text-error'} absolute -bottom-2.5`}>
            {v.valueType}
          </span>
        )}
      </div>
    </div>
  )
}

export default function VariableBoxBlock({ boxes, title }: Props) {
  if (!boxes || boxes.length === 0) return null

  return (
    <section className="bg-white border-2 border-outline-variant rounded-2xl p-5 shadow-sm">
      {title && (
        <h3 className="font-sans text-[13px] font-bold text-on-surface-variant/60 uppercase tracking-wider mb-4">
          {title}
        </h3>
      )}
      <div className="flex flex-col gap-5">
        {boxes.map((row, ri) => (
          <div key={ri} className="flex flex-wrap items-center justify-center gap-3">
            {row.map((v, vi) => (
              <VariableBoxCard key={vi} v={v} />
            ))}
          </div>
        ))}
      </div>
      <p className="font-sans text-[13px] text-on-surface-variant/60 mt-4 text-center">
        ← имя переменной | значение внутри →
      </p>
    </section>
  )
}
