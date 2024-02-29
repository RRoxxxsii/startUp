from pydantic import Field
from src.presentation.api.controllers.v1.responses.exceptions.base import \
    ApiError


class ProjectExistsResponse(ApiError):
    detail: str = Field("Проект с таким названием уже существует")
