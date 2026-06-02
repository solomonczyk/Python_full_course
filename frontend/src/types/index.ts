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
}

// ── Common Mistakes types ──────────────────────────────────────────────

export interface CommonMistake {
  title: string
  wrong: string
  right: string
  note: string
}

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

// ── Quest types ──────────────────────────────────────────────────────────

export interface QuestTestCase {
  input: string
  expected_contains: string[]
}

export interface QuestSummary {
  id: string
  part: number
  title: string
  is_capstone?: boolean
}

export interface Quest {
  id: string
  part: number
  title: string
  is_capstone?: boolean
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

export interface QuestCheckResult {
  quest_id: string
  results: Array<{
    passed: boolean
    input: string
    actual_output: string
    missing_contains: string[]
    error?: string | null
  }>
  all_passed: boolean
  error?: string
}

// ── Recap types ──────────────────────────────────────────────────────────

export interface RecapSummary {
  id: string
  part: number
  title: string
}

export interface HeroSkill {
  name: string
  python: string
  meaning: string
  analogy: string
}

export interface MiniCheckItem {
  question: string
  answer: string
}

export interface Recap {
  id: string
  part: number
  title: string
  story_summary: string
  learned_terms: string[]
  hero_skills: HeroSkill[]
  key_rules: string[]
  mini_check: MiniCheckItem[]
}

export interface TaskPresentation {
  title: string
  description: string
  initial_code: string
  expected_output: string
  what_if?: WhatIfScenario[]
  solutions?: WalkthroughSolution[]
}

// ── Part flow types ────────────────────────────────────────────────────────

export type PartFlowItem =
  | { type: 'lesson'; id: string; lesson: LessonSummary }
  | {
      type: 'recap'
      id: string
      recap: RecapSummary
      unlocked: boolean
      completed: boolean
    }

// ── Adaptive Mission Feedback types ────────────────────────────────────────

export type FeedbackState =
  | 'not_started'
  | 'attempted'
  | 'checking'
  | 'failed'
  | 'passed'

export type ErrorCategory =
  | 'syntax_error'
  | 'type_error'
  | 'wrong_output'
  | 'missing_output'
  | 'empty_code'
  | 'forbidden_import'
  | 'timeout'
  | 'connection_error'
  | 'unknown'

export interface AdaptiveFeedbackConfig {
  /** Short hint shown before first attempt (1 line) */
  preAttemptHint?: DialogueLine[]
  /** Full post-error dialogue shown progressively on failure */
  failDialogue?: DialogueLine[]
  /** Success celebration (2 lines max) */
  successDialogue?: DialogueLine[]
  /** The mission's character for contextual hints */
  character: Character
  /** Expected output for contextual error hints */
  expectedOutput?: string
}
