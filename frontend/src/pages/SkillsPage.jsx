import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function SkillsPage({ sessionId }) {
  const [skills, setSkills] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')

  // 加载 Skills
  const loadSkills = async () => {
    try {
      const params = new URLSearchParams()
      if (selectedCategory) params.append('category', selectedCategory)
      if (searchTerm) params.append('search', searchTerm)

      const res = await fetch(`http://localhost:8000/api/skills?${params}`)
      const data = await res.json()
      setSkills(data.skills)
      setCategories(data.categories)
    } catch (err) {
      console.error('加载 Skills 失败:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      loadSkills()
    }, 300)

    return () => clearTimeout(debounceTimer)
  }, [selectedCategory, searchTerm])

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="page-title">OpenClaw Skills</h1>
      <p className="page-subtitle">发现并安装 AI 技能，扩展你的 AI 助手能力</p>

      {/* 搜索框 */}
      <div className="search-bar">
        <input
          type="text"
          placeholder="搜索 Skills..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {/* 分类筛选 */}
      <div className="category-filters">
        <button
          className={`category-btn ${selectedCategory === '' ? 'active' : ''}`}
          onClick={() => setSelectedCategory('')}
        >
          全部
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            className={`category-btn ${selectedCategory === cat ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Skill 列表 */}
      {skills.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">📦</div>
          <div>暂无 Skills</div>
        </div>
      ) : (
        <div className="skills-grid">
          {skills.map((skill) => (
            <Link
              key={skill.id}
              to={`/skill/${skill.id}`}
              className="skill-card"
            >
              <div className="skill-card-header">
                <h3 className="skill-name">{skill.name}</h3>
                {skill.official && (
                  <span className="official-badge">Official</span>
                )}
              </div>
              <p className="skill-description">{skill.description}</p>
              <div className="skill-meta">
                <span>👤 {skill.author}</span>
                <span>⭐ {skill.stars}</span>
                <span>📥 {skill.installs}</span>
              </div>
              <div className="skill-tags">
                {skill.tags?.split(',').slice(0, 4).map((tag, i) => (
                  <span key={i} className="tag">#{tag.trim()}</span>
                ))}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default SkillsPage
