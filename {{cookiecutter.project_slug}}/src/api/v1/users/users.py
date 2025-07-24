from fastapi import APIRouter, Body, Query

from schemas.users import UserCreate, UserUpdate
from services.user_service import user_service

router = APIRouter()


@router.get("/list", summary="查看用户列表")
async def list_user(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    username: str = Query("", description="用户名称，用于搜索"),
    email: str = Query("", description="邮箱地址"),
    dept_id: int = Query(None, description="部门ID"),
):
    return await user_service.get_user_list(
        page=page,
        page_size=page_size,
        username=username,
        email=email,
        dept_id=dept_id,
    )


@router.get("/get", summary="查看用户")
async def get_user(
    user_id: int = Query(..., description="用户ID"),
):
    return await user_service.get_user_detail(user_id)


@router.post("/create", summary="创建用户")
async def create_user(
    user_in: UserCreate,
):
    return await user_service.create_user(user_in)


@router.post("/update", summary="更新用户")
async def update_user(
    user_in: UserUpdate,
):
    return await user_service.update_user(user_in)


@router.delete("/delete", summary="删除用户")
async def delete_user(
    user_id: int = Query(..., description="用户ID"),
):
    return await user_service.delete_user(user_id)


@router.post("/reset_password", summary="重置密码")
async def reset_password(user_id: int = Body(..., description="用户ID", embed=True)):
    return await user_service.reset_user_password(user_id)
