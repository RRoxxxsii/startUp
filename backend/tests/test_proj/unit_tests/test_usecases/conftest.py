import pytest

from src.domain.app.usecases.user.usecases import UserInteractor
from src.infrastructure.database.uow import StubUnitOfWork
from src.infrastructure.inmemory.service import StubInMemoryService
from src.infrastructure.mailing.services import DebugEmailService
from src.infrastructure.secure.services import PasslibPasswordService
from tests.test_proj.unit_tests.conftest import FakeEmailSettings


@pytest.fixture
def user_interactor() -> UserInteractor:

    uow = StubUnitOfWork(...)
    email_service = DebugEmailService(FakeEmailSettings())

    return UserInteractor(
        uow, PasslibPasswordService(), email_service, StubInMemoryService(...)
    )
