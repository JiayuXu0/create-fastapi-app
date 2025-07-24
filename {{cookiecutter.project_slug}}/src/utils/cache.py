import json
from collections.abc import Callable
from functools import wraps
from typing import Any

import redis.asyncio as redis

from log import logger
from settings.config import settings


class CacheManager:
    """Redis缓存管理器"""

    def __init__(self):
        self.redis: redis.Redis | None = None
        self._connection_pool = None

    async def connect(self):
        """连接Redis"""
        if self.redis is None:
            try:
                self.redis = redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                    max_connections=20,
                    retry_on_timeout=True,
                )
                # 测试连接
                await self.redis.ping()
                logger.info("Redis连接成功")
            except Exception as e:
                logger.warning(f"Redis连接失败: {str(e)}，缓存功能将被禁用")
                self.redis = None

    async def disconnect(self):
        """断开Redis连接"""
        if self.redis:
            await self.redis.close()
            self.redis = None
            logger.info("Redis连接已断开")

    async def get(self, key: str) -> Any | None:
        """获取缓存值"""
        if not self.redis:
            return None

        try:
            data = await self.redis.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"获取缓存失败 key={key}: {str(e)}")
            return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        """设置缓存值"""
        if not self.redis:
            return False

        try:
            ttl = ttl or settings.CACHE_TTL
            serialized_value = json.dumps(value, ensure_ascii=False, default=str)
            await self.redis.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error(f"设置缓存失败 key={key}: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.redis:
            return False

        try:
            result = await self.redis.delete(key)
            return bool(result)
        except Exception as e:
            logger.error(f"删除缓存失败 key={key}: {str(e)}")
            return False

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self.redis:
            return False

        try:
            result = await self.redis.exists(key)
            return bool(result)
        except Exception as e:
            logger.error(f"检查缓存存在性失败 key={key}: {str(e)}")
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """根据模式清除缓存"""
        if not self.redis:
            return 0

        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"批量删除缓存失败 pattern={pattern}: {str(e)}")
            return 0

    def cache_key(self, prefix: str, *args, **kwargs) -> str:
        """生成缓存键"""
        key_parts = [prefix]

        # 添加位置参数
        if args:
            key_parts.extend(str(arg) for arg in args)

        # 添加关键字参数
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            key_parts.extend(f"{k}:{v}" for k, v in sorted_kwargs)

        return ":".join(key_parts)


# 全局缓存管理器实例
cache_manager = CacheManager()


def cached(prefix: str, ttl: int | None = None, key_func: Callable | None = None):
    """缓存装饰器

    Args:
        prefix: 缓存键前缀
        ttl: 过期时间（秒）
        key_func: 自定义键生成函数
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = cache_manager.cache_key(prefix, *args, **kwargs)

            # 尝试从缓存获取
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"缓存命中: {cache_key}")
                return cached_result

            # 执行原函数
            result = await func(*args, **kwargs)

            # 设置缓存
            if result is not None:
                await cache_manager.set(cache_key, result, ttl)
                logger.debug(f"缓存设置: {cache_key}")

            return result

        return wrapper

    return decorator


# 缓存清理工具函数
async def clear_user_cache(user_id: int):
    """清除用户相关缓存"""
    patterns = [
        f"user:{user_id}:*",
        f"userinfo:{user_id}",
        f"user_roles:{user_id}",
        f"user_permissions:{user_id}",
    ]

    total_cleared = 0
    for pattern in patterns:
        cleared = await cache_manager.clear_pattern(pattern)
        total_cleared += cleared

    logger.info(f"清除用户{user_id}相关缓存，共{total_cleared}个键")
    return total_cleared


async def clear_role_cache(role_id: int):
    """清除角色相关缓存"""
    patterns = [
        f"role:{role_id}:*",
        f"role_permissions:{role_id}",
        f"role_menus:{role_id}",
    ]

    total_cleared = 0
    for pattern in patterns:
        cleared = await cache_manager.clear_pattern(pattern)
        total_cleared += cleared

    logger.info(f"清除角色{role_id}相关缓存，共{total_cleared}个键")
    return total_cleared
