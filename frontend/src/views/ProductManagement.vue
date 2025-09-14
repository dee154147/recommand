<template>
  <div class="product-management-page">
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
          <span class="nav-link active">商品管理</span>
        </div>
      </div>
    </nav>

    <div class="main-content">
      <div class="container">
        <!-- 页面标题和操作栏 -->
        <div class="page-header">
          <h1 class="page-title">📦 商品管理</h1>
          <div class="header-actions">
            <el-button type="primary" @click="showAddDialog = true">
              <el-icon><Plus /></el-icon>
              添加商品
            </el-button>
            <el-button @click="refreshData">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>

        <!-- 搜索和筛选 -->
        <div class="search-section">
          <div class="search-bar">
            <el-input
              v-model="searchQuery"
              placeholder="搜索商品名称或描述..."
              @keyup.enter="handleSearch"
            >
              <template #append>
                <el-button @click="handleSearch">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </div>
          
          <div class="filters">
            <el-select v-model="selectedCategory" placeholder="选择分类" @change="handleFilter">
              <el-option label="全部分类" value=""></el-option>
              <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
              />
            </el-select>
            
            <el-select v-model="statusFilter" placeholder="商品状态" @change="handleFilter">
              <el-option label="全部状态" value=""></el-option>
              <el-option label="上架" value="active"></el-option>
              <el-option label="下架" value="inactive"></el-option>
            </el-select>
          </div>
        </div>

        <!-- 商品列表 -->
        <div class="products-table" v-loading="loading">
          <el-table :data="filteredProducts" stripe style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            
            <el-table-column label="商品信息" min-width="200">
              <template #default="{ row }">
                <div class="product-info">
                  <img :src="row.image_url || '/placeholder-product.jpg'" class="product-thumb" />
                  <div class="product-details">
                    <div class="product-name">{{ row.name }}</div>
                    <div class="product-desc">{{ row.description }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="category_name" label="分类" width="120" />
            
            <el-table-column label="价格" width="120">
              <template #default="{ row }">
                <span class="price">¥{{ row.price }}</span>
              </template>
            </el-table-column>
            
            <el-table-column prop="rating" label="评分" width="100">
              <template #default="{ row }">
                <el-rate v-model="row.rating" disabled show-score />
              </template>
            </el-table-column>
            
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
                  {{ row.status === 'active' ? '上架' : '下架' }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editProduct(row)">编辑</el-button>
                <el-button 
                  size="small" 
                  :type="row.status === 'active' ? 'warning' : 'success'"
                  @click="toggleStatus(row)"
                >
                  {{ row.status === 'active' ? '下架' : '上架' }}
                </el-button>
                <el-button size="small" type="danger" @click="deleteProduct(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 分页 -->
        <div class="pagination" v-if="totalProducts > 0">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50]"
            :total="totalProducts"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>

        <!-- 添加/编辑商品对话框 -->
        <el-dialog
          v-model="showAddDialog"
          :title="editingProduct ? '编辑商品' : '添加商品'"
          width="600px"
        >
          <el-form :model="productForm" :rules="formRules" ref="productFormRef" label-width="100px">
            <el-form-item label="商品名称" prop="name">
              <el-input v-model="productForm.name" placeholder="请输入商品名称" />
            </el-form-item>
            
            <el-form-item label="商品描述" prop="description">
              <el-input
                v-model="productForm.description"
                type="textarea"
                :rows="3"
                placeholder="请输入商品描述"
              />
            </el-form-item>
            
            <el-form-item label="商品分类" prop="category_id">
              <el-select v-model="productForm.category_id" placeholder="选择分类">
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>
            
            <el-form-item label="价格" prop="price">
              <el-input-number v-model="productForm.price" :min="0" :precision="2" />
            </el-form-item>
            
            <el-form-item label="原始价格">
              <el-input-number v-model="productForm.original_price" :min="0" :precision="2" />
            </el-form-item>
            
            <el-form-item label="图片URL">
              <el-input v-model="productForm.image_url" placeholder="请输入图片URL" />
            </el-form-item>
            
            <el-form-item label="商品状态">
              <el-radio-group v-model="productForm.status">
                <el-radio value="active">上架</el-radio>
                <el-radio value="inactive">下架</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
          
          <template #footer>
            <el-button @click="showAddDialog = false">取消</el-button>
            <el-button type="primary" @click="saveProduct">保存</el-button>
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search } from '@element-plus/icons-vue'

