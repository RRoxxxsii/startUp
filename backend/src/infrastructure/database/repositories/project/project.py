from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm.strategy_options import joinedload, selectinload
from src.infrastructure.database.models import ProjectORM
from src.infrastructure.database.repositories.base import (AbstractRepository,
                                                           BaseRepository)


class AbstractProjectRepository(AbstractRepository, ABC):
    @abstractmethod
    async def get_project_by_title(self, title: str) -> ProjectORM | None:
        raise NotImplementedError


class ProjectRepository(AbstractProjectRepository, BaseRepository):
    _model = ProjectORM

    async def get_project_by_title(self, title: str) -> ProjectORM | None:
        stmt = (
            select(self._model)
            .where(self._model.title == title)
        )
        project = await self._session.execute(stmt)
        return project.scalar_one_or_none()
