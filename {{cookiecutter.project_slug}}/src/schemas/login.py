from datetime import datetime

from pydantic import BaseModel, Field


class CredentialsSchema(BaseModel):
    username: str = Field(..., description="用户名称", example="admin")
    password: str = Field(..., description="密码", example="请输入正确的测试密码")


class JWTOut(BaseModel):
    access_token: str
    refresh_token: str
    username: str
    token_type: str = "bearer"
    expires_in: int  # 过期时间（秒）


class JWTPayload(BaseModel):
    user_id: int
    username: str
    is_superuser: bool
    exp: datetime
    token_type: str = "access"  # access 或 refresh


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="刷新令牌")


class TokenRefreshOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # 新access_token过期时间（秒）
