import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useLesson } from '../hooks/useApi'
import { useProgressContext } from '../hooks/ProgressContext'
import type { LessonSummary } from '../types'
import DialogueBubble from '../components/DialogueBubble'
import CodeBlock from '../components/CodeBlock'
import CodePanel from '../components/CodePanel'
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
import VariableBoxBlock from '../components/VariableBoxBlock'
import AnalogyBlock from '../components/AnalogyBlock'

interface Props {
  lessons: LessonSummary[]
}

const CHAR_COLORS: Record<string, string> = {
  ksyu: '#74B9FF',
  va: '#A29BFE',
  da: '#28A745',
  bagus: '#FF7675',
}

function SteampunkCard({ children, accentColor = 'rgba(201,162,39,0.15)', className = '' }: { children: React.ReactNode; accentColor?: string; className?: string }) {
  return (
    <div
      className={`rounded-xl p-4 ${className}`}
      style={{
        background: '#1a1924',
        border: `1px solid ${accentColor}`,
      }}
    >
      {children}
    </div>
  )
}

export default function LessonPage({ lessons }: Props) {
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()
  const { lesson, loading, error } = useLesson(id ?? '')
  const { progress, markComplete, isLessonUnlocked } = useProgressContext()

  useEffect(() => {
    if (lesson) window.scrollTo(0, 0)
  }, [lesson?.id])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex flex-col items-center gap-4" style={{ color: '#9b98a8' }}>
          <span className="material-symbols-outlined text-5xl animate-spin" style={{ fontVariationSettings: "'FILL' 0" }}>progress_activity</span>
          <p className="text-sm">Loading lesson...</p>
        </div>
      </div>
    )
  }

  if (error || !lesson) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center" style={{ color: '#ff6b6b' }}>
          <span className="material-symbols-outlined text-5xl block mb-2" style={{ fontVariationSettings: "'FILL' 0" }}>error</span>
          <p>{error ?? 'Lesson not found'}</p>
        </div>
      </div>
    )
  }

  const isDone = progress[lesson.id]?.completed
  const unlocked = isLessonUnlocked(lesson.id, lessons)
  if (!unlocked) {
    const idx = lessons.findIndex(l => l.id === lesson.id)
    const prev = idx > 0 ? lessons[idx - 1] : null
    return (
      <div className="w-full max-w-[800px]">
        <section className="rounded-2xl p-8 text-center" style={{ background: '#1a1924', border: '1px solid rgba(255,107,107,0.3)' }}>
          <span className="material-symbols-outlined text-5xl" style={{ color: '#ff6b6b', fontVariationSettings: "'FILL' 1" }}>lock</span>
          <h2 className="text-2xl font-bold mt-4" style={{ color: '#ffd700' }}>Locked</h2>
          <p className="text-sm mt-2" style={{ color: '#9b98a8' }}>Complete the previous lesson to unlock this one.</p>
          {prev && (
            <button
              onClick={() => navigate(`/lesson/${prev.id}`)}
              className="mt-6 px-8 py-3 rounded-lg text-xs font-bold inline-flex items-center gap-2 cursor-pointer border-none transition-all hover:scale-105"
              style={{ background: '#ff6b6b', color: '#0f0e17' }}
            >
              <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>arrow_back</span>
              Go to {prev.id}: {prev.title}
            </button>
          )}
        </section>
      </div>
    )
  }

  const idx = lessons.findIndex((l) => l.id === lesson.id)
  const prev = idx > 0 ? lessons[idx - 1] : null
  const next = idx >= 0 && idx < lessons.length - 1 ? lessons[idx + 1] : null
  const charColor = CHAR_COLORS[lesson.explanation.character] ?? '#74B9FF'

  return (
    <div className="space-y-6">
      {/* Hero banner (compact) */}
      <section
        className="rounded-[20px] overflow-hidden relative"
        style={{
          background: 'linear-gradient(135deg, #1a2a3a 0%, #2a1a3a 50%, #1a1a2e 100%)',
          border: '1px solid rgba(201,162,39,0.3)',
        }}
      >
        <div className="relative z-10 p-6">
          <div
            className="inline-block px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider mb-3"
            style={{
              background: 'rgba(0,212,170,0.15)',
              border: '1px solid #00d4aa',
              color: '#00d4aa',
            }}
          >
            LESSON {lesson.id}
          </div>
          <h1 className="text-xl font-extrabold mb-2" style={{ color: '#e8e6f0' }}>
            {lesson.title}: {lesson.subtitle}
          </h1>
          <p className="text-xs leading-relaxed max-w-[600px]" style={{ color: '#9b98a8' }}>
            {lesson.story_placement ?? 'Master the arcane arts of Python.'}
          </p>
          <div className="flex items-center gap-2 mt-3">
            <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ background: 'rgba(201,162,39,0.1)', color: '#c9a227' }}>
              Topic: {lesson.topic}
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ background: 'rgba(0,212,170,0.1)', color: '#00d4aa' }}>
              {lesson.difficulty === 'easy' ? 'Complexity: 1/10' : lesson.difficulty === 'medium' ? 'Complexity: 3/10' : 'Complexity: 7/10'}
            </span>
          </div>
        </div>
      </section>

      {/* Pre-topic dialogue */}
      {lesson.pre_topic_dialogue && lesson.pre_topic_dialogue.length > 0 && (
        <SteampunkCard>
          <DialogueScene lines={lesson.pre_topic_dialogue} />
        </SteampunkCard>
      )}

      {/* Analogy block — bridges dialogue to explanation */}
      {lesson.analogy && (
        <SteampunkCard accentColor="rgba(201,162,39,0.2)">
          <AnalogyBlock
            analogy={lesson.analogy}
            character={lesson.explanation.character}
          />
        </SteampunkCard>
      )}

      {/* Character card + Code panel (2-col grid) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Character explanation card */}
        <SteampunkCard accentColor={`${charColor}33`}>
          <div className="flex items-center gap-2.5 mb-3">
            <div
              className="w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold shrink-0"
              style={{ background: `linear-gradient(135deg, ${charColor}, ${charColor}88)`, color: '#0f0e17' }}
            >
              {lesson.explanation.character === 'ksyu' ? 'K' : lesson.explanation.character === 'va' ? 'V' : lesson.explanation.character === 'da' ? 'D' : '?'}
            </div>
            <div>
              <div className="text-xs font-bold" style={{ color: charColor }}>
                {lesson.explanation.character === 'ksyu' ? "Ksyu's Instruction" : lesson.explanation.character === 'va' ? "Va's Logic" : lesson.explanation.character === 'da' ? "Da's Mission" : 'Guide'}
              </div>
              <div className="text-[10px]" style={{ color: '#9b98a8' }}>
                {lesson.explanation.character === 'ksyu' ? 'Arch-Mage of Logic' : lesson.explanation.character === 'va' ? 'Master of Logic' : 'Quest Master'}
              </div>
            </div>
          </div>
          <div className="text-xs leading-relaxed" style={{ color: '#9b98a8' }}>
            {lesson.explanation.text}
          </div>
          <div className="flex gap-2 mt-3">
            <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ background: 'rgba(201,162,39,0.1)', color: '#c9a227' }}>
              Subject: {lesson.topic}
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ background: 'rgba(0,212,170,0.1)', color: '#00d4aa' }}>
              Complexity: {lesson.difficulty === 'easy' ? '1/10' : lesson.difficulty === 'medium' ? '3/10' : '7/10'}
            </span>
          </div>
        </SteampunkCard>

        {/* Code panel + status */}
        <div>
          <CodePanel code={lesson.explanation.code_example} filename={`lesson-${lesson.id}.py`} />
          <div
            className="mt-2 px-3.5 py-2 rounded-lg"
            style={{
              background: '#1a1924',
              border: '1px solid rgba(201,162,39,0.15)',
            }}
          >
            <div className="flex justify-between items-center">
              <span className="text-[10px] uppercase tracking-wider" style={{ color: '#9b98a8' }}>Output</span>
              <span className="text-[10px] font-bold" style={{ color: '#00d4aa' }}>{lesson.explanation.output}</span>
            </div>
            <div className="mt-1.5 h-1 rounded-full" style={{ background: 'rgba(0,212,170,0.1)' }}>
              <div className="h-full rounded-full" style={{ width: '85%', background: '#00d4aa' }} />
            </div>
          </div>
        </div>
      </div>

      {/* Syntax reminder */}
      {lesson.syntax_reminder && (
        <SteampunkCard accentColor="rgba(0,212,170,0.2)">
          <SyntaxReminderBlock reminder={lesson.syntax_reminder} />
        </SteampunkCard>
      )}

      {/* Variable demo */}
      {lesson.variable_demo && (
        <SteampunkCard>
          <VariableBoxBlock boxes={lesson.variable_demo} title="Memory Crystals" />
        </SteampunkCard>
      )}

      {/* Predict output + Game relevance */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {lesson.what_outputs && (
          <SteampunkCard>
            <PredictOutputBlock whatOutputs={lesson.what_outputs} />
          </SteampunkCard>
        )}
        {lesson.game_relevance && (
          <SteampunkCard accentColor="rgba(0,212,170,0.15)">
            <GameRelevanceBlock text={lesson.game_relevance} />
          </SteampunkCard>
        )}
      </div>

      {/* Quiz */}
      <SteampunkCard>
        <QuizSection
          lesson={lesson}
          onScore={(score) => markComplete(lesson.id, score)}
        />
      </SteampunkCard>

      {/* Find Bug */}
      {lesson.find_bug && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FindBugBlock findBug={lesson.find_bug} />

          {/* Connection to game or mini-summary */}
          {lesson.connection_to_game && (
            <SteampunkCard accentColor="rgba(0,212,170,0.15)">
              <ConnectionToGameBlock text={lesson.connection_to_game} />
            </SteampunkCard>
          )}
          {!lesson.connection_to_game && lesson.mini_summary && (
            <SteampunkCard>
              <MiniSummaryBlock text={lesson.mini_summary} />
            </SteampunkCard>
          )}
        </div>
      )}

      {/* Post-error dialogue */}
      {lesson.post_error_dialogue && lesson.post_error_dialogue.length > 0 && (
        <SteampunkCard accentColor="rgba(255,107,107,0.15)">
          <DialogueScene lines={lesson.post_error_dialogue} />
        </SteampunkCard>
      )}

      {/* Mini summary (if not already shown) */}
      {lesson.mini_summary && lesson.find_bug && !lesson.connection_to_game && (
        <SteampunkCard>
          <MiniSummaryBlock text={lesson.mini_summary} />
        </SteampunkCard>
      )}

      {/* Mission */}
      <MissionCard
        mission={lesson.mission}
        lessonId={lesson.id}
        onComplete={(score) => markComplete(lesson.id, score)}
      />

      {/* Bottom navigation */}
      <div
        className="flex items-center justify-between px-4 py-4 rounded-xl"
        style={{
          background: '#1a1924',
          border: '1px solid rgba(201,162,39,0.15)',
        }}
      >
        {prev ? (
          <button
            onClick={() => navigate(`/lesson/${prev.id}`)}
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold cursor-pointer transition-all hover:scale-105"
            style={{
              background: 'transparent',
              border: '1px solid rgba(201,162,39,0.3)',
              color: '#9b98a8',
            }}
          >
            <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>arrow_back</span>
            Previous
          </button>
        ) : <div />}

        {/* Page dots */}
        <div className="flex gap-1.5">
          {[0, 1, 2, 3].map((i) => (
            <div
              key={i}
              className="w-2 h-2 rounded-full"
              style={{
                background: i === 0 ? '#00d4aa' : 'rgba(201,162,39,0.3)',
              }}
            />
          ))}
        </div>

        {next && isLessonUnlocked(next.id, lessons) ? (
          <button
            onClick={() => navigate(`/lesson/${next.id}`)}
            className="flex items-center gap-2 px-5 py-2 rounded-lg text-xs font-bold cursor-pointer transition-all hover:scale-105 border-none"
            style={{
              background: 'linear-gradient(135deg, #c9a227, #8b7355)',
              color: '#1a1a2e',
            }}
          >
            Next
            <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>arrow_forward</span>
          </button>
        ) : next ? (
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold opacity-60"
            style={{
              border: '1px solid rgba(201,162,39,0.3)',
              color: '#9b98a8',
            }}
          >
            Locked
            <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 0" }}>lock</span>
          </div>
        ) : <div />}
      </div>
    </div>
  )
}
