import uuid

from httpx import AsyncClient
from starlette import status


class TestGetCurrentUser:

    async def test_authenticate_ok(self, api_client: AsyncClient, user_in_data_unique, create_user, create_redis_data, redis_pool):
        user = await create_user(**user_in_data_unique)
        access_token = str(uuid.uuid4())
        key = f"user:{user.id}"
        create_redis_data(key=key, value=access_token)   # Create data for redis

        response = await api_client.get("/user/debug/", headers={"Authorization": access_token})
        assert response.status_code == status.HTTP_200_OK

    async def test_authenticate_token_not_valid_failed(self, api_client: AsyncClient, user_in_data_unique, create_user, create_redis_data, redis_pool):
        user = await create_user(**user_in_data_unique)
        access_token = str(uuid.uuid4())
        key = f"user:{user.id}"
        create_redis_data(key=key, value=access_token)   # Create data for redis

        response = await api_client.get("/user/debug/", headers={"Authorization": "FakeToken"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_authenticate_token_not_passed_failed(self, api_client: AsyncClient, user_in_data_unique, create_user, create_redis_data, redis_pool):
        response = await api_client.get("/user/debug/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
