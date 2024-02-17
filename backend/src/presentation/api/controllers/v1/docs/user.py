from starlette import status

create_user = {
    status.HTTP_409_CONFLICT: {
        "description": "Unique constraint failed (e.g. password)",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Пользователь с такими данными уже существует"
                }
            }
        },
    },
}


confirm_email = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Token was not recognized. Email is not confirmed",
        "content": {
            "application/json": {"example": {"detail": "Страница не найдена"}}
        },
    },
    status.HTTP_200_OK: {
        "description": "Token recognized. Email is supposed to be confirmed",
        "content": {
            "application/json": {
                "example": {"detail": "Почтовый адрес успешно подтвержден"}
            }
        },
    },
}


authenticate = {
    status.HTTP_404_NOT_FOUND: {
        "description": "User with the email was not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Пользователь с данной почтой не существует"
                }
            }
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Password does not match the email",
        "content": {
            "application/json": {"example": {"detail": "Пароль некорректен"}}
        },
    },
    status.HTTP_200_OK: {
        "description": "Bearer токен",
        "content": {
            "application/json": {
                "example": {"detail": "c6ba9c87-f850-4304-bfc4-029db2b4f5f4"}
            }
        },
    },
}
