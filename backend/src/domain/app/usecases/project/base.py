from src.domain.common.usecases.base import BaseUseCase
from src.infrastructure.database.uow import AbstractUnitOfWork


class BaseProjectUseCase(BaseUseCase):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        super().__init__(uow)
