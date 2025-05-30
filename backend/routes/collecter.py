from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from models.database import get_db_conn
from models.collecter import save_collecter
from schemas.collecter import CollecterCreate, CollecterResponse
router = APIRouter(tags=["Collecter"])

@router.post("/collecter", response_model=CollecterResponse)
async def create_collecter(data: CollecterCreate, db : AsyncConnection = Depends(get_db_conn)):
    return await save_collecter(db, data)

@router.get("/collecter", response_model=list[CollecterResponse])
async def get_all_collecter(db: AsyncConnection = Depends(get_db_conn)):
    rows = await get_all_collecter(db)
    if not rows:
        raise HTTPException(status_code=404, detail="No collecters found")
    return rows