import json

from httpx import AsyncClient
from starlette import status

from src.presentation.api.controllers.v1.responses.exceptions.user import UserExistsResponse


class TestCreateUser:
    async def test_create_user_ok(
            self,
            api_client: AsyncClient,
            user_in_data_unique: dict
    ):
        response = await api_client.post('/user/create/', json=user_in_data_unique)
        resp_data = json.loads(response.text)

        assert resp_data.get('username') == user_in_data_unique.get('username')
        assert resp_data.get('email') == user_in_data_unique.get('email')
        assert resp_data.get('firstname') == user_in_data_unique.get('firstname')
        assert resp_data.get('lastname') == user_in_data_unique.get('lastname')
        assert response.status_code == status.HTTP_201_CREATED

    async def test_create_user_failed_not_unique(
            self,
            api_client: AsyncClient,
            user_in_data_common: dict,
            create_user
    ):
        await create_user(**user_in_data_common)

        response = await api_client.post('/user/create/', json=user_in_data_common)
        resp_data = json.loads(response.text)

        assert resp_data == UserExistsResponse().model_dump()
        assert response.status_code == status.HTTP_409_CONFLICT
