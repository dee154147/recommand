# 智能推荐系统

基于内容的商品推荐系统，使用机器学习算法为用户提供个性化的商品推荐服务。

## 项目特性

- 🧠 **智能推荐算法**: 基于内容的推荐算法，支持商品相似度计算
- 📊 **数据分析**: 强大的用户行为分析和商品数据管理
- 🚀 **高性能**: 支持大规模并发访问，毫秒级响应
- 🔒 **安全可靠**: 企业级安全保障，数据加密存储
- 📱 **响应式设计**: 支持桌面端和移动端访问
- 🐳 **容器化部署**: Docker支持，一键部署

## 技术栈

### 后端
- **框架**: Flask 2.3.3
- **数据库**: PostgreSQL + Redis
- **机器学习**: scikit-learn, gensim, jieba
- **向量模型**: 腾讯AI实验室中文词向量

### 前端
- **框架**: Vue.js 3
- **UI库**: Element Plus
- **构建工具**: Vite
- **样式**: CSS3 + 现代科技风设计

## 项目结构

```
recommand2/
├── backend/                 # Flask后端
│   ├── app/                # 应用核心
│   │   ├── api/           # API路由
│   │   ├── main/          # 主页面路由
│   │   ├── models.py      # 数据模型
│   │   └── services/      # 业务逻辑层
│   ├── config.py          # 配置文件
│   └── run.py             # 应用入口
├── frontend/              # Vue.js前端
├── data/                  # 数据文件
│   ├── product.txt       # 商品数据
│   └── productType.json  # 商品分类
├── model/                 # 机器学习模型
│   └── Tencent_AILab_ChineseEmbedding.bin
├── docs/                  # 项目文档
└── docker-compose.yml     # Docker编排文件
```

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+ (可选，第一阶段使用模拟数据)
- Redis 6+ (可选，第一阶段使用模拟数据)

### 🚀 一键启动 (推荐)

```bash
# 克隆项目
git clone <repository-url>
cd recommand2

# 一键启动所有服务
./start.sh
```

### 📱 手动启动

#### 1. 启动后端服务
```bash
cd backend
pip3 install -r requirements.txt
python3 run.py
```
后端服务将在 http://localhost:5001 启动

#### 2. 启动前端服务 (另开终端)
```bash
cd frontend
npm install
npm run dev
```
前端服务将在 http://localhost:3000 启动

### 🛑 停止服务
```bash
./stop.sh
```

### 🌐 访问应用
- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:5001
- **健康检查**: http://localhost:5001/health

### 📋 功能模块
- **商品检索**: 搜索、筛选、排序商品
- **商品管理**: 商品的增删改查管理
- **用户交互**: 用户行为分析和推荐效果展示

### Docker部署

1. **构建并启动服务**
```bash
docker-compose up -d
```

2. **查看服务状态**
```bash
docker-compose ps
```

3. **查看日志**
```bash
docker-compose logs -f recommendation-api
```

## API文档

### 商品相关接口

- `GET /api/products` - 获取商品列表
- `GET /api/products/{id}` - 获取商品详情
- `GET /api/categories` - 获取商品分类
- `GET /api/search?q={query}` - 搜索商品

### 推荐相关接口

- `GET /api/recommendations?product_id={id}` - 获取相似商品推荐
- `GET /api/recommendations?user_id={id}` - 获取用户个性化推荐

### 用户相关接口

- `POST /api/users` - 创建用户
- `GET /api/users/{id}` - 获取用户信息
- `POST /api/interactions` - 记录用户交互

## 推荐算法

### 基于内容的推荐
- 使用jieba分词提取商品关键词
- 通过腾讯词向量模型计算商品特征向量
- 基于余弦相似度计算商品相似性

### 协同过滤推荐
- 分析用户交互行为模式
- 找到相似用户群体
- 推荐相似用户喜欢的商品

### 混合推荐策略
- 结合内容推荐和协同过滤
- 根据用户行为动态调整权重
- 实时更新推荐结果

## 开发指南

### 代码规范
- 使用Black进行代码格式化
- 使用flake8进行代码检查
- 遵循PEP8编码规范

### 测试
```bash
# 运行测试
pytest

# 生成测试覆盖率报告
pytest --cov=app
```

### 部署
```bash
# 生产环境部署
docker-compose -f docker-compose.prod.yml up -d
```

## 许可证

MIT License

## 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 联系方式

- 项目地址: [GitHub Repository]
- 问题反馈: [GitHub Issues]
- 邮箱: contact@example.com
