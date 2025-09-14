<template>
  <div class="product-search-page">
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
          <span class="nav-link active">商品检索</span>
        </div>
      </div>
    </nav>

    <div class="main-content">
      <div class="container">
        <!-- 搜索区域 -->
        <div class="search-section">
          <h1 class="page-title">🔍 商品检索</h1>
          <div class="search-box">
            <el-input
              v-model="searchQuery"
              placeholder="请输入商品名称或关键词..."
              size="large"
              @keyup.enter="handleSearch"
            >
              <template #append>
                <el-button @click="handleSearch" type="primary">
                  <el-icon><Search /></el-icon>
                  搜索
                </el-button>
              </template>
            </el-input>
          </div>
          
          <!-- 筛选条件 -->
          <div class="filters">
            <el-select v-model="selectedCategory" placeholder="选择分类" @change="handleFilterChange">
              <el-option label="全部分类" value=""></el-option>
              <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
              />
            </el-select>
            
            <el-select v-model="sortBy" placeholder="排序方式" @change="handleSortChange">
              <el-option label="默认排序" value="default"></el-option>
              <el-option label="价格从低到高" value="price_asc"></el-option>
              <el-option label="价格从高到低" value="price_desc"></el-option>
              <el-option label="评分从高到低" value="rating_desc"></el-option>
            </el-select>
          </div>
        </div>

        <!-- 搜索结果 -->
        <div class="results-section">
          <div class="results-header">
            <h3>搜索结果</h3>
            <span class="result-count">找到 {{ totalResults }} 个商品</span>
          </div>
          
          <!-- 商品列表 -->
          <div class="products-grid" v-loading="loading">
            <div
              v-for="product in products"
              :key="product.id"
              class="product-card card"
              @click="viewProduct(product)"
            >
              <div class="product-image">
                <img :src="product.image_url || '/placeholder-product.jpg'" :alt="product.name" />
                <div class="product-badge" v-if="product.is_recommended">推荐</div>
              </div>
              <div class="product-info">
                <h4 class="product-name">{{ product.name }}</h4>
                <p class="product-description">{{ product.description }}</p>
                <div class="product-meta">
                  <span class="product-category">{{ product.category_name }}</span>
                  <div class="product-rating">
                    <el-rate v-model="product.rating" disabled show-score />
                  </div>
                </div>
                <div class="product-price">
                  <span class="current-price">¥{{ product.price }}</span>
                  <span class="original-price" v-if="product.original_price">¥{{ product.original_price }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div class="pagination" v-if="totalResults > 0">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[12, 24, 48]"
              :total="totalResults"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
          
          <!-- 空状态 -->
          <div v-if="!loading && products.length === 0" class="empty-state">
            <el-empty description="暂无商品数据">
              <el-button type="primary" @click="loadProducts">刷新数据</el-button>
            </el-empty>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import api from '@/utils/api'

export default {
  name: 'ProductSearch',
  components: {
    Search
  },
  setup() {
    const loading = ref(false)
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const sortBy = ref('default')
    const currentPage = ref(1)
    const pageSize = ref(12)
    const totalResults = ref(0)
    
    const products = ref([])
    const categories = ref([
      { id: 1, name: '电子产品' },
      { id: 2, name: '服装鞋帽' },
      { id: 3, name: '家居用品' },
      { id: 4, name: '图书音像' },
      { id: 5, name: '食品饮料' }
    ])
    
    // 模拟数据
    const mockProducts = [
      {
        id: 1,
        name: 'iPhone 15 Pro',
        description: '最新款苹果手机，性能强劲',
        price: 7999,
        original_price: 8999,
        category_name: '电子产品',
        rating: 4.8,
        image_url: 'https://via.placeholder.com/300x200?text=iPhone+15+Pro',
        is_recommended: true
      },
      {
        id: 2,
        name: 'MacBook Air M2',
        description: '轻薄便携的笔记本电脑',
        price: 8999,
        category_name: '电子产品',
        rating: 4.9,
        image_url: 'https://via.placeholder.com/300x200?text=MacBook+Air',
        is_recommended: false
      },
      {
        id: 3,
        name: 'Nike Air Max',
        description: '舒适的运动鞋',
        price: 899,
        original_price: 1299,
        category_name: '服装鞋帽',
        rating: 4.5,
        image_url: 'https://via.placeholder.com/300x200?text=Nike+Air+Max',
        is_recommended: true
      }
    ]
    
    const handleSearch = async () => {
      if (!searchQuery.value.trim()) {
        ElMessage.warning('请输入搜索关键词')
        return
      }
      
      loading.value = true
      currentPage.value = 1
      
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 模拟搜索结果
        const filteredProducts = mockProducts.filter(product =>
          product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          product.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
        
        products.value = filteredProducts
        totalResults.value = filteredProducts.length
        
        ElMessage.success(`找到 ${filteredProducts.length} 个相关商品`)
      } catch (error) {
        ElMessage.error('搜索失败，请重试')
      } finally {
        loading.value = false
      }
    }
    
    const handleFilterChange = () => {
      currentPage.value = 1
      loadProducts()
    }
    
    const handleSortChange = () => {
      loadProducts()
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      loadProducts()
    }
    
    const handleCurrentChange = (page) => {
      currentPage.value = page
      loadProducts()
    }
    
    const loadProducts = async () => {
      loading.value = true
      
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 模拟数据加载
        products.value = mockProducts
        totalResults.value = mockProducts.length
        
      } catch (error) {
        ElMessage.error('加载商品数据失败')
      } finally {
        loading.value = false
      }
    }
    
    const viewProduct = (product) => {
      ElMessage.info(`查看商品: ${product.name}`)
      // 这里可以跳转到商品详情页
    }
    
    onMounted(() => {
      loadProducts()
    })
    
    return {
      loading,
      searchQuery,
      selectedCategory,
      sortBy,
      currentPage,
      pageSize,
      totalResults,
      products,
      categories,
      handleSearch,
      handleFilterChange,
      handleSortChange,
      handleSizeChange,
      handleCurrentChange,
      loadProducts,
      viewProduct
    }
  }
}
</script>

