# 用户管理 API

## 概述

用户管理相关的API接口文档。

## 查看用户列表

- **路径**: `/api/v1/users/list`
- **方法**: `GET`
- **标签**: 用户模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| page | `<class 'int'>` | query | 否 | 页码 | 1 |
| page_size | `<class 'int'>` | query | 否 | 每页数量 | 10 |
| username | `<class 'str'>` | query | 否 | 用户名称，用于搜索 |  |
| email | `<class 'str'>` | query | 否 | 邮箱地址 |  |
| dept_id | `<class 'int'>` | query | 否 | 部门ID | null |

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
curl -X GET "http://localhost:8000/api/v1/users/list" \
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
    "http://localhost:8000/api/v1/users/list",
    headers=headers,
    params=params
)

print(response.json())
```

---

## 查看用户

- **路径**: `/api/v1/users/get`
- **方法**: `GET`
- **标签**: 用户模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| user_id | `<class 'int'>` | query | 否 | 用户ID | PydanticUndefined |

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
curl -X GET "http://localhost:8000/api/v1/users/get" \
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
    "http://localhost:8000/api/v1/users/get",
    headers=headers,
    params=params
)

print(response.json())
```

---

## 创建用户

- **路径**: `/api/v1/users/create`
- **方法**: `POST`
- **标签**: 用户模块

### 请求体

**Content-Type**: `application/json`

**模型**: `UserCreate`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| email | `<class 'pydantic.networks.EmailStr'>` | 是 |  | None |  |
| username | `<class 'str'>` | 是 | 用户名（3-20位字母数字下划线） | None |  |
| password | `<class 'str'>` | 是 | 密码（至少8位，包含字母和数字） | None |  |
| is_active | `bool | None` | 否 |  | None |  |
| is_superuser | `bool | None` | 否 |  | None |  |
| role_ids | `list[int] | None` | 否 |  | None |  |
| dept_id | `int | None` | 否 | 部门ID | None |  |

**请求示例**:

```json
{
  "email": "admin@example.com",
  "username": "admin",
  "password": "password123"
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
curl -X POST "http://localhost:8000/api/v1/users/create" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "username": "admin", "password": "password123"}'
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

data = {
    "email": "admin@example.com",
    "username": "admin",
    "password": "password123",
}

response = requests.post(
    "http://localhost:8000/api/v1/users/create",
    headers=headers,
    json=data
)

print(response.json())
```

---

## 更新用户

- **路径**: `/api/v1/users/update`
- **方法**: `POST`
- **标签**: 用户模块

### 请求体

**Content-Type**: `application/json`

**模型**: `UserUpdate`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| id | `<class 'int'>` | 是 |  | None |  |
| email | `<class 'pydantic.networks.EmailStr'>` | 是 |  | None |  |
| username | `<class 'str'>` | 是 |  | None |  |
| is_active | `bool | None` | 否 |  | None |  |
| is_superuser | `bool | None` | 否 |  | None |  |
| role_ids | `list[int] | None` | 否 |  | None |  |
| dept_id | `int | None` | 否 |  | None |  |

**请求示例**:

```json
{
  "id": 1,
  "email": "admin@example.com",
  "username": "admin"
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
curl -X POST "http://localhost:8000/api/v1/users/update" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "email": "admin@example.com", "username": "admin"}'
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

data = {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin",
}

response = requests.post(
    "http://localhost:8000/api/v1/users/update",
    headers=headers,
    json=data
)

print(response.json())
```

---

## 删除用户

- **路径**: `/api/v1/users/delete`
- **方法**: `DELETE`
- **标签**: 用户模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| user_id | `<class 'int'>` | query | 否 | 用户ID | PydanticUndefined |

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
curl -X DELETE "http://localhost:8000/api/v1/users/delete" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

response = requests.delete(
    "http://localhost:8000/api/v1/users/delete",
    headers=headers
)

print(response.json())
```

---

## 重置密码

- **路径**: `/api/v1/users/reset_password`
- **方法**: `POST`
- **标签**: 用户模块

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
curl -X POST "http://localhost:8000/api/v1/users/reset_password" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

response = requests.post(
    "http://localhost:8000/api/v1/users/reset_password",
    headers=headers,
)

print(response.json())
```

---

