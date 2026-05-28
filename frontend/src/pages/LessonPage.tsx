import { useParams } from 'react-router-dom'
import { useLesson } from '../hooks/useApi'
import { useProgressContext } from '../hooks/ProgressContext'
import DialogueBubble from '../components/DialogueBubble'
import CodeBlock from '../components/CodeBlock'
import QuizSection from '../components/QuizSection'
import MissionCard from '../components/MissionCard'

export default function LessonPage() {
  const { id } = useParams<{ id: string }>()
  const { lesson, loading, error } = useLesson(id ?? '')
  const { progress, markComplete } = useProgressContext()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center gap-4 text-on-surface-variant">
          <span className="material-symbols-outlined text-5xl animate-spin" style={{ fontVariationSettings: "'FILL' 0" }}>progress_activity</span>
          <p className="font-sans text-[15px]">Загружаем урок...</p>
        </div>
      </div>
    )
  }

  if (error || !lesson) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center text-error">
          <span className="material-symbols-outlined text-5xl block mb-2" style={{ fontVariationSettings: "'FILL' 0" }}>error</span>
          <p>{error ?? 'Урок не найден'}</p>
        </div>
      </div>
    )
  }

  const isDone = progress[lesson.id]?.completed

  return (
    <div className="w-full max-w-[800px] flex flex-col gap-12">
      {/* Lesson header */}
      <section>
        <div className="flex items-center gap-2 text-secondary mb-2 font-sans text-[13px] font-bold">
          <span>ЧАСТЬ {lesson.part}</span>
          <span className="material-symbols-outlined text-sm">chevron_right</span>
          <span>УРОК {lesson.id}</span>
          {isDone && (
            <span className="ml-2 inline-flex items-center gap-1 text-action-da">
              <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
              Завершён
            </span>
          )}
        </div>
        <h2 className="font-display font-extrabold text-[36px] leading-[44px] tracking-tight text-on-surface">
          {lesson.title}: {lesson.subtitle}
        </h2>
      </section>

      {/* Scene illustration */}
      {lesson.scene_image && (
        <section className="relative group overflow-hidden rounded-[24px] shadow-sm">
          <img
            src={lesson.scene_image}
            alt=""
            className="w-full aspect-[21/9] object-cover transition-transform duration-700 group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
        </section>
      )}

      {/* Explanation dialogue */}
      <DialogueBubble
        character={lesson.explanation.character}
        text={lesson.explanation.text}
      />

      {/* Code example */}
      <CodeBlock
        code={lesson.explanation.code_example}
        output={lesson.explanation.output}
      />

      {/* Quiz + What outputs + Find bug */}
      <QuizSection
        lesson={lesson}
        onScore={(score) => markComplete(lesson.id, score)}
      />

      {/* Mission */}
      <MissionCard
        mission={lesson.mission}
        lessonId={lesson.id}
        onComplete={(score) => markComplete(lesson.id, score)}
      />
    </div>
  )
}
