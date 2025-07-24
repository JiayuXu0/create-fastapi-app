# 🚀 {{cookiecutter.project_name}}

<div align="center">

**{{cookiecutter.project_description}}**

> **🎉 基于 [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template) 创建**
> 
> 💝 **感谢原作者**: [@JiayuXu0](https://github.com/JiayuXu0) 提供的优秀企业级FastAPI模板
> 
> 🌟 **如果这个模板对你有帮助，请给原项目点个 Star**: [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template)

---

**简体中文** | [English](README.en.md)

[![Python](https://img.shields.io/badge/Python-{{cookiecutter.python_version}}+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-{{cookiecutter.license}}-yellow.svg)](https://opensource.org/licenses/{{cookiecutter.license}})

[![UV](https://img.shields.io/badge/📦_依赖管理-UV-blueviolet.svg)](https://github.com/astral-sh/uv)
[![Architecture](https://img.shields.io/badge/🏗️_架构-三层架构-orange.svg)](#)
[![RBAC](https://img.shields.io/badge/🔐_权限-RBAC-red.svg)](#)
[![Docker](https://img.shields.io/badge/🐳_容器-Docker-blue.svg)](https://www.docker.com/)

[📖 快速开始](#-快速开始) • [🏗️ 架构说明](#-架构说明) • [📚 开发指南](CLAUDE.md) • [🤝 贡献指南](CONTRIBUTING.md)

</div>

---

## ✨ 基于模板的核心特性

本项目基于 [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template) 构建，具备以下企业级特性：

- 🏗️ **清晰的三层架构** - API/Service/Repository 分层设计
- 🔐 **完整的RBAC权限管理** - 角色、菜单、API权限控制
- 👤 **用户认证与JWT管理** - 安全的身份验证系统
- 📝 **审计日志与监控** - 全面的操作追踪
- 🚀 **Redis缓存优化** - 高性能缓存策略
- 📁 **安全文件管理** - 文件上传下载与验证
- 🐳 **Docker容器化** - 开箱即用的部署方案
- 📖 **自动API文档** - Swagger/ReDoc 文档生成
- 🔧 **代码质量保证** - Pre-commit hooks + Ruff
- 📊 **MkDocs文档站** - 完整的项目文档

---

## 🚀 快速开始

### 📋 环境要求

- Python {{cookiecutter.python_version}}+
- UV (推荐) 或 pip
{%- if cookiecutter.database_type == "postgresql" %}
- PostgreSQL 12+
{%- endif %}
{%- if cookiecutter.use_redis == "yes" %}
- Redis 6+
{%- endif %}

### 🛠️ 安装部署

1. **安装依赖**
   ```bash
   # 安装 UV (推荐)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # 安装项目依赖
   uv sync --dev
   ```

2. **环境配置**
   ```bash
   # 复制环境配置文件
   cp .env.example .env
   
   # 编辑配置文件
   nano .env
   ```

3. **数据库初始化**
   ```bash
   # 初始化数据库
   uv run aerich init-db
   
   # 应用迁移
   uv run aerich upgrade
   ```

4. **启动服务**
   ```bash
   # 开发环境启动
   uv run uvicorn src:app --reload --host 0.0.0.0 --port 8000
   ```

5. **访问应用**
   - **API文档**: http://localhost:8000/docs
   - **ReDoc文档**: http://localhost:8000/redoc
   - **健康检查**: http://localhost:8000/api/v1/base/health

### 🔑 默认账户

- **用户名**: `admin`
- **密码**: `abcd1234`
- **邮箱**: `admin@admin.com`

⚠️ **重要**: 生产环境请立即修改默认密码！

---

## 🏗️ 架构说明

项目采用经典的三层架构设计：

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│  (src/api/v1/) - 路由处理、参数验证、响应格式化               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                          │
│  (src/services/) - 业务逻辑、权限校验、数据处理               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Repository Layer                          │
│  (src/repositories/) - 数据访问、CRUD操作、查询优化          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Model Layer                            │
│  (src/models/) - 数据模型、数据库表结构定义                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 开发指南

### 常用命令

```bash
# 开发服务器
uv run uvicorn src:app --reload

# 代码格式化
uv run ruff format src/

# 代码检查
uv run ruff check --fix src/

# 运行测试
uv run pytest

# 数据库迁移
uv run aerich migrate --name "describe_changes"
uv run aerich upgrade

{%- if cookiecutter.include_docs == "yes" %}
# 文档服务
uv run mkdocs serve
{%- endif %}
```

### 项目结构

```
{{cookiecutter.project_slug}}/
├── src/                     # 源代码
│   ├── api/v1/             # API路由层
│   ├── services/           # 业务逻辑层  
│   ├── repositories/       # 数据访问层
│   ├── models/             # 数据模型层
│   ├── schemas/            # Pydantic模式
│   ├── core/               # 核心功能
│   ├── utils/              # 工具函数
│   └── settings/           # 配置管理
├── tests/                  # 测试文件
{%- if cookiecutter.include_docs == "yes" %}
├── docs/                   # 项目文档
{%- endif %}
├── migrations/             # 数据库迁移
└── logs/                   # 日志文件
```

---

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

本项目基于 {{cookiecutter.license}} 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- **模板来源**: [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template) by [@JiayuXu0](https://github.com/JiayuXu0)
- **技术栈**: [FastAPI](https://fastapi.tiangolo.com/), [Tortoise ORM](https://tortoise-orm.readthedocs.io/), [UV](https://github.com/astral-sh/uv)
- **作者**: {{cookiecutter.author_name}} ({{cookiecutter.author_email}})

---

<div align="center">

**🌟 如果这个项目对你有帮助，别忘了给原模板项目点个 Star！**

**[⭐ FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template)**

**感谢 [@JiayuXu0](https://github.com/JiayuXu0) 的优秀工作！**

</div>