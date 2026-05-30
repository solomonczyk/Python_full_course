import { useParams, useNavigate } from 'react-router-dom'
import { useProgressContext } from '../hooks/ProgressContext'
import HeroCheckGame from '../components/games/HeroCheckGame'
import DiceOfFateGame from '../components/games/DiceOfFateGame'
import HeroInventoryGame from '../components/games/HeroInventoryGame'
import EscapeBagusTowerGame from '../components/games/EscapeBagusTowerGame'

export default function MiniGamePage() {
  const { part: partStr } = useParams<{ part: string }>()
  const navigate = useNavigate()
  const { markComplete } = useProgressContext()
  const part = Number(partStr)

  const handleGameComplete = async (score: number) => {
    // Save to backend with ID mini-game-1, mini-game-2, etc.
    try {
      await markComplete(`mini-game-${part}`, score)
    } catch (e) {
      console.error('Error saving progress:', e)
    }
  }

  const renderGame = () => {
    switch (part) {
      case 1:
        return <HeroCheckGame onComplete={handleGameComplete} />
      case 2:
        return <DiceOfFateGame onComplete={handleGameComplete} />
      case 3:
        return <HeroInventoryGame onComplete={handleGameComplete} />
      case 4:
        return <EscapeBagusTowerGame onComplete={handleGameComplete} />
      default:
        return (
          <div className="text-center text-error p-6 bg-white rounded-2xl border border-outline-variant">
            <span className="material-symbols-outlined text-5xl mb-2">error</span>
            <p>Испытание не найдено</p>
          </div>
        )
    }
  }

  return (
    <div className="w-full max-w-[800px] flex flex-col gap-6 animate-fade-in">
      {/* Header bar */}
      <section className="flex items-center justify-between py-2 border-b border-outline-variant/30">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-1.5 text-on-surface-variant hover:text-secondary font-sans text-[14px] font-bold transition-colors"
        >
          <span className="material-symbols-outlined text-[18px]">arrow_back</span>
          <span>На карту курса</span>
        </button>
        <div className="flex items-center gap-1.5 font-sans text-[13px] font-bold text-secondary uppercase tracking-wider">
          <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>stadia_controller</span>
          <span>Часть {part} · Мини-игра</span>
        </div>
      </section>

      {/* Game view container */}
      <main className="w-full min-h-[500px]">
        {renderGame()}
      </main>
    </div>
  )
}
