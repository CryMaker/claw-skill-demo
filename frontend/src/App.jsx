import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import './App.css'

// 导入页面组件
import SkillsPage from './pages/SkillsPage'
import SkillDetailPage from './pages/SkillDetailPage'

// 生成或获取会话 ID
const getSessionId = () => {
  let sessionId = localStorage.getItem('skill_session_id')
  if (!sessionId) {
    sessionId = crypto.randomUUID()
    localStorage.setItem('skill_session_id', sessionId)
  }
  return sessionId
}

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <Link to="/" className="logo">
          <span className="logo-icon">🐾</span>
          <span className="logo-text">OpenClaw Skills</span>
        </Link>
        <nav>
          <ul className="nav-links">
            <li><Link to="/">全部 Skills</Link></li>
            <li><a href="https://github.com/openclaw/openclaw" target="_blank" rel="noopener noreferrer">GitHub</a></li>
          </ul>
        </nav>
      </div>
    </header>
  )
}

function App() {
  const sessionId = getSessionId()

  return (
    <BrowserRouter>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<SkillsPage sessionId={sessionId} />} />
            <Route path="/skill/:id" element={<SkillDetailPage sessionId={sessionId} />} />
          </Routes>
        </main>
        <footer className="footer">
          <p>OpenClaw Skill Store Demo - 发现并安装你的 AI 技能</p>
        </footer>
      </div>
    </BrowserRouter>
  )
}

export default App
