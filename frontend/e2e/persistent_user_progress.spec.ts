import { test, expect, type Page, type Route } from '@playwright/test'

// ── Fixtures ────────────────────────────────────────────────────────────────

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
  find_bug: { description: 'Найди ошибку', code: 'print(Привет)', hint: 'Кавычки', correct: 'print("Привет")' },
  mission: {
    title: 'Миссия: print()',
    description: 'Напиши программу по теме',
    task: 'Выведи на экран строку: Я начинаю путь Python',
    expected_output: 'Я начинаю путь Python',
    character: 'da',
  },
}

const LESSON_1_2_SUMMARY = {
  id: '1-2', part: 1, chapter: 1, lesson: 2,
  slug: 'strings', title: 'Строки', subtitle: 'Слова в коде',
  difficulty: 'easy', estimated_time_min: 15, topic: 'strings', locked: false,
}

const LESSON_1_2 = {
  id: '1-2', part: 1, chapter: 1, lesson: 2,
  slug: 'strings', title: 'Строки', subtitle: 'Слова в коде',
  difficulty: 'easy', estimated_time_min: 15,
  topic: 'strings', locked: false,
  story_placement: 'Маленький герой учится работать со словами.',
  explanation: {
    text: 'Строки — это текст в кавычках.',
    character: 'va',
    code_example: 'print("строка")',
    output: 'строка',
  },
  quiz: {
    question: 'Как создать строку?',
    options: [
      { id: 'a', text: 'В кавычках', correct: true },
      { id: 'b', text: 'Без кавычек', correct: false },
    ],
  },
  what_outputs: { code: 'print("тест")', options: ['тест', 'Ошибка'], correct: 'тест' },
  mission: {
    title: 'Миссия: строки',
    description: 'Работа со строками',
    task: 'Выведи: Привет, мир!',
    expected_output: 'Привет, мир!',
    character: 'da',
  },
}

// ── Helpers ─────────────────────────────────────────────────────────────────

const FORBIDDEN_PAYLOAD_FIELDS = [
  'name', 'full_name', 'email', 'phone', 'age', 'birthdate',
  'city', 'address', 'ip', 'user_agent', 'parent_name', 'child_name', 'payment',
]

const ALLOWED_PAYLOAD_FIELDS = [
  'event', 'anonymous_session_id', 'participant_id', 'timestamp',
  'lesson_id', 'mission_id', 'attempt_count', 'result', 'hint_id', 'source', 'route',
]

function getAnalyticsEvents(page: Page): Promise<Record<string, any>[]> {
  return page.evaluate(() => {
    const api = (window as any).__PYTHON_QUEST_ANALYTICS__
    if (!api || typeof api.getEvents !== 'function') return []
    return api.getEvents()
  })
}

/** Set up onboarding flag without clearing other state */
function setOnboardingFlag(page: Page) {
  return page.addInitScript(() => {
    localStorage.setItem('pq_onboarding_done', 'true')
  })
}

/** Mock all APIs for lesson page operation */
async function mockLessonApis(page: Page, lessonId = '1-1', summaries?: any[]) {
  const lessonSummaries = summaries ?? [LESSON_1_1_SUMMARY, LESSON_1_2_SUMMARY]
  const lessonData = lessonId === '1-2' ? LESSON_1_2 : LESSON_1_1

  await page.route('**/api/lessons', async (route: Route) => {
    const url = route.request().url()
    if (url.includes('/lessons/') && !url.endsWith('/lessons') && !url.endsWith('/lessons/')) {
      await route.fallback()
    } else {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(lessonSummaries) })
    }
  })

  await page.route(`**/api/lessons/${lessonId}`, async (route: Route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(lessonData) })
  })

  await page.route('**/api/progress', async (route: Route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
    } else {
      await route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify({ lesson_id: lessonId, completed: true, quiz_passed: false, mission_done: true, score: 100, updated_at: new Date().toISOString() }),
      })
    }
  })

  await page.route(/\/api\/(health|quiz|quest|recap|reviews?)/, async (route: Route) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  })
}

/**
 * Navigate to a page with clean state.
 * Uses a permanent addInitScript that ONLY sets the onboarding flag (no clears).
 * This ensures:
 *  - First load: clean context (Playwright gives fresh context per test)
 *  - Reloads: existing data preserved, onboarding flag remains set
 */
