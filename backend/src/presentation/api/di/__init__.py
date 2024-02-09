from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.presentation.api.di.database import DBProvider, uow_provider
from src.presentation.api.di.mailing import mailing_provider, MailingProvider


def setup_uow(app: FastAPI, pool: async_sessionmaker[AsyncSession]) -> None:
    provider = DBProvider(pool)
    app.dependency_overrides[uow_provider] = provider.provide_db  # noqa


def setup_mailing(app: FastAPI, settings, prod: bool) -> None:
    provider = MailingProvider(settings)

    if prod:
        app.dependency_overrides[
            mailing_provider
        ] = provider.provide_mailing  # noqa
    else:
        app.dependency_overrides[
            mailing_provider
        ] = provider.provide_mailing_debug  # noqa
