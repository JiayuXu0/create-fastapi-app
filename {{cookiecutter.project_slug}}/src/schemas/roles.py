from datetime import datetime

from pydantic import BaseModel, Field


class BaseRole(BaseModel):
    id: int
    name: str
    desc: str = ""
    users: list | None = []
    menus: list | None = []
    apis: list | None = []
    created_at: datetime | None
    updated_at: datetime | None


class RoleCreate(BaseModel):
    name: str = Field(example="管理员")
    desc: str = Field("", example="管理员角色")


class RoleUpdate(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="管理员")
    desc: str = Field("", example="管理员角色")


class RoleUpdateMenusApis(BaseModel):
    id: int
    menu_ids: list[int] = []
    api_infos: list[dict] = []
