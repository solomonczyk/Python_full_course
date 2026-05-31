import CharacterCard from './CharacterCard'

const CHARACTERS = [
  {
    id: 'novice',
    name: 'Новичок',
    role: 'Главный герой курса',
    description: 'Ты начинаешь с нуля, ничего не знаешь о Python, но хочешь научиться. Проходишь путь от первой команды print() до создания собственной консольной игры.',
    storyFunction: 'Проходит путь от первой команды до финальной игры «Побег из Башни Багуса»',
    image: '/avatars/novichok.webp',
  },
  {
    id: 'ksyu',
    name: 'Ксю',
    role: 'Наставница простых объяснений',
    description: 'Мягко и спокойно объясняет новые темы. Ксю — твой первый проводник в мир Python. С ней даже сложные вещи кажутся простыми.',
    storyFunction: 'Объясняет новые темы простыми словами и поддерживает на всём пути',
    image: '/avatars/ksyu.webp',
  },
  {
    id: 'va',
    name: 'Ва',
    role: 'Мастер логики',
    description: 'Строгий голос логики. Ва не даёт угадывать, заставляет думать и проверять каждое условие. Его вопросы — лучшая подготовка к реальному коду.',
    storyFunction: 'Помогает думать алгоритмически и не пропускать ошибки',
    image: '/avatars/Va.webp',
  },
  {
    id: 'da',
    name: 'Да',
    role: 'Тренер практики',
    description: 'Превращает теорию в действие. Да даёт миссии, задачи и проекты. Если Ксю объясняет, а Ва проверяет, то Да заставляет делать.',
    storyFunction: 'Даёт практические миссии и приближает к финальной игре',
    image: '/avatars/da.webp',
  },
  {
    id: 'bagus',
    name: 'Багус',
    role: 'Вредитель и мастер ошибок',
    description: 'Главный антагонист курса. Багус ломает код, прячет ошибки в отступах, путает индексы и подсовывает баги. Каждая его ловушка — шанс научиться.',
    storyFunction: 'Создаёт ошибки, через которые ученик учится быть внимательнее',
    image: '/avatars/bagus.webp',
    antagonist: true,
  },
]

export default function CharacterIntroSection() {
  return (
    <section className="mb-12">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>diversity_3</span>
        </div>
        <h2 className="font-display text-[24px] leading-8 font-bold text-on-surface">Персонажи курса</h2>
      </div>
      <p className="font-sans text-[15px] leading-[22px] text-on-surface-variant mb-6 max-w-[600px]">
        В Python Quest у каждого персонажа своя роль. Вместе они проводят тебя через все ловушки Башни Алгоритмов.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {CHARACTERS.map((c) => (
          <CharacterCard
            key={c.id}
            name={c.name}
            role={c.role}
            description={c.description}
            storyFunction={c.storyFunction}
            image={c.image}
            antagonist={c.antagonist}
          />
        ))}
      </div>
    </section>
  )
}
