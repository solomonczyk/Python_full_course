import { useState } from 'react'
import type { Lesson } from '../types'
import { checkQuizAnswer } from '../hooks/useApi'

interface Props {
  lesson: Lesson
  onScore?: (score: number) => void
}

export default function QuizSection({ lesson, onScore }: Props) {
  const [quizAnswer, setQuizAnswer] = useState<string | null>(null)
  const [quizResult, setQuizResult] = useState<{ correct: boolean; correct_id: string } | null>(null)

  const handleQuiz = async (id: string) => {
    setQuizAnswer(id)
    const res = await checkQuizAnswer(lesson.id, id)
    setQuizResult(res)
    if (res.correct) onScore?.(100)
  }

  return (
    <section className="bg-white rounded-2xl p-6 shadow-sm border border-outline-variant">
      <div className="flex items-center gap-3 mb-5">
        <div className="w-10 h-10 bg-secondary-container/20 rounded-xl flex items-center justify-center text-secondary">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>quiz</span>
        </div>
        <h3 className="font-display text-[20px] leading-7 font-bold text-on-surface">Мини-квиз</h3>
      </div>

      <p className="mb-6 text-[15px] leading-[22px] text-on-surface-variant">{lesson.quiz.question}</p>

      <div className="space-y-3">
        {lesson.quiz.options.map((opt) => {
          const isSelected = quizAnswer === opt.id
          const isCorrectAnswer = quizResult && quizResult.correct_id === opt.id
          const isWrong = quizResult && isSelected && !quizResult.correct
          return (
            <button
              key={opt.id}
              onClick={() => !quizResult && handleQuiz(opt.id)}
              disabled={!!quizResult}
              className={`w-full flex items-center p-4 border-2 rounded-xl text-left transition-all active:scale-[0.99]
                ${isCorrectAnswer ? 'border-action-da bg-green-50' :
                  isWrong ? 'border-error bg-red-50' :
                  isSelected ? 'border-secondary bg-secondary/5' :
                  'border-surface-container hover:border-secondary'}`}
            >
              <div className={`w-5 h-5 border-2 rounded-full mr-4 shrink-0 flex items-center justify-center
                ${isCorrectAnswer ? 'border-action-da bg-action-da' :
                  isWrong ? 'border-error bg-error' :
                  isSelected ? 'border-secondary bg-secondary' : 'border-outline'}`}>
                {(isSelected || isCorrectAnswer) && <div className="w-2 h-2 bg-white rounded-full" />}
              </div>
              <span className={`text-body-main ${(isSelected || isCorrectAnswer) ? 'font-bold' : ''}`}>{opt.text}</span>
              {isCorrectAnswer && <span className="ml-auto material-symbols-outlined text-action-da" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>}
              {isWrong && <span className="ml-auto material-symbols-outlined text-error" style={{ fontVariationSettings: "'FILL' 1" }}>cancel</span>}
            </button>
          )
        })}
      </div>

      {quizResult && (
        <p className={`mt-4 text-sm font-semibold ${quizResult.correct ? 'text-action-da' : 'text-error'}`}>
          {quizResult.correct ? '✅ Правильно!' : `❌ Неверно. Правильный ответ: ${lesson.quiz.options.find(o => o.id === quizResult.correct_id)?.text}`}
        </p>
      )}
    </section>
  )
}
