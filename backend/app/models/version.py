import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class VersionHistory(BaseModel):
    __tablename__ = "version_history"

    entity_type: Mapped[str] = mapped_column(
        Enum(
            "project", "file", "briefing", "prd_version", "book_version",
            "export", "template", "user",
            name="version_entity_type",
        ),
        nullable=False,
        index=True,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(
        Enum("create", "update", "delete", name="version_action"), nullable=False
    )
    diff: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User | None"] = relationship(back_populates="version_history")

    def __repr__(self) -> str:
        return f"<VersionHistory entity={self.entity_type}:{self.entity_id} action={self.action}>"
