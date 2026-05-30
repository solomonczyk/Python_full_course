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

  // Shuffle options on mount and on each retry
  const shuffledOptions = useMemo(
    () => shuffle(lesson.quiz.options),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [lesson.quiz.question, attempt]
  )

  const handleQuiz = async (id: string) => {
    setQuizAnswer(id)
    try {
      const res = await checkQuizAnswer(lesson.id, id)
      setQuizResult(res)
      if (res.correct) onScore?.(100)
    } catch (e) {
      console.error('Quiz check failed:', e)
      setQuizResult({ correct: false, correct_id: '' })
    }
  }

  const handleRetry = () => {
    setQuizAnswer(null)
    setQuizResult(null)
    setAttempt((a) => a + 1)
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

          return (
            <button
              key={opt.id + String(attempt)}
              onClick={() => !quizResult && handleQuiz(opt.id)}
              disabled={!!quizResult}
              className="w-full flex items-center p-3 rounded-lg text-left transition-all active:scale-[0.99] text-xs"
              style={{
                background: isCorrectAnswer
                  ? 'rgba(0,212,170,0.15)'
                  : isWrong
                    ? 'rgba(255,107,107,0.15)'
                    : isSelected
                      ? 'rgba(0,212,170,0.08)'
                      : '#0f0e17',
                border: `2px solid ${
                  isCorrectAnswer
                    ? '#00d4aa'
                    : isWrong
                      ? '#ff6b6b'
                      : isSelected
                        ? '#00d4aa'
                        : 'rgba(201,162,39,0.2)'
                }`,
                color: isCorrectAnswer
                  ? '#00d4aa'
                  : isWrong
                    ? '#ff6b6b'
                    : '#e8e6f0',
              }}
            >
              <div
                className="w-4 h-4 rounded-full mr-3 shrink-0 flex items-center justify-center"
                style={{
                  border: `2px solid ${
                    isCorrectAnswer
                      ? '#00d4aa'
                      : isWrong
                        ? '#ff6b6b'
                        : isSelected
                          ? '#00d4aa'
                          : 'rgba(201,162,39,0.3)'
                  }`,
                  background: isCorrectAnswer
                    ? '#00d4aa'
                    : isWrong
                      ? '#ff6b6b'
                      : isSelected
                        ? '#00d4aa'
                        : 'transparent',
                }}
              >
                {(isSelected || isCorrectAnswer) && <div className="w-1.5 h-1.5 rounded-full" style={{ background: '#0f0e17' }} />}
              </div>
              <span style={{ fontWeight: isSelected || isCorrectAnswer ? 700 : 400 }}>{opt.text}</span>
              {isCorrectAnswer && <span className="ml-auto material-symbols-outlined text-sm" style={{ color: '#00d4aa', fontVariationSettings: "'FILL' 1" }}>check_circle</span>}
              {isWrong && <span className="ml-auto material-symbols-outlined text-sm" style={{ color: '#ff6b6b', fontVariationSettings: "'FILL' 1" }}>cancel</span>}
            </button>
          )
        })}
      </div>

      {quizResult && (
        <div className="flex items-center justify-between mt-4">
          <p className="text-xs font-bold" style={{ color: quizResult.correct ? '#00d4aa' : '#ff6b6b' }}>
            {quizResult.correct
              ? '✅ Правильно!'
              : `❌ Неверно. Правильный ответ: ${lesson.quiz.options.find(o => o.id === quizResult.correct_id)?.text}`
            }
          </p>
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
        </div>
      )}
    </div>
  )
}
