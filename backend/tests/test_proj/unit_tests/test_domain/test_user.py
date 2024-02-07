import pytest
from pytest_mock import MockFixture
from src.domain.app.dto.user import CreateUserDTO
from src.domain.app.exceptions.user import UserExists
from src.domain.app.usecases.user.usecases import UserInteractor
from src.infrastructure.database.uow import StubUnitOfWork
from src.infrastructure.secure.pwd import PasslibPasswordHandler


class TestCreateUser:
    async def test_create_user_ok(
        self,
        user_in_data_unique: dict,
        mocker: MockFixture,
        create_mock_user,
    ):
        user_fixture = create_mock_user(**user_in_data_unique)

        mocker.patch(
            "src.infrastructure.database.repositories.user.implementation.UserRepository.get_user_by_email"  # noqa
        ).return_value = None
        mocker.patch(
            "src.infrastructure.database.repositories.user.implementation.UserRepository.get_user_by_username"  # noqa
        ).return_value = None
        mocker.patch(
            "src.infrastructure.database.repositories.base.BaseRepository.create"  # noqa
        ).return_value = user_fixture

        uow = StubUnitOfWork(...)

        user = await UserInteractor(uow, PasslibPasswordHandler()).create_user(
            CreateUserDTO(**user_in_data_unique)
        )

        assert user.email == user_in_data_unique.get("email")
        assert user.username == user_in_data_unique.get("username")

    async def test_create_user_failed_email_not_unique(
        self,
        user_in_data_unique: dict,
        mocker: MockFixture,
        create_mock_user,
    ):
        user_fixture = create_mock_user(**user_in_data_unique)

        mocker.patch(
            "src.infrastructure.database.repositories.user.implementation.UserRepository.get_user_by_email"  # noqa
        ).return_value = user_fixture
        mocker.patch(
            "src.infrastructure.database.repositories.user.implementation.UserRepository.get_user_by_username"  # noqa
        ).return_value = None

        uow = StubUnitOfWork(...)

        with pytest.raises(UserExists):
            await UserInteractor(uow, PasslibPasswordHandler()).create_user(
                CreateUserDTO(**user_in_data_unique)
            )

    async def test_create_user_failed_username_not_unique(
        self,
        user_in_data_unique: dict,
        mocker: MockFixture,
        create_mock_user,
    ):
        user_fixture = create_mock_user(**user_in_data_unique)
        mocker.patch(
            "src.infrastructure.database.repositories.user.implementation.UserRepository.get_user_by_email"  # noqa
        ).return_value = None
        mocker.patch(
            "src.infrastructure.database.repositories.user.implementation.UserRepository.get_user_by_username"  # noqa
        ).return_value = user_fixture

        uow = StubUnitOfWork(...)

        with pytest.raises(UserExists):
            await UserInteractor(uow, PasslibPasswordHandler()).create_user(
                CreateUserDTO(**user_in_data_unique)
            )
