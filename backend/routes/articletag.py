from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from models.database import get_db_conn
from models.articletag import create_article_tag, get_articles_by_tag, get_tags_by_article, delete_article_tag
from schemas.articletag import ArticleTagCreate, ArticleTagResponse
from models import articletag as articletag_model

router = APIRouter(prefix="/article-tags", tags=["ArticleTags"])

@router.post("/", response_model=ArticleTagResponse)
async def create(data: ArticleTagCreate, db: AsyncConnection = Depends(get_db_conn)):
    result = await create_article_tag(db, data)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create ArticleTag")
    return result

@router.get("/article/{article_id}")
async def get_tag_by_article(article_id: int, db: AsyncConnection = Depends(get_db_conn)):
    return await articletag_model.get_tags_by_article(db, article_id)

@router.get("/tag/{tag_id}")
async def get_article_by_tag(tag_id: int, db: AsyncConnection = Depends(get_db_conn)):
    return await articletag_model.get_articles_by_tag(db, tag_id)

@router.delete("/")
async def delete(data: ArticleTagCreate, db: AsyncConnection = Depends(get_db_conn)):
    success = await articletag_model.delete_article_tag(db, data.article_id, data.tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tags deleted"}
