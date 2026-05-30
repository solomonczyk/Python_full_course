import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DialogueBubble from '../DialogueBubble'

interface Props {
  onComplete: (score: number) => Promise<void>
}

export default function DiceOfFateGame({ onComplete }: Props) {
  const navigate = useNavigate()
  const [selectedDice, setSelectedDice] = useState<1 | 2 | null>(null)
  const [moves, setMoves] = useState(0)
  const [isRolling, setIsRolling] = useState(false)
  const [logs, setLogs] = useState<string[]>([])
  const [rollResult, setRollResult] = useState<number | null>(null)
  const [rollHistory, setRollHistory] = useState<number[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleRoll = () => {
    if (selectedDice === null) {
      setLogs(['Ошибка: Выберите один из двух кубиков!'])
      return
    }

    setIsRolling(true)
    setRollResult(null)
    setLogs((prev) => [...prev, `>>> # Бросок магического кубика №${selectedDice}...`])

    setTimeout(() => {
      let roll = 0
      if (selectedDice === 1) {
        // Risky: -2 to 6
        roll = Math.floor(Math.random() * 9) - 2
      } else {
        // Safe: 1 to 4
        roll = Math.floor(Math.random() * 4) + 1
      }

      setRollResult(roll)
      const nextMoves = Math.max(0, moves + roll)
      setMoves(nextMoves)
      setRollHistory((prev) => [...prev, roll])
      setIsRolling(false)

      const diceLogs = [
        `>>> import random`,
        selectedDice === 1
          ? `>>> roll = random.randint(-2, 6)`
          : `>>> roll = random.randint(1, 4)`,
        `>>> # Результат броска: ${roll}`,
        `>>> moves = max(0, moves + (${roll}))`,
        `>>> # Всего ходов: ${nextMoves}`,
      ]

      setLogs((prev) => [...prev, ...diceLogs])
    }, 1200)
  }

  const handleFinish = async () => {
    setIsSubmitting(true)
    await onComplete(100)
    setIsSubmitting(false)
    navigate('/')
  }

  const isWon = moves >= 10

  return (
    <div className="w-full bg-white border border-outline-variant rounded-2xl p-6 shadow-sm flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <span className="material-symbols-outlined text-tertiary text-3xl">casino</span>
        <div>
          <h3 className="font-display text-[22px] font-bold text-on-surface">Мини-игра: «Кубик судьбы»</h3>
          <p className="font-sans text-[14px] text-on-surface-variant">
            Бросай кубики и накапливай ходы с помощью генератора случайных чисел! Набери 10 ходов для победы.
          </p>
        </div>
      </div>

      <DialogueBubble
        character="da"
        text="Кубик судьбы — это отличный пример случайности в играх. Выбери кубик: Кубик 1 даёт от -2 до 6 ходов (рисковый!), а Кубик 2 стабильно даёт от 1 до 4 ходов. Твоя цель — добраться до 10 ходов!"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start mt-2">
        {/* Dice Selector Panel */}
        <div className="flex flex-col gap-4 bg-surface-container-low p-5 rounded-xl border border-outline-variant/30">
          <h4 className="font-display font-bold text-[16px] text-on-surface">Магические кубики</h4>

          <div className="grid grid-cols-2 gap-4">
            {/* Dice 1 (Risky) */}
            <button
              onClick={() => setSelectedDice(1)}
              disabled={isRolling || isWon}
              className={`p-4 rounded-xl border-2 flex flex-col items-center gap-2 transition-all active:scale-[0.98]
                ${selectedDice === 1
                  ? 'border-tertiary bg-amber-50/50 shadow-sm'
                  : 'border-outline-variant hover:border-tertiary bg-white'
                } ${isWon ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <span className="material-symbols-outlined text-4xl text-tertiary animate-pulse">explore_hazard</span>
              <span className="font-display font-bold text-[15px]">Кубик №1</span>
              <span className="font-sans text-[11px] text-center text-on-surface-variant leading-tight">
                Рисковый<br />(-2 ... +6 ходов)
              </span>
            </button>

            {/* Dice 2 (Safe) */}
            <button
              onClick={() => setSelectedDice(2)}
              disabled={isRolling || isWon}
              className={`p-4 rounded-xl border-2 flex flex-col items-center gap-2 transition-all active:scale-[0.98]
                ${selectedDice === 2
                  ? 'border-secondary bg-blue-50/50 shadow-sm'
                  : 'border-outline-variant hover:border-secondary bg-white'
                } ${isWon ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <span className="material-symbols-outlined text-4xl text-secondary">shield</span>
              <span className="font-display font-bold text-[15px]">Кубик №2</span>
              <span className="font-sans text-[11px] text-center text-on-surface-variant leading-tight">
                Безопасный<br />(+1 ... +4 ходов)
              </span>
            </button>
          </div>

          <button
            onClick={handleRoll}
            disabled={isRolling || selectedDice === null || isWon}
            className="mt-2 w-full py-3.5 rounded-lg bg-tertiary text-on-tertiary font-display font-bold hover:opacity-95 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
          >
            {isRolling ? (
              <>
                <span className="material-symbols-outlined text-[20px] animate-spin">sync</span>
                <span>Кубик крутится...</span>
              </>
            ) : (
              <>
                <span className="material-symbols-outlined text-[20px]">casino</span>
                <span>Бросить кубик</span>
              </>
            )}
          </button>
        </div>

        {/* Console & Roll animation */}
        <div className="flex flex-col gap-4">
          <div className="flex justify-between items-center bg-surface-container px-4 py-3.5 rounded-xl border border-outline-variant/30">
            <div className="flex flex-col">
              <span className="text-[11px] font-bold text-on-surface-variant uppercase tracking-wider">Всего ходов накоплено</span>
              <span className="font-display text-[26px] font-black text-primary leading-tight mt-0.5">{moves} / 10</span>
            </div>
            {rollResult !== null && (
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-display text-[20px] font-extrabold text-white shadow-sm
                ${rollResult > 0 ? 'bg-green-500' : rollResult < 0 ? 'bg-red-500' : 'bg-neutral-500'}`}
              >
                {rollResult > 0 ? `+${rollResult}` : rollResult}
              </div>
            )}
          </div>

          <div className="flex flex-col gap-1.5">
            <span className="font-sans text-[11px] font-bold uppercase tracking-wider text-outline">Журнал выполнения Python</span>
            <div className="w-full h-[180px] bg-[#1E1E1E] text-[#D4D4D4] font-mono text-[13px] p-4 rounded-xl shadow-inner overflow-y-auto flex flex-col gap-1.5 border border-[#333333]">
              {logs.length === 0 ? (
                <span className="text-neutral-500 italic">Сделайте первый бросок для просмотра журнала...</span>
              ) : (
                logs.map((log, index) => {
                  let colorClass = 'text-neutral-400'
                  if (log.startsWith('>>> #')) colorClass = 'text-green-500 font-medium'
                  else if (log.startsWith('>>>')) colorClass = 'text-sky-400'
                  else if (log.includes('Результат броска')) colorClass = 'text-amber-300'
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
      </div>

      {/* Victory Celebration / Game Results */}
      {isWon && (
        <section className="p-5 rounded-xl border-2 border-green-300 bg-green-50/50 animate-fade-in flex flex-col gap-3 items-center text-center">
          <span className="material-symbols-outlined text-4xl text-green-600">workspace_premium</span>
          <div>
            <h4 className="font-display font-bold text-[18px] text-on-surface">Ура! Условия победы выполнены!</h4>
            <p className="font-sans text-[14px] text-on-surface-variant mt-1 max-w-[500px]">
              Ты накопил {moves} ходов за {rollHistory.length} бросков. Логическая цепочка проверена, и генератор случайных чисел поддался твоей тактике!
            </p>
          </div>
          <button
            onClick={handleFinish}
            disabled={isSubmitting}
            className="px-8 py-3 bg-action-da text-white rounded-xl font-display font-bold hover:brightness-105 active:scale-[0.98] transition-all flex items-center gap-2 shadow-md"
          >
            <span>{isSubmitting ? 'Сохранение...' : 'Завершить испытание'}</span>
            <span className="material-symbols-outlined">done</span>
          </button>
        </section>
      )}
    </div>
  )
}
