#!/usr/bin/env python3
"""
推荐系统Flask应用启动文件
"""

import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product, Category, User, UserInteraction, RecommendationCache
from flask_migrate import upgrade
from config import config

# 创建应用实例
app = create_app(config['development'])

@app.shell_context_processor
def make_shell_context():
    """Shell上下文处理器"""
    return {
        'db': db,
        'Product': Product,
        'Category': Category,
        'User': User,
        'UserInteraction': UserInteraction,
        'RecommendationCache': RecommendationCache
    }

@app.cli.command()
def init_db():
    """初始化数据库"""
    db.create_all()
    print("Database initialized successfully!")

@app.cli.command()
def migrate_db():
    """迁移数据库"""
    upgrade()
    print("Database migration completed!")

if __name__ == '__main__':
    # 开发环境运行
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True,
        threaded=True,  # 启用多线程
        use_reloader=False  # 禁用自动重载以避免端口冲突
    )
