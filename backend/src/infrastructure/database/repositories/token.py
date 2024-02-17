from abc import ABC, abstractmethod

from sqlalchemy import select, desc

from src.infrastructure.database.models.user import TokenORM
from src.infrastructure.database.repositories.base import AbstractRepository, BaseRepository


class AbstractTokenRepository(AbstractRepository, ABC):

    @abstractmethod
    async def get_token_by_user(self, user_id: int) -> TokenORM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_token_by_uuid(self, token: str) -> TokenORM | None:
        raise NotImplementedError


class TokenRepository(AbstractTokenRepository, BaseRepository):
    _model = TokenORM

    async def get_token_by_user(self, user_id: int) -> TokenORM | None:
        stmt = select(self._model).where(self._model.user_id == user_id).order_by(desc(self._model.time_created))
        token = await self._session.execute(stmt)
        return token.scalar_one_or_none()

    async def get_token_by_uuid(self, token: str) -> TokenORM | None:
        stmt = select(self._model).where(self._model.access_token == token)
        token = await self._session.execute(stmt)
        return token.scalar_one_or_none()     # type: ignore
