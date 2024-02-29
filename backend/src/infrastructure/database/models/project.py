import enum
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.database.models import user
from src.infrastructure.database.models.base import (AbstractModel, intpk,
                                                     time_created)


class UserProjectORM(AbstractModel):
    __tablename__ = "users_projects"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)

    is_author: Mapped[bool] = mapped_column(Boolean, default=False)
    datetime_joined: Mapped[time_created]


class EnumStatus(enum.Enum):
    PLANNED = "planned"
    RECRUITMENT_OPENED = "recruitment is opened"
    IN_PROGRESS = "in progress"
    MVP_OPENED = "MVP is opened"
    COMPLETED = "completed"


class CategoryORM(AbstractModel):
    __tablename__ = "categories"

    id: Mapped[intpk]

    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    time_created: Mapped[time_created]

    projects: Mapped[list["ProjectORM"]] = relationship(back_populates="category")


class ResourceORM(AbstractModel):
    __tablename__ = "resources"

    id: Mapped[intpk]

    title: Mapped[str] = mapped_column(String(100))
    link: Mapped[str] = mapped_column(String(150), unique=True)

    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"))
    project: Mapped[Optional["ProjectORM"]] = relationship(back_populates="resources")


class ProjectORM(AbstractModel):
    __tablename__ = "projects"

    id: Mapped[intpk]

    status: Mapped[EnumStatus]
    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None]

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[CategoryORM] = relationship(back_populates="projects")

    resources: Mapped[list["ResourceORM"]] = relationship(back_populates="project")

    users: Mapped[list["user.UserORM"]] = relationship(back_populates="projects", secondary="users_projects")

    time_created: Mapped[time_created]
