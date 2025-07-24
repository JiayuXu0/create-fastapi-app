# API权限 API

## 概述

API权限相关的API接口文档。

## 查看API列表

- **路径**: `/api/v1/api/list`
- **方法**: `GET`
- **标签**: API模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| page | `<class 'int'>` | query | 否 | 页码 | 1 |
| page_size | `<class 'int'>` | query | 否 | 每页数量 | 10 |
| path | `<class 'str'>` | query | 否 | API路径 | null |
| summary | `<class 'str'>` | query | 否 | API简介 | null |
| tags | `<class 'str'>` | query | 否 | API模块 | null |

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
curl -X GET "http://localhost:8000/api/v1/api/list" \
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
    "http://localhost:8000/api/v1/api/list",
    headers=headers,
    params=params
)

print(response.json())
```

---

## 查看Api

- **路径**: `/api/v1/api/get`
- **方法**: `GET`
- **标签**: API模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| id | `<class 'int'>` | query | 否 | Api | PydanticUndefined |

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
curl -X GET "http://localhost:8000/api/v1/api/get" \
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
    "http://localhost:8000/api/v1/api/get",
    headers=headers,
    params=params
)

print(response.json())
```

---

## 创建Api

- **路径**: `/api/v1/api/create`
- **方法**: `POST`
- **标签**: API模块

### 请求体

**Content-Type**: `application/json`

**模型**: `ApiCreate`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| path | `<class 'str'>` | 是 | API路径 | None |  |
| summary | `<class 'str'>` | 否 | API简介 | None |  |
| method | `<enum 'MethodType'>` | 是 | API方法 | None |  |
| tags | `<class 'str'>` | 是 | API标签 | None |  |

**请求示例**:

```json
{
  "path": "/api/v1/example",
  "method": null,
  "tags": "示例模块"
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
curl -X POST "http://localhost:8000/api/v1/api/create" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"path": "/api/v1/example", "method": "value", "tags": "示例模块"}'
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

data = {
    "path": "/api/v1/example",
    "method": "value",
    "tags": "示例模块",
}

response = requests.post(
    "http://localhost:8000/api/v1/api/create",
    headers=headers,
    json=data
)

print(response.json())
```

---

## 更新Api

- **路径**: `/api/v1/api/update`
- **方法**: `POST`
- **标签**: API模块

### 请求体

**Content-Type**: `application/json`

**模型**: `ApiUpdate`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| path | `<class 'str'>` | 是 | API路径 | None |  |
| summary | `<class 'str'>` | 否 | API简介 | None |  |
| method | `<enum 'MethodType'>` | 是 | API方法 | None |  |
| tags | `<class 'str'>` | 是 | API标签 | None |  |
| id | `<class 'int'>` | 是 |  | None |  |

**请求示例**:

```json
{
  "path": "/api/v1/example",
  "method": null,
  "tags": "示例模块",
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
curl -X POST "http://localhost:8000/api/v1/api/update" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"path": "/api/v1/example", "method": "value", "tags": "示例模块", "id": 1}'
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

data = {
    "path": "/api/v1/example",
    "method": "value",
    "tags": "示例模块",
    "id": 1,
}

response = requests.post(
    "http://localhost:8000/api/v1/api/update",
    headers=headers,
    json=data
)

print(response.json())
```

---

## 删除Api

- **路径**: `/api/v1/api/delete`
- **方法**: `DELETE`
- **标签**: API模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| api_id | `<class 'int'>` | query | 否 | ApiID | PydanticUndefined |

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
curl -X DELETE "http://localhost:8000/api/v1/api/delete" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

response = requests.delete(
    "http://localhost:8000/api/v1/api/delete",
    headers=headers
)

print(response.json())
```

---

## 刷新API列表

- **路径**: `/api/v1/api/refresh`
- **方法**: `POST`
- **标签**: API模块

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
curl -X POST "http://localhost:8000/api/v1/api/refresh" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

response = requests.post(
    "http://localhost:8000/api/v1/api/refresh",
    headers=headers,
)

print(response.json())
```

---

