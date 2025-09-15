#!/usr/bin/env python3
"""
数据库迁移脚本：从SQLite迁移到PostgreSQL + pgvector
"""

import os
import sys
import json
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 添加项目路径
sys.path.append(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库配置
SQLITE_DB_PATH = 'recommendation_dev.db'
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'liuzhichao',
    'password': '',
    'database': 'recommendation_db'
}

def create_postgres_database():
    """创建PostgreSQL数据库"""
    try:
        # 连接到默认数据库
        conn = psycopg2.connect(
            host=POSTGRES_CONFIG['host'],
            port=POSTGRES_CONFIG['port'],
            user=POSTGRES_CONFIG['user'],
            password=POSTGRES_CONFIG['password'],
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute(f"CREATE DATABASE {POSTGRES_CONFIG['database']}")
        logger.info(f"成功创建数据库: {POSTGRES_CONFIG['database']}")
        
        cursor.close()
        conn.close()
        
    except psycopg2.errors.DuplicateDatabase:
        logger.info(f"数据库 {POSTGRES_CONFIG['database']} 已存在")
    except Exception as e:
        logger.error(f"创建数据库失败: {e}")
        raise

def install_pgvector_extension():
    """安装pgvector扩展"""
    try:
        # 连接到目标数据库
        conn = psycopg2.connect(
            host=POSTGRES_CONFIG['host'],
            port=POSTGRES_CONFIG['port'],
            user=POSTGRES_CONFIG['user'],
            password=POSTGRES_CONFIG['password'],
            database=POSTGRES_CONFIG['database']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # 安装pgvector扩展
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        logger.info("成功安装pgvector扩展")
        
        # 验证扩展安装
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector'")
        result = cursor.fetchone()
        if result:
            logger.info("pgvector扩展验证成功")
        else:
            logger.error("pgvector扩展验证失败")
            raise Exception("pgvector扩展安装失败")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"安装pgvector扩展失败: {e}")
        raise

def migrate_data():
    """迁移数据从SQLite到PostgreSQL"""
    try:
        # 使用Flask应用上下文
        from app import create_app, db
        from app.models import Product, Category, ProductTag, TagVector
        
        app = create_app()
        
        # 连接PostgreSQL数据库
        postgres_url = f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}"
        postgres_engine = create_engine(postgres_url)
        postgres_session = sessionmaker(bind=postgres_engine)()
        
        logger.info("开始数据迁移...")
        
        with app.app_context():
            # 迁移分类数据
            logger.info("迁移分类数据...")
            categories = Category.query.all()
            for category in categories:
                postgres_session.execute(text("""
                    INSERT INTO categories (id, name, description, parent_id, created_at)
                    VALUES (:id, :name, :description, :parent_id, :created_at)
                    ON CONFLICT (id) DO NOTHING
                """), {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'parent_id': category.parent_id,
                    'created_at': category.created_at
                })
        
            # 迁移商品数据
            logger.info("迁移商品数据...")
            products = Product.query.all()
            for product in products:
                # 处理向量数据
                embedding_vector = None
                if product.embedding:
                    try:
                        vector_data = json.loads(product.embedding)
                        # 转换为PostgreSQL vector格式
                        embedding_vector = '[' + ','.join(map(str, vector_data)) + ']'
                    except:
                        logger.warning(f"商品 {product.id} 的向量数据格式错误")
                
                postgres_session.execute(text("""
                    INSERT INTO products (id, name, description, price, category_id, image_url, tags, embedding, product_vector, created_at, updated_at)
                    VALUES (:id, :name, :description, :price, :category_id, :image_url, :tags, :embedding, :product_vector, :created_at, :updated_at)
                    ON CONFLICT (id) DO NOTHING
                """), {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'category_id': product.category_id,
                    'image_url': product.image_url,
                    'tags': product.tags,
                    'embedding': product.embedding,
                    'product_vector': embedding_vector,
                    'created_at': product.created_at,
                    'updated_at': product.updated_at
                })
        
            # 迁移商品标签数据
            logger.info("迁移商品标签数据...")
            product_tags = ProductTag.query.all()
            for tag in product_tags:
                postgres_session.execute(text("""
                    INSERT INTO product_tags (id, product_id, tag, weight, created_at)
                    VALUES (:id, :product_id, :tag, :weight, :created_at)
                    ON CONFLICT (id) DO NOTHING
                """), {
                    'id': tag.id,
                    'product_id': tag.product_id,
                    'tag': tag.tag,
                    'weight': tag.weight,
                    'created_at': tag.created_at
                })
            
            # 迁移标签向量数据
            logger.info("迁移标签向量数据...")
            tag_vectors = TagVector.query.all()
            for tag_vector in tag_vectors:
                vector_data = None
                if tag_vector.vector:
                    try:
                        vector_list = json.loads(tag_vector.vector)
                        vector_data = '[' + ','.join(map(str, vector_list)) + ']'
                    except:
                        logger.warning(f"标签 {tag_vector.tag} 的向量数据格式错误")
                
                postgres_session.execute(text("""
                    INSERT INTO tag_vectors (id, tag, vector, created_at)
                    VALUES (:id, :tag, :vector, :created_at)
                    ON CONFLICT (id) DO NOTHING
                """), {
                    'id': tag_vector.id,
                    'tag': tag_vector.tag,
                    'vector': tag_vector.vector,
                    'created_at': tag_vector.created_at
                })
        
            # 提交事务
            postgres_session.commit()
            logger.info("数据迁移完成")
            
            # 关闭连接
            postgres_session.close()
        
    except Exception as e:
        logger.error(f"数据迁移失败: {e}")
        raise

