#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL商品图片URL清洗脚本
清洗PostgreSQL数据库中的图片URL，统一截取掉扩展名后面的部分
"""

import psycopg2
import re
import os
from datetime import datetime

def clean_image_url(url):
    """
    清洗图片URL，截取掉扩展名后面的部分
    
    Args:
        url (str): 原始图片URL
        
    Returns:
        str: 清洗后的图片URL
    """
    if not url:
        return url
    
    # 定义图片扩展名模式
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg']
    
    # 构建正则表达式模式 - 匹配扩展名后跟任何非字母数字字符或控制字符的情况
    pattern = r'\.(' + '|'.join(image_extensions) + r')([^\w\-_\./]|[\x00-\x1f\x7f-\x9f])'
    
    # 查找匹配的扩展名和后续内容
    match = re.search(pattern, url.lower())
    
    if match:
        extension = match.group(1)
        # 截取到扩展名结束（包括点号）
        clean_url = url[:match.start(1) + len(extension)]
        return clean_url
    
    return url

def backup_postgresql_database():
    """
    备份PostgreSQL数据库
    
    Returns:
        str: 备份文件路径
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"postgresql_backup_{timestamp}.sql"
    
    # 使用pg_dump备份数据库
    cmd = f"pg_dump -h localhost -U liuzhichao -d recommendation_db > {backup_path}"
    os.system(cmd)
    
    print(f"PostgreSQL数据库已备份到: {backup_path}")
    return backup_path

def analyze_urls(cursor):
    """
    分析URL清洗前后的变化
    
    Args:
        cursor: 数据库游标
    """
    cursor.execute("""
        SELECT id, name, image_url 
        FROM products 
        WHERE image_url IS NOT NULL 
        LIMIT 10
    """)
    
    products = cursor.fetchall()
    
    print("PostgreSQL URL清洗分析:")
    print("=" * 100)
    
    changes_count = 0
    for product in products:
        product_id, name, original_url = product
        cleaned_url = clean_image_url(original_url)
        
        if original_url != cleaned_url:
            changes_count += 1
            print(f"商品ID: {product_id}")
            print(f"商品名: {name[:50]}...")
            print(f"原始URL: {original_url}")
            print(f"清洗后:  {cleaned_url}")
            print("-" * 80)
    
    print(f"需要清洗的URL数量: {changes_count}")
    return changes_count

def clean_all_urls(cursor):
    """
    清洗所有商品图片URL
    
    Args:
        cursor: 数据库游标
    """
    # 获取所有有图片URL的商品
    cursor.execute("SELECT id, image_url FROM products WHERE image_url IS NOT NULL")
    products = cursor.fetchall()
    
    cleaned_count = 0
    error_count = 0
    
    print(f"开始清洗 {len(products)} 个商品的图片URL...")
    
    for product_id, original_url in products:
        try:
            cleaned_url = clean_image_url(original_url)
            
            if original_url != cleaned_url:
                # 更新数据库
                cursor.execute(
                    "UPDATE products SET image_url = %s WHERE id = %s",
                    (cleaned_url, product_id)
                )
                cleaned_count += 1
                
                if cleaned_count % 100 == 0:
                    print(f"已处理 {cleaned_count} 个URL...")
        
        except Exception as e:
            print(f"处理商品ID {product_id} 时出错: {e}")
            error_count += 1
    
    print(f"清洗完成!")
    print(f"成功清洗: {cleaned_count} 个URL")
    print(f"处理错误: {error_count} 个")
    
    return cleaned_count, error_count

def main():
    """主函数"""
    try:
        # 连接PostgreSQL数据库
        conn = psycopg2.connect(
            host="localhost",
            user="liuzhichao",
            database="recommendation_db"
        )
        cursor = conn.cursor()
        
        print("PostgreSQL商品图片URL清洗脚本")
        print("=" * 50)
        
        # 1. 分析URL情况
        print("1. 分析URL清洗情况...")
        changes_count = analyze_urls(cursor)
        
        if changes_count == 0:
            print("所有URL格式都正常，无需清洗!")
            return
        
        # 2. 确认是否继续
        confirm = input(f"\n发现 {changes_count} 个URL需要清洗，是否继续? (y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return
        
        # 3. 备份数据库
        print("\n2. 备份PostgreSQL数据库...")
        backup_path = backup_postgresql_database()
        
        # 4. 执行清洗
        print("\n3. 执行URL清洗...")
        cleaned_count, error_count = clean_all_urls(cursor)
        
        # 5. 提交更改
        if cleaned_count > 0:
            conn.commit()
            print(f"\n4. PostgreSQL数据库已更新，清洗了 {cleaned_count} 个URL")
        else:
            print("\n4. 没有URL需要清洗")
        
        # 6. 验证结果
        print("\n5. 验证清洗结果...")
        verify_changes = analyze_urls(cursor)
        
        if verify_changes == 0:
            print("✅ 所有URL清洗成功!")
        else:
            print(f"⚠️  仍有 {verify_changes} 个URL需要进一步处理")
    
    except Exception as e:
        print(f"执行过程中出错: {e}")
        if 'conn' in locals():
            conn.rollback()
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
