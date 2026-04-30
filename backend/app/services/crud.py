from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class CRUDService(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    def base_query(self) -> Select[tuple[ModelT]]:
        return select(self.model).order_by(self.model.created_at.desc())

    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ModelT]:
        result = await db.execute(self.base_query().offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get(self, db: AsyncSession, item_id: UUID) -> ModelT | None:
        return await db.get(self.model, item_id)

    async def create(self, db: AsyncSession, payload: CreateSchemaT) -> ModelT:
        item = self.model(**payload.model_dump())
        db.add(item)
        await db.flush()
        await db.refresh(item)
        return item

    async def update(self, db: AsyncSession, item: ModelT, payload: UpdateSchemaT) -> ModelT:
        update_data: dict[str, Any] = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        await db.flush()
        await db.refresh(item)
        return item

    async def delete(self, db: AsyncSession, item: ModelT) -> None:
        await db.delete(item)
        await db.flush()
