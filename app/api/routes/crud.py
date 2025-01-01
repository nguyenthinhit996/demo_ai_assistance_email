from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ChatHistory
from app.db.session import get_db

router = APIRouter()

@router.get("/")
async def get_chats(db: AsyncSession = Depends(get_db)):
    chats = await db.execute(select(ChatHistory))
    return chats.scalars().all()
