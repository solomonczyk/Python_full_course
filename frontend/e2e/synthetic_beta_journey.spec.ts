import { test, expect, type Page, type Route } from '@playwright/test'

// ── Fixtures ──────────────────────────────────────────────────────────────────

const LESSON_1_1_SUMMARY = {
  id: '1-1', part: 1, chapter: 1, lesson: 1,
  slug: 'print', title: 'print()', subtitle: 'Твой голос в коде',
  difficulty: 'easy', estimated_time_min: 15, topic: 'print()', locked: false,
  story_placement: 'Новичок мир Python встречает Маленького героя.',
}

const LESSON_1_1 = {
  id: '1-1', part: 1, chapter: 1, lesson: 1,
  slug: 'print', title: 'print()', subtitle: 'Твой голос в коде',
  difficulty: 'easy', estimated_time_min: 15, scene_image: '/scenes/1-1.png',
  topic: 'print()', locked: false,
  story_placement: 'Новичок мир Python встречает Маленького героя.',
  pre_topic_dialogue: [
    { character: 'novice', text: 'Ксю, а как мне вообще что-то сказать программе?' },
    { character: 'ksyu', text: 'print() — это твой голос в мире Python.' },
  ],
  post_error_dialogue: [
    { character: 'novice', text: 'А, понял! Надо было взять print() в кавычки.' },
    { character: 'va', text: 'Типичная ошибка: забыл кавычки вокруг текста.' },
    { character: 'bagus', text: 'Ошибка — это тоже прогресс! Давай попробуем ещё раз.' },
  ],
  mini_summary: 'print() выводит текст на экран.',
  connection_to_game: 'В финальной игре print() будет выводить всё.',
  game_relevance: 'Когда будешь писать финальную игру, ты вспомнишь этот урок.',
  syntax_reminder: { type: 'indentation_reminder', message: 'print() выводит текст на экран. Текст в кавычках.' },
  explanation: {
    text: 'print() выводит текст или значение на экран.',
    character: 'ksyu',
    code_example: 'print("Привет, Python!")',
    output: 'Привет, Python!',
  },
  quiz: {
    question: 'Что делает функция print()?',
    options: [
      { id: 'a', text: 'Выводит текст или значение на экран', correct: true },
      { id: 'b', text: 'Удаляет файл', correct: false },
      { id: 'c', text: 'Запрашивает ввод от пользователя', correct: false },
    ],
  },
  what_outputs: { code: 'print("Python")', options: ['Python', 'Ошибка', 'None'], correct: 'Python' },
  find_bug: {
    description: 'В этом коде есть ошибка. Найди и исправь её.',
    code: 'print(Привет)',
    hint: 'Текст должен быть в кавычках.',
    correct: 'print("Привет")',
  },
  mission: {
    title: 'Миссия: print()',
    description: 'Напиши программу по теме урока «print()»',
    task: 'Первая реплика Новичка на арене. Выведи на экран строку: Я начинаю путь Python',
    expected_output: 'Я начинаю путь Python',
    character: 'da',
  },
  analogy: {
    title: 'Голос в пещере',
    intro: 'Представь, что ты стоишь в огромной пещере.',
    python_mapping: 'Команда print("Привет!") — это как крикнуть "Привет!" в пещере.',
    key_rule: 'print() — это твой голос в мире Python.',
  },
  practice_subtasks: [
    { title: 'Приветствие', description: 'Выведи приветствие на экран.', expected_output: 'Привет, мир!' },
  ],
}

// ── Constants ─────────────────────────────────────────────────────────────────

const FORBIDDEN_PAYLOAD_FIELDS = [
  'name', 'full_name', 'email', 'phone', 'age', 'birthdate',
  'city', 'address', 'ip', 'user_agent', 'parent_name', 'child_name', 'payment',
]

const ALLOWED_PAYLOAD_FIELDS = [
  'event', 'anonymous_session_id', 'timestamp',
  'lesson_id', 'mission_id', 'attempt_count', 'result', 'hint_id', 'source', 'route',
]

const FORBIDDEN_ANALYTICS_DOMAINS = [
  'google-analytics.com', 'googletagmanager.com',
  'mc.yandex', 'metrika', 'facebook.com/tr',
  'posthog', 'amplitude', 'segment',
]

// ── Helpers ───────────────────────────────────────────────────────────────────

function getAnalyticsEvents(page: Page): Promise<Record<string, any>[]> {
  return page.evaluate(() => {
    const api = (window as any).__PYTHON_QUEST_ANALYTICS__
    if (!api || typeof api.getEvents !== 'function') return []
    return api.getEvents()
  })
}

