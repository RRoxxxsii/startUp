import random

import pytest
from passlib.context import CryptContext
from redis import Redis  # type: ignore
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models import CategoryORM, ProjectORM, UserORM
from src.infrastructure.database.models.project import EnumStatus
from src.infrastructure.mailing.utils import get_mediator
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
        "firstname": fake.last_name(),
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
        "firstname": fake.last_name(),
    }
    return data


@pytest.fixture
def category_data() -> dict:
    data = {
        "title": fake.unique.word(),
        "description": fake.sentence(nb_words=3),
    }
    return data


@pytest.fixture
def project_in_data_unique() -> dict:
    """
    Fixture complying with the unique constraints
    """
    data = {
        "title": fake.unique.sentence(nb_words=6),
        "description": fake.sentence(nb_words=10),
        "status": str(random.choice(list(EnumStatus))),
    }
    return data


@pytest.fixture
def project_in_data_common(category_id: int) -> dict:
    """
    Fixture violating with the unique constraints
    """
    data = {
        "title": fake.unique.sentence(nb_words=6),
        "description": fake.sentence(nb_words=10),
    }
    return data


@pytest.fixture
def create_category(db_session_test: sessionmaker):
    async def wrapper(**kwargs):
        async with db_session_test() as session:
            category = CategoryORM(**kwargs)
            session.add(category)
            await session.commit()
            await session.refresh(category)
            return category

    return wrapper


@pytest.fixture
def create_project(db_session_test: sessionmaker):
    async def wrapper(**kwargs):
        async with db_session_test() as session:
            category = ProjectORM(**kwargs)
            session.add(category)
            await session.commit()
            await session.refresh(category)
            return category

    return wrapper


@pytest.fixture
async def create_user(db_session_test: sessionmaker):
    async def wrapper(**kwargs):
        async with db_session_test() as session:
            kwargs["hashed_password"] = pwd_context.hash(
                kwargs.pop("password")
            )
            user_ = UserORM(**kwargs)
            session.add(user_)
            await session.commit()
            await session.refresh(user_)
            return user_

    return wrapper


@pytest.fixture
def create_redis_data(redis_pool: Redis):
    def wrapper(key: str, value: str):
        redis_pool.set(key, value)
        return {key: value}

    return wrapper


@pytest.fixture
def create_mock_redis_data(pool: dict | None = None):
    if pool is None:
        pool = dict()

    def wrapper(**kwargs):
        pool.update(**kwargs)
        return kwargs

    return wrapper


@pytest.fixture
def outbox() -> list:
    mediator = get_mediator()
    if mediator.get_outbox():
        mediator.clear_outbox()
    return mediator.get_outbox()
