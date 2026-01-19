from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import os
from sqlmodel import SQLModel

DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None

ECHO_DB: bool = True if os.getenv("ECHO_DB") == 'True' else False

async_engine = create_async_engine(
    DATABASE_URL, 
    echo=ECHO_DB,
    pool_size=30,
    max_overflow=10
    )

asyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=True
)

async def get_session_async() -> AsyncGenerator[AsyncSession, None]:
    async with asyncSessionLocal() as session:
        yield session

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


asyncSessionDep = Annotated[AsyncSession, Depends(get_session_async)]