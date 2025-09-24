#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试API调用过程
"""

import sys
sys.path.append('backend')
import requests
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api_call():
    """测试API调用过程"""
    print("=== 调试API调用过程 ===")
    
    # 测试数据
    test_data = {
        "tags": ["男装", "商务"],
        "limit": 3
    }
    
    print(f"测试数据: {test_data}")
    
    # 发送API请求
    try:
        response = requests.post(
            "http://localhost:5004/api/v1/product-management/find-similar-by-tags",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=30
        )
        
        print(f"HTTP状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应成功: {result['success']}")
            
            if result['success']:
                data = result['data']
                print(f"查询标签: {data['query_tags']}")
                print(f"相似商品数量: {data['count']}")
                
                for i, product in enumerate(data['similar_products']):
                    print(f"  {i+1}. ID: {product['id']}, 名称: {product['name'][:50]}...")
                    print(f"     匹配类型: {product['match_type']}, 相似度: {product['similarity']}")
                    print(f"     标签: {product['tags']}")
            else:
                print(f"API调用失败: {result.get('error', '未知错误')}")
        else:
            print(f"HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {str(e)}")
    except Exception as e:
        print(f"其他异常: {str(e)}")

if __name__ == "__main__":
    test_api_call()
