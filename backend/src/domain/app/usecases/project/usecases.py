from src.domain.app.dto.project import CreateProjectDTO
from src.domain.app.exceptions.project import ProjectExists
from src.domain.app.usecases.project.base import BaseProjectUseCase
from src.infrastructure.database.models import UserORM
from src.infrastructure.database.models.project import (CategoryORM, EnumStatus, ProjectORM)
from src.infrastructure.database.uow import AbstractUnitOfWork


class CreateProjectUseCase(BaseProjectUseCase):

    async def execute(
            self, dto: CreateProjectDTO
    ) -> tuple[ProjectORM | None, UserORM | None, CategoryORM | None]:
        if await self.uow.project_repo.get_project_by_title(dto.title):
            await self.uow.rollback()
            raise ProjectExists("Project with this title already exists")

        category: CategoryORM = await self.uow.category_repo.get_by_id(dto.category_id)

        dto_dict = dto.dict()
        user_id = dto_dict.pop("user_id")
        project: ProjectORM = await self.uow.project_repo.create(status=EnumStatus.PLANNED, **dto_dict)
        user: UserORM = await self.uow.user_repo.get_by_id(user_id)
        user.projects.append(project)
        await self.uow.commit()
        return project, user, category


class ProjectInteractor:

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def create_project(
            self, dto: CreateProjectDTO
    ) -> tuple[ProjectORM | None, UserORM | None, CategoryORM | None]:
        return await CreateProjectUseCase(self.uow).execute(dto)
