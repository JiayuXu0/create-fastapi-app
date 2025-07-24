<div align="center">

# 🚀 Create FastAPI App

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-00a393.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Cookiecutter-2.0+-D4A76A.svg?style=for-the-badge&logo=cookiecutter&logoColor=white" alt="Cookiecutter">
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/JiayuXu0/create-fastapi-app?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/stars/JiayuXu0/create-fastapi-app?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/github/forks/JiayuXu0/create-fastapi-app?style=for-the-badge" alt="Forks">
</p>

<h3>🎯 Create Production-Ready FastAPI Projects in Seconds</h3>

<p align="center">
  <strong>Enterprise-grade project generator based on <a href="https://github.com/JiayuXu0/FastAPI-Template">FastAPI-Template</a> (200+ ⭐)</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-demo">Demo</a> •
  <a href="#-why-choose">Why Choose</a> •
  <a href="#-options">Options</a>
</p>

</div>

---

## 🎬 Demo

<div align="center">
  <img src="https://github.com/JiayuXu0/create-fastapi-app/assets/demo.gif" alt="Demo" width="600">
</div>

## ✨ Features

<table>
<tr>
<td>

### 🏗️ Architecture
- ✅ **Three-Layer Design** - Clear API/Service/Repository separation
- ✅ **Dependency Injection** - Native FastAPI DI system
- ✅ **Async First** - Full async I/O operations
- ✅ **Type Safety** - Complete type annotations

</td>
<td>

### 🔐 Security & Auth
- ✅ **JWT Authentication** - Dual token system (Access + Refresh)
- ✅ **RBAC System** - Role-based access control
- ✅ **Password Security** - Argon2 hashing
- ✅ **Rate Limiting** - API request throttling

</td>
</tr>
<tr>
<td>

### 🚀 Performance
- ✅ **Redis Caching** - Smart caching strategies
- ✅ **DB Optimization** - Connection pooling + query optimization
- ✅ **File Management** - Secure upload/download
- ✅ **Background Tasks** - Async task processing

</td>
<td>

### 🛠️ Developer Experience
- ✅ **Auto Documentation** - Swagger/ReDoc
- ✅ **Code Quality** - Pre-commit + Ruff
- ✅ **Testing** - Pytest + coverage
- ✅ **Docker Ready** - Container deployment

</td>
</tr>
</table>

## 🚀 Quick Start

### Installation

```bash
pip install cookiecutter
```

### Create Project

```bash
cookiecutter https://github.com/JiayuXu0/create-fastapi-app
```

### Interactive Setup

```bash
project_name [My FastAPI Project]: Awesome API
project_slug [awesome-api]: 
project_description [Enterprise FastAPI Backend]: High-performance microservice API
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
github_username [yourusername]: johndoe
Select database_type:
1 - postgresql
2 - sqlite
Choose from 1, 2 [1]: 1
Select use_redis:
1 - yes
2 - no
Choose from 1, 2 [1]: 1
```

### Start Project

```bash
cd awesome-api
cp .env.example .env
uv sync --dev
uv run aerich init-db
uv run uvicorn src:app --reload
```

🎉 **Done!** Visit http://localhost:8000/docs for API documentation

## 🎯 Why Choose Create FastAPI App?

### 🆚 Comparison

| Feature | Create FastAPI App | Basic Templates | From Scratch |
|---------|-------------------|-----------------|--------------|
| Setup Time | ⚡ 2 minutes | 🐢 10 minutes | 🐌 Hours |
| Enterprise Architecture | ✅ Built-in | ❌ Manual setup | ❌ Manual design |
| RBAC System | ✅ Ready to use | ❌ Need development | ❌ Need development |
| Production Ready | ✅ Fully ready | ⚠️ Needs tuning | ❌ Extensive work |
| Best Practices | ✅ Following standards | ⚠️ Varies | ❌ Easy to miss |

### 💡 Use Cases

- 🏢 **Enterprise Apps** - Systems requiring complete permission management
- 🚀 **Rapid Prototyping** - Quickly validate business ideas
- 📚 **Learning Projects** - Learn FastAPI best practices
- 🔧 **Microservices** - Foundation for microservice architecture

## 📋 Configuration Options

### Basic Options

| Option | Description | Default |
|--------|-------------|---------|
| `project_name` | Project name | My FastAPI Project |
| `project_slug` | URL-friendly identifier | Auto-generated |
| `project_description` | Project description | Enterprise FastAPI Backend |
| `author_name` | Author name | Your Name |
| `author_email` | Author email | your.email@example.com |

### Technical Choices

| Option | Choices | Description |
|--------|---------|-------------|
| `database_type` | postgresql, sqlite | Database type |
| `use_redis` | yes, no | Include Redis caching |
| `include_docs` | yes, no | Include MkDocs documentation |
| `python_version` | 3.11, 3.12 | Python version |

## 📁 Generated Project Structure

```
awesome-api/
├── 📄 README.md                 # Project documentation
├── 🐳 Dockerfile                # Docker configuration
├── 📋 pyproject.toml            # Project dependencies
├── 🔧 .env.example              # Environment variables
├── 📂 src/                      # Source code
│   ├── 🌐 api/v1/              # API routes layer
│   ├── 💼 services/            # Business logic layer
│   ├── 🗄️ repositories/        # Data access layer
│   ├── 📊 models/              # Data models
│   ├── ✅ schemas/             # Validation schemas
│   ├── 🔧 core/                # Core functionality
│   └── 🛠️ utils/               # Utility functions
├── 🧪 tests/                   # Test directory
├── 📚 docs/                    # Documentation
└── 🔄 migrations/              # Database migrations
```

## 🎨 Generated Project Preview

<details>
<summary><b>📱 API Documentation Interface</b></summary>

![API Docs](https://github.com/JiayuXu0/create-fastapi-app/assets/api-docs.png)

</details>

<details>
<summary><b>🔐 RBAC Permission Management</b></summary>

![RBAC System](https://github.com/JiayuXu0/create-fastapi-app/assets/rbac.png)

</details>

<details>
<summary><b>📊 Project Structure</b></summary>

![Project Structure](https://github.com/JiayuXu0/create-fastapi-app/assets/structure.png)

</details>

## 🤝 Contributing

Contributions welcome! Please check [Contributing Guide](CONTRIBUTING.md) to get started.

### Contributors

<a href="https://github.com/JiayuXu0/create-fastapi-app/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=JiayuXu0/create-fastapi-app" />
</a>

## 📄 License

This project is open source under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🌟 [FastAPI-Template](https://github.com/JiayuXu0/FastAPI-Template) - Core template
- 🍪 [Cookiecutter](https://github.com/cookiecutter/cookiecutter) - Project generator
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) - Web framework

---

<div align="center">

### 🌟 If this project helps you, please give it a Star!

<a href="https://github.com/JiayuXu0/create-fastapi-app">
  <img src="https://img.shields.io/github/stars/JiayuXu0/create-fastapi-app?style=social" alt="Star">
</a>

<p>
  <a href="https://github.com/JiayuXu0/FastAPI-Template">⭐ Also welcome to star the original template</a>
</p>

</div>