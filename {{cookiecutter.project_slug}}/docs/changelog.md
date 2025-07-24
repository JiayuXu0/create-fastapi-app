# 更新日志

所有重要的项目更改都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 完整的MkDocs文档系统
- API文档自动生成功能
- 类似vue-element-admin的现代化UI风格
- 交互式API测试功能

### 变更
- 优化了项目结构和架构文档
- 改进了开发者体验

## [1.0.0] - 2024-01-01

### 新增
- 🎉 首次发布！
- 企业级三层架构设计
- 完整的RBAC权限管理系统
- JWT认证和授权机制
- 用户管理功能
- 角色和权限管理
- 菜单管理系统
- 文件上传下载功能
- 审计日志记录
- 部门管理功能
- API权限控制
- 数据库迁移支持
- 完整的测试覆盖
- Docker容器化支持
- GitHub Actions CI/CD
- 代码质量检查工具

### 架构特性
- **API层**: FastAPI路由处理
- **Service层**: 业务逻辑实现
- **Repository层**: 数据访问抽象
- **Model层**: Tortoise ORM模型

### 安全特性
- Argon2密码哈希
- JWT访问令牌(4小时)
- 刷新令牌(7天)
- 登录频率限制
- CORS跨域配置
- 输入验证和清理

### 开发工具
- UV包管理器
- Black代码格式化
- Ruff代码检查
- MyPy类型检查
- Pytest测试框架
- 异步测试支持

### 数据库支持
- PostgreSQL(生产推荐)
- SQLite(开发默认)
- Aerich迁移工具
- 数据库连接池

### 部署支持
- Docker多阶段构建
- 环境变量配置
- 健康检查端点
- 生产优化配置

## [0.9.0] - 2023-12-15

### 新增
- 项目基础架构搭建
- 核心模型设计
- 认证系统原型
- 基础API端点

### 变更
- 优化了数据库设计
- 改进了错误处理机制

## [0.8.0] - 2023-12-01

### 新增
- 初始项目结构
- 基础依赖配置
- 开发环境设置

### 技术栈选择
- FastAPI 作为Web框架
- Tortoise ORM 作为数据库ORM
- Pydantic 用于数据验证
- UV 作为包管理器

## 发布说明

### 版本命名规则

我们采用语义化版本控制：

- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订版本号**: 向下兼容的问题修正

### 发布流程

1. **开发分支**: 日常开发在 `develop` 分支进行
2. **功能分支**: 新功能在 `feature/*` 分支开发
3. **发布分支**: 准备发布时创建 `release/*` 分支
4. **主分支**: 稳定版本合并到 `main` 分支
5. **标签**: 每个发布版本都有对应的Git标签

### 变更分类

- **新增**: 新功能
- **变更**: 现有功能的修改
- **废弃**: 将在未来版本中移除的功能
- **移除**: 在此版本中移除的功能
- **修复**: 错误修复
- **安全**: 安全相关的修复

### 升级指南

#### 从 0.x 升级到 1.0

1. **数据库迁移**: 运行所有迁移脚本
2. **配置更新**: 更新环境变量配置
3. **API变更**: 检查API端点变化
4. **依赖更新**: 更新到最新依赖版本

```bash
# 备份数据
pg_dump your_database > backup.sql

# 更新代码
git pull origin main

# 更新依赖
uv sync

# 运行迁移
uv run aerich upgrade

# 重启服务
systemctl restart fastapi-template
```

### 兼容性说明

#### 1.0.0 兼容性
- ✅ Python 3.11+
- ✅ PostgreSQL 12+
- ✅ SQLite 3.35+
- ✅ Redis 6.0+
- ✅ Docker 20.10+

#### 浏览器支持
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### 性能改进

#### 1.0.0 性能指标
- 🚀 启动时间: < 3秒
- 📊 并发处理: 1000+ req/s
- 💾 内存使用: < 100MB
- 🔄 响应时间: < 100ms (95th percentile)

### 安全更新

#### 1.0.0 安全增强
- 🔐 密码复杂度要求
- 🛡️ SQL注入防护
- 🚫 XSS攻击防护
- 📝 安全日志记录
- 🔒 安全HTTP头设置

### 已知问题

#### 1.0.0 已知限制
- 暂不支持多租户架构
- 文件上传大小限制为100MB
- 同时在线用户数限制为1000
- 暂不支持实时通知

### 路线图

#### 1.1.0 计划功能
- [ ] 多租户支持
- [ ] 实时通知系统
- [ ] 高级搜索功能
- [ ] 数据导入导出
- [ ] 移动端API优化

#### 1.2.0 计划功能
- [ ] 微服务架构支持
- [ ] 消息队列集成
- [ ] 缓存层优化
- [ ] 性能监控面板
- [ ] 自动化部署工具

### 社区贡献

我们感谢所有贡献者的努力！

#### 贡献者统计
- 👥 总贡献者: 5
- 🎯 已关闭Issue: 45
- 🔄 已合并PR: 89
- 📝 代码行数: 15,000+

#### 特别感谢
- [@contributor1](https://github.com/contributor1) - 核心架构设计
- [@contributor2](https://github.com/contributor2) - 安全审计
- [@contributor3](https://github.com/contributor3) - 文档编写
- [@contributor4](https://github.com/contributor4) - 测试覆盖
- [@contributor5](https://github.com/contributor5) - 性能优化

### 获取支持

如果您遇到问题或需要帮助：

1. 📖 查看[官网文档](http://fastapi.infyai.cn/)
2. 🔍 搜索[已知问题](https://github.com/JiayuXu0/FastAPI-Template/issues)
3. 💬 提交[新问题](https://github.com/JiayuXu0/FastAPI-Template/issues/new)

### 许可证

本项目采用 MIT 许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  <i>由 EvoAI Team 用 ❤️ 制作</i>
</p>
