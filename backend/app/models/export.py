import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.content import BookVersion


class Export(BaseModel):
    __tablename__ = "exports"

    book_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("book_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    format: Mapped[str] = mapped_column(
        Enum("pdf", "epub", "docx", "txt", "html", name="export_format"), nullable=False
    )
    storage_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("pending", "processing", "ready", "error", name="export_status"),
        nullable=False,
        default="pending",
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    book_version: Mapped["BookVersion"] = relationship(back_populates="exports")
    user: Mapped["User | None"] = relationship(back_populates="exports")

    def __repr__(self) -> str:
        return f"<Export id={self.id} format={self.format} status={self.status}>"


class Derivative(BaseModel):
    __tablename__ = "derivatives"

    book_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("book_versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[str] = mapped_column(
        Enum("summary", "index", "synopsis", "back_cover", "press_release", name="derivative_type"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    book_version: Mapped["BookVersion"] = relationship(back_populates="derivatives")

    def __repr__(self) -> str:
        return f"<Derivative id={self.id} type={self.type}>"
