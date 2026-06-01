import { useState, useLayoutEffect, useEffect } from 'react'
import { BrowserRouter, Routes, Route, useLocation, Navigate } from 'react-router-dom'
import { useLessons } from './hooks/useApi'
import { ProgressProvider, useProgressContext } from './hooks/ProgressContext'
import { usePageMeta, canonicalUrl, PUBLIC_ROUTES } from './hooks/usePageMeta'
import TopNav from './components/TopNav'
import Sidebar from './components/Sidebar'
import ChatWidget from './components/ChatWidget'
import HomePage from './pages/HomePage'
import LessonPage from './pages/LessonPage'
import ReviewPage from './pages/ReviewPage'
import OnboardingPage from './pages/OnboardingPage'
import CompletionPage from './pages/CompletionPage'
import CourseCatalogPage from './pages/CourseCatalogPage'
import LessonPreviewPage from './pages/LessonPreviewPage'
import GlossaryPage from './pages/GlossaryPage'
import RecapPage from './pages/RecapPage'
import QuestPage from './pages/QuestPage'

/** Layout used for authenticated (onboarded) learning pages. */
function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { lessons } = useLessons()
  const { progress } = useProgressContext()
  const location = useLocation()
  const match = location.pathname.match(/\/(?:lesson|review)\/([\w-]+)/)
  const currentLessonId = match ? match[1] : undefined

  useLayoutEffect(() => {
    window.scrollTo(0, 0)
  }, [location.pathname])

  return (
    <div className="min-h-screen" style={{ background: '#0a0910' }}>
      <Sidebar
        lessons={lessons}
        progress={progress}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <div className="md:ml-[220px] flex flex-col min-h-screen">
        <TopNav
          lessons={lessons}
          currentId={currentLessonId}
          progress={progress}
          onMenuClick={() => setSidebarOpen((v) => !v)}
        />
        <main
          className="flex-1 px-6 py-6 flex justify-center"
          style={{ background: '#0f0e17' }}
        >
          <div className="w-full max-w-[1000px]">
            <Routes>
              <Route path="/" element={<HomePage lessons={lessons} progress={progress} />} />
              <Route path="/lesson/:id" element={<LessonPage lessons={lessons} />} />
              <Route path="/review/:id" element={<ReviewPage />} />
              <Route path="/glossary" element={<GlossaryPage />} />
              <Route path="/recap/:id" element={<RecapPage />} />
              <Route path="/quest/:id" element={<QuestPage />} />
            </Routes>
          </div>
        </main>
      </div>
      <ChatWidget lessonId={currentLessonId} />
    </div>
  )
}

/** Minimal layout for public pages (no sidebar, no onboarding requirement). */
function PublicLayout() {
  const location = useLocation()

  useLayoutEffect(() => {
    window.scrollTo(0, 0)
  }, [location.pathname])

  return (
    <div className="min-h-screen" style={{ background: '#0f0e17' }}>
      <main>
        <Routes>
          <Route path="/course" element={<CourseCatalogPage />} />
          <Route path="/lesson/:id/preview" element={<LessonPreviewPage />} />
        </Routes>
      </main>
    </div>
  )
}

/** SEO metadata router — updates meta tags on every route change. */
function MetaRouter({ children }: { children: React.ReactNode }) {
  const location = useLocation()

  useEffect(() => {
    const path = location.pathname

    // Route-level metadata
    if (path === '/' || path.startsWith('/lesson/') && !path.endsWith('/preview') || path.startsWith('/review/')) {
      usePageMeta({
        ...PUBLIC_ROUTES['/'],
        canonical: canonicalUrl(path),
      })
    } else if (path === '/glossary') {
      usePageMeta({
        title: 'Глоссарий — Python Quest',
        description: 'Словарь терминов Python с простыми определениями, аналогиями и примерами кода.',
        canonical: canonicalUrl('/glossary'),
      })
    } else if (path.startsWith('/recap/')) {
      usePageMeta({
        title: 'Повторение — Python Quest',
        description: 'Напоминалка по пройденному разделу курса Python Quest.',
        canonical: canonicalUrl(path),
      })
    } else if (path.startsWith('/quest/')) {
      usePageMeta({
        title: 'Испытание — Python Quest',
        description: 'Финальное испытание по разделу курса Python Quest.',
        canonical: canonicalUrl(path),
      })
    } else if (path === '/course') {
      usePageMeta({
        ...PUBLIC_ROUTES['/course'],
        canonical: canonicalUrl(path),
      })
    } else if (path === '/onboarding') {
      usePageMeta({
        title: 'Вступление',
        description: 'Начни своё путешествие в мир Python с короткого вступления.',
        canonical: canonicalUrl('/onboarding'),
      })
    }
  }, [location.pathname])

  return <>{children}</>
}

const ONBOARDING_KEY = 'pq_onboarding_done'

export default function App() {
  if (typeof window !== 'undefined') {
    window.history.scrollRestoration = 'manual'
  }

  return (
    <BrowserRouter>
      <ProgressProvider>
        <MetaRouter>
          <Routes>
            {/* Full-screen pages (no sidebar) */}
            <Route path="/onboarding" element={<OnboardingPage />} />
            <Route path="/completion" element={<CompletionPage />} />

            {/* PUBLIC pages — no onboarding required */}
            <Route path="/course" element={<PublicLayout />} />
            <Route path="/lesson/:id/preview" element={<PublicLayout />} />

            {/* Authenticated pages — onboarding required */}
            <Route path="/*" element={
              localStorage.getItem(ONBOARDING_KEY)
                ? <Layout />
                : <Navigate to="/onboarding" replace />
            } />
          </Routes>
        </MetaRouter>
      </ProgressProvider>
    </BrowserRouter>
  )
}