export default {
  name: 'ProductManagement',
  components: {
    Plus,
    Refresh,
    Search
  },
  setup() {
    const loading = ref(false)
    const showAddDialog = ref(false)
    const editingProduct = ref(null)
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const statusFilter = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalProducts = ref(0)
    
    const productFormRef = ref(null)
    
    const categories = ref([
      { id: 1, name: '电子产品' },
      { id: 2, name: '服装鞋帽' },
      { id: 3, name: '家居用品' },
      { id: 4, name: '图书音像' },
      { id: 5, name: '食品饮料' }
    ])
    
    // 模拟商品数据
    const products = ref([
      {
        id: 1,
        name: 'iPhone 15 Pro',
        description: '最新款苹果手机，性能强劲',
        price: 7999,
        original_price: 8999,
        category_id: 1,
        category_name: '电子产品',
        rating: 4.8,
        image_url: 'https://via.placeholder.com/300x200?text=iPhone+15+Pro',
        status: 'active'
      },
      {
        id: 2,
        name: 'MacBook Air M2',
        description: '轻薄便携的笔记本电脑',
        price: 8999,
        category_id: 1,
        category_name: '电子产品',
        rating: 4.9,
        image_url: 'https://via.placeholder.com/300x200?text=MacBook+Air',
        status: 'active'
      },
      {
        id: 3,
        name: 'Nike Air Max',
        description: '舒适的运动鞋',
        price: 899,
        original_price: 1299,
        category_id: 2,
        category_name: '服装鞋帽',
        rating: 4.5,
        image_url: 'https://via.placeholder.com/300x200?text=Nike+Air+Max',
        status: 'inactive'
      }
    ])
    
    const productForm = reactive({
      name: '',
      description: '',
      category_id: null,
      price: 0,
      original_price: null,
      image_url: '',
      status: 'active'
    })
    
    const formRules = {
      name: [
        { required: true, message: '请输入商品名称', trigger: 'blur' }
      ],
      description: [
        { required: true, message: '请输入商品描述', trigger: 'blur' }
      ],
      category_id: [
        { required: true, message: '请选择商品分类', trigger: 'change' }
      ],
      price: [
        { required: true, message: '请输入商品价格', trigger: 'blur' }
      ]
    }
    
    // 计算属性：过滤后的商品列表
    const filteredProducts = computed(() => {
      let filtered = products.value
      
      // 按搜索关键词过滤
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(product =>
          product.name.toLowerCase().includes(query) ||
          product.description.toLowerCase().includes(query)
        )
      }
      
      // 按分类过滤
      if (selectedCategory.value) {
        filtered = filtered.filter(product => product.category_id === selectedCategory.value)
      }
      
      // 按状态过滤
      if (statusFilter.value) {
        filtered = filtered.filter(product => product.status === statusFilter.value)
      }
      
      totalProducts.value = filtered.length
      
      // 分页
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filtered.slice(start, end)
    })
    
    const handleSearch = () => {
      currentPage.value = 1
    }
    
    const handleFilter = () => {
      currentPage.value = 1
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }
    
    const handleCurrentChange = (page) => {
      currentPage.value = page
    }
    
    const refreshData = () => {
      loading.value = true
      setTimeout(() => {
        loading.value = false
        ElMessage.success('数据已刷新')
      }, 1000)
    }
    
    const editProduct = (product) => {
      editingProduct.value = product
      Object.assign(productForm, product)
      showAddDialog.value = true
    }
    
    const saveProduct = async () => {
      try {
        await productFormRef.value.validate()
        
        if (editingProduct.value) {
          // 编辑商品
          const index = products.value.findIndex(p => p.id === editingProduct.value.id)
          if (index !== -1) {
            const category = categories.value.find(c => c.id === productForm.category_id)
            products.value[index] = {
              ...products.value[index],
              ...productForm,
              category_name: category?.name || ''
            }
          }
          ElMessage.success('商品更新成功')
        } else {
          // 添加商品
          const newProduct = {
            ...productForm,
            id: Date.now(),
            category_name: categories.value.find(c => c.id === productForm.category_id)?.name || '',
            rating: 0
          }
          products.value.unshift(newProduct)
          ElMessage.success('商品添加成功')
        }
        
        showAddDialog.value = false
        resetForm()
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }
    
    const resetForm = () => {
      editingProduct.value = null
      Object.assign(productForm, {
        name: '',
        description: '',
        category_id: null,
        price: 0,
        original_price: null,
        image_url: '',
        status: 'active'
      })
      productFormRef.value?.resetFields()
    }
    
    const toggleStatus = async (product) => {
      const action = product.status === 'active' ? '下架' : '上架'
      
      try {
        await ElMessageBox.confirm(
          `确定要${action}商品"${product.name}"吗？`,
          '确认操作',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        product.status = product.status === 'active' ? 'inactive' : 'active'
        ElMessage.success(`商品已${action}`)
      } catch {
        // 用户取消操作
      }
    }
    
    const deleteProduct = async (product) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除商品"${product.name}"吗？此操作不可恢复。`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'error'
          }
        )
        
        const index = products.value.findIndex(p => p.id === product.id)
        if (index !== -1) {
          products.value.splice(index, 1)
          ElMessage.success('商品删除成功')
        }
      } catch {
        // 用户取消操作
      }
    }
    
    onMounted(() => {
      refreshData()
    })
    
    return {
      loading,
      showAddDialog,
      editingProduct,
      searchQuery,
      selectedCategory,
      statusFilter,
      currentPage,
      pageSize,
      totalProducts,
      productFormRef,
      categories,
      products,
      productForm,
      formRules,
      filteredProducts,
      handleSearch,
      handleFilter,
      handleSizeChange,
      handleCurrentChange,
      refreshData,
      editProduct,
      saveProduct,
      toggleStatus,
      deleteProduct
    }
  }
}
</script>

<style lang="scss" scoped>
.product-management-page {
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  
  .page-title {
    font-size: 2rem;
    color: var(--text-color);
    margin: 0;
  }
  
  .header-actions {
    display: flex;
    gap: 1rem;
  }
}

.search-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: var(--shadow);
  margin-bottom: 2rem;
  
  .search-bar {
    margin-bottom: 1rem;
    max-width: 400px;
  }
  
  .filters {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }
}

.products-table {
  background: white;
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 1rem;
  margin-bottom: 2rem;
  
  .product-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    
    .product-thumb {
      width: 60px;
      height: 60px;
      object-fit: cover;
      border-radius: 8px;
    }
    
    .product-details {
      .product-name {
        font-weight: 600;
        margin-bottom: 0.25rem;
        color: var(--text-color);
      }
      
      .product-desc {
        font-size: 0.9rem;
        color: #666;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
    }
  }
  
  .price {
    font-weight: 600;
    color: #e74c3c;
  }
}

.pagination {
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .search-section .filters {
    flex-direction: column;
  }
  
  .products-table .product-info {
    flex-direction: column;
    text-align: center;
  }
}
</style>
