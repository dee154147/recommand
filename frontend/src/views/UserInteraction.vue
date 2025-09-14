<template>
  <div class="user-interaction-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="container">
        <div class="nav-brand">
          <router-link to="/">
            <h2>🚀 推荐系统</h2>
          </router-link>
        </div>
        <div class="nav-menu">
          <router-link to="/" class="nav-link">首页</router-link>
          <span class="nav-link active">用户交互</span>
        </div>
      </div>
    </nav>

    <div class="main-content">
      <div class="container">
        <!-- 页面标题 -->
        <div class="page-header">
          <h1 class="page-title">👥 用户交互</h1>
          <p class="page-subtitle">用户行为分析和推荐效果展示</p>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card card">
            <div class="stat-icon">👤</div>
            <div class="stat-content">
              <h3>总用户数</h3>
              <p class="stat-number">{{ stats.totalUsers }}</p>
            </div>
          </div>
          
          <div class="stat-card card">
            <div class="stat-icon">🛒</div>
            <div class="stat-content">
              <h3>今日访问</h3>
              <p class="stat-number">{{ stats.todayVisits }}</p>
            </div>
          </div>
          
          <div class="stat-card card">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
              <h3>推荐点击率</h3>
              <p class="stat-number">{{ stats.clickRate }}%</p>
            </div>
          </div>
          
          <div class="stat-card card">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <h3>平均评分</h3>
              <p class="stat-number">{{ stats.averageRating }}</p>
            </div>
          </div>
        </div>

        <!-- 主要内容区域 -->
        <div class="content-grid">
          <!-- 用户行为分析 -->
          <div class="section card">
            <div class="section-header">
              <h2>📊 用户行为分析</h2>
              <el-button @click="refreshUserBehavior">刷新数据</el-button>
            </div>
            
            <div class="behavior-list" v-loading="loadingBehavior">
              <div
                v-for="behavior in userBehaviors"
                :key="behavior.id"
                class="behavior-item"
              >
                <div class="user-info">
                  <div class="user-avatar">
                    {{ behavior.user_name.charAt(0).toUpperCase() }}
                  </div>
                  <div class="user-details">
                    <h4>{{ behavior.user_name }}</h4>
                    <p>{{ behavior.action_time }}</p>
                  </div>
                </div>
                
                <div class="action-info">
                  <el-tag :type="getActionType(behavior.action_type)">
                    {{ getActionText(behavior.action_type) }}
                  </el-tag>
                  <span class="product-name">{{ behavior.product_name }}</span>
                </div>
                
                <div class="action-result">
                  <span class="rating" v-if="behavior.rating">
                    <el-rate v-model="behavior.rating" disabled />
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 推荐效果展示 -->
          <div class="section card">
            <div class="section-header">
              <h2>🎯 推荐效果展示</h2>
              <el-button @click="generateRecommendations">生成推荐</el-button>
            </div>
            
            <div class="recommendation-demo">
              <div class="demo-user">
                <h3>模拟用户: {{ demoUser.name }}</h3>
                <p>历史行为偏好: {{ demoUser.preferences.join(', ') }}</p>
              </div>
              
              <div class="recommendations" v-loading="loadingRecommendations">
                <div
                  v-for="(product, index) in recommendations"
                  :key="product.id"
                  class="recommendation-item"
                  :class="{ 'top-recommendation': index < 3 }"
                >
                  <div class="rank">{{ index + 1 }}</div>
                  <img :src="product.image_url || '/placeholder-product.jpg'" class="product-image" />
                  <div class="product-info">
                    <h4>{{ product.name }}</h4>
                    <p>{{ product.description }}</p>
                    <div class="recommendation-score">
                      <span>推荐度: {{ product.score }}%</span>
                      <el-progress :percentage="product.score" :show-text="false" />
                    </div>
                  </div>
                  <div class="actions">
                    <el-button size="small" @click="simulateClick(product)">点击</el-button>
                    <el-button size="small" @click="simulatePurchase(product)">购买</el-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 交互测试区域 -->
        <div class="interaction-test card">
          <div class="section-header">
            <h2>🧪 交互测试</h2>
            <p>模拟用户与推荐系统的交互过程</p>
          </div>
          
          <div class="test-interface">
            <div class="test-controls">
              <el-select v-model="selectedUser" placeholder="选择测试用户">
                <el-option
                  v-for="user in testUsers"
                  :key="user.id"
                  :label="user.name"
                  :value="user.id"
                />
              </el-select>
              
              <el-select v-model="selectedProduct" placeholder="选择商品">
                <el-option
                  v-for="product in testProducts"
                  :key="product.id"
                  :label="product.name"
                  :value="product.id"
                />
              </el-select>
              
              <el-select v-model="selectedAction" placeholder="选择行为">
                <el-option label="浏览" value="view"></el-option>
                <el-option label="点击" value="click"></el-option>
                <el-option label="收藏" value="favorite"></el-option>
                <el-option label="购买" value="purchase"></el-option>
              </el-select>
              
              <el-button type="primary" @click="simulateInteraction">模拟交互</el-button>
            </div>
            
            <div class="test-results">
              <h4>交互结果:</h4>
              <div v-if="interactionResult" class="result-item">
                <p><strong>用户:</strong> {{ interactionResult.user_name }}</p>
                <p><strong>行为:</strong> {{ getActionText(interactionResult.action_type) }}</p>
                <p><strong>商品:</strong> {{ interactionResult.product_name }}</p>
                <p><strong>时间:</strong> {{ interactionResult.action_time }}</p>
                <p><strong>推荐度变化:</strong> 
                  <span :class="interactionResult.score_change > 0 ? 'positive' : 'negative'">
                    {{ interactionResult.score_change > 0 ? '+' : '' }}{{ interactionResult.score_change }}%
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'UserInteraction',
  setup() {
    const loadingBehavior = ref(false)
    const loadingRecommendations = ref(false)
    
    const stats = reactive({
      totalUsers: 1250,
      todayVisits: 3420,
      clickRate: 15.8,
      averageRating: 4.6
    })
    
    const selectedUser = ref(null)
    const selectedProduct = ref(null)
    const selectedAction = ref('')
    const interactionResult = ref(null)
    
    const demoUser = reactive({
      name: '张三',
      preferences: ['电子产品', '运动用品', '数码配件']
    })
    
    const testUsers = ref([
      { id: 1, name: '张三' },
      { id: 2, name: '李四' },
      { id: 3, name: '王五' },
      { id: 4, name: '赵六' }
    ])
    
    const testProducts = ref([
      { id: 1, name: 'iPhone 15 Pro' },
      { id: 2, name: 'MacBook Air M2' },
      { id: 3, name: 'Nike Air Max' },
      { id: 4, name: 'Samsung Galaxy S24' }
    ])
    
    // 模拟用户行为数据
    const userBehaviors = ref([
      {
        id: 1,
        user_name: '张三',
        action_type: 'view',
        product_name: 'iPhone 15 Pro',
        action_time: '2024-12-20 14:30:25',
        rating: null
      },
      {
        id: 2,
        user_name: '李四',
        action_type: 'click',
        product_name: 'MacBook Air M2',
        action_time: '2024-12-20 14:25:10',
        rating: null
      },
      {
        id: 3,
        user_name: '王五',
        action_type: 'purchase',
        product_name: 'Nike Air Max',
        action_time: '2024-12-20 14:20:45',
        rating: 5
      },
      {
        id: 4,
        user_name: '赵六',
        action_type: 'favorite',
        product_name: 'Samsung Galaxy S24',
        action_time: '2024-12-20 14:15:30',
        rating: null
      }
    ])
    
    // 模拟推荐数据
    const recommendations = ref([
      {
        id: 1,
        name: 'iPhone 15 Pro',
        description: '最新款苹果手机，性能强劲',
        score: 95,
        image_url: 'https://via.placeholder.com/100x100?text=iPhone'
      },
      {
        id: 2,
        name: 'AirPods Pro',
        description: '无线降噪耳机',
        score: 88,
        image_url: 'https://via.placeholder.com/100x100?text=AirPods'
      },
      {
        id: 3,
        name: 'Apple Watch',
        description: '智能手表',
        score: 82,
        image_url: 'https://via.placeholder.com/100x100?text=Watch'
      },
      {
        id: 4,
        name: 'iPad Pro',
        description: '专业平板电脑',
        score: 76,
        image_url: 'https://via.placeholder.com/100x100?text=iPad'
      },
      {
        id: 5,
        name: 'MacBook Pro',
        description: '专业笔记本电脑',
        score: 72,
        image_url: 'https://via.placeholder.com/100x100?text=MacBook'
      }
    ])
    
    const getActionType = (actionType) => {
      const types = {
        view: 'info',
        click: 'warning',
        favorite: 'success',
        purchase: 'danger',
        rate: 'primary'
      }
      return types[actionType] || 'info'
    }
    
    const getActionText = (actionType) => {
      const texts = {
        view: '浏览',
        click: '点击',
        favorite: '收藏',
        purchase: '购买',
        rate: '评分'
      }
      return texts[actionType] || '未知'
    }
    
    const refreshUserBehavior = () => {
      loadingBehavior.value = true
      setTimeout(() => {
        loadingBehavior.value = false
        ElMessage.success('用户行为数据已刷新')
      }, 1000)
    }
    
    const generateRecommendations = () => {
      loadingRecommendations.value = true
      setTimeout(() => {
        loadingRecommendations.value = false
        ElMessage.success('推荐结果已更新')
      }, 1500)
    }
    
    const simulateClick = (product) => {
      ElMessage.success(`用户点击了商品: ${product.name}`)
    }
    
    const simulatePurchase = (product) => {
      ElMessage.success(`用户购买了商品: ${product.name}`)
    }
    
    const simulateInteraction = () => {
      if (!selectedUser.value || !selectedProduct.value || !selectedAction.value) {
        ElMessage.warning('请选择用户、商品和行为')
        return
      }
      
      const user = testUsers.value.find(u => u.id === selectedUser.value)
      const product = testProducts.value.find(p => p.id === selectedProduct.value)
      
      // 模拟交互结果
      interactionResult.value = {
        user_name: user.name,
        action_type: selectedAction.value,
        product_name: product.name,
        action_time: new Date().toLocaleString(),
        score_change: Math.floor(Math.random() * 20) - 10 // -10 到 +10 的随机变化
      }
      
      ElMessage.success('交互模拟完成')
    }
    
    onMounted(() => {
      // 初始化数据
      refreshUserBehavior()
      generateRecommendations()
    })
    
    return {
      loadingBehavior,
      loadingRecommendations,
      stats,
      selectedUser,
      selectedProduct,
      selectedAction,
      interactionResult,
      demoUser,
      testUsers,
      testProducts,
      userBehaviors,
      recommendations,
      getActionType,
      getActionText,
      refreshUserBehavior,
      generateRecommendations,
      simulateClick,
      simulatePurchase,
      simulateInteraction
    }
  }
}
</script>

