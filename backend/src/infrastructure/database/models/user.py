from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    tokens: Mapped[list["TokenORM"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return self.username


class TokenORM(AbstractModel):
    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserORM"] = relationship(back_populates="tokens")

    access_token: Mapped[str] = mapped_column(unique=True, index=True)
    time_created: Mapped[time_created]
