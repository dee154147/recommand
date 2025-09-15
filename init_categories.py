#!/usr/bin/env python3
"""
初始化商品分类数据到数据库
"""

import sys
import os
import json
sys.path.append('backend')

from backend.app import create_app, db
from backend.app.models import Category

def init_categories():
    """初始化商品分类数据"""
    
    print("=" * 80)
    print("初始化商品分类数据")
    print("=" * 80)
    
    app = create_app()
    
    with app.app_context():
        # 检查是否已有分类数据
        existing_categories = Category.query.count()
        print(f"当前数据库中分类数量: {existing_categories}")
        
        if existing_categories > 0:
            print("分类数据已存在，跳过初始化")
            return
        
        # 加载分类数据
        categories_file = os.path.join(os.path.dirname(__file__), 'data/productType.json')
        
        if not os.path.exists(categories_file):
            print(f"分类文件不存在: {categories_file}")
            return
        
        with open(categories_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        categories_data = data['categories']
        print(f"从文件加载分类数量: {len(categories_data)}")
        
        # 创建分类记录
        success_count = 0
        error_count = 0
        
        for cat_data in categories_data:
            try:
                # 检查是否已存在
                existing = Category.query.filter_by(id=cat_data['id']).first()
                if existing:
                    print(f"分类 {cat_data['name']} (ID: {cat_data['id']}) 已存在，跳过")
                    continue
                
                # 创建新分类
                category = Category(
                    id=cat_data['id'],
                    name=cat_data['name'],
                    description=cat_data.get('description', ''),
                    parent_id=None  # 暂时不设置父分类
                )
                
                db.session.add(category)
                success_count += 1
                
                print(f"添加分类: {cat_data['name']} (ID: {cat_data['id']})")
                
            except Exception as e:
                print(f"添加分类失败: {cat_data['name']}, 错误: {e}")
                error_count += 1
        
        # 提交事务
        try:
            db.session.commit()
            print(f"\n分类数据初始化完成:")
            print(f"成功添加: {success_count}")
            print(f"失败数量: {error_count}")
            
            # 验证结果
            total_categories = Category.query.count()
            print(f"数据库中总分类数: {total_categories}")
            
        except Exception as e:
            db.session.rollback()
            print(f"提交事务失败: {e}")

def verify_categories():
    """验证分类数据"""
    
    print("\n" + "=" * 80)
    print("验证分类数据")
    print("=" * 80)
    
    app = create_app()
    
    with app.app_context():
        categories = Category.query.all()
        
        print(f"总分类数: {len(categories)}")
        print("\n分类列表:")
        print("-" * 60)
        
        for category in categories:
            print(f"ID: {category.id:2d} | 名称: {category.name:15s} | 描述: {category.description}")
        
        # 检查热门分类
        print("\n热门分类 (商品数量):")
        print("-" * 60)
        
        # 这里需要查询商品表来统计每个分类的商品数量
        # 由于我们使用的是SQLite，需要直接执行SQL查询
        from sqlalchemy import text
        
        result = db.session.execute(text("""
            SELECT category_id, COUNT(*) as count 
            FROM products 
            WHERE category_id IS NOT NULL 
            GROUP BY category_id 
            ORDER BY count DESC 
            LIMIT 10
        """)).fetchall()
        
        for row in result:
            category_id, count = row
            category = Category.query.filter_by(id=category_id).first()
            category_name = category.name if category else f"未知分类({category_id})"
            print(f"ID: {category_id:2d} | 名称: {category_name:15s} | 商品数: {count:5d}")

if __name__ == "__main__":
    init_categories()
    verify_categories()
