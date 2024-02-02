from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine


def create_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(
        database_url,    # noqa
        poolclass=NullPool
    )


def get_async_session_maker(
        engine: AsyncEngine
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
