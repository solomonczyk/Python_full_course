import { useState } from 'react'
import CodePlayground from './CodePlayground'

interface Props {
  code: string
  output?: string
  filename?: string
  runnable?: boolean
}

export default function CodeBlock({ code, output, filename = 'python-quest.py', runnable = false }: Props) {
  const [copied, setCopied] = useState(false)

  if (runnable) {
    return <CodePlayground initialCode={code} fileName={filename} />
  }

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
  type Token = { start: number; end: number; color: string }
  const tokens: Token[] = []

  // 1. Comments (highest priority — match first, prevent other matches inside)
  const commentRe = /#.*/g
  let m: RegExpExecArray | null
  while ((m = commentRe.exec(line)) !== null) {
    // Check the # is not inside a string — handled by ordering (strings matched first below)
    tokens.push({ start: m.index, end: m.index + m[0].length, color: '#6A9955' })
  }

  // 2. Strings — triple quotes first, then single/double
  const strRe = /"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/g
  while ((m = strRe.exec(line)) !== null) {
    if (!tokens.some(t => m!.index >= t.start && m!.index < t.end)) {
      tokens.push({ start: m.index, end: m.index + m[0].length, color: '#ce9178' })
    }
  }

  // 3. Numbers
  const numRe = /\b\d+(\.\d+)?\b/g
  while ((m = numRe.exec(line)) !== null) {
    if (!tokens.some(t => m!.index >= t.start && m!.index < t.end)) {
      tokens.push({ start: m.index, end: m.index + m[0].length, color: '#b5cea8' })
    }
  }

  // 4. Keywords (only outside strings and comments)
  const kwRe = /\b(print|input|if|else|elif|for|while|def|return|in|range|True|False|None|and|or|not|import|from|class|pass|break|continue|lambda|with|as|try|except|finally|raise|yield|global|nonlocal|del|assert|is)\b/g
  while ((m = kwRe.exec(line)) !== null) {
    if (!tokens.some(t => m!.index >= t.start && m!.index < t.end)) {
      tokens.push({ start: m.index, end: m.index + m[0].length, color: '#c586c0' })
    }
  }

  // 5. Function calls (identifier before parenthesis)
  const funcRe = /\b([a-zA-Z_]\w*)\s*(?=\()/g
  while ((m = funcRe.exec(line)) !== null) {
    if (!tokens.some(t => m!.index >= t.start && m!.index < t.end)) {
      tokens.push({ start: m.index, end: m.index + m[1].length, color: '#dcdcaa' })
    }
  }

  // Sort tokens by position
  tokens.sort((a, b) => a.start - b.start)
  const segments: { text: string; color: string }[] = []
  let pos = 0
  for (const tok of tokens) {
    if (tok.start > pos) segments.push({ text: line.slice(pos, tok.start), color: '#9cdcfe' })
    segments.push({ text: line.slice(tok.start, tok.end), color: tok.color })
    pos = tok.end
  }
  if (pos < line.length) segments.push({ text: line.slice(pos), color: '#9cdcfe' })
  if (segments.length === 0) return <span style={{ color: '#9cdcfe' }}>{line}</span>
  return segments.map((s, i) => <span key={i} style={{ color: s.color }}>{s.text}</span>)
}
