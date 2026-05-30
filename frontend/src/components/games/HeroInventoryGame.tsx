import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DialogueBubble from '../DialogueBubble'

interface Props {
  onComplete: (score: number) => Promise<void>
}

const ITEMS = [
  { id: 'key', name: 'золотой ключ', icon: 'key', desc: 'Ключ от выходных ворот Башни Багуса.' },
  { id: 'potion', name: 'зелье лечения', icon: 'healing', desc: 'Флакон с бурлящей красной жидкостью.' },
  { id: 'shield', name: 'щит стража', icon: 'shield', desc: 'Тяжёлый кованый щит с гербом Ва.' },
  { id: 'note', name: 'старая записка', icon: 'description', desc: 'Листок бумаги с надписью «Ксю была тут».' },
  { id: 'shoe', name: 'пыльный башмак', icon: 'footprint', desc: 'Обычный рваный башмак, покрытый пылью.' },
]

export default function HeroInventoryGame({ onComplete }: Props) {
  const navigate = useNavigate()
  const [inventory, setInventory] = useState<string[]>([])
  const [currentEncounter, setCurrentEncounter] = useState<typeof ITEMS[0] | null>(null)
  const [logs, setLogs] = useState<string[]>(['>>> inventory = []'])
  const [roomsSearched, setRoomsSearched] = useState(0)
  const [isWon, setIsWon] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSearchRoom = () => {
    setMessage(null)
    const item = ITEMS[Math.floor(Math.random() * ITEMS.length)]
    setCurrentEncounter(item)
    setRoomsSearched((prev) => prev + 1)
    setLogs((prev) => [
      ...prev,
      `>>> # Комната ${roomsSearched + 1} исследована`,
      `>>> found_item = "${item.name}"`,
    ])
  }

  const handleTakeItem = () => {
    if (!currentEncounter) return

    if (inventory.length >= 4) {
      setMessage('Рюкзак полон! Выброси что-нибудь, чтобы взять новый предмет.')
      setLogs((prev) => [...prev, `>>> # Ошибка: Рюкзак полон!`])
      return
    }

    if (inventory.includes(currentEncounter.name)) {
      setMessage(`Предмет «${currentEncounter.name}» уже есть в инвентаре!`)
      return
    }

    const nextInv = [...inventory, currentEncounter.name]
    setInventory(nextInv)
    setLogs((prev) => [
      ...prev,
      `>>> inventory.append("${currentEncounter.name}")`,
      `>>> print(inventory)  # -> ${JSON.stringify(nextInv)}`,
    ])
    setCurrentEncounter(null)
  }

  const handleLeaveItem = () => {
    if (!currentEncounter) return
    setLogs((prev) => [...prev, `>>> # Предмет "${currentEncounter.name}" оставлен в комнате`])
    setCurrentEncounter(null)
  }

  const handleRemoveItem = (itemName: string) => {
    const nextInv = inventory.filter((item) => item !== itemName)
    setInventory(nextInv)
    setLogs((prev) => [
      ...prev,
      `>>> inventory.remove("${itemName}")`,
      `>>> print(inventory)  # -> ${JSON.stringify(nextInv)}`,
    ])
  }

  const handleEscape = () => {
    setLogs((prev) => [
      ...prev,
      `>>> # Попытка побега...`,
      `>>> if "золотой ключ" in inventory:`,
    ])

    if (inventory.includes('золотой ключ')) {
      setIsWon(true)
      setLogs((prev) => [...prev, `>>>     print("Побег успешен!")`])
    } else {
      setMessage('Дверь заперта! Тебе нужен золотой ключ в инвентаре.')
      setLogs((prev) => [...prev, `>>>     print("Дверь заперта! Нужен ключ.")`])
    }
  }

  const handleFinish = async () => {
    setIsSubmitting(true)
    await onComplete(100)
    setIsSubmitting(false)
    navigate('/')
  }

  return (
    <div className="w-full bg-white border border-outline-variant rounded-2xl p-6 shadow-sm flex flex-col gap-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <span className="material-symbols-outlined text-secondary text-3xl">backpack</span>
        <div>
          <h3 className="font-display text-[22px] font-bold text-on-surface">Мини-игра: «Инвентарь героя»</h3>
          <p className="font-sans text-[14px] text-on-surface-variant">
            Используй списки Python для сбора предметов! Отыщи «золотой ключ», чтобы сбежать из подземелья.
          </p>
        </div>
      </div>

      <DialogueBubble
        character="ksyu"
        text="Списки — это фундамент хранения данных. В этой игре рюкзак героя — обычный список. Ты можешь добавлять предметы через `append()` и убирать их через `remove()`. Ищи золотой ключ и беги к выходу!"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start mt-2">
        {/* Left column: Encounter & Exploration */}
        <div className="flex flex-col gap-4">
          {/* Dungeon Room Card */}
          <div className="bg-surface-container-low border border-outline-variant/30 rounded-xl p-5 shadow-sm min-h-[220px] flex flex-col justify-center">
            {isWon ? (
              <div className="text-center py-4 flex flex-col items-center gap-2">
                <span className="material-symbols-outlined text-green-500 text-5xl animate-bounce">door_open</span>
                <span className="font-display font-extrabold text-[18px]">Выход найден!</span>
                <span className="font-sans text-[14px] text-on-surface-variant">
                  Вы применили золотой ключ и открыли массивные ворота!
                </span>
              </div>
            ) : currentEncounter ? (
              <div className="flex flex-col gap-4 animate-fade-in">
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 bg-secondary/10 text-secondary rounded-xl flex items-center justify-center">
                    <span className="material-symbols-outlined text-3xl">{currentEncounter.icon}</span>
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-secondary uppercase tracking-wider">Найдено в комнате</span>
                    <h4 className="font-display font-extrabold text-[18px] text-on-surface leading-tight mt-0.5">{currentEncounter.name}</h4>
                    <p className="font-sans text-[13px] text-on-surface-variant mt-1">{currentEncounter.desc}</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 mt-2">
                  <button
                    onClick={handleTakeItem}
                    className="py-2.5 rounded-lg bg-secondary text-white font-display font-bold text-[14px] hover:brightness-105 active:scale-[0.98] transition-all flex items-center justify-center gap-1"
                  >
                    <span className="material-symbols-outlined text-[18px]">add_circle</span>
                    <span>Взять (append)</span>
                  </button>
                  <button
                    onClick={handleLeaveItem}
                    className="py-2.5 rounded-lg border-2 border-outline-variant text-on-surface-variant font-display font-bold text-[14px] hover:bg-surface-container active:scale-[0.98] transition-all flex items-center justify-center gap-1"
                  >
                    <span className="material-symbols-outlined text-[18px]">close</span>
                    <span>Оставить</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center py-6 flex flex-col items-center gap-4">
                <span className="material-symbols-outlined text-4xl text-outline animate-pulse">location_searching</span>
                <div>
                  <h5 className="font-display font-bold text-[16px] text-on-surface">Комната пуста</h5>
                  <p className="font-sans text-[13px] text-on-surface-variant mt-0.5">Исследуйте следующую комнату подземелья.</p>
                </div>
                <button
                  onClick={handleSearchRoom}
                  className="px-6 py-3 bg-primary text-white rounded-lg font-display font-bold hover:opacity-95 active:scale-[0.98] transition-all flex items-center gap-2 shadow-sm"
                >
                  <span className="material-symbols-outlined text-[20px]">explore</span>
                  <span>Исследовать комнату</span>
                </button>
              </div>
            )}
          </div>

          {/* Feedback/Messages */}
          {message && (
            <div className="bg-amber-50 border border-amber-200 text-amber-800 text-[13px] font-sans px-4 py-3 rounded-lg flex items-start gap-2">
              <span className="material-symbols-outlined text-[18px] shrink-0 mt-0.5">info</span>
              <span>{message}</span>
            </div>
          )}
        </div>

        {/* Right column: Inventory Grid & CLI */}
        <div className="flex flex-col gap-4">
          {/* Inventory board */}
          <div className="bg-white border-2 border-outline-variant rounded-xl p-5 shadow-sm">
            <h4 className="font-display font-bold text-[16px] text-on-surface mb-3 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <span className="material-symbols-outlined text-secondary">backpack</span>
                Рюкзак героя (inventory)
              </span>
              <span className="text-[12px] font-bold text-outline-variant">{inventory.length} / 4 ячеек</span>
            </h4>

            {inventory.length === 0 ? (
              <div className="border-2 border-dashed border-outline-variant rounded-xl p-6 text-center text-outline-variant text-[13px] font-sans">
                Инвентарь пуст. Найдите и возьмите предметы!
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-3">
                {inventory.map((item, index) => {
                  const details = ITEMS.find((i) => i.name === item) || { icon: 'deployed_code_account', desc: 'Предмет' }
                  return (
                    <div key={index} className="flex items-center justify-between p-3 bg-surface-container-low border border-outline-variant/30 rounded-xl">
                      <div className="flex items-center gap-2 overflow-hidden">
                        <span className="material-symbols-outlined text-secondary shrink-0">{details.icon}</span>
                        <span className="font-sans text-[13.5px] font-semibold text-on-surface truncate">{item}</span>
                      </div>
                      <button
                        onClick={() => handleRemoveItem(item)}
                        className="text-outline hover:text-red-500 hover:bg-red-50 p-1 rounded transition-all"
                        title="Выбросить предмет"
                      >
                        <span className="material-symbols-outlined text-[18px]">delete</span>
                      </button>
                    </div>
                  )
                })}
              </div>
            )}

            {/* Escape action */}
            {!isWon && (
              <button
                onClick={handleEscape}
                className="mt-4 w-full py-3.5 bg-secondary text-white font-display font-bold text-[15px] rounded-lg hover:brightness-105 active:scale-[0.98] transition-all flex items-center justify-center gap-2 shadow-sm"
              >
                <span className="material-symbols-outlined text-[20px]">door_open</span>
                <span>Сбежать к воротам</span>
              </button>
            )}
          </div>

          {/* Console logs */}
          <div className="flex flex-col gap-1.5">
            <span className="font-sans text-[11px] font-bold uppercase tracking-wider text-outline">Интерпретатор списков</span>
            <div className="w-full h-[150px] bg-[#1E1E1E] text-[#D4D4D4] font-mono text-[12.5px] p-4 rounded-xl shadow-inner overflow-y-auto flex flex-col gap-1.5 border border-[#333333]">
              {logs.map((log, index) => {
                let colorClass = 'text-neutral-400'
                if (log.startsWith('>>> #')) colorClass = 'text-green-500 font-medium'
                else if (log.startsWith('>>>')) colorClass = 'text-sky-400'
                return (
                  <div key={index} className={colorClass}>
                    {log}
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Win section */}
      {isWon && (
        <section className="p-5 rounded-xl border-2 border-green-300 bg-green-50/50 animate-fade-in flex flex-col gap-3 items-center text-center">
          <span className="material-symbols-outlined text-4xl text-green-600">workspace_premium</span>
          <div>
            <h4 className="font-display font-bold text-[18px] text-on-surface">Испытание успешно пройдено!</h4>
            <p className="font-sans text-[14px] text-on-surface-variant mt-1 max-w-[500px]">
              Ключ подошёл, и вы успешно покинули подземелье. Ксю машет вам рукой, приглашая в финальную часть курса: Башню Алгоритмов!
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
