from fastapi import APIRouter, Depends, Response
from src.domain.app.dto.user import CreateUserDTO
from src.domain.app.exceptions.user import TokenDoesNotExist, UserExists
from src.domain.app.usecases.user.usecases import UserInteractor
from src.domain.common.dto.url import UrlPathDTO
from src.presentation.api.controllers.v1.docs.user import (
    create_user as create_user_docs,
)
from src.presentation.api.controllers.v1.requests.user import UserInSchema
from src.presentation.api.controllers.v1.responses.exceptions.user import (
    TokenDoesNotExistResponse,
    UserExistsResponse,
)
from src.presentation.api.controllers.v1.responses.user import (
    EmailConfirmed,
    UserOutSchema,
)
from src.presentation.api.di.services import get_user_services
from starlette import status
from starlette.requests import Request

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/create/",
    response_model=UserOutSchema | UserExistsResponse,
    status_code=status.HTTP_201_CREATED,
    responses=create_user_docs,
)
async def create_user(
    user_schema: UserInSchema,
    request: Request,
    response: Response,
    service: UserInteractor = Depends(get_user_services),
):
    try:
        user = await service.create_user(
            CreateUserDTO(**user_schema.model_dump()),
            UrlPathDTO(
                domain=str(request.base_url), path=str(request.url.path)
            ),
        )
    except UserExists:
        response.status_code = status.HTTP_409_CONFLICT
        return UserExistsResponse()
    else:
        response.status_code = status.HTTP_201_CREATED
        return user


@router.get(
    "/create/{token}",
    status_code=status.HTTP_200_OK,
    response_model=TokenDoesNotExistResponse | EmailConfirmed,
)
async def confirm_email(
    token: str,
    response: Response,
    service: UserInteractor = Depends(get_user_services),
):
    try:
        await service.confirm_email(token)
    except TokenDoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return TokenDoesNotExistResponse()
    else:
        response.status_code = status.HTTP_200_OK
        return EmailConfirmed()
