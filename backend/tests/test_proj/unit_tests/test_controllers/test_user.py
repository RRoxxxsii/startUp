import json

from httpx import AsyncClient
from pytest_mock import MockFixture
from src.domain.app.exceptions.user import UserExists
from src.presentation.api.controllers.v1.responses.exceptions.user import (
    UserExistsResponse,
)
from starlette import status
from tests.conftest import fake


class TestCreateUser:
    async def test_create_user_ok(
        self,
        api_client: AsyncClient,
        user_in_data_unique: dict,
        mocker: MockFixture,
        create_mock_user,
    ):
        user = create_mock_user(
            fake.unique.random_int(), **user_in_data_unique
        )

        mocker.patch(
            "src.domain.app.usecases.user.usecases.UserInteractor.create_user",
            return_value=user,
        )  # Mock Fake response
        response = await api_client.post(
            "/user/create/", json=user_in_data_unique
        )

        assert response.status_code == status.HTTP_201_CREATED

    async def test_create_user_failed_not_unique(
        self,
        api_client: AsyncClient,
        user_in_data_common: dict,
        mocker: MockFixture,
    ):
        mocker.patch(
            "src.domain.app.usecases.user.usecases.CreateUser.execute",
            side_effect=UserExists,
        )  # Mock Exception raise for unique constraint violated

        response = await api_client.post(
            "/user/create/", json=user_in_data_common
        )
        resp_data = json.loads(response.text)

        assert resp_data == UserExistsResponse().model_dump()
        assert response.status_code == status.HTTP_409_CONFLICT
