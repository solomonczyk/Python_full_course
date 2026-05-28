import { useState } from 'react'
import type { Lesson } from '../types'
import { checkQuizAnswer, checkWhatOutputs } from '../hooks/useApi'

interface Props {
  lesson: Lesson
  onScore?: (score: number) => void
}

export default function QuizSection({ lesson, onScore }: Props) {
  const [quizAnswer, setQuizAnswer] = useState<string | null>(null)
  const [quizResult, setQuizResult] = useState<{ correct: boolean; correct_id: string } | null>(null)
  const [outputAnswer, setOutputAnswer] = useState<string | null>(null)
  const [outputResult, setOutputResult] = useState<{ correct: boolean; correct_answer: string } | null>(null)
  const [showHint, setShowHint] = useState(false)

  const handleQuiz = async (id: string) => {
    setQuizAnswer(id)
    const res = await checkQuizAnswer(lesson.id, id)
    setQuizResult(res)
    if (res.correct && outputResult?.correct) onScore?.(100)
  }

  const handleOutput = async (answer: string) => {
    setOutputAnswer(answer)
    const res = await checkWhatOutputs(lesson.id, answer)
    setOutputResult(res)
    if (res.correct && quizResult?.correct) onScore?.(100)
  }

  return (
    <div className="flex flex-col gap-12">
      {/* Quiz */}
      <section className="bg-white rounded-xl p-8 shadow-sm border border-outline-variant">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-secondary-container/20 rounded-lg flex items-center justify-center text-secondary">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>quiz</span>
          </div>
          <h3 className="font-display text-[20px] leading-7 font-semibold">Мини-квиз</h3>
        </div>
        <p className="mb-6 text-on-surface-variant">{lesson.quiz.question}</p>
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

      {/* What outputs + Find bug bento */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* What outputs */}
        <section className="bg-surface-container-low p-6 rounded-2xl border border-outline-variant flex flex-col gap-4">
          <div className="flex items-center gap-2 text-tertiary">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>visibility</span>
            <h4 className="font-sans text-[13px] font-bold tracking-wider">ЧТО ВЫВЕДЕТ КОД?</h4>
          </div>
          <div className="bg-black/80 p-4 rounded-lg font-mono text-sm text-green-400 whitespace-pre">{lesson.what_outputs.code}</div>
          <div className="flex gap-2 flex-wrap">
            {lesson.what_outputs.options.map((opt) => {
              const isSelected = outputAnswer === opt
              const isCorrect = outputResult && outputResult.correct_answer === opt
              const isWrong = outputResult && isSelected && !outputResult.correct
              return (
                <button
                  key={opt}
                  onClick={() => !outputResult && handleOutput(opt)}
                  disabled={!!outputResult}
                  className={`flex-1 min-w-[60px] py-2 px-3 rounded-lg border font-sans text-[13px] font-bold transition-all
                    ${isCorrect ? 'bg-green-100 border-action-da text-action-da' :
                      isWrong ? 'bg-red-50 border-error text-error' :
                      isSelected ? 'bg-secondary/10 border-secondary' :
                      'bg-white border-outline-variant hover:bg-surface-container-highest'}`}
                >
                  {opt}
                </button>
              )
            })}
          </div>
          {outputResult && (
            <p className={`text-xs font-semibold ${outputResult.correct ? 'text-action-da' : 'text-error'}`}>
              {outputResult.correct ? '✅ Верно!' : `❌ Правильный ответ: ${outputResult.correct_answer}`}
            </p>
          )}
        </section>

        {/* Find bug */}
        <section className="bg-error-container/20 p-6 rounded-2xl border border-error-bagus/30 flex flex-col gap-4 relative overflow-hidden">
          <div className="flex items-center gap-2 text-error">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 0" }}>bug_report</span>
            <h4 className="font-sans text-[13px] font-bold tracking-wider">НАЙДИ ОШИБКУ</h4>
          </div>
          <p className="text-sm text-on-surface-variant">{lesson.find_bug.description}</p>
          <div className="bg-white/60 p-4 rounded-lg font-mono text-sm border-l-4 border-error text-on-surface">
            <span className="text-error">{lesson.find_bug.code.split('(')[0]}</span>
            {lesson.find_bug.code.includes('(') ? '(' + lesson.find_bug.code.split('(').slice(1).join('(') : ''}
          </div>
          {!showHint ? (
            <button
              onClick={() => setShowHint(true)}
              className="mt-auto w-full py-2 bg-error-bagus/10 text-error font-sans text-[13px] font-bold rounded-lg hover:bg-error-bagus/20 transition-colors"
            >
              Показать подсказку
            </button>
          ) : (
            <div className="mt-auto p-3 bg-white/80 rounded-lg border border-error-bagus/30">
              <p className="text-sm text-on-surface">💡 {lesson.find_bug.hint}</p>
            </div>
          )}
          <div className="absolute -right-4 -bottom-4 w-16 h-16 opacity-10">
            <span className="material-symbols-outlined text-6xl text-error">dangerous</span>
          </div>
        </section>
      </div>
    </div>
  )
}
