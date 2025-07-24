import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class BaseUser(BaseModel):
    id: int
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    created_at: datetime | None
    updated_at: datetime | None
    last_login: datetime | None
    roles: list | None = []


class UserCreate(BaseModel):
    email: EmailStr = Field(example="admin@qq.com")
    username: str = Field(
        example="admin",
        min_length=3,
        max_length=20,
        pattern="^[a-zA-Z0-9_]+$",
        description="用户名（3-20位字母数字下划线）",
    )
    password: str = Field(
        example="AdminPass123",
        min_length=8,
        description="密码（至少8位，包含字母和数字）",
    )
    is_active: bool | None = True
    is_superuser: bool | None = False
    role_ids: list[int] | None = []
    dept_id: int | None = Field(0, description="部门ID")

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError("密码长度至少8位")

        if not re.search(r"[A-Za-z]", v):
            raise ValueError("密码必须包含字母")

        if not re.search(r"\d", v):
            raise ValueError("密码必须包含数字")

        # 可选：检查特殊字符
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        #     raise ValueError('密码建议包含特殊字符')

        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        """验证用户名格式"""
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("用户名只能包含字母、数字和下划线")
        return v

    def create_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"role_ids"})


class UserUpdate(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool | None = True
    is_superuser: bool | None = False
    role_ids: list[int] | None = []
    dept_id: int | None = 0


class UpdatePassword(BaseModel):
    old_password: str = Field(description="旧密码")
    new_password: str = Field(
        min_length=8, description="新密码（至少8位，包含字母和数字）"
    )

    @field_validator("new_password")
    @classmethod
    def validate_new_password_strength(cls, v):
        """验证新密码强度"""
        if len(v) < 8:
            raise ValueError("新密码长度至少8位")

        if not re.search(r"[A-Za-z]", v):
            raise ValueError("新密码必须包含字母")

        if not re.search(r"\d", v):
            raise ValueError("新密码必须包含数字")

        return v
