#!/bin/bash

# FastAPI Template 文档部署脚本

set -e

echo "🚀 FastAPI Template 文档部署脚本"
echo "================================="

# 检查是否安装了UV
if ! command -v uv &> /dev/null; then
    echo "❌ UV 未安装，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc
fi

# 检查是否安装了Git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

# 安装文档依赖
echo "📦 安装文档依赖..."
uv sync --group docs

# 构建文档
echo "🏗️  构建文档..."
uv run mkdocs build

# 检查构建结果
if [ -d "site" ]; then
    echo "✅ 文档构建成功！"
    echo "📁 构建文件位于: site/"
else
    echo "❌ 文档构建失败"
    exit 1
fi

# 询问是否部署到GitHub Pages
read -p "🤔 是否部署到GitHub Pages? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 部署到GitHub Pages..."
    uv run mkdocs gh-deploy
    echo "✅ 部署完成！"
    echo "🌐 访问地址: https://$(git remote get-url origin | sed 's/.*github.com[:/]//' | sed 's/.git$//' | sed 's/\//./').github.io/$(basename $(git remote get-url origin) .git)/"
else
    echo "📋 手动部署选项:"
    echo "   - 本地预览: uv run mkdocs serve"
    echo "   - 构建文档: uv run mkdocs build"
    echo "   - 部署到GitHub Pages: uv run mkdocs gh-deploy"
fi

# 显示本地预览信息
echo ""
echo "📖 本地预览:"
echo "   uv run mkdocs serve"
echo "   访问地址: http://localhost:8000"
echo ""
echo "🎉 文档系统设置完成！"
