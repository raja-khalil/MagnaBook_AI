from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TimestampedSchema


class PRDBase(BaseModel):
    project_id: UUID
    briefing_id: UUID | None = None
    content: str = Field(min_length=1)
    version: int = Field(default=1, ge=1)
    notes: str | None = None


class PRDCreate(PRDBase):
    pass


class PRDUpdate(BaseModel):
    briefing_id: UUID | None = None
    content: str | None = Field(default=None, min_length=1)
    version: int | None = Field(default=None, ge=1)
    notes: str | None = None


class PRDRead(TimestampedSchema, PRDBase):
    pass
