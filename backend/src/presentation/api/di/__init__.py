from fastapi import FastAPI
from redis import Redis  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.presentation.api.di.providers.common import (
    in_memory_provider,
    mailing_provider,
    uow_provider,
)
from src.presentation.api.di.providers.main import (
    DBProvider,
    MailingProvider,
    RedisProvider,
)


def setup_providers(
    app: FastAPI,
    is_production: bool,
    db_pool: async_sessionmaker[AsyncSession],
    redis_pool: Redis,
    mailing_settings,
):
    db = DBProvider(db_pool)
    redis = RedisProvider(redis_pool)
    mailing = MailingProvider(mailing_settings)
    app.dependency_overrides[uow_provider] = db.provide_db  # noqa
    app.dependency_overrides[in_memory_provider] = redis.provide_db  # noqa

    if is_production:
        app.dependency_overrides[  # noqa
            mailing_provider
        ] = mailing.provide_mailing
    else:
        app.dependency_overrides[  # noqa
            mailing_provider
        ] = mailing.provide_mailing_debug
