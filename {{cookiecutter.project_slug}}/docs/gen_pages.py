#!/usr/bin/env python3
"""
API文档自动生成脚本
从FastAPI应用中提取路由信息，生成API文档
"""

import inspect
import json
import sys
from pathlib import Path
from typing import Any, Union

import mkdocs_gen_files

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fastapi import FastAPI
    from fastapi.openapi.utils import get_openapi
    from fastapi.routing import APIRoute
    from pydantic import BaseModel

    # 导入应用
    from src import app
except ImportError as e:
    print(f"无法导入FastAPI应用: {e}")
    app = None


def get_model_fields(model: type[BaseModel]) -> list[dict[str, Any]]:
    """提取Pydantic模型的字段信息"""
    fields = []
    if not hasattr(model, "model_fields"):
        return fields

    for field_name, field_info in model.model_fields.items():
        field_type = field_info.annotation
        field_type_str = str(field_type).replace("typing.", "").replace("builtins.", "")

        # 获取字段描述
        description = ""
        if hasattr(field_info, "description") and field_info.description:
            description = field_info.description
        elif hasattr(field_info, "title") and field_info.title:
            description = field_info.title

        # 获取默认值
        default = None
        if hasattr(field_info, "default") and field_info.default is not None:
            default = field_info.default

        # 获取示例值
        example = None
        if hasattr(field_info, "examples") and field_info.examples:
            example = (
                field_info.examples[0]
                if isinstance(field_info.examples, list)
                else field_info.examples
            )
        elif hasattr(field_info, "example") and field_info.example is not None:
            example = field_info.example

        # 获取约束
        constraints = []
        if hasattr(field_info, "min_length") and field_info.min_length is not None:
            constraints.append(f"最小长度: {field_info.min_length}")
        if hasattr(field_info, "max_length") and field_info.max_length is not None:
            constraints.append(f"最大长度: {field_info.max_length}")
        if hasattr(field_info, "ge") and field_info.ge is not None:
            constraints.append(f"最小值: {field_info.ge}")
        if hasattr(field_info, "le") and field_info.le is not None:
            constraints.append(f"最大值: {field_info.le}")
        if hasattr(field_info, "pattern") and field_info.pattern is not None:
            constraints.append(f"正则: `{field_info.pattern}`")

        required = (
            field_info.is_required() if hasattr(field_info, "is_required") else True
        )

        fields.append(
            {
                "name": field_name,
                "type": field_type_str,
                "required": required,
                "description": description,
                "default": default,
                "example": example,
                "constraints": constraints,
            }
        )

    return fields


