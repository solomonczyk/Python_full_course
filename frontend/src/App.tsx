import { useState, useLayoutEffect } from 'react'
import { BrowserRouter, Routes, Route, useLocation, Navigate } from 'react-router-dom'
import { useLessons } from './hooks/useApi'
import { ProgressProvider, useProgressContext } from './hooks/ProgressContext'
import TopNav from './components/TopNav'
import Sidebar from './components/Sidebar'
import ChatWidget from './components/ChatWidget'
import HomePage from './pages/HomePage'
import LessonPage from './pages/LessonPage'
import ReviewPage from './pages/ReviewPage'
import OnboardingPage from './pages/OnboardingPage'
import CompletionPage from './pages/CompletionPage'

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
      {/* Persistent Sidebar */}
      <Sidebar
        lessons={lessons}
        progress={progress}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main area: TopBar + Content */}
      <div className="md:ml-[220px] flex flex-col min-h-screen">
        <TopNav
          lessons={lessons}
          currentId={currentLessonId}
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
            </Routes>
          </div>
        </main>
      </div>

      <ChatWidget lessonId={currentLessonId} />
    </div>
  )
}

const ONBOARDING_KEY = 'pq_onboarding_done'

export default function App() {
  if (typeof window !== 'undefined') {
    window.history.scrollRestoration = 'manual'
  }

  const onboardingDone = typeof window !== 'undefined' ? localStorage.getItem(ONBOARDING_KEY) : null

  return (
    <BrowserRouter>
      <ProgressProvider>
        <Routes>
          {/* Full-screen pages (no sidebar) */}
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/completion" element={<CompletionPage />} />

          {/* Layout pages (with sidebar/nav) — catch-all */}
          <Route path="/*" element={
            onboardingDone ? <Layout /> : <Navigate to="/onboarding" replace />
          } />
        </Routes>
      </ProgressProvider>
    </BrowserRouter>
  )
}
