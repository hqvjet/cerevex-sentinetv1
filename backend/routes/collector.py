from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from models.database import get_db_conn
from models.collector import save_collector
from schemas.collector import CollectorCreate, CollectorResponse
router = APIRouter(tags=["Collecter"])

@router.post("/collector", response_model=CollectorResponse)
async def create_collector(data: CollectorCreate, db : AsyncConnection = Depends(get_db_conn)):
    return await save_collector(db, data)

@router.get("/collector", response_model=list[CollectorResponse])
async def get_all_collector(db: AsyncConnection = Depends(get_db_conn)):
    rows = await get_all_collector(db)
    if not rows:
        raise HTTPException(status_code=404, detail="No collectors found")
    return rows