function getEventNames(page: Page): Promise<string[]> {
  return getAnalyticsEvents(page).then(events => events.map(e => e.event))
}

function countEvent(page: Page, eventName: string): Promise<number> {
  return getEventNames(page).then(names => names.filter(n => n === eventName).length)
}

/** Set up full API mocking for the lesson page */
async function mockLessonApis(page: Page, missionResponse?: {
  correct: boolean; actual_output?: string; expected_output?: string; error?: string
}) {
  // Mock lessons list (must be registered before the more specific route)
  await page.route('**/api/lessons', async (route: Route, request) => {
    const url = request.url()
    // Check if this is a request for a specific lesson (e.g., /api/lessons/1-1)
    if (url.includes('/lessons/') && !url.endsWith('/lessons') && !url.endsWith('/lessons/')) {
      await route.fallback() // Let the more specific handler take it
    } else {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([LESSON_1_1_SUMMARY]) })
    }
  })

  // Mock lesson detail (for api/lessons/1-1) — register after the general route so it takes priority
  await page.route('**/api/lessons/1-1', async (route: Route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(LESSON_1_1) })
  })

  // Mock progress
  await page.route('**/api/progress', async (route: Route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
    } else {
      await route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify({ lesson_id: '1-1', completed: true, quiz_passed: false, mission_done: true, score: 100, updated_at: new Date().toISOString() }),
      })
    }
  })

  // Mock mission check
  if (missionResponse) {
    await page.route('**/api/mission/check', async (route: Route) => {
      await route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify(missionResponse),
      })
    })
  }

  // Block health/quiz/quest/recap endpoints that aren't needed
  await page.route(/\/api\/(health|quiz|quest|recap|reviews?)/, async (route: Route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  })
}

/** Prep localStorage for a clean test session */
function cleanSession(page: Page) {
  return page.addInitScript(() => {
    localStorage.clear()
    localStorage.setItem('pq_onboarding_done', 'true')
  })
}

/** Navigate to beta landing with clean state */
async function goToBeta(page: Page) {
  await cleanSession(page)
  await page.goto('/beta')
  await page.waitForLoadState('load')
  await page.waitForTimeout(500)
}

/** Navigate to lesson 1-1 with clean state and mocked APIs */
async function goToLesson(page: Page) {
  await cleanSession(page)
  await page.goto('/lesson/1-1')
  await page.waitForLoadState('load')
  // Wait for lesson content to render (mission card textarea)
  await page.waitForSelector('textarea[placeholder*="Напиши"]', { timeout: 10000 })
}

// ── Shared setup ──────────────────────────────────────────────────────────────

test.afterEach(async ({ page }) => {
  await page.unrouteAll({ behavior: 'ignoreErrors' })
})

// ── Analytics Debug API ───────────────────────────────────────────────────────

test('analytics debug API is available and functional', async ({ page }) => {
  await goToBeta(page)

  // Debug API exists
  const apiExists = await page.evaluate(() =>
    typeof (window as any).__PYTHON_QUEST_ANALYTICS__ !== 'undefined'
  )
  expect(apiExists).toBe(true)

  // getEvents returns array with events
  const events = await getAnalyticsEvents(page)
  expect(Array.isArray(events)).toBe(true)
  expect(events.length).toBeGreaterThan(0)

  // Events have required fields
  const ev = events[0]
  expect(ev).toHaveProperty('event')
  expect(ev).toHaveProperty('anonymous_session_id')
  expect(ev).toHaveProperty('timestamp')
  expect(typeof ev.anonymous_session_id).toBe('string')
  expect(ev.anonymous_session_id).toMatch(/^pq_session_/)

  // clearEvents works
  const cleared = await page.evaluate(() => {
    const api = (window as any).__PYTHON_QUEST_ANALYTICS__
    try { api.clearEvents(); return true } catch { return false }
  })
  expect(cleared).toBe(true)

  const afterClear = await getAnalyticsEvents(page)
  expect(afterClear).toHaveLength(0)
})

// ── No External Analytics Requests ────────────────────────────────────────────

test('no external analytics requests are made', async ({ page }) => {
  const interceptedForbidden: string[] = []

  await page.route('**/*', async (route: Route) => {
    const url = route.request().url()
    const isForbidden = FORBIDDEN_ANALYTICS_DOMAINS.some(domain => url.includes(domain))
    if (isForbidden) interceptedForbidden.push(url)
    await route.continue()
  })

  await goToBeta(page)

  // Navigate to lesson
  const ctaButton = page.locator('button:has-text("Начать демо")')
  await ctaButton.first().click()
  await page.waitForURL('**/lesson/1-1', { timeout: 15000 })
  await page.waitForTimeout(3000)

  expect(interceptedForbidden).toHaveLength(0)
})

