# OpenClaw Skill Store Demo

一个基于 React + Python FastAPI 的 OpenClaw Skill 发现平台 demo，类似 [clawskills.sh](https://clawskills.sh/)。

## 技术栈

### 前端
- React 19
- React Router DOM (路由管理)
- 原生 CSS (GitHub 深色主题风格)
- Vite (构建工具)

### 后端
- Python 3.14
- FastAPI (Web 框架)
- SQLAlchemy (ORM)
- SQLite (数据库)
- Uvicorn (ASGI 服务器)

## 项目结构

```
claw-skill-demo/
├── backend/                 # Python 后端
│   ├── venv/               # Python 虚拟环境
│   ├── main.py             # FastAPI 应用入口
│   ├── models.py           # 数据库模型
│   ├── schemas.py          # Pydantic 数据模式
│   ├── database.py         # 数据库配置
│   └── requirements.txt    # Python 依赖
├── frontend/               # React 前端
│   ├── src/
│   │   ├── pages/         # 页面组件
│   │   ├── App.jsx        # 主应用组件
│   │   ├── App.css        # GitHub 深色主题样式
│   │   └── main.jsx       # 入口文件
│   └── package.json       # Node 依赖
└── README.md              # 项目文档
```

## 功能特性

- ✅ Skill 列表展示（支持分类筛选、搜索）
- ✅ Skill 详情页（查看完整信息、安装命令）
- ✅ 收藏/点赞功能
- ✅ 一键复制安装命令
- ✅ 响应式设计（支持移动端）
- ✅ GitHub 深色主题风格

## 快速开始

### 环境要求
- Python 3.10+
- Node.js 16+

### 1. 启动后端

```bash
# 进入后端目录
cd backend

# 激活虚拟环境 (Windows)
.\venv\Scripts\activate

# 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 http://localhost:8000 启动  
API 文档地址：http://localhost:8000/docs

### 2. 启动前端

打开新终端：

```bash
# 进入前端目录
cd frontend

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动

## API 接口

### Skills
- `GET /api/skills` - 获取 Skill 列表（支持分类、搜索）
- `GET /api/skills/{id}` - 获取 Skill 详情
- `POST /api/skills` - 创建新 Skill
- `PUT /api/skills/{id}` - 更新 Skill 信息
- `DELETE /api/skills/{id}` - 删除 Skill

### 收藏
- `POST /api/skills/{id}/star?session_id=xxx` - 收藏/取消收藏
- `GET /api/skills/{id}/star?session_id=xxx` - 检查收藏状态

### 分类
- `GET /api/categories` - 获取所有分类

## 示例数据

应用首次启动时会自动初始化 15 个示例 Skills：

### 官方技能 (5 个)
| 名称 | 分类 | 描述 |
|------|------|------|
| @openclaw/web-search | 搜索工具 | 实时搜索互联网内容 |
| @openclaw/code-executor | 开发工具 | 执行 Python/Node.js 代码 |
| @openclaw/file-manager | 效率工具 | 管理本地文件系统 |
| @openclaw/git-helper | 开发工具 | Git 版本控制辅助 |
| @openclaw/image-analyzer | AI 工具 | 分析图片内容 |

### 社区技能 (10 个)
- @devtools/sql-explorer - 数据库查询工具
- @aistudio/prompt-optimizer - Prompt 优化工具
- @automation/jira-integration - Jira 集成
- @datascience/csv-analyzer - CSV 数据分析
- @social/twitter-bot - Twitter 机器人
- @security/vuln-scanner - 安全漏洞扫描
- @translation/deepl-connector - DeepL 翻译
- @cloud/aws-helper - AWS 云管理
- @fun/meme-generator - 表情包生成器
- @productivity/notion-sync - Notion 同步工具

## 界面预览

访问 http://localhost:5173 即可浏览 Skill 商店。

## 开发说明

### 后端热重载
后端使用 `--reload` 参数，代码修改后自动重启。

### 前端热更新
前端使用 Vite，支持 HMR 热模块替换。

### 数据库
数据库文件位于 `backend/claw_store.db`，如需重置数据，删除该文件后重启后端即可。

## 注意事项

1. 确保先启动后端服务，再启动前端
2. 首次运行请检查后端控制台是否显示"初始化完成"
3. 收藏功能使用 localStorage 存储 session ID
4. 本项目为 demo，生产环境需要添加更多功能

## License

MIT
