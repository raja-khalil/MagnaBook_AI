from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema

ProjectStatus = Literal["draft", "active", "archived"]


class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatus = "draft"


class ProjectCreate(ProjectBase):
    owner_id: UUID


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatus | None = None


class ProjectRead(TimestampedSchema, ProjectBase):
    owner_id: UUID
