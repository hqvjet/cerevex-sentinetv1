from psycopg import AsyncConnection
from schemas.comment import CommentCreate, CommentUpdate, CommentResponse

async def create_comment(db: AsyncConnection, comment: CommentCreate):
    query = """
        INSERT INTO Comment (article_id, user_id, content, sentiment)
        VALUES (%s, %s, %s, %s)
        RETURNING id, article_id, user_id, content, sentiment, created_at
    """
    async with db.cursor() as cur:
        await cur.execute(query, (comment.article_id, comment.user_id, comment.content, comment.sentiment))
        row = await cur.fetchone()
        if row:
            return ({
                "id":row[0],
                "article_id":row[1],
                "user_id":row[2],
                "content":row[3],
                "sentiment":row[4],
                "created_at":row[5]
            })

async def get_all_comments(db: AsyncConnection):
    query = """SELECT c.id, u.name, c.article_id, c.content, c.sentiment, c.created_at
        FROM comment m 
        LEFT JOIN users u ON c.user_id = u.id"""
    async with db.cursor() as cur:
        await cur.execute(query)
        rows = await cur.fetchall()
        return [CommentResponse(
            id=row[0],
            name=row[1],
            article_id=row[2],
            content=row[3],
            sentiment=row[4],
            created_at=row[5]
        ) for row in rows]

async def get_comments_by_article(db: AsyncConnection, aritcle_id: int):
    query = """
        SELECT c.id, u.name, c.article_id, c.content, c.sentiment, c.created_at
        FROM comment m 
        LEFT JOIN users u ON c.user_id = u.id
        WHERE article_id = %s
    """
    async with db.cursor() as cur:
        await cur.execute(query, (aritcle_id,))
        rows = cur.fetchall()
        comments = []
        for row in rows:
            comments.append({
                "id":row[0],
                "name":row[1],
                "aritcle_id": row[2],
                "content":row[3],
                "sentiment":row[4],
                "created_at":row[5]
            })

async def delete_comment(db: AsyncConnection, comment_id: int):
    query = """DELETE FROM Comment WHERE id = %s RETURNING id"""
    async with db.cursor() as cur:
        await cur.execute(query, (comment_id,))
        row = await cur.fetchone()
        return bool(row)
