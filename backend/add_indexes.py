#!/usr/bin/env python3
"""
添加数据库索引以优化查询性能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import create_app, db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_database_indexes():
    """添加数据库索引"""
    
    app = create_app()
    
    with app.app_context():
        logger.info("开始添加数据库索引...")
        
        # 定义需要添加的索引
        indexes = [
            # 商品表索引
            {
                'name': 'idx_products_category_id',
                'table': 'products',
                'columns': 'category_id',
                'description': '商品分类索引'
            },
            {
                'name': 'idx_products_name',
                'table': 'products',
                'columns': 'name',
                'description': '商品名称索引'
            },
            {
                'name': 'idx_products_created_at',
                'table': 'products',
                'columns': 'created_at',
                'description': '商品创建时间索引'
            },
            {
                'name': 'idx_products_embedding',
                'table': 'products',
                'columns': 'embedding',
                'description': '商品向量索引'
            },
            
            # 商品标签表索引
            {
                'name': 'idx_product_tags_product_id',
                'table': 'product_tags',
                'columns': 'product_id',
                'description': '商品标签商品ID索引'
            },
            {
                'name': 'idx_product_tags_tag',
                'table': 'product_tags',
                'columns': 'tag',
                'description': '商品标签索引'
            },
            
            # 标签向量表索引
            {
                'name': 'idx_tag_vectors_tag',
                'table': 'tag_vectors',
                'columns': 'tag',
                'description': '标签向量索引'
            },
            
            # 分类表索引
            {
                'name': 'idx_categories_name',
                'table': 'categories',
                'columns': 'name',
                'description': '分类名称索引'
            }
        ]
        
        success_count = 0
        error_count = 0
        
        for index_info in indexes:
            try:
                # 检查索引是否已存在
                check_sql = text(f"""
                    SELECT name FROM sqlite_master 
                    WHERE type='index' AND name='{index_info['name']}'
                """)
                
                result = db.session.execute(check_sql).fetchone()
                
                if result:
                    logger.info(f"索引 {index_info['name']} 已存在，跳过")
                    continue
                
                # 创建索引
                create_sql = text(f"""
                    CREATE INDEX {index_info['name']} 
                    ON {index_info['table']} ({index_info['columns']})
                """)
                
                db.session.execute(create_sql)
                db.session.commit()
                
                logger.info(f"成功创建索引: {index_info['name']} - {index_info['description']}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"创建索引失败: {index_info['name']}, 错误: {e}")
                db.session.rollback()
                error_count += 1
        
        logger.info(f"索引创建完成: 成功 {success_count}, 失败 {error_count}")
        
        # 分析表以更新统计信息
        try:
            logger.info("更新数据库统计信息...")
            tables = ['products', 'product_tags', 'tag_vectors', 'categories']
            
            for table in tables:
                analyze_sql = text(f"ANALYZE {table}")
                db.session.execute(analyze_sql)
            
            db.session.commit()
            logger.info("统计信息更新完成")
            
        except Exception as e:
            logger.error(f"更新统计信息失败: {e}")
            db.session.rollback()

def verify_indexes():
    """验证索引创建情况"""
    
    app = create_app()
    
    with app.app_context():
        logger.info("验证索引创建情况...")
        
        # 查询所有索引
        sql = text("""
            SELECT name, tbl_name, sql 
            FROM sqlite_master 
            WHERE type='index' AND name NOT LIKE 'sqlite_%'
            ORDER BY tbl_name, name
        """)
        
        result = db.session.execute(sql).fetchall()
        
        logger.info(f"当前数据库索引数量: {len(result)}")
        
        for row in result:
            logger.info(f"表: {row.tbl_name}, 索引: {row.name}")

if __name__ == "__main__":
    add_database_indexes()
    verify_indexes()
