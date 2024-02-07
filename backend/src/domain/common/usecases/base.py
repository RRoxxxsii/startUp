from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.secure.pwd import AbstractPasswordHandler


class BaseUseCase:
    def __init__(self, uow: UnitOfWork, pwd_handler: AbstractPasswordHandler) -> None:
        self.uow = uow
        self.pwd_handler = pwd_handler
