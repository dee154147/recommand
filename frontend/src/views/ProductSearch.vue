<template>
  <div class="product-search">
    <!-- 背景动画层 -->
    <div class="bg-animation"></div>
    
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="logo">智能推荐系统</div>
        <ul class="nav-menu">
          <li class="nav-item"><router-link to="/" class="nav-link">首页</router-link></li>
          <li class="nav-item"><a href="#features" class="nav-link">产品特性</a></li>
          <li class="nav-item"><a href="#team" class="nav-link">团队介绍</a></li>
          <li class="nav-item"><a href="#contact" class="nav-link">联系我们</a></li>
          <li class="nav-item dropdown">
            <a href="#" class="nav-link dropdown-toggle">功能演示</a>
            <div class="dropdown-menu">
              <router-link to="/product-search" class="dropdown-item active">商品检索</router-link>
              <router-link to="/product-management" class="dropdown-item">商品管理</router-link>
              <router-link to="/user-interaction" class="dropdown-item">用户交互</router-link>
            </div>
          </li>
        </ul>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="container">
        <!-- 搜索区域 -->
        <section class="search-section">
          <div class="search-container">
            <h1 class="page-title">商品检索</h1>
            <p class="page-subtitle">智能搜索，快速找到您需要的商品</p>
            
            <!-- 搜索框 -->
            <div class="search-bar">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="请输入商品名称或关键词..."
                class="search-input"
                @keyup.enter="performSearch"
                @input="onSearchInput"
              />
            </div>
            
            <!-- 搜索按钮组 -->
            <div class="search-buttons">
              <button
                @click="performFuzzySearch"
                :class="['search-btn', { active: searchType === 'fuzzy' }]"
              >
                模糊匹配
              </button>
              <button
                @click="performSemanticSearch"
                :class="['search-btn', { active: searchType === 'semantic' }]"
              >
                语义检索
              </button>
            </div>
            
            <!-- 分类筛选已移除 -->
          </div>
        </section>
        
        <!-- 搜索结果区域 -->
        <section class="results-section">
          <!-- 结果统计 -->
          <div v-if="searchResults" class="results-header">
            <div class="results-info">
              <span class="results-count">
                找到 {{ searchResults.pagination.total }} 个商品
              </span>
              <span class="search-info">
                {{ searchResults.search_info.type === 'fuzzy' ? '模糊匹配' : '语义检索' }}：
                "{{ searchResults.search_info.query }}"
              </span>
            </div>
          </div>
          
          <!-- 商品网格 -->
          <div v-if="searchResults && searchResults.products.length > 0" class="products-grid">
            <div
              v-for="product in searchResults.products"
              :key="product.id"
              class="product-card"
            >
              <div class="product-image">
                <img
                  :src="getProductImage(product.image_url)"
                  :alt="product.name"
                  @error="handleImageError"
                />
                <div class="product-overlay">
                  <div class="product-id">ID: {{ product.id }}</div>
                </div>
              </div>
              <div class="product-info">
                <h3 class="product-name">{{ product.name }}</h3>
                <div class="product-tags">
                  <span
                    v-for="tag in product.tags.slice(0, 5)"
                    :key="tag"
                    class="tag"
                  >
                    {{ tag }}
                  </span>
                  <span v-if="product.tags.length > 5" class="more-tags">
                    +{{ product.tags.length - 5 }}
                  </span>
                </div>
                <div v-if="product.match_score" class="match-score">
                  匹配度: {{ (product.match_score * 100).toFixed(1) }}%
                </div>
                <button 
                  @click="showSimilarProducts(product)"
                  class="similar-btn"
                >
                  🔍 查找相似商品
                </button>
              </div>
            </div>
          </div>
          
          <!-- 无结果 -->
          <div v-else-if="searchResults && searchResults.products.length === 0" class="no-results">
            <div class="no-results-icon">
              <i class="icon">🔍</i>
            </div>
            <h3>未找到相关商品</h3>
            <p>请尝试其他关键词或调整搜索条件</p>
          </div>
          
          <!-- 分页 -->
          <div v-if="searchResults && searchResults.pagination.pages > 1" class="pagination">
            <button
              @click="goToPage(searchResults.pagination.page - 1)"
              :disabled="!searchResults.pagination.has_prev"
              class="page-btn"
            >
              上一页
            </button>
            
            <span class="page-info">
              第 {{ searchResults.pagination.page }} 页，共 {{ searchResults.pagination.pages }} 页
            </span>
            
            <button
              @click="goToPage(searchResults.pagination.page + 1)"
              :disabled="!searchResults.pagination.has_next"
              class="page-btn"
            >
              下一页
            </button>
          </div>
        </section>
      </div>
    </main>

    <!-- 相似商品弹窗 -->
    <div v-if="showSimilarModal" class="similar-modal" @click="closeSimilarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>相似商品推荐</h2>
          <button @click="closeSimilarModal" class="close-btn">×</button>
        </div>
        
        <div class="reference-product">
          <h3>参考商品</h3>
          <div class="reference-info">
            <div class="reference-image">
              <img 
                :src="referenceProduct.image_url || 'https://via.placeholder.com/80x80/cccccc/ffffff?text=商品图片'" 
                :alt="referenceProduct.name"
                @error="handleImageError"
              />
            </div>
            <div class="reference-details">
              <div class="reference-name">{{ referenceProduct.name }}</div>
            </div>
          </div>
        </div>
        
        <div class="similar-products-section">
          <h3>相似商品</h3>
          <div v-if="loadingSimilar" class="loading">
            <div class="loading-spinner"></div>
            <div class="loading-text">正在查找相似商品...</div>
          </div>
          <div v-else-if="similarProducts.length > 0" class="similar-grid">
            <div
              v-for="product in similarProducts"
              :key="product.product_id"
              class="similar-product-card"
            >
              <div class="similar-image">
                <img 
                  :src="product.image_url || 'https://via.placeholder.com/80x80/cccccc/ffffff?text=商品图片'" 
                  :alt="product.name"
                  @error="handleImageError"
                />
              </div>
              <div class="similar-name">{{ product.name }}</div>
              <div class="similarity-score">相似度: {{ (product.similarity * 100).toFixed(1) }}%</div>
            </div>
          </div>
          <div v-else class="no-similar">
            <div class="no-similar-icon">⚠️</div>
            <div class="no-similar-text">相似商品服务暂时不可用</div>
            <div class="no-similar-detail">请检查后端服务是否正常运行</div>
            <div class="no-similar-tip">提示：请确保后端服务在端口5002上运行</div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="closeSimilarModal" class="btn-secondary">关闭</button>
          <button @click="refreshSimilarProducts" class="btn-primary">刷新推荐</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ProductSearch',
  setup() {
    const searchQuery = ref('')
    const searchType = ref('fuzzy')
    const searchResults = ref(null)
    // 提示列表功能已移除
    const loading = ref(false)
    
    // 相似商品功能
    const showSimilarModal = ref(false)
    const referenceProduct = ref(null)
    const similarProducts = ref([])
    const loadingSimilar = ref(false)
    
    // 搜索配置
    const searchConfig = reactive({
      page: 1,
      per_page: 20
    })
    
    // 分类列表功能已移除
    
    // 搜索建议功能已移除
    
    // 执行搜索
    const performSearch = async () => {
      if (!searchQuery.value.trim()) {
        alert('请输入搜索关键词')
        return
      }
      
      loading.value = true
      
      try {
        const params = {
          q: searchQuery.value.trim(),
          type: searchType.value,
          page: searchConfig.page,
          per_page: searchConfig.per_page
        }
        
        const response = await axios.get('http://localhost:5001/api/v1/search/products', { params })
        
        if (response.data.success) {
          searchResults.value = response.data.data
        } else {
          alert('搜索失败: ' + response.data.message)
        }
      } catch (error) {
        console.error('搜索失败:', error)
        alert('搜索失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
    
    // 模糊匹配搜索
    const performFuzzySearch = () => {
      searchType.value = 'fuzzy'
      searchConfig.page = 1
      performSearch()
    }
    
    // 语义检索
    const performSemanticSearch = () => {
      searchType.value = 'semantic'
      searchConfig.page = 1
      performSearch()
    }
    
    // 搜索输入处理
    const onSearchInput = () => {
      // 输入事件处理（提示列表功能已移除）
    }
    
    // 选择搜索建议功能已移除
    
    // 分类变化处理已移除
    
    // 分页处理
    const goToPage = (page) => {
      searchConfig.page = page
      performSearch()
    }
    
    // 获取商品图片
    const getProductImage = (imageUrl) => {
      if (!imageUrl || imageUrl.trim() === '') {
        return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIyMCIgdmlld0JveD0iMCAwIDMwMCAyMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjIwIiBmaWxsPSIjMzMzIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTEwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM2NjYiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuaXoOazleiDveWKoOi9vTwvdGV4dD4KPC9zdmc+'
      }
      
      // 清理图片URL，移除特殊字符
      let cleanUrl = imageUrl.trim()
      
      // 如果URL包含特殊字符，尝试提取有效部分
      if (cleanUrl.includes('\u0001')) {
        const parts = cleanUrl.split('\u0001')
        cleanUrl = parts.find(part => part.startsWith('http'))
      }
      
      // 如果还是没有有效URL，返回占位符
      if (!cleanUrl || !cleanUrl.startsWith('http')) {
        return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIyMCIgdmlld0JveD0iMCAwIDMwMCAyMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjIwIiBmaWxsPSIjMzMzIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTEwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM2NjYiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuaXoOazleiDveWKoOi9vTwvdGV4dD4KPC9zdmc+'
      }
      
      return cleanUrl
    }
    
    // 图片错误处理
    const handleImageError = (event) => {
      event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIyMCIgdmlld0JveD0iMCAwIDMwMCAyMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjIwIiBmaWxsPSIjMzMzIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTEwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM2NjYiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuaXoOazleiDveWKoOi9vTwvdGV4dD4KPC9zdmc+'
    }
    
    // 清理图片URL - 仅用于修复相似商品列表图片显示问题
    const cleanImageUrl = (imageUrl) => {
      if (!imageUrl) return ''
      
      // 直接去掉文件扩展名之后的所有字符串
      if (imageUrl.includes('.jpg')) {
        return imageUrl.split('.jpg')[0] + '.jpg'
      } else if (imageUrl.includes('.jpeg')) {
        return imageUrl.split('.jpeg')[0] + '.jpeg'
      } else if (imageUrl.includes('.png')) {
        return imageUrl.split('.png')[0] + '.png'
      } else if (imageUrl.includes('.gif')) {
        return imageUrl.split('.gif')[0] + '.gif'
      } else if (imageUrl.includes('.webp')) {
        return imageUrl.split('.webp')[0] + '.webp'
      } else if (imageUrl.includes('.bmp')) {
        return imageUrl.split('.bmp')[0] + '.bmp'
      }
      
      return imageUrl
    }
    
    // 相似商品功能
    const showSimilarProducts = async (product) => {
      // 清理参考商品的图片URL
      const cleanedProduct = {
        ...product,
        image_url: cleanImageUrl(product.image_url)
      }
      referenceProduct.value = cleanedProduct
      showSimilarModal.value = true
      await loadSimilarProducts(product.id)
    }
    
    const loadSimilarProducts = async (productId) => {
      loadingSimilar.value = true
      similarProducts.value = []
      
      try {
        const response = await axios.get(`http://localhost:5002/api/v1/similar-products/${productId}?limit=12&threshold=0.0`)
        
        if (response.data.success) {
          similarProducts.value = response.data.data.similar_products
        } else {
          console.error('获取相似商品失败:', response.data.error)
          // 显示错误信息而不是模拟数据
          similarProducts.value = []
        }
      } catch (error) {
        console.error('API调用失败:', error)
        // 显示错误信息而不是模拟数据
        similarProducts.value = []
      } finally {
        loadingSimilar.value = false
      }
    }
    
    
    const closeSimilarModal = () => {
      showSimilarModal.value = false
      referenceProduct.value = null
      similarProducts.value = []
    }
    
    const refreshSimilarProducts = async () => {
      if (referenceProduct.value) {
        await loadSimilarProducts(referenceProduct.value.id)
      }
    }
    
    const getProductIcon = (productName) => {
      if (productName.includes('手机') || productName.includes('iPhone') || productName.includes('Samsung')) {
        return '📱'
      } else if (productName.includes('鞋') || productName.includes('Nike') || productName.includes('Adidas')) {
        return '👟'
      } else if (productName.includes('电脑') || productName.includes('MacBook') || productName.includes('笔记本')) {
        return '💻'
      } else if (productName.includes('耳机') || productName.includes('AirPods')) {
        return '🎧'
      } else if (productName.includes('平板') || productName.includes('iPad')) {
        return '📱'
      } else if (productName.includes('手表') || productName.includes('Watch')) {
        return '⌚'
      } else if (productName.includes('相机') || productName.includes('Canon')) {
        return '📷'
      } else if (productName.includes('游戏') || productName.includes('Switch')) {
        return '🎮'
      } else if (productName.includes('汽车') || productName.includes('Tesla')) {
        return '🚗'
      } else if (productName.includes('吸尘器') || productName.includes('Dyson')) {
        return '🧹'
      } else {
        return '📦'
      }
    }
    
    // 组件挂载时初始化
    onMounted(() => {
      // 初始化完成
    })
    
    return {
      searchQuery,
      searchType,
      searchResults,
      loading,
      searchConfig,
      performSearch,
      performFuzzySearch,
      performSemanticSearch,
      onSearchInput,
      goToPage,
      getProductImage,
      handleImageError,
      cleanImageUrl,
      // 相似商品功能
      showSimilarModal,
      referenceProduct,
      similarProducts,
      loadingSimilar,
      showSimilarProducts,
      closeSimilarModal,
      refreshSimilarProducts,
      getProductIcon
    }
  }
}
</script>

<style scoped>
/* 基础样式 */
.product-search {
  min-height: 100vh;
  background: #0a0a0a;
  color: #ffffff;
  font-family: 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
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
}

.nav-item a {
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

.nav-item.active a {
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
  background: rgba(20, 20, 20, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 12px;
  padding: 0.5rem 0;
  min-width: 200px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1001;
}

.dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: block;
  padding: 0.75rem 1.5rem;
  color: #ffffff;
  text-decoration: none;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 0.5rem;
}

.dropdown-item:hover {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
}

.dropdown-item.active {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
}

/* 主要内容区域 */
.main-content {
  padding-top: 70px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 搜索区域 */
.search-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 3rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.search-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff, #00ff00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
}

.page-subtitle {
  font-size: 1.1rem;
  color: #cccccc;
  margin-bottom: 1rem;
}

/* 搜索框 */
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

/* 搜索建议功能已移除 */

/* 搜索按钮组 */
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

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.4);
}

.search-btn.active {
  background: linear-gradient(45deg, #00ff00, #00ffff);
  box-shadow: 0 5px 15px rgba(0, 255, 0, 0.3);
}

.search-btn.active:hover {
  box-shadow: 0 10px 25px rgba(0, 255, 0, 0.4);
}

/* 分类筛选样式已移除 */

/* 搜索结果区域 */
.results-section {
  margin-bottom: 3rem;
}

.results-header {
  margin-bottom: 2rem;
  padding: 0 1rem;
}

.results-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-count {
  font-size: 1.2rem;
  font-weight: 600;
  color: #00ffff;
}

.search-info {
  color: #cccccc;
  font-size: 1rem;
}

/* 商品网格 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 2rem;
  margin-bottom: 3rem;
}

.product-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.product-card:hover {
  transform: translateY(-10px);
  border-color: #00ffff;
  box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  position: relative;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.product-overlay {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: #00ffff;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.product-info {
  padding: 1.5rem;
}

.product-name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #ffffff;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-category {
  margin-bottom: 1rem;
}

.category-tag {
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  color: #000000;
  padding: 6px 15px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.product-tags {
  margin-bottom: 1rem;
}

.tag {
  display: inline-block;
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  margin: 3px 6px 3px 0;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.more-tags {
  color: #888888;
  font-size: 0.8rem;
}

.match-score {
  color: #00ff00;
  font-size: 0.9rem;
  font-weight: 600;
}

/* 相似商品按钮 */
.similar-btn {
  width: 100%;
  padding: 0.8rem 1rem;
  background: linear-gradient(45deg, #ff6b6b, #ffa500) !important;
  color: #ffffff !important;
  border: 2px solid #ff6b6b !important;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.5);
  position: relative;
  z-index: 10;
  min-height: 50px;
  display: flex !important;
  align-items: center;
  justify-content: center;
}

.similar-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.6);
  background: linear-gradient(45deg, #ff5252, #ff9800) !important;
  border-color: #ff5252 !important;
}

.similar-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.5);
}

