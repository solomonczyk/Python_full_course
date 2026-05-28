import { useState } from 'react'
import { BrowserRouter, Routes, Route, useParams } from 'react-router-dom'
import { useLessons, useProgress } from './hooks/useApi'
import TopNav from './components/TopNav'
import Sidebar from './components/Sidebar'
import HomePage from './pages/HomePage'
import LessonPage from './pages/LessonPage'

function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { lessons } = useLessons()
  const { progress } = useProgress()
  const { id } = useParams()

  return (
    <div className="min-h-screen bg-background">
      <TopNav
        lessons={lessons}
        currentId={id}
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
          <Route path="/lesson/:id" element={<LessonPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/*" element={<Layout />} />
      </Routes>
    </BrowserRouter>
  )
}
