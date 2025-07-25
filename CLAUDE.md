# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Create FastAPI App** is a Cookiecutter-based project generator that creates enterprise-grade FastAPI backend applications. It serves as a template system that generates production-ready FastAPI projects with comprehensive features including RBAC authorization, JWT authentication, audit logging, file management, and clean three-layer architecture.

## Common Development Commands

### Template Generation
```bash
# Generate a new FastAPI project from this template
cookiecutter https://github.com/JiayuXu0/create-fastapi-app

# Generate locally (for testing template changes)
cookiecutter . --no-input --overwrite-if-exists
```

### Template Testing
```bash
# Test template generation with default values
cd /tmp && cookiecutter /path/to/create-fastapi-app --no-input

# Test generated project setup
cd my-fastapi-project
cp .env.example .env
uv sync --dev
uv run aerich init-db
uv run uvicorn src:app --reload
```

### Template Development
```bash
# Validate cookiecutter configuration
cookiecutter --help

# Test hooks execution
python hooks/pre_gen_project.py
python hooks/post_gen_project.py
```

## Architecture

### Cookiecutter Template Structure
The template uses Cookiecutter's Jinja2 templating system with the following key components:

- **cookiecutter.json**: Defines template variables and defaults
- **{{cookiecutter.project_slug}}/**: Template directory containing the FastAPI project structure
- **hooks/**: Pre and post-generation Python scripts for validation and setup
- **README.md**: Documentation for template users

### Generated Project Architecture
The template creates projects with clean three-layer architecture:

```
API Layer (src/api/v1/) 
    ↓ calls
Service Layer (src/services/) 
    ↓ calls  
Repository Layer (src/repositories/)
    ↓ calls
Model Layer (src/models/)
```

### Key Template Features
- **Enterprise-Ready**: RBAC authorization, JWT auth, audit logging
- **Modern Stack**: FastAPI + Tortoise ORM + UV package manager + Ruff formatting
- **Production Features**: Docker support, Redis caching, rate limiting, security middleware
- **Developer Experience**: Pre-commit hooks, comprehensive testing, MkDocs documentation
- **Flexible Configuration**: PostgreSQL/SQLite, optional Redis, Docker, docs generation

## Template Configuration Options

### Basic Information
- `project_name`: Human-readable project name
- `project_slug`: URL-friendly identifier (auto-generated from project_name)
- `project_description`: Brief project description
- `author_name` / `author_email`: Author information
- `github_username`: GitHub username for repository links

### Technical Choices
- `python_version`: 3.11 or 3.12
- `database_type`: postgresql or sqlite
- `use_redis`: yes/no - Redis caching support
- `include_docs`: yes/no - MkDocs documentation
- `include_docker`: yes/no - Docker configuration files
- `use_pre_commit`: yes/no - Pre-commit hooks setup

## Hook Scripts

### Pre-generation Hook (hooks/pre_gen_project.py)
Validates user input before template generation:
- Project name length (minimum 3 characters)
- Project slug format (valid Python package name)
- Email format validation
- GitHub username format validation

### Post-generation Hook (hooks/post_gen_project.py)
Performs cleanup and setup after generation:
- Removes unused files based on configuration choices
- Creates appropriate .env.example file
- Sets executable permissions on scripts
- Displays setup instructions to user

## Development Workflow

### Making Template Changes
1. **Edit Template Files**: Modify files in `{{cookiecutter.project_slug}}/`
2. **Update Configuration**: Adjust `cookiecutter.json` if adding new options
3. **Test Generation**: Use `cookiecutter . --no-input` to test locally
4. **Test Generated Project**: Verify the generated project works correctly
5. **Update Hooks**: Modify validation/setup logic if needed

### Adding New Features to Generated Projects
1. **Add to Template**: Implement feature in `{{cookiecutter.project_slug}}/src/`
2. **Update Dependencies**: Modify `pyproject.toml` template
3. **Add Configuration**: Update environment variables in hooks
4. **Update Documentation**: Modify generated `README.md` and `CLAUDE.md`
5. **Add Tests**: Include test coverage in template

### Template Variables Usage
Use Jinja2 syntax for dynamic content:
- `{{ cookiecutter.variable_name }}`: Insert variable value
- `{% if cookiecutter.option == "yes" %}...{% endif %}`: Conditional content
- Template files use `.j2` extension or are processed by default

## Generated Project Standards

### Code Quality Tools
- **Ruff**: Modern linting and formatting (replaces Black, isort, flake8)
- **MyPy**: Type checking with strict configuration
- **Pre-commit**: Automated code quality checks
- **Pytest**: Comprehensive testing with async support

### Security Best Practices
- Argon2 password hashing
- JWT token management with refresh tokens
- CORS configuration with specific origins
- Rate limiting with SlowAPI
- Input validation with Pydantic
- Environment-based configuration

### Development Commands (Generated Projects)
```bash
# Setup
uv sync --dev
uv run aerich init-db

# Development
uv run uvicorn src:app --reload

# Testing
uv run pytest
uv run pytest --cov=src --cov-report=html

# Code Quality
uv run ruff check --fix src/
uv run ruff format src/
uv run mypy src/

# Database
uv run aerich migrate --name "description"
uv run aerich upgrade

# Documentation
uv run mkdocs serve
```

## Important Notes

- **Template Location**: Main template content is in `{{cookiecutter.project_slug}}/`
- **Variable References**: Use exact cookiecutter variable names from `cookiecutter.json`
- **File Filtering**: Use `_copy_without_render` for files that shouldn't be templated
- **Hook Execution**: Pre-gen hook runs before generation, post-gen after
- **Testing Required**: Always test both template generation and generated project functionality
- **UV Package Manager**: Generated projects use UV exclusively, not pip
- **Entry Point**: Generated FastAPI apps start from `src/__init__.py`