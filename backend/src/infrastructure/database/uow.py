from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.repositories import (
    AbstractCategoryRepository,
    AbstractProjectRepository,
    AbstractTokenRepository,
    AbstractUserRepository,
    CategoryRepository,
    ProjectRepository,
    TokenRepository,
    UserRepository,
)


class AbstractUnitOfWork:
    token_repo: AbstractTokenRepository
    user_repo: AbstractUserRepository
    project_repo: AbstractProjectRepository
    category_repo: AbstractCategoryRepository

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.user_repo = UserRepository(self._session)
        self.token_repo = TokenRepository(self._session)
        self.project_repo = ProjectRepository(self._session)
        self.category_repo = CategoryRepository(self._session)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()


class StubUnitOfWork(UnitOfWork):
    async def commit(self):
        pass

    async def rollback(self):
        pass