<style lang="scss" scoped>
.user-interaction-page {
  min-height: 100vh;
  background: #f8f9fa;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: white;
  box-shadow: var(--shadow);
  z-index: 1000;
  
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    max-width: 1400px;
    margin: 0 auto;
  }
  
  .nav-brand a {
    text-decoration: none;
    color: var(--primary-color);
  }
  
  .nav-menu {
    display: flex;
    align-items: center;
    gap: 2rem;
    
    .nav-link {
      text-decoration: none;
      color: var(--text-color);
      font-weight: 500;
      transition: color 0.3s ease;
      
      &.active {
        color: var(--primary-color);
      }
      
      &:hover:not(.active) {
        color: var(--primary-color);
      }
    }
  }
}

.main-content {
  margin-top: 80px;
  padding: 2rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
  
  .page-title {
    font-size: 2.5rem;
    color: var(--text-color);
    margin-bottom: 0.5rem;
  }
  
  .page-subtitle {
    font-size: 1.1rem;
    color: #666;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
  
  .stat-card {
    display: flex;
    align-items: center;
    padding: 2rem;
    
    .stat-icon {
      font-size: 3rem;
      margin-right: 1.5rem;
    }
    
    .stat-content {
      .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
      }
      
      h3 {
        margin: 0 0 0.5rem 0;
        color: var(--text-color);
      }
    }
  }
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

.section {
  padding: 2rem;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    
    h2 {
      margin: 0;
      color: var(--text-color);
    }
  }
}

