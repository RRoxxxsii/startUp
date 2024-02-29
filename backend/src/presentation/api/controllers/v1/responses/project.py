from enum import Enum

from pydantic import BaseModel, ConfigDict
from src.presentation.api.controllers.v1.responses.user import UserOutSchema


class CategoryOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str


class ProjectOutSchema(BaseModel):
    id: int
    status: Enum
    title: str
    category: CategoryOutSchema
    user: UserOutSchema
    description: str | None = None
