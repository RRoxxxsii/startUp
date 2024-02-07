from src.domain.app.dto.user import CreateUserDTO
from src.domain.app.exceptions.user import UserExists
from src.domain.app.usecases.user.base import UserUseCase
from src.infrastructure.database.models import UserORM
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.secure.pwd import AbstractPasswordHandler


class CreateUser(UserUseCase):

    async def __call__(self, user_dto: CreateUserDTO) -> UserORM | None:
        if await self.uow.app_holder.user_repo.get_user_by_email(user_dto.email):
            raise UserExists("User with this email already exists")
        elif await self.uow.app_holder.user_repo.get_user_by_username(user_dto.username):
            raise UserExists("User with this username already exists")

        user_dto_dict = user_dto.dict()
        user_dto_dict.pop("password")
        user = await self.uow.app_holder.user_repo.create(
            hashed_password=self.pwd_handler.hash_password(user_dto.password),
            **user_dto_dict
        )
        await self.uow.commit()
        return user


class UserInteractor:

    def __init__(self, uow: UnitOfWork, pwd_handler: AbstractPasswordHandler):
        self.uow = uow
        self.pwd_handler = pwd_handler

    async def create_user(self, user_dto: CreateUserDTO):
        return await CreateUser(self.uow, self.pwd_handler)(user_dto)
