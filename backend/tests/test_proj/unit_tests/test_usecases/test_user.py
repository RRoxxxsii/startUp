import datetime
import uuid

import pytest
from pytest_mock import MockFixture
from src.domain.app.dto.user import AuthDTO, CreateUserDTO
from src.domain.app.exceptions.user import (
    PasswordDoesNotMatch,
    UserDoesNotExist,
    UserExists,
)
from src.domain.common.dto.url import UrlPathDTO
from tests.conftest import fake


class TestCreateUser:
    async def test_create_user_ok(
        self,
        user_in_data_unique: dict,
        mocker: MockFixture,
        create_mock_user,
        create_mock_token,
        outbox,
        user_interactor,
    ):
        user_fixture = create_mock_user(
            fake.unique.random_int(), **user_in_data_unique
        )
        token_fixture = create_mock_token(
            fake.unique.random_int(),
            str(uuid.uuid4()),
            datetime.datetime.now(),
        )
        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_email"  # noqa
        ).return_value = None
        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_username"  # noqa
        ).return_value = None
        mocker.patch(
            "src.infrastructure.database.repositories.user.token."
            "TokenRepository.create"
        ).return_value = token_fixture
        mocker.patch(
            "src.infrastructure.database.repositories.base.BaseRepository.create"  # noqa
        ).return_value = user_fixture

        user = await user_interactor.create_user(
            CreateUserDTO(**user_in_data_unique),
            UrlPathDTO(domain="http://test"),
        )
        assert user.email == user_in_data_unique.get("email")
        assert user.username == user_in_data_unique.get("username")
        assert len(outbox) == 1

    async def test_create_user_failed_email_not_unique(
        self,
        user_in_data_unique: dict,
        mocker: MockFixture,
        create_mock_user,
        create_mock_token,
        outbox,
        user_interactor,
    ):
        user_fixture = create_mock_user(
            fake.unique.random_int(), **user_in_data_unique
        )
        token_fixture = create_mock_token(
            fake.unique.random_int(),
            str(uuid.uuid4()),
            datetime.datetime.now(),
        )
        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_email"  # noqa
        ).return_value = user_fixture
        mocker.patch(
            "src.infrastructure.database.repositories.user.token."
            "TokenRepository.create"
        ).return_value = token_fixture
        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_username"  # noqa
        ).return_value = None

        with pytest.raises(UserExists):
            await user_interactor.create_user(
                CreateUserDTO(**user_in_data_unique),
                UrlPathDTO(domain="http://test/"),
            )
        assert len(outbox) == 0

    async def test_create_user_failed_username_not_unique(
        self,
        user_in_data_unique: dict,
        mocker: MockFixture,
        create_mock_user,
        outbox,
        user_interactor,
    ):
        user_fixture = create_mock_user(
            fake.unique.random_int(), **user_in_data_unique
        )
        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_email"  # noqa
        ).return_value = None
        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_username"  # noqa
        ).return_value = user_fixture

        with pytest.raises(UserExists):
            await user_interactor.create_user(
                CreateUserDTO(**user_in_data_unique),
                UrlPathDTO(domain="http://test"),
            )
        assert len(outbox) == 0


class TestAuthenticate:
    async def test_authenticate_ok(
        self,
        user_in_data_unique: dict,
        create_user,
        user_interactor,
        mocker: MockFixture,
    ):
        user = await create_user(**user_in_data_unique)
        dto = AuthDTO(
            password=user_in_data_unique.get("password"), email=user.email
        )

        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_email"  # noqa
        ).return_value = user

        mocker.patch(
            "src.infrastructure.secure.services.PasslibPasswordService."
            "check_password"  # noqa
        ).return_value = True

        res = await user_interactor.auth_user(dto=dto)
        assert res

    async def test_authenticate_user_doesnt_exist(
        self,
        user_in_data_unique: dict,
        create_user,
        mocker: MockFixture,
        user_interactor,
    ):
        user = await create_user(**user_in_data_unique)
        dto = AuthDTO(
            password=user_in_data_unique.get("password"), email=user.email
        )

        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_email"  # noqa
        ).return_value = None

        with pytest.raises(UserDoesNotExist):
            await user_interactor.auth_user(dto=dto)

    async def test_authenticate_password_doesnt_match(
        self,
        user_in_data_unique: dict,
        create_user,
        user_interactor,
        mocker: MockFixture,
    ):
        user = await create_user(**user_in_data_unique)
        dto = AuthDTO(password="RandomPasswordString123", email=user.email)

        mocker.patch(
            "src.infrastructure.database.repositories.user.user."
            "UserRepository.get_user_by_email"  # noqa
        ).return_value = user

        mocker.patch(
            "src.infrastructure.secure.services.PasslibPasswordService."
            "check_password"  # noqa
        ).return_value = False

        with pytest.raises(PasswordDoesNotMatch):
            await user_interactor.auth_user(dto=dto)
