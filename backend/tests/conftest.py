import os
from collections.abc import AsyncGenerator
from typing import Any

import faker
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.orm import close_all_sessions, sessionmaker
from src.infrastructure.database.config import (
    create_engine,
    get_async_session_maker,
)
from src.infrastructure.inmemory.config import init_redis_pool
from src.infrastructure.mailing.config import EmailSettings
from src.infrastructure.settings import get_settings
from src.presentation.api.controllers import setup_controllers
from src.presentation.api.di import (
    setup_in_memory_db,
    setup_mailing,
    setup_uow,
)


def create_test_app() -> FastAPI:
    """Creating FastAPI application for testing purposes"""
    app = FastAPI()

    settings = get_settings()

    db_engine = create_engine(settings.PG_DSN)

    setup_uow(app, get_async_session_maker(db_engine))
    setup_mailing(app, settings=EmailSettings(), prod=False)
    setup_controllers(app.router)  # noqa

    pool = init_redis_pool(host=os.getenv("REDIS_HOST"))
    setup_in_memory_db(app, pool)

    return app


@pytest_asyncio.fixture(scope="session")
async def db_session_test() -> sessionmaker:
    yield get_async_session_maker(create_engine(get_settings().PG_DSN))
    close_all_sessions()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_tables(db_session_test) -> None:
    tables = ("users",)
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


fake = faker.Faker()
