interface Props {
  code: string
  filename?: string
}

export default function CodePanel({ code, filename = 'engraving.py' }: Props) {
  return (
    <div
      className="rounded-xl overflow-hidden"
      style={{
        background: '#0d0c14',
        border: '1px solid rgba(0,212,170,0.2)',
      }}
    >
      {/* Header */}
      <div
        className="px-3.5 py-2 flex items-center gap-2 text-[10px] font-semibold"
        style={{
          background: 'rgba(0,212,170,0.05)',
          borderBottom: '1px solid rgba(0,212,170,0.1)',
          color: '#00d4aa',
        }}
      >
        <span
          className="w-2 h-2 rounded-full"
          style={{ background: '#c9a227' }}
        />
        {filename}
      </div>
      {/* Body */}
      <div className="p-3.5 font-mono text-xs leading-relaxed" style={{ color: '#e8e6f0' }}>
        {code.split('\n').map((line, i) => (
          <div key={i} className="flex gap-3">
            <span className="shrink-0" style={{ color: '#6b7280' }}>{i + 1}</span>
            <span className="whitespace-pre">{highlightSteampunk(line)}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function highlightSteampunk(line: string): React.ReactNode {
  const tokens: { start: number; end: number; color: string }[] = []

  // 1. Comments
  const commentRe = /#.*/g
  let m: RegExpExecArray | null
  while ((m = commentRe.exec(line)) !== null) {
    tokens.push({ start: m.index, end: m.index + m[0].length, color: '#6b7280' })
  }

  // 2. Strings
  const strRe = /"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/g
  while ((m = strRe.exec(line)) !== null) {
    if (!tokens.some(t => m!.index >= t.start && m!.index < t.end))
      tokens.push({ start: m.index, end: m.index + m[0].length, color: '#4ade80' })
  }

  // 3. Numbers
  const numRe = /\b\d+(\.\d+)?\b/g
  while ((m = numRe.exec(line)) !== null) {
    if (!tokens.some(t => m!.index >= t.start && m!.index < t.end))
      tokens.push({ start: m.index, end: m.index + m[0].length, color: '#b5cea8' })
  }

  // 4. Keywords
  const kwRe = /\b(print|input|if|else|elif|for|while|def|return|in|range|True|False|None|and|or|not|import|from|class|pass|break|continue)\b/g
  while ((m = kwRe.exec(line)) !== null) {
    if (!tokens.some(t => m!.index >= t.start && m!.index < t.end))
      tokens.push({ start: m.index, end: m.index + m[0].length, color: '#c084fc' })
  }

  // 5. Function calls
  const funcRe = /\b([a-zA-Z_]\w*)\s*(?=\()/g
  while ((m = funcRe.exec(line)) !== null) {
    if (!tokens.some(t => m!.index >= t.start && m!.index < t.end))
      tokens.push({ start: m.index, end: m.index + m[1].length, color: '#60a5fa' })
  }

  tokens.sort((a, b) => a.start - b.start)
  const segments: { text: string; color: string }[] = []
  let pos = 0
  for (const tok of tokens) {
    if (tok.start > pos) segments.push({ text: line.slice(pos, tok.start), color: '#e8e6f0' })
    segments.push({ text: line.slice(tok.start, tok.end), color: tok.color })
    pos = tok.end
  }
  if (pos < line.length) segments.push({ text: line.slice(pos), color: '#e8e6f0' })
  if (segments.length === 0) return <span style={{ color: '#e8e6f0' }}>{line}</span>
  return segments.map((s, i) => <span key={i} style={{ color: s.color }}>{s.text}</span>)
}
