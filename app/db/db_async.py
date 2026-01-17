from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import os
from sqlmodel import SQLModel

DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None

async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async def get_session_async() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession() as session:
        yield session

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


asyncSessionDeb = Annotated[AsyncSession, Depends(get_session_async)]