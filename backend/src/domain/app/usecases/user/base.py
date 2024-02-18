from src.domain.common.usecases.base import BaseUseCase
from src.infrastructure.database.uow import AbstractUnitOfWork
from src.infrastructure.inmemory_db.service import AbstractInMemoryService
from src.infrastructure.mailing.services import AbstractEmailService
from src.infrastructure.secure.services import AbstractPasswordService


class CreateUserUseCase(BaseUseCase):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        pwd_service: AbstractPasswordService,
        email_service: AbstractEmailService,
    ) -> None:
        super().__init__(uow)
        self.pwd_service = pwd_service
        self.email_service = email_service


class AuthUserUseCase(BaseUseCase):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        pwd_service: AbstractPasswordService,
        in_memory_service: AbstractInMemoryService,
    ) -> None:
        super().__init__(uow)
        self.pwd_service = pwd_service
        self.in_memory_service = in_memory_service
