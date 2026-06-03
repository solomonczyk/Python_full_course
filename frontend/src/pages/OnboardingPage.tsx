import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { navigateWithFallback } from '../lib/navigation'

const ONBOARDING_KEY = 'pq_onboarding_done'

interface Answers {
  experience: string | null
  goal: string | null
  time: string | null
}

export default function OnboardingPage() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState<Answers>({ experience: null, goal: null, time: null })

  // If already done, redirect
  if (localStorage.getItem(ONBOARDING_KEY)) {
    navigateWithFallback(navigate, '/lesson/1-1', true)
    return null
  }

  const setAndNext = (field: keyof Answers, value: string) => {
    const updated = { ...answers, [field]: value }
    setAnswers(updated)
    if (step < 2) {
      setStep(step + 1)
    } else {
      // Save and redirect
      localStorage.setItem(ONBOARDING_KEY, 'true')
      localStorage.setItem('pq_onboarding', JSON.stringify(updated))
      navigateWithFallback(navigate, '/lesson/1-1', true)
    }
  }

  const questions = [
    {
      title: 'Был ли у тебя опыт программирования?',
      options: [
        { value: 'no', label: 'Нет, Python — мой первый язык', icon: '🌟' },
        { value: 'other', label: 'Писал на других языках', icon: '⚡' },
        { value: 'some', label: 'Немного знаю Python', icon: '🐍' },
      ],
    },
    {
      title: 'Зачем тебе программирование?',
      options: [
        { value: 'understand', label: 'Хочу понять, как это работает', icon: '🧠' },
        { value: 'automate', label: 'Хочу автоматизировать работу', icon: '🤖' },
        { value: 'career', label: 'Хочу перейти в IT', icon: '🚀' },
        { value: 'curious', label: 'Просто интересно', icon: '❓' },
      ],
    },
    {
      title: 'Сколько времени готов уделять в день?',
      options: [
        { value: '15min', label: '~15 минут', icon: '⏱️', sub: 'Пройдёшь курс за ~3 недели' },
        { value: '30min', label: '~30 минут', icon: '⏳', sub: 'Пройдёшь курс за ~10 дней' },
        { value: '1h', label: '1 час и больше', icon: '🔥', sub: 'Пройдёшь курс за 4-5 дней' },
      ],
    },
  ]

  const q = questions[step]

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{ background: '#0f0e17' }}>
      <div className="w-full max-w-lg">
        {/* Step indicator */}
        <div className="flex justify-center gap-2 mb-8">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="w-3 h-3 rounded-full transition-all"
              style={{
                background: i <= step ? '#c9a227' : 'rgba(201,162,39,0.2)',
                transform: i === step ? 'scale(1.3)' : 'scale(1)',
              }}
            />
          ))}
        </div>

        {/* Question */}
        <div className="rounded-xl p-6" style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.15)' }}>
          <h2 className="text-lg font-bold mb-2" style={{ color: '#c9a227' }}>
            {q.title}
          </h2>
          <p className="text-xs mb-6" style={{ color: '#9b98a8' }}>
            Это поможет подобрать темп обучения
          </p>

          <div className="space-y-3">
            {q.options.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setAndNext(step === 0 ? 'experience' : step === 1 ? 'goal' : 'time', opt.value)}
                className="w-full flex items-center gap-4 p-4 rounded-xl text-left cursor-pointer transition-all hover:scale-[1.02] active:scale-[0.99] border-2"
                style={{
                  background: 'rgba(15,14,23,0.8)',
                  borderColor: 'rgba(201,162,39,0.2)',
                  color: '#e8e6f0',
                }}
                onMouseEnter={(e) => e.currentTarget.style.borderColor = '#c9a227'}
                onMouseLeave={(e) => e.currentTarget.style.borderColor = 'rgba(201,162,39,0.2)'}
              >
                <span className="text-2xl">{opt.icon}</span>
                <div>
                  <div className="text-sm font-medium">{opt.label}</div>
                  {'sub' in opt && opt.sub && (
                    <div className="text-[10px] mt-0.5" style={{ color: '#9b98a8' }}>
                      {(opt as any).sub}
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Skip */}
        <div className="text-center mt-6">
          <button
            onClick={() => {
              localStorage.setItem(ONBOARDING_KEY, 'true')
              navigateWithFallback(navigate, '/lesson/1-1', true)
            }}
            className="text-xs cursor-pointer hover:opacity-80"
            style={{ color: '#6b7280', background: 'none', border: 'none' }}
          >
            Пропустить →
          </button>
        </div>
      </div>
    </div>
  )
}
