from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.repositories.token import (
    AbstractTokenRepository,
    TokenRepository,
)
from src.infrastructure.database.repositories.user import (
    AbstractUserRepository,
    UserRepository,
)


class AbstractUnitOfWork:
    token_repo: AbstractTokenRepository
    user_repo: AbstractUserRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self):
        self.user_repo = UserRepository(self._session)
        self.token_repo = TokenRepository(self._session)
        return super().__aenter__()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()


class StubUnitOfWork(UnitOfWork):
    async def commit(self):
        pass

    async def rollback(self):
        pass
