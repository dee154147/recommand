# 第一阶段API接口文档

## 文档信息
- **创建时间**: 2024年12月20日
- **版本**: v1.0
- **用途**: 系统API接口的完整文档，供前后端开发对接使用

---

## 1. API概览

### 1.1 基础信息
- **基础URL**: `http://localhost:5000/api/v1`
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8

### 1.2 响应格式标准
```json
{
  "success": true,
  "data": {},
  "message": "操作成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 1.3 错误响应格式
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "参数验证失败",
    "details": {}
  },
  "code": 400,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 1.4 HTTP状态码
- `200` - 请求成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权
- `403` - 禁止访问
- `404` - 资源不存在
- `500` - 服务器内部错误

---

## 2. 商品管理接口

### 2.1 获取商品列表
**接口**: `GET /api/v1/products`

**请求参数**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| per_page | integer | 否 | 20 | 每页数量 |
| category_id | integer | 否 | - | 分类ID |
| search | string | 否 | - | 搜索关键词 |
| sort | string | 否 | created_at_desc | 排序方式 |
| min_price | float | 否 | - | 最低价格 |
| max_price | float | 否 | - | 最高价格 |

**排序方式选项**:
- `created_at_desc` - 创建时间降序
- `created_at_asc` - 创建时间升序
- `price_desc` - 价格降序
- `price_asc` - 价格升序
- `name_asc` - 名称升序

**响应示例**:
```json
{
  "success": true,
  "data": {
    "products": [
      {
        "id": 1,
        "name": "智能手机",
        "description": "高性能智能手机",
        "price": 2999.00,
        "category_id": 1,
        "category_name": "电子产品",
        "image_url": "https://example.com/image.jpg",
        "tags": ["手机", "智能", "高性能"],
        "created_at": "2024-12-20T10:30:00Z",
        "updated_at": "2024-12-20T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5
    }
  },
  "message": "获取商品列表成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 2.2 获取单个商品详情
**接口**: `GET /api/v1/products/{id}`

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 商品ID |

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "智能手机",
    "description": "高性能智能手机，配备最新处理器",
    "price": 2999.00,
    "category_id": 1,
    "category_name": "电子产品",
    "image_url": "https://example.com/image.jpg",
    "tags": ["手机", "智能", "高性能"],
    "created_at": "2024-12-20T10:30:00Z",
    "updated_at": "2024-12-20T10:30:00Z",
    "similar_products": [
      {
        "id": 2,
        "name": "平板电脑",
        "price": 1999.00,
        "image_url": "https://example.com/tablet.jpg"
      }
    ]
  },
  "message": "获取商品详情成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 2.3 创建商品
**接口**: `POST /api/v1/products`

**请求体**:
```json
{
  "name": "智能手机",
  "description": "高性能智能手机",
  "price": 2999.00,
  "category_id": 1,
  "image_url": "https://example.com/image.jpg",
  "tags": ["手机", "智能", "高性能"]
}
```

**字段验证**:
- `name`: 必填，字符串，长度1-200字符
- `description`: 可选，字符串，最大1000字符
- `price`: 必填，数字，大于0
- `category_id`: 必填，整数，必须存在
- `image_url`: 可选，字符串，有效URL格式
- `tags`: 可选，字符串数组，每个标签长度1-50字符

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "智能手机",
    "description": "高性能智能手机",
    "price": 2999.00,
    "category_id": 1,
    "image_url": "https://example.com/image.jpg",
    "tags": ["手机", "智能", "高性能"],
    "created_at": "2024-12-20T10:30:00Z",
    "updated_at": "2024-12-20T10:30:00Z"
  },
  "message": "商品创建成功",
  "code": 201,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 2.4 更新商品
**接口**: `PUT /api/v1/products/{id}`

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 商品ID |

