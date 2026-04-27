from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SkillBase(BaseModel):
    name: str
    description: str
    author: str
    category: str
    tags: Optional[str] = None
    version: Optional[str] = "1.0.0"
    install_command: str
    repo_url: Optional[str] = None
    official: Optional[bool] = False


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    version: Optional[str] = None
    stars: Optional[int] = None
    installs: Optional[int] = None
    install_command: Optional[str] = None
    repo_url: Optional[str] = None
    official: Optional[bool] = None


class SkillResponse(SkillBase):
    id: int
    stars: int
    installs: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SkillListResponse(BaseModel):
    skills: List[SkillResponse]
    total: int
    categories: List[str]
