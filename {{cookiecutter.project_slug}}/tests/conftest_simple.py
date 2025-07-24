"""简化的测试配置，避免复杂依赖"""

import asyncio
import os
import sys
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings():
    """测试环境设置"""
    os.environ["DEBUG"] = "True"
    os.environ["APP_ENV"] = "testing"
    os.environ["DB_ENGINE"] = "sqlite"
    os.environ["SECRET_KEY"] = "test_secret_key_for_testing_only_32_chars_long"
    os.environ["REDIS_URL"] = "redis://localhost:6379/1"  # 测试Redis数据库


@pytest.fixture
def mock_app(test_settings):
    """模拟应用，避免Redis依赖"""
    from unittest.mock import Mock, patch

    # Mock Redis相关模块
    with patch("src.utils.cache.redis") as mock_redis:
        mock_redis.from_url.return_value = Mock()

        # 导入并创建应用
        from src import app

        yield app


@pytest.fixture
def client(mock_app):
    """同步测试客户端"""
    with TestClient(mock_app) as c:
        yield c


@pytest.fixture
async def async_client(mock_app) -> AsyncGenerator[AsyncClient, None]:
    """异步测试客户端"""
    async with AsyncClient(app=mock_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_jwt_token():
    """样例JWT令牌"""
    from utils.jwt import create_token_pair

    access_token, refresh_token = create_token_pair(
        user_id=1, username="test_user", is_superuser=True
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "headers": {"Authorization": f"Bearer {access_token}"},
    }
