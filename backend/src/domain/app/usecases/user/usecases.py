from src.domain.app.dto.user import CreateUserDTO
from src.domain.app.exceptions.user import UserExists
from src.domain.app.usecases.user.base import UserUseCase
from src.domain.common.dto.mail import EmailDTO
from src.domain.common.dto.url import UrlPathDTO
from src.infrastructure.database.models import UserORM
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.mailing.services import AbstractEmailService
from src.infrastructure.secure.services import AbstractPasswordService


class CreateUser(UserUseCase):
    def _send_email(self, to_email: str, urlpath_dto: UrlPathDTO):
        dto = EmailDTO(
            to_email=to_email,
            subject="Активация аккаунта",
            template_name="activation.html",
            extra={"activation_url": urlpath_dto.domain},
        )

        self.email_service.send_message(dto)

    async def execute(
        self, user_dto: CreateUserDTO, urlpath_dto: UrlPathDTO
    ) -> UserORM | None:
        if await self.uow.app_holder.user_repo.get_user_by_email(
            user_dto.email
        ):
            raise UserExists("User with this email already exists")
        elif await self.uow.app_holder.user_repo.get_user_by_username(
            user_dto.username
        ):
            raise UserExists("User with this username already exists")

        user_dto_dict = user_dto.dict()
        user_dto_dict.pop("password")
        user = await self.uow.app_holder.user_repo.create(
            hashed_password=self.pwd_service.hash_password(user_dto.password),
            **user_dto_dict
        )
        await self.uow.commit()
        self._send_email(to_email=user_dto.email, urlpath_dto=urlpath_dto)
        return user


class UserInteractor:
    def __init__(
        self,
        uow: UnitOfWork,
        pwd_service: AbstractPasswordService,
        email_service: AbstractEmailService,
    ):
        self.uow = uow
        self.pwd_service = pwd_service
        self.email_service = email_service

    async def create_user(
        self, user_dto: CreateUserDTO, urlpath_dto: UrlPathDTO
    ):
        return await CreateUser(
            self.uow, self.pwd_service, self.email_service
        ).execute(user_dto, urlpath_dto)
