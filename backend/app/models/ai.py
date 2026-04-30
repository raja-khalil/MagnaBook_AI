import uuid
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project


class APIProvider(BaseModel):
    __tablename__ = "api_providers"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    base_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    api_keys: Mapped[list["APIKey"]] = relationship(back_populates="provider", lazy="select")
    api_usage: Mapped[list["APIUsage"]] = relationship(back_populates="provider", lazy="select")
    ai_logs: Mapped[list["AILog"]] = relationship(back_populates="provider", lazy="select")

    def __repr__(self) -> str:
        return f"<APIProvider id={self.id} name={self.name}>"


class APIKey(BaseModel):
    __tablename__ = "api_keys"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("api_providers.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    key_hash: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship(back_populates="api_keys")
    provider: Mapped["APIProvider"] = relationship(back_populates="api_keys")
    usage: Mapped[list["APIUsage"]] = relationship(back_populates="api_key", lazy="select")

    def __repr__(self) -> str:
        return f"<APIKey id={self.id} label={self.label}>"


class APIUsage(BaseModel):
    __tablename__ = "api_usage"

    api_key_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("api_keys.id", ondelete="SET NULL"), nullable=True, index=True
    )
    provider_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("api_providers.id", ondelete="SET NULL"), nullable=True
    )
    tokens_input: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    tokens_output: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    cost_usd: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False, default=0)
    endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)

    api_key: Mapped["APIKey | None"] = relationship(back_populates="usage")
    provider: Mapped["APIProvider | None"] = relationship(back_populates="api_usage")

    def __repr__(self) -> str:
        return f"<APIUsage id={self.id} tokens_in={self.tokens_input} tokens_out={self.tokens_output}>"


class AILog(BaseModel):
    __tablename__ = "ai_logs"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True
    )
    provider_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("api_providers.id", ondelete="SET NULL"), nullable=True
    )
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str | None] = mapped_column(Text, nullable=True)
    tokens_input: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    tokens_output: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("success", "error", "timeout", name="ai_log_status"),
        nullable=False,
        default="success",
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User | None"] = relationship(back_populates="ai_logs")
    project: Mapped["Project | None"] = relationship(back_populates="ai_logs")
    provider: Mapped["APIProvider | None"] = relationship(back_populates="ai_logs")

    def __repr__(self) -> str:
        return f"<AILog id={self.id} model={self.model} status={self.status}>"
