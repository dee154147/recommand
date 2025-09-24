import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://liuzhichao@localhost:5432/recommendation_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis配置（用于缓存）
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # 推荐系统配置
    VECTOR_MODEL_PATH = os.environ.get('VECTOR_MODEL_PATH') or '../model/Tencent_AILab_ChineseEmbedding.bin'
    PRODUCT_DATA_PATH = os.environ.get('PRODUCT_DATA_PATH') or '../data/product.txt'
    PRODUCT_TYPE_PATH = os.environ.get('PRODUCT_TYPE_PATH') or '../data/productType.json'
    
    # 分页配置
    POSTS_PER_PAGE = 20
    RECOMMENDATIONS_PER_PAGE = 10

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://liuzhichao@localhost:5432/recommendation_db'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or 'sqlite:///recommendation_prod.db'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
