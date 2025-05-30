from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from models.database import get_db_conn
from models.tag import create_tag, get_all_tags, get_tag, delete_tag, update_tag
from schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/create", response_model=TagResponse)
async def create(tag: TagCreate, conn: AsyncConnection = Depends(get_db_conn)):
    result = await create_tag(conn, tag)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create tag")
    return result

@router.get("/get/{tag_id}", response_model=TagResponse)
async def get(tag_id: int, conn: AsyncConnection = Depends(get_db_conn)):
    result = await get_tag(conn, tag_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tag not found")
    return result

@router.get("/all", response_model=list[TagResponse])
async def get_all(conn: AsyncConnection = Depends(get_db_conn)):
    return await get_all_tags(conn)

@router.put("/update/{tag_id}", response_model=TagResponse)
async def update_(tag_id: int, tag: TagUpdate, conn: AsyncConnection = Depends(get_db_conn)):
    result = await update_tag(conn, tag_id, tag)
    if not result:
        raise HTTPException(status_code=404, detail="Tag not found")
    return result

@router.delete("/delete/{tag_id}")
async def delete(tag_id: int, conn: AsyncConnection = Depends(get_db_conn)):
    result = await delete_tag(conn, tag_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"detail": "Tag deleted successfully"}
