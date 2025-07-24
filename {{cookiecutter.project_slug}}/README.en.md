# 🚀 {{cookiecutter.project_name}}

<div align="center">

**{{cookiecutter.project_description}}**

> **🎉 Created based on [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template)**
> 
> 💝 **Thanks to**: [@JiayuXu0](https://github.com/JiayuXu0) for providing this excellent enterprise FastAPI template
> 
> 🌟 **If this template helps you, please give the original project a Star**: [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template)

---

[简体中文](README.md) | **English**

[![Python](https://img.shields.io/badge/Python-{{cookiecutter.python_version}}+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-{{cookiecutter.license}}-yellow.svg)](https://opensource.org/licenses/{{cookiecutter.license}})

[![UV](https://img.shields.io/badge/📦_Package_Manager-UV-blueviolet.svg)](https://github.com/astral-sh/uv)
[![Architecture](https://img.shields.io/badge/🏗️_Architecture-Three_Layer-orange.svg)](#)
[![RBAC](https://img.shields.io/badge/🔐_Permission-RBAC-red.svg)](#)
[![Docker](https://img.shields.io/badge/🐳_Container-Docker-blue.svg)](https://www.docker.com/)

[📖 Quick Start](#-quick-start) • [🏗️ Architecture](#-architecture) • [📚 Development Guide](CLAUDE.md) • [🤝 Contributing](CONTRIBUTING.md)

</div>

---

## ✨ Template-Based Core Features

This project is built based on [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template) with the following enterprise-grade features:

- 🏗️ **Clean Three-Layer Architecture** - API/Service/Repository layered design
- 🔐 **Complete RBAC Permission Management** - Role, menu, and API permission control
- 👤 **User Authentication & JWT Management** - Secure identity verification system
- 📝 **Audit Logging & Monitoring** - Comprehensive operation tracking
- 🚀 **Redis Cache Optimization** - High-performance caching strategy
- 📁 **Secure File Management** - File upload/download with validation
- 🐳 **Docker Containerization** - Ready-to-use deployment solution
- 📖 **Automatic API Documentation** - Swagger/ReDoc documentation generation
- 🔧 **Code Quality Assurance** - Pre-commit hooks + Ruff
- 📊 **MkDocs Documentation Site** - Complete project documentation

---

## 🚀 Quick Start

### 📋 Requirements

- Python {{cookiecutter.python_version}}+
- UV (recommended) or pip
{%- if cookiecutter.database_type == "postgresql" %}
- PostgreSQL 12+
{%- endif %}
{%- if cookiecutter.use_redis == "yes" %}
- Redis 6+
{%- endif %}

### 🛠️ Installation & Deployment

1. **Install Dependencies**
   ```bash
   # Install UV (recommended)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install project dependencies
   uv sync --dev
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment configuration file
   cp .env.example .env
   
   # Edit configuration file
   nano .env
   ```

3. **Database Initialization**
   ```bash
   # Initialize database
   uv run aerich init-db
   
   # Apply migrations
   uv run aerich upgrade
   ```

4. **Start Service**
   ```bash
   # Development environment startup
   uv run uvicorn src:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access Application**
   - **API Documentation**: http://localhost:8000/docs
   - **ReDoc Documentation**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/api/v1/base/health

### 🔑 Default Account

- **Username**: `admin`
- **Password**: `abcd1234`
- **Email**: `admin@admin.com`

⚠️ **Important**: Please change the default password immediately in production!

---

## 🏗️ Architecture

The project adopts a classic three-layer architecture design:

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│  (src/api/v1/) - Route handling, validation, response       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                          │
│  (src/services/) - Business logic, permissions, processing  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Repository Layer                          │
│  (src/repositories/) - Data access, CRUD, query optimization│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Model Layer                            │
│  (src/models/) - Data models, database schema definitions   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Development Guide

### Common Commands

```bash
# Development server
uv run uvicorn src:app --reload

# Code formatting
uv run ruff format src/

# Code checking
uv run ruff check --fix src/

# Run tests
uv run pytest

# Database migration
uv run aerich migrate --name "describe_changes"
uv run aerich upgrade

{%- if cookiecutter.include_docs == "yes" %}
# Documentation service
uv run mkdocs serve
{%- endif %}
```

### Project Structure

```
{{cookiecutter.project_slug}}/
├── src/                     # Source code
│   ├── api/v1/             # API route layer
│   ├── services/           # Business logic layer  
│   ├── repositories/       # Data access layer
│   ├── models/             # Data model layer
│   ├── schemas/            # Pydantic schemas
│   ├── core/               # Core functionality
│   ├── utils/              # Utility functions
│   └── settings/           # Configuration management
├── tests/                  # Test files
{%- if cookiecutter.include_docs == "yes" %}
├── docs/                   # Project documentation
{%- endif %}
├── migrations/             # Database migrations
└── logs/                   # Log files
```

---

## 🤝 Contributing

1. Fork this project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is open source under the {{cookiecutter.license}} license - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Template Source**: [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template) by [@JiayuXu0](https://github.com/JiayuXu0)
- **Tech Stack**: [FastAPI](https://fastapi.tiangolo.com/), [Tortoise ORM](https://tortoise-orm.readthedocs.io/), [UV](https://github.com/astral-sh/uv)
- **Author**: {{cookiecutter.author_name}} ({{cookiecutter.author_email}})

---

<div align="center">

**🌟 If this project helps you, don't forget to give the original template project a Star!**

**[⭐ FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template)**

**Thanks to [@JiayuXu0](https://github.com/JiayuXu0) for the excellent work!**

</div>