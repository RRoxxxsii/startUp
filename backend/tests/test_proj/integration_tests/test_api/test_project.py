import uuid

from httpx import AsyncClient
from starlette import status


class TestCreateProject:

    async def test_create_project_ok(
            self, api_client: AsyncClient, user_in_data_unique, create_user, create_redis_data, redis_pool,
            create_category, category_data, project_in_data_unique
    ):
        user = await create_user(**user_in_data_unique)
        category = await create_category(**category_data)

        access_token = str(uuid.uuid4())
        key = f"user:{user.id}"
        create_redis_data(key=key, value=access_token)   # Create data for redis

        response = await api_client.post(
            f"/project/{category.id}/",
            json=project_in_data_unique,
            headers={"Authorization": access_token}
        )
        assert response.status_code == status.HTTP_201_CREATED

    async def test_create_project_no_authorization_header_failed(
            self, api_client: AsyncClient, user_in_data_unique, create_user, create_redis_data, redis_pool,
            create_category, category_data, project_in_data_unique
    ):
        user = await create_user(**user_in_data_unique)
        category = await create_category(**category_data)

        access_token = str(uuid.uuid4())
        key = f"user:{user.id}"
        create_redis_data(key=key, value=access_token)   # Create data for redis

        response = await api_client.post(
            f"/project/{category.id}/",
            json=project_in_data_unique,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
