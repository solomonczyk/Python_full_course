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
    <div className={`rounded-2xl border-2 overflow-hidden transition-all hover:shadow-md
      ${antagonist
        ? 'border-error-bagus/40 bg-error-container/10'
        : 'border-outline-variant bg-white'
      }`}
    >
      <div className="w-full aspect-[3/2] overflow-hidden bg-surface-container-low">
        <img src={image} alt={name} className="w-full h-full object-contain" />
      </div>
      <div className="p-5">
        <div className="flex items-center gap-2 flex-wrap mb-2">
          <h3 className="font-display text-[22px] leading-7 font-bold text-on-surface">{name}</h3>
          <span className={`text-[12px] font-bold font-sans px-2.5 py-0.5 rounded-full
            ${antagonist ? 'bg-error-bagus/15 text-error' : 'bg-primary/10 text-primary'}`}
          >
            {role}
          </span>
        </div>
        <p className="font-sans text-[14px] leading-[20px] text-on-surface-variant">{description}</p>
        <p className="font-sans text-[13px] leading-[18px] text-on-surface-variant/70 mt-2 pt-2 border-t border-outline-variant/30">
          <span className="font-bold">{antagonist ? '⚔️' : '✨'}</span> {storyFunction}
        </p>
      </div>
    </div>
  )
}
