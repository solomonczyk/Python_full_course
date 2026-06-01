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
  foundation?: FoundationBlock
  game_relevance?: string
  analogy?: {
    title: string
    story_metaphor: string
    python_mapping: string
    key_rule: string
  }
  pre_topic_dialogue?: DialogueLine[]
  post_error_dialogue?: DialogueLine[]
  common_mistakes?: CommonMistake[]
  code_watch?: CodeWalkthrough
  task_presentation?: TaskPresentation
  mini_summary?: string
  connection_to_game?: string
  practice_subtasks?: PracticeSubtask[]
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

export interface PracticeSubtask {
  title: string
  task: string
  expected_output: string
  hint?: string
}

export interface MissionResult {
  correct: boolean
  actual_output: string | null
  expected_output: string
  error: string | null
  // New v2 fields (optional for backward compatibility)
  output_correct?: boolean | null
  structure_correct?: boolean
  safety_passed?: boolean
  finally_correct?: boolean
  hints?: string[]
  details?: {
    constructs_found?: string[]
    required_constructs?: string[]
    missing_constructs?: string[]
  }
}

// ── Common Mistakes types ──────────────────────────────────────────────

// ── Foundation types (embedding inside lessons) ──────────────────────────────

export interface FoundationTerm {
  term_id: string
  label: string
  definition: string
}

export interface FoundationBlock {
  title: string
  terms?: FoundationTerm[]
  glossary_terms?: string[]
  rules?: string[]
}

// ── Glossary types ──────────────────────────────────────────────────────────

export type GlossaryCategory =
  | 'basics'
  | 'strings'
  | 'variables'
  | 'numbers'
  | 'conditions'
  | 'loops'
  | 'functions'
  | 'lists'
  | 'errors'
  | 'style'

export interface GlossaryTerm {
  id: string
  term: string
  python_name: string
  category: GlossaryCategory
  simple_definition: string
  analogy: string
  code_example: string
  common_mistake: string
  mistake_explanation: string
  related_lessons: string[]
  beginner_level: string
}

export interface GlossaryTermSummary {
  id: string
  term: string
  python_name: string
  category: string
  beginner_level: string
}

// ── Recap types ─────────────────────────────────────────────────────────────

export interface MiniCheck {
  question: string
  answer: string
}

export interface HeroSkill {
  name: string
  python: string
  meaning: string
  analogy: string
}

export interface Recap {
  id: string
  part: number
  title: string
  story_summary: string
  learned_terms: string[]
  hero_skills: HeroSkill[]
  key_rules: string[]
  mini_check: MiniCheck[]
}

export interface RecapSummary {
  id: string
  part: number
  title: string
}

// ── Quest types ─────────────────────────────────────────────────────────────

export interface QuestTestCase {
  input: string
  expected_contains: string[]
}

export interface ChapterQuest {
  id: string
  part: number
  title: string
  story: string
  required_lessons: string[]
  required_constructs: string[]
  task: string
  starter_code: string
  example_solution: string
  test_cases: QuestTestCase[]
  success_criteria: string[]
  hints: string[]
}

export interface QuestSummary {
  id: string
  part: number
  title: string
}

export interface CommonMistake {
  title: string
  wrong: string
  right: string
  note: string
}

// ── Code Walkthrough types ──────────────────────────────────────────────

export interface WalkthroughStep {
  speaker: Character
  text: string
  code?: string
  output?: string
  caption?: string
}

export interface WhatIfScenario {
  description: string
  input: string
  code: string
  output: string
}

export interface WalkthroughSolution {
  title: string
  description: string
  code: string
  output?: string
}

export interface CodeWalkthrough {
  title: string
  main_code: string
  dialogue: WalkthroughStep[]
  what_if?: WhatIfScenario[]
  solutions?: WalkthroughSolution[]
}

export interface TaskPresentation {
  title: string
  description: string
  initial_code: string
  expected_output: string
  what_if?: WhatIfScenario[]
  solutions?: WalkthroughSolution[]
}
