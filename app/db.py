from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app import config


class Base(DeclarativeBase):
    pass


engine = create_async_engine(config.DATABASE_URL)
Session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with Session() as session:
        yield session
