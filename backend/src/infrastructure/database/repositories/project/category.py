from abc import ABC

from src.infrastructure.database.models import CategoryORM
from src.infrastructure.database.repositories.base import (AbstractRepository,
                                                           BaseRepository)


class AbstractCategoryRepository(AbstractRepository, ABC):
    pass


class CategoryRepository(AbstractCategoryRepository, BaseRepository):
    _model = CategoryORM
