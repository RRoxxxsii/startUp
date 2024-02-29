from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.infrastructure.database.models import UserORM
from src.infrastructure.database.repositories.base import (
    AbstractRepository,
    BaseRepository,
)


class AbstractUserRepository(AbstractRepository, ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserORM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserORM | None:
        raise NotImplementedError


class UserRepository(AbstractUserRepository, BaseRepository):
    _model = UserORM

    async def get_user_by_email(self, email: str) -> UserORM | None:
        stmt = select(self._model).where(self._model.email == email)
        user = await self._session.execute(stmt)
        return user.unique().scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserORM | None:
        stmt = select(self._model).where(self._model.username == username)
        user = await self._session.execute(stmt)
        return user.unique().scalar_one_or_none()

    async def get_by_id(self, id_: int) -> UserORM | None:
        stmt = (
            select(self._model)
            .where(self._model.id == id_)
            .options(selectinload(self._model.projects))
        )
        return (await self._session.execute(stmt)).scalar_one_or_none()
