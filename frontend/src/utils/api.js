import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5002/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
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
    if (data.status === 'success') {
      return data
    } else {
      ElMessage.error(data.message || '请求失败')
      return Promise.reject(new Error(data.message || '请求失败'))
    }
  },
  error => {
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
  }
}

export const userAPI = {
  // 获取用户信息
  getUser(id) {
    return api.get(`/users/${id}`)
  },
  
  // 更新用户偏好
  updateUserPreferences(userId, preferences) {
    return api.put(`/users/${userId}/preferences`, preferences)
  },
  
  // 记录用户行为
  recordUserInteraction(interaction) {
    return api.post('/user-interactions', interaction)
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
