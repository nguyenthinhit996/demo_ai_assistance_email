from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User
from passlib.context import CryptContext
from app.core.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user, db: AsyncSession):
    query = select(User).where(User.username == user.username)
    existing_user = await db.execute(query)
    if existing_user.scalar():
        return None

    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    return new_user

async def authenticate_user(username: str, password: str, db: AsyncSession):
    query = select(User).where(User.username == username)
    user = await db.execute(query)
    user = user.scalar()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user
