import os

import uvicorn
from fastapi import FastAPI
from src.infrastructure.database.config import (
    create_engine,
    get_async_session_maker,
)
from src.infrastructure.mailing.config import EmailSettings
from src.infrastructure.settings import get_settings
from src.presentation.api.controllers import setup_controllers
from src.presentation.api.di import setup_mailing, setup_uow


def create_app() -> FastAPI:
    app = FastAPI()

    settings = get_settings()

    db_engine = create_engine(database_url=settings.PG_DSN)
    setup_uow(app, get_async_session_maker(db_engine))

    setup_mailing(
        app,
        settings=EmailSettings(),
        prod=True if os.getenv("PROD") else False,
    )
    setup_controllers(router=app.router)  # noqa
    return app


if __name__ == "__main__":
    uvicorn.run(
        app="src.presentation.api.main:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
