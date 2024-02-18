from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

import pytest
from src.infrastructure.mailing.config import SMTPMailConfig


@dataclass(frozen=True)
class FakeSMTPMailConfig(SMTPMailConfig):
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

    id: int
    password: str
    username: str
    email: str
    surname: str
    firstname: str


@dataclass(frozen=True)
class MockToken:
    id: int
    access_token: str
    time_created: datetime


@pytest.fixture
def create_mock_user() -> Callable[[int, str, str, str, str, str], MockUser]:
    def wrapper(
        pk: int,
        password: str,
        username: str,
        email: str,
        surname: str,
        firstname: str,
    ):
        mock_user = MockUser(pk, password, username, email, surname, firstname)

        return mock_user

    return wrapper


@pytest.fixture
def create_mock_token() -> Callable[[int, str, Any], MockToken]:
    def wrapper(pk: int, access_token: str, time_created):
        mock_token = MockToken(pk, access_token, time_created)
        return mock_token

    return wrapper
