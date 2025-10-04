from typing import (
    Any,
    Generic,
    TypeVar,
)
from collections.abc import Sequence

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType], db: AsyncSession) -> None:
        self.model = model
        self.db = db

    async def get(self, id: Any) -> ModelType | None:
        statement = select(self.model).where(self.model.id == id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_multi(
        self, *, page: int = 1, size: int = 10
    ) -> tuple[Sequence[ModelType], int]:
        """
        return (ModelType , number of total record)
        """
        statement = select(self.model)
        statement = statement.offset((page - 1) * size).limit(size)
        result = await self.db.execute(statement)

        count_statement = select(func.count(self.model.id))
        total_count_result = await self.db.execute(count_statement)
        total_count = total_count_result.scalar()
        if total_count is None:
            total_count = 0
        return (result.scalars().all(), total_count)

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        return db_obj

    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """Update a record."""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.db.add(db_obj)
        return db_obj

    async def remove(self, *, id: int) -> ModelType | None:
        """Delete a record by id."""
        obj = await self.get(id=id)
        if obj:
            await self.db.delete(obj)
        return obj
