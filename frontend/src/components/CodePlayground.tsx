import { useEffect, useRef, useState } from 'react'

interface Props {
  initialCode: string
  fileName?: string
}

export default function CodePlayground({ initialCode, fileName = 'playground.py' }: Props) {
  const [code, setCode] = useState(initialCode)
  const [output, setOutput] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'ready' | 'running'>('idle')
  const [expanded, setExpanded] = useState(false)
  const pyodideRef = useRef<any>(null)
  const scriptLoaded = useRef(false)

  const lineCount = code.split('\n').length
  const collapsedHeight = Math.min(lineCount * 28 + 40, 180)

  // Load Pyodide script once
  useEffect(() => {
    if (scriptLoaded.current) return
    scriptLoaded.current = true
    setStatus('loading')

    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js'
    script.onload = async () => {
      try {
        // @ts-expect-error — Pyodide adds loadPyodide to window
        const pyodide = await window.loadPyodide({
          indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/',
        })
        pyodideRef.current = pyodide
        setStatus('ready')
      } catch {
        setStatus('idle')
      }
    }
    script.onerror = () => {
      setStatus('idle')
      scriptLoaded.current = false
    }
    document.head.appendChild(script)

    return () => {
      // Cleanup not needed — script stays cached
    }
  }, [])

  const runCode = async () => {
    const py = pyodideRef.current
    if (!py) {
      if (status === 'loading') {
        setOutput('⏳ Python всё ещё загружается, подожди...')
      } else {
        setOutput('❌ Python не загрузился. Проверь интернет.')
      }
      return
    }

    setStatus('running')
    setOutput('')

    try {
      // Redirect stdout to capture print() output
      await py.runPython(`
import sys, io as _io
_stdout = _io.StringIO()
sys.stdout = _stdout
      `)

      await py.runPython(code)

      const captured = await py.runPython(`
sys.stdout = sys.__stdout__
_stdout.getvalue()
      `)
      setOutput(captured || '(пустой вывод)')
    } catch (err: any) {
      const msg = err?.message ?? String(err)
      setOutput('❌ ' + msg)
    } finally {
      setStatus('ready')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault()
      runCode()
    }
  }

  return (
    <div
      className="rounded-xl overflow-hidden mt-4"
      style={{
        background: '#0d0c14',
        border: '1px solid rgba(0,212,170,0.2)',
      }}
    >
      {/* Terminal header */}
      <div
        className="flex items-center justify-between px-3 py-1.5"
        style={{
          background: 'rgba(0,212,170,0.05)',
          borderBottom: '1px solid rgba(0,212,170,0.1)',
        }}
      >
        <div className="flex items-center gap-2">
          <div className="flex gap-1">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ff5f56' }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ffbd2e' }} />
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#27c93f' }} />
          </div>
          <span className="text-[10px]" style={{ color: '#9b98a8' }}>{fileName}</span>
          {status === 'loading' && (
            <span className="text-[10px] ml-2" style={{ color: '#c9a227' }}>⏳ Загрузка Python...</span>
          )}
          {status === 'ready' && (
            <span className="text-[10px] ml-2" style={{ color: '#00d4aa' }}>✓ Python готов</span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-[10px] cursor-pointer hover:opacity-80"
            style={{ color: '#9b98a8', background: 'none', border: 'none' }}
          >
            <span className="material-symbols-outlined text-[14px]">
              {expanded ? 'fullscreen_exit' : 'fullscreen'}
            </span>
          </button>
          <button
            onClick={runCode}
            disabled={status === 'loading' || status === 'running'}
            className="flex items-center gap-1 px-3 py-1 rounded text-[10px] font-bold cursor-pointer transition-all hover:scale-105 border-none disabled:opacity-50"
            style={{
              background: status === 'running' ? '#6b7280' : '#00d4aa',
              color: '#0f0e17',
            }}
          >
            <span className="material-symbols-outlined text-[12px]">play_arrow</span>
            {status === 'running' ? 'Запуск...' : 'Запустить'}
          </button>
        </div>
      </div>

      {/* Code area */}
      <div className="relative">
        <div className="flex" style={{ minHeight: expanded ? '400px' : `${collapsedHeight}px` }}>
          <div
            className="p-3 pr-2 text-right font-mono text-xs leading-7 select-none shrink-0"
            style={{ color: '#6b7280', minWidth: '32px' }}
          >
            {code.split('\n').map((_, i) => (
              <div key={i}>{i + 1}</div>
            ))}
            {!code && <div>1</div>}
          </div>
          <textarea
            value={code}
            onChange={(e) => { setCode(e.target.value); setOutput('') }}
            onKeyDown={handleKeyDown}
            className="w-full p-3 pl-2 font-mono text-xs leading-7 resize-none outline-none"
            style={{
              minHeight: expanded ? '400px' : `${collapsedHeight}px`,
              background: '#0d0c14',
              color: '#e8e6f0',
              border: 'none',
            }}
            spellCheck={false}
            placeholder="# Напиши код здесь и нажми Запустить"
          />
        </div>

        {!expanded && lineCount > 6 && (
          <div
            className="absolute bottom-0 left-0 right-0 h-8 pointer-events-none flex items-end justify-center pb-1"
            style={{ background: 'linear-gradient(transparent, rgba(13,12,20,0.9))' }}
          >
            <span className="text-[10px] animate-pulse" style={{ color: '#9b98a8' }}>
              ⋮ скроль или разверни
            </span>
          </div>
        )}
      </div>

      {/* Output */}
      {output && (
        <div
          className="px-4 py-3 font-mono text-xs leading-relaxed whitespace-pre-wrap border-t"
          style={{
            background: output.startsWith('❌') ? 'rgba(255,107,107,0.08)' : 'rgba(0,212,170,0.05)',
            borderColor: output.startsWith('❌') ? 'rgba(255,107,107,0.2)' : 'rgba(0,212,170,0.1)',
            color: output.startsWith('❌') ? '#ff6b6b' : '#00d4aa',
          }}
        >
          <div className="text-[10px] font-bold mb-1 uppercase tracking-wider" style={{ color: '#9b98a8' }}>
            Вывод:
          </div>
          {output}
        </div>
      )}

      {/* Keyboard shortcut hint */}
      {status === 'ready' && (
        <div className="px-3 py-1 text-[9px] text-right" style={{ color: '#6b7280' }}>
          Ctrl+Enter / ⌘+Enter — запуск
        </div>
      )}
    </div>
  )
}
