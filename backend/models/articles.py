from psycopg import AsyncConnection
from schemas.articles import ArticleCreate, ArticleResponse, ArticleUpdate
from models.database import get_db_conn

async def create_article(conn: AsyncConnection, article: ArticleCreate) -> ArticleResponse:
    query_create_articles = """
        INSERT INTO Article (user_id, title, content)
        VALUES (%s, %s, %s)
        RETURNING id, user_id, title, content, created_at
    """
    query_create_tags = """INSERT INTO Tag (name) VALUES (%s) RETURNING id, name"""
    query_create_articles_tag = """
        INSERT INTO ArticleTag (article_id, tag_id)
        VALUES (%s, %s)
        RETURNING article_id, tag_id
    """
    async with conn.cursor() as cur:
        await cur.execute(query_create_articles, (
            article.user_id, 
            article.title, 
            article.content, 
        ))
        row = await cur.fetchone()
        user_id = row[0]
        
        await cur.execute(query_create_tags, (article.tag,))
        row_tag = await cur.fetchone()
        tag_name = row_tag[0]

        await cur.execute(query_create_articles_tag, (user_id, tag_name,))

        return ArticleResponse(
                id=row[0],
                user_id=row[1],
                title=row[2],
                content=row[3],
                created_at=row[4]
        )

async def get_article(conn: AsyncConnection, article_id: int) -> ArticleResponse:
    query = """
        SELECT id, user_id, title, content, created_at
        FROM Article
        WHERE id = %s
    """
    async with conn.cursor() as cur:
        await cur.execute(query, (article_id,))
        row = await cur.fetchone()
        if row:
            return ArticleResponse(
                id=row[0],
                user_id=row[1],
                title=row[2],
                content=row[3],
                created_at=row[4]
            )
        return None

async def get_all_articles(conn: AsyncConnection) -> list[ArticleResponse]:
    query = """
        SELECT id, user_id, title, content, created_at
        FROM Article
    """
    async with conn.cursor() as cur:
        await cur.execute(query)
        rows = await cur.fetchall()
        articles = [ArticleResponse(
            id=row[0],
            user_id=row[1],
            title=row[2],
            content=row[3],
            created_at=row[4]
        ) for row in rows]
        return articles

async def update_article(conn: AsyncConnection, article_id: int, article: ArticleUpdate) -> ArticleResponse:
    query = """
        UPDATE Article
        SET title = %s, content = %s
        WHERE id = %s
        RETURNING id, user_id, title, content, created_at
    """
    async with conn.cursor() as cur:
        await cur.execute(query, (
            article.title, 
            article.content, 
            article_id
        ))
        row = await cur.fetchone()
        if row:
            return ArticleResponse(
                id=row[0],
                user_id=row[1],
                title=row[2],
                content=row[3],
                created_at=row[4]
            )
        return None

async def delete_article(conn: AsyncConnection, article_id: int) -> bool:
    query = """
        DELETE FROM Article
        WHERE id = %s
    """
    async with conn.cursor() as cur:
        await cur.execute(query, (article_id,))
        if cur.rowcount == 0:
            return False
        return True
