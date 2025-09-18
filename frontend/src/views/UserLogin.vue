<template>
  <div class="login-page">
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
        <div class="login-card">
          <div class="login-header">
            <h1 class="login-title">用户交互系统</h1>
            <p class="login-subtitle">体验个性化推荐，记录您的商品偏好</p>
          </div>

          <form class="login-form" @submit.prevent="handleLogin">
            <div class="form-group">
              <label class="form-label" for="userId">请输入用户ID</label>
              <input 
                type="text" 
                class="form-input" 
                id="userId" 
                v-model="userId"
                placeholder="例如：user001, alice, 张三..."
                required
              >
            </div>

            <div class="form-buttons">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? '🔄 正在进入...' : '🚀 进入交互' }}
              </button>
              <button type="button" class="btn btn-secondary" @click="goHome">
                ❌ 取消
              </button>
            </div>
          </form>

          <div class="login-info">
            <div class="info-title">💡 使用说明</div>
            <ul class="info-list">
              <li>输入任意用户ID即可开始体验</li>
              <li>系统会自动创建新用户或加载现有用户</li>
              <li>通过商品交互获得个性化推荐</li>
              <li>支持点击、查看、收藏、购买等操作</li>
              <li>推荐质量随交互次数提升</li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userId = ref('')
const loading = ref(false)

const handleLogin = async () => {
  if (!userId.value.trim()) {
    ElMessage.warning('请输入用户ID')
    return
  }

  if (userId.value.trim().length < 2) {
    ElMessage.warning('用户ID至少需要2个字符')
    return
  }

  loading.value = true

  try {
    // 模拟登录过程
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // 保存用户ID到localStorage
    localStorage.setItem('currentUserId', userId.value.trim())
    
    ElMessage.success('登录成功！')
    
    // 跳转到用户交互页面
    router.push('/user-interaction')
  } catch (error) {
    ElMessage.error('登录失败，请重试')
  } finally {
    loading.value = false
  }
}

const goHome = () => {
  router.push('/')
}

// 页面加载时检查是否已有用户登录
onMounted(() => {
  const currentUserId = localStorage.getItem('currentUserId')
  if (currentUserId) {
    // 如果已有用户登录，直接跳转到用户交互页面
    router.push('/user-interaction')
  }
})
</script>

<style lang="scss" scoped>
.login-page {
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

.nav-item.active {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 8px;
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
  min-height: calc(100vh - 70px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 5%;
}

.container {
  max-width: 600px;
  width: 100%;
}

/* 登录卡片 */
.login-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 20px;
  padding: 3rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.login-header {
  margin-bottom: 2rem;
}

.login-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 300;
}

.login-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 2rem;
}

.form-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #ffffff;
}

.form-input {
  width: 100%;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(0, 255, 255, 0.2);
  border-radius: 50px;
  color: #ffffff;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  text-align: center;
}

.form-input:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.08);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  min-width: 120px;
}

.btn-primary {
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  color: #ffffff;
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: #ffffff;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #ffffff;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.login-info {
  margin-top: 2rem;
  padding: 1.5rem;
  background: rgba(0, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 15px;
}

.info-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #00ffff;
  margin-bottom: 1rem;
}

.info-list {
  list-style: none;
  text-align: left;
}

.info-list li {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
}

.info-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #00ffff;
  font-weight: bold;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }

  .main-content {
    padding: 1rem 2%;
  }

  .login-card {
    padding: 2rem;
  }

  .login-title {
    font-size: 2rem;
  }

  .form-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }

  .login-title {
    font-size: 1.8rem;
  }

  .form-input {
    font-size: 1rem;
  }
}
</style>
