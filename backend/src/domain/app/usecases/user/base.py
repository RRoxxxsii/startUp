from src.domain.common.usecases.base import BaseUseCase
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.inmemory.service import AbstractInMemoryService
from src.infrastructure.mailing.services import AbstractEmailService
from src.infrastructure.secure.services import AbstractPasswordService


class CreateUserUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        pwd_service: AbstractPasswordService,
        email_service: AbstractEmailService,
    ):
        super().__init__(uow)
        self.pwd_service = pwd_service
        self.email_service = email_service


class AuthUserUseCase(BaseUseCase):
    def __init__(
        self,
        uow: UnitOfWork,
        pwd_service: AbstractPasswordService,
        in_memory_service: AbstractInMemoryService,
    ):
        super().__init__(uow)
        self.pwd_service = pwd_service
        self.in_memory_service = in_memory_service
