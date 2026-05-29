interface Props {
  text: string
}

export default function ConnectionToGameBlock({ text }: Props) {
  return (
    <section className="bg-secondary-container rounded-2xl p-6 border-l-8 border-secondary shadow-sm">
      <div className="flex items-center gap-3 mb-3">
        <span className="material-symbols-outlined text-secondary text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>flag</span>
        <h3 className="font-display text-[20px] font-bold text-on-secondary-container">🚀 В финальной игре</h3>
      </div>
      <p className="font-sans text-[15px] leading-[22px] text-on-secondary-container text-opacity-85">{text}</p>
    </section>
  )
}
