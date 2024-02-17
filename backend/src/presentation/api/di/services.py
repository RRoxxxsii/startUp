from fastapi import Depends
from src.domain.app.usecases.user.usecases import UserInteractor
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.inmemory.service import AbstractInMemoryService
from src.infrastructure.mailing.services import AbstractEmailService
from src.infrastructure.secure.services import AbstractPasswordService
from src.presentation.api.di import (
    in_memory_provider,
    mailing_provider,
    uow_provider,
)
from src.presentation.api.di.common import get_password_service


def get_user_services(
    uow: UnitOfWork = Depends(uow_provider),
    in_memory_service: AbstractInMemoryService = Depends(in_memory_provider),
    password_handler: AbstractPasswordService = Depends(get_password_service),
    email_service: AbstractEmailService = Depends(mailing_provider),
) -> UserInteractor:
    return UserInteractor(
        uow, password_handler, email_service, in_memory_service
    )
