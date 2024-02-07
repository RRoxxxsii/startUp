from fastapi import Depends
from src.domain.app.usecases.user.usecases import UserInteractor
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.secure.pwd import AbstractPasswordHandler
from src.presentation.api.di import uow_provider
from src.presentation.api.di.common import get_password_handler


def get_user_services(
    uow: UnitOfWork = Depends(uow_provider),
    password_handler: AbstractPasswordHandler = Depends(get_password_handler),
) -> UserInteractor:
    return UserInteractor(uow, password_handler)