def create_vector_index():
    """创建向量索引"""
    try:
        postgres_url = f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}"
        postgres_engine = create_engine(postgres_url)
        
        with postgres_engine.connect() as conn:
            # 创建向量索引
            logger.info("创建向量索引...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS products_product_vector_idx 
                ON products USING ivfflat (product_vector vector_cosine_ops) 
                WITH (lists = 100)
            """))
            
            # 分析表以更新统计信息
            logger.info("更新数据库统计信息...")
            conn.execute(text("ANALYZE products"))
            conn.execute(text("ANALYZE product_tags"))
            conn.execute(text("ANALYZE tag_vectors"))
            conn.execute(text("ANALYZE categories"))
            
            conn.commit()
            logger.info("向量索引创建完成")
        
    except Exception as e:
        logger.error(f"创建向量索引失败: {e}")
        raise

def verify_migration():
    """验证迁移结果"""
    try:
        postgres_url = f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}"
        postgres_engine = create_engine(postgres_url)
        
        with postgres_engine.connect() as conn:
            # 验证数据数量
            logger.info("验证迁移结果...")
            
            # 检查商品数量
            result = conn.execute(text("SELECT COUNT(*) FROM products")).fetchone()
            logger.info(f"商品数量: {result[0]}")
            
            # 检查有向量的商品数量
            result = conn.execute(text("SELECT COUNT(*) FROM products WHERE product_vector IS NOT NULL")).fetchone()
            logger.info(f"有向量的商品数量: {result[0]}")
            
            # 检查标签数量
            result = conn.execute(text("SELECT COUNT(*) FROM product_tags")).fetchone()
            logger.info(f"商品标签数量: {result[0]}")
            
            # 检查分类数量
            result = conn.execute(text("SELECT COUNT(*) FROM categories")).fetchone()
            logger.info(f"分类数量: {result[0]}")
            
            # 测试向量搜索
            logger.info("测试向量搜索...")
            # 创建一个200维的测试向量
            test_vector = '[' + ','.join(['0.1'] * 200) + ']'
            test_result = conn.execute(text("""
                SELECT id, name, product_vector <=> :test_vector as distance
                FROM products 
                WHERE product_vector IS NOT NULL
                ORDER BY product_vector <=> :test_vector
                LIMIT 5
            """), {'test_vector': test_vector}).fetchall()
            
            logger.info(f"向量搜索测试成功，返回 {len(test_result)} 条结果")
            for row in test_result:
                logger.info(f"商品ID: {row.id}, 名称: {row.name[:50]}, 距离: {row.distance}")
        
    except Exception as e:
        logger.error(f"验证迁移结果失败: {e}")
        raise

def main():
    """主函数"""
    try:
        logger.info("开始数据库迁移...")
        
        # 步骤1: 创建PostgreSQL数据库
        create_postgres_database()
        
        # 步骤2: 安装pgvector扩展
        install_pgvector_extension()
        
        # 步骤3: 迁移数据
        migrate_data()
        
        # 步骤4: 创建向量索引
        create_vector_index()
        
        # 步骤5: 验证迁移结果
        verify_migration()
        
        logger.info("数据库迁移完成！")
        
    except Exception as e:
        logger.error(f"迁移失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
