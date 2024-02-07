from abc import ABC, abstractmethod

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.base import AbstractModel


class AbstractRepository(ABC):
    _model: type[AbstractModel]

    @abstractmethod
    def __init__(self, session: AsyncSession):  # noqa
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_obj(self, id_: int, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_obj(self, id_: int) -> None:
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    _model: type[AbstractModel]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, **kwargs):
        obj = self._model(**kwargs)
        self._session.add(obj)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def get_by_id(self, id_: int):
        stmt = select(self._model).where(self._model.id == id_)
        return (await self._session.execute(stmt)).scalar_one_or_none()

    async def get_all(self):
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def update_obj(self, id_: int, **kwargs) -> None:
        query = update(self._model).where(self._model.id == id_).values(kwargs)
        await self._session.execute(query)

    async def delete_obj(self, id_: int) -> None:
        query = delete(self._model).where(self._model.id == id_)
        await self._session.execute(query)
