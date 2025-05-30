from psycopg import AsyncConnection
from schemas.articles import ArticleCreate, ArticleResponse, ArticleUpdate

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
        article_id = row[0]
        
        await cur.execute(query_create_tags, (article.tag,))
        row_tag = await cur.fetchone()
        tag_id = row_tag[0]
        tag_name = row_tag[1]

        await cur.execute(query_create_articles_tag, (article_id, tag_id,))

        return ArticleResponse(
                id=row[0],
                user_id=row[1],
                tag=tag_name,
                title=row[2],
                content=row[3],
                created_at=row[4]
        )

async def get_article(conn: AsyncConnection, article_id: int) -> ArticleResponse:
    query = """
        SELECT a.id, a.user_id, a.title, a.content, a.created_at, t.name AS tag
        FROM Article a
        LEFT JOIN ArticleTag at ON a.id = at.article_id
        LEFT JOIN Tag t ON at.tag_id = t.id
        WHERE a.id = %s;
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
                created_at=row[4],
                tag=row[5]
            )
        return None

async def get_all_articles(conn: AsyncConnection) -> list[ArticleResponse]:
    query = """
        SELECT a.id, a.user_id, a.title, a.content, a.created_at, t.name AS tag
        FROM Article a
        LEFT JOIN ArticleTag at ON a.id = at.article_id
        LEFT JOIN Tag t ON at.tag_id = t.id
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