def extract_route_details(route: APIRoute) -> dict[str, Any]:
    """提取路由的详细信息，包括参数和响应"""
    route_info = {
        "path": route.path,
        "methods": list(route.methods),
        "name": route.name,
        "summary": getattr(route, "summary", ""),
        "description": getattr(route, "description", ""),
        "tags": getattr(route, "tags", []),
        "deprecated": getattr(route, "deprecated", False),
        "parameters": [],
        "request_body": None,
        "responses": {},
    }

    # 获取端点函数
    endpoint = route.endpoint
    if endpoint:
        # 获取函数签名
        sig = inspect.signature(endpoint)

        # 分析参数
        for param_name, param in sig.parameters.items():
            if param_name in ["request", "response", "background_tasks"]:
                continue

            param_info = {
                "name": param_name,
                "in": "query",  # 默认
                "type": "string",  # 默认
                "required": param.default == param.empty,
                "description": "",
                "default": None if param.default == param.empty else param.default,
            }

            # 检查参数注解
            if param.annotation != param.empty:
                # 处理 Query, Body, Path 等参数
                if hasattr(param.default, "__class__"):
                    param_class = param.default.__class__.__name__

                    if param_class == "Query" or "Query" in str(param.default):
                        param_info["in"] = "query"
                        if hasattr(param.default, "description"):
                            param_info["description"] = param.default.description
                        if hasattr(param.default, "default"):
                            param_info["default"] = param.default.default
                            param_info["required"] = param.default.default == ...

                    elif param_class == "Body" or "Body" in str(param.default):
                        param_info["in"] = "body"
                        if hasattr(param.default, "description"):
                            param_info["description"] = param.default.description

                    elif param_class == "Path" or "Path" in str(param.default):
                        param_info["in"] = "path"
                        if hasattr(param.default, "description"):
                            param_info["description"] = param.default.description

                # 处理 Pydantic 模型 - 这是关键的修复
                try:
                    if inspect.isclass(param.annotation) and issubclass(
                        param.annotation, BaseModel
                    ):
                        param_info["in"] = "body"
                        param_info["type"] = param.annotation.__name__
                        param_info["model_fields"] = get_model_fields(param.annotation)
                        route_info["request_body"] = param_info
                        continue
                except (TypeError, AttributeError):
                    # 如果不是class或者不是BaseModel的子类，继续其他处理
                    pass

                # 处理泛型和Union类型
                if hasattr(param.annotation, "__origin__"):
                    if param.annotation.__origin__ is Union:
                        # 处理Union类型，比如Optional[str]
                        args = param.annotation.__args__
                        if len(args) == 2 and type(None) in args:
                            # 这是Optional类型
                            param_info["required"] = False
                            non_none_type = (
                                args[0] if args[1] is type(None) else args[1]
                            )
                            param_info["type"] = (
                                str(non_none_type)
                                .replace("typing.", "")
                                .replace("builtins.", "")
                            )
                        else:
                            param_info["type"] = (
                                str(param.annotation)
                                .replace("typing.", "")
                                .replace("builtins.", "")
                            )
                    else:
                        param_info["type"] = (
                            str(param.annotation)
                            .replace("typing.", "")
                            .replace("builtins.", "")
                        )
                else:
                    # 简化类型名称
                    param_info["type"] = (
                        str(param.annotation)
                        .replace("typing.", "")
                        .replace("builtins.", "")
                    )

            if param_info["in"] != "body":
                route_info["parameters"].append(param_info)

        # 获取响应模型
        if hasattr(route, "response_model") and route.response_model:
            response_model = route.response_model
            try:
                if inspect.isclass(response_model) and issubclass(
                    response_model, BaseModel
                ):
                    route_info["responses"]["200"] = {
                        "model": response_model.__name__,
                        "fields": get_model_fields(response_model),
                    }
            except (TypeError, AttributeError):
                pass

    return route_info


def generate_parameter_table(parameters: list[dict[str, Any]]) -> str:
    """生成参数表格"""
    if not parameters:
        return "无需参数"

    table = "| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |\n"
    table += "|--------|------|------|------|------|--------|\n"

    for param in parameters:
        required = "是" if param.get("required", False) else "否"
        default = param.get("default", "-")
        if default is None:
            default = "null"
        elif default == ...:
            default = "-"

        table += f"| {param['name']} | `{param['type']}` | {param['in']} | {required} | {param.get('description', '')} | {default} |\n"

    return table


