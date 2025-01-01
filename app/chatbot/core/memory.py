# from typing import Any, Dict, Optional
# from datetime import datetime
# import json
# import asyncio
# from sqlalchemy import Column, Integer, String, JSON, DateTime, create_engine
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import declarative_base, sessionmaker
# from langgraph.checkpoint import BaseCheckpointer

# Base = declarative_base()

# class StateCheckpoint(Base):
#     __tablename__ = 'state_checkpoints'
#     id = Column(Integer, primary_key=True)
#     thread_id = Column(String, index=True)
#     step = Column(String)
#     state = Column(JSON)
#     timestamp = Column(DateTime, default=datetime.utcnow)

# class AsyncPostgresSaver(BaseCheckpointer):
#     def __init__(self, connection_string: str):
#         self.engine = create_async_engine(connection_string)
#         self.async_session = sessionmaker(
#             self.engine, class_=AsyncSession, expire_on_commit=False
#         )

#     async def init_db(self):
#         async with self.engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)

#     async def get(self, thread_id: str, step: Optional[str] = None) -> Dict[str, Any]:
#         async with self.async_session() as session:
#             query = session.query(StateCheckpoint).filter(
#                 StateCheckpoint.thread_id == thread_id
#             )
#             if step:
#                 query = query.filter(StateCheckpoint.step == step)
#             checkpoint = await query.order_by(StateCheckpoint.timestamp.desc()).first()
#             return checkpoint.state if checkpoint else {}

#     async def put(self, thread_id: str, step: str, state: Dict[str, Any]):
#         async with self.async_session() as session:
#             checkpoint = StateCheckpoint(
#                 thread_id=thread_id,
#                 step=step,
#                 state=state
#             )
#             session.add(checkpoint)
#             await session.commit()


from app.core import config
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

 # Create a settings instance
settings = config.Settings()

async def initializeCheckpoint():
    checkpoint = await AsyncPostgresSaver.from_conn_string(settings.database_url_normal)
    return checkpoint