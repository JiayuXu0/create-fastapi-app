import re
import secrets
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer

from core.ctx import CTX_USER_ID
from models import Role, User
from settings.config import settings

security = HTTPBasic()
bearer_scheme = HTTPBearer()


def get_current_username(
    credentials: HTTPBasicCredentials = Depends(security),
):
    correct_username = secrets.compare_digest(
        credentials.username, settings.SWAGGER_UI_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.SWAGGER_UI_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Required",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class AuthControl:
    @classmethod
    async def is_authed(cls, token: str = Depends(bearer_scheme)) -> Optional["User"]:
        try:
            # 直接使用 HTTPBearer 提供的 token (已经去掉了 Bearer 前缀)
            if not token:
                raise HTTPException(
                    status_code=401, detail="Missing authentication token"
                )

            decode_data = jwt.decode(
                token.credentials,
                settings.SECRET_KEY,
                algorithms=settings.JWT_ALGORITHM,
            )
            user_id = decode_data.get("user_id")
            user = await User.filter(id=user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail="Authentication failed")
            CTX_USER_ID.set(int(user_id))
            return user
        except jwt.DecodeError as e:
            raise HTTPException(status_code=401, detail="无效的Token") from e
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="登录已过期") from e
        except Exception as e:
            # 记录详细错误信息到日志，但不返回给用户
            raise HTTPException(status_code=401, detail="认证失败") from e


class PermissionControl:
    @classmethod
    async def has_permission(
        cls,
        request: Request,
        current_user: User = Depends(AuthControl.is_authed),
    ) -> None:
        """检查用户是否有访问指定API的权限

        Args:
            request: FastAPI请求对象
            current_user: 当前认证用户

        Raises:
            HTTPException: 当用户无权限时抛出403错误
        """
        if current_user.is_superuser:
            return

        method = request.method
        path = request.url.path
        roles: list[Role] = await current_user.roles.all()

        if not roles:
            raise HTTPException(
                status_code=403, detail="The user is not bound to a role"
            )

        # 获取用户所有角色的API权限
        apis = [await role.apis.all() for role in roles]
        permission_apis = [(api.method, api.path) for api in sum(apis, [])]

        # 检查权限匹配（支持路径参数）
        for perm_method, perm_path in permission_apis:
            if method == perm_method:
                # 将路径参数占位符转换为正则表达式
                # 例如: /api/v1/agent/{agent_id} -> /api/v1/agent/[^/]+
                pattern = re.sub(r"\{[^}]+\}", r"[^/]+", perm_path)
                pattern = f"^{pattern}$"
                if re.match(pattern, path):
                    return

        raise HTTPException(
            status_code=403,
            detail=f"Permission denied method:{method} path:{path}",
        )


class AgentPermissionControl:
    """智能体权限控制类"""

    @classmethod
    async def has_agent_permission(
        cls,
        request: Request,
        current_user: User = Depends(AuthControl.is_authed),
    ) -> User:
        """检查用户是否有访问智能体的权限

        Args:
            request: FastAPI请求对象
            current_user: 当前认证用户

        Returns:
            User: 当前用户对象

        Raises:
            HTTPException: 当用户无权限时抛出403错误
        """
        # 超级管理员拥有所有权限
        if current_user.is_superuser:
            return current_user

        # 从URL路径中提取agent_id
        path_params = request.path_params
        agent_id = path_params.get("agent_id")

        if not agent_id:
            raise HTTPException(status_code=400, detail="缺少智能体ID参数")

        try:
            agent_id = int(agent_id)
        except (ValueError, TypeError) as e:
            raise HTTPException(status_code=400, detail="无效的智能体ID") from e

        # 获取用户角色
        roles: list[Role] = await current_user.roles.all()
        if not roles:
            raise HTTPException(
                status_code=403, detail="用户未绑定角色，无权限访问智能体"
            )

        # 检查用户角色是否有权限访问该智能体
        for role in roles:
            role_agents = await role.agents.all()
            if any(agent.id == agent_id for agent in role_agents):
                return current_user

        raise HTTPException(status_code=403, detail="无权限访问该智能体")

    @classmethod
    async def filter_agents_by_permission(
        cls,
        current_user: User = Depends(AuthControl.is_authed),
    ) -> set[int]:
        """获取用户有权限访问的智能体ID集合

        Args:
            current_user: 当前认证用户

        Returns:
            set[int]: 用户有权限访问的智能体ID集合，超级管理员返回空集合表示无限制
        """
        # 超级管理员拥有所有权限，返回空集合表示无限制
        if current_user.is_superuser:
            return set()

        # 获取用户角色关联的所有智能体ID
        roles: list[Role] = await current_user.roles.all()
        if not roles:
            return set()  # 没有角色，返回空集合

        allowed_agent_ids = set()
        for role in roles:
            role_agents = await role.agents.all()
            allowed_agent_ids.update(agent.id for agent in role_agents)

        return allowed_agent_ids


DependAuth = Depends(AuthControl.is_authed)
DependPermisson = Depends(PermissionControl.has_permission)
DependAgentPermission = Depends(AgentPermissionControl.has_agent_permission)
DependAgentFilter = Depends(AgentPermissionControl.filter_agents_by_permission)
