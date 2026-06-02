import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useRecap } from '../hooks/useApi'
import { useProgressContext } from '../hooks/ProgressContext'

export default function RecapPage() {
  const { id } = useParams<{ id: string }>()
  const { recap, loading, error } = useRecap(id ?? '')
  const { markComplete } = useProgressContext()
  const [completed, setCompleted] = useState(false)
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [checked, setChecked] = useState<Record<number, boolean | null>>({})
  const [allRevealed, setAllRevealed] = useState(false)

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-sm" style={{ color: '#9b98a8' }}>Загрузка повторения...</div>
      </div>
    )
  }

  if (error || !recap) {
    return (
      <div className="rounded-xl p-6" style={{ background: '#1a1924', border: '1px solid rgba(255,107,107,0.3)' }}>
        <p style={{ color: '#ff6b6b' }}>Повторение не найдено. <Link to="/" style={{ color: '#c9a227' }}>На главную</Link></p>
      </div>
    )
  }

  const isCheckpoint = recap.id.startsWith('recap-3') && recap.id !== 'recap-3'
  const partColor = isCheckpoint ? '#6c5ce7' : '#c9a227'
  const partLabel = isCheckpoint ? 'ЧЕКПОИНТ' : 'RECAP'

  const handleCheckAnswer = (index: number) => {
    const userAnswer = (answers[index] || '').trim().toLowerCase()
    const correctAnswer = recap.mini_check[index].answer.toLowerCase()
    const isCorrect = userAnswer === correctAnswer || correctAnswer.includes(userAnswer) || userAnswer.includes(correctAnswer.substring(0, 10))
    setChecked((prev) => ({ ...prev, [index]: isCorrect }))
  }

  const handleRevealAll = () => {
    setAllRevealed(true)
  }

  const handleComplete = async () => {
    setCompleted(true)
    await markComplete(recap.id)
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
            {partLabel} · Part {recap.part}
          </span>
        </div>
        <h1 className="text-lg font-bold" style={{ color: '#e8e6f0' }}>{recap.title}</h1>
      </div>

      {/* Story Summary */}
      <div className="rounded-xl p-4" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.1)' }}>
        <p className="text-xs leading-relaxed" style={{ color: '#b8b6c4' }}>{recap.story_summary}</p>
      </div>

      {/* Learned Terms */}
      <div>
        <h3 className="text-xs font-bold mb-2 uppercase tracking-wider" style={{ color: '#c9a227' }}>Изученные термины</h3>
        <div className="flex flex-wrap gap-1.5">
          {recap.learned_terms.map((term) => (
            <span
              key={term}
              className="text-[10px] px-2 py-0.5 rounded"
              style={{
                background: 'rgba(0,212,170,0.1)',
                color: '#00d4aa',
                border: '1px solid rgba(0,212,170,0.2)',
              }}
            >
              {term}
            </span>
          ))}
        </div>
      </div>

      {/* Hero Skills */}
      <div>
        <h3 className="text-xs font-bold mb-2 uppercase tracking-wider" style={{ color: '#c9a227' }}>Навыки героя</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {recap.hero_skills.map((skill, i) => (
            <div
              key={i}
              className="rounded-xl p-3"
              style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.1)' }}
            >
              <h4 className="text-xs font-bold mb-1" style={{ color: '#e8e6f0' }}>{skill.name}</h4>
              <code className="text-[11px] block mb-1" style={{ color: '#c9a227' }}>{skill.python}</code>
              <p className="text-[10px]" style={{ color: '#9b98a8' }}>{skill.meaning}</p>
              <p className="text-[10px] italic mt-1" style={{ color: '#6b6878' }}>{skill.analogy}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Key Rules */}
      <div className="rounded-xl p-4" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.1)' }}>
        <h3 className="text-xs font-bold mb-2 uppercase tracking-wider" style={{ color: '#c9a227' }}>Ключевые правила</h3>
        <ul className="space-y-1">
          {recap.key_rules.map((rule, i) => (
            <li key={i} className="text-xs flex items-start gap-2" style={{ color: '#b8b6c4' }}>
              <span style={{ color: '#c9a227', fontSize: '8px' }}>◆</span>
              {rule}
            </li>
          ))}
        </ul>
      </div>

      {/* Mini Check */}
      <div className="rounded-xl p-4" style={{ background: '#1a1924', border: '1px solid rgba(108,92,231,0.3)' }}>
        <h3 className="text-xs font-bold mb-3 uppercase tracking-wider" style={{ color: '#6c5ce7' }}>Мини-проверка</h3>
        <div className="space-y-4">
          {recap.mini_check.map((item, i) => (
            <div key={i} className="rounded-lg p-3" style={{ background: '#0f0e17', border: '1px solid rgba(108,92,231,0.15)' }}>
              <p className="text-xs font-bold mb-2" style={{ color: '#e8e6f0' }}>{item.question}</p>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={answers[i] || ''}
                  onChange={(e) => setAnswers((prev) => ({ ...prev, [i]: e.target.value }))}
                  placeholder="Твой ответ..."
                  className="flex-1 rounded-lg px-3 py-1.5 text-xs outline-none"
                  style={{
                    background: '#1a1924',
                    color: '#e8e6f0',
                    border: '1px solid rgba(108,92,231,0.2)',
                  }}
                />
                <button
                  onClick={() => handleCheckAnswer(i)}
                  className="px-3 py-1.5 rounded-lg text-xs font-bold cursor-pointer border-none hover:opacity-80"
                  style={{ background: '#6c5ce7', color: '#fff' }}
                >
                  Проверить
                </button>
              </div>
              {checked[i] !== undefined && (
                <p className="text-xs mt-1" style={{ color: checked[i] ? '#00d4aa' : '#ff6b6b' }}>
                  {checked[i] ? '✓ Верно!' : '✗ Попробуй ещё раз'}
                </p>
              )}
              {(allRevealed || checked[i]) && (
                <p className="text-xs mt-1" style={{ color: '#9b98a8' }}>
                  <span style={{ color: '#6c5ce7' }}>Ответ: </span>{item.answer}
                </p>
              )}
            </div>
          ))}
        </div>
        <button
          onClick={handleRevealAll}
          className="mt-3 text-xs hover:underline"
          style={{ color: '#9b98a8' }}
        >
          Показать все ответы
        </button>
      </div>

      {/* Complete Button */}
      {!completed && (
        <button
          onClick={handleComplete}
          className="px-5 py-2.5 rounded-xl text-xs font-bold cursor-pointer border-none transition-all hover:scale-[1.02] active:scale-[0.98]"
          style={{
            background: '#c9a227',
            color: '#0f0e17',
          }}
        >
          ✓ Отметить как пройдено
        </button>
      )}
      {completed && (
        <div className="rounded-xl p-4 text-xs font-bold text-center" style={{ background: 'rgba(0,212,170,0.1)', border: '1px solid rgba(0,212,170,0.3)', color: '#00d4aa' }}>
          ✓ Повторение пройдено
        </div>
      )}
    </div>
  )
}
