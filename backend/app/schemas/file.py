from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema

FileStatus = Literal["pending", "processing", "ready", "error"]


class FileBase(BaseModel):
    project_id: UUID
    owner_id: UUID | None = None
    filename: str = Field(min_length=1, max_length=500)
    original_name: str = Field(min_length=1, max_length=500)
    storage_path: str = Field(min_length=1, max_length=1000)
    mime_type: str = Field(min_length=1, max_length=127)
    file_size: int = Field(ge=0)
    status: FileStatus = "pending"


class FileCreate(FileBase):
    pass


class FileUpdate(BaseModel):
    filename: str | None = Field(default=None, min_length=1, max_length=500)
    original_name: str | None = Field(default=None, min_length=1, max_length=500)
    storage_path: str | None = Field(default=None, min_length=1, max_length=1000)
    mime_type: str | None = Field(default=None, min_length=1, max_length=127)
    file_size: int | None = Field(default=None, ge=0)
    status: FileStatus | None = None


class FileRead(TimestampedSchema, FileBase):
    pass
