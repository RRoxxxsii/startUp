# from typing import Annotated
#
# from fastapi import Depends, HTTPException
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
# from src.infrastructure.database.config import get_async_session_maker
# from src.infrastructure.database.models import UserORM
# from src.presentation.api.dependencies import apikey_scheme
# from starlette import status

# async def get_current_user_or_401(
#     access_token: Annotated[str, Depends(apikey_scheme)],
#     session: AsyncSession = Depends(get_async_session_maker),
# ) -> UserORM | None:
#     stmt = select(Token)
#     .where(Token.access_token == access_token)
#     .options(selectinload(Token.user))
#
#     token = await session.execute(stmt)
#     if token:
#         token = token.scalar_one()
#         return token.user
#     else:
#         raise HTTPException(
#             status.HTTP_401_UNAUTHORIZED,
#             "Authorization has been refused for provided credentials"
#         )