def generate_request_body_section(request_body: dict[str, Any]) -> str:
    """生成请求体文档"""
    if not request_body:
        return ""

    content = "### 请求体\n\n"
    content += "**Content-Type**: `application/json`\n\n"

    if "model_fields" in request_body:
        content += f"**模型**: `{request_body['type']}`\n\n"

        # 生成字段表格
        content += "| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |\n"
        content += "|--------|------|------|------|------|------|\n"

        for field in request_body["model_fields"]:
            required = "是" if field["required"] else "否"
            example = field.get("example", "")
            if example:
                example = f"`{example}`"
            constraints = "<br>".join(field.get("constraints", []))

            content += f"| {field['name']} | `{field['type']}` | {required} | {field.get('description', '')} | {example} | {constraints} |\n"

        # 生成示例
        content += "\n**请求示例**:\n\n```json\n"
        example_data = {}
        for field in request_body["model_fields"]:
            if field.get("example") is not None:
                example_data[field["name"]] = field["example"]
            elif field["required"]:
                # 根据字段名和类型生成更真实的示例
                field_name = field["name"].lower()
                field_type = field["type"].lower()

                if "email" in field_name:
                    example_data[field["name"]] = "admin@example.com"
                elif "username" in field_name or "name" == field_name:
                    example_data[field["name"]] = "admin"
                elif "password" in field_name:
                    example_data[field["name"]] = "password123"
                elif "id" in field_name and "int" in field_type:
                    example_data[field["name"]] = 1
                elif "bool" in field_type:
                    example_data[field["name"]] = True
                elif "list" in field_type:
                    if "role" in field_name:
                        example_data[field["name"]] = [1, 2]
                    else:
                        example_data[field["name"]] = []
                elif "str" in field_type:
                    if "desc" in field_name or "description" in field_name:
                        example_data[field["name"]] = "描述信息"
                    elif "path" in field_name:
                        example_data[field["name"]] = "/api/v1/example"
                    elif "method" in field_name:
                        example_data[field["name"]] = "GET"
                    elif "tag" in field_name:
                        example_data[field["name"]] = "示例模块"
                    else:
                        example_data[field["name"]] = "示例文本"
                elif "int" in field_type:
                    example_data[field["name"]] = 1
                else:
                    example_data[field["name"]] = None

        content += json.dumps(example_data, indent=2, ensure_ascii=False)
        content += "\n```\n\n"

    return content


