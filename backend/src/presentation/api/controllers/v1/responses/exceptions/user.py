from pydantic import Field
from src.presentation.api.controllers.v1.responses.exceptions.base import (
    ApiError,
)


class UserExistsResponse(ApiError):
    detail: str = Field("Пользователь с такими данными уже существует")


class TokenDoesNotExistResponse(ApiError):
    detail: str = Field("Страница не найдена")
