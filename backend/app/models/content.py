import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.export import Export, Derivative


class Briefing(BaseModel):
    __tablename__ = "briefings"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped["Project"] = relationship(back_populates="briefings")
    prd_versions: Mapped[list["PRDVersion"]] = relationship(back_populates="briefing", lazy="select")

    def __repr__(self) -> str:
        return f"<Briefing id={self.id} project={self.project_id} v{self.version}>"


class PRDVersion(BaseModel):
    __tablename__ = "prd_versions"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    briefing_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("briefings.id", ondelete="SET NULL"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    briefing: Mapped["Briefing | None"] = relationship(back_populates="prd_versions")
    book_versions: Mapped[list["BookVersion"]] = relationship(back_populates="prd_version", lazy="select")

    def __repr__(self) -> str:
        return f"<PRDVersion id={self.id} project={self.project_id} v{self.version}>"


class BookVersion(BaseModel):
    __tablename__ = "book_versions"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    prd_version_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(
        Enum("draft", "review", "approved", "published", name="book_status"),
        nullable=False,
        default="draft",
    )

    project: Mapped["Project"] = relationship(back_populates="book_versions")
    prd_version: Mapped["PRDVersion | None"] = relationship(back_populates="book_versions")
    exports: Mapped[list["Export"]] = relationship(back_populates="book_version", lazy="select")
    derivatives: Mapped[list["Derivative"]] = relationship(back_populates="book_version", lazy="select")

    def __repr__(self) -> str:
        return f"<BookVersion id={self.id} title={self.title} v{self.version}>"
