from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema

BookStatus = Literal["draft", "review", "approved", "published"]


class BookBase(BaseModel):
    project_id: UUID
    prd_version_id: UUID | None = None
    title: str = Field(min_length=1, max_length=500)
    content: str = Field(min_length=1)
    version: int = Field(default=1, ge=1)
    status: BookStatus = "draft"


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    prd_version_id: UUID | None = None
    title: str | None = Field(default=None, min_length=1, max_length=500)
    content: str | None = Field(default=None, min_length=1)
    version: int | None = Field(default=None, ge=1)
    status: BookStatus | None = None


class BookRead(TimestampedSchema, BookBase):
    pass