def generate_module_doc(module_name: str, routes: list[dict[str, Any]]) -> str:
    """为模块生成文档"""

    # 模块名称映射
    module_names = {
        "users": "用户管理",
        "role": "角色管理",
        "menu": "菜单管理",
        "files": "文件管理",
        "dept": "部门管理",
        "api": "API权限",
        "auditlog": "审计日志",
        "base": "认证授权",
    }

    module_display_name = module_names.get(module_name, module_name.title())

    content = f"""# {module_display_name} API

## 概述

{module_display_name}相关的API接口文档。

"""

    # 为每个路由生成详细文档
    for route_data in routes:
        # 提取详细信息
        route_details = (
            extract_route_details(route_data)
            if isinstance(route_data, APIRoute)
            else route_data
        )

        content += f"## {route_details['summary'] or route_details['name']}\n\n"

        # 基本信息
        content += f"- **路径**: `{route_details['path']}`\n"
        content += f"- **方法**: {', '.join(f'`{method}`' for method in route_details['methods'])}\n"

        if route_details["tags"]:
            content += f"- **标签**: {', '.join(route_details['tags'])}\n"

        if route_details.get("deprecated"):
            content += "- **状态**: ⚠️ 已弃用\n"

        content += "\n"

        # 描述
        if route_details["description"]:
            content += f"### 描述\n\n{route_details['description']}\n\n"

        # 参数
        if route_details.get("parameters"):
            content += "### 请求参数\n\n"
            content += generate_parameter_table(route_details["parameters"])
            content += "\n"

        # 请求体
        if route_details.get("request_body"):
            content += generate_request_body_section(route_details["request_body"])

        # 响应
        content += "### 响应\n\n"
        content += "**成功响应**:\n\n"
        content += "- **状态码**: `200`\n"
        content += "- **Content-Type**: `application/json`\n\n"

        # 标准响应格式
        content += "```json\n{\n"
        content += '  "code": 200,\n'
        content += '  "msg": "success",\n'
        content += '  "data": ...\n'
        content += "}\n```\n\n"

        # 错误响应
        content += "**错误响应**:\n\n"
        content += "- **状态码**: `400` / `401` / `403` / `404` / `500`\n\n"
        content += "```json\n{\n"
        content += '  "code": 400,\n'
        content += '  "msg": "错误信息",\n'
        content += '  "data": null\n'
        content += "}\n```\n\n"

        # 使用示例
        content += "### 使用示例\n\n"

        # cURL 示例
        content += "**cURL**:\n```bash\n"

        method = (
            list(route_details["methods"])[0] if route_details["methods"] else "GET"
        )

        # 构建cURL命令
        curl_cmd = f'curl -X {method} "http://localhost:8000{route_details["path"]}'

        # 添加查询参数示例
        query_params = [
            p for p in route_details.get("parameters", []) if p["in"] == "query"
        ]
        if query_params:
            param_examples = []
            for param in query_params:
                if param.get("example"):
                    param_examples.append(f"{param['name']}={param['example']}")
                elif param["required"]:
                    param_examples.append(f"{param['name']}=...")

            if param_examples:
                curl_cmd += "?" + "&".join(param_examples)

        curl_cmd += '"'

        # 添加认证头
        if module_name != "base":
            curl_cmd += ' \\\n  -H "Authorization: Bearer <your-token>"'

        # 添加请求体
        if method in ["POST", "PUT", "PATCH"] and route_details.get("request_body"):
            curl_cmd += ' \\\n  -H "Content-Type: application/json"'
            if route_details["request_body"].get("model_fields"):
                example_data = {}
                for field in route_details["request_body"]["model_fields"]:
                    if field.get("example") is not None:
                        example_data[field["name"]] = field["example"]
                    elif field["required"]:
                        # 根据字段名和类型生成更真实的示例
                        field_name = field["name"].lower()
                        field_type = field["type"].lower()

                        if "email" in field_name:
                            example_data[field["name"]] = "admin@example.com"
                        elif "username" in field_name or "name" == field_name:
                            example_data[field["name"]] = "admin"
                        elif "password" in field_name:
                            example_data[field["name"]] = "password123"
                        elif "id" in field_name and "int" in field_type:
                            example_data[field["name"]] = 1
                        elif "bool" in field_type:
                            example_data[field["name"]] = True
                        elif "list" in field_type:
                            if "role" in field_name:
                                example_data[field["name"]] = [1, 2]
                            else:
                                example_data[field["name"]] = []
                        elif "str" in field_type:
                            if "desc" in field_name or "description" in field_name:
                                example_data[field["name"]] = "描述信息"
                            elif "path" in field_name:
                                example_data[field["name"]] = "/api/v1/example"
                            elif "method" in field_name:
                                example_data[field["name"]] = "GET"
                            elif "tag" in field_name:
                                example_data[field["name"]] = "示例模块"
                            else:
                                example_data[field["name"]] = "示例文本"
                        else:
                            example_data[field["name"]] = "value"

                if example_data:
                    curl_cmd += (
                        f" \\\n  -d '{json.dumps(example_data, ensure_ascii=False)}'"
                    )
                else:
                    curl_cmd += ' \\\n  -d \'{"key": "value"}\''

        content += curl_cmd + "\n```\n\n"

        # Python 示例
        content += "**Python (requests)**:\n```python\n"
        content += "import requests\n\n"

        if module_name != "base":
            content += "headers = {\n"
            content += '    "Authorization": "Bearer <your-token>"\n'
            content += "}\n\n"

        if method == "GET":
            if query_params:
                content += "params = {\n"
                for param in query_params[:3]:  # 只显示前3个参数作为示例
                    if param.get("example"):
                        content += f'    "{param["name"]}": "{param["example"]}",\n'
                    elif param["required"]:
                        content += f'    "{param["name"]}": "...",\n'
                content += "}\n\n"
                content += "response = requests.get(\n"
                content += f'    "http://localhost:8000{route_details["path"]}",\n'
                if module_name != "base":
                    content += "    headers=headers,\n"
                content += "    params=params\n"
                content += ")\n"
            else:
                content += "response = requests.get(\n"
                content += f'    "http://localhost:8000{route_details["path"]}"'
                if module_name != "base":
                    content += ",\n    headers=headers"
                content += "\n)\n"

        elif method in ["POST", "PUT", "PATCH"]:
            if route_details.get("request_body") and route_details["request_body"].get(
                "model_fields"
            ):
                content += "data = {\n"
                example_count = 0
                for field in route_details["request_body"]["model_fields"]:
                    if example_count >= 5:  # 限制显示数量
                        break

                    if field.get("example") is not None:
                        if isinstance(field["example"], str):
                            content += f'    "{field["name"]}": "{field["example"]}",\n'
                        else:
                            content += f'    "{field["name"]}": {json.dumps(field["example"])},\n'
                        example_count += 1
                    elif field["required"]:
                        # 生成真实示例数据
                        field_name = field["name"].lower()
                        field_type = field["type"].lower()

                        if "email" in field_name:
                            content += f'    "{field["name"]}": "admin@example.com",\n'
                        elif "username" in field_name or "name" == field_name:
                            content += f'    "{field["name"]}": "admin",\n'
                        elif "password" in field_name:
                            content += f'    "{field["name"]}": "password123",\n'
                        elif "id" in field_name and "int" in field_type:
                            content += f'    "{field["name"]}": 1,\n'
                        elif "bool" in field_type:
                            content += f'    "{field["name"]}": True,\n'
                        elif "list" in field_type:
                            if "role" in field_name:
                                content += f'    "{field["name"]}": [1, 2],\n'
                            else:
                                content += f'    "{field["name"]}": [],\n'
                        elif "str" in field_type:
                            if "desc" in field_name or "description" in field_name:
                                content += f'    "{field["name"]}": "描述信息",\n'
                            elif "path" in field_name:
                                content += (
                                    f'    "{field["name"]}": "/api/v1/example",\n'
                                )
                            elif "method" in field_name:
                                content += f'    "{field["name"]}": "GET",\n'
                            elif "tag" in field_name:
                                content += f'    "{field["name"]}": "示例模块",\n'
                            else:
                                content += f'    "{field["name"]}": "示例文本",\n'
                        else:
                            content += f'    "{field["name"]}": "value",\n'
                        example_count += 1
                content += "}\n\n"

            content += f"response = requests.{method.lower()}(\n"
            content += f'    "http://localhost:8000{route_details["path"]}",\n'
            if module_name != "base":
                content += "    headers=headers,\n"
            if route_details.get("request_body"):
                content += "    json=data\n"
            content += ")\n"

        elif method == "DELETE":
            content += "response = requests.delete(\n"
            content += f'    "http://localhost:8000{route_details["path"]}"'
            if module_name != "base":
                content += ",\n    headers=headers"
            content += "\n)\n"

        content += "\nprint(response.json())\n"
        content += "```\n\n"

        # 添加分隔线
        content += "---\n\n"

    return content


