import { useState, useMemo } from 'react'
import type { Lesson } from '../types'
import { checkQuizAnswer } from '../hooks/useApi'

interface Props {
  lesson: Lesson
  onScore?: (score: number) => void
}

/** Fisher-Yates shuffle */
function shuffle<T>(arr: T[]): T[] {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

export default function QuizSection({ lesson, onScore }: Props) {
  const [quizAnswer, setQuizAnswer] = useState<string | null>(null)
  const [quizResult, setQuizResult] = useState<{ correct: boolean; correct_id: string } | null>(null)
  const [attempt, setAttempt] = useState(0)
  const [checking, setChecking] = useState(false)

  // Shuffle options on mount and on each retry
  const shuffledOptions = useMemo(
    () => shuffle(lesson.quiz.options),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [lesson.quiz.question, attempt]
  )

  const handleQuiz = async (id: string) => {
    if (checking || quizResult) return // Prevent double-click
    setQuizAnswer(id)
    setChecking(true)
    try {
      const res = await checkQuizAnswer(lesson.id, id)
      setQuizResult(res)
      if (res.correct) onScore?.(100)
    } catch (e) {
      console.error('Quiz check failed:', e)
      setQuizResult({ correct: false, correct_id: '' })
    } finally {
      setChecking(false)
    }
  }

  const handleRetry = () => {
    setQuizAnswer(null)
    setQuizResult(null)
    setAttempt((a) => a + 1)
    setChecking(false)
  }

  return (
    <div
      className="rounded-xl p-4"
      style={{
        background: 'rgba(201,162,39,0.05)',
        border: '1px solid rgba(201,162,39,0.15)',
      }}
    >
      <div className="flex items-center gap-2 mb-3">
        <span className="material-symbols-outlined text-sm" style={{ color: '#c9a227', fontVariationSettings: "'FILL' 1" }}>quiz</span>
        <h3 className="text-xs font-bold" style={{ color: '#c9a227' }}>Мини-квиз</h3>
      </div>

      <p className="text-xs leading-relaxed mb-4" style={{ color: '#e8e6f0' }}>{lesson.quiz.question}</p>

      <div className="space-y-2">
        {shuffledOptions.map((opt) => {
          const isSelected = quizAnswer === opt.id
          const isCorrectAnswer = quizResult && quizResult.correct_id === opt.id
          const isWrong = quizResult && isSelected && !quizResult.correct
          const isLoading = checking && isSelected

          let bgColor = '#0f0e17'
          let borderColor = 'rgba(201,162,39,0.2)'
          let textColor = '#e8e6f0'
          let dotColor = 'transparent'
          let dotBorder = 'rgba(201,162,39,0.3)'

          if (isCorrectAnswer) {
            bgColor = 'rgba(0,212,170,0.15)'
            borderColor = '#00d4aa'
            textColor = '#00d4aa'
            dotColor = '#00d4aa'
            dotBorder = '#00d4aa'
          } else if (isWrong) {
            bgColor = 'rgba(255,107,107,0.15)'
            borderColor = '#ff6b6b'
            textColor = '#ff6b6b'
            dotColor = '#ff6b6b'
            dotBorder = '#ff6b6b'
          } else if (isSelected) {
            bgColor = 'rgba(0,212,170,0.08)'
            borderColor = '#00d4aa'
            dotColor = '#00d4aa'
            dotBorder = '#00d4aa'
          }

          // Add hover glow only when interactive
          const hoverStyle = !quizResult && !checking
            ? { boxShadow: '0 0 12px rgba(0,212,170,0.15)' }
            : {}

          return (
            <button
              key={opt.id + String(attempt)}
              onClick={() => handleQuiz(opt.id)}
              disabled={!!quizResult || checking}
              className={`
                w-full flex items-center p-3 rounded-lg text-left text-xs
                transition-all duration-200
                ${!quizResult && !checking ? 'cursor-pointer hover:scale-[1.01] active:scale-[0.99]' : 'cursor-default'}
                ${isLoading ? 'animate-pulse' : ''}
              `}
              style={{
                background: bgColor,
                border: `2px solid ${borderColor}`,
                color: textColor,
                transform: isSelected && !quizResult ? 'scale(1.01)' : 'scale(1)',
                ...hoverStyle,
              }}
            >
              <div
                className="w-5 h-5 rounded-full mr-3 shrink-0 flex items-center justify-center transition-all duration-200"
                style={{
                  border: `2px solid ${dotBorder}`,
                  background: dotColor,
                  boxShadow: isSelected ? '0 0 6px rgba(0,212,170,0.4)' : 'none',
                }}
              >
                {(isSelected || isCorrectAnswer) && (
                  <div
                    className="w-1.5 h-1.5 rounded-full animate-[scale-in_0.15s_ease-out]"
                    style={{ background: '#0f0e17' }}
                  />
                )}
              </div>
              <span className="flex-1" style={{ fontWeight: isSelected || isCorrectAnswer ? 700 : 400 }}>
                {opt.text}
              </span>
              {isLoading && (
                <span className="ml-2 material-symbols-outlined text-sm animate-spin" style={{ color: '#c9a227', fontVariationSettings: "'FILL' 0" }}>
                  progress_activity
                </span>
              )}
              {isCorrectAnswer && (
                <span className="ml-2 material-symbols-outlined text-sm" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>
                  check_circle
                </span>
              )}
              {isWrong && (
                <span className="ml-2 material-symbols-outlined text-sm" style={{ color: '#ff6b6b', fontVariationSettings: "'FILL' 1" }}>
                  cancel
                </span>
              )}
            </button>
          )
        })}
      </div>

      {quizResult && (
        <div className="flex items-center justify-between mt-4 pt-3 border-t" style={{ borderColor: 'rgba(201,162,39,0.1)' }}>
          <p className="text-xs font-bold flex items-center gap-2" style={{ color: quizResult.correct ? '#00d4aa' : '#ff6b6b' }}>
            <span className="text-base">{quizResult.correct ? '✅' : '❌'}</span>
            {quizResult.correct
              ? 'Правильно!'
              : `Неверно. Правильный ответ: ${lesson.quiz.options.find(o => o.id === quizResult.correct_id)?.text}`
            }
          </p>
          {!quizResult.correct && (
            <button
              onClick={handleRetry}
              className="text-xs font-bold cursor-pointer transition-all hover:scale-105 active:scale-95"
              style={{
                color: '#0f0e17',
                background: '#c9a227',
                border: 'none',
                borderRadius: '8px',
                padding: '6px 14px',
              }}
            >
              ↻ Ещё попытка
            </button>
          )}
        </div>
      )}
    </div>
  )
}
