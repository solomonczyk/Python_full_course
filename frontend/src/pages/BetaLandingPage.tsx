import { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { trackEvent } from '../lib/analytics'
import {
  getOrCreateParticipantCode,
  getStoredParticipantCode,
  storeParticipantCode,
  isValidCodeFormat,
} from '../lib/participantIdentity'
import { loadBetaProgress, initBetaProgress, clearBetaProgress, saveBetaProgress } from '../lib/progressStore'
import { restoreBetaProgress } from '../lib/progressSync'
import { createBackendProgress } from '../lib/backendProgressStore'
import ParticipantCodePanel from '../components/ParticipantCodePanel'
import ResumeProgressCard from '../components/ResumeProgressCard'
import type { BetaProgressData } from '../types'

// ── Flow state ──────────────────────────────────────────────────────────────

type FlowState =
  | 'idle'
  | 'creating_code'
  | 'code_shown'
  | 'entering_code'
  | 'restoring'
  | 'restored'

// ── FAQ data ─────────────────────────────────────────────────────────────

const FAQ_ITEMS = [
  {
    q: 'Что такое Python Quest?',
    a: 'Python Quest — это игровой курс программирования на Python для новичков. Вы изучаете Python через историю, персонажей и миссии: сначала герой учится говорить через print(), потом хранить значения, считать, принимать решения и проходить всё более сложные задания. Это не сухие лекции — каждая тема вплетена в сюжет.'
  },
  {
    q: 'Нужно ли устанавливать Python?',
    a: 'Нет. Всё работает прямо в браузере — редактор кода, проверка миссий, подсказки. Вам не нужно ничего устанавливать, настраивать или регистрироваться. Просто откройте страницу и начните.'
  },
  {
    q: 'Подходит ли для полного новичка?',
    a: 'Да. Курс начинается с самых основ: первая миссия знакомит с командой print(). Никакого опыта программирования не требуется. Все понятия объясняются через аналогии и историю.'
  },
  {
    q: 'Что значит beta?',
    a: 'Продукт уже можно проходить и тестировать — все уроки, миссии, повторения и квесты работают. Прогресс сохраняется на сервере: вы можете продолжить обучение на другом устройстве, введя свой beta-код. Некоторые коммерческие функции (оплата, родительский дашборд) ещё не финальные. Это возможность попробовать курс бесплатно и повлиять на его развитие.'
  },
  {
    q: 'Что делать, если ребёнок ошибается?',
    a: 'Каждая миссия включает подсказки при ошибках. Курс спроектирован так, чтобы ошибка была частью обучения: игровой персонаж помогает понять, что пошло не так, и попробовать снова. Мы не наказываем за ошибки — мы через них учим.'
  },
  {
    q: 'Когда будет платная версия?',
    a: 'Точная дата пока не определена. В beta-версии весь функционал доступен бесплатно. О запуске платной версии будет объявлено заранее — вы сможете принять решение после полного тестирования.'
  },
  {
    q: 'Как я могу повлиять на развитие курса?',
    a: 'После прохождения уроков вы можете отправить обратную связь через встроенный чат. Ваши замечания помогают улучшать объяснения, миссии и игровой баланс до финального релиза.'
  },
]

// ── How it works steps ────────────────────────────────────────────────────

const STEPS = [
  { number: 1, title: 'Читаем историю', description: 'Каждый урок начинается с короткой сюжетной сцены. Герой попадает в новую ситуацию — и ему нужна ваша помощь.' },
  { number: 2, title: 'Разбираем концепцию', description: 'Через простую аналогию и пример кода объясняется новая тема Python. Никакой магии — только понятные правила.' },
  { number: 3, title: 'Выполняем миссию', description: 'Вы пишете код, который решает игровую задачу. Миссия проверяется автоматически — вы сразу видите результат.' },
  { number: 4, title: 'Получаем подсказку', description: 'Если что-то пошло не так — персонаж курса даёт подсказку. Ошибка становится шагом к пониманию.' },
  { number: 5, title: 'Открываем способность', description: 'Каждая пройденная тема добавляет новое умение герою. К концу курса вы соберёте полный арсенал Python.' },
]

// ── FAQ Accordion component ───────────────────────────────────────────────

function AccordionItem({
  item,
  isOpen,
  onToggle,
}: {
  item: { q: string; a: string }
  isOpen: boolean
  onToggle: () => void
}) {
  return (
    <div
      className="rounded-xl overflow-hidden transition-all"
      style={{
        background: '#1a1924',
        border: isOpen ? '1px solid rgba(201,162,39,0.4)' : '1px solid rgba(201,162,39,0.1)',
      }}
    >
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between px-4 py-3.5 text-left cursor-pointer border-none bg-transparent"
        aria-expanded={isOpen}
      >
        <span className="text-sm font-medium pr-4" style={{ color: '#e8e6f0' }}>
          {item.q}
        </span>
        <span
          className="shrink-0 text-lg transition-transform duration-200"
          style={{ color: '#c9a227', transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)' }}
        >
          ▼
        </span>
      </button>
      {isOpen && (
        <div className="px-4 pb-4">
          <p className="text-xs leading-relaxed" style={{ color: '#9b98a8' }}>
            {item.a}
          </p>
        </div>
      )}
    </div>
  )
}

// ── Beta Landing Page ────────────────────────────────────────────────────

export default function BetaLandingPage() {
  const navigate = useNavigate()
  const [openFaq, setOpenFaq] = useState<number | null>(null)
  const [flowState, setFlowState] = useState<FlowState>('idle')
  const [returnCode, setReturnCode] = useState('')
  const [codeError, setCodeError] = useState<string | null>(null)
  const [restoredProgress, setRestoredProgress] = useState<BetaProgressData | null>(null)
  const [hasExistingCode, setHasExistingCode] = useState(false)

  useEffect(() => {
    trackEvent('landing_opened', { source: 'beta_landing', route: '/beta' })
    // Check if user already has a participant code in this browser
    const existing = getStoredParticipantCode()
    setHasExistingCode(!!existing)
  }, [])

  const scrollToHowItWorks = () => {
    const el = document.getElementById('how-it-works')
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }

  const toggleFaq = (idx: number) => {
    setOpenFaq(openFaq === idx ? null : idx)
  }

  // ── New participant flow ─────────────────────────────────────────────

  const handleStartLearning = useCallback(() => {
    setFlowState('creating_code')
    // Generate but delay showing for the animation
    setTimeout(() => {
      getOrCreateParticipantCode()
      setFlowState('code_shown')
    }, 300)
  }, [])

  const handleContinueAfterCode = useCallback(() => {
    const code = getStoredParticipantCode()
    trackEvent('demo_started', { source: 'hero_cta', route: '/lesson/1-1' })
    initBetaProgress()
    // Create backend progress asynchronously (non-blocking)
    if (code) {
      createBackendProgress(code)
    }
    navigate('/lesson/1-1')
  }, [navigate])

  // ── Returning participant flow ───────────────────────────────────────

  const handleEnterCodeClick = useCallback(() => {
    setFlowState('entering_code')
    setReturnCode('')
    setCodeError(null)
    setRestoredProgress(null)
  }, [])

  const handleCodeInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setReturnCode(e.target.value.toUpperCase())
    setCodeError(null)
  }, [])

  const handleRestoreProgress = useCallback(async () => {
    const trimmed = returnCode.trim().toUpperCase()

    if (!isValidCodeFormat(trimmed)) {
      setCodeError('Неверный формат кода. Код должен быть в формате BETA-XXXXXX.')
      return
    }

    // Store the entered code
    const stored = storeParticipantCode(trimmed)
    if (!stored) {
      setCodeError('Не удалось сохранить код. Проверьте формат.')
      return
    }

    // Try backend first, fall back to localStorage
    const result = await restoreBetaProgress(trimmed)
    if (result.source === 'backend' && result.progress) {
      setRestoredProgress(result.progress)
      setFlowState('restored')
      setCodeError(null)
      return
    }

    // Fall back to localStorage
    const progress = loadBetaProgress(trimmed)
    if (progress) {
      setRestoredProgress(progress)
      setFlowState('restored')
      setCodeError(null)
    } else {
      // Code format is valid but no progress found anywhere
      setCodeError('Код не найден. Проверьте код или начните заново.')
      // Remove the stored code since no progress was found
      clearBetaProgress()
    }
  }, [returnCode])

  const handleContinueRestored = useCallback((lessonId: string) => {
    trackEvent('demo_started', { source: 'restored_progress', route: `/lesson/${lessonId}` })
    navigate(`/lesson/${lessonId}`)
  }, [navigate])

  const handleStartFresh = useCallback(() => {
    clearBetaProgress()
    setFlowState('idle')
    setRestoredProgress(null)
    setCodeError(null)
  }, [])

  // ── Quick Continue (existing code in browser) ───────────────────────

  const handleQuickContinue = useCallback(() => {
    const code = getOrCreateParticipantCode()
    initBetaProgress(code)
    const progress = loadBetaProgress(code)
    const lessonId = progress?.currentLessonId ?? '1-1'
    trackEvent('demo_started', { source: 'quick_continue', route: `/lesson/${lessonId}` })
    navigate(`/lesson/${lessonId}`)
  }, [navigate])

  // ── Get code for display ───────────────────────────────────────────

  const currentCode = getStoredParticipantCode() ?? ''

  return (
    <div className="min-h-screen" style={{ background: '#0f0e17' }}>
      {/* ── subtle top bar ─────────────────────────────────────── */}
      <div
        className="sticky top-0 z-40 flex items-center justify-between px-4 sm:px-6 h-12"
        style={{
          background: 'rgba(15,14,23,0.92)',
          backdropFilter: 'blur(8px)',
          borderBottom: '1px solid rgba(201,162,39,0.08)',
        }}
      >
        <span className="text-[10px] font-bold tracking-wider" style={{ color: '#c9a227' }}>
          PYTHON QUEST
        </span>
        <button
          onClick={() => navigate('/')}
          className="text-[11px] cursor-pointer border-none bg-transparent hover:opacity-80"
          style={{ color: '#9b98a8' }}
        >
          ← Вернуться к курсу
        </button>
      </div>

      <div className="max-w-[720px] mx-auto px-4 sm:px-6 py-8 sm:py-12 space-y-12 sm:space-y-16">

        {/* ═══════════ 1. HERO ═══════════ */}
        <section className="text-center space-y-5 pt-4 sm:pt-8">
          <h1
            className="text-2xl sm:text-3xl md:text-4xl font-bold leading-tight"
            style={{ color: '#e8e6f0' }}
          >
            Python Quest — игровой курс Python для новичков
          </h1>

          <p
            className="text-sm sm:text-base leading-relaxed max-w-[580px] mx-auto"
            style={{ color: '#c9a227', lineHeight: '1.7' }}
          >
            Ребёнок учится программированию через историю, персонажей и миссии:
            сначала герой учится говорить через <code style={{ color: '#00d4aa' }}>print()</code>,
            потом хранить значения, считать, принимать решения
            и проходить всё более сложные задания.
          </p>

          <p className="text-xs sm:text-sm" style={{ color: '#9b98a8' }}>
            Начните с демо и проверьте, подходит ли формат вашему ребёнку.
          </p>

          {/* ── Flow-dependent CTA / Content ── */}
          {flowState === 'code_shown' && currentCode ? (
            /* ═══ Code shown — new participant ═══ */
            <div className="max-w-[480px] mx-auto">
              <ParticipantCodePanel
                participantCode={currentCode}
                onContinue={handleContinueAfterCode}
              />
            </div>
          ) : flowState === 'entering_code' ? (
            /* ═══ Entering code — returning participant ═══ */
            <div
              className="max-w-[480px] mx-auto rounded-xl p-6 space-y-4"
              style={{
                background: '#1a1924',
                border: '1px solid rgba(201,162,39,0.2)',
              }}
            >
              <h3 className="text-sm font-bold" style={{ color: '#e8e6f0' }}>
                Введите ваш beta-код
              </h3>
              <p className="text-xs" style={{ color: '#9b98a8' }}>
                Введите код в формате BETA-XXXXXX, чтобы восстановить прогресс.
              </p>
              <input
                type="text"
                value={returnCode}
                onChange={handleCodeInputChange}
                placeholder="BETA-······"
                className="w-full px-4 py-3 rounded-lg text-sm font-mono tracking-wider outline-none"
                style={{
                  background: '#0f0e17',
                  border: codeError
                    ? '1px solid #ff6b6b'
                    : '1px solid rgba(201,162,39,0.3)',
                  color: '#e8e6f0',
                }}
                maxLength={12}
                autoFocus
              />
              {codeError && (
                <p className="text-xs text-left" style={{ color: '#ff6b6b' }}>
                  {codeError}
                </p>
              )}
              <div className="flex flex-col sm:flex-row gap-3 pt-1">
                <button
                  onClick={() => setFlowState('idle')}
                  className="px-4 py-2.5 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:opacity-80"
                  style={{
                    background: 'transparent',
                    border: '1px solid rgba(201,162,39,0.3)',
                    color: '#9b98a8',
                  }}
                >
                  ← Назад
                </button>
                <button
                  onClick={handleRestoreProgress}
                  className="px-6 py-2.5 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:opacity-90 disabled:opacity-50"
                  style={{
                    background: returnCode.trim()
                      ? 'linear-gradient(135deg, #c9a227, #b8922a)'
                      : '#3a3944',
                    color: returnCode.trim() ? '#0f0e17' : '#6b7280',
                  }}
                  disabled={!returnCode.trim()}
                >
                  Восстановить прогресс
                </button>
              </div>
            </div>
          ) : flowState === 'restored' && restoredProgress ? (
            /* ═══ Restored — resume card ═══ */
            <div className="max-w-[480px] mx-auto">
              <ResumeProgressCard
                progress={restoredProgress}
                onContinue={handleContinueRestored}
                onStartFresh={handleStartFresh}
              />
            </div>
          ) : flowState === 'creating_code' ? (
            /* ═══ Creating — spinner ═══ */
            <div className="flex items-center justify-center py-12">
              <div className="flex flex-col items-center gap-4">
                <span
                  className="material-symbols-outlined text-4xl animate-spin"
                  style={{ color: '#c9a227', fontVariationSettings: "'FILL' 0" }}
                >
                  progress_activity
                </span>
                <p className="text-xs" style={{ color: '#9b98a8' }}>
                  Создаём ваш beta-код...
                </p>
              </div>
            </div>
          ) : (
            /* ═══ Idle — CTAs ═══ */
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
              {hasExistingCode ? (
                /* Returning user with existing code */
                <button
                  onClick={handleQuickContinue}
                  className="px-6 py-3 rounded-lg text-sm font-bold cursor-pointer border-none transition-all hover:opacity-90 active:scale-[0.97]"
                  style={{
                    background: 'linear-gradient(135deg, #00d4aa, #00b894)',
                    color: '#0f0e17',
                    boxShadow: '0 4px 20px rgba(0,212,170,0.3)',
                  }}
                >
                  Продолжить обучение →
                </button>
              ) : (
                <button
                  onClick={handleStartLearning}
                  className="px-6 py-3 rounded-lg text-sm font-bold cursor-pointer border-none transition-all hover:opacity-90 active:scale-[0.97]"
                  style={{
                    background: 'linear-gradient(135deg, #c9a227, #b8922a)',
                    color: '#0f0e17',
                    boxShadow: '0 4px 20px rgba(201,162,39,0.3)',
                  }}
                >
                  Начать обучение
                </button>
              )}

              <button
                onClick={hasExistingCode ? handleEnterCodeClick : scrollToHowItWorks}
                className="px-6 py-3 rounded-lg text-sm font-bold cursor-pointer border-none transition-all hover:opacity-80"
                style={{
                  background: 'transparent',
                  border: '1px solid rgba(201,162,39,0.3)',
                  color: '#c9a227',
                }}
              >
                {hasExistingCode ? 'У меня другой код' : 'Посмотреть, как это работает'}
              </button>
            </div>
          )}

          {/* ── Code entry link (when idle) ── */}
          {flowState === 'idle' && !hasExistingCode && (
            <div className="pt-1">
              <button
                onClick={handleEnterCodeClick}
                className="text-[11px] cursor-pointer border-none bg-transparent hover:opacity-80 underline underline-offset-2"
                style={{ color: '#9b98a8' }}
              >
                У меня уже есть beta-код
              </button>
            </div>
          )}

          {/* ── Beta identity model info ── */}
          {flowState === 'idle' && (
            <div
              className="inline-block px-4 py-2 rounded-lg text-[10px] leading-relaxed max-w-[420px]"
              style={{
                background: 'rgba(201,162,39,0.06)',
                border: '1px solid rgba(201,162,39,0.1)',
                color: '#6b7280',
              }}
            >
              Сохраните beta-код. По нему можно продолжить обучение позже — даже с другого устройства.
              Мы не просим имя ребёнка, телефон или платёжные данные.
            </div>
          )}
        </section>

        {/* ═══════════ 2. HOW IT WORKS ═══════════ */}
        <section id="how-it-works" className="space-y-5">
          <h2 className="text-lg sm:text-xl font-bold text-center" style={{ color: '#e8e6f0' }}>
            Как это работает
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {STEPS.map((step) => (
              <div
                key={step.number}
                className="rounded-xl p-4 flex items-start gap-4"
                style={{
                  background: '#1a1924',
                  border: '1px solid rgba(201,162,39,0.1)',
                }}
              >
                <div
                  className="w-9 h-9 rounded-full flex items-center justify-center shrink-0 text-sm font-bold"
                  style={{
                    background: 'rgba(201,162,39,0.15)',
                    color: '#c9a227',
                  }}
                >
                  {step.number}
                </div>
                <div>
                  <h3 className="text-sm font-bold mb-0.5" style={{ color: '#e8e6f0' }}>
                    {step.title}
                  </h3>
                  <p className="text-[11px] leading-relaxed" style={{ color: '#9b98a8' }}>
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ═══════════ 3. TARGET AUDIENCE ═══════════ */}
        <section className="space-y-5">
          <h2 className="text-lg sm:text-xl font-bold text-center" style={{ color: '#e8e6f0' }}>
            Кому подходит
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* For */}
            <div
              className="rounded-xl p-5"
              style={{
                background: '#1a1924',
                border: '1px solid rgba(0,212,170,0.2)',
              }}
            >
              <h3 className="text-sm font-bold mb-3" style={{ color: '#00d4aa' }}>
                ✓ Подходит
              </h3>
              <ul className="space-y-2">
                {[
                  'Детям и новичкам, которые только начинают Python',
                  'Родителям, которые хотят понятный учебный формат',
                  'Ученикам, которым скучны сухие курсы',
                ].map((text) => (
                  <li key={text} className="flex items-start gap-2 text-xs" style={{ color: '#b0aea8' }}>
                    <span style={{ color: '#00d4aa' }}>✓</span>
                    {text}
                  </li>
                ))}
              </ul>
            </div>

            {/* Not for */}
            <div
              className="rounded-xl p-5"
              style={{
                background: '#1a1924',
                border: '1px solid rgba(201,162,39,0.1)',
              }}
            >
              <h3 className="text-sm font-bold mb-3" style={{ color: '#c9a227' }}>
                ✗ Не подходит
              </h3>
              <ul className="space-y-2">
                {[
                  'Тем, кто уже уверенно пишет на Python',
                  'Тем, кто ищет справочник без игры',
                  'Тем, кому нужен полный промышленный Python прямо сейчас',
                ].map((text) => (
                  <li key={text} className="flex items-start gap-2 text-xs" style={{ color: '#b0aea8' }}>
                    <span style={{ color: '#c9a227' }}>✗</span>
                    {text}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        {/* ═══════════ 4. BETA PACKAGE ═══════════ */}
        <section
          className="rounded-xl p-5 sm:p-6"
          style={{
            background: '#1a1924',
            border: '1px solid rgba(201,162,39,0.15)',
          }}
        >
          <h2 className="text-lg sm:text-xl font-bold mb-3" style={{ color: '#e8e6f0' }}>
            Что входит в beta
          </h2>

          <p className="text-xs sm:text-sm leading-relaxed mb-4" style={{ color: '#c9a227' }}>
            Beta означает: продукт уже можно проходить и тестировать, но некоторые коммерческие функции ещё не финальные.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {[
              { label: 'Курс', value: 'Доступен полностью — все уроки, темы и части' },
              { label: 'Миссии', value: 'Работают — каждая проверяется автоматически' },
              { label: 'Повторения', value: 'Встроены в учебный маршрут каждой части' },
              { label: 'Квесты', value: 'Доступны — проверка синтаксиса и логики' },
              { label: 'Прогресс', value: 'Сохраняется на сервере — можно продолжить с другого устройства по beta-коду' },
              { label: 'Подсказки', value: 'Встроены в каждую миссию при ошибке' },
            ].map((item) => (
              <div
                key={item.label}
                className="rounded-lg px-3.5 py-2.5 flex items-center justify-between gap-2"
                style={{ background: 'rgba(15,14,23,0.6)' }}
              >
                <span className="text-[11px] font-bold uppercase tracking-wider shrink-0" style={{ color: '#9b98a8' }}>
                  {item.label}
                </span>
                <span className="text-[11px] text-right" style={{ color: '#b0aea8' }}>
                  {item.value}
                </span>
              </div>
            ))}
          </div>

          <p className="text-[11px] mt-4 leading-relaxed" style={{ color: '#6b7280' }}>
            Мы ожидаем обратную связь от первых пользователей, чтобы улучшить курс до финального релиза.
            Продукт может измениться после beta — мы учитываем ваши замечания.
          </p>
        </section>

        {/* ═══════════ 5. FAQ ═══════════ */}
        <section className="space-y-4">
          <h2 className="text-lg sm:text-xl font-bold text-center" style={{ color: '#e8e6f0' }}>
            Часто задаваемые вопросы
          </h2>

          <div className="space-y-2">
            {FAQ_ITEMS.map((item, idx) => (
              <AccordionItem
                key={idx}
                item={item}
                isOpen={openFaq === idx}
                onToggle={() => toggleFaq(idx)}
              />
            ))}
          </div>
        </section>

        {/* ═══════════ 6. SAFE ACCESS + BOTTOM CTA ═══════════ */}
        <section
          className="rounded-xl p-5 sm:p-6 text-center space-y-5"
          style={{
            background: '#1a1924',
            border: '1px solid rgba(201,162,39,0.15)',
          }}
        >
          <div
            className="rounded-lg px-4 py-3 inline-block text-xs leading-relaxed"
            style={{
              background: 'rgba(0,212,170,0.06)',
              border: '1px solid rgba(0,212,170,0.15)',
              color: '#9b98a8',
            }}
          >
            На beta-этапе не подключена оплата, не собираются платёжные данные
            и не создаются детские персональные профили. Прогресс сохраняется
            на сервере по beta-коду — это технические данные, которые не содержат
            личной информации.
          </div>

          <div>
            <p className="text-sm mb-4" style={{ color: '#e8e6f0' }}>
              Готовы попробовать?
            </p>
            <button
              onClick={handleStartLearning}
              className="px-8 py-3.5 rounded-lg text-sm font-bold cursor-pointer border-none transition-all hover:opacity-90 active:scale-[0.97]"
              style={{
                background: 'linear-gradient(135deg, #c9a227, #b8922a)',
                color: '#0f0e17',
                boxShadow: '0 4px 20px rgba(201,162,39,0.3)',
              }}
            >
              Начать обучение
            </button>
          </div>
        </section>

        {/* ── Footer ───────────────────────────────────────────── */}
        <footer className="text-center pb-8">
          <p className="text-[10px]" style={{ color: '#6b7280' }}>
            Python Quest · Игровой курс программирования · 2026
          </p>
        </footer>
      </div>
    </div>
  )
}