def extract_route_info(app: FastAPI) -> dict[str, list[Any]]:
    """提取路由信息，返回原始的APIRoute对象"""
    if app is None:
        return {}

    routes_info = {}

    for route in app.routes:
        if isinstance(route, APIRoute):
            # 提取路径的模块信息
            path_parts = route.path.split("/")
            if (
                len(path_parts) >= 4
                and path_parts[1] == "api"
                and path_parts[2] == "v1"
            ):
                module = path_parts[3]

                if module not in routes_info:
                    routes_info[module] = []

                # 直接保存APIRoute对象
                routes_info[module].append(route)

    return routes_info


def generate_api_index() -> str:
    """生成API索引页面"""
    return """# API 文档

## 概述

这里是FastAPI后端模板的完整API文档。所有API都遵循RESTful设计原则，使用JSON格式进行数据交换。

## 认证

大部分API需要JWT认证。请先通过登录接口获取访问令牌，然后在请求头中包含：

```
Authorization: Bearer <your-access-token>
```

## 响应格式

所有API响应都遵循统一的格式：

### 成功响应
```json
{
  "code": 200,
  "msg": "success",
  "data": {...}
}
```

### 错误响应
```json
{
  "code": 400,
  "msg": "error message",
  "data": null
}
```

### 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 422 | 参数验证失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

## API 模块

- [认证授权](base.md) - 用户登录、token刷新等
- [用户管理](users.md) - 用户CRUD操作
- [角色管理](role.md) - 角色权限管理
- [菜单管理](menu.md) - 系统菜单配置
- [文件管理](files.md) - 文件上传下载
- [部门管理](dept.md) - 组织架构管理
- [API权限](api.md) - API权限控制
- [审计日志](auditlog.md) - 操作日志记录

## 在线测试

启动服务后，您可以通过以下地址访问交互式API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 请求限制

- 文件上传大小限制：10MB
- 登录尝试限制：5次/分钟
- Token刷新限制：10次/分钟
- API请求频率：根据具体接口而定

## 健康检查

- **健康状态**: `GET /api/v1/base/health`
- **版本信息**: `GET /api/v1/base/version`
"""


