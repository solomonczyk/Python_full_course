import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuest } from '../hooks/useApi'
import { getUserId } from '../utils/userId'
import { usePageMeta } from '../hooks/usePageMeta'

const PART_LABELS: Record<number, string> = {
  1: 'Hello Python',
  2: 'Data Magic',
  3: 'The Logic Gate',
  4: 'Loop Labyrinth',
  5: 'Constructs',
}

const PART_RECAPS: Record<number, string> = {
  1: 'recap-1',
  2: 'recap-2',
  3: 'recap-3',
  4: 'recap-4',
  5: 'recap-5',
}

export default function QuestPage() {
  const { id } = useParams<{ id: string }>()
  const { quest, loading, error } = useQuest(id || '')

  usePageMeta({
    title: quest ? `${quest.title}` : 'Испытание',
    description: quest ? quest.story.slice(0, 160) : 'Финальное испытание',
  })

  const [code, setCode] = useState('')
  const [showHints, setShowHints] = useState(false)
  const [showSolution, setShowSolution] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [checking, setChecking] = useState(false)

  // Set starter code when quest loads
  if (quest && !code && quest.starter_code) {
    setCode(quest.starter_code)
  }

  const handleCheck = async () => {
    if (!code.trim() || !quest) return
    setChecking(true)
    setResult(null)
    try {
      const res = await fetch('/api/mission/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': getUserId(),
        },
        body: JSON.stringify({
          lesson_id: quest.required_lessons[0] || '1-1',
          code: code,
        }),
      })
      const data = await res.json()
      setResult(data)
    } catch (e: any) {
      setResult({ correct: false, error: e.message || 'Ошибка проверки' })
    }
    setChecking(false)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin w-6 h-6 border-2 border-emerald-400 border-t-transparent rounded-full" />
      </div>
    )
  }

  if (error || !quest) {
    return (
      <div className="text-center py-20">
        <p className="text-sm" style={{ color: '#ff6b6b' }}>Испытание не найдено</p>
        <Link to="/" className="text-xs mt-3 inline-block" style={{ color: '#00d4aa' }}>
          ← Вернуться на главную
        </Link>
      </div>
    )
  }

  const recapId = PART_RECAPS[quest.part]

  return (
    <div className="py-6">
      {/* Header */}
      <div
        className="rounded-xl p-5 mb-6"
        style={{
          background: 'linear-gradient(135deg, rgba(255,107,107,0.1), rgba(255,107,107,0.02))',
          border: '1px solid rgba(255,107,107,0.25)',
        }}
      >
        <div className="flex items-center gap-2 mb-1">
          <span className="material-symbols-outlined text-xl" style={{ color: '#ff7675' }}>
            swords
          </span>
          <span className="text-[10px] font-bold uppercase tracking-wider" style={{ color: '#ff7675' }}>
            QUEST · Part {quest.part}: {PART_LABELS[quest.part] ?? ''}
          </span>
        </div>
        <h1 className="text-lg font-bold mt-1" style={{ color: '#e8e6f0' }}>⚔️ {quest.title}</h1>
      </div>

      {/* Story */}
      <div
        className="rounded-xl p-4 mb-5"
        style={{
          background: 'rgba(15,14,23,0.6)',
          border: '1px solid rgba(255,107,107,0.1)',
        }}
      >
        <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#9b98a8' }}>
          📖 История
        </h3>
        <p className="text-xs leading-relaxed" style={{ color: '#c4c2d0' }}>
          {quest.story}
        </p>
      </div>

      {/* Required lessons */}
      <div className="mb-5">
        <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#9b98a8' }}>
          📚 Требуемые уроки
        </h3>
        <div className="flex flex-wrap gap-1.5">
          {quest.required_lessons.map((lid) => (
            <Link
              key={lid}
              to={`/lesson/${lid}`}
              className="text-[10px] px-2 py-0.5 rounded no-underline transition-all hover:opacity-80"
              style={{
                background: 'rgba(0,212,170,0.1)',
                border: '1px solid rgba(0,212,170,0.2)',
                color: '#00d4aa',
              }}
            >
              {lid}
            </Link>
          ))}
        </div>
      </div>

      {/* Required constructs */}
      <div className="mb-5">
        <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#9b98a8' }}>
          🔧 Нужно использовать
        </h3>
        <div className="flex flex-wrap gap-1.5">
          {quest.required_constructs.map((c, i) => (
            <span
              key={i}
              className="text-[10px] px-2 py-0.5 rounded"
              style={{ background: 'rgba(201,162,39,0.1)', color: '#c9a227' }}
            >
              {c}
            </span>
          ))}
        </div>
      </div>

      {/* Task */}
      <div
        className="rounded-xl p-4 mb-5"
        style={{
          background: 'rgba(0,150,255,0.04)',
          border: '1px solid rgba(0,150,255,0.15)',
        }}
      >
        <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#5b9aff' }}>
          🎯 Задание
        </h3>
        <pre
          className="text-xs leading-relaxed whitespace-pre-wrap font-sans"
          style={{ color: '#c4c2d0' }}
        >
          {quest.task}
        </pre>
      </div>

      {/* Code editor */}
      <div
        className="rounded-xl overflow-hidden mb-4"
        style={{
          border: '1px solid rgba(0,212,170,0.2)',
        }}
      >
        <div
          className="px-4 py-2 text-[10px] font-bold uppercase tracking-wider"
          style={{ background: 'rgba(0,212,170,0.08)', color: '#00d4aa', borderBottom: '1px solid rgba(0,212,170,0.1)' }}
        >
          💻 Редактор кода
        </div>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="w-full min-h-[180px] p-4 text-xs leading-relaxed outline-none resize-y"
          style={{
            background: '#0a0910',
            color: '#7ee8d4',
            fontFamily: "'JetBrains Mono', monospace",
            border: 'none',
          }}
          placeholder="# Напиши свой код здесь"
          spellCheck={false}
        />
      </div>

      {/* Check button */}
      <div className="flex items-center gap-3 mb-5">
        <button
          onClick={handleCheck}
          disabled={checking || !code.trim()}
          className="text-xs px-4 py-2.5 rounded-lg font-bold border-none cursor-pointer transition-all disabled:opacity-40"
          style={{
            background: checking ? 'rgba(0,212,170,0.3)' : 'linear-gradient(135deg, #00d4aa, #00a88a)',
            color: '#0f0e17',
          }}
        >
          {checking ? 'Проверка...' : '🚀 Проверить'}
        </button>

        <button
          onClick={() => setShowHints(!showHints)}
          className="text-xs px-3 py-2 rounded-lg border-none cursor-pointer transition-all"
          style={{
            background: 'rgba(201,162,39,0.1)',
            border: '1px solid rgba(201,162,39,0.2)',
            color: '#c9a227',
          }}
        >
          💡 Подсказки {showHints ? '▲' : '▼'}
        </button>

        <button
          onClick={() => setShowSolution(!showSolution)}
          className="text-xs px-3 py-2 rounded-lg border-none cursor-pointer transition-all"
          style={{
            background: 'rgba(255,107,107,0.1)',
            border: '1px solid rgba(255,107,107,0.2)',
            color: '#ff7675',
          }}
        >
          👀 Решение {showSolution ? '▲' : '▼'}
        </button>
      </div>

      {/* Hints */}
      {showHints && quest.hints && quest.hints.length > 0 && (
        <div
          className="rounded-xl p-4 mb-5"
          style={{
            background: 'rgba(201,162,39,0.04)',
            border: '1px solid rgba(201,162,39,0.1)',
          }}
        >
          <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#c9a227' }}>
            💡 Подсказки
          </h3>
          <ul className="space-y-1.5">
            {quest.hints.map((hint, i) => (
              <li key={i} className="flex items-start gap-2 text-xs" style={{ color: '#c4c2d0' }}>
                <span style={{ color: '#ffd700' }}>{i + 1}.</span>
                <span>{hint}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Example solution */}
      {showSolution && quest.example_solution && (
        <div
          className="rounded-xl p-4 mb-5"
          style={{
            background: 'rgba(255,107,107,0.04)',
            border: '1px solid rgba(255,107,107,0.1)',
          }}
        >
          <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#ff7675' }}>
            👀 Пример решения (после своей попытки)
          </h3>
          <pre
            className="text-xs p-3 rounded-lg overflow-x-auto"
            style={{
              background: '#0a0910',
              border: '1px solid rgba(255,107,107,0.1)',
              color: '#ffb3b3',
              fontFamily: "'JetBrains Mono', monospace",
            }}
          >
            {quest.example_solution}
          </pre>
        </div>
      )}

      {/* Result feedback */}
      {result && (
        <div
          className="rounded-xl p-4 mb-5"
          style={{
            background: result.finally_correct || result.correct
              ? 'rgba(0,212,170,0.06)'
              : 'rgba(255,107,107,0.06)',
            border: `1px solid ${
              result.finally_correct || result.correct
                ? 'rgba(0,212,170,0.2)'
                : 'rgba(255,107,107,0.2)'
            }`,
          }}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="material-symbols-outlined" style={{ color: result.finally_correct || result.correct ? '#00d4aa' : '#ff6b6b' }}>
              {result.finally_correct || result.correct ? 'check_circle' : 'error'}
            </span>
            <span className="text-xs font-bold" style={{ color: result.finally_correct || result.correct ? '#00d4aa' : '#ff6b6b' }}>
              {result.finally_correct || result.correct ? 'Правильно!' : 'Нужно доработать'}
            </span>
          </div>
          {result.error && (
            <p className="text-xs mb-1" style={{ color: '#ffb3b3' }}>⚠️ {result.error}</p>
          )}
          {result.hints && result.hints.length > 0 && (
            <ul className="space-y-0.5">
              {result.hints.map((h: string, i: number) => (
                <li key={i} className="text-xs" style={{ color: '#c4c2d0' }}>
                  {h}
                </li>
              ))}
            </ul>
          )}
          {result.actual_output && (
            <div className="mt-2">
              <p className="text-[10px] font-bold mb-0.5" style={{ color: '#9b98a8' }}>Твой вывод:</p>
              <pre className="text-xs" style={{ color: '#7ee8d4', fontFamily: "'JetBrains Mono', monospace" }}>
                {result.actual_output}
              </pre>
            </div>
          )}
        </div>
      )}

      {/* Success criteria */}
      {quest.success_criteria && quest.success_criteria.length > 0 && (
        <div className="mb-5">
          <h3 className="text-[10px] font-bold uppercase tracking-wider mb-2" style={{ color: '#9b98a8' }}>
            ✅ Критерии успеха
          </h3>
          <ul className="space-y-1">
            {quest.success_criteria.map((criteria, i) => (
              <li key={i} className="flex items-start gap-2 text-xs" style={{ color: '#c4c2d0' }}>
                <span style={{ color: '#00d4aa' }}>✓</span>
                <span>{criteria}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Navigation */}
      <div className="flex flex-wrap gap-3 mt-6">
        {recapId && (
          <Link
            to={`/recap/${recapId}`}
            className="text-xs px-4 py-2.5 rounded-lg font-bold no-underline transition-all hover:opacity-90"
            style={{
              background: 'rgba(201,162,39,0.1)',
              border: '1px solid rgba(201,162,39,0.2)',
              color: '#ffd700',
            }}
          >
            🔄 Повторить напоминалку
          </Link>
        )}
        <Link
          to="/"
          className="text-xs px-4 py-2.5 rounded-lg font-bold no-underline transition-all hover:opacity-90"
          style={{
            background: 'rgba(255,255,255,0.05)',
            border: '1px solid rgba(255,255,255,0.1)',
            color: '#e8e6f0',
          }}
        >
          ← Вернуться к урокам
        </Link>
      </div>
    </div>
  )
}
