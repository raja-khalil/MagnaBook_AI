import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.ai import APIKey, AILog
    from app.models.export import Export
    from app.models.version import VersionHistory


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    projects: Mapped[list["Project"]] = relationship(back_populates="owner", lazy="select")
    permissions: Mapped[list["Permission"]] = relationship(back_populates="user", lazy="select")
    api_keys: Mapped[list["APIKey"]] = relationship(back_populates="user", lazy="select")
    ai_logs: Mapped[list["AILog"]] = relationship(back_populates="user", lazy="select")
    exports: Mapped[list["Export"]] = relationship(back_populates="user", lazy="select")
    version_history: Mapped[list["VersionHistory"]] = relationship(back_populates="user", lazy="select")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"


class Permission(BaseModel):
    __tablename__ = "permissions"
    __table_args__ = (UniqueConstraint("user_id", "project_id", name="uq_permission_user_project"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(
        Enum("owner", "editor", "viewer", name="permission_role"), nullable=False, default="viewer"
    )

    user: Mapped["User"] = relationship(back_populates="permissions")
    project: Mapped["Project"] = relationship(back_populates="permissions")

    def __repr__(self) -> str:
        return f"<Permission user={self.user_id} project={self.project_id} role={self.role}>"
