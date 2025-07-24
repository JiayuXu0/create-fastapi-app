# 认证授权 API

## 概述

认证授权相关的API接口文档。

## 获取token

- **路径**: `/api/v1/base/access_token`
- **方法**: `POST`
- **标签**: 基础模块

### 请求体

**Content-Type**: `application/json`

**模型**: `CredentialsSchema`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| username | `<class 'str'>` | 是 | 用户名称 | None |  |
| password | `<class 'str'>` | 是 | 密码 | None |  |

**请求示例**:

```json
{
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
curl -X POST "http://localhost:8000/api/v1/base/access_token" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'
```

**Python (requests)**:
```python
import requests

data = {
    "username": "admin",
    "password": "password123",
}

response = requests.post(
    "http://localhost:8000/api/v1/base/access_token",
    json=data
)

print(response.json())
```

---

## 刷新token

- **路径**: `/api/v1/base/refresh_token`
- **方法**: `POST`
- **标签**: 基础模块

### 描述

使用刷新令牌获取新的访问令牌和刷新令牌

### 请求体

**Content-Type**: `application/json`

**模型**: `RefreshTokenRequest`

| 字段名 | 类型 | 必填 | 描述 | 示例 | 约束 |
|--------|------|------|------|------|------|
| refresh_token | `<class 'str'>` | 是 | 刷新令牌 | None |  |

**请求示例**:

```json
{
  "refresh_token": "示例文本"
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
curl -X POST "http://localhost:8000/api/v1/base/refresh_token" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "示例文本"}'
```

**Python (requests)**:
```python
import requests

data = {
    "refresh_token": "示例文本",
}

response = requests.post(
    "http://localhost:8000/api/v1/base/refresh_token",
    json=data
)

print(response.json())
```

---

## 查看用户信息

- **路径**: `/api/v1/base/userinfo`
- **方法**: `GET`
- **标签**: 基础模块

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| current_user | `<class 'models.admin.User'>` | query | 否 |  | Depends(is_authed) |

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
curl -X GET "http://localhost:8000/api/v1/base/userinfo"
```

**Python (requests)**:
```python
import requests

params = {
}

response = requests.get(
    "http://localhost:8000/api/v1/base/userinfo",
    params=params
)

print(response.json())
```

---

## 健康检查

- **路径**: `/api/v1/base/health`
- **方法**: `GET`
- **标签**: 基础模块

### 描述

系统健康检查

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
curl -X GET "http://localhost:8000/api/v1/base/health"
```

**Python (requests)**:
```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/base/health"
)

print(response.json())
```

---

## 版本信息

- **路径**: `/api/v1/base/version`
- **方法**: `GET`
- **标签**: 基础模块

### 描述

获取API版本信息

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
curl -X GET "http://localhost:8000/api/v1/base/version"
```

**Python (requests)**:
```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/base/version"
)

print(response.json())
```

---

