import os
from collections.abc import AsyncGenerator
from typing import Any

import faker
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from redis import Redis  # type: ignore
from sqlalchemy import text
from sqlalchemy.orm import close_all_sessions, sessionmaker
from src.infrastructure.database.main import (
    create_engine,
    get_async_session_maker,
)
from src.infrastructure.inmemory_db.main import init_redis_pool
from src.infrastructure.settings import get_settings
from src.presentation.api.controllers import setup_controllers
from src.presentation.api.di import setup_providers


def create_test_app() -> FastAPI:
    """Creating FastAPI application for testing purposes"""

    app = FastAPI()
    settings = get_settings()

    db_pool = get_async_session_maker(
        create_engine(database_url=settings.POSTGRES_DB.PG_DSN)
    )
    redis_pool = init_redis_pool(host=os.getenv("REDIS_HOST"))

    setup_controllers(router=app.router)  # noqa
    setup_providers(
        app,
        is_production=False,
        db_pool=db_pool,
        redis_pool=redis_pool,
        mailing_settings=get_settings().SMTP_MAIL,
    )

    return app


@pytest_asyncio.fixture(scope="session")
async def db_session_test() -> sessionmaker:
    yield get_async_session_maker(
        create_engine(get_settings().POSTGRES_DB.PG_DSN)
    )
    close_all_sessions()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_tables(db_session_test) -> None:
    tables = (
        "users",
        "tokens",
        "users_projects",
        "categories",
        "resources",
        "projects",
    )
    async with db_session_test() as session:
        for table in tables:
            stmt = text(f"""TRUNCATE TABLE {table} CASCADE;""")
            await session.execute(stmt)
            await session.commit()


@pytest_asyncio.fixture(scope="function")
async def api_client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
        app=create_test_app(), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def redis_pool() -> Redis:
    return init_redis_pool(host=os.getenv("REDIS_HOST"))


@pytest.fixture(scope="function", autouse=True)
def clean_redis(redis_pool) -> None:
    redis_pool.flushdb()


@pytest.fixture
def mock_redis_pool() -> dict:
    return {}


fake = faker.Faker()