async function navigateClean(page: Page, url: string) {
  await page.addInitScript(() => {
    // Only set the onboarding flag so Layout renders on lesson navigation
    // Does NOT clear localStorage so progress survives reloads
    localStorage.setItem('pq_onboarding_done', 'true')
  })
  await page.goto(url)
  await page.waitForLoadState('load')
  await page.waitForTimeout(500)
}

// ── Cleanup ─────────────────────────────────────────────────────────────────

test.afterEach(async ({ page }) => {
  await page.unrouteAll({ behavior: 'ignoreErrors' })
})

// ── Scenario 1: New participant created ─────────────────────────────────────

test('PERS-001: new participant code created on /beta', async ({ page }) => {
  // Catch JS errors
  const errors: string[] = []
  page.on('pageerror', err => {
    errors.push(`PAGE ERROR: ${err.message}`)
    console.log('PAGE ERROR:', err.message, err.stack?.slice(0, 200))
  })
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(`CONSOLE ERROR: ${msg.text()}`)
    }
  })

  await mockLessonApis(page)
  await navigateClean(page, '/beta')

  // There are two "Начать обучение" buttons (hero + bottom CTA) — use first
  const startButton = page.getByRole('button', { name: 'Начать обучение' }).first()
  await expect(startButton).toBeVisible()
  await startButton.click()

  // Wait for code creation (spinner + transition)
  await page.waitForTimeout(1000)

  // Check that participant code panel is shown
  const codePanel = page.locator('text=Ваш beta-код создан')
  await expect(codePanel).toBeVisible({ timeout: 5000 })

  // Verify code stored in localStorage
  const storedCode = await page.evaluate(() => localStorage.getItem('pq_beta_participant_code'))
  expect(storedCode).not.toBeNull()
  expect(storedCode).toMatch(/^BETA-[A-Z0-9]{6}$/)

  // Click "Продолжить обучение" (only one in the code panel, unambiguous)
  const continueBtn = page.locator('button:has-text("Продолжить обучение")')
  await expect(continueBtn).toBeVisible({ timeout: 5000 })
  await continueBtn.click()

  // Wait for SPA navigation using URL check (reliable for React Router)
  await page.waitForFunction(
    () => window.location.href.includes('/lesson/'),
    { timeout: 15000 }
  )
  // Verify progress record created
  const betaProgress = await page.evaluate(() => localStorage.getItem('pq_beta_progress'))
  expect(betaProgress).not.toBeNull()

  const parsed = JSON.parse(betaProgress!)
  expect(parsed.participantCode).toBe(storedCode)
  expect(parsed.currentLessonId).toBe('1-1')
  expect(Array.isArray(parsed.completedLessons)).toBe(true)
})

// ── Scenario 2: Progress saved after mission pass ───────────────────────────

test('PERS-002: mission progress persists after lesson completion', async ({ page }) => {
  await mockLessonApis(page, '1-1')

  // Mock mission check to return success
  await page.route('**/api/mission/check', async (route: Route) => {
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ correct: true, actual_output: 'Я начинаю путь Python', expected_output: 'Я начинаю путь Python' }),
    })
  })

  // Create participant and navigate to lesson
  await navigateClean(page, '/beta')

  // Click "Начать обучение" and wait for code
  await page.getByRole('button', { name: 'Начать обучение' }).first().click()
  await page.waitForTimeout(1000)
  await page.locator('text=Ваш beta-код создан').waitFor({ timeout: 5000 })

  const storedCode = await page.evaluate(() => localStorage.getItem('pq_beta_participant_code'))

  // Continue to lesson
  await page.locator('button:has-text("Продолжить обучение")').click()
  await page.waitForFunction(
    () => window.location.href.includes('/lesson/1-1'),
    { timeout: 15000 }
  )
  await page.waitForTimeout(1500)

  // Submit correct mission
  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill('print("Я начинаю путь Python")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  // Reload page to verify persistence — no init script clears localStorage now
  // We only need to set up mock routes again before reload
  await page.unrouteAll({ behavior: 'ignoreErrors' })
  await mockLessonApis(page, '1-1')
  await page.route('**/api/mission/check', async (route: Route) => {
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ correct: true, actual_output: 'Я начинаю путь Python', expected_output: 'Я начинаю путь Python' }),
    })
  })

  await page.reload()
  await page.waitForLoadState('load')
  await page.waitForTimeout(2000)

  // Verify beta progress persisted
  const progressAfterReload = await page.evaluate(() => localStorage.getItem('pq_beta_progress'))
  expect(progressAfterReload).not.toBeNull()

  const parsed = JSON.parse(progressAfterReload!)
  expect(parsed.participantCode).toBe(storedCode)
  expect(parsed.completedLessons).toContain('1-1')
  expect(parsed.missionStats['1-1']).toBeDefined()
  expect(parsed.missionStats['1-1'].passed).toBe(true)
  expect(parsed.missionStats['1-1'].attempts).toBe(1)
})