/* 无结果 */
.no-results {
  text-align: center;
  padding: 4rem 2rem;
  color: #888888;
}

.no-results-icon {
  margin-bottom: 2rem;
}

.no-results-icon .icon {
  font-size: 4rem;
  opacity: 0.3;
}

.no-results h3 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #ffffff;
}

.no-results p {
  font-size: 1.1rem;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 3rem;
}

.page-btn {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(0, 255, 255, 0.3);
  color: #ffffff;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.page-btn:hover:not(:disabled) {
  background: rgba(0, 255, 255, 0.1);
  border-color: #00ffff;
  transform: translateY(-2px);
}

.page-btn:disabled {
  background: rgba(255, 255, 255, 0.02);
  border-color: rgba(255, 255, 255, 0.1);
  color: #666666;
  cursor: not-allowed;
}

.page-info {
  color: #cccccc;
  font-weight: 500;
  font-size: 1rem;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .products-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }
}

@media (max-width: 1200px) {
  .products-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .nav-menu {
    gap: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .search-container {
    gap: 1rem;
  }
  
  .search-buttons {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .results-info {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .pagination {
    flex-direction: column;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .products-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

/* 相似商品弹窗 */
.similar-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 20px;
  max-width: 1000px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
}

.modal-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.close-btn {
  background: none;
  border: none;
  color: #ffffff;
  font-size: 2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 0, 0, 0.2);
  color: #ff6b6b;
}

.reference-product {
  padding: 2rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
}

.reference-product h3 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #00ffff;
}

.reference-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.reference-image {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid rgba(0, 255, 255, 0.3);
  background: rgba(0, 255, 255, 0.1);
}

.reference-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.reference-details {
  flex: 1;
}

.reference-name {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #ffffff;
}


.similar-products-section {
  padding: 2rem;
}

.similar-products-section h3 {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  color: #00ffff;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 255, 255, 0.3);
  border-top: 3px solid #00ffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #cccccc;
  font-size: 1rem;
}

.similar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.similar-product-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.similar-product-card:hover {
  transform: translateY(-5px);
  border-color: #00ffff;
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.2);
}

.similar-image {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid rgba(0, 255, 255, 0.3);
  background: rgba(0, 255, 255, 0.1);
}

.similar-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.similar-name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #ffffff;
  line-height: 1.4;
}

.similarity-score {
  font-size: 0.9rem;
  color: #ffa500;
  font-weight: 500;
}

.no-similar {
  text-align: center;
  padding: 3rem;
  color: #888888;
}

.no-similar-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-similar-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ff6b6b;
  margin-bottom: 0.5rem;
}

.no-similar-detail {
  font-size: 1rem;
  color: #cccccc;
  margin-bottom: 0.5rem;
}

.no-similar-tip {
  font-size: 0.9rem;
  color: #888888;
  font-style: italic;
  background: rgba(255, 107, 107, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 107, 107, 0.3);
  margin-top: 1rem;
  display: inline-block;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 2rem;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.btn-secondary {
  padding: 0.8rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: #ffffff;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #ffffff;
}

.btn-primary {
  padding: 0.8rem 2rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  border: none;
  color: #ffffff;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.4);
}
</style>