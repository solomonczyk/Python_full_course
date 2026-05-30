import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DialogueBubble from '../DialogueBubble'

interface Props {
  onComplete: (score: number) => Promise<void>
}

export default function HeroCheckGame({ onComplete }: Props) {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [age, setAge] = useState('18')
  const [strength, setStrength] = useState('10')
  const [isRunning, setIsRunning] = useState(false)
  const [logs, setLogs] = useState<string[]>([])
  const [currentStep, setCurrentStep] = useState(0)
  const [ratingResult, setRatingResult] = useState<number | null>(null)
  const [isSuccess, setIsSuccess] = useState<boolean | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleRun = () => {
    if (!name.trim()) {
      setLogs(['Ошибка: Имя героя не может быть пустым!'])
      return
    }
    const ageNum = parseInt(age, 10)
    const strNum = parseInt(strength, 10)
    if (isNaN(ageNum) || ageNum <= 0) {
      setLogs(['Ошибка: Некорректный возраст!'])
      return
    }
    if (isNaN(strNum) || strNum < 0) {
      setLogs(['Ошибка: Некорректная сила!'])
      return
    }

    setIsRunning(true)
    setLogs([])
    setCurrentStep(0)
    setRatingResult(null)
    setIsSuccess(null)

    const codeSteps = [
      `>>> name = "${name}"`,
      `>>> age = ${ageNum}`,
      `>>> strength = ${strNum}`,
      `>>> rating = age * 2 + strength`,
      `>>> # Проверка рейтинга...`,
    ]

    let step = 0
    const interval = setInterval(() => {
      if (step < codeSteps.length) {
        setLogs((prev) => [...prev, codeSteps[step]])
        step++
        setCurrentStep(step)
      } else {
        clearInterval(interval)
        const calcRating = ageNum * 2 + strNum
        setRatingResult(calcRating)
        const passed = calcRating >= 50
        setIsSuccess(passed)
        setLogs((prev) => [
          ...prev,
          `Рассчитанный рейтинг героя: ${calcRating}`,
          passed
            ? `[УСПЕХ] Рейтинг ${calcRating} >= 50. Вход в мир Python РАЗРЕШЕН!`
            : `[ОТКАЗ] Рейтинг ${calcRating} < 50. Увеличь возраст или силу и попробуй снова!`,
        ])
      }
    }, 800)
  }

  const handleFinish = async () => {
    setIsSubmitting(true)
    await onComplete(100)
    setIsSubmitting(false)
    navigate('/')
  }

  return (
    <div className="w-full bg-white border border-outline-variant rounded-2xl p-6 shadow-sm flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <span className="material-symbols-outlined text-action-da text-3xl">verified_user</span>
        <div>
          <h3 className="font-display text-[22px] font-bold text-on-surface">Мини-игра: «Проверка героя»</h3>
          <p className="font-sans text-[14px] text-on-surface-variant">
            Перед входом в мир Python стоит Страж Ва. Настрой своего героя так, чтобы пройти проверку!
          </p>
        </div>
      </div>

      {/* Story Introduction Dialogue */}
      <DialogueBubble
        character="va"
        text="Перед входом в замок ты должен зарегистрироваться. Я написал скрипт на Python, который рассчитывает твой рейтинг: `rating = age * 2 + strength`. Пропускной порог — 50 очков."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start mt-2">
        {/* Form settings */}
        <div className="flex flex-col gap-4 bg-surface-container-low p-5 rounded-xl border border-outline-variant/30">
          <h4 className="font-display font-bold text-[16px] text-on-surface mb-2">Настройки персонажа</h4>
          
          <div className="flex flex-col gap-1.5">
            <label className="font-sans text-[13px] font-bold text-on-surface-variant">Имя героя</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Введите имя..."
              disabled={isRunning && isSuccess === null}
              className="px-4 py-2.5 rounded-lg border border-outline bg-white font-sans text-[15px] focus:outline-none focus:border-primary"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="font-sans text-[13px] font-bold text-on-surface-variant flex justify-between">
              <span>Возраст героя:</span>
              <span className="text-secondary font-mono">{age}</span>
            </label>
            <input
              type="range"
              min="5"
              max="40"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              disabled={isRunning && isSuccess === null}
              className="accent-primary"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="font-sans text-[13px] font-bold text-on-surface-variant flex justify-between">
              <span>Сила героя:</span>
              <span className="text-secondary font-mono">{strength}</span>
            </label>
            <input
              type="range"
              min="1"
              max="30"
              value={strength}
              onChange={(e) => setStrength(e.target.value)}
              disabled={isRunning && isSuccess === null}
              className="accent-primary"
            />
          </div>

          <button
            onClick={handleRun}
            disabled={isRunning && isSuccess === null}
            className="mt-2 w-full py-3 rounded-lg bg-primary text-on-primary font-display font-bold hover:opacity-95 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
          >
            <span className="material-symbols-outlined text-[20px]">play_arrow</span>
            <span>Запустить скрипт</span>
          </button>
        </div>

        {/* Python Console Emulator */}
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <span className="font-sans text-[12px] font-bold uppercase tracking-wider text-outline">Эмулятор Терминала Python</span>
            {isRunning && isSuccess === null && (
              <span className="flex items-center gap-1 text-[12px] text-secondary">
                <span className="w-2 h-2 bg-secondary rounded-full animate-ping" />
                Выполнение...
              </span>
            )}
          </div>

          <div className="w-full h-[255px] bg-[#1E1E1E] text-[#D4D4D4] font-mono text-[13px] p-4 rounded-xl shadow-inner overflow-y-auto flex flex-col gap-2 border border-[#333333]">
            {logs.length === 0 ? (
              <span className="text-neutral-500 italic">Нажмите «Запустить скрипт», чтобы увидеть выполнение кода...</span>
            ) : (
              logs.map((log, index) => {
                let colorClass = 'text-neutral-400'
                if (log.startsWith('>>>')) colorClass = 'text-sky-400'
                else if (log.startsWith('[УСПЕХ]')) colorClass = 'text-green-400 font-bold'
                else if (log.startsWith('[ОТКАЗ]') || log.startsWith('Ошибка:')) colorClass = 'text-red-400 font-bold'
                else if (log.startsWith('Рассчитанный')) colorClass = 'text-amber-300'

                return (
                  <div key={index} className={colorClass}>
                    {log}
                  </div>
                )
              })
            )}
          </div>
        </div>
      </div>

      {/* Victory / Defeat card */}
      {isSuccess !== null && (
        <section className={`p-5 rounded-xl border-2 animate-fade-in flex flex-col gap-3 items-center text-center
          ${isSuccess
            ? 'border-green-300 bg-green-50/50'
            : 'border-red-300 bg-red-50/50'
          }`}
        >
          <span className="material-symbols-outlined text-4xl">
            {isSuccess ? 'workspace_premium' : 'warning'}
          </span>
          <div>
            <h4 className="font-display font-bold text-[18px]">
              {isSuccess
                ? `Поздравляем, ${name}! Ты прошёл проверку!`
                : 'Недостаточно рейтинга для прохода!'}
            </h4>
            <p className="font-sans text-[14px] text-on-surface-variant mt-1 max-w-[500px]">
              {isSuccess
                ? `Твой итоговый рейтинг равен ${ratingResult}. Этого с запасом хватает для входа в мир Python. Страж Ва кивает и открывает перед тобой ворота.`
                : `Твой итоговый рейтинг составил ${ratingResult}. Это меньше необходимых 50 очков. Увеличь ползунками возраст героя (умножается на 2!) или его силу, чтобы перешагнуть порог.`}
            </p>
          </div>
          {isSuccess ? (
            <button
              onClick={handleFinish}
              disabled={isSubmitting}
              className="mt-2 px-8 py-3 bg-action-da text-white rounded-xl font-display font-bold hover:brightness-105 active:scale-[0.98] transition-all flex items-center gap-2 shadow-md"
            >
              <span>{isSubmitting ? 'Сохранение...' : 'Завершить испытание'}</span>
              <span className="material-symbols-outlined">done</span>
            </button>
          ) : (
            <div className="text-[12px] font-bold text-red-600 uppercase mt-1 tracking-wider">
              Перенастрой параметры и нажми кнопку запуска!
            </div>
          )}
        </section>
      )}
    </div>
  )
}
