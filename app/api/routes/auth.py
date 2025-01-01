from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import UserCreate, Token
from app.services.auth_service import authenticate_user, create_user
from app.core.security import create_access_token
from app.db.session import get_db

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists.")
    token = create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    authenticated_user = await authenticate_user(user.username, user.password, db)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    token = create_access_token({"sub": authenticated_user.username})
    return {"access_token": token, "token_type": "bearer"}
