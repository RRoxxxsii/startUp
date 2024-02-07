from starlette import status

create_user = {
    status.HTTP_409_CONFLICT: {
        "description": "Unique constraint failed (e.g. password)",
        "content": {
            "application/json": {
                "example": {"detail": "Пользователь с такими данными уже существует"}
            }
        },
    },
}