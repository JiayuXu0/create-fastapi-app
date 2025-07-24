# 🤝 贡献指南

首先，感谢你考虑为 Create FastAPI App 做贡献！

## 📋 行为准则

参与此项目即表示你同意遵守我们的行为准则：尊重、包容、专业。

## 🚀 如何贡献

### 报告 Bug

1. 使用 GitHub Issues 创建新 issue
2. 描述清楚问题和复现步骤
3. 包含错误信息和环境信息

### 提出新功能

1. 先在 Issues 中讨论你的想法
2. 说明功能的使用场景和价值
3. 等待社区反馈后再开始开发

### 提交代码

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 开发指南

### 环境设置

```bash
# 克隆项目
git clone https://github.com/yourusername/create-fastapi-app.git
cd create-fastapi-app

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements-dev.txt
```

### 测试

```bash
# 测试模板生成
cookiecutter . --no-input

# 运行钩子测试
python hooks/pre_gen_project.py
python hooks/post_gen_project.py
```

### 代码风格

- 使用 Black 格式化 Python 代码
- 遵循 PEP 8 规范
- 编写清晰的注释和文档

## 📌 提交信息规范

使用以下格式：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

示例：`feat: 添加 MySQL 数据库选项`

## 🙏 致谢

所有贡献者都将被列在项目 README 中！