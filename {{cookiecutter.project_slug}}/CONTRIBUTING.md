# 🤝 贡献指南

感谢您对企业级FastAPI后端模板项目的关注！我们欢迎所有形式的贡献。

## 🚀 快速开始

1. **Fork项目**到您的GitHub账户
2. **克隆**您的fork到本地机器
3. **创建分支**用于您的功能或修复
4. **开发和测试**您的更改
5. **提交**Pull Request

## 💻 开发环境设置

```bash
# 克隆您的fork
git clone https://github.com/your-username/FastAPI-Template.git
cd FastAPI-Template

# 安装UV (如果还没有)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync --dev

# 复制环境配置
cp .env.example .env
# 编辑 .env 文件，设置必要的配置

# 初始化数据库
uv run aerich init-db

# 运行开发服务器
uv run uvicorn src:app --reload --host 0.0.0.0 --port 8000
```

## 📋 代码规范

我们使用以下工具来保持代码质量：

```bash
# 代码格式化
uv run ruff format src/

# 代码检查
uv run ruff check src/

# 类型检查
uv run mypy src/

# 运行测试
uv run pytest
```

## 🎯 贡献类型

我们欢迎以下类型的贡献：

- 🐛 **Bug修复**
- ✨ **新功能**
- 📚 **文档改进**
- 🧪 **测试添加**
- ⚡ **性能优化**
- 🎨 **代码重构**

## 📝 提交规范

请使用清晰的提交信息：

```
类型(范围): 简短描述

详细描述（如果需要）
```

示例：
- `feat(api): 添加用户导出功能`
- `fix(auth): 修复JWT token过期处理`
- `docs(readme): 更新安装说明`

## 🔄 Pull Request流程

1. **确保**您的代码通过所有检查
2. **更新**相关文档
3. **添加**适当的测试
4. **填写**PR模板中的所有信息
5. **等待**代码审查

## 🧪 测试

请为您的更改添加测试：

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_your_feature.py

# 生成覆盖率报告
uv run pytest --cov=src --cov-report=html
```

## 📚 文档

如果您的更改影响用户体验，请更新相关文档：

- **README.md** - 项目概述和快速开始
- **CLAUDE.md** - 开发者详细指南
- **API文档** - 如果有API变更

## 🐛 报告问题

发现bug？请使用我们的issue模板报告：

1. 检查是否已有相似的issue
2. 使用appropriate的issue模板
3. 提供详细的重现步骤
4. 包含相关的环境信息

## 💡 功能请求

有好的想法？我们很乐意听到：

1. 使用功能请求模板
2. 清楚地描述用例
3. 考虑向后兼容性
4. 讨论实现方法

## ❓ 需要帮助？

- 🌐 访问[官网](http://fastapi.infyai.cn/)获取最新文档
- 📖 查看[CLAUDE.md](CLAUDE.md)开发指南
- 🔍 搜索现有的issues
- 💬 在discussions中提问
- 📧 联系维护者

## 🏆 贡献者

感谢所有为这个项目做出贡献的开发者！

---

**每个贡献都很重要，无论大小。感谢您帮助改进这个项目！** 🙏
