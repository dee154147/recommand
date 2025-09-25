import axios from 'axios'
import { ElMessage } from 'element-plus'

// 自动检测API基础URL
const getApiBaseUrl = () => {
  // 获取当前主机地址
  const hostname = window.location.hostname
  const protocol = window.location.protocol
  
  // 如果是localhost或127.0.0.1，使用localhost
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:5004/api'
  }
  
  // 如果是局域网IP，使用相同的主机地址
  return `${protocol}//${hostname}:5004/api`
}

// 创建axios实例
const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 30000, // 增加超时时间到30秒
  headers: {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    const { data } = response
    
    // 统一处理响应格式
    if (data.success === true) {
      return data
    } else {
      // 对于个性化推荐API，不显示错误消息，让调用方处理
      if (response.config.url.includes('/personalized-recommendations/')) {
        return data
      } else {
        ElMessage.error(data.message || '请求失败')
        return Promise.reject(new Error(data.message || '请求失败'))
      }
    }
  },
  error => {
    // 对于用户查询API的404错误，不显示错误消息，让调用方处理
    if (error.response?.status === 404 && error.config?.url?.includes('/users/')) {
      return Promise.reject(error)
    }
    
    const message = error.response?.data?.message || error.message || '网络错误'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// API接口方法
export const productAPI = {
  // 获取商品列表
  getProducts(params = {}) {
    return api.get('/products', { params })
  },
  
  // 获取商品详情
  getProduct(id) {
    return api.get(`/products/${id}`)
  },
  
  // 搜索商品
  searchProducts(query, params = {}) {
    return api.get('/search', { params: { q: query, ...params } })
  },
  
  // 语义搜索
  semanticSearch(query, params = {}) {
    return api.get('/v1/search/products', { 
      params: { q: query, type: 'semantic', ...params } 
    })
  },
  
  // 模糊搜索
  fuzzySearch(query, params = {}) {
    return api.get('/v1/search/products', { 
      params: { q: query, type: 'fuzzy', ...params } 
    })
  },
  
  // 获取商品分类
  getCategories() {
    return api.get('/categories')
  }
}

export const recommendationAPI = {
  // 获取推荐商品
  getRecommendations(params = {}) {
    return api.get('/recommendations', { params })
  },
  
  // 获取相似商品
  getSimilarProducts(productId, limit = 10) {
    return api.get('/recommendations', { 
      params: { product_id: productId, limit } 
    })
  },
  
  // 获取用户推荐
  getUserRecommendations(userId, limit = 10) {
    return api.get('/recommendations', { 
      params: { user_id: userId, limit } 
    })
  },
  
  // 获取个性化推荐 - 使用v2确定性算法
  getPersonalizedRecommendations(userId, params = {}) {
    // 添加时间戳和唯一标识符避免浏览器缓存
    const timestamp = Date.now()
    const requestId = `req_${timestamp}_${Math.random().toString(36).substr(2, 9)}`
    console.log(`🌐 API调用 [${requestId}]: 获取个性化推荐 (v2确定性算法)`, { userId, params })
    
    return api.get(`/v2/personalized-recommendations/user/${userId}`, { 
      params: { 
        ...params, 
        _t: timestamp,
        _req: requestId
      }
    })
  },
  
  // 获取相似用户
  getSimilarUsers(userId, limit = 10) {
    return api.get(`/v1/personalized-recommendations/user/${userId}/similar-users`, {
      params: { limit }
    })
  },
  
  // 更新用户画像 - 使用v2确定性算法
  updateUserProfile(userId) {
    return api.post(`/v2/personalized-recommendations/user/${userId}/update-profile`)
  },
  
  // 获取偏好推荐
  getPreferenceRecommendations(userId, params = {}) {
    return api.get(`/v1/personalized-recommendations/user/${userId}/preferences`, { params })
  },
  
  // 获取趋势推荐
  getTrendingRecommendations(userId, params = {}) {
    return api.get(`/v1/personalized-recommendations/user/${userId}/trending`, { params })
  },
  
  // 刷新用户推荐
  refreshUserRecommendations(userId) {
    return api.post(`/v1/personalized-recommendations/user/${userId}/refresh`)
  }
}

export const userAPI = {
  // 用户注册
  register(userData) {
    return api.post('/v1/users/register', userData)
  },
  
  // 用户登录
  login(credentials) {
    return api.post('/v1/users/login', credentials)
  },
  
  // 获取用户信息
  getUser(id) {
    return api.get(`/v1/users/${id}`)
  },
  
  // 更新用户信息
  updateUser(id, userData) {
    return api.put(`/v1/users/${id}`, userData)
  },
  
  // 更新用户偏好
  updateUserPreferences(userId, preferences) {
    return api.put(`/v1/user-interactions/user/${userId}/preferences`, preferences)
  },
  
  // 记录用户行为
  recordUserInteraction(interaction) {
    return api.post('/v1/user-interactions/record', interaction)
  },
  
  // 获取用户交互历史
  getUserInteractions(userId, params = {}) {
    return api.get(`/v1/user-interactions/user/${userId}`, { params })
  },
  
  // 获取用户交互统计
  getUserStatistics(userId) {
    return api.get(`/v1/user-interactions/user/${userId}/statistics`)
  }
}

// 系统API
export const systemAPI = {
  // 健康检查
  healthCheck() {
    return api.get('/health')
  },
  
  // 获取系统状态
  getSystemStatus() {
    return api.get('/status')
  }
}

export default api
