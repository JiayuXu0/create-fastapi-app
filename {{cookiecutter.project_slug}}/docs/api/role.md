# 角色管理 API

## 概述

角色管理相关的API接口文档。

## 查看角色列表

- **路径**: `/api/v1/role/list`
- **方法**: `GET`
- **标签**: 角色模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| page | `<class 'int'>` | query | 否 | 页码 | 1 |
| page_size | `<class 'int'>` | query | 否 | 每页数量 | 10 |
| role_name | `<class 'str'>` | query | 否 | 角色名称，用于查询 |  |

### 响应

**成功响应**:

- **状态码**: `200`
- **Content-Type**: `application/json`

```json
{
  "code": 200,
  "msg": "success",
  "data": ...
}
```

**错误响应**:

- **状态码**: `400` / `401` / `403` / `404` / `500`

```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

### 使用示例

**cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/role/list" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

params = {
}

response = requests.get(
    "http://localhost:8000/api/v1/role/list",
    headers=headers,
    params=params
)

print(response.json())
```

---

## 查看角色

- **路径**: `/api/v1/role/get`
- **方法**: `GET`
- **标签**: 角色模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| role_id | `<class 'int'>` | query | 否 | 角色ID | PydanticUndefined |

### 响应

**成功响应**:

- **状态码**: `200`
- **Content-Type**: `application/json`

```json
{
  "code": 200,
  "msg": "success",
  "data": ...
}
```

**错误响应**:

- **状态码**: `400` / `401` / `403` / `404` / `500`

```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

### 使用示例

**cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/role/get" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

params = {
}

response = requests.get(
    "http://localhost:8000/api/v1/role/get",
    headers=headers,
    params=params
)

print(response.json())
```

---

## 创建角色

- **路径**: `/api/v1/role/create`
- **方法**: `POST`
- **标签**: 角色模块

### 请求体

**Content-Type**: `application/json`

**模型**: `RoleCreate`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| name | `<class 'str'>` | 是 |  | None |  |
| desc | `<class 'str'>` | 否 |  | None |  |

**请求示例**:

```json
{
  "name": "admin"
}
```

### 响应

**成功响应**:

- **状态码**: `200`
- **Content-Type**: `application/json`

```json
{
  "code": 200,
  "msg": "success",
  "data": ...
}
```

**错误响应**:

- **状态码**: `400` / `401` / `403` / `404` / `500`

```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

### 使用示例

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/role/create" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "admin"}'
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

data = {
    "name": "admin",
}

response = requests.post(
    "http://localhost:8000/api/v1/role/create",
    headers=headers,
    json=data
)

print(response.json())
```

---

## 更新角色

- **路径**: `/api/v1/role/update`
- **方法**: `POST`
- **标签**: 角色模块

### 请求体

**Content-Type**: `application/json`

**模型**: `RoleUpdate`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| id | `<class 'int'>` | 是 |  | None |  |
| name | `<class 'str'>` | 是 |  | None |  |
| desc | `<class 'str'>` | 否 |  | None |  |

**请求示例**:

```json
{
  "id": 1,
  "name": "admin"
}
```

### 响应

**成功响应**:

- **状态码**: `200`
- **Content-Type**: `application/json`

```json
{
  "code": 200,
  "msg": "success",
  "data": ...
}
```

**错误响应**:

- **状态码**: `400` / `401` / `403` / `404` / `500`

```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

### 使用示例

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/role/update" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "admin"}'
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

data = {
    "id": 1,
    "name": "admin",
}

response = requests.post(
    "http://localhost:8000/api/v1/role/update",
    headers=headers,
    json=data
)

print(response.json())
```

---

## 删除角色

- **路径**: `/api/v1/role/delete`
- **方法**: `DELETE`
- **标签**: 角色模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| role_id | `<class 'int'>` | query | 否 | 角色ID | PydanticUndefined |

### 响应

**成功响应**:

- **状态码**: `200`
- **Content-Type**: `application/json`

```json
{
  "code": 200,
  "msg": "success",
  "data": ...
}
```

**错误响应**:

- **状态码**: `400` / `401` / `403` / `404` / `500`

```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

### 使用示例

**cURL**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/role/delete" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

response = requests.delete(
    "http://localhost:8000/api/v1/role/delete",
    headers=headers
)

print(response.json())
```

---

## 查看角色权限

- **路径**: `/api/v1/role/authorized`
- **方法**: `GET`
- **标签**: 角色模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| id | `<class 'int'>` | query | 否 | 角色ID | PydanticUndefined |

### 响应

**成功响应**:

- **状态码**: `200`
- **Content-Type**: `application/json`

```json
{
  "code": 200,
  "msg": "success",
  "data": ...
}
```

**错误响应**:

- **状态码**: `400` / `401` / `403` / `404` / `500`

```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

### 使用示例

**cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/role/authorized" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

params = {
}

response = requests.get(
    "http://localhost:8000/api/v1/role/authorized",
    headers=headers,
    params=params
)

print(response.json())
```

---

## 更新角色权限

- **路径**: `/api/v1/role/authorized`
- **方法**: `POST`
- **标签**: 角色模块

### 请求体

**Content-Type**: `application/json`

**模型**: `RoleUpdateMenusApis`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| id | `<class 'int'>` | 是 |  | None |  |
| menu_ids | `list[int]` | 否 |  | None |  |
| api_infos | `list[dict]` | 否 |  | None |  |

**请求示例**:

```json
{
  "id": 1
}
```

### 响应

**成功响应**:

- **状态码**: `200`
- **Content-Type**: `application/json`

```json
{
  "code": 200,
  "msg": "success",
  "data": ...
}
```

**错误响应**:

- **状态码**: `400` / `401` / `403` / `404` / `500`

```json
{
  "code": 400,
  "msg": "错误信息",
  "data": null
}
```

### 使用示例

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/role/authorized" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

data = {
    "id": 1,
}

response = requests.post(
    "http://localhost:8000/api/v1/role/authorized",
    headers=headers,
    json=data
)

print(response.json())
```

---

