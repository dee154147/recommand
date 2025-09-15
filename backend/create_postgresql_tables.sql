-- PostgreSQL + pgvector 表结构创建脚本

-- 创建分类表
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建商品表
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    category_id INTEGER REFERENCES categories(id),
    image_url VARCHAR(500),
    tags TEXT,  -- JSON字符串存储标签
    embedding TEXT,  -- 原始JSON格式向量（保留兼容性）
    product_vector vector(200),  -- pgvector格式向量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建商品标签表
CREATE TABLE IF NOT EXISTS product_tags (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    tag VARCHAR(100) NOT NULL,
    weight DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建标签向量表
CREATE TABLE IF NOT EXISTS tag_vectors (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(100) UNIQUE NOT NULL,
    vector TEXT,  -- JSON格式存储标签向量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(120) UNIQUE,
    preferences TEXT,  -- JSON格式存储用户偏好
    behavior_vector TEXT,  -- JSON格式存储行为向量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建用户交互表
CREATE TABLE IF NOT EXISTS user_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    interaction_type VARCHAR(50) NOT NULL,
    interaction_score FLOAT DEFAULT 1.0,
    session_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建推荐缓存表
CREATE TABLE IF NOT EXISTS recommendation_cache (
    id SERIAL PRIMARY KEY,
    cache_key VARCHAR(200) UNIQUE NOT NULL,
    cache_type VARCHAR(50) NOT NULL,
    target_id VARCHAR(50) NOT NULL,
    recommendations TEXT NOT NULL,  -- JSON格式存储推荐结果
    similarity_scores TEXT,  -- JSON格式存储相似度分数
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);
CREATE INDEX IF NOT EXISTS idx_products_embedding ON products(embedding);

-- 创建向量索引
CREATE INDEX IF NOT EXISTS products_product_vector_idx 
ON products USING ivfflat (product_vector vector_cosine_ops) 
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_product_tags_product_id ON product_tags(product_id);
CREATE INDEX IF NOT EXISTS idx_product_tags_tag ON product_tags(tag);
CREATE INDEX IF NOT EXISTS idx_tag_vectors_tag ON tag_vectors(tag);
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);

-- 创建用户交互索引
CREATE INDEX IF NOT EXISTS idx_user_product ON user_interactions(user_id, product_id);
CREATE INDEX IF NOT EXISTS idx_interaction_type ON user_interactions(interaction_type);
CREATE INDEX IF NOT EXISTS idx_created_at ON user_interactions(created_at);

-- 创建推荐缓存索引
CREATE INDEX IF NOT EXISTS idx_cache_key ON recommendation_cache(cache_key);
CREATE INDEX IF NOT EXISTS idx_cache_expires ON recommendation_cache(expires_at);