def main():
    """主函数"""
    print("正在生成API文档...")

    # 生成API索引页面
    with mkdocs_gen_files.open("api/index.md", "w") as f:
        f.write(generate_api_index())

    # 如果应用可用，生成详细文档
    if app is not None:
        try:
            # 提取路由信息
            routes_info = extract_route_info(app)

            # 为每个模块生成文档
            for module_name, routes in routes_info.items():
                file_name = f"api/{module_name}.md"
                content = generate_module_doc(module_name, routes)

                with mkdocs_gen_files.open(file_name, "w") as f:
                    f.write(content)

                print(f"已生成: {file_name}")

            # 生成OpenAPI规范文件
            openapi_schema = get_openapi_schema(app)
            if openapi_schema:
                with mkdocs_gen_files.open("api/openapi.json", "w") as f:
                    json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
                print("已生成: api/openapi.json")

            print(f"API文档生成完成！共生成 {len(routes_info)} 个模块文档")

        except Exception as e:
            print(f"生成API文档时出错: {e}")
            import traceback

            traceback.print_exc()
            print("将生成基础文档结构...")

            # 生成基础文档结构
            basic_modules = [
                "base",
                "users",
                "role",
                "menu",
                "files",
                "dept",
                "api",
                "auditlog",
            ]

            for module in basic_modules:
                file_name = f"api/{module}.md"
                content = f"""# {module.title()} API

## 概述

{module.title()}相关的API接口文档。

!!! note "注意"
    请启动FastAPI应用后重新生成文档以获取完整的API信息。

## 快速开始

```bash
# 启动应用
uv run uvicorn src:app --reload

# 访问交互式文档
open http://localhost:8000/docs
```
"""

                with mkdocs_gen_files.open(file_name, "w") as f:
                    f.write(content)

                print(f"已生成基础文档: {file_name}")

    else:
        print("FastAPI应用不可用，生成基础文档结构...")

        # 生成基础文档结构
        basic_modules = [
            "base",
            "users",
            "role",
            "menu",
            "files",
            "dept",
            "api",
            "auditlog",
        ]

        for module in basic_modules:
            file_name = f"api/{module}.md"
            content = f"""# {module.title()} API

## 概述

{module.title()}相关的API接口文档。

!!! note "注意"
    请启动FastAPI应用后重新生成文档以获取完整的API信息。

## 快速开始

```bash
# 启动应用
uv run uvicorn src:app --reload

# 访问交互式文档
open http://localhost:8000/docs
```
"""

            with mkdocs_gen_files.open(file_name, "w") as f:
                f.write(content)

            print(f"已生成基础文档: {file_name}")


def get_openapi_schema(app: FastAPI) -> dict:
    """获取OpenAPI模式"""
    if app is None:
        return {}

    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )


if __name__ == "__main__":
    main()
