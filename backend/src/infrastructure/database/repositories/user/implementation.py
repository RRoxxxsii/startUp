from sqlalchemy import select

from src.infrastructure.database.models import UserORM
from src.infrastructure.database.repositories.user.interface import AbstractUserRepository
from src.infrastructure.database.repositories.base import BaseRepository


class UserRepository(AbstractUserRepository, BaseRepository):
    _model = UserORM

    async def get_user_by_email(self, email: str) -> UserORM | None:
        stmt = select(self._model).where(self._model.email == email)
        user = await self._session.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserORM | None:
        stmt = select(self._model).where(self._model.username == username)
        user = await self._session.execute(stmt)
        return user.scalar_one_or_none()

