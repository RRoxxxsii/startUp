from fastapi import APIRouter
from src.presentation.api.controllers.v1.project import (
    router as project_router,
)
from src.presentation.api.controllers.v1.user import router as user_router


def setup_controllers(router: APIRouter) -> None:
    router.include_router(user_router)
    router.include_router(project_router)