.behavior-list {
  .behavior-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0;
    border-bottom: 1px solid #f0f0f0;
    
    &:last-child {
      border-bottom: none;
    }
    
    .user-info {
      display: flex;
      align-items: center;
      
      .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--primary-color);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
      }
      
      .user-details {
        h4 {
          margin: 0 0 0.25rem 0;
          font-size: 1rem;
        }
        
        p {
          margin: 0;
          font-size: 0.9rem;
          color: #666;
        }
      }
    }
    
    .action-info {
      flex: 1;
      margin: 0 2rem;
      
      .product-name {
        display: block;
        margin-top: 0.5rem;
        color: var(--text-color);
      }
    }
    
    .action-result {
      .rating {
        display: flex;
        align-items: center;
      }
    }
  }
}

.recommendation-demo {
  .demo-user {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    
    h3 {
      margin: 0 0 0.5rem 0;
      color: var(--text-color);
    }
    
    p {
      margin: 0;
      color: #666;
    }
  }
  
  .recommendations {
    .recommendation-item {
      display: flex;
      align-items: center;
      padding: 1rem;
      border: 1px solid #e9ecef;
      border-radius: 8px;
      margin-bottom: 1rem;
      transition: all 0.3s ease;
      
      &.top-recommendation {
        border-color: var(--primary-color);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
      }
      
      .rank {
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--primary-color);
        margin-right: 1rem;
        min-width: 30px;
      }
      
      .product-image {
        width: 60px;
        height: 60px;
        object-fit: cover;
        border-radius: 8px;
        margin-right: 1rem;
      }
      
      .product-info {
        flex: 1;
        
        h4 {
          margin: 0 0 0.5rem 0;
          color: var(--text-color);
        }
        
        p {
          margin: 0 0 0.5rem 0;
          color: #666;
          font-size: 0.9rem;
        }
        
        .recommendation-score {
          display: flex;
          align-items: center;
          gap: 1rem;
          
          span {
            font-size: 0.9rem;
            color: var(--primary-color);
            font-weight: 500;
          }
        }
      }
      
      .actions {
        display: flex;
        gap: 0.5rem;
      }
    }
  }
}

.interaction-test {
  padding: 2rem;
  
  .test-interface {
    .test-controls {
      display: flex;
      gap: 1rem;
      margin-bottom: 2rem;
      flex-wrap: wrap;
      
      .el-select {
        min-width: 150px;
      }
    }
    
    .test-results {
      background: #f8f9fa;
      padding: 1.5rem;
      border-radius: 8px;
      
      h4 {
        margin: 0 0 1rem 0;
        color: var(--text-color);
      }
      
      .result-item {
        p {
          margin: 0.5rem 0;
          color: var(--text-color);
          
          .positive {
            color: #52c41a;
            font-weight: bold;
          }
          
          .negative {
            color: #ff4d4f;
            font-weight: bold;
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
  
  .behavior-item {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .recommendation-item {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .test-controls {
    flex-direction: column;
    
    .el-select {
      min-width: auto !important;
    }
  }
}
</style>
