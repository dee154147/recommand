# 第三阶段API接口文档

## 概述
本文档描述了第三阶段新增的API接口，主要包括用户交互、用户管理和个性化推荐功能。

## 接口分类

### 1. 用户交互API (`/api/v1/user-interactions`)

#### 1.1 记录用户交互
- **接口**: `POST /api/v1/user-interactions/record`
- **功能**: 记录用户与商品的交互行为
- **请求参数**:
  ```json
  {
    "user_id": 1,
    "product_id": 123,
    "interaction_type": "click",
    "interaction_score": 1.0,
    "session_id": "session_123"
  }
  ```
- **响应示例**:
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "user_id": 1,
      "product_id": 123,
      "interaction_type": "click",
      "interaction_score": 1.0,
      "session_id": "session_123",
      "created_at": "2024-12-20T10:00:00Z"
    },
    "message": "交互记录成功"
  }
  ```

#### 1.2 获取用户交互历史
- **接口**: `GET /api/v1/user-interactions/user/{user_id}`
- **功能**: 获取指定用户的交互历史
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20, 最大: 100)
  - `type`: 交互类型过滤 (可选)
- **响应示例**:
  ```json
  {
    "success": true,
    "data": {
      "interactions": [...],
      "pagination": {
        "page": 1,
        "pages": 5,
        "per_page": 20,
        "total": 100,
        "has_next": true,
        "has_prev": false
      }
    },
    "message": "获取用户交互历史成功"
  }
  ```

#### 1.3 获取用户交互统计
- **接口**: `GET /api/v1/user-interactions/user/{user_id}/statistics`
- **功能**: 获取用户的交互统计信息
- **响应示例**:
  ```json
  {
    "success": true,
    "data": {
      "total_interactions": 150,
      "unique_products_viewed": 45,
      "recent_week_activity": 12,
      "top_categories": [
        {"category_id": 1, "interaction_count": 25},
        {"category_id": 2, "interaction_count": 20}
      ],
      "account_created": "2024-01-01T00:00:00Z",
      "last_updated": "2024-12-20T10:00:00Z"
    },
    "message": "获取用户统计成功"
  }
  ```

#### 1.4 获取用户偏好分析
- **接口**: `GET /api/v1/user-interactions/user/{user_id}/preferences`
- **功能**: 获取用户的偏好分析数据
- **响应示例**:
  ```json
  {
    "success": true,
    "data": {
      "interaction_types": {
        "click": 50,
        "view": 30,
        "favorite": 10,
        "purchase": 5
      },
      "category_preferences": {
        "电子产品": 25.5,
        "服装": 15.2,
        "家居": 8.8
      },
      "recent_activity": 12,
      "total_interactions": 150,
      "preferences": {}
    },
    "message": "获取用户偏好成功"
  }
  ```

#### 1.5 更新用户偏好
- **接口**: `PUT /api/v1/user-interactions/user/{user_id}/preferences`
- **功能**: 更新用户的偏好设置
- **请求参数**:
  ```json
  {
    "preferences": {
      "favorite_categories": ["电子产品", "服装"],
      "price_range": {"min": 100, "max": 1000},
      "brand_preferences": ["苹果", "小米"]
    }
  }
  ```

#### 1.6 获取商品交互统计
- **接口**: `GET /api/v1/user-interactions/product/{product_id}/interactions`
- **功能**: 获取指定商品的交互统计信息
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20, 最大: 100)

#### 1.7 获取最近交互记录
- **接口**: `GET /api/v1/user-interactions/recent`
- **功能**: 获取最近的交互记录
- **查询参数**:
  - `limit`: 限制数量 (默认: 50, 最大: 200)
  - `hours`: 时间范围（小时）(默认: 24)

### 2. 用户管理API (`/api/v1/users`)

#### 2.1 用户注册
- **接口**: `POST /api/v1/users/register`
- **功能**: 注册新用户
- **请求参数**:
  ```json
  {
    "username": "user123",
    "email": "user@example.com",
    "preferences": {}
  }
  ```

#### 2.2 用户登录
- **接口**: `POST /api/v1/users/login`
- **功能**: 用户登录
- **请求参数**:
  ```json
  {
    "username": "user123"
  }
  ```

#### 2.3 获取用户信息
- **接口**: `GET /api/v1/users/{user_id}`
- **功能**: 获取指定用户的详细信息

#### 2.4 更新用户信息
- **接口**: `PUT /api/v1/users/{user_id}`
- **功能**: 更新用户信息
- **请求参数**:
  ```json
  {
    "username": "new_username",
    "email": "new_email@example.com",
    "preferences": {...}
  }
  ```

#### 2.5 删除用户
- **接口**: `DELETE /api/v1/users/{user_id}`
- **功能**: 删除用户及其相关数据

#### 2.6 获取用户仪表板
- **接口**: `GET /api/v1/users/{user_id}/dashboard`
- **功能**: 获取用户仪表板数据，包括基本信息、统计、偏好和最近交互

#### 2.7 获取用户活动记录
- **接口**: `GET /api/v1/users/{user_id}/activity`
- **功能**: 获取用户的活动记录
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20, 最大: 100)
  - `days`: 时间范围（天）(默认: 30)

#### 2.8 搜索用户
- **接口**: `GET /api/v1/users/search`
- **功能**: 搜索用户
- **查询参数**:
  - `q`: 搜索关键词
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20, 最大: 100)

### 3. 个性化推荐API (`/api/v1/personalized-recommendations`)

#### 3.1 获取用户个性化推荐
- **接口**: `GET /api/v1/personalized-recommendations/user/{user_id}`
- **功能**: 获取用户的个性化推荐商品
- **查询参数**:
  - `limit`: 推荐数量 (默认: 10, 最大: 50)
  - `algorithm`: 推荐算法 (hybrid/collaborative/content_based, 默认: hybrid)
  - `refresh`: 是否刷新推荐 (true/false, 默认: false)
- **响应示例**:
  ```json
  {
    "success": true,
    "data": {
      "user_id": 1,
      "recommendations": [
        {
          "id": 123,
          "name": "商品名称",
          "description": "商品描述",
          "price": 299.99,
          "category_id": 1,
          "category_name": "电子产品",
          "image_url": "https://example.com/image.jpg",
          "tags": ["标签1", "标签2"],
          "recommendation_reason": "基于您的偏好",
          "similarity_score": 0.85
        }
      ],
      "count": 10,
      "algorithm_type": "hybrid",
      "generated_at": "2024-12-20T10:00:00Z"
    },
    "message": "获取个性化推荐成功"
  }
  ```

#### 3.2 获取相似用户
- **接口**: `GET /api/v1/personalized-recommendations/user/{user_id}/similar-users`
- **功能**: 获取与指定用户相似的其他用户
- **查询参数**:
  - `limit`: 限制数量 (默认: 10, 最大: 50)

#### 3.3 获取偏好推荐
- **接口**: `GET /api/v1/personalized-recommendations/user/{user_id}/preferences`
- **功能**: 基于用户偏好获取推荐商品
- **查询参数**:
  - `limit`: 推荐数量 (默认: 10, 最大: 50)

#### 3.4 获取趋势推荐
- **接口**: `GET /api/v1/personalized-recommendations/user/{user_id}/trending`
- **功能**: 获取趋势推荐商品
- **查询参数**:
  - `limit`: 推荐数量 (默认: 10, 最大: 50)
  - `days`: 时间范围（天）(默认: 7)

#### 3.5 刷新用户推荐
- **接口**: `POST /api/v1/personalized-recommendations/user/{user_id}/refresh`
- **功能**: 刷新用户的推荐结果

## 错误处理

### 标准错误响应格式
```json
{
  "success": false,
  "error": "错误描述信息"
}
```

### 常见HTTP状态码
- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `404`: 资源不存在
- `409`: 资源冲突（如用户名已存在）
- `500`: 服务器内部错误

## 交互类型说明

### 支持的交互类型
- `click`: 点击行为，评分 +1
- `view`: 查看行为，评分 +2
- `favorite`: 收藏行为，评分 +3
- `purchase`: 购买行为，评分 +5
- `dislike`: 不推荐行为，评分 -2

## 推荐算法说明

### 1. 混合推荐 (hybrid)
结合协同过滤和基于内容的推荐，提供更准确的推荐结果。

### 2. 协同过滤 (collaborative)
基于用户行为相似性，推荐相似用户喜欢的商品。

### 3. 基于内容 (content_based)
基于商品特征和用户偏好，推荐相似的商品。

## 使用示例

### 前端集成示例
```javascript
// 记录用户交互
const recordInteraction = async (userId, productId, interactionType) => {
  const response = await fetch('/api/v1/user-interactions/record', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      product_id: productId,
      interaction_type: interactionType,
      interaction_score: getInteractionScore(interactionType)
    })
  });
  
  return response.json();
};

// 获取个性化推荐
const getRecommendations = async (userId) => {
  const response = await fetch(`/api/v1/personalized-recommendations/user/${userId}?limit=10`);
  return response.json();
};

// 获取用户交互历史
const getUserInteractions = async (userId, page = 1) => {
  const response = await fetch(`/api/v1/user-interactions/user/${userId}?page=${page}`);
  return response.json();
};
```

## 性能优化建议

1. **分页查询**: 所有列表接口都支持分页，建议使用合理的分页大小
2. **缓存策略**: 推荐结果可以缓存，减少重复计算
3. **异步处理**: 大量数据处理建议使用异步任务
4. **索引优化**: 确保数据库查询字段有适当的索引

## 安全考虑

1. **参数验证**: 所有输入参数都经过验证
2. **权限控制**: 用户只能访问自己的数据
3. **SQL注入防护**: 使用参数化查询
4. **速率限制**: 建议对API调用进行速率限制
