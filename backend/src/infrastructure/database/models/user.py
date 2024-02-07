from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database.models.base import AbstractModel, time_created


class UserORM(AbstractModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(35), unique=True)
    age: Mapped[str] = mapped_column(String(3), nullable=True)
    email: Mapped[str] = mapped_column(String(155), unique=True)

    surname: Mapped[str] = mapped_column(String(100))
    firstname: Mapped[str] = mapped_column(String(100))
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    about: Mapped[str] = mapped_column(nullable=True)
    file_path: Mapped[str] = mapped_column(nullable=True)

    hashed_password: Mapped[str] = mapped_column(String(125))
    is_active: Mapped[bool] = mapped_column(default=False)

    time_created: Mapped[time_created]

    def __repr__(self) -> str:
        return self.username
