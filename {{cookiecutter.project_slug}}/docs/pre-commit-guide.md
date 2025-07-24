# Pre-commit Hooks 使用指南

本项目使用 pre-commit hooks 确保代码质量和一致性。

## 🔧 什么是 Pre-commit Hooks？

Pre-commit hooks 是在每次 `git commit` 之前自动运行的脚本，用于：
- 自动格式化代码
- 检查代码质量
- 防止低质量代码提交

## ✅ 启用的检查项

### 基础检查
- **trailing-whitespace**: 移除行尾空格
- **end-of-file-fixer**: 确保文件以换行符结尾
- **check-yaml/json/toml/xml**: 检查文件语法
- **check-added-large-files**: 防止提交大文件 (>10MB)
- **check-merge-conflict**: 检查合并冲突标记
- **debug-statements**: 检查调试语句 (如 `pdb.set_trace()`)
- **mixed-line-ending**: 统一行结束符
- **check-case-conflict**: 防止文件名大小写冲突

### Python 代码检查
- **ruff**: 代码质量检查和自动修复
- **ruff-format**: 代码格式化 (替代 black)

## 🚀 使用方法

### 自动安装 (推荐)
```bash
# 克隆项目后自动安装
uv sync  # hooks 会自动安装
```

### 手动安装
```bash
# 安装 pre-commit
uv add --dev pre-commit

# 安装 hooks
uv run pre-commit install
```

### 手动运行检查
```bash
# 检查所有文件
uv run pre-commit run --all-files

# 检查特定文件
uv run pre-commit run --files src/main.py

# 只运行 ruff 检查
uv run pre-commit run ruff --all-files
```

## 🔄 工作流程

1. **编写代码** - 正常开发
2. **提交代码** - `git commit -m "your message"`
3. **自动检查** - pre-commit 自动运行
4. **如有问题** - 自动修复或提示手动修复
5. **重新提交** - 修复后重新 commit

## 🛑 如何禁用 Pre-commit Hooks

### 方法1: 完全卸载 (不推荐)
```bash
# 卸载 hooks
uv run pre-commit uninstall

# 重新安装
uv run pre-commit install
```

### 方法2: 跳过单次检查
```bash
# 跳过本次检查 (谨慎使用)
git commit --no-verify -m "urgent fix"
```

### 方法3: 禁用特定检查
编辑 `.pre-commit-config.yaml`，注释掉不需要的 hooks：

```yaml
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      # - id: debug-statements    # 注释掉不需要的检查
```

### 方法4: 设置环境变量
```bash
# 临时禁用
export SKIP=ruff,ruff-format
git commit -m "message"

# 或在 .env 中设置
echo "SKIP=ruff" >> .env
```

## 🎯 推荐配置

### 团队开发 (推荐全部启用)
适合需要统一代码风格的团队项目。

### 个人项目 (可选择性启用)
```yaml
# 最小化配置 - 只保留基本检查
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### 严格模式 (取消注释可选项)
启用 mypy 类型检查和 bandit 安全检查。

## ❓ 常见问题

### Q: 提交很慢怎么办？
A: 首次运行会下载工具，后续会很快。可以用 `--no-verify` 跳过紧急提交。

### Q: 格式化改动太多？
A: 先运行 `uv run pre-commit run --all-files` 一次性格式化所有文件。

### Q: 想自定义规则？
A: 编辑 `pyproject.toml` 中的 ruff 配置：

```toml
[tool.ruff]
extend-ignore = ["E501"]  # 忽略行长度检查
```

### Q: CI/CD 中如何使用？
A: 在 GitHub Actions 中：

```yaml
- name: Run pre-commit
  run: |
    uv sync
    uv run pre-commit run --all-files
```

## 📚 参考资源

- [Pre-commit 官方文档](https://pre-commit.com/)
- [Ruff 配置指南](https://docs.astral.sh/ruff/)
- [项目 CLAUDE.md](../CLAUDE.md) - 完整开发指南
