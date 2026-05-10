import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://admin:password@localhost:5432/interview_db")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session_maker() as session:
        yield session
