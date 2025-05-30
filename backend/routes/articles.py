from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from models.database import get_db_conn
from models.articles import create_article, get_article,  get_all_articles, delete_article
from schemas.articles import ArticleCreate, ArticleUpdate, ArticleResponse

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.post("/create", response_model=ArticleResponse)
async def create_article_route(article: ArticleCreate, conn: AsyncConnection = Depends(get_db_conn)):
    result = await create_article(conn, article)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create article")
    return result

@router.get("/get/{article_id}", response_model=ArticleResponse)
async def get_article_detail(article_id: int, conn: AsyncConnection = Depends(get_db_conn)):
    result = await get_article(conn, article_id)
    if not result:
        raise HTTPException(status_code=404, detail="Article not found")
    return result

@router.get("/all", response_model=list[ArticleResponse])
async def get_all_articles_route(conn: AsyncConnection = Depends(get_db_conn)):
    return await get_all_articles(conn)

@router.delete("/delete/{article_id}")
async def delete_article_route(article_id: int, conn: AsyncConnection = Depends(get_db_conn)):
    result = await delete_article(conn, article_id)
    if not result:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"detail": "Article deleted successfully"}
