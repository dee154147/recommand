<template>
  <div class="user-interaction-page">
    <!-- 背景动画 -->
    <div class="bg-animation"></div>

    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="logo">智能推荐系统</div>
        <ul class="nav-menu">
          <li class="nav-item"><router-link to="/">首页</router-link></li>
          <li class="nav-item"><router-link to="/#features">产品特性</router-link></li>
          <li class="nav-item"><router-link to="/#team">团队介绍</router-link></li>
          <li class="nav-item"><router-link to="/#contact">联系我们</router-link></li>
          <li class="nav-item dropdown">
            <a href="#" class="dropdown-toggle">功能演示</a>
            <div class="dropdown-menu">
              <router-link to="/product-search" class="dropdown-item">商品检索</router-link>
              <router-link to="/product-management" class="dropdown-item">商品管理</router-link>
              <router-link to="/user-login" class="dropdown-item active">用户交互</router-link>
        </div>
          </li>
        </ul>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="container">
        <!-- 用户信息栏 -->
        <div class="user-info" v-if="currentUser">
          <div class="user-avatar">{{ getUserAvatar(currentUser.name) }}</div>
          <div class="user-details">
            <div class="user-name">{{ currentUser.name }}</div>
            <div class="user-stats">已交互: {{ userInteractions.length }}次 | 总评分: {{ totalScore }}分</div>
          </div>
          <div class="user-actions">
            <button class="btn-small btn-history" @click="showInteractionHistory">📋 交互历史</button>
            <button class="btn-small btn-logout" @click="logout">🚪 退出</button>
          </div>
        </div>
          
        <!-- 搜索区域 -->
        <section class="search-section">
          <div class="search-container">
            <div class="search-bar">
              <input 
                type="text" 
                class="search-input" 
                placeholder="请输入商品关键词，如：智能手机、运动鞋、笔记本电脑..."
                v-model="searchQuery"
                @keypress.enter="() => performSemanticSearch(1)"
              >
            </div>
            <div class="search-buttons">
              <button class="search-btn" @click="() => performSemanticSearch(1)" :disabled="loading">
                🔍 语义检索
              </button>
              <button class="search-btn secondary" @click="() => performFuzzySearch(1)" :disabled="loading">
                📝 模糊匹配
              </button>
            </div>
          </div>
        </section>

        <!-- 商品展示区域 -->
        <section class="products-section" v-if="currentProducts.length > 0">
          <!-- 搜索结果信息 -->
          <div class="search-results-info">
            <div class="results-summary">
              <span class="results-count">找到 {{ totalProducts }} 个商品</span>
              <span class="results-page">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
            </div>
            <div class="search-type-indicator">
              <span class="search-type-badge" :class="searchType">
                {{ searchType === 'semantic' ? '🔍 语义检索' : '📝 模糊匹配' }}
              </span>
            </div>
          </div>
          
          <!-- 商品网格 -->
          <div class="products-grid">
            <div
              v-for="product in currentProducts"
              :key="product.id"
              class="product-card"
            >
              <div class="product-image" v-if="product.image_url">
                <img :src="product.image_url" :alt="product.name">
              </div>
              <div class="product-info">
                <div class="product-details">
                  <h3 class="product-name">{{ product.name }}</h3>
                  <p class="product-description">{{ product.description }}</p>
                  <div class="product-tags">
                    <span v-for="tag in product.tags" :key="tag" class="product-tag">{{ tag }}</span>
                  </div>
                </div>
                <div class="interaction-buttons">
                  <button class="interaction-btn btn-click" @click="recordInteraction(product.id, 'click', 1)">
                    👆 点击
                  </button>
                  <button class="interaction-btn btn-view" @click="recordInteraction(product.id, 'view', 2)">
                    👁 查看
                  </button>
                  <button class="interaction-btn btn-favorite" @click="recordInteraction(product.id, 'favorite', 3)">
                    ❤ 收藏
                  </button>
                  <button class="interaction-btn btn-purchase" @click="recordInteraction(product.id, 'purchase', 5)">
                    🛒 购买
                  </button>
                  <button class="interaction-btn btn-dislike" @click="recordInteraction(product.id, 'dislike', -2)">
                    👎 不推荐
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页控件 -->
          <div class="pagination-container" v-if="totalPages > 1">
            <div class="pagination">
              <!-- 首页按钮 -->
              <button 
                class="pagination-btn pagination-first" 
                @click="goToFirstPage"
                :disabled="currentPage === 1"
                title="首页"
              >
                ⏮
              </button>
              
              <!-- 上一页按钮 -->
              <button 
                class="pagination-btn pagination-prev" 
                @click="goToPreviousPage"
                :disabled="currentPage === 1"
                title="上一页"
              >
                ◀
              </button>
              
              <!-- 页码按钮 -->
              <button
                v-for="page in getPageNumbers()"
                :key="page"
                class="pagination-btn pagination-number"
                :class="{ active: page === currentPage }"
                @click="goToPage(page)"
              >
                {{ page }}
              </button>
              
              <!-- 下一页按钮 -->
              <button 
                class="pagination-btn pagination-next" 
                @click="goToNextPage"
                :disabled="currentPage === totalPages"
                title="下一页"
              >
                ▶
              </button>
              
              <!-- 末页按钮 -->
              <button 
                class="pagination-btn pagination-last" 
                @click="goToLastPage"
                :disabled="currentPage === totalPages"
                title="末页"
              >
                ⏭
              </button>
            </div>
            
            <!-- 分页信息 -->
            <div class="pagination-info">
              <span class="pagination-text">
                显示第 {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, totalProducts) }} 条，
                共 {{ totalProducts }} 条记录
              </span>
            </div>
          </div>
        </section>


        <!-- 推荐区域 -->
        <section class="recommendations-section">
        <div class="recommendations-header">
          <h2 class="recommendations-title">🎯 个性化推荐</h2>
          <button class="update-profile-btn" @click="updateUserProfile" :disabled="updatingProfile">
            🎨 {{ updatingProfile ? '更新中...' : '更新用户画像' }}
          </button>
        </div>
          
          <!-- 加载中状态 -->
          <div v-if="loadingRecommendations" class="loading-state">
            <div class="loading-icon">⏳</div>
            <div class="loading-text">正在加载推荐数据...</div>
          </div>
          
          <!-- 有推荐数据时显示推荐商品 -->
          <div v-else-if="currentRecommendations.length > 0" class="recommendations-content recommendations-content-loaded">
            <div class="recommendations-grid">
              <div v-for="product in currentRecommendations" :key="product.id" class="recommendation-card">
                <div class="recommendation-image">
                  <img :src="product.image_url || 'https://via.placeholder.com/280x200/00ff00/ffffff?text=' + encodeURIComponent(product.name)" 
                       :alt="product.name" 
                       @error="handleImageError">
                </div>
                <div class="recommendation-info">
                  <h3 class="recommendation-title">{{ product.name }}</h3>
                  <div class="recommendation-tags">
                    <span v-for="tag in product.tags" :key="tag" class="recommendation-tag">{{ tag }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 推荐商品分页 -->
            <div class="pagination" v-if="recommendationTotalPages > 1">
              <button @click="goToRecommendationPage(recommendationCurrentPage - 1)" :disabled="recommendationCurrentPage <= 1" class="page-btn">
                ← 上一页
              </button>
              <span class="page-info">
                第 {{ recommendationCurrentPage }} 页，共 {{ recommendationTotalPages }} 页
              </span>
              <button @click="goToRecommendationPage(recommendationCurrentPage + 1)" :disabled="recommendationCurrentPage >= recommendationTotalPages" class="page-btn">
                下一页 →
              </button>
            </div>
          </div>
          
          <!-- 没有推荐数据时显示提示 -->
          <div v-else class="no-recommendations">
            <div class="no-recommendations-icon">🎯</div>
            <div class="no-recommendations-title">暂无推荐商品</div>
            <div class="no-recommendations-description">
              请先进行商品交互，然后点击"更新用户画像"按钮<br>
              系统会根据您的交互行为生成专属推荐列表
            </div>
          </div>
        </section>
          </div>
    </main>

    <!-- 交互历史弹窗 -->
    <div class="history-modal" :class="{ show: showHistoryModal }" @click="closeHistoryModal">
      <div class="history-modal-content" @click.stop>
        <div class="history-modal-header">
          <h2 class="history-modal-title">📋 交互历史</h2>
          <button class="history-modal-close" @click="closeHistoryModal">&times;</button>
          </div>
          
        <div class="history-content">
          <div v-if="userInteractions.length === 0" class="history-empty">
            <div class="history-empty-icon">📋</div>
            <div class="history-empty-text">暂无交互历史</div>
            <div class="history-empty-description">开始与商品交互，您的行为将记录在这里</div>
            </div>
          <div v-else>
            <div
              v-for="product in sortedProductScores"
              :key="product.productId"
              class="history-item"
            >
              <div class="history-product-info">
                <div class="history-product-name">{{ product.productName }}</div>
                <div class="history-product-category">{{ product.productCategory }}</div>
              </div>
              <div class="history-score-section">
                <div class="history-total-score" :class="getScoreClass(product.totalScore)">
                  {{ product.totalScore > 0 ? '+' + product.totalScore : product.totalScore }}
            </div>
                <div class="score-label">{{ getScoreLabel(product.totalScore) }}</div>
          </div>
            </div>
          </div>
        </div>
        
        <div class="history-modal-footer">
          <button class="history-modal-btn" @click="closeHistoryModal">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, nextTick, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { productAPI, recommendationAPI, userAPI } from '@/utils/api'

export default {
  name: 'UserInteraction',
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const currentUser = ref(null)
    const userInteractions = ref([])
    const currentProducts = ref([])
    
    // 使用reactive对象管理推荐状态，提供更稳定的响应式更新
    const recommendationState = reactive({
      data: [],
      loading: false,
      updating: false,
      lastUpdate: 0,
      requestId: null
    })
    
    // 保持向后兼容的ref引用
    const currentRecommendations = computed(() => recommendationState.data)
    const loadingRecommendations = computed(() => recommendationState.loading)
    const updatingProfile = ref(false)
    const showHistoryModal = ref(false)
    const lastRecommendationUpdate = computed(() => recommendationState.lastUpdate)
    const searchQuery = ref('')
    const loading = ref(false)
    
    // 分页相关数据
    const currentPage = ref(1)
    const pageSize = ref(12)
    const totalPages = ref(0)
    const totalProducts = ref(0)
    const searchType = ref('semantic')
    
    // 推荐商品分页相关数据
    const recommendationCurrentPage = ref(1)
    const recommendationPageSize = ref(24) // 增加推荐商品数量从12个到24个
    const recommendationTotalPages = ref(0)
    const recommendationTotalProducts = ref(0) // 'semantic' 或 'fuzzy'

    // 计算属性
    const totalScore = computed(() => {
      return userInteractions.value.reduce((sum, interaction) => sum + interaction.score, 0)
    })

    const sortedProductScores = computed(() => {
      const productScores = {}
      
      userInteractions.value.forEach(interaction => {
        const productId = interaction.productId
        const productName = interaction.productName
        const productCategory = getProductCategory(productName)
        
        if (!productScores[productId]) {
          productScores[productId] = {
            productId: productId,
            productName: productName,
            productCategory: productCategory,
            totalScore: 0,
            lastInteraction: interaction.timestamp
          }
        }
        
        productScores[productId].totalScore += interaction.score
        
        if (new Date(interaction.timestamp) > new Date(productScores[productId].lastInteraction)) {
          productScores[productId].lastInteraction = interaction.timestamp
        }
      })
      
      return Object.values(productScores).sort((a, b) => b.totalScore - a.totalScore)
    })

    // 方法
    const initializeUser = async () => {
      const userId = localStorage.getItem('currentUserId')
      if (!userId) {
        // 如果没有用户ID，跳转到登录页面
        ElMessage.warning('请先登录')
        router.push('/user-login')
        return
      }
      
      try {
        // 尝试从后端获取用户信息
        const response = await userAPI.getUser(userId)
        currentUser.value = {
          id: response.data.id,
          name: response.data.username || `用户${userId}`,
          email: response.data.email || `${userId}@example.com`
        }
        loadUserInteractions()
      } catch (error) {
        console.error('获取用户信息失败:', error)
        // 如果用户不存在，尝试创建测试用户
        try {
          await registerTestUser()
        } catch (registerError) {
          console.error('创建测试用户失败:', registerError)
          // 使用模拟数据作为最后备选
          currentUser.value = {
            id: userId,
            name: `用户${userId}`,
            email: `${userId}@example.com`
          }
          loadUserInteractions()
        }
      }
    }

    const registerTestUser = async () => {
      try {
        const userId = localStorage.getItem('currentUserId') || 'testuser'
        const response = await userAPI.register({
          user_id: userId,
          username: userId,
          email: `${userId}@example.com`
        })
        
        currentUser.value = {
          id: response.data.id,
          name: response.data.username,
          email: response.data.email
        }
        localStorage.setItem('currentUserId', response.data.id.toString())
        ElMessage.success('用户注册成功')
        
        loadUserInteractions()
      } catch (error) {
        console.error('用户注册失败:', error)
        ElMessage.error('用户注册失败，使用模拟数据')
        
        // 使用模拟用户
        const userId = localStorage.getItem('currentUserId') || '1'
        currentUser.value = {
          id: userId,
          name: `用户${userId}`,
          email: `${userId}@example.com`
        }
        localStorage.setItem('currentUserId', userId)
        loadUserInteractions()
      }
    }

    const getUserAvatar = (userName) => {
      if (!userName) return '👤'
      const avatars = ['👤', '👨', '👩', '🧑', '👨‍💻', '👩‍💻', '👨‍🎨', '👩‍🎨']
      const hash = userName.split('').reduce((a, b) => a + b.charCodeAt(0), 0)
      return avatars[hash % avatars.length]
    }

    const loadUserInteractions = async () => {
      if (!currentUser.value) return
      
      try {
        // 调用后端API获取真实的用户交互历史
        const response = await userAPI.getUserInteractions(currentUser.value.id, { per_page: 100 })
        const interactions = response.data?.interactions || []
        
        // 转换为前端需要的格式
        userInteractions.value = interactions.map(interaction => ({
          productId: interaction.product_id,
          productName: interaction.product?.name || '未知商品',
          interactionType: interaction.interaction_type,
          score: interaction.interaction_score,
          timestamp: new Date(interaction.created_at)
        }))
        
        console.log('加载用户交互历史成功:', userInteractions.value.length, '条记录')
        
        // 加载交互历史后自动更新推荐数据（强制刷新）
        console.log('🔄 开始加载推荐数据...')
        await updateRecommendations(true)
        console.log('✅ 推荐数据加载完成')
      } catch (error) {
        console.error('获取用户交互历史失败:', error)
        // 如果API失败，使用空数组而不是模拟数据
        userInteractions.value = []
        ElMessage.warning('无法加载交互历史，请稍后重试')
      }
    }

    const performSemanticSearch = async (page = 1) => {
      if (!searchQuery.value.trim()) {
        ElMessage.warning('请输入搜索关键词')
        return
      }
      
      loading.value = true
      searchType.value = 'semantic'
      currentPage.value = page
      
      try {
        // 调用语义搜索API，支持分页
        const response = await productAPI.semanticSearch(searchQuery.value, { 
          page: page,
          per_page: pageSize.value
        })
        
        const products = response.data?.products || []
        const pagination = response.data?.pagination || {}
        
        // 清理图片URL，移除损坏的字符
        currentProducts.value = products.map(product => ({
          ...product,
          image_url: cleanImageUrl(product.image_url)
        }))
        
        // 更新分页信息
        totalPages.value = pagination.pages || 0
        totalProducts.value = pagination.total || 0
        
        if (currentProducts.value.length === 0) {
          ElMessage.info('未找到相关商品')
        } else {
          ElMessage.success(`找到 ${totalProducts.value} 个相关商品，当前第 ${page} 页`)
        }
      } catch (error) {
        console.error('语义搜索失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        
        // 清空商品列表
        currentProducts.value = []
        totalPages.value = 0
        totalProducts.value = 0
        
        // 显示错误信息
        const errorMessage = error.response?.data?.message || error.message || '搜索失败'
        ElMessage.error(`语义搜索失败: ${errorMessage}`)
      } finally {
        loading.value = false
      }
    }

    const performFuzzySearch = async (page = 1) => {
      if (!searchQuery.value.trim()) {
        ElMessage.warning('请输入搜索关键词')
        return
      }
      
      loading.value = true
      searchType.value = 'fuzzy'
      currentPage.value = page
      
      try {
        // 调用模糊搜索API，支持分页
        const response = await productAPI.fuzzySearch(searchQuery.value, { 
          page: page,
          per_page: pageSize.value
        })
        
        const products = response.data?.products || []
        const pagination = response.data?.pagination || {}
        
        // 清理图片URL，移除损坏的字符
        currentProducts.value = products.map(product => ({
          ...product,
          image_url: cleanImageUrl(product.image_url)
        }))
        
        // 更新分页信息
        totalPages.value = pagination.pages || 0
        totalProducts.value = pagination.total || 0
        
        if (currentProducts.value.length === 0) {
          ElMessage.info('未找到相关商品')
        } else {
          ElMessage.success(`找到 ${totalProducts.value} 个相关商品，当前第 ${page} 页`)
        }
      } catch (error) {
        console.error('模糊搜索失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        
        // 清空商品列表
        currentProducts.value = []
        totalPages.value = 0
        totalProducts.value = 0
        
        // 显示错误信息
        const errorMessage = error.response?.data?.message || error.message || '搜索失败'
        ElMessage.error(`模糊搜索失败: ${errorMessage}`)
      } finally {
        loading.value = false
      }
    }

    const cleanImageUrl = (url) => {
      if (!url) return null
      
      // 移除URL中的损坏字符（如%01等）
      let cleanUrl = url.replace(/%01/g, '').replace(/\x01/g, '')
      
      // 处理图片格式后的多余字符串，如 .jpgxxx 后面的 xxx
      const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
      for (const ext of imageExtensions) {
        const extIndex = cleanUrl.toLowerCase().indexOf(ext)
        if (extIndex !== -1) {
          // 找到图片格式后，截取到格式结束位置
          cleanUrl = cleanUrl.substring(0, extIndex + ext.length)
          break
        }
      }
      
      // 验证URL是否有效
      if (!cleanUrl.startsWith('http')) {
        return null
      }
      
      return cleanUrl
    }

    const getMockSearchResults = () => {
      return [
        {
          id: 7,
          name: 'Samsung Galaxy S24 Ultra 256GB',
          description: '三星旗舰手机，200MP主摄像头，S Pen支持，AI功能丰富',
          price: '8999',
          tags: ['智能手机', '三星', 'AI'],
          image_url: 'https://via.placeholder.com/280x200/2196f3/ffffff?text=Galaxy+S24'
        },
        {
          id: 8,
          name: 'Nike Air Max 270 运动鞋',
          description: '经典运动鞋款，舒适透气，适合日常运动和休闲穿着',
          price: '899',
          tags: ['运动鞋', 'Nike', '休闲'],
          image_url: 'https://via.placeholder.com/280x200/ff00ff/ffffff?text=Nike+Air+Max'
        }
      ]
    }

    const recordInteraction = async (productId, interactionType, score) => {
      const product = currentProducts.value.find(p => p.id === productId) || 
                     currentRecommendations.value.find(p => p.id === productId)
      
      if (!product) {
        ElMessage.error('商品不存在')
        return
      }

      if (!currentUser.value) {
        ElMessage.warning('请先登录')
        return
      }

      const interaction = {
        user_id: currentUser.value.id,
        product_id: productId,
        interaction_type: interactionType,
        interaction_score: score
      }

      try {
        // 调用API记录交互
        const response = await userAPI.recordUserInteraction(interaction)
        
        // 添加到本地交互历史
        const localInteraction = {
          productId: productId,
          productName: product.name,
          interactionType: interactionType,
          score: score,
          timestamp: new Date()
        }
        userInteractions.value.push(localInteraction)
        
        // 显示反馈
        showInteractionFeedback(localInteraction)
        
        // 移除自动更新推荐的逻辑
        // 只有刷新页面和更新用户画像成功后，才应该刷新个性化推荐列表
        // setTimeout(() => {
        //   updateRecommendations()
        // }, 1000)
        
        console.log('交互记录成功:', localInteraction)
        
      } catch (error) {
        console.error('记录交互失败:', error)
        ElMessage.error('记录交互失败，请稍后重试')
        
        // 即使API失败，也添加到本地历史（用于演示）
        const localInteraction = {
          productId: productId,
          productName: product.name,
          interactionType: interactionType,
          score: score,
          timestamp: new Date()
        }
        userInteractions.value.push(localInteraction)
        showInteractionFeedback(localInteraction)
      }
    }

    const showInteractionFeedback = (interaction) => {
      const feedbackMessages = {
        'click': '👆 已记录点击行为',
        'view': '👁 已记录查看行为',
        'favorite': '❤ 已添加到收藏',
        'purchase': '🛒 已记录购买行为',
        'dislike': '👎 已记录不推荐'
      }

      const message = feedbackMessages[interaction.interactionType] || '✅ 交互已记录'
      ElMessage.success(message)
    }

    const updateUserProfile = async () => {
      if (!currentUser.value) {
        ElMessage.error('用户未登录')
        return
      }
      
      updatingProfile.value = true
      
      try {
        console.log('开始更新用户画像，用户ID:', currentUser.value.id)
        
        // 调用更新用户画像API
        const response = await recommendationAPI.updateUserProfile(currentUser.value.id)
        console.log('更新用户画像API响应:', response)
        
        if (response.success) {
          // 显示成功弹窗
          ElMessage({
            message: `用户画像更新成功！共处理 ${response.interaction_count || 0} 条交互记录`,
            type: 'success',
            duration: 3000,
            showClose: true
          })
          
          // 自动刷新推荐列表
          console.log('开始刷新推荐列表...')
          await updateRecommendations(true)
          
          // 显示推荐列表刷新成功提示
          ElMessage({
            message: '推荐列表已根据新的用户画像更新！',
            type: 'success',
            duration: 2000,
            showClose: true
          })
          
        } else {
          ElMessage.error(response.error || '用户画像更新失败')
        }
      } catch (error) {
        console.error('🔴 更新用户画像失败:', error)
        
        // 显示错误弹窗
        const errorMessage = error.response?.data?.error || error.message || '更新失败'
        ElMessage({
          message: `更新用户画像失败: ${errorMessage}`,
          type: 'error',
          duration: 5000,
          showClose: true
        })
      } finally {
        // 重置加载状态
        updatingProfile.value = false
      }
    }

    const updateRecommendations = async (force = false) => {
      if (!currentUser.value) {
        recommendationState.data = []
        return
      }
      
      // 防重复调用：如果距离上次更新不到500毫秒，且不是强制更新，则跳过
      const now = Date.now()
      if (!force && now - recommendationState.lastUpdate < 500) {
        console.log('跳过重复的推荐更新请求')
        return
      }
      
      // 状态更新锁：防止并发更新
      if (recommendationState.updating) {
        console.log('推荐更新正在进行中，跳过重复请求')
        return
      }
      
      // 生成唯一请求ID，用于追踪数据一致性
      const requestId = `req_${now}_${Math.random().toString(36).substr(2, 9)}`
      console.log(`🔄 开始推荐更新 [${requestId}]`, {
        userId: currentUser.value.id,
        force,
        timestamp: new Date().toISOString()
      })
      
      // 原子化状态更新
      recommendationState.updating = true
      recommendationState.loading = true
      recommendationState.lastUpdate = now
      recommendationState.requestId = requestId
      
      try {
        console.log('开始获取推荐数据，用户ID:', currentUser.value.id)
        const response = await recommendationAPI.getPersonalizedRecommendations(currentUser.value.id, { 
          limit: recommendationPageSize.value,
          page: recommendationCurrentPage.value
        })
        
        console.log(`📥 API响应 [${requestId}]:`, response)
        const recommendations = response.recommendations || []
        console.log(`📊 提取的推荐数据 [${requestId}]:`, recommendations.length, '个商品')
        
        // 验证数据完整性
        if (!Array.isArray(recommendations)) {
          console.error(`❌ 推荐数据格式错误 [${requestId}]:`, recommendations)
          throw new Error('推荐数据格式错误')
        }
        
        // 原子化数据更新：一次性设置所有状态
        console.log(`📝 设置新推荐数据 [${requestId}]:`, recommendations.slice(0, 3).map(r => r.name))
        
        // 使用Object.assign确保原子化更新
        Object.assign(recommendationState, {
          data: [...recommendations], // 使用展开运算符创建新数组
          loading: false,
          updating: false
        })
        
        // 计算分页信息
        recommendationTotalProducts.value = recommendations.length
        recommendationTotalPages.value = Math.ceil(recommendationTotalProducts.value / recommendationPageSize.value)
        
        console.log(`✅ 推荐数据更新成功 [${requestId}]:`, recommendationState.data.length, '个商品')
        console.log(`📋 当前推荐数据 [${requestId}]:`, recommendationState.data.slice(0, 3).map(r => r.name))
      } catch (error) {
        console.error('获取推荐失败:', error)
        console.error('错误详情:', {
          message: error.message,
          code: error.code,
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data
        })
        console.log('推荐API失败，清空推荐数据')
        // API失败时清空推荐数据，显示"暂无推荐数据"状态
        Object.assign(recommendationState, {
          data: [],
          loading: false,
          updating: false
        })
        recommendationTotalProducts.value = 0
        recommendationTotalPages.value = 0
      } finally {
        // 确保状态重置
        recommendationState.loading = false
        recommendationState.updating = false
      }
    }

    const getMockRecommendations = () => {
      return [
      {
        id: 4,
          name: 'iPad Pro 12.9英寸 M2芯片',
          description: '专业级平板电脑，支持Apple Pencil，适合创作和办公',
          price: '8999',
          tags: ['平板电脑', '苹果', '专业'],
          image_url: 'https://via.placeholder.com/280x200/00ffff/ffffff?text=iPad+Pro'
      },
      {
        id: 5,
          name: 'Sony WH-1000XM5 降噪耳机',
          description: '业界领先的降噪技术，30小时续航，支持快速充电',
          price: '2299',
          tags: ['耳机', '降噪', '无线'],
          image_url: 'https://via.placeholder.com/280x200/ff00ff/ffffff?text=Sony+耳机'
        },
        {
          id: 6,
          name: 'Apple Watch Series 9',
          description: '智能手表，健康监测，GPS定位，防水设计',
          price: '2999',
          tags: ['智能手表', '健康', '运动'],
          image_url: 'https://via.placeholder.com/280x200/00ff00/ffffff?text=Apple+Watch'
        }
      ]
    }

    const refreshRecommendations = async () => {
      loadingRecommendations.value = true
      try {
        await updateRecommendations(true) // 强制更新
        ElMessage.success('推荐已刷新')
      } catch (error) {
        ElMessage.error('刷新推荐失败')
      } finally {
        loadingRecommendations.value = false
      }
    }

    const showInteractionHistory = () => {
      showHistoryModal.value = true
    }

    const closeHistoryModal = () => {
      showHistoryModal.value = false
    }

    const getScoreClass = (score) => {
      if (score >= 10) return 'score-excellent'
      if (score >= 5) return 'score-good'
      if (score >= 0) return 'score-neutral'
      return 'score-poor'
    }

    const getScoreLabel = (score) => {
      if (score >= 10) return '非常喜欢'
      if (score >= 5) return '喜欢'
      if (score >= 0) return '一般'
      return '不喜欢'
    }

    const getProductCategory = (productName) => {
      const categoryMap = {
        'iPhone': '手机数码',
        'MacBook': '电脑办公',
        'AirPods': '手机数码',
        'iPad': '电脑办公',
        'Sony': '手机数码',
        'Nike': '运动户外',
        'Samsung': '手机数码',
        'Galaxy': '手机数码',
        'Apple Watch': '手机数码'
      }
      
      for (const [keyword, category] of Object.entries(categoryMap)) {
        if (productName.includes(keyword)) {
          return category
        }
      }
      
      return '其他'
    }

    // 移除scrollToSearch和scrollToRecommendations函数，因为对应的按钮已被移除

    const logout = () => {
      if (confirm('确定要退出当前用户吗？')) {
        localStorage.removeItem('currentUserId')
        ElMessage.success('已退出登录')
        // 跳转到登录页面
        router.push('/user-login')
      }
    }

    // 分页相关方法
    const goToPage = (page) => {
      if (page < 1 || page > totalPages.value || page === currentPage.value) {
        return
      }
      
      if (searchType.value === 'semantic') {
        performSemanticSearch(page)
      } else {
        performFuzzySearch(page)
      }
    }

    const goToRecommendationPage = (page) => {
      if (page >= 1 && page <= recommendationTotalPages.value) {
        recommendationCurrentPage.value = page
        updateRecommendations(true) // 强制更新推荐数据
      }
    }

    const goToPreviousPage = () => {
      if (currentPage.value > 1) {
        goToPage(currentPage.value - 1)
      }
    }

    const goToNextPage = () => {
      if (currentPage.value < totalPages.value) {
        goToPage(currentPage.value + 1)
      }
    }

    const goToFirstPage = () => {
      goToPage(1)
    }

    const goToLastPage = () => {
      goToPage(totalPages.value)
    }

    // 生成页码数组
    const getPageNumbers = () => {
      const pages = []
      const maxVisible = 5 // 最多显示5个页码
      const start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
      const end = Math.min(totalPages.value, start + maxVisible - 1)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    }

    // 组件状态重置函数
    const resetComponentState = () => {
      console.log('🔄 重置组件状态')
      Object.assign(recommendationState, {
        data: [],
        loading: false,
        updating: false,
        lastUpdate: 0,
        requestId: null
      })
      recommendationTotalProducts.value = 0
      recommendationTotalPages.value = 0
    }

    // 状态一致性检查机制
    watchEffect(() => {
      // 确保推荐数据状态一致性
      if (recommendationState.data.length > 0 && recommendationTotalProducts.value === 0) {
        console.log('🔧 修复推荐数据状态不一致')
        recommendationTotalProducts.value = recommendationState.data.length
        recommendationTotalPages.value = Math.ceil(recommendationTotalProducts.value / recommendationPageSize.value)
      }
    })

    // 生命周期
    onMounted(() => {
      console.log('🚀 组件挂载开始')
      resetComponentState()
      initializeUser()
    })
    
    return {
      currentUser,
      userInteractions,
      currentProducts,
      currentRecommendations,
      searchQuery,
      loading,
      loadingRecommendations,
      updatingProfile,
      showHistoryModal,
      totalScore,
      sortedProductScores,
      // 分页相关
      currentPage,
      pageSize,
      totalPages,
      totalProducts,
      searchType,
      getUserAvatar,
      performSemanticSearch,
      performFuzzySearch,
      recordInteraction,
      updateUserProfile,
      refreshRecommendations,
      showInteractionHistory,
      closeHistoryModal,
      getScoreClass,
      getScoreLabel,
      logout,
      // 分页方法
      goToPage,
      goToPreviousPage,
      goToNextPage,
      goToFirstPage,
      goToLastPage,
      getPageNumbers,
      // 推荐商品分页方法
      goToRecommendationPage,
      recommendationCurrentPage,
      recommendationPageSize,
      recommendationTotalPages,
      recommendationTotalProducts
    }
  }
}
</script>

<style lang="scss" scoped>
.user-interaction-page {
  min-height: 100vh;
  background: #0a0a0a;
  color: #ffffff;
  font-family: 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  overflow-x: hidden;
}

/* 背景动画 */
.bg-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: 
    radial-gradient(circle at 20% 50%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 0, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 80%, rgba(0, 255, 0, 0.1) 0%, transparent 50%);
  animation: backgroundMove 20s ease-in-out infinite;
}

@keyframes backgroundMove {
  0%, 100% { transform: translateX(0) translateY(0); }
  25% { transform: translateX(-2%) translateY(-2%); }
  50% { transform: translateX(2%) translateY(-1%); }
  75% { transform: translateX(-1%) translateY(2%); }
}

/* 顶部导航栏 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(10, 10, 10, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
  z-index: 1000;
  padding: 0 5%;
}
  
.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
  height: 70px;
  max-width: 1200px;
    margin: 0 auto;
  }
  
.logo {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  }
  
  .nav-menu {
    display: flex;
  list-style: none;
    gap: 2rem;
  margin: 0;
  padding: 0;
}
    
.nav-item a, .nav-item span {
  color: #ffffff;
      text-decoration: none;
      font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.nav-item a:hover {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
}

.nav-item.active span {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
}

/* 下拉菜单样式 */
.dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: rgba(10, 10, 10, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 12px;
  min-width: 200px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 999;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  pointer-events: none;
}

.dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  pointer-events: auto;
}

