#!/usr/bin/env python3
"""
Post-generation hook for FastAPI Template Cookiecutter.
Performs cleanup and setup tasks after project generation.
"""

import os
import shutil
import subprocess
from pathlib import Path

# Get variables from cookiecutter context
include_docs = "{{ cookiecutter.include_docs }}" == "yes"
use_redis = "{{ cookiecutter.use_redis }}" == "yes"
database_type = "{{ cookiecutter.database_type }}"
include_docker = "{{ cookiecutter.include_docker }}" == "yes"
use_pre_commit = "{{ cookiecutter.use_pre_commit }}" == "yes"

def remove_docs_if_not_needed():
    """Remove documentation files if not needed."""
    if not include_docs:
        docs_dirs = ["docs", "site"]
        files_to_remove = ["mkdocs.yml", "deploy-docs.sh"]
        
        for doc_dir in docs_dirs:
            if os.path.exists(doc_dir):
                shutil.rmtree(doc_dir)
                print(f"🗑️  Removed {doc_dir}/ directory")
        
        for file_name in files_to_remove:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"🗑️  Removed {file_name}")

def setup_database_config():
    """Setup database configuration based on choice."""
    if database_type == "sqlite":
        print("🗄️  Configured for SQLite database")
    else:
        print("🐘 Configured for PostgreSQL database")

def create_env_example():
    """Create .env.example file with appropriate settings."""
    if database_type == "postgresql":
        db_config = """# 数据库配置
DB_ENGINE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_NAME={{ cookiecutter.project_slug.replace('-', '_') }}_db"""
    else:  # sqlite
        db_config = """# 数据库配置
DB_ENGINE=sqlite
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME={{ cookiecutter.project_slug.replace('-', '_') }}_db"""
    
    env_content = f"""# 应用配置
APP_ENV=development
DEBUG=True
APP_TITLE="{{ cookiecutter.project_name }}"
PROJECT_NAME="{{ cookiecutter.project_name }}"
APP_DESCRIPTION="{{ cookiecutter.project_description }}"

# 安全配置
SECRET_KEY=your-secret-key-here-minimum-32-chars
SWAGGER_UI_USERNAME=admin
SWAGGER_UI_PASSWORD=your-swagger-password

{db_config}

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# JWT配置
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=240
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
"""

    if use_redis:
        env_content += """
# Redis配置
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=300
"""

    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)
    print("📝 Created .env.example file")

def remove_docker_if_not_needed():
    """Remove Docker files if not needed."""
    if not include_docker:
        docker_files = ["Dockerfile", "docker-compose.yml", ".dockerignore"]
        for file_name in docker_files:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"🗑️  Removed {file_name}")

def remove_pre_commit_if_not_needed():
    """Remove pre-commit configuration if not needed."""
    if not use_pre_commit:
        if os.path.exists(".pre-commit-config.yaml"):
            os.remove(".pre-commit-config.yaml")
            print("🗑️  Removed .pre-commit-config.yaml")

def remove_migrations_directory():
    """Remove migrations directory to ensure clean start."""
    migrations_dir = "migrations"
    if os.path.exists(migrations_dir):
        shutil.rmtree(migrations_dir)
        print("🗑️  Removed migrations/ directory for clean start")

def set_file_permissions():
    """Set appropriate file permissions."""
    executable_files = [
        "deploy-docs.sh",
    ]
    
    for file_path in executable_files:
        if os.path.exists(file_path):
            os.chmod(file_path, 0o755)
            print(f"🔧 Set executable permissions for {file_path}")

def print_success_message():
    """Print success message with next steps."""
    print("\n" + "="*60)
    print("🎉 FastAPI项目创建成功！")
    print("="*60)
    print("\n📋 接下来的步骤:")
    print("1. cd {{ cookiecutter.project_slug }}")
    print("2. 复制 .env.example 到 .env 并配置环境变量")
    print("3. 安装依赖: uv sync --dev")
    print("4. 初始化数据库: uv run aerich init-db")
    print("5. 启动开发服务器: uv run uvicorn src:app --reload")
    print("\n📖 更多信息请查看 README.md")
    print("\n💝 感谢使用 FastAPI-Template!")
    print("🌟 如果有帮助，请给原项目点个Star: https://github.com/JiayuXu0/FastAPI-Template")
    print("="*60)

if __name__ == "__main__":
    print("🔧 Setting up your FastAPI project...")
    
    remove_docs_if_not_needed()
    remove_docker_if_not_needed()
    remove_pre_commit_if_not_needed()
    remove_migrations_directory()
    setup_database_config()
    create_env_example()
    set_file_permissions()
    
    print_success_message()