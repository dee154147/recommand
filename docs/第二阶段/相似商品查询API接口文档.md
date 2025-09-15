# 相似商品查询API接口文档

## 文档信息
- **项目名称**: 智能推荐系统
- **模块名称**: 相似商品查询API
- **文档版本**: v1.0
- **创建日期**: 2024年12月20日
- **最后更新**: 2024年12月20日
- **API版本**: v1.0

## 1. API概述

### 1.1 基础信息
- **Base URL**: `https://api.recommendation.com/v1`
- **协议**: HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8
- **认证方式**: Bearer Token (可选)

### 1.2 通用响应格式
```json
{
    "success": true,
    "data": {},
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": null
}
```

### 1.3 错误响应格式
```json
{
    "success": false,
    "data": null,
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": {
        "code": "PRODUCT_NOT_FOUND",
        "message": "Product not found",
        "details": "Product with ID 999 does not exist"
    }
}
```

## 2. 相似商品查询接口

### 2.1 获取相似商品

#### 2.1.1 接口信息
- **URL**: `/api/similar-products/{product_id}`
- **方法**: `GET`
- **描述**: 根据商品ID获取相似商品列表

#### 2.1.2 路径参数
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| product_id | integer | 是 | 目标商品ID |

#### 2.1.3 查询参数
| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| limit | integer | 否 | 12 | 返回商品数量 (1-20) |
| threshold | float | 否 | 0.75 | 相似度阈值 (0.0-1.0) |
| user_id | integer | 否 | null | 用户ID (用于个性化推荐) |
| include_metadata | boolean | 否 | false | 是否包含元数据 |

#### 2.1.4 请求示例
```bash
# 基础查询
GET /api/similar-products/123

# 带参数查询
GET /api/similar-products/123?limit=6&threshold=0.8&user_id=456

# 包含元数据
GET /api/similar-products/123?include_metadata=true
```

#### 2.1.5 响应示例
```json
{
    "success": true,
    "data": {
        "reference_product": {
            "id": 123,
            "name": "iPhone 15 Pro Max 256GB 深空黑色",
            "price": 9999.00,
            "image_url": "https://example.com/images/iphone15.jpg",
            "category": "智能手机",
            "brand": "苹果"
        },
        "similar_products": [
            {
                "id": 124,
                "name": "iPhone 15 Pro 128GB 自然钛色",
                "price": 8999.00,
                "image_url": "https://example.com/images/iphone15pro.jpg",
                "category": "智能手机",
                "brand": "苹果",
                "similarity_score": 0.95,
                "similarity_percentage": "95.0%"
            },
            {
                "id": 125,
                "name": "iPhone 14 Pro Max 256GB 深紫色",
                "price": 7999.00,
                "image_url": "https://example.com/images/iphone14.jpg",
                "category": "智能手机",
                "brand": "苹果",
                "similarity_score": 0.92,
                "similarity_percentage": "92.0%"
            }
        ],
        "query_info": {
            "product_id": 123,
            "result_count": 2,
            "threshold": 0.75,
            "algorithm_version": "v1.0",
            "response_time_ms": 150
        }
    },
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": null
}
```

#### 2.1.6 错误响应
```json
{
    "success": false,
    "data": null,
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": {
        "code": "PRODUCT_NOT_FOUND",
        "message": "Product not found",
        "details": "Product with ID 999 does not exist"
    }
}
```

### 2.2 批量获取相似商品

#### 2.2.1 接口信息
- **URL**: `/api/similar-products/batch`
- **方法**: `POST`
- **描述**: 批量获取多个商品的相似商品

#### 2.2.2 请求体
```json
{
    "product_ids": [123, 124, 125],
    "limit": 6,
    "threshold": 0.75,
    "user_id": 456
}
```

#### 2.2.3 请求参数
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| product_ids | array[integer] | 是 | 商品ID列表 (最多10个) |
| limit | integer | 否 | 每个商品返回的相似商品数量 |
| threshold | float | 否 | 相似度阈值 |
| user_id | integer | 否 | 用户ID |

#### 2.2.4 响应示例
```json
{
    "success": true,
    "data": {
        "results": {
            "123": {
                "reference_product": {...},
                "similar_products": [...]
            },
            "124": {
                "reference_product": {...},
                "similar_products": [...]
            }
        },
        "query_info": {
            "total_queries": 2,
            "successful_queries": 2,
            "failed_queries": 0,
            "response_time_ms": 300
        }
    },
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": null
}
```

## 3. 商品向量管理接口

### 3.1 更新商品向量

#### 3.1.1 接口信息
- **URL**: `/api/products/{product_id}/vector`
- **方法**: `POST`
- **描述**: 更新指定商品的向量嵌入

#### 3.1.2 路径参数
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| product_id | integer | 是 | 商品ID |

