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
          <div className="text-center p-6 rounded-xl" style={{ background: '#1a1924', border: '1px solid rgba(255,107,107,0.3)', color: '#ff6b6b' }}>
            <span className="material-symbols-outlined text-5xl mb-2">error</span>
            <p>Challenge not found</p>
          </div>
        )
    }
  }

  return (
    <div className="w-full max-w-[800px] flex flex-col gap-6 animate-fade-in">
      {/* Header bar */}
      <section className="flex items-center justify-between py-2" style={{ borderBottom: '1px solid rgba(201,162,39,0.15)' }}>
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-1.5 text-xs font-bold transition-all hover:scale-105"
          style={{ color: '#9b98a8' }}
        >
          <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 0" }}>arrow_back</span>
          <span>Back to Course</span>
        </button>
        <div className="flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider" style={{ color: '#00d4aa' }}>
          <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>stadia_controller</span>
          <span>Part {part} · Mini-Game</span>
        </div>
      </section>

      {/* Game view container */}
      <main className="w-full min-h-[500px]">
        {renderGame()}
      </main>
    </div>
  )
}
