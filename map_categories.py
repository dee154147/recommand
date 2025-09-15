#!/usr/bin/env python3
"""
商品分类映射脚本
将原始的商品分类ID映射到我们定义的分类
"""

import sqlite3
import json
import os

# 数据库路径
DB_PATH = 'backend/instance/recommendation_dev.db'

# 分类映射关系（基于商品名称分析）
CATEGORY_MAPPING = {
    # 原始ID -> 新分类ID
    84: 1,   # 汽车用品类 - 车品世家、汽车钥匙包等
    71: 2,   # 手表类 - 卡西欧、手表等
    35: 3,   # 图书类 - 华图、公务员考试等
    39: 4,   # 数码产品类 - 酷派手机、手机套等
    67: 5,   # 厨具餐具类 - 苏氏陶瓷、餐具等
    10: 6,   # 包包类 - 各种包包
    5: 7,    # 童装类 - 儿童相关产品
    16: 8,   # 鞋子类 - 鞋类产品
    60: 9,   # 文具办公类 - 办公用品
    25: 10,  # 打火机类 - ZIPPO等
    48: 11,  # 数码配件类 - 数码配件
    # 其他映射...
    1: 12,   # 女装类
    2: 13,   # 男装类
    3: 14,   # 运动户外类
    4: 15,   # 家居用品类
    6: 16,   # 鞋子类
    7: 17,   # 配饰类
    8: 18,   # 美妆护肤类
    9: 19,   # 食品饮料类
    11: 20,  # 母婴用品类
    12: 21,  # 宠物用品类
    13: 22,  # 汽车用品类
    14: 23,  # 珠宝首饰类
    15: 24,  # 乐器类
    17: 25,  # 其他类
}

def map_categories():
    """执行分类映射"""
    if not os.path.exists(DB_PATH):
        print(f"数据库文件不存在: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查分类表是否存在
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        
        if category_count == 0:
            print("分类表为空，请先初始化分类数据")
            return False
        
        print(f"开始映射分类，共找到 {len(CATEGORY_MAPPING)} 个映射关系")
        
        # 执行映射
        updated_count = 0
        for old_id, new_id in CATEGORY_MAPPING.items():
            # 检查新分类ID是否存在
            cursor.execute("SELECT id FROM categories WHERE id = ?", (new_id,))
            if not cursor.fetchone():
                print(f"警告: 分类ID {new_id} 不存在，跳过映射 {old_id} -> {new_id}")
                continue
            
            # 更新商品分类
            cursor.execute("""
                UPDATE products 
                SET category_id = ? 
                WHERE category_id = ?
            """, (new_id, old_id))
            
            affected_rows = cursor.rowcount
            if affected_rows > 0:
                updated_count += affected_rows
                print(f"映射 {old_id} -> {new_id}: 更新了 {affected_rows} 个商品")
        
        # 提交更改
        conn.commit()
        
        print(f"\n映射完成！总共更新了 {updated_count} 个商品的分类")
        
        # 验证结果
        cursor.execute("""
            SELECT 
                c.id,
                c.name,
                COUNT(p.id) as product_count
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id, c.name
            ORDER BY product_count DESC
        """)
        
        print("\n分类统计:")
        for row in cursor.fetchall():
            print(f"ID {row[0]}: {row[1]} - {row[2]} 个商品")
        
        return True
        
    except Exception as e:
        print(f"映射失败: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    map_categories()
