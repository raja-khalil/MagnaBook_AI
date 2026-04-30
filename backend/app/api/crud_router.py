from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.crud import CRUDService


def create_crud_router(
    *,
    prefix: str,
    tags: list[str],
    service: CRUDService[Any, Any, Any],
    create_schema: type[BaseModel],
    update_schema: type[BaseModel],
    read_schema: type[BaseModel],
    not_found_message: str,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    async def get_item_or_404(item_id: UUID, db: AsyncSession) -> Any:
        item = await service.get(db, item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found_message)
        return item

    @router.get("", response_model=list[read_schema])
    async def list_items(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
    ) -> list[Any]:
        return await service.list(db, skip=skip, limit=limit)

    @router.post("", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    async def create_item(
        payload: create_schema,
        db: AsyncSession = Depends(get_db),
    ) -> Any:
        return await service.create(db, payload)

    @router.get("/{item_id}", response_model=read_schema)
    async def get_item(
        item_id: UUID,
        db: AsyncSession = Depends(get_db),
    ) -> Any:
        return await get_item_or_404(item_id, db)

    @router.put("/{item_id}", response_model=read_schema)
    async def update_item(
        item_id: UUID,
        payload: update_schema,
        db: AsyncSession = Depends(get_db),
    ) -> Any:
        item = await get_item_or_404(item_id, db)
        return await service.update(db, item, payload)

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_item(
        item_id: UUID,
        db: AsyncSession = Depends(get_db),
    ) -> Response:
        item = await get_item_or_404(item_id, db)
        await service.delete(db, item)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
