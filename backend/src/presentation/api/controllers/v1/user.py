from fastapi import Depends, APIRouter, Response
from starlette import status

from src.domain.app.dto.user import CreateUserDTO
from src.domain.app.exceptions.user import UserExists
from src.domain.app.usecases.user.usecases import UserInteractor
from src.presentation.api.controllers.v1.docs.user import create_user
from src.presentation.api.controllers.v1.requests.user import UserInSchema
from src.presentation.api.controllers.v1.responses.exceptions.user import UserExistsResponse
from src.presentation.api.controllers.v1.responses.user import UserOutSchema
from src.presentation.api.di.services import get_user_services


router = APIRouter(prefix="/user", tags=["user"])


@router.post('/create/', response_model=UserOutSchema | UserExistsResponse, status_code=status.HTTP_201_CREATED, responses=create_user)
async def create_user(
        user_schema: UserInSchema,
        response: Response,
        service: UserInteractor = Depends(get_user_services)
):
    try:
        user = await service.create_user(CreateUserDTO(**user_schema.model_dump()))
    except UserExists:
        response.status_code = status.HTTP_409_CONFLICT
        return UserExistsResponse()
    else:
        response.status_code = status.HTTP_201_CREATED
        return user