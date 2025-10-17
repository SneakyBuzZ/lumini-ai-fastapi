from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData
from app._core.config import settings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.lib.embeddings.qdrant import setup_qdrant

engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

meta_data = MetaData()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@asynccontextmanager
async def lifespan(app : FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await setup_qdrant()
    yield
    await engine.dispose()
