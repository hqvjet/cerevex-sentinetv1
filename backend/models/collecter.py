from psycopg import AsyncConnection
from schemas.collecter import CollecterCreate


async def save_collecter(db: AsyncConnection, data: CollecterCreate):
    query = """
        INSERT INTO collecter (content, label)
        VALUES (%s, %s)
        RETURNING id, content, label
    """
    async with db.cursor() as cur:
        await cur.execute(query, (data.content, data.label))
        row = await cur.fetchone()
        if row:
            return {"id": row[0], "content": row[1], "label": row[2]}
    return None

async def get_all_collecter(db: AsyncConnection):
    query = """
        SELECT id, content, label
        FROM collecter
    """
    async with db.cursor() as cur:
        await cur.execute(query)
        rows = await cur.fetchall()
        return [{"id": row[0], "content": row[1], "label": row[2]} for row in rows]
