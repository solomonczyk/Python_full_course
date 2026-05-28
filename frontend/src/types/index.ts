export type Character = 'ksyu' | 'va' | 'da' | 'bagus'

export interface QuizOption {
  id: string
  text: string
  correct: boolean
}

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
  scene_image?: string
}

export interface Lesson extends LessonSummary {
  scene_image?: string
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
