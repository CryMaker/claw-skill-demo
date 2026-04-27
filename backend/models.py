from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    author = Column(String, nullable=False)  # 作者 GitHub 用户名
    category = Column(String, nullable=False)
    tags = Column(String)  # 逗号分隔的标签
    version = Column(String, default="1.0.0")
    stars = Column(Integer, default=0)
    installs = Column(Integer, default=0)
    install_command = Column(String, nullable=False)
    repo_url = Column(String)
    official = Column(Boolean, default=False)  # 是否官方技能
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SkillFavorite(Base):
    """用户收藏的技能"""
    __tablename__ = "skill_favorites"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"))
    session_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    skill = relationship("Skill")
