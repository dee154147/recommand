#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟真实API调用过程
"""

import sys
sys.path.append('backend')
from app import create_app
from flask import request
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_real_api():
    """测试真实API调用过程"""
    print("=== 测试真实API调用过程 ===")
    
    app = create_app()
    
    with app.test_client() as client:
        # 模拟POST请求
        test_data = {
            "tags": ["男装", "商务"],
            "limit": 3
        }
        
        print(f"发送数据: {test_data}")
        
        response = client.post(
            '/api/v1/product-management/find-similar-by-tags',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        print(f"HTTP状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.get_json()
            print(f"响应成功: {result['success']}")
            
            if result['success']:
                data = result['data']
                print(f"查询标签: {data['query_tags']}")
                print(f"相似商品数量: {data['count']}")
                
                for i, product in enumerate(data['similar_products']):
                    print(f"  {i+1}. ID: {product['id']}, 名称: {product['name'][:50]}...")
                    print(f"     匹配类型: {product['match_type']}, 相似度: {product['similarity']}")
            else:
                print(f"API调用失败: {result.get('error', '未知错误')}")
        else:
            print(f"HTTP错误: {response.status_code}")
            print(f"响应内容: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    test_real_api()
