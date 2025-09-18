#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加用户特征向量字段的数据库迁移脚本
"""

import psycopg2
from datetime import datetime

def add_user_feature_vector_fields():
    """添加用户特征向量相关字段"""
    try:
        # 连接PostgreSQL数据库
        conn = psycopg2.connect(
            host="localhost",
            user="liuzhichao",
            database="recommendation_db"
        )
        cursor = conn.cursor()
        
        print("开始添加用户特征向量字段...")
        
        # 检查字段是否已存在
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name IN ('feature_vector', 'vector_updated_at')
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # 添加feature_vector字段
        if 'feature_vector' not in existing_columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN feature_vector TEXT
            """)
            print("✅ 添加feature_vector字段")
        else:
            print("⚠️  feature_vector字段已存在")
        
        # 添加vector_updated_at字段
        if 'vector_updated_at' not in existing_columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN vector_updated_at TIMESTAMP
            """)
            print("✅ 添加vector_updated_at字段")
        else:
            print("⚠️  vector_updated_at字段已存在")
        
        # 提交更改
        conn.commit()
        print("🎉 用户特征向量字段添加完成!")
        
    except Exception as e:
        print(f"❌ 添加字段时出错: {e}")
        if 'conn' in locals():
            conn.rollback()
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    add_user_feature_vector_fields()