// ── No Personal Data in Analytics Payload ─────────────────────────────────────

test('analytics payload contains no personal data', async ({ page }) => {
  await goToBeta(page)

  // Navigate to lesson to generate more events
  const ctaButton = page.locator('button:has-text("Начать демо")')
  await ctaButton.first().click()
  await page.waitForURL('**/lesson/1-1', { timeout: 15000 })
  await page.waitForTimeout(2000)

  const events = await getAnalyticsEvents(page)
  expect(events.length).toBeGreaterThan(0)

  // Check no forbidden fields
  for (const ev of events) {
    for (const key of Object.keys(ev)) {
      expect(FORBIDDEN_PAYLOAD_FIELDS).not.toContain(key)
    }
  }

  // Check all fields are allowed
  for (const ev of events) {
    for (const key of Object.keys(ev)) {
      const isAllowed = ALLOWED_PAYLOAD_FIELDS.includes(key)
      expect(isAllowed).toBe(true)
    }
  }
})

// ── SYN-001: Fast Success ─────────────────────────────────────────────────────

test('SYN-001: fast success — happy path', async ({ page }) => {
  await mockLessonApis(page, {
    correct: true,
    actual_output: 'Я начинаю путь Python',
    expected_output: 'Я начинаю путь Python',
  })

  await goToBeta(page)

  // Click demo CTA
  const ctaButton = page.locator('button:has-text("Начать демо")')
  await ctaButton.first().click()
  await page.waitForURL('**/lesson/1-1', { timeout: 15000 })
  await page.waitForTimeout(2000)

  // Fill and submit correct code
  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill('print("Я начинаю путь Python")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  // Verify analytics
  const names = await getEventNames(page)
  expect(names).toContain('landing_opened')
  expect(names).toContain('demo_started')
  expect(names).toContain('lesson_started')
  expect(names).toContain('mission_attempted')
  expect(names).toContain('mission_passed')
})

// ── SYN-002: Error Recovery ───────────────────────────────────────────────────

test('SYN-002: one error then success', async ({ page }) => {
  // First submission: wrong answer
  await mockLessonApis(page, {
    correct: false,
    actual_output: 'нет',
    expected_output: 'Я начинаю путь Python',
    error: 'Output mismatch',
  })

  await goToBeta(page)

  const ctaButton = page.locator('button:has-text("Начать демо")')
  await ctaButton.first().click()
  await page.waitForURL('**/lesson/1-1', { timeout: 15000 })
  await page.waitForTimeout(2000)

  // Submit wrong code
  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill('print("нет")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  // Now update mock for correct answer
  await page.unroute('**/api/mission/check')
  await page.route('**/api/mission/check', async (route: Route) => {
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ correct: true, actual_output: 'Я начинаю путь Python', expected_output: 'Я начинаю путь Python' }),
    })
  })

  await textarea.fill('print("Я начинаю путь Python")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  // Verify analytics
  const names = await getEventNames(page)
  expect(names).toContain('landing_opened')
  expect(names).toContain('demo_started')
  expect(names).toContain('lesson_started')
  expect(names).toContain('mission_attempted')
  expect(names).toContain('mission_failed')
  expect(names).toContain('hint_used')
  expect(names).toContain('mission_passed')

  const attemptedCount = await countEvent(page, 'mission_attempted')
  expect(attemptedCount).toBe(2)
})

// ── SYN-003: Multiple Failures ────────────────────────────────────────────────

test('SYN-003: multiple errors then success', async ({ page }) => {
  await mockLessonApis(page, {
    correct: false,
    actual_output: 'ошибка',
    expected_output: 'Я начинаю путь Python',
    error: 'Output mismatch',
  })

  await goToLesson(page)

  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })

  // Submit wrong answer 3 times
  for (let i = 0; i < 3; i++) {
    await textarea.fill(`print("wrong_${i}")`)
    await page.click('button:has-text("Запустить миссию")')
    await page.waitForTimeout(1500)
  }

  // Verify counts
  const failedCount = await countEvent(page, 'mission_failed')
  expect(failedCount).toBe(3)

  const attemptedCount = await countEvent(page, 'mission_attempted')
  expect(attemptedCount).toBe(3)

  const hintCount = await countEvent(page, 'hint_used')
  expect(hintCount).toBeGreaterThanOrEqual(1)
})