// ── Scenario 3: Returning participant restores progress ──────────────────────

test('PERS-003: returning participant restores progress with code', async ({ page }) => {
  // Simulate a returning user with existing progress in localStorage
  const testCode = 'BETA-TEST01'
  const testProgress = {
    participantCode: testCode,
    currentLessonId: '1-2',
    completedLessons: ['1-1'],
    lessonStatus: { '1-1': 'completed' as const, '1-2': 'started' as const },
    missionStats: {
      '1-1': { attempts: 2, failed: 1, passed: true, hintsUsed: 1 },
    },
    lastActiveAt: new Date().toISOString(),
    createdAt: new Date(Date.now() - 86400000).toISOString(),
  }

  // Set localStorage BEFORE page load so React useEffect picks it up
  await page.addInitScript((data: { code: string; progress: string }) => {
    localStorage.setItem('pq_beta_participant_code', data.code)
    localStorage.setItem('pq_beta_progress', data.progress)
    localStorage.setItem('pq_onboarding_done', 'true')
  }, { code: testCode, progress: JSON.stringify(testProgress) })

  await page.goto('/beta')
  await page.waitForLoadState('load')
  await page.waitForTimeout(500)

  // User has existing code — "Продолжить обучение" button should appear (unambiguous here)
  await expect(page.locator('button:has-text("Продолжить обучение")')).toBeVisible()

  // Click "У меня другой код" to test code entry
  await page.locator('button:has-text("У меня другой код")').click()
  await page.waitForTimeout(500)

  // Should show code entry form
  const codeInput = page.locator('input[placeholder="BETA-······"]')
  await expect(codeInput).toBeVisible()

  // Enter correct code
  await codeInput.fill(testCode)

  // Click "Восстановить прогресс"
  await page.locator('button:has-text("Восстановить прогресс")').click()
  await page.waitForTimeout(1000)

  // Should show resume card
  const resumeCard = page.locator('text=Ваш прогресс найден')
  await expect(resumeCard).toBeVisible({ timeout: 5000 })

  // Should show correct lesson — use first() since "Урок 1-2" appears in text and button
  const resumeLesson = page.getByText('Урок 1-2').first()
  await expect(resumeLesson).toBeVisible()

  // Click continue — unique button text
  await page.locator('button:has-text("Продолжить урок 1-2")').click()
  await page.waitForFunction(
    () => window.location.href.includes('/lesson/1-2'),
    { timeout: 15000 }
  )
})

// ── Clean state returning participant (no stored data) ───────────────────────

test('PERS-004: returning participant enters code and restores from blank state', async ({ page }) => {
  // Simulate returning user on a different browser — no participant code
  // but progress pre-stored in localStorage (same browser was used before)
  const testCode = 'BETA-ABC123'
  const testProgress = {
    participantCode: testCode,
    currentLessonId: '1-1',
    completedLessons: ['1-1'],
    lessonStatus: { '1-1': 'completed' as const },
    missionStats: {
      '1-1': { attempts: 1, failed: 0, passed: true, hintsUsed: 0 },
    },
    lastActiveAt: new Date().toISOString(),
    createdAt: new Date(Date.now() - 86400000).toISOString(),
  }

  // Set progress BEFORE page load but NOT participant code (simulating different browser)
  await page.addInitScript((data: { progress: string }) => {
    localStorage.setItem('pq_beta_progress', data.progress)
    localStorage.setItem('pq_onboarding_done', 'true')
  }, { progress: JSON.stringify(testProgress) })

  await page.goto('/beta')
  await page.waitForLoadState('load')
  await page.waitForTimeout(300)

  // No existing code with participant code key — should show "Начать обучение"
  await expect(page.getByRole('button', { name: 'Начать обучение' }).first()).toBeVisible()

  // Click "У меня уже есть beta-код"
  await page.getByText('У меня уже есть beta-код').click()
  await page.waitForTimeout(500)

  // Enter code
  const codeInput = page.locator('input[placeholder="BETA-······"]')
  await expect(codeInput).toBeVisible()
  await codeInput.fill(testCode)

  // Restore
  await page.locator('button:has-text("Восстановить прогресс")').click()
  await page.waitForTimeout(1000)

  // Progress found
  const resumeCard = page.locator('text=Ваш прогресс найден')
  await expect(resumeCard).toBeVisible({ timeout: 5000 })
})