#### 3.1.3 请求示例
```bash
POST /api/products/123/vector
```

#### 3.1.4 响应示例
```json
{
    "success": true,
    "data": {
        "product_id": 123,
        "vector_updated": true,
        "vector_dimension": 384,
        "update_time": "2024-12-20T10:30:00Z"
    },
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": null
}
```

### 3.2 批量更新商品向量

#### 3.2.1 接口信息
- **URL**: `/api/products/vectors/batch-update`
- **方法**: `POST`
- **描述**: 批量更新商品向量

#### 3.2.2 请求体
```json
{
    "product_ids": [123, 124, 125],
    "force_update": false
}
```

#### 3.2.3 请求参数
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| product_ids | array[integer] | 否 | 商品ID列表，为空则更新所有商品 |
| force_update | boolean | 否 | 是否强制更新已有向量 |

#### 3.2.4 响应示例
```json
{
    "success": true,
    "data": {
        "total_products": 3,
        "updated_products": 3,
        "failed_products": 0,
        "update_time": "2024-12-20T10:30:00Z",
        "details": [
            {
                "product_id": 123,
                "status": "success",
                "vector_dimension": 384
            },
            {
                "product_id": 124,
                "status": "success",
                "vector_dimension": 384
            }
        ]
    },
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": null
}
```

## 4. 相似度计算接口

### 4.1 计算商品相似度

#### 4.1.1 接口信息
- **URL**: `/api/similarity/calculate`
- **方法**: `POST`
- **描述**: 计算两个商品的相似度

#### 4.1.2 请求体
```json
{
    "product1_id": 123,
    "product2_id": 124,
    "method": "cosine"
}
```

#### 4.1.3 请求参数
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| product1_id | integer | 是 | 商品1的ID |
| product2_id | integer | 是 | 商品2的ID |
| method | string | 否 | 计算方法 (cosine/euclidean) |

#### 4.1.4 响应示例
```json
{
    "success": true,
    "data": {
        "product1_id": 123,
        "product2_id": 124,
        "similarity_score": 0.95,
        "similarity_percentage": "95.0%",
        "method": "cosine",
        "calculation_time_ms": 25
    },
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": null
}
```

## 5. 推荐算法接口

### 5.1 个性化推荐

#### 5.1.1 接口信息
- **URL**: `/api/recommendations/personalized`
- **方法**: `GET`
- **描述**: 获取个性化商品推荐

#### 5.1.2 查询参数
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| user_id | integer | 是 | 用户ID |
| limit | integer | 否 | 推荐数量 |
| algorithm | string | 否 | 推荐算法 (hybrid/content/collaborative) |

#### 5.1.3 响应示例
```json
{
    "success": true,
    "data": {
        "user_id": 456,
        "recommendations": [
            {
                "product_id": 123,
                "name": "iPhone 15 Pro Max",
                "price": 9999.00,
                "recommendation_score": 0.92,
                "reason": "基于您的浏览历史推荐"
            }
        ],
        "algorithm": "hybrid",
        "total_count": 1
    },
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": null
}
```

## 6. 统计分析接口

### 6.1 相似商品统计

#### 6.1.1 接口信息
- **URL**: `/api/analytics/similarity-stats`
- **方法**: `GET`
- **描述**: 获取相似商品查询统计信息

#### 6.1.2 查询参数
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| start_date | string | 否 | 开始日期 (YYYY-MM-DD) |
| end_date | string | 否 | 结束日期 (YYYY-MM-DD) |
| product_id | integer | 否 | 特定商品ID |

#### 6.1.3 响应示例
```json
{
    "success": true,
    "data": {
        "query_stats": {
            "total_queries": 1250,
            "unique_products": 89,
            "avg_response_time_ms": 180,
            "success_rate": 98.5
        },
        "popular_products": [
            {
                "product_id": 123,
                "name": "iPhone 15 Pro Max",
                "query_count": 45,
                "avg_similarity": 0.87
            }
        ],
        "time_range": {
            "start_date": "2024-12-01",
            "end_date": "2024-12-20"
        }
    },
    "meta": {
        "timestamp": "2024-12-20T10:30:00Z",
        "request_id": "req_123456789",
        "version": "v1.0"
    },
    "error": null
}
```

## 7. 错误码定义

### 7.1 HTTP状态码
| 状态码 | 描述 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权访问 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 429 | 请求频率限制 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

### 7.2 业务错误码
| 错误码 | HTTP状态码 | 描述 |
|--------|------------|------|
| PRODUCT_NOT_FOUND | 404 | 商品不存在 |
| INVALID_PRODUCT_ID | 400 | 无效的商品ID |
| INVALID_PARAMETERS | 400 | 无效的请求参数 |
| VECTOR_NOT_FOUND | 404 | 商品向量不存在 |
| SIMILARITY_CALCULATION_FAILED | 500 | 相似度计算失败 |
| DATABASE_ERROR | 500 | 数据库错误 |
| CACHE_ERROR | 500 | 缓存错误 |
| RATE_LIMIT_EXCEEDED | 429 | 请求频率超限 |
| SERVICE_UNAVAILABLE | 503 | 服务不可用 |

