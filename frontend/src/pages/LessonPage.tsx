import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useLesson } from '../hooks/useApi'
import { useProgressContext } from '../hooks/ProgressContext'
import type { LessonSummary } from '../types'
import DialogueBubble from '../components/DialogueBubble'
import CodeBlock from '../components/CodeBlock'
import QuizSection from '../components/QuizSection'
import MissionCard from '../components/MissionCard'
import StoryPlacementBlock from '../components/StoryPlacementBlock'
import DialogueScene from '../components/DialogueScene'
import GameRelevanceBlock from '../components/GameRelevanceBlock'
import MiniSummaryBlock from '../components/MiniSummaryBlock'
import ConnectionToGameBlock from '../components/ConnectionToGameBlock'
import PredictOutputBlock from '../components/PredictOutputBlock'
import FindBugBlock from '../components/FindBugBlock'
import SyntaxReminderBlock from '../components/SyntaxReminderBlock'

interface Props {
  lessons: LessonSummary[]
}

export default function LessonPage({ lessons }: Props) {
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()
  const { lesson, loading, error } = useLesson(id ?? '')
  const { progress, markComplete } = useProgressContext()

  // Scroll to top when lesson data loads (handles async fetch completion)
  useEffect(() => {
    if (lesson) window.scrollTo(0, 0)
  }, [lesson?.id])

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

      {/* Story placement */}
      {lesson.story_placement && (
        <StoryPlacementBlock text={lesson.story_placement} />
      )}

      {/* Pre-topic dialogue */}
      {lesson.pre_topic_dialogue && lesson.pre_topic_dialogue.length > 0 && (
        <DialogueScene lines={lesson.pre_topic_dialogue} />
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

      {/* Syntax reminder */}
      {lesson.syntax_reminder && (
        <SyntaxReminderBlock reminder={lesson.syntax_reminder} />
      )}

      {/* Game relevance */}
      {lesson.game_relevance && (
        <GameRelevanceBlock text={lesson.game_relevance} />
      )}

      {/* Predict output */}
      {lesson.what_outputs && (
        <PredictOutputBlock whatOutputs={lesson.what_outputs} />
      )}

      {/* Quiz */}
      <QuizSection
        lesson={lesson}
        onScore={(score) => markComplete(lesson.id, score)}
      />

      {/* Find bug */}
      {lesson.find_bug && (
        <FindBugBlock findBug={lesson.find_bug} />
      )}

      {/* Post-error dialogue */}
      {lesson.post_error_dialogue && lesson.post_error_dialogue.length > 0 && (
        <DialogueScene lines={lesson.post_error_dialogue} />
      )}

      {/* Mini summary */}
      {lesson.mini_summary && (
        <MiniSummaryBlock text={lesson.mini_summary} />
      )}

      {/* Mission */}
      <MissionCard
        mission={lesson.mission}
        lessonId={lesson.id}
        onComplete={(score) => markComplete(lesson.id, score)}
      />

      {/* Connection to the final game */}
      {lesson.connection_to_game && (
        <ConnectionToGameBlock text={lesson.connection_to_game} />
      )}

      {/* Navigation */}
      {(() => {
        const idx = lessons.findIndex((l) => l.id === lesson.id)
        const prev = idx > 0 ? lessons[idx - 1] : null
        const next = idx >= 0 && idx < lessons.length - 1 ? lessons[idx + 1] : null
        return (
          <section className="flex items-center justify-between gap-4 pt-4 border-t border-outline-variant">
            {prev ? (
              <button
                onClick={() => navigate(`/lesson/${prev.id}`)}
                className="flex items-center gap-2 px-5 py-3 rounded-xl border-2 border-outline-variant text-on-surface-variant hover:border-secondary hover:text-secondary active:scale-[0.98] transition-all font-sans text-[14px] font-bold"
              >
                <span className="material-symbols-outlined text-[18px]">arrow_back</span>
                <div className="text-left">
                  <div className="text-[11px] text-on-surface-variant/60 font-normal">Попередній</div>
                  <div>{prev.id}: {prev.title}</div>
                </div>
              </button>
            ) : <div />}
            {next && !next.locked ? (
              <button
                onClick={() => navigate(`/lesson/${next.id}`)}
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-primary text-on-primary shadow-md hover:opacity-90 active:scale-[0.98] transition-all font-sans text-[14px] font-bold"
              >
                <div className="text-right">
                  <div className="text-[11px] text-on-primary/70 font-normal">Наступний</div>
                  <div>{next.id}: {next.title}</div>
                </div>
                <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
              </button>
            ) : next?.locked ? (
              <div className="flex items-center gap-2 px-6 py-3 rounded-xl border-2 border-outline-variant text-outline font-sans text-[14px] font-bold opacity-60">
                <div className="text-right">
                  <div className="text-[11px] font-normal">Заблоковано</div>
                  <div>{next.id}: {next.title}</div>
                </div>
                <span className="material-symbols-outlined text-[18px]">lock</span>
              </div>
            ) : <div />}
          </section>
        )
      })()}
    </div>
  )
}