// ── SYN-005: Landing Abandon ──────────────────────────────────────────────────

test('SYN-005: landing open but no demo', async ({ page }) => {
  await goToBeta(page)
  await page.waitForTimeout(1000)

  // Scroll down and back up
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
  await page.waitForTimeout(500)
  await page.evaluate(() => window.scrollTo(0, 0))
  await page.waitForTimeout(500)

  const names = await getEventNames(page)
  expect(names).toContain('landing_opened')
  expect(names).not.toContain('demo_started')
  expect(names).not.toContain('lesson_started')

  const ctaButton = page.locator('button:has-text("Начать демо")')
  await expect(ctaButton.first()).toBeVisible()
})

// ── SYN-006: Demo Open, No Mission Attempt ────────────────────────────────────

test('SYN-006: demo open but no mission attempt', async ({ page }) => {
  // Mock APIs so lesson data loads but no mission response needed
  await mockLessonApis(page)
  await goToBeta(page)
  await page.waitForTimeout(300)

  const ctaButton = page.locator('button:has-text("Начать демо")')
  await ctaButton.first().click()
  await page.waitForURL('**/lesson/1-1', { timeout: 15000 })
  await page.waitForTimeout(2000)

  // Scroll through lesson without submitting
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
  await page.waitForTimeout(500)
  await page.evaluate(() => window.scrollTo(0, 0))
  await page.waitForTimeout(500)

  const names = await getEventNames(page)
  expect(names).toContain('landing_opened')
  expect(names).toContain('demo_started')
  expect(names).toContain('lesson_started')
  expect(names).not.toContain('mission_attempted')
  expect(names).not.toContain('mission_failed')
  expect(names).not.toContain('mission_passed')
})

// ── SYN-007: Hint After First Fail ────────────────────────────────────────────

