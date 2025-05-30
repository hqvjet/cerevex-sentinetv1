from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TagCreate(BaseModel):
    name: str

class ArticleCreate(BaseModel):
    user_id: int
    title: Optional[str]
    content: Optional[str]

    tag: Optional[str] = None

    class Config:
        from_attributes = True

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    class Config:
        from_attributes = True

class ArticleResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    content: Optional[str]
    created_at: datetime

    tag: Optional[str] = None

    class Config:
        from_attributes = True
