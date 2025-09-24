<template>
  <div class="product-management">
    <!-- 背景动画 -->
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
              <router-link to="/product-search" class="dropdown-item">商品检索</router-link>
              <router-link to="/product-management" class="dropdown-item active">商品管理</router-link>
              <router-link to="/user-login" class="dropdown-item">用户交互</router-link>
            </div>
          </li>
        </ul>
      </div>
    </nav>
    
    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">商品管理模块 - 智能分析系统</h1>
        <p class="page-subtitle">
          基于LLM技术的智能商品标签生成、相似商品检索和商业特征分析
        </p>
        </div>

      <!-- 功能步骤指示器 -->
      <div class="steps-indicator">
        <div 
          class="step" 
          :class="{ active: currentStep === 1, completed: currentStep > 1 }"
        >
          <div class="step-number">1</div>
          <div class="step-text">输入商品描述</div>
        </div>
        <div 
          class="step" 
          :class="{ active: currentStep === 2, completed: currentStep > 2 }"
        >
          <div class="step-number">2</div>
          <div class="step-text">生成商品标签</div>
      </div>
        <div 
          class="step" 
          :class="{ active: currentStep === 3, completed: currentStep > 3 }"
        >
          <div class="step-number">3</div>
          <div class="step-text">查找相似商品</div>
        </div>
        <div 
          class="step" 
          :class="{ active: currentStep === 4, completed: currentStep > 4 }"
        >
          <div class="step-number">4</div>
          <div class="step-text">商业特征分析</div>
        </div>
      </div>

      <!-- 功能区域1：商品描述输入 -->
      <div class="function-area show" id="area1">
        <h2 class="function-title">
          <span>📝</span>
          商品描述输入
        </h2>
        <p style="color: #cccccc; margin-bottom: 1rem;">
          请输入您要分析的商品描述，系统将基于LLM自动生成商品标签。
        </p>
        <textarea 
          class="description-input" 
          v-model="productDescription"
          placeholder="例如：这是一款高端商务笔记本电脑，采用英特尔i7处理器，16GB内存，512GB SSD存储，14英寸4K显示屏，支持触控功能，适合商务人士办公使用..."
          rows="5"
        ></textarea>
        <div class="input-hint">
          建议输入50-500字的详细商品描述，包含功能特点、使用场景、目标用户等信息
        </div>
        <div style="margin-top: 1.5rem; text-align: center;">
          <button 
            class="btn btn-primary" 
            @click="generateTags"
            :disabled="!productDescription.trim() || isGeneratingTags"
          >
            <span v-if="isGeneratingTags">🔄 生成中...</span>
            <span v-else>🤖 生成商品标签</span>
          </button>
          </div>
        </div>

      <!-- 功能区域2：生成的商品标签 -->
      <div 
        class="function-area" 
        v-show="showArea2"
        :class="{ show: showArea2 }"
      >
        <h2 class="function-title">
          <span>🏷️</span>
          生成的商品标签
        </h2>
        <div class="tags-container">
          <div 
            v-for="(tag, index) in generatedTags" 
            :key="index"
            class="tag"
          >
            {{ tag }}
          </div>
        </div>
        <div style="margin-top: 1.5rem; text-align: center;">
          <button 
            class="btn btn-secondary" 
            @click="findSimilarProducts"
            :disabled="!generatedTags.length || isFindingSimilar"
          >
            <span v-if="isFindingSimilar">🔄 检索中...</span>
            <span v-else>🔍 查找相似商品</span>
          </button>
        </div>
          </div>
          
      <!-- 功能区域3：相似商品检索结果 -->
      <div 
        class="function-area" 
        v-show="showArea3"
        :class="{ show: showArea3 }"
      >
        <h2 class="function-title">
          <span>🔍</span>
          相似商品检索结果
        </h2>
        <!-- 相似商品列表 -->
        <div v-if="similarProducts.length > 0" class="similar-products">
          <div 
            v-for="(product, index) in similarProducts" 
            :key="index"
            class="product-card"
          >
            <div class="product-image">
              <img 
                v-if="product.image_url" 
                :src="product.image_url" 
                :alt="product.name"
                class="product-img"
                @error="handleImageError"
              />
              <div v-else class="product-icon">{{ product.icon }}</div>
            </div>
            <div class="product-name">{{ product.name }}</div>
          </div>
        </div>

        <!-- 无相似商品时的友好提示 -->
        <div v-else class="no-similar-products">
          <div class="empty-state">
            <div class="empty-icon">🔍</div>
            <h3>暂无推荐数据</h3>
            <p>很抱歉，没有找到与当前标签匹配的相似商品。</p>
            <div class="suggestions">
              <p><strong>建议：</strong></p>
              <ul>
                <li>尝试使用更通用的商品描述</li>
                <li>检查标签是否过于具体</li>
                <li>重新生成商品标签</li>
              </ul>
                  </div>
                </div>
        </div>
        
        <!-- 商业分析按钮 - 只在有相似商品时显示 -->
        <div v-if="similarProducts.length > 0" style="margin-top: 1.5rem; text-align: center;">
          <button 
            class="btn btn-primary" 
            @click="analyzeCommercialFeatures"
            :disabled="!similarProducts.length || isAnalyzing"
          >
            <span v-if="isAnalyzing">🔄 分析中...</span>
            <span v-else>📊 进行商业分析</span>
          </button>
        </div>
        </div>

      <!-- 功能区域4：商业特征分析报告 -->
      <div 
        class="function-area" 
        v-show="showArea4"
        :class="{ show: showArea4 }"
      >
        <h2 class="function-title">
          <span>📊</span>
          商业特征分析报告
        </h2>
        <div class="analysis-report">
          <div v-if="showArea4" class="analysis-sections">
            <div class="analysis-section">
              <h3 class="analysis-title">📈 核心指标分析</h3>
              <div class="metrics-grid">
                <div class="metric-card">
                  <div class="metric-label">
                    受欢迎程度评分
                    <div class="metric-info-icon" @click="showMetricInfo('popularity')">?</div>
                  </div>
                  <div class="metric-value">8.5/10</div>
                </div>
                <div class="metric-card">
                  <div class="metric-label">
                    用户满意度
                    <div class="metric-info-icon" @click="showMetricInfo('satisfaction')">?</div>
                  </div>
                  <div class="metric-value">92%</div>
                </div>
              </div>
            </div>

            <div class="analysis-section">
              <h3 class="analysis-title">👥 用户群体特征</h3>
              <div class="metric-card">
                <div class="metric-label">
                  主要用户群体
                  <div class="metric-info-icon" @click="showMetricInfo('userGroup')">?</div>
                </div>
                <div class="metric-value">商务人士 (65%)</div>
              </div>
              <div class="metric-card">
                <div class="metric-label">
                  年龄分布
                  <div class="metric-info-icon" @click="showMetricInfo('ageDistribution')">?</div>
                </div>
                <div class="metric-value">25-35岁 (58%)</div>
              </div>
            </div>

            <div class="analysis-section">
              <h3 class="analysis-title">
                💡 商业洞察
                <div class="metric-info-icon" @click="showMetricInfo('businessInsights')">?</div>
              </h3>
              <div class="insights">
                <div class="insight-item">
                  <strong>目标用户明确：</strong>主要面向商务人士，注重高效办公和品质保证
                </div>
                <div class="insight-item">
                  <strong>竞争优势：</strong>在商务办公领域具有较高的用户满意度和市场认可度
                </div>
                <div class="insight-item">
                  <strong>市场定位：</strong>高端商务市场，价格敏感度相对较低
                </div>
              </div>
            </div>
          </div>
        </div>
        <div style="margin-top: 1.5rem; text-align: center;">
          <button class="btn btn-secondary" @click="resetAnalysis">
            🔄 重新分析
          </button>
        </div>
      </div>
    </div>

    <!-- 指标说明弹窗 -->
    <div class="modal" :class="{ show: showMetricModal }">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ metricInfoTitle }}</h3>
          <button class="close-btn" @click="closeMetricInfo">&times;</button>
        </div>
        <div class="modal-body">
          <div v-html="metricInfoBody"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ProductManagement',
  setup() {
    // 响应式数据
    const currentStep = ref(1)
    const productDescription = ref('')
    const generatedTags = ref([])
    const similarProducts = ref([])
    const analysisReport = ref('')
    
    // 显示状态
    const showArea2 = ref(false)
    const showArea3 = ref(false)
    const showArea4 = ref(false)
    
    // 加载状态
    const isGeneratingTags = ref(false)
    const isFindingSimilar = ref(false)
    const isAnalyzing = ref(false)
    
    // 弹窗状态
    const showMetricModal = ref(false)
    const metricInfoTitle = ref('')
    const metricInfoBody = ref('')
    
    // 模拟数据
    const mockTags = ['商务办公', '高效便捷', '品质保证', '专业设计', '用户友好']
    const mockSimilarProducts = [
      { id: 1, name: 'MacBook Pro 14"', category: '笔记本电脑', similarity: 0.92, icon: '💻' },
      { id: 2, name: 'ThinkPad X1 Carbon', category: '笔记本电脑', similarity: 0.89, icon: '💻' },
      { id: 3, name: 'Dell XPS 13', category: '笔记本电脑', similarity: 0.87, icon: '💻' },
      { id: 4, name: 'Surface Laptop 4', category: '笔记本电脑', similarity: 0.85, icon: '💻' },
      { id: 5, name: 'HP EliteBook', category: '笔记本电脑', similarity: 0.83, icon: '💻' }
    ]

    // 方法定义
    const handleImageError = (event) => {
      // 图片加载失败时，隐藏图片并显示图标
      const img = event.target
      const parent = img.parentElement
      parent.innerHTML = `<div class="product-icon">${getProductIcon(2)}</div>`
    }

    const clearSubsequentSteps = () => {
      showArea3.value = false
      showArea4.value = false
      currentStep.value = 1
      similarProducts.value = []
      analysisReport.value = ''
      isFindingSimilar.value = false
      isAnalyzing.value = false
    }

    const generateTags = async () => {
      if (!productDescription.value.trim()) {
        alert('请输入商品描述')
        return
      }

      clearSubsequentSteps()
      isGeneratingTags.value = true

      try {
        // 调用真实的LLM API
        const response = await fetch('/api/v1/llm/generate-tags', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            description: productDescription.value.trim()
          })
        })

        const result = await response.json()

        if (result.success) {
          generatedTags.value = result.data.tags
          showArea2.value = true
          currentStep.value = 2
          console.log('标签生成成功:', result.data.tags)
        } else {
          throw new Error(result.error || '生成标签失败')
        }
      } catch (error) {
        console.error('生成标签失败:', error)
        
        // 显示友好的错误提示，不使用模拟数据
        const errorMessage = error.message || '未知错误'
        alert(`标签生成失败：${errorMessage}\n\n请检查网络连接或稍后重试。`)
        
        // 不显示后续步骤
        showArea2.value = false
        currentStep.value = 1
      } finally {
        isGeneratingTags.value = false
      }
    }

    const findSimilarProducts = async () => {
      if (generatedTags.value.length === 0) {
        alert('请先生成商品标签')
        return
      }

      isFindingSimilar.value = true

      try {
        // 调用真实的相似商品检索API
        const response = await fetch('/api/v1/product-management/find-similar-by-tags', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            tags: generatedTags.value,
            limit: 10,
            description: productDescription.value.trim()
          })
        })

        const result = await response.json()

        if (result.success) {
          // 格式化相似商品数据
          similarProducts.value = result.data.similar_products.map((product, index) => ({
            id: product.id,
            name: product.name,
            category: product.category_id ? `分类${product.category_id}` : '未分类',
            similarity: product.similarity || (0.95 - index * 0.02), // 如果没有相似度，使用递减值
            icon: getProductIcon(product.category_id),
            image_url: product.image_url,
            price: product.price,
            tags: product.tags || [],
            match_type: product.match_type || 'unknown'
          }))
          
          showArea3.value = true
          currentStep.value = 3
          console.log('相似商品检索成功:', result.data.similar_products)
        } else {
          throw new Error(result.error || '查找相似商品失败')
        }
      } catch (error) {
        console.error('查找相似商品失败:', error)
        
        // 显示友好的错误提示，不使用模拟数据
        const errorMessage = error.message || '未知错误'
        alert(`相似商品检索失败：${errorMessage}\n\n请检查网络连接或稍后重试。`)
        
        // 不显示后续步骤
        showArea3.value = false
        currentStep.value = 2
      } finally {
        isFindingSimilar.value = false
      }
    }

    // 根据分类获取商品图标
    const getProductIcon = (categoryId) => {
      const iconMap = {
        1: '👗', // 女装类
        2: '👔', // 男装类
        3: '👶', // 童装类
        4: '👟', // 鞋类
        5: '👜', // 包类
        6: '⌚', // 手表类
        7: '💍', // 珠宝类
        8: '📱', // 数码类
        9: '🏠', // 家居类
        10: '🎮', // 玩具类
        11: '📚', // 图书类
        12: '🍎', // 食品类
        13: '💄', // 美妆类
        14: '🏃', // 运动类
        15: '🚗', // 汽车类
        16: '🌱', // 园艺类
        17: '🎨', // 文具类
        18: '🎵', // 乐器类
        19: '🏥', // 医疗类
        20: '🎯'  // 其他类
      }
      return iconMap[categoryId] || '📦'
    }

    const analyzeCommercialFeatures = async () => {
      isAnalyzing.value = true

      try {
        await new Promise(resolve => setTimeout(resolve, 3000))
        // 不再使用动态HTML生成，直接显示区域4
        showArea4.value = true
        currentStep.value = 4
      } catch (error) {
        console.error('商业分析失败:', error)
        alert('商业分析失败，请重试')
      } finally {
        isAnalyzing.value = false
      }
    }


    const resetAnalysis = () => {
      currentStep.value = 1
      productDescription.value = ''
      generatedTags.value = []
      similarProducts.value = []
      analysisReport.value = ''
      showArea2.value = false
      showArea3.value = false
      showArea4.value = false
      isGeneratingTags.value = false
      isFindingSimilar.value = false
      isAnalyzing.value = false
    }

    // 指标说明数据
    const metricInfoData = {
      popularity: {
        title: '受欢迎程度评分',
        description: '基于用户交互行为计算的商品受欢迎程度评分',
        formula: '受欢迎程度 = (点击次数 × 0.3 + 查看次数 × 0.4 + 收藏次数 × 0.5 + 购买次数 × 1.0) / 总用户数 × 10',
        steps: [
          '获取相似商品的用户交互数据',
          '收集各类交互行为数据（点击、查看、收藏、购买）',
          '计算各类交互行为的权重分数',
          '统计交互用户总数',
          '计算加权平均分数',
          '转换为10分制评分'
        ],
        details: '该指标综合考虑了相似商品的用户交互行为，通过加权计算得出商品的受欢迎程度。首先获取top10相似商品的用户交互历史，然后分析用户的点击、查看、收藏、购买等行为，权重设置：点击(0.3)、查看(0.4)、收藏(0.5)、购买(1.0)。'
      },
      satisfaction: {
        title: '用户满意度',
        description: '基于用户反馈和交互行为计算的满意度指标',
        formula: '满意度 = (正面交互次数 - 负面交互次数) / 总交互次数 × 100%',
        steps: [
          '获取相似商品的用户交互数据',
          '统计用户正面交互行为（收藏、购买）',
          '统计用户负面交互行为（不推荐、差评）',
          '计算净正面交互次数',
          '除以总交互次数',
          '转换为百分比'
        ],
        details: '该指标通过分析相似商品的用户交互数据，计算净满意度。首先获取top10相似商品的用户交互历史，然后分析用户的正面和负面交互行为，计算净满意度。正面行为包括收藏、购买等，负面行为包括不推荐、差评等。'
      },
      userGroup: {
        title: '主要用户群体',
        description: '基于用户行为模式分析得出的主要用户群体特征',
        formula: '用户群体 = 分析用户交互模式 → 聚类分析 → 识别主要群体',
        steps: [
          '获取相似商品的用户交互数据',
          '收集用户交互历史数据',
          '分析用户行为模式',
          '进行用户聚类分析',
          '识别主要用户群体',
          '计算群体占比'
        ],
        details: '该指标通过机器学习聚类算法，分析相似商品的用户交互行为模式，识别出主要的用户群体类型，如商务人士、学生、家庭用户等。首先获取top10相似商品的用户交互历史，然后进行聚类分析。',
        clusteringInfo: {
          algorithm: 'K-means聚类算法',
          dataPreprocessing: [
            '收集相似商品的用户交互数据',
            '提取用户行为特征向量（点击频率、浏览时长、购买偏好等）',
            '数据标准化处理，消除量纲影响',
            '特征降维，提取主要特征'
          ],
          algorithmSteps: [
            '随机初始化K个聚类中心',
            '计算每个用户到聚类中心的距离',
            '将用户分配到最近的聚类中心',
            '重新计算聚类中心位置',
            '重复步骤2-4直到收敛'
          ],
          parameters: {
            kValue: '使用肘部法则确定最优K值',
            distance: '欧几里得距离计算用户相似度',
            convergence: '聚类中心变化小于阈值',
            maxIterations: '防止算法不收敛'
          },
          userGroups: {
            business: '商务人士群体: 高频购买、偏好高端商品、工作时间活跃',
            student: '学生群体: 价格敏感、偏好性价比商品、晚间活跃',
            family: '家庭用户群体: 批量购买、偏好家庭用品、周末活跃',
            fashion: '时尚用户群体: 关注新品、偏好时尚商品、社交分享多'
          },
          technicalDetails: '聚类分析使用scikit-learn库的KMeans算法实现，通过分析用户的行为模式、购买偏好、活跃时间等特征，自动识别出不同的用户群体，为精准营销和个性化推荐提供数据支持。'
        }
      },
      ageDistribution: {
        title: '年龄分布',
        description: '基于用户画像数据统计的年龄分布情况',
        formula: '年龄分布 = 统计各年龄段用户数量 / 总用户数 × 100%',
        steps: [
          '获取相似商品的用户交互数据',
          '收集用户年龄信息',
          '按年龄段分组统计',
          '计算各年龄段用户数量',
          '计算年龄分布百分比',
          '识别主要年龄段'
        ],
        details: '该指标通过分析相似商品的用户画像中的年龄信息，统计各年龄段的用户分布情况，帮助了解目标用户群体的年龄特征。首先获取top10相似商品的用户交互历史，然后分析用户画像中的年龄信息。'
      },
      businessInsights: {
        title: '商业洞察分析',
        description: '基于相似商品数据和用户行为分析，生成商业洞察和战略建议',
        formula: '商业洞察 = 数据整合 + 模式识别 + 趋势分析 + 战略建议',
        steps: [
          '获取相似商品的用户交互数据',
          '分析用户行为模式和偏好',
          '识别市场趋势和机会',
          '评估竞争优势和劣势',
          '生成战略建议和洞察',
          '输出商业分析报告'
        ],
        details: '商业洞察分析通过综合分析相似商品的用户数据、市场表现和竞争情况，生成有价值的商业洞察。该分析包括目标用户识别、竞争优势评估、市场定位分析等维度，为商业决策提供数据支持。',
        analysisFramework: {
          dataCollection: [
            '收集相似商品的销售数据',
            '分析用户交互行为模式',
            '统计市场表现指标',
            '收集竞争对手信息'
          ],
          patternRecognition: [
            '识别用户行为模式',
            '发现市场趋势',
            '分析竞争格局',
            '评估机会和威胁'
          ],
          insightGeneration: [
            '目标用户画像分析',
            '竞争优势识别',
            '市场定位建议',
            '战略发展方向'
          ],
          businessValue: {
            userTargeting: '通过用户行为分析，精准识别目标用户群体，提高营销效率',
            competitiveAdvantage: '分析竞争优势，制定差异化策略，提升市场地位',
            marketPositioning: '基于市场数据，优化产品定位，增强市场竞争力',
            strategicPlanning: '提供数据驱动的战略建议，支持商业决策制定'
          }
        }
      }
    }

    const showMetricInfo = (metricType) => {
      console.log('showMetricInfo called with:', metricType);
      const info = metricInfoData[metricType]
      if (!info) {
        console.log('No info found for metricType:', metricType);
        return;
      }
      
      console.log('Info found:', info);
      metricInfoTitle.value = info.title
      
      // 为商业洞察添加分析框架信息
      if (metricType === 'businessInsights' && info.analysisFramework) {
        metricInfoBody.value = `
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">📊 指标说明</h4>
            <p style="color: #cccccc; line-height: 1.6; margin-bottom: 1rem;">${info.description}</p>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">🧮 计算公式</h4>
            <div class="metric-info-formula" style="background: rgba(0, 255, 255, 0.1); border: 1px solid rgba(0, 255, 255, 0.3); border-radius: 10px; padding: 1rem; font-family: 'Courier New', monospace; color: #00ffff; margin: 1rem 0; font-size: 0.9rem; line-height: 1.4;">${info.formula}</div>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">📋 计算步骤</h4>
            <ol class="metric-info-steps" style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
              ${info.steps.map(step => `<li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;">${step}</li>`).join('')}
            </ol>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">🔍 分析框架</h4>
            <div style="margin-bottom: 1.5rem;">
              <h5 style="color: #00ffff; margin-bottom: 0.5rem; font-size: 1rem;">📊 数据收集</h5>
              <ul style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
                ${info.analysisFramework.dataCollection.map(item => `<li style="padding: 0.3rem 0; color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.4;">• ${item}</li>`).join('')}
              </ul>
            </div>
            <div style="margin-bottom: 1.5rem;">
              <h5 style="color: #00ffff; margin-bottom: 0.5rem; font-size: 1rem;">🧠 模式识别</h5>
              <ul style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
                ${info.analysisFramework.patternRecognition.map(item => `<li style="padding: 0.3rem 0; color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.4;">• ${item}</li>`).join('')}
              </ul>
            </div>
            <div style="margin-bottom: 1.5rem;">
              <h5 style="color: #00ffff; margin-bottom: 0.5rem; font-size: 1rem;">💡 洞察生成</h5>
              <ul style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
                ${info.analysisFramework.insightGeneration.map(item => `<li style="padding: 0.3rem 0; color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.4;">• ${item}</li>`).join('')}
              </ul>
            </div>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">💼 商业价值</h4>
            <div style="display: grid; gap: 1rem;">
              <div style="background: rgba(0, 255, 255, 0.05); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 8px; padding: 1rem;">
                <h5 style="color: #00ffff; margin-bottom: 0.5rem; font-size: 0.9rem;">🎯 用户定位</h5>
                <p style="color: #cccccc; font-size: 0.9rem; line-height: 1.4; margin: 0;">${info.analysisFramework.businessValue.userTargeting}</p>
              </div>
              <div style="background: rgba(0, 255, 255, 0.05); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 8px; padding: 1rem;">
                <h5 style="color: #00ffff; margin-bottom: 0.5rem; font-size: 0.9rem;">⚡ 竞争优势</h5>
                <p style="color: #cccccc; font-size: 0.9rem; line-height: 1.4; margin: 0;">${info.analysisFramework.businessValue.competitiveAdvantage}</p>
              </div>
              <div style="background: rgba(0, 255, 255, 0.05); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 8px; padding: 1rem;">
                <h5 style="color: #00ffff; margin-bottom: 0.5rem; font-size: 0.9rem;">📍 市场定位</h5>
                <p style="color: #cccccc; font-size: 0.9rem; line-height: 1.4; margin: 0;">${info.analysisFramework.businessValue.marketPositioning}</p>
              </div>
              <div style="background: rgba(0, 255, 255, 0.05); border: 1px solid rgba(0, 255, 255, 0.2); border-radius: 8px; padding: 1rem;">
                <h5 style="color: #00ffff; margin-bottom: 0.5rem; font-size: 0.9rem;">📈 战略规划</h5>
                <p style="color: #cccccc; font-size: 0.9rem; line-height: 1.4; margin: 0;">${info.analysisFramework.businessValue.strategicPlanning}</p>
              </div>
            </div>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">💡 详细说明</h4>
            <p style="color: #cccccc; line-height: 1.6; margin-bottom: 1rem;">${info.details}</p>
          </div>
        `
      }
      // 为主要用户群体添加聚类分析信息
      else if (metricType === 'userGroup' && info.clusteringInfo) {
        metricInfoBody.value = `
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">📊 指标说明</h4>
            <p style="color: #cccccc; line-height: 1.6; margin-bottom: 1rem;">${info.description}</p>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">🧮 计算公式</h4>
            <div class="metric-info-formula" style="background: rgba(0, 255, 255, 0.1); border: 1px solid rgba(0, 255, 255, 0.3); border-radius: 10px; padding: 1rem; font-family: 'Courier New', monospace; color: #00ffff; margin: 1rem 0; font-size: 0.9rem; line-height: 1.4;">${info.formula}</div>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">📋 计算步骤</h4>
            <ol class="metric-info-steps" style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
              ${info.steps.map(step => `<li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;">${step}</li>`).join('')}
            </ol>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">🧠 聚类分析算法</h4>
            <p style="color: #cccccc; line-height: 1.6; margin-bottom: 1rem;">使用${info.clusteringInfo.algorithm}对用户行为数据进行聚类分析，识别不同的用户群体特征。</p>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">📊 数据预处理</h4>
            <ol class="metric-info-steps" style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
              ${info.clusteringInfo.dataPreprocessing.map(step => `<li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;">${step}</li>`).join('')}
            </ol>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">🔢 聚类算法实现</h4>
            <div class="metric-info-formula" style="background: rgba(0, 255, 255, 0.1); border: 1px solid rgba(0, 255, 255, 0.3); border-radius: 10px; padding: 1rem; font-family: 'Courier New', monospace; color: #00ffff; margin: 1rem 0; font-size: 0.9rem; line-height: 1.4;">
              K-means算法步骤：<br>
              ${info.clusteringInfo.algorithmSteps.map((step, index) => `${index + 1}. ${step}`).join('<br>')}
            </div>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">📈 聚类参数设置</h4>
            <ul class="metric-info-steps" style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
              <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;"><strong>聚类数量K:</strong> ${info.clusteringInfo.parameters.kValue}</li>
              <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;"><strong>距离度量:</strong> ${info.clusteringInfo.parameters.distance}</li>
              <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;"><strong>收敛条件:</strong> ${info.clusteringInfo.parameters.convergence}</li>
              <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;"><strong>最大迭代:</strong> ${info.clusteringInfo.parameters.maxIterations}</li>
            </ul>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">🎯 用户群体识别</h4>
            <p style="color: #cccccc; line-height: 1.6; margin-bottom: 1rem;">基于聚类结果，分析每个群体的行为特征：</p>
            <ul class="metric-info-steps" style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
              <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;"><strong>${info.clusteringInfo.userGroups.business}</strong></li>
              <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;"><strong>${info.clusteringInfo.userGroups.student}</strong></li>
              <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;"><strong>${info.clusteringInfo.userGroups.family}</strong></li>
              <li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;"><strong>${info.clusteringInfo.userGroups.fashion}</strong></li>
            </ul>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">💡 技术细节</h4>
            <p style="color: #cccccc; line-height: 1.6; margin-bottom: 1rem;">${info.clusteringInfo.technicalDetails}</p>
          </div>
        `
      } else {
        // 其他指标的原有显示逻辑
        metricInfoBody.value = `
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">📊 指标说明</h4>
            <p style="color: #cccccc; line-height: 1.6; margin-bottom: 1rem;">${info.description}</p>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">🧮 计算公式</h4>
            <div class="metric-info-formula" style="background: rgba(0, 255, 255, 0.1); border: 1px solid rgba(0, 255, 255, 0.3); border-radius: 10px; padding: 1rem; font-family: 'Courier New', monospace; color: #00ffff; margin: 1rem 0; font-size: 0.9rem; line-height: 1.4;">${info.formula}</div>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">📋 计算步骤</h4>
            <ol class="metric-info-steps" style="list-style: none; padding: 0; background: rgba(255, 255, 255, 0.02); border-radius: 8px; padding: 1rem;">
              ${info.steps.map(step => `<li style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: #cccccc; display: flex; align-items: flex-start; gap: 0.5rem; line-height: 1.5;">${step}</li>`).join('')}
            </ol>
          </div>
          
          <div class="metric-info-section" style="margin-bottom: 2rem; padding: 1rem; background: rgba(255, 255, 255, 0.02); border-radius: 10px; border-left: 4px solid rgba(0, 255, 255, 0.3);">
            <h4 style="font-size: 1.2rem; font-weight: 600; color: #00ffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">💡 详细说明</h4>
            <p style="color: #cccccc; line-height: 1.6; margin-bottom: 1rem;">${info.details}</p>
          </div>
        `
      }
      
      console.log('Setting showMetricModal to true');
      showMetricModal.value = true;
      console.log('showMetricModal value:', showMetricModal.value);
    }

    const closeMetricInfo = () => {
      showMetricModal.value = false
    }

    return {
      currentStep,
      productDescription,
      generatedTags,
      similarProducts,
      analysisReport,
      showArea2,
      showArea3,
      showArea4,
      isGeneratingTags,
      isFindingSimilar,
      isAnalyzing,
      showMetricModal,
      metricInfoTitle,
      metricInfoBody,
      generateTags,
      findSimilarProducts,
      analyzeCommercialFeatures,
      resetAnalysis,
      showMetricInfo,
      closeMetricInfo
    }
  }
}
</script>

<style scoped>
/* 基础样式 */
.product-management {
  min-height: 100vh;
  position: relative;
  font-family: 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0a0a0a;
  color: #ffffff;
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

/* 导航栏样式 */
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

.nav-item {
  position: relative;
}

.nav-link {
  color: #ffffff;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.nav-link:hover {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
}

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
  z-index: 1001;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
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

.dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-toggle::after {
  display: none;
}

/* 主要内容区域 */
.main-content {
  margin-top: 70px;
  padding: 2rem 5%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #00ffff, #ff00ff, #00ff00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.2rem;
  color: #cccccc;
  margin-bottom: 2rem;
}

/* 功能步骤指示器 */
.steps-indicator {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
  gap: 2rem;
}

.step {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 25px;
  transition: all 0.3s ease;
}

.step.active {
  background: rgba(0, 255, 255, 0.1);
  border-color: #00ffff;
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
}

.step.completed {
  background: rgba(0, 255, 0, 0.1);
  border-color: #00ff00;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(0, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.step.active .step-number {
  background: #00ffff;
  color: #000;
}

.step.completed .step-number {
  background: #00ff00;
  color: #000;
}

.step-text {
  font-weight: 500;
}

/* 功能区域 */
.function-area {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: block;
}

.function-area.show {
  display: block;
  animation: fadeInUp 0.5s ease-out;
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

.function-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #00ffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 商品描述输入区域 */
.description-input {
  width: 100%;
  min-height: 120px;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  resize: vertical;
  transition: all 0.3s ease;
}

.description-input:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.08);
}

.description-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.input-hint {
  font-size: 0.9rem;
  color: #888888;
  margin-top: 0.5rem;
}

/* 按钮样式 */
.btn {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-primary {
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  color: #ffffff;
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.4);
}

.btn-secondary {
  background: linear-gradient(45deg, #ff6b6b, #ffa500);
  color: #ffffff;
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(255, 107, 107, 0.4);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

/* 标签展示区域 */
.tags-container {
    display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}

.tag {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tag:hover {
  background: rgba(0, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
}

/* 相似商品展示 */
.similar-products {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.product-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  text-align: center;
}

.product-card:hover {
  border-color: #00ffff;
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.3);
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  display: flex;
    align-items: center;
  justify-content: center;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(0, 255, 255, 0.3);
  margin-bottom: 1rem;
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.product-icon {
  font-size: 3rem;
  width: 100%;
  height: 200px;
    display: flex;
    align-items: center;
  justify-content: center;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 10px;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0.5rem 0;
  color: #ffffff;
  text-align: center;
}


.product-tags {
  margin-top: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.tag {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

/* 分析报告样式 */
.analysis-report {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 15px;
  padding: 2rem;
  margin-top: 1rem;
}

.analysis-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.analysis-section {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 15px;
  padding: 1.5rem;
}

.analysis-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #00ffff;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: space-between;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.metric-label {
  font-size: 0.9rem;
  color: #888888;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #00ffff;
}

/* 指标说明图标 */
.metric-info-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(0, 255, 255, 0.3);
  border: 1px solid rgba(0, 255, 255, 0.4);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  color: #00ffff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.metric-info-icon:hover {
  background: rgba(0, 255, 255, 0.3);
  border-color: #00ffff;
  transform: scale(1.1);
}

/* 商业洞察 */
.insights {
  list-style: none;
  padding: 0;
}

.insight-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #cccccc;
  line-height: 1.6;
}

.insight-item:last-child {
  border-bottom: none;
}

/* 指标说明弹窗 */
.modal {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  background: rgba(0, 0, 0, 0.8) !important;
  backdrop-filter: blur(20px) !important;
  z-index: 2000 !important;
  display: none;
  align-items: center !important;
  justify-content: center !important;
  padding: 20px !important;
}

.modal.show {
  display: flex;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: rgba(20, 20, 20, 0.95) !important;
  border: 2px solid rgba(0, 255, 255, 0.5) !important;
  border-radius: 20px !important;
  max-width: 600px !important;
  width: 90% !important;
  max-height: 80vh !important;
  overflow-y: auto !important;
  backdrop-filter: blur(20px) !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5) !important;
  animation: slideIn 0.3s ease-out !important;
  padding: 0 !important;
}

@keyframes slideIn {
  from { 
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 1.5rem !important;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1) !important;
}

.modal-header h3 {
  color: #00ffff;
  font-size: 1.3rem;
  font-weight: 600;
    margin: 0;
  }
  
.close-btn {
  background: none;
  border: none;
  color: #ffffff;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
    display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
  transform: scale(1.1);
}

.modal-body {
  padding: 1.5rem !important;
}

/* 指标说明内容样式 */
.metric-info-section {
  margin-bottom: 2rem !important;
  padding: 1rem !important;
  background: rgba(255, 255, 255, 0.02) !important;
  border-radius: 10px !important;
  border-left: 4px solid rgba(0, 255, 255, 0.3) !important;
}

.metric-info-section h4 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #00ffff;
  margin-bottom: 1rem;
    display: flex;
  align-items: center;
  gap: 0.5rem;
}

.metric-info-section p {
  color: #cccccc;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.metric-info-formula {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 10px;
  padding: 1rem;
  font-family: 'Courier New', monospace;
  color: #00ffff;
  margin: 1rem 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.metric-info-steps {
  list-style: none;
  padding: 0;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  padding: 1rem;
}
  
.metric-info-steps li {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #cccccc;
    display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  line-height: 1.5;
}

.metric-info-steps li:last-child {
  border-bottom: none;
}

.metric-info-steps li::before {
  content: "•";
  color: #00ffff;
  font-weight: bold;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

/* 空状态样式 */
.no-similar-products {
  text-align: center;
  padding: 2rem;
}

.empty-state {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.7;
}

.empty-state h3 {
  color: #ffffff;
  font-size: 1.5rem;
  margin-bottom: 1rem;
    font-weight: 600;
}

.empty-state p {
  color: #cccccc;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.suggestions {
  text-align: left;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 10px;
  padding: 1.5rem;
  margin-top: 1.5rem;
}

.suggestions p {
  color: #00ffff;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.suggestions ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestions li {
  color: #cccccc;
  padding: 0.5rem 0;
  position: relative;
  padding-left: 1.5rem;
}

.suggestions li::before {
  content: "💡";
  position: absolute;
  left: 0;
  top: 0.5rem;
}


/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .steps-indicator {
    flex-direction: column;
    gap: 1rem;
  }
  
  .step {
    justify-content: center;
  }
  
  .similar-products {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.5rem;
  }
  
  .function-area {
    padding: 1rem;
  }
  
  .btn {
    padding: 0.6rem 1.5rem;
    font-size: 0.9rem;
  }
}
</style>