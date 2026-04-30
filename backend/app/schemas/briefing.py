from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class BriefingBase(BaseModel):
    project_id: UUID
    content: str = Field(min_length=1)
    version: int = Field(default=1, ge=1)
    notes: str | None = None


class BriefingCreate(BriefingBase):
    pass


class BriefingUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1)
    version: int | None = Field(default=None, ge=1)
    notes: str | None = None


class BriefingRead(TimestampedSchema, BriefingBase):
    pass
