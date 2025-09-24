#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逐步调试API调用过程
"""

import sys
sys.path.append('backend')
from app import create_app, db
from app.api.product_management_routes import _find_similar_by_tag_vectors, _find_similar_by_vector_similarity
from app.services.recommendation_service import RecommendationService
from app.services.similar_product_service import SimilarProductService
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_step_by_step():
    """逐步调试API调用过程"""
    print("=== 逐步调试API调用过程 ===")
    
    app = create_app()
    with app.app_context():
        # 模拟API调用逻辑
        tags = ['男装', '商务']
        limit = 3
        description = ""  # 没有描述
        
        print(f"输入参数: tags={tags}, limit={limit}, description='{description}'")
        
        # 步骤1: 基于标签向量相似度搜索
        print("\n=== 步骤1: 基于标签向量相似度搜索 ===")
        try:
            similar_products = _find_similar_by_tag_vectors(tags, limit)
            print(f"✅ 标签向量相似度搜索成功，结果数量: {len(similar_products)}")
            for i, product in enumerate(similar_products):
                print(f"  {i+1}. ID: {product['id']}, 匹配类型: {product['match_type']}, 相似度: {product['similarity']}")
        except Exception as e:
            print(f"❌ 标签向量相似度搜索异常: {str(e)}")
            similar_products = []
        
        # 步骤2: 检查是否需要第二种方法
        print(f"\n=== 步骤2: 检查是否需要第二种方法 ===")
        print(f"当前结果数量: {len(similar_products)}, 需要数量: {limit}")
        print(f"是否有描述: {bool(description)}")
        need_second_method = len(similar_products) < limit and description
        print(f"是否需要第二种方法: {need_second_method}")
        
        if need_second_method:
            print("\n=== 执行第二种方法: 基于商品描述向量相似度 ===")
            try:
                vector_similarities = _find_similar_by_vector_similarity(tags, description, limit - len(similar_products))
                print(f"✅ 商品描述向量相似度搜索成功，结果数量: {len(vector_similarities)}")
                similar_products.extend(vector_similarities)
            except Exception as e:
                print(f"❌ 商品描述向量相似度搜索异常: {str(e)}")
        else:
            print("跳过第二种方法")
        
        # 步骤3: 去重并限制数量
        print(f"\n=== 步骤3: 去重并限制数量 ===")
        print(f"去重前数量: {len(similar_products)}")
        
        seen_ids = set()
        unique_products = []
        for product in similar_products:
            if product['id'] not in seen_ids:
                seen_ids.add(product['id'])
                unique_products.append(product)
                if len(unique_products) >= limit:
                    break
        
        print(f"去重后数量: {len(unique_products)}")
        
        # 最终结果
        print(f"\n=== 最终结果 ===")
        for i, product in enumerate(unique_products):
            print(f"  {i+1}. ID: {product['id']}, 匹配类型: {product['match_type']}, 相似度: {product['similarity']}")
        
        return unique_products

if __name__ == "__main__":
    result = debug_step_by_step()
    print(f"\n🎯 调试完成，最终返回 {len(result)} 个商品")
