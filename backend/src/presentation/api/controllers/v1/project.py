from fastapi import APIRouter, Depends
from src.domain.app.dto.project import CreateProjectDTO
from src.domain.app.exceptions.project import ProjectExists
from src.domain.app.usecases.project.usecases import ProjectInteractor
from src.infrastructure.database.models import UserORM
from src.presentation.api.controllers.v1.requests.project import \
    CreateProjectSchema
from src.presentation.api.controllers.v1.responses.exceptions.project import \
    ProjectExistsResponse
from src.presentation.api.controllers.v1.responses.project import \
    ProjectOutSchema
from src.presentation.api.dependencies.user import get_current_user_or_401
from src.presentation.api.di.services import get_project_services
from starlette import status
from starlette.responses import Response

router = APIRouter(prefix="/project", tags=["user"])


@router.post(
    "/{category_id}/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectOutSchema | ProjectExistsResponse
)
async def create_project(
        category_id: int,
        project_schema: CreateProjectSchema,
        response: Response,
        user_id: int = Depends(get_current_user_or_401),
        service: ProjectInteractor = Depends(get_project_services)
):
    try:
        project, user, category = await service.create_project(
            CreateProjectDTO(user_id=user_id, category_id=category_id, **project_schema.model_dump())
        )
    except ProjectExists:
        response.status_code = status.HTTP_409_CONFLICT
        return ProjectExistsResponse()
    else:
        return ProjectOutSchema(
            id=project.id,
            status=project.status,
            title=project.title,
            description=project.description,
            category=category,
            user=user
        )


def update_project_with_resources():
    raise NotImplementedError


def add_users_to_project():
    raise NotImplementedError


def update_project_description():
    raise NotImplementedError

