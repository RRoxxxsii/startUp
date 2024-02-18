import os

import uvicorn
from fastapi import FastAPI
from src.infrastructure.database.main import (
    create_engine,
    get_async_session_maker,
)
from src.infrastructure.inmemory_db.main import init_redis_pool
from src.infrastructure.settings import get_settings
from src.presentation.api.controllers import setup_controllers
from src.presentation.api.di import setup_providers


def create_app() -> FastAPI:
    app = FastAPI()
    settings = get_settings()

    db_pool = get_async_session_maker(
        create_engine(database_url=settings.POSTGRES_DB.PG_DSN)
    )
    redis_pool = init_redis_pool(host=os.getenv("REDIS_HOST"))

    setup_controllers(router=app.router)  # noqa
    setup_providers(
        app,
        is_production=bool(os.getenv("PROD")),
        db_pool=db_pool,
        redis_pool=redis_pool,
        mailing_settings=get_settings().SMTP_MAIL,
    )

    return app


if __name__ == "__main__":
    uvicorn.run(
        app="src.presentation.api.main:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
