<template>
  <div class="home-page">
    <!-- 背景动画层 -->
    <div class="bg-animation"></div>
    
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="logo">智能推荐系统</div>
        <ul class="nav-menu">
          <li class="nav-item"><a href="#home" class="nav-link">首页</a></li>
          <li class="nav-item"><a href="#features" class="nav-link">产品特性</a></li>
          <li class="nav-item"><a href="#team" class="nav-link">团队介绍</a></li>
          <li class="nav-item"><a href="#contact" class="nav-link">联系我们</a></li>
          <li class="nav-item dropdown">
            <a href="#" class="nav-link dropdown-toggle">功能演示</a>
            <div class="dropdown-menu">
              <router-link to="/product-search" class="dropdown-item">商品检索</router-link>
              <router-link to="/product-management" class="dropdown-item">商品管理</router-link>
              <router-link to="/user-interaction" class="dropdown-item">用户交互</router-link>
            </div>
          </li>
        </ul>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- Hero Section -->
      <section id="home" class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">智能推荐系统</h1>
          <p class="hero-subtitle">基于AI的商品推荐引擎</p>
          <p class="hero-description">运用先进的机器学习算法，为用户提供精准的商品推荐服务。通过分析商品特征和用户偏好，实现个性化的购物体验。</p>
          <div class="hero-buttons">
            <a href="#features" class="cta-button">了解更多</a>
          </div>
        </div>
        
        <!-- 背景动画元素 -->
        <div class="hero-visual">
          <div class="floating-shapes">
            <div class="shape shape-1"></div>
            <div class="shape shape-2"></div>
            <div class="shape shape-3"></div>
            <div class="shape shape-4"></div>
            <div class="shape shape-5"></div>
          </div>
          <div class="tech-grid">
            <div class="grid-item"></div>
            <div class="grid-item"></div>
            <div class="grid-item"></div>
            <div class="grid-item"></div>
            <div class="grid-item"></div>
            <div class="grid-item"></div>
            <div class="grid-item"></div>
            <div class="grid-item"></div>
            <div class="grid-item"></div>
          </div>
        </div>
      </section>

      <!-- 产品特性 -->
      <section id="features" class="content-section">
        <h2 class="section-title fade-in">核心特性</h2>
        <div class="features-grid">
          <div class="feature-card fade-in">
            <div class="feature-icon">🧠</div>
            <h3 class="feature-title">智能算法</h3>
            <p class="feature-description">
              基于深度学习的推荐算法，能够准确理解用户偏好，
              提供个性化的商品推荐服务。
            </p>
          </div>
          <div class="feature-card fade-in">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">实时推荐</h3>
            <p class="feature-description">
              毫秒级响应速度，实时分析用户行为，
              动态调整推荐策略，提升用户体验。
            </p>
          </div>
          <div class="feature-card fade-in">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">数据分析</h3>
            <p class="feature-description">
              强大的数据分析能力，为商家提供详细的用户洞察
              和销售趋势分析，助力业务决策。
            </p>
          </div>
          <div class="feature-card fade-in">
            <div class="feature-icon">🔒</div>
            <h3 class="feature-title">安全可靠</h3>
            <p class="feature-description">
              企业级安全保障，数据加密存储，
              确保用户隐私和商业机密的安全。
            </p>
          </div>
          <div class="feature-card fade-in">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">精准匹配</h3>
            <p class="feature-description">
              基于内容相似度的智能匹配算法，
              准确识别商品间的关联关系。
            </p>
          </div>
          <div class="feature-card fade-in">
            <div class="feature-icon">🚀</div>
            <h3 class="feature-title">高性能</h3>
            <p class="feature-description">
              分布式架构设计，支持大规模并发访问，
              确保系统稳定高效的运行。
            </p>
          </div>
        </div>
      </section>

      <!-- 团队介绍 -->
      <section id="team" class="content-section">
        <h2 class="section-title fade-in">核心团队</h2>
        <div class="team-grid">
          <div class="team-card fade-in">
            <div class="team-avatar">👨‍💻</div>
            <h3 class="team-name">张明</h3>
            <p class="team-position">技术总监</p>
            <p class="team-bio">
              拥有10年AI算法研发经验，专注于推荐系统和机器学习领域，
              曾任职于知名互联网公司，主导过多个大型推荐系统项目。
            </p>
          </div>
          <div class="team-card fade-in">
            <div class="team-avatar">👩‍🔬</div>
            <h3 class="team-name">李雪</h3>
            <p class="team-position">算法工程师</p>
            <p class="team-bio">
              机器学习博士，在深度学习推荐算法方面有深入研究，
              发表多篇顶级会议论文，具备丰富的算法优化经验。
            </p>
          </div>
          <div class="team-card fade-in">
            <div class="team-avatar">👨‍💼</div>
            <h3 class="team-name">王强</h3>
            <p class="team-position">产品经理</p>
            <p class="team-bio">
              资深产品经理，专注电商和推荐系统产品设计，
              深度理解用户需求，擅长将技术转化为产品价值。
            </p>
          </div>
          <div class="team-card fade-in">
            <div class="team-avatar">👩‍💻</div>
            <h3 class="team-name">陈静</h3>
            <p class="team-position">前端工程师</p>
            <p class="team-bio">
              前端技术专家，精通Vue.js和React框架，
              注重用户体验设计，致力于打造现代化的用户界面。
            </p>
          </div>
          <div class="team-card fade-in">
            <div class="team-avatar">👨‍🔧</div>
            <h3 class="team-name">刘伟</h3>
            <p class="team-position">后端工程师</p>
            <p class="team-bio">
              后端架构师，擅长Python和微服务架构设计，
              具备丰富的分布式系统开发和运维经验。
            </p>
          </div>
          <div class="team-card fade-in">
            <div class="team-avatar">👩‍🎨</div>
            <h3 class="team-name">赵丽</h3>
            <p class="team-position">UI/UX设计师</p>
            <p class="team-bio">
              资深UI/UX设计师，专注科技产品的视觉设计，
              擅长将复杂的技术概念转化为直观的用户界面。
            </p>
          </div>
        </div>
      </section>

      <!-- 联系我们 -->
      <section id="contact" class="contact-section">
        <div class="container">
          <h2 class="section-title fade-in">联系我们</h2>
          <div class="contact-content">
            <div class="contact-hero">
              <div class="contact-main-info">
                <div class="contact-primary">
                  <div class="contact-icon-large">📧</div>
                  <div class="contact-details">
                    <h3>邮箱联系</h3>
                    <p>contact@example.com</p>
                    <span class="contact-label">主要联系方式</span>
                  </div>
                </div>
                <div class="contact-secondary">
                  <div class="contact-item">
                    <div class="contact-icon">📞</div>
                    <div class="contact-text">
                      <h4>电话咨询</h4>
                      <p>+86 400-123-4567</p>
                    </div>
                  </div>
                  <div class="contact-item">
                    <div class="contact-icon">📍</div>
                    <div class="contact-text">
                      <h4>公司地址</h4>
                      <p>北京市朝阳区科技园区</p>
                    </div>
                  </div>
                  <div class="contact-item">
                    <div class="contact-icon">🕒</div>
                    <div class="contact-text">
                      <h4>工作时间</h4>
                      <p>周一至周五 9:00-18:00</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-logo">智能推荐系统</div>
        <p class="footer-description">
          专业的AI推荐解决方案提供商，致力于为企业和用户创造价值
        </p>
        <div class="footer-links">
          <a href="#home" class="footer-link">首页</a>
          <a href="#features" class="footer-link">产品特性</a>
          <a href="#team" class="footer-link">团队介绍</a>
          <a href="#contact" class="footer-link">联系我们</a>
        </div>
        <div class="copyright">
          © 2024 智能推荐系统. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    goToDemo() {
      this.$router.push('/product-search')
    }
  }
}
</script>

