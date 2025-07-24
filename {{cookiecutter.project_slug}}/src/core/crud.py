from typing import Any, Generic, NewType, TypeVar

from pydantic import BaseModel
from tortoise.expressions import Q
from tortoise.models import Model

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(self, id: int) -> ModelType:
        return await self.model.get(id=id)

    async def list(
        self, page: int, page_size: int, search: Q = Q(), order: list | None = None
    ) -> tuple[Total, list[ModelType]]:
        query = self.model.filter(search)
        if order is None:
            order = []
        return await query.count(), await query.offset((page - 1) * page_size).limit(
            page_size
        ).order_by(*order)

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        if isinstance(obj_in, dict):
            obj_dict = obj_in
        else:
            obj_dict = obj_in.model_dump()
        obj = self.model(**obj_dict)
        await obj.save()
        return obj

    async def update(
        self, id: int, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            obj_dict = obj_in
        else:
            obj_dict = obj_in.model_dump(exclude_unset=True, exclude={"id"})
        obj = await self.get(id=id)
        obj = obj.update_from_dict(obj_dict)
        await obj.save()
        return obj

    async def remove(self, id: int) -> None:
        obj = await self.get(id=id)
        await obj.delete()
