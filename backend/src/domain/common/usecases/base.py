from src.infrastructure.database.uow import AbstractUnitOfWork


class BaseUseCase:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow
