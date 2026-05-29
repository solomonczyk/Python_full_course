interface Props {
  text: string
}

export default function MiniSummaryBlock({ text }: Props) {
  return (
    <section className="bg-surface-container-highest rounded-xl px-5 py-4 flex items-start gap-3 shadow-sm">
      <span className="material-symbols-outlined text-primary text-xl shrink-0 mt-0.5" style={{ fontVariationSettings: "'FILL' 1" }}>lightbulb</span>
      <div>
        <span className="font-sans text-[13px] font-bold text-primary tracking-wider">МИНИ-ИТОГ</span>
        <p className="font-sans text-[15px] leading-[22px] text-on-surface font-medium mt-1">{text}</p>
      </div>
    </section>
  )
}
