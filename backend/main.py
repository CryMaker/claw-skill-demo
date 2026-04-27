from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import engine, SessionLocal, Base
from models import Skill, SkillFavorite
from schemas import SkillCreate, SkillResponse, SkillUpdate, SkillListResponse

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OpenClaw Skill Store API", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== Skill APIs ==========

@app.get("/api/skills", response_model=SkillListResponse, tags=["Skills"])
def list_skills(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取 Skill 列表，支持分类筛选和搜索"""
    query = db.query(Skill)

    if category:
        query = query.filter(Skill.category == category)
    if search:
        query = query.filter(
            Skill.name.contains(search) |
            Skill.description.contains(search) |
            Skill.author.contains(search)
        )

    skills = query.all()

    # 获取所有分类
    categories = db.query(Skill.category).distinct().all()
    category_list = [c[0] for c in categories]

    return {"skills": skills, "total": len(skills), "categories": category_list}


@app.get("/api/skills/{skill_id}", response_model=SkillResponse, tags=["Skills"])
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """获取 Skill 详情"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")

    # 增加浏览量
    skill.installs += 1
    db.commit()
    db.refresh(skill)

    return skill


@app.post("/api/skills", response_model=SkillResponse, tags=["Skills"])
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    """创建新 Skill"""
    # 检查是否已存在
    existing = db.query(Skill).filter(Skill.name == skill.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill 名称已存在")

    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@app.put("/api/skills/{skill_id}", response_model=SkillResponse, tags=["Skills"])
def update_skill(skill_id: int, skill: SkillUpdate, db: Session = Depends(get_db)):
    """更新 Skill 信息"""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")

    update_data = skill.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_skill, key, value)

    db.commit()
    db.refresh(db_skill)
    return db_skill


@app.delete("/api/skills/{skill_id}", tags=["Skills"])
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    """删除 Skill"""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")

    db.delete(db_skill)
    db.commit()
    return {"message": "Skill 已删除"}


# ========== 收藏 APIs ==========

