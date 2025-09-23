from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, DeclarativeBase
from config import DATABASE_URL

class Base(DeclarativeBase): pass


async_engine = create_async_engine(DATABASE_URL, echo=True )

AsyncSessionLocal = async_sessionmaker(async_engine)

@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session