<style lang="scss" scoped>
.product-search-page {
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
    max-width: 1200px;
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.search-section {
  text-align: center;
  margin-bottom: 3rem;
  
  .page-title {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    color: var(--text-color);
  }
  
  .search-box {
    max-width: 600px;
    margin: 0 auto 2rem;
  }
  
  .filters {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
  }
}

.results-section {
  .results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    
    h3 {
      font-size: 1.5rem;
      color: var(--text-color);
    }
    
    .result-count {
      color: #666;
    }
  }
  
  .products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
  }
  
  .product-card {
    cursor: pointer;
    overflow: hidden;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-4px);
    }
    
    .product-image {
      position: relative;
      height: 200px;
      overflow: hidden;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
      }
      
      .product-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #e74c3c;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
      }
    }
    
    &:hover .product-image img {
      transform: scale(1.05);
    }
    
    .product-info {
      padding: 1.5rem;
      
      .product-name {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--text-color);
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .product-description {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .product-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        
        .product-category {
          background: #f0f0f0;
          padding: 4px 8px;
          border-radius: 12px;
          font-size: 0.8rem;
          color: #666;
        }
      }
      
      .product-price {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        
        .current-price {
          font-size: 1.2rem;
          font-weight: 600;
          color: #e74c3c;
        }
        
        .original-price {
          font-size: 0.9rem;
          color: #999;
          text-decoration: line-through;
        }
      }
    }
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 3rem;
  }
  
  .empty-state {
    text-align: center;
    padding: 4rem 0;
  }
}

@media (max-width: 768px) {
  .search-section .filters {
    flex-direction: column;
    align-items: center;
  }
  
  .results-section .results-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }
}
</style>
