from abc import ABC, abstractmethod

from src.infrastructure.database.models import UserORM
from src.infrastructure.database.repositories.base import AbstractRepository


class AbstractUserRepository(AbstractRepository, ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserORM | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserORM | None:
        raise NotImplementedError
