interface Props {
  name: string
  role: string
  description: string
  storyFunction: string
  image: string
  antagonist?: boolean
}

export default function CharacterCard({ name, role, description, storyFunction, image, antagonist }: Props) {
  return (
    <div className={`flex items-start gap-4 p-5 rounded-2xl border-2 transition-all hover:shadow-md
      ${antagonist
        ? 'border-error-bagus/40 bg-error-container/10'
        : 'border-outline-variant bg-white'
      }`}
    >
      <div className={`w-16 h-16 rounded-full overflow-hidden shrink-0 border-2 shadow-sm
        ${antagonist ? 'border-error-bagus' : 'border-outline-variant'}`}
      >
        <img src={image} alt={name} className="w-full h-full object-cover" />
      </div>
      <div className="min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <h3 className="font-display text-[20px] leading-7 font-bold text-on-surface">{name}</h3>
          <span className={`text-[12px] font-bold font-sans px-2 py-0.5 rounded-full
            ${antagonist ? 'bg-error-bagus/15 text-error' : 'bg-surface-container text-on-surface-variant'}`}
          >
            {role}
          </span>
        </div>
        <p className="font-sans text-[14px] leading-[20px] text-on-surface-variant mt-1">{description}</p>
        <p className="font-sans text-[13px] leading-[18px] text-on-surface-variant/70 mt-1">
          <span className="font-bold text-primary">{antagonist ? '⚔️' : '✨'}</span> {storyFunction}
        </p>
      </div>
    </div>
  )
}
