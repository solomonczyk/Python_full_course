import { useState, useRef, useEffect } from 'react'
import { CHARACTER_AVATARS } from '../constants'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface Props {
  lessonId?: string
}

export default function ChatWidget({ lessonId }: Props = {}) {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Привет! Я — Python-эксперт из Python Quest. Спрашивай по темам курса: синтаксис, ошибки, примеры. Отвечаю коротко и по делу.' },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const listRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight
    }
  }, [messages])

  const INJECTION_BLOCKS = [
    'ignore all', 'ignore previous', 'forget', 'you are an ai', 'you are a chatbot',
    'disregard', 'system prompt', 'new instructions', 'override',
  ]

  const handleSend = async () => {
    let text = input.trim()
    if (!text || loading) return

    // Client-side injection guard
    const msgLower = text.toLowerCase()
    if (INJECTION_BLOCKS.some(kw => msgLower.includes(kw))) {
      setMessages((prev) => [...prev, { role: 'user', content: text }])
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Я отвечаю только на вопросы по Python в рамках курса Python Quest. Если у тебя вопрос по теме урока — задай его прямо.' }])
      setInput('')
      return
    }
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setLoading(true)

    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, lesson_id: lessonId ?? null }),
      })
      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Ошибка соединения. Проверь, запущен ли сервер.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      {/* Floating button with hover tooltip */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-2 group/chat">
        <div className={`bg-white rounded-xl shadow-lg border border-outline-variant px-4 py-3 max-w-[250px] relative transition-all duration-200
          ${open ? 'opacity-0 pointer-events-none' : 'opacity-0 group-hover/chat:opacity-100'}`}>
          <p className="font-sans text-[13px] leading-[18px] text-on-surface">
            <span className="font-bold text-primary">Ва:</span> Нажимай, только если сам не можешь решить задание 😉
          </p>
          <div className="absolute -bottom-2 right-6 w-3 h-3 bg-white border-r border-b border-outline-variant rotate-45" />
        </div>
        <button
          onClick={() => setOpen((v) => !v)}
          className="w-14 h-14 rounded-full bg-primary shadow-xl hover:scale-105 active:scale-95 transition-all overflow-hidden border-2 border-white ring-2 ring-primary/30 relative"
          aria-label={open ? 'Закрыть чат' : 'Открыть чат'}
        >
          <img
            src={CHARACTER_AVATARS.va}
            alt="Python Expert"
            className="w-full h-full object-cover"
          />
        </button>
      </div>

      {/* Chat panel */}
      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-[360px] max-h-[520px] bg-white rounded-2xl shadow-2xl border border-outline-variant flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-primary text-on-primary px-4 py-3 flex items-center gap-3 shrink-0">
            <div className="w-8 h-8 rounded-full overflow-hidden border-2 border-white/50 shrink-0">
              <img src={CHARACTER_AVATARS.va} alt="Ва" className="w-full h-full object-cover" />
            </div>
            <div className="min-w-0">
              <p className="font-sans text-[14px] font-bold">Python Expert</p>
              <p className="font-sans text-[11px] opacity-80">Ва — магистр логики</p>
            </div>
          </div>

          {/* Messages */}
          <div ref={listRef} className="flex-1 overflow-y-auto p-4 space-y-3 bg-surface-soft" style={{ maxHeight: '360px' }}>
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] px-3 py-2 rounded-2xl text-[14px] leading-5 font-sans ${
                    msg.role === 'user'
                      ? 'bg-primary-container text-on-primary-container rounded-br-md'
                      : 'bg-white border border-outline-variant text-on-surface rounded-bl-md'
                  }`}
                >
                  {msg.content.split('\n').map((line, j) => (
                    <span key={j}>
                      {j > 0 && <br />}
                      {line}
                    </span>
                  ))}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white border border-outline-variant px-3 py-2 rounded-2xl rounded-bl-md text-[14px] text-on-surface-variant flex items-center gap-1">
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-outline-variant p-3 bg-white shrink-0">
            <div className="flex items-end gap-2">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Спросить про Python..."
                rows={1}
                className="flex-1 resize-none rounded-xl border border-outline-variant px-3 py-2 font-sans text-[14px] focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                style={{ minHeight: '36px', maxHeight: '80px' }}
              />
              <button
                onClick={handleSend}
                disabled={loading || !input.trim()}
                className="w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center shrink-0 disabled:opacity-40 hover:scale-105 active:scale-95 transition-all"
              >
                <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>send</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
