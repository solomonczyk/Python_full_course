interface Props {
  text: string
}

export default function GameRelevanceBlock({ text }: Props) {
  return (
    <section className="bg-primary-container rounded-2xl p-6 border-l-8 border-action-da shadow-sm">
      <div className="flex items-center gap-3 mb-3">
        <span className="material-symbols-outlined text-primary text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>stadia_controller</span>
        <h3 className="font-display text-[20px] font-bold text-on-primary-container">Связь с финальной игрой</h3>
      </div>
      <p className="font-sans text-[15px] leading-[22px] text-on-primary-container text-opacity-85">{text}</p>
    </section>
  )
}
