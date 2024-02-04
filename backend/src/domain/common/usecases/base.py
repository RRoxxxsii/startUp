from src.infrastructure.database.uow import UnitOfWork


class BaseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
