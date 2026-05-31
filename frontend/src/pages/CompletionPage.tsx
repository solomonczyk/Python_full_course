import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useProgress } from '../hooks/useProgress'
import { useLessons } from '../hooks/useApi'
import Certificate from '../components/Certificate'

export default function CompletionPage() {
  const navigate = useNavigate()
  const { progress, completedCount, totalLessons } = useProgress()
  const { lessons } = useLessons()
  const [showCert, setShowCert] = useState(false)

  const total = lessons.length || totalLessons
  const allDone = completedCount >= total

  useEffect(() => {
    if (!allDone && lessons.length > 0) {
      // Not done yet — redirect back
      navigate('/lesson/1-1', { replace: true })
    }
  }, [allDone, lessons.length, navigate])

  // Check for user name
  const nameKey = 'pq_user_name'
  const [userName, setUserName] = useState(() => localStorage.getItem(nameKey) || '')

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserName(e.target.value)
    localStorage.setItem(nameKey, e.target.value)
  }

  if (!allDone) return null

  const skills = [
    'Писать программы на Python с нуля',
    'Работать с числами, строками, списками',
    'Строить логику: условия, циклы, флаги',
    'Создавать чат-ботов, игры, таск-менеджеры',
    'Понимать чужой код на Python',
    'Различать изменяемые и неизменяемые типы',
    'Использовать ссылки, копирование, deepcopy',
  ]

  const nextSteps = [
    {
      title: '🌐 Веб-разработка',
      desc: 'FastAPI, Django — делай сайты и API',
      link: 'https://fastapi.tiangolo.com/tutorial/',
    },
    {
      title: '📊 Данные и аналитика',
      desc: 'pandas, Jupyter — работай с таблицами и графиками',
      link: 'https://www.kaggle.com/learn',
    },
    {
      title: '🤖 Автоматизация',
      desc: 'selenium, requests — роботы для рутины',
      link: 'https://automatetheboringstuff.com/',
    },
    {
      title: '🧠 Алгоритмы',
      desc: 'LeetCode, Codeforces — прокачай логику',
      link: 'https://leetcode.com/problemset/all/',
    },
  ]

  return (
    <div className="min-h-screen p-4" style={{ background: '#0f0e17' }}>
      <div className="max-w-2xl mx-auto space-y-6">
        {/* Congratulations */}
        <div
          className="rounded-xl p-8 text-center"
          style={{
            background: 'linear-gradient(135deg, rgba(0,212,170,0.1), rgba(201,162,39,0.1))',
            border: '2px solid #c9a227',
          }}
        >
          <span className="text-6xl block mb-4">🎉</span>
          <h1 className="text-2xl font-bold mb-2" style={{ color: '#c9a227' }}>
            Поздравляем с завершением!
          </h1>
          <p className="text-sm" style={{ color: '#9b98a8' }}>
            Ты прошёл все {total} уроков Python Quest!
          </p>
          <div className="mt-4 inline-block px-4 py-2 rounded-full text-sm font-bold" style={{ background: 'rgba(0,212,170,0.15)', color: '#00d4aa', border: '1px solid #00d4aa' }}>
            Твой уровень: A2+ (уверенный начинающий)
          </div>
        </div>

        {/* Name for certificate */}
        <div
          className="rounded-xl p-4"
          style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.15)' }}
        >
          <label className="text-xs font-bold block mb-2" style={{ color: '#9b98a8' }}>
            Имя для сертификата:
          </label>
          <div className="flex gap-2">
            <input
              value={userName}
              onChange={handleNameChange}
              placeholder="Введи своё имя"
              className="flex-1 p-2 rounded-lg text-xs font-mono outline-none"
              style={{ background: '#0f0e17', color: '#e8e6f0', border: '1px solid rgba(0,212,170,0.2)' }}
            />
            <button
              onClick={() => setShowCert(!showCert)}
              disabled={!userName.trim()}
              className="px-4 py-2 rounded-lg text-xs font-bold cursor-pointer border-none disabled:opacity-50"
              style={{ background: '#c9a227', color: '#0f0e17' }}
            >
              {showCert ? 'Скрыть' : 'Показать сертификат'}
            </button>
          </div>
        </div>

        {showCert && userName.trim() && <Certificate userName={userName} />}

        {/* Skills checklist */}
        <div
          className="rounded-xl p-4"
          style={{ background: '#1a1924', border: '1px solid rgba(0,212,170,0.15)' }}
        >
          <h2 className="text-sm font-bold mb-3" style={{ color: '#00d4aa' }}>
            ✅ Что ты теперь умеешь
          </h2>
          <ul className="space-y-2">
            {skills.map((s, i) => (
              <li key={i} className="flex items-center gap-2 text-xs" style={{ color: '#e8e6f0' }}>
                <span style={{ color: '#00d4aa' }}>✓</span>
                {s}
              </li>
            ))}
          </ul>
        </div>

        {/* What's next */}
        <div
          className="rounded-xl p-4"
          style={{ background: '#1a1924', border: '1px solid rgba(201,162,39,0.15)' }}
        >
          <h2 className="text-sm font-bold mb-3" style={{ color: '#c9a227' }}>
            🗺️ Что изучать дальше
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {nextSteps.map((step) => (
              <a
                key={step.title}
                href={step.link}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 rounded-lg text-xs transition-all hover:scale-105"
                style={{
                  background: '#0f0e17',
                  border: '1px solid rgba(201,162,39,0.15)',
                  color: '#e8e6f0',
                  textDecoration: 'none',
                }}
              >
                <div className="font-bold mb-1">{step.title}</div>
                <div style={{ color: '#9b98a8' }}>{step.desc}</div>
              </a>
            ))}
          </div>
        </div>

        {/* Share */}
        <div className="text-center">
          <button
            onClick={() => {
              const text = `Я прошёл Python Quest! 🐍 Уровень A2+`
              if (navigator.share) {
                navigator.share({ title: 'Python Quest', text }).catch(() => {})
              } else {
                navigator.clipboard.writeText(text).catch(() => {})
                alert('Скопировано в буфер!')
              }
            }}
            className="px-6 py-3 rounded-lg text-xs font-bold cursor-pointer border-none"
            style={{ background: 'rgba(0,212,170,0.15)', color: '#00d4aa', border: '1px solid #00d4aa' }}
          >
            📤 Поделиться результатом
          </button>
        </div>

        {/* Back to lessons */}
        <div className="text-center pb-8">
          <button
            onClick={() => navigate('/lesson/1-1')}
            className="text-xs cursor-pointer hover:opacity-80"
            style={{ color: '#6b7280', background: 'none', border: 'none' }}
          >
            ← Вернуться к урокам
          </button>
        </div>
      </div>
    </div>
  )
}
