from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.repositories import UserRepository, AbstractUserRepository


class SqlAlchemyUOW:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class AppHolder:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo: AbstractUserRepository = UserRepository(session)


class UnitOfWork(SqlAlchemyUOW):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.app_holder = AppHolder(session)


class StubUnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.app_holder = AppHolder(session)

    async def commit(self):
        pass

    async def rollback(self):
        pass