// ── Scenario 4: Invalid code ────────────────────────────────────────────────

test('PERS-005: invalid code format shows safe error', async ({ page }) => {
  await navigateClean(page, '/beta')

  // Click "У меня уже есть beta-код"
  await page.getByText('У меня уже есть beta-код').click()
  await page.waitForTimeout(500)

  const codeInput = page.locator('input[placeholder="BETA-······"]')
  await expect(codeInput).toBeVisible()

  // Test invalid format codes (non-empty but wrong format)
  const invalidCodes = ['abc', 'BETA-', 'BETA-12345', 'INVALID-CODE']
  for (const invalid of invalidCodes) {
    await codeInput.fill(invalid)
    await page.locator('button:has-text("Восстановить прогресс")').click()
    await page.waitForTimeout(500)

    // Should show error message (no crash)
    const formatError = page.locator('text=Неверный формат кода')
    await expect(formatError).toBeVisible({ timeout: 3000 })

    // Go back to return to idle
    await page.locator('button:has-text("Назад")').click()
    await page.waitForTimeout(300)
    // Re-enter code flow
    await page.getByText('У меня уже есть beta-код').click()
    await page.waitForTimeout(300)
  }
})

test('PERS-006: non-existent code shows not found error', async ({ page }) => {
  await navigateClean(page, '/beta')

  // Enter code entry flow
  await page.getByText('У меня уже есть beta-код').click()
  await page.waitForTimeout(500)

  const codeInput = page.locator('input[placeholder="BETA-······"]')
  await expect(codeInput).toBeVisible()
  await codeInput.fill('BETA-NONE01')

  // Restore — this code won't have progress
  await page.locator('button:has-text("Восстановить прогресс")').click()
  await page.waitForTimeout(1000)

  // Should show not found message (safe, no crash)
  const notFoundMsg = page.locator('text=не найден')
  await expect(notFoundMsg).toBeVisible({ timeout: 3000 })

  // No crash — page is still interactive
  await expect(page.locator('button:has-text("Назад")')).toBeVisible()
})

// ── Scenario 5: Analytics bound to participant ──────────────────────────────

test('PERS-007: analytics events contain participant marker', async ({ page }) => {
  await mockLessonApis(page)
  await navigateClean(page, '/beta')

  // Create participant — use first() since there are two buttons
  await page.getByRole('button', { name: 'Начать обучение' }).first().click()
  await page.waitForTimeout(1000)
  await page.locator('text=Ваш beta-код создан').waitFor({ timeout: 5000 })

  // Navigate to lesson
  await page.locator('button:has-text("Продолжить обучение")').click()
  await page.waitForFunction(
    () => window.location.href.includes('/lesson/'),
    { timeout: 15000 }
  )
  await page.waitForTimeout(2000)

  // Check analytics events
  const events = await getAnalyticsEvents(page)

  // landing_opened should have participant_id
  const landingEvent = events.find((e: any) => e.event === 'landing_opened')
  expect(landingEvent).toBeDefined()

  // demo_started should have participant_id
  const demoEvent = events.find((e: any) => e.event === 'demo_started')
  expect(demoEvent).toBeDefined()

  // lesson_started should have participant_id
  const lessonEvent = events.find((e: any) => e.event === 'lesson_started')
  expect(lessonEvent).toBeDefined()

  // All events with participant_id should have the same ID
  const ids = events.filter((e: any) => e.participant_id)
    .map((e: any) => e.participant_id)
  expect(ids.length).toBeGreaterThan(0)
  const firstId = ids[0]
  for (const id of ids) {
    expect(id).toBe(firstId)
  }
  // Should look like p_<hash>
  expect(firstId).toMatch(/^p_[a-z0-9]+$/)

  // No personal data in any event
  for (const ev of events) {
    for (const key of Object.keys(ev)) {
      expect(FORBIDDEN_PAYLOAD_FIELDS).not.toContain(key)
    }
    for (const key of Object.keys(ev)) {
      const isAllowed = ALLOWED_PAYLOAD_FIELDS.includes(key)
      expect(isAllowed).toBe(true)
    }
  }
})

