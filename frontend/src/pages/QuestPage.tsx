import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuest, checkQuest } from '../hooks/useApi'
import { useProgressContext } from '../hooks/ProgressContext'
import CodeBlock from '../components/CodeBlock'

const PART_COLORS: Record<number, string> = {
  1: '#00d4aa',
  2: '#c9a227',
  3: '#ff6b6b',
  4: '#6c5ce7',
  5: '#fd79a8',
}

export default function QuestPage() {
  const { id } = useParams<{ id: string }>()
  const { quest, loading, error } = useQuest(id ?? '')
  const { markComplete } = useProgressContext()
  const [code, setCode] = useState('')
  const [results, setResults] = useState<any>(null)
  const [checking, setChecking] = useState(false)
  const [showHints, setShowHints] = useState(false)
  const [showSolution, setShowSolution] = useState(false)
  const [completed, setCompleted] = useState(false)

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-sm" style={{ color: '#9b98a8' }}>Загрузка квеста...</div>
      </div>
    )
  }

  if (error || !quest) {
    return (
      <div className="rounded-xl p-6" style={{ background: '#1a1924', border: '1px solid rgba(255,107,107,0.3)' }}>
        <p style={{ color: '#ff6b6b' }}>Квест не найден. <Link to="/" style={{ color: '#c9a227' }}>На главную</Link></p>
      </div>
    )
  }

  const partColor = PART_COLORS[quest.part] ?? '#c9a227'

  const handleSubmit = async () => {
    if (!code.trim()) return
    setChecking(true)
    setResults(null)
    try {
      const res = await checkQuest(quest.id, code)
      setResults(res)
      if (res.all_passed) {
        setShowSolution(true)
        setCompleted(true)
        await markComplete(`quest-${quest.id}`)
      }
    } catch (e: any) {
      setResults({ all_passed: false, results: [], error: e.message })
    } finally {
      setChecking(false)
    }
  }

  const handleComplete = async () => {
    setCompleted(true)
    await markComplete(`quest-${quest.id}`)
  }

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link to="/" className="text-xs hover:underline inline-block" style={{ color: '#9b98a8' }}>
        ← На главную
      </Link>

      {/* Header */}
      <div
        className="rounded-xl p-6"
        style={{
          background: '#1a1924',
          border: `1px solid ${partColor}33`,
        }}
      >
        <div className="flex items-center gap-2 mb-2">
          <span
            className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded"
            style={{
              background: `${partColor}22`,
              color: partColor,
              border: `1px solid ${partColor}44`,
            }}
          >
            {quest.is_capstone ? 'CAPSTONE QUEST' : 'PART QUEST'} · Part {quest.part}
          </span>
          {quest.is_capstone && (
            <span className="text-[10px] font-bold px-2 py-0.5 rounded" style={{ background: '#fd79a822', color: '#fd79a8', border: '1px solid #fd79a844' }}>
              ФИНАЛЬНЫЙ
            </span>
          )}
        </div>
        <h1 className="text-lg font-bold" style={{ color: '#e8e6f0' }}>{quest.title}</h1>
      </div>

      {/* Story */}
      <div className="rounded-xl p-4" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.1)' }}>
        <p className="text-xs leading-relaxed" style={{ color: '#b8b6c4' }}>{quest.story}</p>
      </div>

      {/* Required Constructs */}
      <div>
        <div className="flex flex-wrap gap-1.5">
          {quest.required_constructs.map((c) => (
            <span
              key={c}
              className="text-[10px] px-2 py-0.5 rounded"
              style={{
                background: `${partColor}15`,
                color: partColor,
                border: `1px solid ${partColor}33`,
              }}
            >
              {c}
            </span>
          ))}
        </div>
      </div>

      {/* Task */}
      <div className="rounded-xl p-4" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.1)' }}>
        <h3 className="text-xs font-bold mb-2 uppercase tracking-wider" style={{ color: '#c9a227' }}>Задание</h3>
        <pre className="text-xs whitespace-pre-wrap font-sans leading-relaxed" style={{ color: '#b8b6c4' }}>{quest.task}</pre>
      </div>

      {/* Starter Code */}
      <div>
        <h3 className="text-xs font-bold mb-2" style={{ color: '#9b98a8' }}>Стартовый код</h3>
        <CodeBlock code={quest.starter_code} />
      </div>

      {/* Code Editor */}
      <div>
        <h3 className="text-xs font-bold mb-2" style={{ color: '#9b98a8' }}>Твой код</h3>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Напиши свой код здесь..."
          className="w-full rounded-xl p-4 text-xs font-mono leading-relaxed resize-y min-h-[180px] outline-none"
          style={{
            background: '#0f0e17',
            color: '#e8e6f0',
            border: '1px solid rgba(201,162,39,0.15)',
          }}
          spellCheck={false}
        />
      </div>

      {/* Submit Button */}
      <div className="flex gap-3">
        <button
          onClick={handleSubmit}
          disabled={checking || !code.trim()}
          className="px-5 py-2.5 rounded-xl text-xs font-bold cursor-pointer border-none transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed"
          style={{
            background: partColor,
            color: '#0f0e17',
          }}
        >
          {checking ? 'Проверка...' : 'Отправить на проверку'}
        </button>
        {completed && (
          <button
            onClick={handleComplete}
            className="px-5 py-2.5 rounded-xl text-xs font-bold cursor-pointer border-none transition-all hover:scale-[1.02] active:scale-[0.98]"
            style={{
              background: '#00d4aa',
              color: '#0f0e17',
            }}
          >
            ✓ Отметить как пройденный
          </button>
        )}
      </div>

      {/* Results */}
      {results && (
        <div
          className="rounded-xl p-4"
          style={{
            background: '#1a1924',
            border: `1px solid ${results.all_passed ? '#00d4aa44' : '#ff6b6b44'}`,
          }}
        >
          <h3 className="text-xs font-bold mb-3" style={{ color: results.all_passed ? '#00d4aa' : '#ff6b6b' }}>
            {results.all_passed ? '✓ Все тесты пройдены!' : `✗ ${results.results.filter((r: any) => r.passed).length}/${results.results.length} тестов пройдено`}
          </h3>
          {results.error && (
            <p className="text-xs mb-2" style={{ color: '#ff6b6b' }}>{results.error}</p>
          )}
          <div className="space-y-2">
            {results.results.map((r: any, i: number) => (
              <div
                key={i}
                className="rounded-lg p-3 text-xs"
                style={{
                  background: r.passed ? 'rgba(0,212,170,0.05)' : 'rgba(255,107,107,0.05)',
                  border: `1px solid ${r.passed ? 'rgba(0,212,170,0.2)' : 'rgba(255,107,107,0.2)'}`,
                }}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span style={{ color: r.passed ? '#00d4aa' : '#ff6b6b' }}>{r.passed ? '✓' : '✗'}</span>
                  <span className="font-bold" style={{ color: '#e8e6f0' }}>Тест {i + 1}</span>
                  {r.input && <span style={{ color: '#9b98a8' }}>Ввод: {r.input}</span>}
                </div>
                {r.actual_output && (
                  <div className="mt-1">
                    <span style={{ color: '#9b98a8' }}>Вывод: </span>
                    <code style={{ color: '#b8b6c4' }}>{r.actual_output}</code>
                  </div>
                )}
                {r.missing_contains && r.missing_contains.length > 0 && (
                  <div className="mt-1">
                    <span style={{ color: '#ff6b6b' }}>Не найдено: </span>
                    <code style={{ color: '#ff6b6b' }}>{r.missing_contains.join(', ')}</code>
                  </div>
                )}
                {r.error && (
                  <div className="mt-1" style={{ color: '#ff6b6b' }}>Ошибка: {r.error}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Success Criteria */}
      <div className="rounded-xl p-4" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.1)' }}>
        <h3 className="text-xs font-bold mb-2 uppercase tracking-wider" style={{ color: '#c9a227' }}>Критерии успеха</h3>
        <ul className="space-y-1">
          {quest.success_criteria.map((c, i) => (
            <li key={i} className="text-xs flex items-start gap-2" style={{ color: '#b8b6c4' }}>
              <span style={{ color: '#c9a227' }}>◆</span>
              {c}
            </li>
          ))}
        </ul>
      </div>

      {/* Hints */}
      <div>
        <button
          onClick={() => setShowHints(!showHints)}
          className="text-xs font-bold flex items-center gap-2 mb-2 hover:opacity-80"
          style={{ color: '#c9a227' }}
        >
          {showHints ? '▼' : '▶'} Подсказки ({quest.hints.length})
        </button>
        {showHints && (
          <div className="rounded-xl p-4 space-y-2" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.1)' }}>
            {quest.hints.map((h, i) => (
              <p key={i} className="text-xs" style={{ color: '#b8b6c4' }}>
                <span style={{ color: '#c9a227' }}>{i + 1}.</span> {h}
              </p>
            ))}
          </div>
        )}
      </div>

      {/* Example Solution */}
      <div>
        <button
          onClick={() => setShowSolution(!showSolution)}
          className="text-xs font-bold flex items-center gap-2 mb-2 hover:opacity-80"
          style={{ color: results?.all_passed ? '#00d4aa' : '#9b98a8' }}
        >
          {showSolution ? '▼' : '▶'} Пример решения
        </button>
        {showSolution && (
          <div className="rounded-xl overflow-hidden" style={{ border: '1px solid rgba(0,212,170,0.3)' }}>
            <CodeBlock code={quest.example_solution} />
          </div>
        )}
      </div>
    </div>
  )
}
