from abc import ABC, abstractmethod

from src.infrastructure.database.models.user import TokenORM
from src.infrastructure.database.repositories.base import AbstractRepository


class AbstractTokenRepository(AbstractRepository, ABC):

    @abstractmethod
    async def get_token_by_user(self, user_id: int) -> TokenORM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_token_by_uuid(self, token: str) -> TokenORM | None:
        raise NotImplementedError
