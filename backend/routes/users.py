from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from models.database import get_db_conn
from models.users import create_user, get_all_users, get_user_by_id, update_user, delete_user, login
from schemas.users import UserCreate, UserUpdate, UserResponse, UserLogin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=UserResponse)
async def create_users(user: UserCreate, conn: AsyncConnection = Depends(get_db_conn)):
    return await create_user(conn, user)

@router.post("/login", response_model=UserResponse)
async def login_user(data: UserLogin, conn: AsyncConnection = Depends(get_db_conn)):
    result = await login(conn, data)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result

@router.get("/get/{user_id}", response_model=UserResponse)
async def get_user_by_id_route(user_id: int, conn: AsyncConnection = Depends(get_db_conn)):
    result = await get_user_by_id(conn, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.get("/all", response_model=list[UserResponse])
async def get_all_users_route(conn: AsyncConnection = Depends(get_db_conn)):
    return await get_all_users(conn)

@router.put("/update/{user_id}")
async def update_user_route(user_id: int, user: UserUpdate, conn: AsyncConnection = Depends(get_db_conn)):
    result = await update_user(conn, user_id, user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found or no changes")
    return result

@router.delete("/delete/{user_id}")
async def delete_user_route(user_id: int, conn: AsyncConnection = Depends(get_db_conn)):
    result = await delete_user(conn, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
