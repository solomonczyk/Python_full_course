export type Character = 'ksyu' | 'va' | 'da' | 'bagus' | 'novice'

export interface QuizOption {
  id: string
  text: string
  correct: boolean
}

export interface DialogueLine {
  character: Character
  text: string
}

export type ReminderType =
  | 'indentation_reminder'
  | 'colon_reminder'
  | 'block_structure_reminder'
  | 'input_conversion_reminder'
  | 'index_reminder'
  | 'range_reminder'
  | 'loop_stop_reminder'
  | 'mutation_reminder'
  | 'copy_reference_reminder'

export interface SyntaxReminder {
  type: ReminderType
  message: string
}

// ── Spaced review types ─────────────────────────────────────────────────

export type ReviewType = 'quick_recall' | 'chapter_review' | 'boss_review' | 'part_review'

export interface ReviewOption {
  id: string
  text: string
  correct: boolean
}

export interface ReviewQuestion {
  question: string
  options: ReviewOption[]
}

export interface ReviewTask {
  title: string
  description: string
  expected_output: string
}

export interface ReviewBlock {
  id: string
  type: ReviewType
  title: string
  subtitle: string
  position_after: string
  part: number
  chapter: number
  topics: string[]
  dialogue?: DialogueLine[]
  questions: ReviewQuestion[]
  what_outputs: {
    code: string
    options: string[]
    correct: string
  }
  find_bug: {
    description: string
    code: string
    hint: string
    correct?: string
  }
  task: ReviewTask
}

export interface ReviewSummary {
  id: string
  type: ReviewType
  title: string
  subtitle: string
  position_after: string
  part: number
  chapter: number
  topics: string[]
}

// ── Lesson types ────────────────────────────────────────────────────────

export type Difficulty = 'easy' | 'medium' | 'hard' | 'boss'

export interface LessonSummary {
  id: string
  part: number
  chapter: number
  lesson: number
  slug: string
  title: string
  subtitle: string
  topic: string
  locked: boolean
  difficulty: Difficulty
  estimated_time_min: number
  scene_image?: string
}

export interface Lesson extends LessonSummary {
  scene_image?: string
  game_relevance?: string
  pre_topic_dialogue?: DialogueLine[]
  post_error_dialogue?: DialogueLine[]
  mini_summary?: string
  connection_to_game?: string
  story_placement?: string
  syntax_reminder?: SyntaxReminder
  variable_demo?: import('../components/VariableBoxBlock').VariableBox[][]
  explanation: {
    text: string
    character: Character
    code_example: string
    output: string
  }
  quiz: {
    question: string
    options: QuizOption[]
  }
  what_outputs: {
    code: string
    options: string[]
    correct: string
  }
  find_bug: {
    description: string
    code: string
    hint: string
    correct?: string
  }
  mission: {
    title: string
    description: string
    task: string
    expected_output: string
    character: Character
  }
}

export interface Progress {
  lesson_id: string
  completed: boolean
  score: number | null
  updated_at: string
}

export interface MissionResult {
  correct: boolean
  actual_output: string | null
  expected_output: string
  error: string | null
}
