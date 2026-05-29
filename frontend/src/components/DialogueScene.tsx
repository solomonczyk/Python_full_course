import type { DialogueLine } from '../types'
import DialogueBubble from './DialogueBubble'

interface Props {
  lines: DialogueLine[]
}

export default function DialogueScene({ lines }: Props) {
  if (!lines || lines.length === 0) return null

  return (
    <section className="flex flex-col gap-4">
      {lines.map((line, i) => (
        <DialogueBubble key={i} character={line.character} text={line.text} />
      ))}
    </section>
  )
}
