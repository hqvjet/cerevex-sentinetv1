from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from models.database import get_db_conn
from models.comment import create_comment, get_all_comments, get_comments_by_article, delete_comment
from schemas.comment import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/create", response_model=CommentResponse)
async def create_comments(comment: CommentCreate, conn: AsyncConnection = Depends(get_db_conn)):
    return await create_comment(conn, comment)

@router.get("/all", response_model=list[CommentResponse])
async def get_all(conn: AsyncConnection = Depends(get_db_conn)):
    return await get_all_comments(conn)


@router.delete("/delete/{comment_id}")
async def delete_cmt(comment_id: int, conn: AsyncConnection = Depends(get_db_conn)):
    result = await delete_comment(conn, comment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
