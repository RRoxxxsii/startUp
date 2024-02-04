from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.database.uow import UnitOfWork


class DBProvider:

    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def provide_db(self):
        async with self.pool() as session:
            yield UnitOfWork(session)


def uow_provider() -> None:
    pass