// ── Scenario 6: Fresh start after choosing "Начать заново" ───────────────────

test('PERS-008: fresh start resets progress', async ({ page }) => {
  // Create existing progress
  const testCode = 'BETA-RST123'
  const testProgress = {
    participantCode: testCode,
    currentLessonId: '1-2',
    completedLessons: ['1-1'],
    lessonStatus: { '1-1': 'completed' as const, '1-2': 'started' as const },
    missionStats: { '1-1': { attempts: 2, failed: 1, passed: true, hintsUsed: 1 } },
    lastActiveAt: new Date().toISOString(),
    createdAt: new Date().toISOString(),
  }

  // Set up state BEFORE page load so React picks it up
  await mockLessonApis(page)
  await page.addInitScript((data: { code: string; progress: string }) => {
    localStorage.setItem('pq_beta_participant_code', data.code)
    localStorage.setItem('pq_beta_progress', data.progress)
    localStorage.setItem('pq_onboarding_done', 'true')
  }, { code: testCode, progress: JSON.stringify(testProgress) })

  await page.goto('/beta')
  await page.waitForLoadState('load')
  await page.waitForTimeout(500)

  // Should show quick continue
  await expect(page.locator('button:has-text("Продолжить обучение")')).toBeVisible()

  // Click "У меня другой код"
  await page.locator('button:has-text("У меня другой код")').click()
  await page.waitForTimeout(500)

  // Enter the existing code to see progress
  await page.locator('input[placeholder="BETA-······"]').fill(testCode)
  await page.waitForTimeout(300)

  // Verify button is enabled before clicking
  const restoreBtn = page.locator('button:has-text("Восстановить прогресс")')
  await expect(restoreBtn).toBeEnabled({ timeout: 3000 })
  await restoreBtn.click()
  await page.waitForTimeout(1500)

  // Progress found
  await expect(page.locator('text=Ваш прогресс найден')).toBeVisible({ timeout: 8000 })

  // Click "Начать заново"
  await page.locator('button:has-text("Начать заново")').click()
  await page.waitForTimeout(500)

  // Should return to idle state
  // Progress was cleared — pq_beta_progress is removed from localStorage
  const freshProgress = await page.evaluate(() => localStorage.getItem('pq_beta_progress'))
  expect(freshProgress).toBeNull()
})

// ── Scenario 9: Mission stats tracked correctly ─────────────────────────────

test('PERS-009: mission attempts and hints are tracked', async ({ page }) => {
  await mockLessonApis(page, '1-1')

  // First submission: wrong
  await page.route('**/api/mission/check', async (route: Route) => {
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ correct: false, actual_output: 'wrong', expected_output: 'Я начинаю путь Python', error: 'Output mismatch' }),
    })
  })

  await navigateClean(page, '/beta')

  // Create participant and go to lesson
  await page.getByRole('button', { name: 'Начать обучение' }).first().click()
  await page.waitForTimeout(1000)
  await page.locator('button:has-text("Продолжить обучение")').click()
  await page.waitForFunction(
    () => window.location.href.includes('/lesson/'),
    { timeout: 15000 }
  )
  await page.waitForTimeout(1500)

  // Submit wrong answer (triggers 1 failed attempt)
  const textarea = page.getByPlaceholder('# Напиши свой код здесь')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill('print("wrong")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  // Update mock for correct answer
  await page.unroute('**/api/mission/check')
  await page.route('**/api/mission/check', async (route: Route) => {
    await route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ correct: true, actual_output: 'Я начинаю путь Python', expected_output: 'Я начинаю путь Python' }),
    })
  })

  // Submit correct answer (triggers pass)
  await textarea.fill('print("Я начинаю путь Python")')
  await page.click('button:has-text("Запустить миссию")')
  await page.waitForTimeout(2000)

  // Verify mission stats
  const progressData = await page.evaluate(() => localStorage.getItem('pq_beta_progress'))
  const parsed = JSON.parse(progressData!)
  const stats = parsed.missionStats['1-1']

  expect(stats).toBeDefined()
  // 1 wrong attempt + 1 correct attempt = 2 total attempts
  expect(stats.attempts).toBe(2)
  expect(stats.failed).toBe(1)
  expect(stats.passed).toBe(true)
  expect(parsed.completedLessons).toContain('1-1')
})
