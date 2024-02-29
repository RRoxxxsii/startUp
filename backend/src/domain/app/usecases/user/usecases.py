import uuid

from src.domain.app.dto.user import AuthDTO, CreateUserDTO
from src.domain.app.exceptions.user import (
    PasswordDoesNotMatch,
    TokenDoesNotExist,
    UserDoesNotExist,
    UserExists,
)
from src.domain.app.usecases.user.base import (
    AuthUserUseCase,
    CreateUserUseCase,
)
from src.domain.common.dto.mail import EmailDTO
from src.domain.common.dto.url import UrlPathDTO
from src.domain.common.usecases.base import BaseUseCase
from src.infrastructure.database.models import TokenORM, UserORM
from src.infrastructure.database.uow import AbstractUnitOfWork
from src.infrastructure.inmemory_db.service import AbstractInMemoryService
from src.infrastructure.mailing.services import AbstractEmailService
from src.infrastructure.secure.services import AbstractPasswordService


class CreateUser(CreateUserUseCase):
    def _send_email(self, to_email: str, urlpath_dto: UrlPathDTO) -> None:
        dto = EmailDTO(
            to_email=to_email,
            subject="Активация аккаунта",
            template_name="activation.html",
            extra={"activation_url": urlpath_dto.base_url},
        )

        self.email_service.send_message(dto)

    async def execute(
        self, user_dto: CreateUserDTO, urlpath_dto: UrlPathDTO
    ) -> UserORM | None:
        if await self.uow.user_repo.get_user_by_email(user_dto.email):
            await self.uow.rollback()
            raise UserExists("User with this email already exists")

        elif await self.uow.user_repo.get_user_by_username(user_dto.username):
            await self.uow.rollback()
            raise UserExists("User with this username already exists")

        user_dto_dict = user_dto.dict()
        user_dto_dict.pop("password")
        user: UserORM = await self.uow.user_repo.create(
            hashed_password=self.pwd_service.hash_password(user_dto.password),
            **user_dto_dict,
        )
        token: TokenORM = await self.uow.token_repo.create(
            user_id=user.id, access_token=str(uuid.uuid4())
        )
        await self.uow.commit()
        urlpath_dto.path += token.access_token
        self._send_email(to_email=user_dto.email, urlpath_dto=urlpath_dto)
        return user


class ConfirmEmail(BaseUseCase):
    async def execute(self, token: str) -> None:
        token = await self.uow.token_repo.get_token_by_uuid(token)
        if not token:
            await self.uow.rollback()
            raise TokenDoesNotExist("This token does not exist")
        await self.uow.user_repo.update_obj(token.user_id, is_active=True)
        await self.uow.commit()


class AuthUser(AuthUserUseCase):
    async def execute(self, dto: AuthDTO) -> str:
        user = await self.uow.user_repo.get_user_by_email(dto.email)

        if not user:
            await self.uow.rollback()
            raise UserDoesNotExist("User with provided email does not exist")

        if not self.pwd_service.check_password(
            password=dto.password, hashed_password=user.hashed_password
        ):
            await self.uow.rollback()
            raise PasswordDoesNotMatch(
                "Email does not appear to match the password"
            )

        if self.in_memory_service.get_value(f"user:{user.id}"):
            self.in_memory_service.delete_value(f"user:{user.id}")

        token = str(uuid.uuid4())
        self.in_memory_service.set_value(key=f"user:{user.id}", value=token)
        await self.uow.commit()
        return token


class GetCurrentUserID(AuthUserUseCase):
    async def execute(self, token: str) -> int | None:  # type: ignore
        if user_key := self.in_memory_service.get_key(value=token):
            await self.uow.commit()
            return int(user_key.split(":")[-1])


class UserInteractor:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        pwd_service: AbstractPasswordService,
        email_service: AbstractEmailService,
        in_memory_service: AbstractInMemoryService,
    ) -> None:
        self.uow = uow
        self.pwd_service = pwd_service
        self.email_service = email_service
        self.in_memory_service = in_memory_service

    async def create_user(
        self, user_dto: CreateUserDTO, urlpath_dto: UrlPathDTO
    ) -> UserORM:
        return await CreateUser(
            self.uow, self.pwd_service, self.email_service
        ).execute(user_dto, urlpath_dto)

    async def confirm_email(self, token: str) -> None:
        await ConfirmEmail(self.uow).execute(token)

    async def auth_user(self, dto: AuthDTO) -> str:
        return await AuthUser(
            self.uow, self.pwd_service, self.in_memory_service
        ).execute(dto)

    async def get_current_user_id_or_none(self, token: str) -> int | None:
        return await GetCurrentUserID(
            self.uow, self.pwd_service, self.in_memory_service
        ).execute(token)