.dropdown-item {
  display: block;
  padding: 1rem 1.5rem;
  color: #ffffff;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  text-align: left;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  color: #ff4444;
  background: rgba(255, 68, 68, 0.1);
  padding-left: 2rem;
}

.dropdown-item.active {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
}

.dropdown-toggle::after {
  content: '▼';
  font-size: 0.7rem;
  margin-left: 0.5rem;
  transition: transform 0.3s ease;
}

.dropdown:hover .dropdown-toggle::after {
  transform: rotate(180deg);
}

/* 主要内容区域 */
.main-content {
  margin-top: 70px;
  padding: 2rem 5%;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 用户信息栏 */
.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 2rem;
  background: rgba(0, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 15px;
  margin: 1rem 0;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #ffffff;
}

.user-details {
  flex: 1;
}

.user-name {
    font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.2rem;
}

.user-stats {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.user-actions {
    display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 移除btn-search和btn-recommend样式，因为对应的按钮已被移除 */

.btn-history {
  background: linear-gradient(45deg, #9C27B0, #E91E63);
  color: #ffffff;
}

.btn-logout {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #ffffff;
}

.btn-small:hover {
  transform: translateY(-1px);
}

/* 搜索区域 */
.search-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}
  
.search-container {
    display: flex;
  flex-direction: column;
  gap: 1.5rem;
    align-items: center;
}

.search-bar {
  width: 100%;
  max-width: 600px;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(0, 255, 255, 0.2);
  border-radius: 50px;
  color: #ffffff;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.search-input:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.08);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-buttons {
    display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.search-btn {
  padding: 0.8rem 2rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  color: #ffffff;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.4);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.search-btn.secondary {
  background: linear-gradient(45deg, #ff6b6b, #ffa500);
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
}

.search-btn.secondary:hover:not(:disabled) {
  box-shadow: 0 10px 25px rgba(255, 107, 107, 0.4);
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 20px;
  margin-bottom: 2rem;
  min-height: 200px; /* 设置最小高度，与推荐内容区域保持一致 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease; /* 添加平滑过渡效果 */
}

.loading-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.7;
  animation: spin 2s linear infinite;
}

.loading-text {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 检索商品区域 */
.search-results-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.search-results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.search-results-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #00ffff;
  margin: 0;
}

.search-results-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-type {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.search-count {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

/* 推荐内容区域 */
.recommendations-content {
  overflow: hidden; /* 防止出现滚动条 */
  width: 100%;
  min-height: 200px; /* 设置最小高度，防止内容切换时高度变化 */
  transition: all 0.3s ease; /* 添加平滑过渡效果 */
}

/* 推荐内容加载完成后的样式 */
.recommendations-content-loaded {
  opacity: 1;
  transform: translateY(0);
}

/* 推荐商品网格 */
.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  overflow: hidden; /* 防止网格溢出 */
  min-height: 150px; /* 设置最小高度，保持布局稳定 */
}

.recommendation-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.recommendation-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 255, 255, 0.4);
  box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2);
}

.recommendation-image {
  width: 100%;
  height: 150px;
  overflow: hidden;
  position: relative;
}

.recommendation-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.recommendation-card:hover .recommendation-image img {
  transform: scale(1.05);
}

.recommendation-info {
  padding: 1rem;
}

.recommendation-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.recommendation-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.recommendation-tag {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* 暂无推荐数据 */
.no-recommendations {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 20px;
  margin-bottom: 2rem;
  min-height: 200px; /* 设置最小高度，与其他状态保持一致 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease; /* 添加平滑过渡效果 */
}

.no-recommendations-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-recommendations-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.8);
}

.no-recommendations-description {
  font-size: 1rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 2rem;
}

/* 搜索结果信息 */
.search-results-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem 1.5rem;
  background: rgba(0, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 12px;
}

.results-summary {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.results-count {
  font-size: 1.1rem;
  font-weight: 600;
  color: #00ffff;
}

.results-page {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.search-type-indicator {
  display: flex;
  align-items: center;
}

.search-type-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.search-type-badge.semantic {
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  color: #ffffff;
}

.search-type-badge.fuzzy {
  background: linear-gradient(45deg, #ff6b6b, #ffa500);
  color: #ffffff;
}

/* 商品网格 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.product-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 15px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: visible;
      display: flex;
  flex-direction: column;
  height: 100%;
}

.product-card:hover {
  transform: translateY(-5px);
  border-color: #00ffff;
  box-shadow: 0 15px 30px rgba(0, 255, 255, 0.2);
}

.product-image {
  width: 100%;
  height: 200px;
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
  border-radius: 10px;
  margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
  font-size: 3rem;
  color: rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.product-info {
  text-align: left;
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-content: space-between;
}

.product-details {
      flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
      
      .product-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.5rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.8rem;
}

.product-description {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  margin-bottom: 1rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.7rem;
}

.product-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: #00ffff;
  margin-bottom: 1rem;
  min-height: 1.5rem;
}

.product-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.product-tag {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
  border: 1px solid rgba(0, 255, 255, 0.2);
}

/* 交互按钮组 */
.interaction-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  margin-top: auto;
}

.interaction-btn {
  padding: 0.6rem 0.8rem;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  min-height: 40px;
        display: flex;
        align-items: center;
  justify-content: center;
  gap: 0.3rem;
}

.btn-click {
  background: linear-gradient(45deg, #4CAF50, #8BC34A);
  color: #ffffff;
}

.btn-view {
  background: linear-gradient(45deg, #2196F3, #03A9F4);
  color: #ffffff;
}

.btn-favorite {
  background: linear-gradient(45deg, #E91E63, #F06292);
  color: #ffffff;
}

.btn-purchase {
  background: linear-gradient(45deg, #FF9800, #FFC107);
  color: #ffffff;
}

.btn-dislike {
  background: linear-gradient(45deg, #F44336, #E57373);
  color: #ffffff;
}

.interaction-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.interaction-btn:active {
  transform: translateY(0);
}

/* 推荐区域 */
.recommendations-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden; /* 防止推荐区域出现滚动条 */
  min-height: 300px; /* 设置最小高度，防止加载时高度变化 */
}

.recommendations-header {
      display: flex;
  justify-content: space-between;
      align-items: center;
  margin-bottom: 2rem;
}

.recommendations-title {
        font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.update-profile-btn {
  padding: 0.8rem 1.5rem;
  background: linear-gradient(45deg, #4ecdc4, #44a08d);
  color: #ffffff;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.update-profile-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4);
}

.update-profile-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 交互历史弹窗 */
.history-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  z-index: 2000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.history-modal.show {
          display: flex;
}

.history-modal-content {
  background: rgba(10, 10, 10, 0.95);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 20px;
  max-width: 800px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.history-modal-header {
  display: flex;
  justify-content: space-between;
          align-items: center;
  padding: 2rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
}

.history-modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(45deg, #9C27B0, #E91E63);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.history-modal-close {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.history-modal-close:hover {
  color: #ff4444;
  background: rgba(255, 68, 68, 0.1);
}

.history-content {
  padding: 2rem;
  max-height: 50vh;
  overflow-y: auto;
}

/* 简化的商品评分展示样式 */
.history-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
        display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

.history-item:hover {
  border-color: #9C27B0;
  box-shadow: 0 8px 25px rgba(156, 39, 176, 0.2);
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.08);
}

.history-product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.history-product-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffffff;
  line-height: 1.3;
  margin: 0;
}

.history-product-category {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

.history-score-section {
      display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.history-total-score {
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  font-size: 1.2rem;
  font-weight: 700;
  text-align: center;
  min-width: 80px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.score-excellent {
  background: linear-gradient(135deg, #4CAF50, #8BC34A);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
}

.score-good {
  background: linear-gradient(135deg, #FF9800, #FFC107);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
}

.score-neutral {
  background: linear-gradient(135deg, #2196F3, #03A9F4);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
}

.score-poor {
  background: linear-gradient(135deg, #F44336, #E57373);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
}

.score-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.history-empty {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.6);
}

.history-empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.history-empty-text {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
}

.history-empty-description {
  font-size: 1rem;
}

.history-modal-footer {
  padding: 2rem;
  border-top: 1px solid rgba(0, 255, 255, 0.1);
  text-align: center;
}

.history-modal-btn {
  padding: 0.8rem 2rem;
  background: linear-gradient(45deg, #9C27B0, #E91E63);
  color: #ffffff;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.history-modal-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(156, 39, 176, 0.4);
}

/* 分页控件 */
.pagination-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 15px;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.pagination-btn {
  padding: 0.8rem 1rem;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(0, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.pagination-number {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.pagination-number.active {
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  color: #ffffff;
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
}

.pagination-first,
.pagination-last {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.pagination-prev,
.pagination-next {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.pagination-info {
  text-align: center;
}

.pagination-text {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }
  
  .main-content {
    padding: 1rem 2%;
  }
  
  .user-info {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .user-actions {
    width: 100%;
    justify-content: center;
  }

  .search-buttons {
    flex-direction: column;
    width: 100%;
    max-width: 300px;
  }

  .search-btn {
    width: 100%;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  .interaction-buttons {
    grid-template-columns: repeat(2, 1fr);
  }

  .search-results-info {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .pagination {
    gap: 0.3rem;
  }

  .pagination-btn {
    padding: 0.6rem 0.8rem;
    font-size: 0.8rem;
    min-width: 35px;
    height: 35px;
  }

  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .history-product-info {
    width: 100%;
  }
  
  .history-score-section {
    align-self: flex-end;
  }
  
  .history-total-score {
    min-width: 70px;
    padding: 0.6rem 1.2rem;
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .products-grid {
    grid-template-columns: 1fr;
  }

  .product-card {
    padding: 1rem;
  }

  .product-image {
    height: 150px;
  }

  .interaction-buttons {
    grid-template-columns: 1fr;
  }
}
</style>

