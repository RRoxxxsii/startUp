from collections.abc import Callable
from dataclasses import dataclass

import pytest


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
