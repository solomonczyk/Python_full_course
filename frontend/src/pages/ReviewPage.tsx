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

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [id])

  if (loading) {
    return (
      <div className="w-full max-w-[800px] flex items-center justify-center h-64">
        <div className="flex flex-col items-center gap-4 text-on-surface-variant">
          <span className="material-symbols-outlined text-5xl animate-spin" style={{ fontVariationSettings: "'FILL' 0" }}>progress_activity</span>
          <p className="font-sans text-[15px]">Загружаем повторение...</p>
        </div>
      </div>
    )
  }

  if (error || !review) {
    return (
      <div className="w-full max-w-[800px] flex items-center justify-center h-64">
        <div className="text-center text-error">
          <span className="material-symbols-outlined text-5xl block mb-2" style={{ fontVariationSettings: "'FILL' 0" }}>error</span>
          <p>{error ?? 'Повторение не найдено'}</p>
        </div>
      </div>
    )
  }

  const colors = REVIEW_COLORS[review.type] ?? { bg: 'bg-surface-container', border: 'border-outline', label: 'ПОВТОРЕНИЕ' }
  const allQuizAnswered = review.questions.every((q) => quizAnswers[q.question] != null)
  const allDone = allQuizAnswered && (outputResult != null || !review.what_outputs)

  const handleQuiz = (question: string, optId: string, correctId: string) => {
    setQuizAnswers((prev) => ({ ...prev, [question]: optId }))
    setQuizResults((prev) => ({
      ...prev,
      [question]: { correct: optId === correctId, correct_id: correctId },
    }))
    checkAllDone()
  }

  const handleOutput = (correct: boolean, _answer: string) => {
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
    <div className="w-full max-w-[800px] flex flex-col gap-10">
      {/* Header */}
      <section className={`${colors.bg} ${colors.border} border-l-8 rounded-2xl p-6`}>
        <div className="flex items-center gap-2 text-on-surface-variant mb-1 font-sans text-[13px] font-bold">
          <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>repeat</span>
          <span>{colors.label}</span>
          <span className="mx-1">·</span>
          <span>Часть {review.part} · Глава {review.chapter}</span>
        </div>
        <h1 className="font-display font-extrabold text-[36px] leading-[44px] tracking-tight text-on-surface mt-2">
          {review.title}
        </h1>
        <p className="font-sans text-[16px] leading-6 text-on-surface-variant mt-2">{review.subtitle}</p>
        <div className="mt-4 flex gap-2 flex-wrap">
          {review.topics.map((topic) => (
            <span key={topic} className="bg-white/70 px-3 py-1 rounded-full font-mono text-[12px] text-on-surface-variant border border-outline-variant">
              {topic}
            </span>
          ))}
        </div>
      </section>

      {/* Dialogue */}
      {review.dialogue && review.dialogue.length > 0 && (
        <section className="flex flex-col gap-4">
          {review.dialogue.map((line, i) => (
            <DialogueBubble key={i} character={line.character} text={line.text} />
          ))}
        </section>
      )}

      {/* Quick questions */}
      {review.questions.length > 0 && (
        <section className="flex flex-col gap-6">
          <h2 className="font-display text-[24px] leading-8 font-bold text-on-surface">Вопросы для проверки</h2>
          {review.questions.map((q, qi) => (
            <div key={qi} className="bg-white rounded-2xl p-6 shadow-sm border border-outline-variant">
              <p className="text-[15px] leading-[22px] font-bold text-on-surface mb-4">{q.question}</p>
              <div className="space-y-3">
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
                      className={`w-full flex items-center p-4 border-2 rounded-xl text-left transition-all active:scale-[0.99]
                        ${isCorrect ? 'border-action-da bg-green-50' :
                          isWrong ? 'border-error bg-red-50' :
                          selected ? 'border-secondary bg-secondary/5' :
                          'border-surface-container hover:border-secondary'}`}
                    >
                      <div className={`w-5 h-5 border-2 rounded-full mr-4 shrink-0 flex items-center justify-center
                        ${isCorrect ? 'border-action-da bg-action-da' :
                          isWrong ? 'border-error bg-error' :
                          selected ? 'border-secondary bg-secondary' : 'border-outline'}`}>
                        {selected && <div className="w-2 h-2 bg-white rounded-full" />}
                      </div>
                      <span className={`text-body-main ${selected || isCorrect ? 'font-bold' : ''}`}>{opt.text}</span>
                      {isCorrect && <span className="ml-auto material-symbols-outlined text-action-da" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>}
                      {isWrong && <span className="ml-auto material-symbols-outlined text-error" style={{ fontVariationSettings: "'FILL' 1" }}>cancel</span>}
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
        <section className="bg-white rounded-2xl p-6 shadow-sm border border-outline-variant">
          <h2 className="font-display text-[24px] leading-8 font-bold text-on-surface mb-4">Практическая задача</h2>
          <p className="text-on-surface-variant mb-2">{review.task.description}</p>
          <div className="bg-surface-container p-4 rounded-xl font-mono text-sm border border-outline-variant">
            {review.task.expected_output}
          </div>
        </section>
      )}

      {/* Complete button */}
      {allDone && !completed && (
        <button
          onClick={handleComplete}
          className="w-full py-4 bg-action-da text-white font-display text-[22px] font-bold rounded-2xl shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all"
        >
          ✅ Повторение завершено!
        </button>
      )}

      {completed && (
        <section className="bg-green-50 border-l-8 border-action-da rounded-2xl p-6 text-center">
          <span className="material-symbols-outlined text-5xl text-action-da" style={{ fontVariationSettings: "'FILL' 1" }}>celebration</span>
          <h2 className="font-display text-[24px] font-bold text-on-surface mt-2">Отлично!</h2>
          <p className="text-on-surface-variant mt-1">Материал закреплён. Можно двигаться дальше.</p>
          <div className="mt-4 flex gap-4 justify-center">
            <button
              onClick={() => navigate('/')}
              className="px-6 py-3 bg-surface-container-highest rounded-xl font-bold hover:bg-surface-container transition-all"
            >
              На главную
            </button>
          </div>
        </section>
      )}
    </div>
  )
}
