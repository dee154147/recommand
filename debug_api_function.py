#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试API函数调用
"""

import sys
sys.path.append('backend')
from app import create_app, db
from app.api.product_management_routes import _find_similar_by_tag_vectors, _find_similar_by_tag_keywords
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api_functions():
    """测试API函数调用"""
    print("=== 调试API函数调用 ===")
    
    app = create_app()
    with app.app_context():
        # 测试标签
        tags = ['男装', '商务']
        limit = 3
        
        print(f"测试标签: {tags}, 限制: {limit}")
        
        # 测试向量匹配函数
        print("\n--- 测试向量匹配函数 ---")
        try:
            vector_results = _find_similar_by_tag_vectors(tags, limit)
            print(f"向量匹配结果数量: {len(vector_results)}")
            for i, product in enumerate(vector_results):
                print(f"  {i+1}. ID: {product['id']}, 名称: {product['name'][:50]}...")
                print(f"     匹配类型: {product['match_type']}, 相似度: {product['similarity']}")
        except Exception as e:
            print(f"向量匹配函数异常: {str(e)}")
            import traceback
            print(f"详细错误信息: {traceback.format_exc()}")
        
        # 测试关键词匹配函数
        print("\n--- 测试关键词匹配函数 ---")
        try:
            keyword_results = _find_similar_by_tag_keywords(tags, limit)
            print(f"关键词匹配结果数量: {len(keyword_results)}")
            for i, product in enumerate(keyword_results):
                print(f"  {i+1}. ID: {product['id']}, 名称: {product['name'][:50]}...")
                print(f"     匹配类型: {product['match_type']}, 相似度: {product['similarity']}")
        except Exception as e:
            print(f"关键词匹配函数异常: {str(e)}")
            import traceback
            print(f"详细错误信息: {traceback.format_exc()}")

if __name__ == "__main__":
    test_api_functions()
