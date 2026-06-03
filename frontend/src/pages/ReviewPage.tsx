import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useReview } from '../hooks/useApi'
import { useProgressContext } from '../hooks/ProgressContext'
import DialogueBubble from '../components/DialogueBubble'
import CharacterAvatar from '../components/CharacterAvatar'
import PredictOutputBlock from '../components/PredictOutputBlock'
import FindBugBlock from '../components/FindBugBlock'
import type { ReviewBlock } from '../types'

const REVIEW_COLORS: Record<string, { bg: string; border: string; label: string }> = {
  quick_recall: { bg: 'bg-cyan-50', border: 'border-cyan-400', label: 'БЫСТРОЕ ПОВТОРЕНИЕ' },
  chapter_review: { bg: 'bg-violet-50', border: 'border-violet-400', label: 'ПОВТОРЕНИЕ ГЛАВЫ' },
  boss_review: { bg: 'bg-amber-50', border: 'border-amber-500', label: 'ПРОВЕРКА ПЕРЕД МИНИ-ИГРОЙ' },
  part_review: { bg: 'bg-rose-50', border: 'border-rose-400', label: 'ФИНАЛЬНОЕ ПОВТОРЕНИЕ ЧАСТИ' },
}

export default function ReviewPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { review, loading, error } = useReview(id ?? '')
  const { markComplete } = useProgressContext()
  const [quizAnswers, setQuizAnswers] = useState<Record<string, string>>({})
  const [quizResults, setQuizResults] = useState<Record<string, { correct: boolean; correct_id: string }>>({})
  const [outputResult, setOutputResult] = useState<{ correct: boolean; correct_answer: string } | null>(null)
  const [completed, setCompleted] = useState(false)
  const [hasInteracted, setHasInteracted] = useState(false)

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [id])

  // Scroll to top when review data loads (catches async fetch completion)
  useEffect(() => {
    if (review) window.scrollTo(0, 0)
  }, [review?.id])

  if (loading) {
    return (
      <div className="w-full max-w-[800px] flex items-center justify-center h-64">
        <div className="flex flex-col items-center gap-4" style={{ color: '#9b98a8' }}>
          <span className="material-symbols-outlined text-5xl animate-spin" style={{ fontVariationSettings: "'FILL' 0" }}>progress_activity</span>
          <p className="text-sm">Загрузка повторения...</p>
        </div>
      </div>
    )
  }

  if (error || !review) {
    return (
      <div className="w-full max-w-[800px] flex items-center justify-center h-64">
        <div className="text-center" style={{ color: '#ff6b6b' }}>
          <span className="material-symbols-outlined text-5xl block mb-2" style={{ fontVariationSettings: "'FILL' 0" }}>error</span>
          <p>{error ?? 'Review not found'}</p>
        </div>
      </div>
    )
  }

  const colors = REVIEW_COLORS[review.type] ?? { bg: 'bg-surface-container', border: 'border-outline', label: 'ПОВТОРЕНИЕ' }
  const allQuizAnswered = review.questions.every((q) => quizAnswers[q.question] != null)
  const allDone = allQuizAnswered && (outputResult != null || !review.what_outputs)

  const handleQuiz = (question: string, optId: string, correctId: string) => {
    setHasInteracted(true)
    setQuizAnswers((prev) => ({ ...prev, [question]: optId }))
    setQuizResults((prev) => ({
      ...prev,
      [question]: { correct: optId === correctId, correct_id: correctId },
    }))
    checkAllDone()
  }

  const handleOutput = (correct: boolean, _answer: string) => {
    setHasInteracted(true)
    setOutputResult({ correct, correct_answer: review.what_outputs?.correct ?? '' })
    checkAllDone()
  }

  const checkAllDone = () => {
    // Will check after state settles
    setTimeout(() => {
      const allQ = review.questions.every((q) => quizResults[q.question]?.correct !== undefined)
      if (allQ && (outputResult != null || !review.what_outputs)) {
        setCompleted(true)
      }
    }, 100)
  }

  const handleComplete = () => {
    markComplete(`review-${review.id}`)
    setCompleted(true)
  }

  return (
    <div className="w-full max-w-[800px] flex flex-col gap-6">
      {/* Header */}
      <section
        className="rounded-xl p-6"
        style={{
          background: '#1a1924',
          borderLeft: '8px solid',
          borderLeftColor: review.type === 'quick_recall' ? '#00d4aa' : review.type === 'chapter_review' ? '#c9a227' : review.type === 'boss_review' ? '#ff6b6b' : '#ffd700',
          border: '1px solid rgba(201,162,39,0.15)',
        }}
      >
        <div className="flex items-center gap-2 mb-1" style={{ color: '#00d4aa' }}>
          <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>repeat</span>
          <span className="text-[11px] font-bold uppercase tracking-wider">{colors.label}</span>
          <span className="mx-1 text-[11px]" style={{ color: '#c9a227' }}>·</span>
          <span className="text-[11px]" style={{ color: '#9b98a8' }}>Part {review.part} · Chapter {review.chapter}</span>
        </div>
        <h1 className="text-xl font-extrabold mt-2" style={{ color: '#ffd700' }}>{review.title}</h1>
        <p className="text-xs mt-2" style={{ color: '#9b98a8' }}>{review.subtitle}</p>
        <div className="flex gap-2 flex-wrap mt-3">
          {review.topics.map((topic) => (
            <span
              key={topic}
              className="px-2.5 py-1 rounded-full text-[10px]"
              style={{
                background: 'rgba(0,212,170,0.1)',
                border: '1px solid rgba(0,212,170,0.2)',
                color: '#00d4aa',
              }}
            >
              {topic}
            </span>
          ))}
        </div>
      </section>

      {/* Dialogue — shown only after user interacts with questions */}
      {hasInteracted && review.dialogue && review.dialogue.length > 0 && (
        <section className="flex flex-col gap-4">
          {review.dialogue.map((line, i) => (
            <DialogueBubble key={i} character={line.character} text={line.text} />
          ))}
        </section>
      )}
      {!hasInteracted && review.dialogue && review.dialogue.length > 0 && (
        <div
          className="rounded-xl p-4"
          style={{
            background: '#1a1924',
            border: '1px solid rgba(201,162,39,0.15)',
          }}
        >
          <p className="text-xs" style={{ color: '#9b98a8' }}>
            💬 Персонажи прокомментируют твои ответы после первой попытки.
          </p>
        </div>
      )}

      {/* Quick questions */}
      {review.questions.length > 0 && (
        <section className="flex flex-col gap-4">
          <h2 className="text-sm font-bold" style={{ color: '#e8e6f0' }}>Knowledge Check</h2>
          {review.questions.map((q, qi) => (
            <div
              key={qi}
              className="rounded-xl p-4"
              style={{
                background: '#1a1924',
                border: '1px solid rgba(201,162,39,0.15)',
              }}
            >
              <p className="text-xs font-bold mb-3" style={{ color: '#e8e6f0' }}>{q.question}</p>
              <div className="space-y-2">
                {q.options.map((opt) => {
                  const selected = quizAnswers[q.question] === opt.id
                  const result = quizResults[q.question]
                  const isCorrect = result?.correct_id === opt.id
                  const isWrong = result && selected && !result.correct
                  return (
                    <button
                      key={opt.id}
                      onClick={() => !result && handleQuiz(q.question, opt.id, q.options.find((o) => o.correct)?.id ?? '')}
                      disabled={!!result}
                      className="w-full flex items-center p-3 rounded-lg text-left transition-all active:scale-[0.99] text-xs"
                      style={{
                        background: isCorrect ? 'rgba(0,212,170,0.15)' : isWrong ? 'rgba(255,107,107,0.15)' : selected ? 'rgba(0,212,170,0.08)' : '#0f0e17',
                        border: `2px solid ${
                          isCorrect ? '#00d4aa' : isWrong ? '#ff6b6b' : selected ? '#00d4aa' : 'rgba(201,162,39,0.2)'
                        }`,
                        color: isCorrect ? '#00d4aa' : isWrong ? '#ff6b6b' : '#e8e6f0',
                      }}
                    >
                      <div
                        className="w-4 h-4 rounded-full mr-3 shrink-0 flex items-center justify-center"
                        style={{
                          border: `2px solid ${
                            isCorrect ? '#00d4aa' : isWrong ? '#ff6b6b' : selected ? '#00d4aa' : 'rgba(201,162,39,0.3)'
                          }`,
                          background: isCorrect ? '#00d4aa' : isWrong ? '#ff6b6b' : selected ? '#00d4aa' : 'transparent',
                        }}
                      >
                        {selected && <div className="w-1.5 h-1.5 rounded-full" style={{ background: '#0f0e17' }} />}
                      </div>
                      <span style={{ fontWeight: selected || isCorrect ? 700 : 400 }}>{opt.text}</span>
                      {isCorrect && <span className="ml-auto material-symbols-outlined text-sm" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>check_circle</span>}
                      {isWrong && <span className="ml-auto material-symbols-outlined text-sm" style={{ color: '#ff6b6b', fontVariationSettings: "'FILL' 1" }}>cancel</span>}
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </section>
      )}

      {/* Predict output */}
      {review.what_outputs && (
        <PredictOutputBlock whatOutputs={review.what_outputs as any} onAnswer={handleOutput} />
      )}

      {/* Find bug */}
      {review.find_bug && (
        <FindBugBlock findBug={review.find_bug} />
      )}

      {/* Task */}
      {review.task && (
        <section
          className="rounded-xl p-4"
          style={{
            background: '#1a1924',
            border: '1px solid rgba(201,162,39,0.15)',
          }}
        >
          <h2 className="text-sm font-bold mb-3" style={{ color: '#ffd700' }}>Practical Task</h2>
          <p className="text-xs mb-2" style={{ color: '#9b98a8' }}>{review.task.description}</p>
          <div
            className="p-3 rounded-lg font-mono text-xs"
            style={{
              background: '#0d0c14',
              border: '1px solid rgba(0,212,170,0.2)',
              color: '#00d4aa',
            }}
          >
            {review.task.expected_output}
          </div>
        </section>
      )}

      {/* Complete button */}
      {allDone && !completed && (
        <button
          onClick={handleComplete}
          className="w-full py-4 rounded-lg text-sm font-bold cursor-pointer border-none transition-all hover:scale-[1.02]"
          style={{
            background: 'linear-gradient(135deg, #c9a227, #8b7355)',
            color: '#1a1a2e',
          }}
        >
          ✅ Review Complete!
        </button>
      )}

      {completed && (
        <section
          className="rounded-xl p-6 text-center"
          style={{
            background: 'rgba(0,212,170,0.1)',
            border: '1px solid #00d4aa',
          }}
        >
          <span className="material-symbols-outlined text-4xl" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>celebration</span>
          <h2 className="text-lg font-bold mt-2" style={{ color: '#00d4aa' }}>Excellent!</h2>
          <p className="text-xs mt-1" style={{ color: '#9b98a8' }}>Material consolidated. You may proceed.</p>
          <div className="mt-4 flex gap-4 justify-center">
            <button
              onClick={() => navigate('/')}
              className="px-6 py-2.5 rounded-lg text-xs font-bold cursor-pointer transition-all"
              style={{
                background: '#1a1924',
                border: '1px solid rgba(201,162,39,0.3)',
                color: '#9b98a8',
              }}
            >
              Return to Hub
            </button>
          </div>
        </section>
      )}
    </div>
  )
}
