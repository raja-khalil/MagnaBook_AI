from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema

ExportFormat = Literal["pdf", "epub", "docx", "txt", "html"]
ExportStatus = Literal["pending", "processing", "ready", "error"]


class ExportBase(BaseModel):
    book_version_id: UUID
    user_id: UUID | None = None
    format: ExportFormat
    storage_path: str | None = Field(default=None, max_length=1000)
    status: ExportStatus = "pending"
    error_message: str | None = None


class ExportCreate(ExportBase):
    pass


class ExportUpdate(BaseModel):
    format: ExportFormat | None = None
    storage_path: str | None = Field(default=None, max_length=1000)
    status: ExportStatus | None = None
    error_message: str | None = None


class ExportRead(TimestampedSchema, ExportBase):
    pass
