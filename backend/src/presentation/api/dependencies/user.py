from typing import Annotated

from fastapi import Depends, HTTPException
from src.domain.app.usecases.user.usecases import UserInteractor
from src.presentation.api.dependencies import apikey_scheme
from src.presentation.api.di.services import get_user_services
from starlette import status


async def get_current_user_or_401(
    access_token: Annotated[str, Depends(apikey_scheme)],
    service: UserInteractor = Depends(get_user_services),
) -> int | None:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user_id = await service.get_current_user_id_or_none(access_token)
    if user_id:
        return user_id
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED, "Authorization has been refused"
    )
