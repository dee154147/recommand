import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # 注册蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 注册数据处理路由
    from app.api.data_routes import data_bp
    from app.api.search_routes import search_bp
    from app.api.recommendation_routes import recommendation_bp
    from app.api.similar_product_routes import similar_product_bp
    app.register_blueprint(data_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(similar_product_bp)
    
    # 在应用启动时预加载词向量模型（暂时禁用，避免启动卡住）
    # with app.app_context():
    #     try:
    #         from app.services.recommendation_service import RecommendationService
    #         import logging
    #         
    #         logger = logging.getLogger(__name__)
    #         logger.info("应用启动，正在预加载词向量模型...")
    #         
    #         service = RecommendationService()
    #         if service.load_word_vectors():
    #             logger.info("词向量模型预加载成功")
    #         else:
    #             logger.warning("词向量模型预加载失败")
    #             
    #     except Exception as e:
    #         logger.error(f"预加载词向量模型失败: {str(e)}")
    
    return app

# 导入模型以确保它们被注册
from app import models