<style lang="scss" scoped>
.home-page {
  min-height: 100vh;
  background: #0a0a0a;
  color: #ffffff;
  font-family: 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  overflow-x: hidden;
  position: relative;
}

// 背景动画层
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

// Fade-in动画
.fade-in {
  opacity: 0;
  animation: fadeInUp 1s ease-out forwards;
}

.fade-in:nth-child(1) { animation-delay: 0.1s; }
.fade-in:nth-child(2) { animation-delay: 0.2s; }
.fade-in:nth-child(3) { animation-delay: 0.3s; }
.fade-in:nth-child(4) { animation-delay: 0.4s; }
.fade-in:nth-child(5) { animation-delay: 0.5s; }
.fade-in:nth-child(6) { animation-delay: 0.6s; }

// 导航栏样式
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
  
  .nav-item {
    position: relative;
    
    .nav-link {
      color: #ffffff;
      text-decoration: none;
      font-weight: 500;
      transition: all 0.3s ease;
      padding: 0.5rem 1rem;
      border-radius: 8px;
      
      &:hover {
        color: #00ffff;
        background: rgba(0, 255, 255, 0.1);
      }
    }
  }
  
  .dropdown {
    position: relative;
    
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
      z-index: 1001;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
      
      .dropdown-item {
        display: block;
        padding: 1rem 1.5rem;
        color: #ffffff;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        text-align: left;
        
        &:last-child {
          border-bottom: none;
        }
        
        &:hover {
          color: #ff4444;
          background: rgba(255, 68, 68, 0.1);
          padding-left: 2rem;
        }
      }
    }
    
    &:hover .dropdown-menu {
      opacity: 1;
      visibility: visible;
      transform: translateY(0);
    }
  }
  
  .dropdown-toggle::after {
    display: none;
  }
}

