from typing import Callable, Any, Coroutine, Dict

import pytest
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.models import UserORM
from tests.conftest import fake


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def user_in_data_unique() -> dict:
    """
    Fixture complying with the unique constraints
    """
    data = {
        "password": fake.word(),
        "username": fake.unique.user_name(),
        "email": fake.unique.free_email(),
        "surname": fake.first_name(),
        "firstname": fake.last_name()
    }
    return data


@pytest.fixture
def user_in_data_common() -> dict:
    """
    Fixture violating with the unique constraints
    """
    data = {
        "password": fake.word(),
        "username": fake.user_name(),
        "email": fake.free_email(),
        "surname": fake.first_name(),
        "firstname": fake.last_name()
    }
    return data


@pytest.fixture
async def create_user(db_session_test: sessionmaker):
    async def wrapper(**kwargs):
        async with db_session_test() as session:
            kwargs["hashed_password"] = pwd_context.hash(kwargs.pop("password"))
            user_ = UserORM(**kwargs)
            session.add(user_)
            await session.commit()
            await session.refresh(user_)
            return user_
    return wrapper
