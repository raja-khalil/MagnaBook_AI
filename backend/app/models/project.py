import uuid
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User, Permission
    from app.models.content import Briefing, BookVersion
    from app.models.ai import AILog


class Project(BaseModel):
    __tablename__ = "projects"

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("draft", "active", "archived", name="project_status"),
        nullable=False,
        default="draft",
    )

    # Relationships
    owner: Mapped["User"] = relationship(back_populates="projects")
    permissions: Mapped[list["Permission"]] = relationship(back_populates="project", lazy="select")
    files: Mapped[list["File"]] = relationship(back_populates="project", lazy="select")
    briefings: Mapped[list["Briefing"]] = relationship(back_populates="project", lazy="select")
    book_versions: Mapped[list["BookVersion"]] = relationship(back_populates="project", lazy="select")
    ai_logs: Mapped[list["AILog"]] = relationship(back_populates="project", lazy="select")

    def __repr__(self) -> str:
        return f"<Project id={self.id} name={self.name}>"


class File(BaseModel):
    __tablename__ = "files"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    original_name: Mapped[str] = mapped_column(String(500), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(127), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("pending", "processing", "ready", "error", name="file_status"),
        nullable=False,
        default="pending",
    )

    project: Mapped["Project"] = relationship(back_populates="files")

    def __repr__(self) -> str:
        return f"<File id={self.id} name={self.original_name}>"