test('SYN-007: hint fires after first fail', async ({ page }) => {
  await mockLessonApis(page, {
    correct: false,
    actual_output: 'неправильно',
    expected_output: 'Я начинаю путь Python',
    error: 'Output mismatch',
  })

  await goToLesson(page)

  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill('print("неправильно")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  const names = await getEventNames(page)
  expect(names).toContain('hint_used')
  expect(names).toContain('mission_failed')
})

// ── SYN-008: Never Uses Hint ──────────────────────────────────────────────────

test('SYN-008: no hint fires on first-try success', async ({ page }) => {
  await mockLessonApis(page, {
    correct: true,
    actual_output: 'Я начинаю путь Python',
    expected_output: 'Я начинаю путь Python',
  })

  await goToLesson(page)

  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill('print("Я начинаю путь Python")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  const names = await getEventNames(page)
  expect(names).toContain('mission_passed')
  expect(names).not.toContain('hint_used')
})

// ── SYN-009: Analytics Preserved After Refresh ────────────────────────────────

test('SYN-009: analytics preserved after page refresh', async ({ page }) => {
  await mockLessonApis(page, {
    correct: false,
    actual_output: 'неверно',
    expected_output: 'Я начинаю путь Python',
    error: 'Output mismatch',
  })

  // Set onboarding flag without clearing analytics
  await page.addInitScript(() => {
    localStorage.setItem('pq_onboarding_done', 'true')
  })

  await page.goto('/lesson/1-1')
  await page.waitForLoadState('load')
  // Wait for lesson content
  await page.waitForSelector('textarea[placeholder*="Напиши"]', { timeout: 10000 })

  // Clear initial lesson-load events
  await page.evaluate(() => {
    const api = (window as any).__PYTHON_QUEST_ANALYTICS__
    if (api && typeof api.clearEvents === 'function') {
      api.clearEvents()
    }
    localStorage.removeItem('pq_analytics_events')
  })

  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill('print("неверно")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  // lesson_started was cleared above; check only mission events
  const namesBefore = await getEventNames(page)
  expect(namesBefore).toContain('mission_attempted')
  expect(namesBefore).toContain('mission_failed')

  const eventCountBefore = (await getAnalyticsEvents(page)).length

  // Refresh page — init script runs but only sets onboarding flag, not clear
  await page.reload()
  await page.waitForLoadState('load')
  await page.waitForTimeout(2000)

  // Events from before refresh should still be present (minus any from re-load)
  const eventsAfter = await getAnalyticsEvents(page)
  expect(eventsAfter.length).toBeGreaterThanOrEqual(eventCountBefore - 1)

  const namesAfter = await getEventNames(page)
  expect(namesAfter).toContain('mission_attempted')
  expect(namesAfter).toContain('mission_failed')
})

// ── SYN-010: Mobile Small Screen Path ─────────────────────────────────────────

test('SYN-010: mobile small screen path', async ({ page }) => {
  // Mock APIs so lesson page loads properly
  await mockLessonApis(page)

  await cleanSession(page)
  await page.setViewportSize({ width: 375, height: 667 })

  await page.goto('/beta')
  await page.waitForLoadState('load')
  await page.waitForTimeout(1000)

  // Check landing page readability
  const heading = page.locator('h1')
  await expect(heading).toBeVisible()

  // Check CTA tappability — use bottom CTA which may be more visible
  const ctaButtons = page.locator('button:has-text("Начать демо")')
  await expect(ctaButtons.first()).toBeVisible()
  await expect(ctaButtons.first()).toBeEnabled()

  // Scroll to CTA to ensure it's in the visible viewport
  await ctaButtons.first().scrollIntoViewIfNeeded()
  await page.waitForTimeout(300)

  // Navigate to lesson
  await ctaButtons.first().click()
  await page.waitForURL('**/lesson/1-1', { timeout: 15000 })
  await page.waitForTimeout(3000)

  const lessonTitle = page.locator('h1')
  await expect(lessonTitle).toBeVisible()

  const names = await getEventNames(page)
  expect(names).toContain('landing_opened')
  expect(names).toContain('demo_started')
  expect(names).toContain('lesson_started')

  // Textarea may be below the fold on mobile
  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible()
})

// ── Analytics Export: Full Event Types ────────────────────────────────────────

test('analytics export contains all required event types', async ({ page }) => {
  await mockLessonApis(page, {
    correct: true,
    actual_output: 'Я начинаю путь Python',
    expected_output: 'Я начинаю путь Python',
  })

  await cleanSession(page)
  await page.goto('/beta')
  await page.waitForLoadState('load')
  await page.waitForTimeout(300)

  const ctaButton = page.locator('button:has-text("Начать демо")')
  await ctaButton.first().click()
  await page.waitForURL('**/lesson/1-1', { timeout: 15000 })
  await page.waitForTimeout(2000)

  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill('print("Я начинаю путь Python")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  const events = await getAnalyticsEvents(page)
  const eventNames = events.map((e: any) => e.event)

  const requiredEvents = [
    'landing_opened', 'demo_started', 'lesson_started',
    'mission_attempted', 'mission_passed',
  ]
  for (const required of requiredEvents) {
    expect(eventNames).toContain(required)
  }

  // Verify payload structure
  for (const event of events) {
    expect(event.anonymous_session_id).toBeTruthy()
    expect(typeof event.anonymous_session_id).toBe('string')
    expect(event.timestamp).toBeTruthy()
    expect(() => new Date(event.timestamp)).not.toThrow()
  }
})

// ── LocalStorage Persistence ──────────────────────────────────────────────────

test('analytics events persist to localStorage', async ({ page }) => {
  await cleanSession(page)
  await page.goto('/beta')
  await page.waitForLoadState('load')
  await page.waitForTimeout(500)

  const storedRaw = await page.evaluate(() => localStorage.getItem('pq_analytics_events'))
  expect(storedRaw).not.toBeNull()

  const stored = JSON.parse(storedRaw!)
  expect(Array.isArray(stored)).toBe(true)
  expect(stored.length).toBeGreaterThan(0)

  const apiEvents = await getAnalyticsEvents(page)
  expect(apiEvents.length).toBe(stored.length)

  for (const ev of stored) {
    expect(ev).toHaveProperty('event')
    expect(ev).toHaveProperty('anonymous_session_id')
    expect(ev).toHaveProperty('timestamp')
  }
})

// ── No External Scripts on Load ───────────────────────────────────────────────

test('no external analytics scripts are loaded on initial load', async ({ page }) => {
  const scriptSources: string[] = []

  await page.route('**/*', async (route: Route) => {
    const req = route.request()
    if (req.resourceType() === 'script') {
      scriptSources.push(req.url())
    }
    await route.continue()
  })

  await cleanSession(page)
  await page.goto('/beta')
  await page.waitForLoadState('load')

  for (const src of scriptSources) {
    const isForbidden = FORBIDDEN_ANALYTICS_DOMAINS.some(domain => src.includes(domain))
    expect(isForbidden).toBe(false)
  }
})
