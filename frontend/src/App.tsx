import { useState, useLayoutEffect } from 'react'
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import { useLessons } from './hooks/useApi'
import { ProgressProvider, useProgressContext } from './hooks/ProgressContext'
import TopNav from './components/TopNav'
import Sidebar from './components/Sidebar'
import ChatWidget from './components/ChatWidget'
import HomePage from './pages/HomePage'
import LessonPage from './pages/LessonPage'
import ReviewPage from './pages/ReviewPage'

function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { lessons } = useLessons()
  const { progress } = useProgressContext()
  const location = useLocation()
  const match = location.pathname.match(/\/(?:lesson|review)\/([\w-]+)/)
  const currentLessonId = match ? match[1] : undefined

  // Scroll to top on every route change (useLayoutEffect fires before paint)
  useLayoutEffect(() => {
    window.scrollTo(0, 0)
  }, [location.pathname])

  return (
    <div className="min-h-screen bg-background">
      <TopNav
        lessons={lessons}
        currentId={currentLessonId}
        onMenuClick={() => setSidebarOpen((v) => !v)}
      />
      <Sidebar
        lessons={lessons}
        progress={progress}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <main className="md:ml-[280px] pt-24 pb-12 px-6 flex justify-center">
        <Routes>
          <Route path="/" element={<HomePage lessons={lessons} progress={progress} />} />
          <Route path="/lesson/:id" element={<LessonPage lessons={lessons} />} />
          <Route path="/review/:id" element={<ReviewPage />} />
        </Routes>
      </main>
      <ChatWidget />
    </div>
  )
}

export default function App() {
  // Prevent browser from restoring scroll position on back/forward navigation
  if (typeof window !== 'undefined') {
    window.history.scrollRestoration = 'manual'
  }

  return (
    <BrowserRouter>
      <ProgressProvider>
        <Routes>
          <Route path="/*" element={<Layout />} />
        </Routes>
      </ProgressProvider>
    </BrowserRouter>
  )
}
