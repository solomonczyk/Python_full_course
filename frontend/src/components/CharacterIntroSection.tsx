const CHARACTERS = [
  { id: 'novice', image: '/avatars/novichok.webp' },
  { id: 'ksyu', image: '/avatars/ksyu.webp' },
  { id: 'va', image: '/avatars/Va.webp' },
  { id: 'da', image: '/avatars/da.webp' },
  { id: 'bagus', image: '/avatars/bagus.webp' },
]

export default function CharacterIntroSection() {
  return (
    <section className="mb-12">
      <div className="flex items-center gap-3 mb-2">
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center"
          style={{ background: 'rgba(201,162,39,0.15)' }}
        >
          <span className="material-symbols-outlined text-lg" style={{ color: '#c9a227', fontVariationSettings: "'FILL' 1" }}>diversity_3</span>
        </div>
        <h2 className="font-display text-[24px] leading-8 font-bold" style={{ color: '#e8e6f0' }}>Персонажи курса</h2>
      </div>
      <p className="font-sans text-[15px] leading-[22px] mb-6 max-w-[600px]" style={{ color: '#9b98a8' }}>
        В Python Quest у каждого персонажа своя роль. Вместе они проводят тебя через все ловушки Башни Алгоритмов.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {CHARACTERS.map((c) => (
          <div
            key={c.id}
            className="rounded-2xl overflow-hidden"
            style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.15)' }}
          >
            <img
              src={c.image}
              alt={c.id}
              className="w-full h-auto object-contain"
              style={{ display: 'block' }}
            />
          </div>
        ))}
      </div>
    </section>
  )
}