**请求体**: 与创建商品相同，所有字段可选

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "智能手机 Pro",
    "description": "高性能智能手机 Pro版本",
    "price": 3999.00,
    "category_id": 1,
    "image_url": "https://example.com/image-pro.jpg",
    "tags": ["手机", "智能", "高性能", "Pro"],
    "created_at": "2024-12-20T10:30:00Z",
    "updated_at": "2024-12-20T10:35:00Z"
  },
  "message": "商品更新成功",
  "code": 200,
  "timestamp": "2024-12-20T10:35:00Z"
}
```

### 2.5 删除商品
**接口**: `DELETE /api/v1/products/{id}`

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 商品ID |

**响应示例**:
```json
{
  "success": true,
  "data": null,
  "message": "商品删除成功",
  "code": 200,
  "timestamp": "2024-12-20T10:35:00Z"
}
```

---

## 3. 分类管理接口

### 3.1 获取分类列表
**接口**: `GET /api/v1/categories`

**请求参数**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| parent_id | integer | 否 | null | 父分类ID |
| include_children | boolean | 否 | false | 是否包含子分类 |

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "电子产品",
      "description": "各类电子产品",
      "parent_id": null,
      "created_at": "2024-12-20T10:30:00Z",
      "children": [
        {
          "id": 2,
          "name": "手机",
          "description": "智能手机",
          "parent_id": 1,
          "created_at": "2024-12-20T10:30:00Z"
        }
      ]
    }
  ],
  "message": "获取分类列表成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 3.2 获取分类树
**接口**: `GET /api/v1/categories/tree`

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "电子产品",
      "description": "各类电子产品",
      "parent_id": null,
      "created_at": "2024-12-20T10:30:00Z",
      "children": [
        {
          "id": 2,
          "name": "手机",
          "description": "智能手机",
          "parent_id": 1,
          "created_at": "2024-12-20T10:30:00Z",
          "children": []
        },
        {
          "id": 3,
          "name": "电脑",
          "description": "各类电脑",
          "parent_id": 1,
          "created_at": "2024-12-20T10:30:00Z",
          "children": []
        }
      ]
    }
  ],
  "message": "获取分类树成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 3.3 创建分类
**接口**: `POST /api/v1/categories`

**请求体**:
```json
{
  "name": "电子产品",
  "description": "各类电子产品",
  "parent_id": null
}
```

**字段验证**:
- `name`: 必填，字符串，长度1-100字符，唯一
- `description`: 可选，字符串，最大500字符
- `parent_id`: 可选，整数，必须存在或为null

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "电子产品",
    "description": "各类电子产品",
    "parent_id": null,
    "created_at": "2024-12-20T10:30:00Z"
  },
  "message": "分类创建成功",
  "code": 201,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

---

## 4. 用户管理接口

### 4.1 用户注册
**接口**: `POST /api/v1/users/register`

**请求体**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

**字段验证**:
- `username`: 必填，字符串，长度3-80字符，唯一
- `email`: 必填，字符串，有效邮箱格式，唯一
- `password`: 必填，字符串，长度6-128字符

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-12-20T10:30:00Z"
  },
  "message": "用户注册成功",
  "code": 201,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 4.2 用户登录
**接口**: `POST /api/v1/users/login`

**请求体**:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "created_at": "2024-12-20T10:30:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  },
  "message": "登录成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 4.3 获取用户信息
**接口**: `GET /api/v1/users/profile`

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "profile": {
      "preferences": {},
      "interests": []
    },
    "created_at": "2024-12-20T10:30:00Z",
    "last_login": "2024-12-20T10:30:00Z"
  },
  "message": "获取用户信息成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 4.4 更新用户信息
**接口**: `PUT /api/v1/users/profile`

**请求头**:
```
Authorization: Bearer <token>
```

**请求体**:
```json
{
  "email": "newemail@example.com",
  "profile": {
    "preferences": {
      "theme": "dark",
      "language": "zh-CN"
    },
    "interests": ["电子产品", "运动"]
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "newemail@example.com",
    "profile": {
      "preferences": {
        "theme": "dark",
        "language": "zh-CN"
      },
      "interests": ["电子产品", "运动"]
    },
    "created_at": "2024-12-20T10:30:00Z",
    "updated_at": "2024-12-20T10:35:00Z"
  },
  "message": "用户信息更新成功",
  "code": 200,
  "timestamp": "2024-12-20T10:35:00Z"
}
```

---

## 5. 推荐系统接口

### 5.1 获取推荐商品
**接口**: `GET /api/v1/recommendations`

**请求参数**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| user_id | integer | 是 | - | 用户ID |
| algorithm | string | 否 | hybrid | 推荐算法 |
| limit | integer | 否 | 10 | 推荐数量 |
| category_id | integer | 否 | - | 分类过滤 |

**推荐算法选项**:
- `content_based` - 基于内容的推荐
- `collaborative` - 协同过滤推荐
- `hybrid` - 混合推荐算法

**响应示例**:
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "product": {
          "id": 1,
          "name": "智能手机",
          "price": 2999.00,
          "image_url": "https://example.com/image.jpg",
          "category_name": "电子产品"
        },
        "score": 0.95,
        "reason": "基于您的浏览历史和偏好推荐"
      }
    ],
    "algorithm": "hybrid",
    "total": 10,
    "user_id": 1
  },
  "message": "获取推荐成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 5.2 记录用户交互
**接口**: `POST /api/v1/interactions`

**请求体**:
```json
{
  "user_id": 1,
  "product_id": 1,
  "interaction_type": "view",
  "rating": 4.5,
  "duration": 30
}
```

**字段验证**:
- `user_id`: 必填，整数，必须存在
- `product_id`: 必填，整数，必须存在
- `interaction_type`: 必填，字符串，枚举值
- `rating`: 可选，浮点数，范围1-5
- `duration`: 可选，整数，大于0

**交互类型选项**:
- `view` - 浏览
- `like` - 点赞
- `purchase` - 购买
- `share` - 分享
- `search` - 搜索

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 1,
    "product_id": 1,
    "interaction_type": "view",
    "rating": 4.5,
    "duration": 30,
    "created_at": "2024-12-20T10:30:00Z"
  },
  "message": "交互记录成功",
  "code": 201,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 5.3 获取用户交互历史
**接口**: `GET /api/v1/users/{user_id}/interactions`

**路径参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | integer | 是 | 用户ID |

**请求参数**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| per_page | integer | 否 | 20 | 每页数量 |
| interaction_type | string | 否 | - | 交互类型过滤 |
| start_date | string | 否 | - | 开始日期 |
| end_date | string | 否 | - | 结束日期 |

**响应示例**:
```json
{
  "success": true,
  "data": {
    "interactions": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "智能手机",
          "price": 2999.00,
          "image_url": "https://example.com/image.jpg"
        },
        "interaction_type": "view",
        "rating": 4.5,
        "duration": 30,
        "created_at": "2024-12-20T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 50,
      "pages": 3
    }
  },
  "message": "获取交互历史成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