## 8. 限流和配额

### 8.1 请求限制
| 接口类型 | 限制 | 时间窗口 |
|----------|------|----------|
| 相似商品查询 | 100次/分钟 | 1分钟 |
| 批量查询 | 10次/分钟 | 1分钟 |
| 向量更新 | 50次/小时 | 1小时 |
| 统计分析 | 20次/小时 | 1小时 |

### 8.2 配额响应头
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

## 9. 认证和授权

### 9.1 认证方式
```http
Authorization: Bearer <access_token>
```

### 9.2 权限级别
| 权限 | 描述 | 接口范围 |
|------|------|----------|
| public | 公开访问 | 相似商品查询 |
| user | 用户权限 | 个性化推荐 |
| admin | 管理员权限 | 向量管理、统计分析 |

## 10. SDK和示例

### 10.1 Python SDK示例
```python
import requests

class SimilarProductClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}' if api_key else None
        }
    
    def get_similar_products(self, product_id, limit=12, threshold=0.75, user_id=None):
        """获取相似商品"""
        url = f"{self.base_url}/api/similar-products/{product_id}"
        params = {
            'limit': limit,
            'threshold': threshold
        }
        if user_id:
            params['user_id'] = user_id
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def batch_get_similar_products(self, product_ids, limit=6, threshold=0.75, user_id=None):
        """批量获取相似商品"""
        url = f"{self.base_url}/api/similar-products/batch"
        data = {
            'product_ids': product_ids,
            'limit': limit,
            'threshold': threshold
        }
        if user_id:
            data['user_id'] = user_id
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

# 使用示例
client = SimilarProductClient('https://api.recommendation.com/v1', 'your_api_key')

# 获取相似商品
similar_products = client.get_similar_products(123, limit=6, user_id=456)
print(similar_products)
```

### 10.2 JavaScript SDK示例
```javascript
class SimilarProductClient {
    constructor(baseUrl, apiKey = null) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Content-Type': 'application/json',
            'Authorization': apiKey ? `Bearer ${apiKey}` : null
        };
    }
    
    async getSimilarProducts(productId, options = {}) {
        const { limit = 12, threshold = 0.75, userId = null } = options;
        
        const url = new URL(`${this.baseUrl}/api/similar-products/${productId}`);
        url.searchParams.append('limit', limit);
        url.searchParams.append('threshold', threshold);
        if (userId) {
            url.searchParams.append('user_id', userId);
        }
        
        const response = await fetch(url, {
            method: 'GET',
            headers: this.headers
        });
        
        return await response.json();
    }
    
    async batchGetSimilarProducts(productIds, options = {}) {
        const { limit = 6, threshold = 0.75, userId = null } = options;
        
        const url = `${this.baseUrl}/api/similar-products/batch`;
        const data = {
            product_ids: productIds,
            limit,
            threshold
        };
        
        if (userId) {
            data.user_id = userId;
        }
        
        const response = await fetch(url, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        
        return await response.json();
    }
}

// 使用示例
const client = new SimilarProductClient('https://api.recommendation.com/v1', 'your_api_key');

// 获取相似商品
client.getSimilarProducts(123, { limit: 6, userId: 456 })
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

## 11. 测试工具

### 11.1 Postman集合
```json
{
    "info": {
        "name": "Similar Products API",
        "description": "相似商品查询API测试集合"
    },
    "item": [
        {
            "name": "Get Similar Products",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "{{base_url}}/api/similar-products/123?limit=12&threshold=0.75",
                    "host": ["{{base_url}}"],
                    "path": ["api", "similar-products", "123"],
                    "query": [
                        {"key": "limit", "value": "12"},
                        {"key": "threshold", "value": "0.75"}
                    ]
                }
            }
        }
    ]
}
```

### 11.2 curl示例
```bash
# 获取相似商品
curl -X GET "https://api.recommendation.com/v1/api/similar-products/123?limit=12&threshold=0.75" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json"

# 批量获取相似商品
curl -X POST "https://api.recommendation.com/v1/api/similar-products/batch" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": [123, 124, 125],
    "limit": 6,
    "threshold": 0.75
  }'
```

## 12. 附录

### 12.1 更新日志
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2024-12-20 | 初始版本，包含基础相似商品查询功能 |

### 12.2 相关文档
- 需求文档
- 数据库设计文档
- 详细设计文档
- 系统架构文档

### 12.3 联系方式
- **技术支持**: tech-support@recommendation.com
- **API问题**: api-support@recommendation.com
- **文档反馈**: docs@recommendation.com
