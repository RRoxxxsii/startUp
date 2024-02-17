import json
import re

from httpx import AsyncClient
from src.presentation.api.controllers.v1.responses.exceptions.user import (
    UserExistsResponse,
)
from starlette import status


class TestCreateUser:
    async def test_create_user_ok(
        self, api_client: AsyncClient, user_in_data_unique: dict, outbox
    ):
        response = await api_client.post(
            "/user/create/", json=user_in_data_unique
        )
        resp_data = json.loads(response.text)

        assert resp_data.get("username") == user_in_data_unique.get("username")
        assert resp_data.get("email") == user_in_data_unique.get("email")
        assert resp_data.get("firstname") == user_in_data_unique.get(
            "firstname"
        )
        assert resp_data.get("lastname") == user_in_data_unique.get("lastname")
        assert response.status_code == status.HTTP_201_CREATED
        assert len(outbox) == 1

    async def test_create_user_failed_not_unique(
        self,
        api_client: AsyncClient,
        user_in_data_common: dict,
        create_user,
        outbox,
    ):
        await create_user(**user_in_data_common)

        response = await api_client.post(
            "/user/create/", json=user_in_data_common
        )
        resp_data = json.loads(response.text)

        assert resp_data == UserExistsResponse().model_dump()
        assert response.status_code == status.HTTP_409_CONFLICT
        assert len(outbox) == 0


class TestConfirmEmail:
    async def test_confirm_email_ok(
        self, api_client: AsyncClient, user_in_data_unique: dict, outbox
    ):
        await api_client.post("/user/create/", json=user_in_data_unique)
        url = re.findall(r"https?://\S+", outbox[0].get("message"))
        response = await api_client.get((url[0]).split("test")[1])

        assert response.status_code == status.HTTP_200_OK

    async def test_confirm_email_token_not_valid(
        self, api_client: AsyncClient, user_in_data_unique: dict, outbox
    ):
        await api_client.post("/user/create/", json=user_in_data_unique)
        response = await api_client.get("/user/create/NotValidToken")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAuthenticate:
    async def test_authenticate_ok(
        self, api_client: AsyncClient, user_in_data_unique: dict, create_user
    ):
        user = await create_user(**user_in_data_unique)
        response = await api_client.post(
            "/user/auth/",
            json={
                "password": user_in_data_unique.get("password"),
                "email": user.email,
            },
        )

        assert response.status_code == status.HTTP_200_OK

    async def test_authenticate_user_doesnt_exist(
        self, api_client: AsyncClient, user_in_data_unique: dict, create_user
    ):
        await create_user(**user_in_data_unique)
        response = await api_client.post(
            "/user/auth/",
            json={
                "password": "RandomPasswordString123",
                "email": "fakeemail@example.com",
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_authenticate_password_doesnt_match(
        self, api_client: AsyncClient, user_in_data_unique: dict, create_user
    ):
        user = await create_user(**user_in_data_unique)
        response = await api_client.post(
            "/user/auth/",
            json={"password": "RandomPasswordString123", "email": user.email},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
