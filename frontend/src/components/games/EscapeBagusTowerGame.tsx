interface Props {
  onComplete: (score: number) => void
}

export default function EscapeBagusTowerGame({ onComplete }: Props) {
  return (
    <div className="flex flex-col items-center justify-center gap-6 p-12 text-center">
      <span className="material-symbols-outlined text-6xl text-secondary" style={{ fontVariationSettings: "'FILL' 1" }}>
        construction
      </span>
      <h2 className="font-display text-[28px] font-bold text-on-surface">Побег из Башни Багуса</h2>
      <p className="font-sans text-[16px] text-on-surface-variant max-w-md">
        Финальная мини-игра ещё в разработке. Скоро вы сможете применить все полученные знания в финальном испытании!
      </p>
      <button
        onClick={() => onComplete(100)}
        className="mt-4 bg-primary text-on-primary font-display text-[18px] font-semibold px-8 py-3 rounded-xl shadow-sm hover:opacity-90 active:scale-95 transition-all"
      >
        Отметить как пройдено
      </button>
    </div>
  )
}
