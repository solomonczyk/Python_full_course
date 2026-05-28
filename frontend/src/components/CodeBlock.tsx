import { useState } from 'react'

interface Props {
  code: string
  output?: string
  filename?: string
}

export default function CodeBlock({ code, output, filename = 'python-quest.py' }: Props) {
  const [copied, setCopied] = useState(false)

  const copy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <section className="bg-[#1e1e1e] rounded-xl overflow-hidden shadow-[0_4px_20px_rgba(0,0,0,0.1)]">
      <div className="bg-[#333] px-4 py-2 flex items-center justify-between">
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
          <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
          <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
        </div>
        <span className="text-[11px] text-gray-400 font-mono uppercase tracking-widest">{filename}</span>
      </div>

      <div className="p-6 font-mono text-[14px] leading-5">
        {code.split('\n').map((line, i) => (
          <div key={i} className="flex gap-4">
            <span className="text-gray-600 select-none w-4 text-right shrink-0">{i + 1}</span>
            <code className="text-white whitespace-pre">{highlightLine(line)}</code>
          </div>
        ))}
      </div>

      {output !== undefined && (
        <div className="border-t border-white/10 px-4 py-3 bg-black/20 flex items-center justify-between">
          <div className="flex items-center gap-2 text-gray-400 text-xs font-mono">
            <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>play_circle</span>
            <span>Результат:</span>
            <span className="text-green-400 whitespace-pre">{output}</span>
          </div>
          <button onClick={copy} className="text-white/60 hover:text-white transition-colors" title="Копировать">
            <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: "'FILL' 0" }}>
              {copied ? 'check' : 'content_copy'}
            </span>
          </button>
        </div>
      )}
    </section>
  )
}

function highlightLine(line: string): React.ReactNode {
  const keywordRe = /\b(print|input|if|else|elif|for|while|def|return|in|range|True|False|None|and|or|not|import|from)\b/g
  const stringRe = /(["'])(?:(?!\1)[^\\]|\\.)*\1/g
  const commentRe = /#.*/g
  const numRe = /\b\d+(\.\d+)?\b/g

  type Segment = { text: string; color: string }
  const segments: Segment[] = []
  let pos = 0

  const ranges: { start: number; end: number; color: string }[] = []

  let m: RegExpExecArray | null
  const re = new RegExp(`${stringRe.source}|${commentRe.source}|${keywordRe.source}|${numRe.source}`, 'g')
  while ((m = re.exec(line)) !== null) {
    const token = m[0]
    const start = m.index
    const end = start + token.length
    let color = 'text-white'
    if (/^["']/.test(token)) color = 'text-[#ce9178]'
    else if (/^#/.test(token)) color = 'text-[#6A9955]'
    else if (/^\d/.test(token)) color = 'text-[#b5cea8]'
    else color = 'text-[#c586c0]'
    ranges.push({ start, end, color })
  }

  for (const range of ranges) {
    if (pos < range.start) {
      segments.push({ text: line.slice(pos, range.start), color: 'text-white' })
    }
    segments.push({ text: line.slice(range.start, range.end), color: range.color })
    pos = range.end
  }
  if (pos < line.length) {
    segments.push({ text: line.slice(pos), color: 'text-white' })
  }

  if (segments.length === 0) return <span className="text-white">{line}</span>
  return segments.map((s, i) => <span key={i} className={s.color}>{s.text}</span>)
}
