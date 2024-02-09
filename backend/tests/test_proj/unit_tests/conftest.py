from collections.abc import Callable
from dataclasses import asdict, dataclass

import pytest
from src.infrastructure.mailing.config import EmailSettings


@dataclass(frozen=True)
class FakeEmailSettings(EmailSettings):
    MAIL_USERNAME: str = "fake"
    MAIL_PASSWORD: str = "fake"
    MAIL_FROM: str = "fake"

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass(frozen=True)
class MockUser:
    """
    Mock object for user
    """

    password: str
    username: str
    email: str
    surname: str
    firstname: str


@pytest.fixture
def create_mock_user() -> Callable[[str, str, str, str, str], MockUser]:
    def wrapper(
        password: str, username: str, email: str, surname: str, firstname: str
    ):
        mock_user = MockUser(password, username, email, surname, firstname)

        return mock_user

    return wrapper
