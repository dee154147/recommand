-- 创建数据库扩展（用于向量搜索）
CREATE EXTENSION IF NOT EXISTS vector;

-- 创建用户和权限
CREATE USER recommendation_user WITH PASSWORD 'recommendation_password';
GRANT ALL PRIVILEGES ON DATABASE recommendation_db TO recommendation_user;

-- 设置时区
SET timezone = 'UTC';