---

## 6. 搜索接口

### 6.1 商品搜索
**接口**: `GET /api/v1/search/products`

**请求参数**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| q | string | 是 | - | 搜索关键词 |
| page | integer | 否 | 1 | 页码 |
| per_page | integer | 否 | 20 | 每页数量 |
| category_id | integer | 否 | - | 分类过滤 |
| min_price | float | 否 | - | 最低价格 |
| max_price | float | 否 | - | 最高价格 |
| sort | string | 否 | relevance | 排序方式 |

**排序方式选项**:
- `relevance` - 相关性排序
- `price_asc` - 价格升序
- `price_desc` - 价格降序
- `created_at_desc` - 创建时间降序

**响应示例**:
```json
{
  "success": true,
  "data": {
    "products": [
      {
        "id": 1,
        "name": "智能手机",
        "description": "高性能智能手机",
        "price": 2999.00,
        "category_name": "电子产品",
        "image_url": "https://example.com/image.jpg",
        "relevance_score": 0.95
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 25,
      "pages": 2
    },
    "search_info": {
      "query": "手机",
      "total_results": 25,
      "search_time": 0.05
    }
  },
  "message": "搜索成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

---

## 7. 统计分析接口

### 7.1 获取商品统计
**接口**: `GET /api/v1/statistics/products`

**请求参数**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| period | string | 否 | 7d | 统计周期 |
| category_id | integer | 否 | - | 分类过滤 |

**统计周期选项**:
- `1d` - 1天
- `7d` - 7天
- `30d` - 30天
- `90d` - 90天

**响应示例**:
```json
{
  "success": true,
  "data": {
    "total_products": 1000,
    "new_products": 50,
    "category_distribution": [
      {
        "category_id": 1,
        "category_name": "电子产品",
        "count": 300,
        "percentage": 30.0
      }
    ],
    "price_statistics": {
      "min_price": 99.00,
      "max_price": 9999.00,
      "avg_price": 1299.50,
      "median_price": 899.00
    },
    "period": "7d"
  },
  "message": "获取统计成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

### 7.2 获取用户统计
**接口**: `GET /api/v1/statistics/users`

**请求参数**:
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| period | string | 否 | 7d | 统计周期 |

**响应示例**:
```json
{
  "success": true,
  "data": {
    "total_users": 5000,
    "new_users": 200,
    "active_users": 1200,
    "user_growth": [
      {
        "date": "2024-12-20",
        "new_users": 25,
        "active_users": 180
      }
    ],
    "period": "7d"
  },
  "message": "获取统计成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

---

## 8. 错误码说明

### 8.1 通用错误码
| 错误码 | HTTP状态码 | 说明 |
|--------|------------|------|
| SUCCESS | 200 | 操作成功 |
| CREATED | 201 | 创建成功 |
| VALIDATION_ERROR | 400 | 参数验证失败 |
| UNAUTHORIZED | 401 | 未授权 |
| FORBIDDEN | 403 | 禁止访问 |
| NOT_FOUND | 404 | 资源不存在 |
| CONFLICT | 409 | 资源冲突 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |

### 8.2 业务错误码
| 错误码 | 说明 |
|--------|------|
| USER_NOT_FOUND | 用户不存在 |
| PRODUCT_NOT_FOUND | 商品不存在 |
| CATEGORY_NOT_FOUND | 分类不存在 |
| INVALID_CREDENTIALS | 认证凭据无效 |
| EMAIL_ALREADY_EXISTS | 邮箱已存在 |
| USERNAME_ALREADY_EXISTS | 用户名已存在 |
| INSUFFICIENT_PERMISSIONS | 权限不足 |

---

## 9. 认证授权

### 9.1 JWT Token认证
系统使用JWT Token进行用户认证，Token包含以下信息：
- 用户ID
- 用户名
- 过期时间
- 签发时间

### 9.2 Token使用方式
```
Authorization: Bearer <token>
```

### 9.3 Token刷新
**接口**: `POST /api/v1/auth/refresh`

**请求头**:
```
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  },
  "message": "Token刷新成功",
  "code": 200,
  "timestamp": "2024-12-20T10:30:00Z"
}
```

---

## 10. 接口测试

### 10.1 测试工具推荐
- **Postman** - API测试和文档生成
- **curl** - 命令行测试工具
- **Insomnia** - API测试客户端

### 10.2 测试环境
- **开发环境**: `http://localhost:5000/api/v1`
- **测试环境**: `http://test.example.com/api/v1`
- **生产环境**: `https://api.example.com/api/v1`

### 10.3 测试数据
系统提供测试数据用于接口测试：
- 测试用户账号
- 测试商品数据
- 测试分类数据

---

## 11. 接口版本管理

### 11.1 版本策略
- 使用URL路径进行版本控制
- 当前版本：v1
- 向后兼容原则

### 11.2 版本升级
- 重大变更：创建新版本
- 向后兼容：保持旧版本
- 废弃通知：提前通知

---

## 12. 性能优化

### 12.1 缓存策略
- Redis缓存热点数据
- 商品列表缓存
- 用户推荐缓存

### 12.2 分页优化
- 默认分页大小：20
- 最大分页大小：100
- 游标分页支持

### 12.3 查询优化
- 数据库索引优化
- 查询条件优化
- 关联查询优化

---

*本文档包含了第一阶段系统的所有API接口，为前后端开发对接提供完整参考。接口设计遵循RESTful规范，支持完整的CRUD操作和业务功能。*