// 主要内容区域
.main-content {
  margin-top: 70px;
}

// Hero Section
.hero-section {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  overflow: hidden;
  
  .hero-content {
    max-width: 800px;
    z-index: 2;
    position: relative;
  }
  
  .hero-title {
    font-size: 4rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    line-height: 1.2;
    background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 3s ease-in-out infinite;
  }
  
  .hero-subtitle {
    font-size: 1.5rem;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 2rem;
    font-weight: 300;
  }
  
  .hero-description {
    font-size: 1.2rem;
    color: rgba(255, 255, 255, 0.6);
    margin-bottom: 3rem;
    line-height: 1.8;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .hero-buttons {
    display: flex;
    gap: 2rem;
    justify-content: center;
    
    .cta-button {
      display: inline-block;
      padding: 1rem 2rem;
      background: linear-gradient(45deg, #00ffff, #ff00ff);
      color: #ffffff;
      text-decoration: none;
      border-radius: 50px;
      font-weight: 600;
      transition: all 0.3s ease;
      box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
      text-transform: uppercase;
      letter-spacing: 1px;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(0, 255, 255, 0.4);
      }
    }
  }
  
  .hero-visual {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    overflow: hidden;
  }
  
  .floating-shapes {
    position: absolute;
    width: 100%;
    height: 100%;
    
    .shape {
      position: absolute;
      background: linear-gradient(45deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
      border-radius: 50%;
      animation: float 6s ease-in-out infinite;
    }
    
    .shape-1 {
      width: 80px;
      height: 80px;
      top: 20%;
      left: 10%;
      animation-delay: 0s;
    }
    
    .shape-2 {
      width: 120px;
      height: 120px;
      top: 60%;
      right: 15%;
      animation-delay: 2s;
    }
    
    .shape-3 {
      width: 60px;
      height: 60px;
      top: 30%;
      right: 30%;
      animation-delay: 4s;
    }
    
    .shape-4 {
      width: 100px;
      height: 100px;
      bottom: 20%;
      left: 20%;
      animation-delay: 1s;
    }
    
    .shape-5 {
      width: 90px;
      height: 90px;
      top: 70%;
      left: 60%;
      animation-delay: 3s;
    }
  }
  
  .tech-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    width: 100%;
    height: 100%;
    padding: 50px;
    opacity: 0.05;
    
    .grid-item {
      background: linear-gradient(45deg, #00ffff, #ff00ff);
      border-radius: 10px;
      animation: pulse 2s ease-in-out infinite;
      
      &:nth-child(1) { animation-delay: 0s; }
      &:nth-child(2) { animation-delay: 0.2s; }
      &:nth-child(3) { animation-delay: 0.4s; }
      &:nth-child(4) { animation-delay: 0.6s; }
      &:nth-child(5) { animation-delay: 0.8s; }
      &:nth-child(6) { animation-delay: 1s; }
      &:nth-child(7) { animation-delay: 1.2s; }
      &:nth-child(8) { animation-delay: 1.4s; }
      &:nth-child(9) { animation-delay: 1.6s; }
    }
  }
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-20px) rotate(120deg); }
  66% { transform: translateY(10px) rotate(240deg); }
}

@keyframes pulse {
  0%, 100% { 
    opacity: 0.1;
    transform: scale(1);
  }
  50% { 
    opacity: 0.3;
    transform: scale(1.05);
  }
}

