# 文件管理 API

## 概述

文件管理相关的API接口文档。

## 上传文件

- **路径**: `/api/v1/files/upload`
- **方法**: `POST`
- **标签**: 上传文件

### 描述

通用文件上传

Args:
    file: 上传的文件

Returns:
    上传成功的响应，包含文件信息

### 请求参数

| 参数名 | 类型 | 位置 | 必填 | 描述 | 默认值 |
|--------|------|------|------|------|--------|
| file | `<class 'fastapi.datastructures.UploadFile'>` | query | 否 |  | annotation=UploadFile required=True alias='file' description='要上传的文件' json_schema_extra={} |

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
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer <your-token>"
```

**Python (requests)**:
```python
import requests

headers = {
    "Authorization": "Bearer <your-token>"
}

response = requests.post(
    "http://localhost:8000/api/v1/files/upload",
    headers=headers,
)

print(response.json())
```

---

