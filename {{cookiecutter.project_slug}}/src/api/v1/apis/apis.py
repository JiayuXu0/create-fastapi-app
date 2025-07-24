from fastapi import APIRouter, Query
from tortoise.expressions import Q

from repositories.api import api_repository
from schemas import Success, SuccessExtra
from schemas.apis import *

router = APIRouter()


@router.get("/list", summary="查看API列表")
async def list_api(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    path: str = Query(None, description="API路径"),
    summary: str = Query(None, description="API简介"),
    tags: str = Query(None, description="API模块"),
):
    q = Q()
    if path:
        q &= Q(path__contains=path)
    if summary:
        q &= Q(summary__contains=summary)
    if tags:
        q &= Q(tags__contains=tags)
    total, api_objs = await api_repository.list(
        page=page, page_size=page_size, search=q, order=["tags", "id"]
    )
    data = [await obj.to_dict() for obj in api_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看Api")
async def get_api(
    id: int = Query(..., description="Api"),
):
    api_obj = await api_repository.get(id=id)
    data = await api_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="创建Api")
async def create_api(
    api_in: ApiCreate,
):
    await api_repository.create(obj_in=api_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新Api")
async def update_api(
    api_in: ApiUpdate,
):
    await api_repository.update(id=api_in.id, obj_in=api_in)
    return Success(msg="Update Successfully")


@router.delete("/delete", summary="删除Api")
async def delete_api(
    api_id: int = Query(..., description="ApiID"),
):
    await api_repository.remove(id=api_id)
    return Success(msg="Deleted Success")


@router.post("/refresh", summary="刷新API列表")
async def refresh_api():
    await api_repository.refresh_api()
    return Success(msg="OK")