@keyframes backgroundMove {
  0%, 100% { transform: translateX(0) translateY(0); }
  25% { transform: translateX(-2%) translateY(-2%); }
  50% { transform: translateX(2%) translateY(-1%); }
  75% { transform: translateX(-1%) translateY(2%); }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// 内容区域
.content-section {
  padding: 5rem 5%;
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 3rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

// 功能特性
.features-section {
  padding: 5rem 0;
  background: #0f0f0f;
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 5rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  
  &:hover {
    transform: translateY(-10px);
    border-color: #00ffff;
    box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
  }
  
  .feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #00ffff, #ff00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .feature-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #ffffff;
  }
  
  .feature-description {
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.6;
  }
}

// 团队介绍
.team-section {
  padding: 5rem 0;
  background: #0a0a0a;
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 5rem;
}

.team-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  
  &:hover {
    transform: translateY(-5px);
    border-color: #00ffff;
    box-shadow: 0 15px 30px rgba(0, 255, 255, 0.2);
  }
  
  .team-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(45deg, #00ffff, #ff00ff);
    margin: 0 auto 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: #ffffff;
  }
  
  .team-name {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #ffffff;
  }
  
  .team-position {
    color: #00ffff;
    margin-bottom: 1rem;
    font-weight: 500;
  }
  
  .team-bio {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    line-height: 1.5;
  }
}

// 联系我们区域
.contact-section {
  padding: 6rem 0;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(255, 0, 255, 0.1) 0%, transparent 50%);
    pointer-events: none;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    position: relative;
    z-index: 1;
  }
  
  .contact-content {
    margin-top: 4rem;
  }
  
  .contact-hero {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(0, 255, 255, 0.1);
    border-radius: 30px;
    padding: 4rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }
  
  .contact-main-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
  }
  
  .contact-primary {
    display: flex;
    align-items: center;
    gap: 2rem;
    padding: 2rem;
    background: rgba(0, 255, 255, 0.05);
    border: 1px solid rgba(0, 255, 255, 0.2);
    border-radius: 20px;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
    }
    
    .contact-icon-large {
      font-size: 4rem;
      background: linear-gradient(45deg, #00ffff, #ff00ff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.3));
    }
    
    .contact-details {
      h3 {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #00ffff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
      
      p {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 0.5rem;
        font-weight: 500;
      }
      
      .contact-label {
        display: inline-block;
        background: linear-gradient(45deg, #00ffff, #ff00ff);
        color: #000;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
      }
    }
  }
  
  .contact-secondary {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .contact-item {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    
    &:hover {
      transform: translateX(10px);
      border-color: rgba(0, 255, 255, 0.3);
      background: rgba(0, 255, 255, 0.05);
    }
    
    .contact-icon {
      font-size: 2rem;
      background: linear-gradient(45deg, #00ffff, #ff00ff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      min-width: 40px;
    }
    
    .contact-text {
      h4 {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.3rem;
      }
      
      p {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin: 0;
      }
    }
  }
}

// 页脚
.footer {
  background: #0a0a0a;
  border-top: 1px solid rgba(0, 255, 255, 0.1);
  padding: 3rem 5%;
  text-align: center;
  
  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .footer-logo {
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(45deg, #00ffff, #ff00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
  }
  
  .footer-description {
    color: rgba(255, 255, 255, 0.6);
    margin-bottom: 2rem;
  }
  
  .footer-links {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 2rem;
    
    .footer-link {
      color: rgba(255, 255, 255, 0.7);
      text-decoration: none;
      transition: color 0.3s ease;
      
      &:hover {
        color: #00ffff;
      }
    }
  }
  
  .copyright {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.9rem;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .hero-section {
    .hero-content {
      padding: 0 2rem;
    }
    
    .hero-title {
      font-size: 2.5rem !important;
    }
    
    .hero-subtitle {
      font-size: 1.1rem !important;
    }
    
    .hero-buttons {
      flex-direction: column;
      align-items: center;
      gap: 1rem;
      
      .btn-primary, .btn-secondary {
        width: 200px;
      }
    }
  }
  
  .nav-menu {
    display: none;
  }
  
  .features-grid, .team-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .feature-card, .team-member {
    padding: 2rem 1.5rem;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .contact-main-info {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .contact-hero {
    padding: 2rem;
  }
  
  .contact-primary {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
}
</style>
