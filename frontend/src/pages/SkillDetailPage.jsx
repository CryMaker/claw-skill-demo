import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

function SkillDetailPage({ sessionId }) {
  const { id } = useParams()
  const [skill, setSkill] = useState(null)
  const [loading, setLoading] = useState(true)
  const [starred, setStarred] = useState(false)
  const [toast, setToast] = useState(null)

  // 加载 Skill 详情
  const loadSkill = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/skills/${id}`)
      if (!res.ok) throw new Error('Skill not found')
      const data = await res.json()
      setSkill(data)
    } catch (err) {
      console.error('加载 Skill 失败:', err)
    } finally {
      setLoading(false)
    }
  }

  // 检查收藏状态
  const checkStarStatus = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/skills/${id}/star?session_id=${sessionId}`)
      const data = await res.json()
      setStarred(data.starred)
    } catch (err) {
      console.error('检查收藏状态失败:', err)
    }
  }

  // 切换收藏
  const toggleStar = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/skills/${id}/star?session_id=${sessionId}`, {
        method: 'POST',
      })
      const data = await res.json()
      setStarred(data.starred)
      setSkill({ ...skill, stars: data.stars })
    } catch (err) {
      console.error('收藏失败:', err)
    }
  }

  // 复制安装命令
  const copyInstallCommand = () => {
    navigator.clipboard.writeText(skill.install_command)
    setToast({ type: 'success', message: '安装命令已复制到剪贴板' })
    setTimeout(() => setToast(null), 2000)
  }

  useEffect(() => {
    loadSkill()
    checkStarStatus()
  }, [id])

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
      </div>
    )
  }

  if (!skill) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">❌</div>
        <div>Skill 不存在</div>
        <Link to="/" className="btn btn-primary" style={{ marginTop: '1rem' }}>
          返回首页
        </Link>
      </div>
    )
  }

  return (
    <div>
      <Link to="/" className="btn btn-secondary" style={{ marginBottom: '1rem' }}>
        ← 返回
      </Link>

      <div className="skill-detail">
        {/* 头部信息 */}
        <div className="skill-detail-header">
          <div className="skill-detail-title">
            <h1 className="skill-detail-name">{skill.name}</h1>
            {skill.official && (
              <span className="official-badge">Official</span>
            )}
          </div>
          <div className="skill-detail-stats">
            <span>⭐ {skill.stars} stars</span>
            <span>📥 {skill.installs} installs</span>
            <span>📦 v{skill.version}</span>
          </div>
        </div>

        {/* 描述 */}
        <div className="skill-detail-section">
          <h3>描述</h3>
          <p>{skill.description}</p>
        </div>

        {/* 作者 */}
        <div className="skill-detail-section">
          <h3>作者</h3>
          <p>{skill.author}</p>
        </div>

        {/* 分类 */}
        <div className="skill-detail-section">
          <h3>分类</h3>
          <p>{skill.category}</p>
        </div>

        {/* 标签 */}
        <div className="skill-detail-section">
          <h3>标签</h3>
          <div className="skill-tags">
            {skill.tags?.split(',').map((tag, i) => (
              <span key={i} className="tag">#{tag.trim()}</span>
            ))}
          </div>
        </div>

        {/* 安装命令 */}
        <div className="skill-detail-section">
          <h3>安装</h3>
          <div className="install-box">
            <code className="install-command">{skill.install_command}</code>
          </div>
          <button className="copy-btn" onClick={copyInstallCommand}>
            📋 复制命令
          </button>
        </div>

        {/* 仓库链接 */}
        {skill.repo_url && (
          <div className="skill-detail-section">
            <h3>源代码</h3>
            <a
              href={skill.repo_url}
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#58a6ff' }}
            >
              🔗 {skill.repo_url}
            </a>
          </div>
        )}

        {/* 操作按钮 */}
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
          <button
            className="btn btn-primary"
            onClick={toggleStar}
          >
            {starred ? '⭐ 已收藏' : '☆ 收藏'}
          </button>
          {skill.repo_url && (
            <a
              href={skill.repo_url}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-secondary"
            >
              🔗 查看源码
            </a>
          )}
        </div>
      </div>

      {/* Toast 提示 */}
      {toast && (
        <div className={`toast toast-${toast.type}`}>
          {toast.message}
        </div>
      )}
    </div>
  )
}

export default SkillDetailPage
