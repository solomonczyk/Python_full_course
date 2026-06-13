import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useRecap } from '../hooks/useApi'
import { useProgressContext } from '../hooks/ProgressContext'
import DialogueBubble from '../components/DialogueBubble'
import ComicPanel from '../components/ComicPanel'
import CharacterGrowthCard from '../components/CharacterGrowthCard'
import type { Character, LessonSummary, Lesson } from '../types'

// ── New recap format rendering (from lessons.json) ──────────────────────

interface NewRecapProps {
  lesson: Lesson
  lessons: LessonSummary[]
}

function NewRecapView({ lesson, lessons }: NewRecapProps) {
  const { markComplete } = useProgressContext()
  const [completed, setCompleted] = useState(false)
  const [code, setCode] = useState('')
  const [output, setOutput] = useState<string | null>(null)
  const [checking, setChecking] = useState(false)
  const [passed, setPassed] = useState(false)

  const finalTask = lesson.final_task
  const recapSteps = lesson.recap_steps
  const narrator = lesson.narrator || 'da'
  const storyScene = lesson.story_scene || ''

  const handleCheck = async () => {
    if (!code.trim() || !finalTask) return
    setChecking(true)
    try {
      const res = await fetch('/api/mission/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lesson_id: lesson.id, code }),
      })
      const data = await res.json()
      setOutput(data.actual_output ?? data.error ?? '—')
      setPassed(data.correct === true)
    } catch {
      setOutput('Ошибка проверки')
    } finally {
      setChecking(false)
    }
  }

  const handleComplete = async () => {
    setCompleted(true)
    await markComplete(lesson.id)
  }

  // Count complete among lessons in this part
  const partLessons = lessons.filter(l => l.part === lesson.part)
  const completedInPart = lessons.filter(l => l.part === lesson.part).length // placeholder
  const partTotal = partLessons.length

  return (
    <div className="space-y-6">
      {/* Header */}
      <div
        className="rounded-xl p-6"
        style={{
          background: '#1a1924',
          border: '1px solid rgba(201,162,39,0.3)',
        }}
      >
        <div className="flex items-center gap-2 mb-2">
          <span
            className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded"
            style={{
              background: 'rgba(201,162,39,0.15)',
              color: '#c9a227',
              border: '1px solid rgba(201,162,39,0.3)',
            }}
          >
            RECAP · Chapter {lesson.part}
          </span>
        </div>
        <h1 className="text-lg font-bold" style={{ color: '#e8e6f0' }}>{lesson.title}</h1>
      </div>

      {/* Story scene — narrated by Da (or other narrator) */}
      {storyScene && (
        <ComicPanel
          character={narrator}
          emotion="proud"
          text={storyScene}
          position="hook"
        />
      )}

      {/* Recap steps */}
      {recapSteps && recapSteps.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider" style={{ color: '#c9a227' }}>
            Что теперь умеет игра
          </h3>
          {recapSteps.map((step, i) => (
            <div
              key={i}
              className="rounded-xl p-4"
              style={{
                background: '#1a1924',
                border: '1px solid rgba(201,162,39,0.1)',
              }}
            >
              <div className="flex items-center gap-2 mb-2">
                <span
                  className="text-[10px] px-2 py-0.5 rounded-full"
                  style={{
                    background: 'rgba(0,212,170,0.1)',
                    color: '#00d4aa',
                    border: '1px solid rgba(0,212,170,0.2)',
                  }}
                >
                  {step.skill}
                </span>
                <span
                  className="text-[10px]"
                  style={{ color: '#9b98a8' }}
                >
                  Урок {step.lesson_ref}
                </span>
              </div>
              <p className="text-xs leading-relaxed mb-2" style={{ color: '#b8b6c4' }}>
                {step.reminder}
              </p>
              <div
                className="rounded-lg p-3"
                style={{
                  background: 'rgba(201,162,39,0.05)',
                  border: '1px dashed rgba(201,162,39,0.2)',
                }}
              >
                <span className="text-[10px] font-bold uppercase" style={{ color: '#c9a227' }}>
                  Мини-задача:
                </span>
                <p className="text-xs mt-1" style={{ color: '#e8e6f0' }}>
                  {step.mini_task}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Final task */}
      {finalTask && (
        <div
          className="rounded-xl p-4"
          style={{
            background: '#1a1924',
            border: '1px solid rgba(0,212,170,0.3)',
          }}
        >
          <h3 className="text-xs font-bold mb-2 uppercase tracking-wider" style={{ color: '#00d4aa' }}>
            Финальная задача
          </h3>
          <p className="text-xs leading-relaxed mb-3" style={{ color: '#b8b6c4' }}>
            {finalTask.description}
          </p>

          <div
            className="rounded-xl overflow-hidden"
            style={{
              background: '#0d0c14',
              border: '1px solid rgba(0,212,170,0.2)',
            }}
          >
            {/* Terminal header */}
            <div
              className="flex items-center px-3 py-1.5"
              style={{
                background: 'rgba(0,212,170,0.05)',
                borderBottom: '1px solid rgba(0,212,170,0.1)',
              }}
            >
              <div className="flex gap-1">
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ff5f56' }} />
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ffbd2e' }} />
                <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#27c93f' }} />
              </div>
              <span className="text-[10px] ml-2" style={{ color: '#9b98a8' }}>final_mission.py</span>
            </div>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full p-4 font-mono text-xs leading-relaxed resize-none outline-none"
              style={{
                minHeight: '120px',
                background: '#0d0c14',
                color: '#e8e6f0',
                border: 'none',
              }}
              spellCheck={false}
              placeholder="# Напиши свой код здесь..."
            />
          </div>

          <div className="flex gap-2 mt-3">
            <button
              onClick={handleCheck}
              disabled={checking || !code.trim()}
              className="px-4 py-2 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:opacity-80 disabled:opacity-50"
              style={{ background: '#00d4aa', color: '#0f0e17' }}
            >
              {checking ? 'Проверяю...' : 'Проверить'}
            </button>
          </div>

          {output !== null && (
            <div
              className="mt-3 rounded-lg p-3"
              style={{
                background: passed ? 'rgba(0,212,170,0.1)' : 'rgba(255,107,107,0.1)',
                border: `1px solid ${passed ? 'rgba(0,212,170,0.3)' : 'rgba(255,107,107,0.3)'}`,
              }}
            >
              <div className="flex items-center gap-2 mb-1">
                <span
                  className="material-symbols-outlined text-sm"
                  style={{
                    color: passed ? '#00d4aa' : '#ff6b6b',
                    fontVariationSettings: "'FILL' 1",
                  }}
                >
                  {passed ? 'check_circle' : 'error'}
                </span>
                <span className="text-xs font-bold" style={{ color: passed ? '#00d4aa' : '#ff6b6b' }}>
                  {passed ? 'Пройдено!' : 'Попробуй ещё раз'}
                </span>
              </div>
              {!passed && (
                <>
                  <p className="text-[10px]" style={{ color: '#9b98a8' }}>
                    Твой вывод: <code style={{ color: '#ff6b6b' }}>{output}</code>
                  </p>
                  <p className="text-[10px]" style={{ color: '#9b98a8' }}>
                    Ожидается: <code style={{ color: '#00d4aa' }}>{finalTask.expected_output}</code>
                  </p>
                </>
              )}
            </div>
          )}
        </div>
      )}

      {/* Character Growth — Malek's internal monologue at end of part */}
      {lesson.character_growth && (
        <CharacterGrowthCard characterGrowth={lesson.character_growth} />
      )}

      {/* Complete button */}
      {!completed && (
        <button
          onClick={handleComplete}
          className="px-5 py-2.5 rounded-xl text-xs font-bold cursor-pointer border-none transition-all hover:scale-[1.02] active:scale-[0.98]"
          style={{ background: '#c9a227', color: '#0f0e17' }}
        >
          ✓ Отметить как пройдено
        </button>
      )}
      {completed && (
        <div
          className="rounded-xl p-4 text-xs font-bold text-center"
          style={{
            background: 'rgba(0,212,170,0.1)',
            border: '1px solid rgba(0,212,170,0.3)',
            color: '#00d4aa',
          }}
        >
          ✓ Глава пройдена — игра растёт!
        </div>
      )}
    </div>
  )
}

// ── Existing recap format rendering (from recaps.json) ─────────────────

function OldRecapView() {
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
              {checked[i] !== undefined && (
                <div className="mt-2">
                  {checked[i] ? (
                    <DialogueBubble character="novice" text="Верно! Я это запомнил." />
                  ) : (
                    <DialogueBubble character="va" text="Не совсем. Попробуй ещё раз — подумай, что мы проходили в этой части." />
                  )}
                </div>
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

      {/* Character Growth — Malek's internal monologue */}
      {recap.character_growth && (
        <CharacterGrowthCard characterGrowth={recap.character_growth} />
      )}

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

// ── Main RecapPage — dispatches to old or new format ────────────────────

interface RecapPageProps {
  lesson?: Lesson
  lessons?: LessonSummary[]
}

export default function RecapPage({ lesson, lessons }: RecapPageProps = {}) {
  const { id } = useParams<{ id: string }>()

  // If we received a lesson prop (from LessonPage recap detection), render new format
  if (lesson) {
    return <NewRecapView lesson={lesson} lessons={lessons ?? []} />
  }

  // Otherwise, use the old recap system (route: /recap/:id)
  return <OldRecapView />
}