@app.post("/api/skills/{skill_id}/star", tags=["Favorites"])
def star_skill(skill_id: int, session_id: str, db: Session = Depends(get_db)):
    """收藏/点赞 Skill"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")

    # 检查是否已收藏
    existing = db.query(SkillFavorite).filter(
        SkillFavorite.skill_id == skill_id,
        SkillFavorite.session_id == session_id
    ).first()

    if existing:
        # 取消收藏
        db.delete(existing)
        skill.stars -= 1
    else:
        # 添加收藏
        db_favorite = SkillFavorite(skill_id=skill_id, session_id=session_id)
        db.add(db_favorite)
        skill.stars += 1

    db.commit()
    db.refresh(skill)
    return {"stars": skill.stars, "starred": not bool(existing)}


@app.get("/api/skills/{skill_id}/star", tags=["Favorites"])
def check_star_status(skill_id: int, session_id: str, db: Session = Depends(get_db)):
    """检查收藏状态"""
    favorite = db.query(SkillFavorite).filter(
        SkillFavorite.skill_id == skill_id,
        SkillFavorite.session_id == session_id
    ).first()
    return {"starred": bool(favorite)}


# ========== 分类 APIs ==========

@app.get("/api/categories", tags=["Categories"])
def get_categories(db: Session = Depends(get_db)):
    """获取所有分类"""
    categories = db.query(Skill.category).distinct().all()
    return {"categories": [c[0] for c in categories]}


# ========== 健康检查 ==========

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "message": "OpenClaw Skill Store API 运行正常"}


# ========== 初始化示例数据 ==========

@app.on_event("startup")
def startup_event():
    """应用启动时初始化示例数据"""
    db = SessionLocal()
    try:
        if db.query(Skill).count() > 0:
            return

        # OpenClaw 官方技能
        official_skills = [
            Skill(
                name="@openclaw/web-search",
                description="实时搜索互联网内容，获取最新信息和新闻",
                author="@openclaw",
                category="搜索工具",
                tags="search,web,news",
                version="2.1.0",
                stars=2345,
                installs=15678,
                install_command="npx @openclaw/web-search",
                repo_url="https://github.com/openclaw/web-search",
                official=True
            ),
            Skill(
                name="@openclaw/code-executor",
                description="在安全沙箱中执行 Python/Node.js 代码",
                author="@openclaw",
                category="开发工具",
                tags="code,execution,python,nodejs",
                version="3.0.1",
                stars=3421,
                installs=23456,
                install_command="npx @openclaw/code-executor",
                repo_url="https://github.com/openclaw/code-executor",
                official=True
            ),
            Skill(
                name="@openclaw/file-manager",
                description="读取、写入、管理本地文件系统",
                author="@openclaw",
                category="效率工具",
                tags="files,management,io",
                version="1.5.2",
                stars=1876,
                installs=12345,
                install_command="npx @openclaw/file-manager",
                repo_url="https://github.com/openclaw/file-manager",
                official=True
            ),
            Skill(
                name="@openclaw/git-helper",
                description="Git 版本控制辅助，支持 commit、diff、log 等操作",
                author="@openclaw",
                category="开发工具",
                tags="git,version-control,dev",
                version="2.0.0",
                stars=1543,
                installs=8765,
                install_command="npx @openclaw/git-helper",
                repo_url="https://github.com/openclaw/git-helper",
                official=True
            ),
            Skill(
                name="@openclaw/image-analyzer",
                description="分析图片内容，提取文字和描述图像",
                author="@openclaw",
                category="AI 工具",
                tags="image,vision,ocr",
                version="1.2.0",
                stars=2109,
                installs=9876,
                install_command="npx @openclaw/image-analyzer",
                repo_url="https://github.com/openclaw/image-analyzer",
                official=True
            ),
        ]

        # 社区技能
        community_skills = [
            Skill(
                name="@devtools/sql-explorer",
                description="数据库查询和管理工具，支持 MySQL、PostgreSQL、SQLite",
                author="@devtools",
                category="开发工具",
                tags="database,sql,query",
                version="1.0.3",
                stars=876,
                installs=4321,
                install_command="npx @devtools/sql-explorer",
                repo_url="https://github.com/devtools/sql-explorer",
                official=False
            ),
            Skill(
                name="@aistudio/prompt-optimizer",
                description="优化和测试 LLM Prompt 的工具",
                author="@aistudio",
                category="AI 工具",
                tags="prompt,ai,optimization",
                version="2.2.1",
                stars=1234,
                installs=5678,
                install_command="npx @aistudio/prompt-optimizer",
                repo_url="https://github.com/aistudio/prompt-optimizer",
                official=False
            ),
            Skill(
                name="@automation/jira-integration",
                description="Jira 项目管理集成，支持创建 issue、查询任务等",
                author="@automation",
                category="办公效率",
                tags="jira,project,automation",
                version="1.1.0",
                stars=654,
                installs=3210,
                install_command="npx @automation/jira-integration",
                repo_url="https://github.com/automation/jira-integration",
                official=False
            ),
            Skill(
                name="@datascience/csv-analyzer",
                description="CSV 数据分析工具，支持统计、过滤、导出",
                author="@datascience",
                category="数据分析",
                tags="csv,data,analysis",
                version="1.0.0",
                stars=432,
                installs=2109,
                install_command="npx @datascience/csv-analyzer",
                repo_url="https://github.com/datascience/csv-analyzer",
                official=False
            ),
            Skill(
                name="@social/twitter-bot",
                description="Twitter/X 机器人，支持自动发推、回复",
                author="@social",
                category="社交媒体",
                tags="twitter,social,bot",
                version="3.1.0",
                stars=1987,
                installs=7654,
                install_command="npx @social/twitter-bot",
                repo_url="https://github.com/social/twitter-bot",
                official=False
            ),
            Skill(
                name="@security/vuln-scanner",
                description="代码安全漏洞扫描工具",
                author="@security",
                category="安全工具",
                tags="security,vulnerability,scanner",
                version="2.0.1",
                stars=765,
                installs=3456,
                install_command="npx @security/vuln-scanner",
                repo_url="https://github.com/security/vuln-scanner",
                official=False
            ),
            Skill(
                name="@translation/deepl-connector",
                description="DeepL 翻译集成，支持多语言互译",
                author="@translation",
                category="效率工具",
                tags="translation,deepl,multilingual",
                version="1.3.0",
                stars=543,
                installs=4567,
                install_command="npx @translation/deepl-connector",
                repo_url="https://github.com/translation/deepl-connector",
                official=False
            ),
            Skill(
                name="@cloud/aws-helper",
                description="AWS 云服务管理工具，支持 EC2、S3、Lambda 等",
                author="@cloud",
                category="云服务",
                tags="aws,cloud,devops",
                version="2.1.0",
                stars=1098,
                installs=5432,
                install_command="npx @cloud/aws-helper",
                repo_url="https://github.com/cloud/aws-helper",
                official=False
            ),
            Skill(
                name="@fun/meme-generator",
                description="表情包生成器，支持自定义文字和模板",
                author="@fun",
                category="生活娱乐",
                tags="meme,fun,image",
                version="1.0.2",
                stars=2345,
                installs=8765,
                install_command="npx @fun/meme-generator",
                repo_url="https://github.com/fun/meme-generator",
                official=False
            ),
            Skill(
                name="@productivity/notion-sync",
                description="Notion 笔记同步和管理工具",
                author="@productivity",
                category="办公效率",
                tags="notion,notes,productivity",
                version="1.2.1",
                stars=876,
                installs=4321,
                install_command="npx @productivity/notion-sync",
                repo_url="https://github.com/productivity/notion-sync",
                official=False
            ),
        ]

        for skill in official_skills + community_skills:
            db.add(skill)

        db.commit()
        print(f"初始化完成：共 {len(official_skills) + len(community_skills)} 个 Skills")
    except Exception as e:
        db.rollback()
        print(f"初始化示例数据时出错：{e}")
    finally:
        db.close()
