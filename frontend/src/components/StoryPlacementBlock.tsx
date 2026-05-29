interface Props {
  text: string
}

export default function StoryPlacementBlock({ text }: Props) {
  return (
    <section className="bg-surface-container rounded-2xl p-6 border-l-8 border-tertiary shadow-sm">
      <div className="flex items-center gap-3 mb-3">
        <span className="material-symbols-outlined text-tertiary text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>auto_stories</span>
        <h3 className="font-display text-[20px] font-bold text-on-surface">Место в истории</h3>
      </div>
      <p className="font-sans text-[15px] leading-[22px] text-on-surface-variant">{text}</p>
    </section>
  )
}
