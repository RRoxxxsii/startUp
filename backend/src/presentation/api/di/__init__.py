from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.presentation.api.di.database import DBProvider, uow_provider


def setup_uow(app: FastAPI, pool: async_sessionmaker[AsyncSession]):
    provider = DBProvider(pool)
    app.dependency_overrides[uow_provider] = provider.provide_db   # noqa
