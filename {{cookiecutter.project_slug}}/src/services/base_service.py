from collections.abc import Callable
from typing import Any, TypeVar

from fastapi import HTTPException
from tortoise.expressions import Q
from tortoise.models import Model

from core.crud import CRUDBase
from log import logger
from models.admin import Role, User
from schemas.base import Fail, Success, SuccessExtra

T = TypeVar("T", bound=Model)


class BaseService:
    """基础服务类 - 统一公共逻辑"""

    def __init__(self, repository: CRUDBase):
        self.repository = repository
        self.logger = logger

    async def get_paginated_list(
        self,
        page: int = 1,
        page_size: int = 10,
        search_filters: Q | None = None,
        order: list[str] | None = None,
        exclude_fields: list[str] | None = None,
        include_m2m: bool = False,
        transform_func: Callable | None = None,
    ) -> SuccessExtra:
        """获取分页列表 - 统一版本

        Args:
            page: 页码
            page_size: 每页数量
            search_filters: 搜索条件
            order: 排序字段
            exclude_fields: 排除字段
            include_m2m: 是否包含多对多关系
            transform_func: 数据转换函数

        Returns:
            SuccessExtra: 分页响应
        """
        try:
            total, items = await self.repository.list(
                page=page,
                page_size=page_size,
                search=search_filters or Q(),
                order=order or ["-created_at"],
            )

            # 转换数据
            if transform_func:
                data = await transform_func(items)
            else:
                data = [
                    await item.to_dict(
                        m2m=include_m2m, exclude_fields=exclude_fields or []
                    )
                    for item in items
                ]

            return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

        except Exception as e:
            self.logger.error(f"获取分页列表失败: {str(e)}")
            return Fail(msg="获取列表失败")

    async def get_by_id(
        self,
        item_id: int,
        exclude_fields: list[str] | None = None,
        include_m2m: bool = False,
        not_found_msg: str = "记录不存在",
    ) -> Success:
        """根据ID获取单个记录

        Args:
            item_id: 记录ID
            exclude_fields: 排除字段
            include_m2m: 是否包含多对多关系
            not_found_msg: 未找到时的错误消息

        Returns:
            Success: 成功响应
        """
        try:
            item = await self.repository.get(item_id)
            if not item:
                raise HTTPException(status_code=404, detail=not_found_msg)

            data = await item.to_dict(
                m2m=include_m2m, exclude_fields=exclude_fields or []
            )
            return Success(data=data)

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"获取记录失败: {str(e)}")
            return Fail(msg="获取记录失败")

    async def create_item(
        self,
        item_data: dict[str, Any],
        success_msg: str = "创建成功",
        exclude_fields: list[str] | None = None,
    ) -> Success:
        """创建记录

        Args:
            item_data: 创建数据
            success_msg: 成功消息
            exclude_fields: 排除字段

        Returns:
            Success: 成功响应
        """
        try:
            item = await self.repository.create(item_data)
            data = await item.to_dict(exclude_fields=exclude_fields or [])
            return Success(data=data, msg=success_msg)

        except Exception as e:
            self.logger.error(f"创建记录失败: {str(e)}")
            return Fail(msg="创建失败")

    async def update_item(
        self,
        item_id: int,
        item_data: dict[str, Any],
        success_msg: str = "更新成功",
        not_found_msg: str = "记录不存在",
        exclude_fields: list[str] | None = None,
    ) -> Success:
        """更新记录

        Args:
            item_id: 记录ID
            item_data: 更新数据
            success_msg: 成功消息
            not_found_msg: 未找到消息
            exclude_fields: 排除字段

        Returns:
            Success: 成功响应
        """
        try:
            item = await self.repository.get(item_id)
            if not item:
                raise HTTPException(status_code=404, detail=not_found_msg)

            updated_item = await self.repository.update(item_id, item_data)
            data = await updated_item.to_dict(exclude_fields=exclude_fields or [])
            return Success(data=data, msg=success_msg)

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"更新记录失败: {str(e)}")
            return Fail(msg="更新失败")

    async def delete_item(
        self,
        item_id: int,
        success_msg: str = "删除成功",
        not_found_msg: str = "记录不存在",
    ) -> Success:
        """删除记录

        Args:
            item_id: 记录ID
            success_msg: 成功消息
            not_found_msg: 未找到消息

        Returns:
            Success: 成功响应
        """
        try:
            item = await self.repository.get(item_id)
            if not item:
                raise HTTPException(status_code=404, detail=not_found_msg)

            await self.repository.remove(item_id)
            return Success(msg=success_msg)

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"删除记录失败: {str(e)}")
            return Fail(msg="删除失败")


class PermissionService:
    """权限服务 - 统一权限检查逻辑"""

    @staticmethod
    async def check_superuser(
        user: User, error_msg: str = "权限不足，需要超级管理员权限"
    ):
        """检查超级管理员权限"""
        if not user.is_superuser:
            return Fail(code=403, msg=error_msg)
        return None

    @staticmethod
    async def get_user_agent_ids(user: User) -> set:
        """获取用户有权限的智能体ID集合"""
        if user.is_superuser:
            return set()  # 超级管理员无限制

        roles: list[Role] = await user.roles.all()
        if not roles:
            return set()

        allowed_agent_ids = set()
        for role in roles:
            role_agents = await role.agents.all()
            allowed_agent_ids.update(agent.id for agent in role_agents)

        return allowed_agent_ids

    @staticmethod
    def build_search_filters(
        keyword: str | None = None,
        search_fields: list[str] | None = None,
        extra_filters: dict[str, Any] | None = None,
    ) -> Q:
        """构建搜索过滤条件"""
        filters = Q()

        # 关键词搜索
        if keyword and search_fields:
            keyword_filters = Q()
            for field in search_fields:
                keyword_filters |= Q(**{f"{field}__icontains": keyword})
            filters &= keyword_filters

        # 额外过滤条件
        if extra_filters:
            for field, value in extra_filters.items():
                if value is not None:
                    if field.endswith("__icontains"):
                        filters &= Q(**{field: value})
                    else:
                        filters &= Q(**{field: value})

        return filters


# 全局实例
permission_service = PermissionService()
