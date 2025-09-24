# -*- coding: utf-8 -*-
"""
商品管理模块API路由
用于处理商品标签生成后的相似商品检索功能
"""

from flask import Blueprint, request, jsonify
import logging
import json
import numpy as np
from typing import List, Dict, Optional
from app.services.similar_product_service import SimilarProductService
from app.services.recommendation_service import RecommendationService
from app import db
from app.models import Product

logger = logging.getLogger(__name__)

# 创建蓝图
product_management_bp = Blueprint('product_management', __name__, url_prefix='/api/v1/product-management')

# 初始化服务
similar_product_service = SimilarProductService()
recommendation_service = RecommendationService()

@product_management_bp.route('/find-similar-by-tags', methods=['POST'])
def find_similar_by_tags():
    """
    基于标签查找相似商品
    
    Request Body:
    {
        "tags": ["标签1", "标签2", "标签3", "标签4", "标签5"],
        "limit": 10,
        "description": "商品描述（可选）"
    }
    
    Response:
    {
        "success": true,
        "data": {
            "similar_products": [...],
            "query_tags": [...],
            "count": 10
        }
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据不能为空"
            }), 400
        
        # 验证必需参数
        tags = data.get('tags', [])
        if not tags or not isinstance(tags, list):
            return jsonify({
                "success": False,
                "error": "标签列表不能为空"
            }), 400
        
        limit = data.get('limit', 10)
        description = data.get('description', '')
        
        # 参数验证
        if limit <= 0 or limit > 50:
            return jsonify({
                "success": False,
                "error": "limit参数必须在1-50之间"
            }), 400
        
        logger.info(f"基于标签查找相似商品，标签: {tags}, 限制: {limit}")
        
        # 方法1：基于标签向量相似度搜索
        logger.info(f"开始执行标签向量相似度搜索")
        try:
            similar_products = _find_similar_by_tag_vectors(tags, limit)
            logger.info(f"标签向量相似度搜索结果数量: {len(similar_products)}")
        except Exception as e:
            logger.error(f"标签向量相似度搜索异常: {str(e)}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            similar_products = []
        
        # 如果结果不足，使用方法2：基于商品描述向量相似度
        if len(similar_products) < limit and description:
            vector_similarities = _find_similar_by_vector_similarity(tags, description, limit - len(similar_products))
            similar_products.extend(vector_similarities)
        
        # 去重并限制数量
        seen_ids = set()
        unique_products = []
        for product in similar_products:
            if product['id'] not in seen_ids:
                seen_ids.add(product['id'])
                unique_products.append(product)
                if len(unique_products) >= limit:
                    break
        
        logger.info(f"找到 {len(unique_products)} 个相似商品")
        
        return jsonify({
            "success": True,
            "data": {
                "similar_products": unique_products,
                "query_tags": tags,
                "count": len(unique_products),
                "description": description
            }
        })
        
    except Exception as e:
        logger.error(f"基于标签查找相似商品失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"查找相似商品失败: {str(e)}"
        }), 500

def _find_similar_by_tag_vectors(tags: List[str], limit: int) -> List[Dict]:
    """
    基于标签向量搜索相似商品
    
    Args:
        tags: 标签列表
        limit: 返回数量限制
        
    Returns:
        相似商品列表
    """
    try:
        # 确保推荐服务已初始化
        if not hasattr(recommendation_service, 'word_vectors') or not recommendation_service.word_vectors:
            logger.warning("词向量模型未加载，降级到关键词搜索")
            return _find_similar_by_tag_keywords(tags, limit)
        
        # 获取标签向量
        tag_vectors = []
        for tag in tags:
            vector = recommendation_service.get_word_vector(tag)
            if vector is not None:
                tag_vectors.append(vector)
                logger.info(f"标签 '{tag}' 向量获取成功，维度: {len(vector)}")
            else:
                logger.warning(f"标签 '{tag}' 向量获取失败")
        
        if not tag_vectors:
            logger.warning("无法获取任何标签向量，降级到关键词搜索")
            return _find_similar_by_tag_keywords(tags, limit)
        
        # 计算标签向量的平均值作为查询向量
        import numpy as np
        query_vector = np.mean(tag_vectors, axis=0)
        logger.info(f"成功计算查询向量，维度: {len(query_vector)}")
        
        # 转换为PostgreSQL vector格式
        vector_str = '[' + ','.join(map(str, query_vector)) + ']'
        
        # 使用pgvector进行向量相似度搜索
        from sqlalchemy import text
        
        sql_query = text("""
            SELECT 
                id, 
                name, 
                description, 
                price, 
                category_id, 
                image_url, 
                tags,
                product_vector <=> :query_vector as distance,
                1 - (product_vector <=> :query_vector) as similarity
            FROM products 
            WHERE product_vector IS NOT NULL
            ORDER BY product_vector <=> :query_vector
            LIMIT :limit
        """)
        
        result = db.session.execute(sql_query, {
            'query_vector': vector_str,
            'limit': limit
        })
        
        products = []
        for row in result.fetchall():
            # 解析标签
            import json
            try:
                product_tags = json.loads(row.tags) if row.tags else []
            except (json.JSONDecodeError, TypeError):
                product_tags = []
            
            products.append({
                'id': row.id,
                'name': row.name,
                'description': row.description,
                'price': float(row.price) if row.price else None,
                'category_id': row.category_id,
                'image_url': _clean_image_url(row.image_url),
                'similarity': round(float(row.similarity), 4),
                'tags': product_tags,
                'match_type': 'vector_similarity'
            })
        
        logger.info(f"基于标签向量搜索找到 {len(products)} 个相似商品")
        return products
        
    except Exception as e:
        logger.error(f"基于标签向量搜索失败: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        # 降级到关键词搜索
        return _find_similar_by_tag_keywords(tags, limit)

def _find_similar_by_tag_keywords(tags: List[str], limit: int) -> List[Dict]:
    """
    基于标签关键词搜索相似商品
    
    Args:
        tags: 标签列表
        limit: 返回数量限制
        
    Returns:
        相似商品列表
    """
    try:
        # 使用SQLAlchemy查询，避免SQL注入
        from sqlalchemy import text
        
        # 构建搜索条件：使用PostgreSQL的数组操作符
        search_conditions = []
        params = {}
        
        for i, tag in enumerate(tags):
            # 使用LIKE操作符来检查文本字段中是否包含标签
            search_conditions.append(f"tags LIKE :tag_{i}")
            params[f'tag_{i}'] = f'%{tag}%'
        
        # 使用OR连接所有条件
        where_clause = " OR ".join(search_conditions)
        
        # 构建SQL查询
        sql_query = text(f"""
            SELECT 
                id, 
                name, 
                description, 
                price, 
                category_id, 
                image_url, 
                tags
            FROM products 
            WHERE {where_clause}
            ORDER BY 
                id
            LIMIT :limit
        """)
        
        params['limit'] = limit * 2  # 获取更多结果用于后续处理
        logger.info(f"执行SQL查询: {sql_query}")
        logger.info(f"查询参数: {params}")
        result = db.session.execute(sql_query, params)
        
        products = []
        for row in result.fetchall():
            # 计算标签匹配度
            import json
            try:
                product_tags = json.loads(row.tags) if row.tags else []
            except (json.JSONDecodeError, TypeError):
                product_tags = []
            matched_tags = sum(1 for tag in tags if tag in product_tags)
            similarity = min(0.95, 0.5 + (matched_tags / len(tags)) * 0.4)  # 0.5-0.95范围
            
            products.append({
                'id': row.id,
                'name': row.name,
                'description': row.description,
                'price': float(row.price) if row.price else None,
                'category_id': row.category_id,
                'image_url': _clean_image_url(row.image_url),
                'similarity': round(similarity, 4),
                'tags': product_tags,
                'match_type': 'tag_keyword'
            })
        
        return products
        
    except Exception as e:
        logger.error(f"基于标签关键词搜索失败: {str(e)}")
        return []

def _find_similar_by_vector_similarity(tags: List[str], description: str, limit: int) -> List[Dict]:
    """
    基于向量相似度搜索相似商品
    
    Args:
        tags: 标签列表
        description: 商品描述
        limit: 返回数量限制
        
    Returns:
        相似商品列表
    """
    try:
        # 生成查询向量
        query_vector = _generate_query_vector_from_tags(tags, description)
        if query_vector is None:
            logger.warning("无法生成查询向量")
            return []
        
        # 使用pgvector进行向量相似度搜索
        from sqlalchemy import text
        
        # 将查询向量转换为PostgreSQL数组格式
        vector_str = '[' + ','.join(map(str, query_vector)) + ']'
        
        sql_query = text("""
            SELECT 
                id, 
                name, 
                description, 
                price, 
                category_id, 
                image_url, 
                tags,
                product_vector <=> :query_vector as distance,
                1 - (product_vector <=> :query_vector) as similarity
            FROM products 
            WHERE product_vector IS NOT NULL
            ORDER BY product_vector <=> :query_vector
            LIMIT :limit
        """)
        
        result = db.session.execute(sql_query, {
            'query_vector': vector_str,
            'limit': limit
        })
        
        products = []
        for row in result.fetchall():
            products.append({
                'id': row.id,
                'name': row.name,
                'description': row.description,
                'price': float(row.price) if row.price else None,
                'category_id': row.category_id,
                'image_url': _clean_image_url(row.image_url),
                'similarity': round(float(row.similarity), 4),
                'tags': json.loads(row.tags) if row.tags else [],
                'match_type': 'vector_similarity'
            })
        
        return products
        
    except Exception as e:
        logger.error(f"基于向量相似度搜索失败: {str(e)}")
        return []

def _generate_query_vector_from_tags(tags: List[str], description: str = '') -> Optional[np.ndarray]:
    """
    基于标签生成查询向量
    
    Args:
        tags: 标签列表
        description: 商品描述
        
    Returns:
        查询向量
    """
    try:
        # 尝试使用推荐服务的词向量功能
        if hasattr(recommendation_service, 'word_vectors') and recommendation_service.word_vectors:
            # 合并标签和描述
            text_content = ' '.join(tags) + ' ' + description
            
            # 使用推荐服务生成向量
            vector = recommendation_service.generate_text_vector(text_content)
            if vector is not None:
                return vector
        
        # 如果无法生成向量，返回None
        logger.warning("无法生成查询向量，词向量模型可能未加载")
        return None
        
    except Exception as e:
        logger.error(f"生成查询向量失败: {str(e)}")
        return None

def _clean_image_url(image_url: str) -> str:
    """清理图片URL中的特殊字符"""
    if not image_url:
        return ""
    
    # 去掉文件扩展名之后的所有字符串
    if '.jpg' in image_url:
        return image_url.split('.jpg')[0] + '.jpg'
    elif '.jpeg' in image_url:
        return image_url.split('.jpeg')[0] + '.jpeg'
    elif '.png' in image_url:
        return image_url.split('.png')[0] + '.png'
    elif '.gif' in image_url:
        return image_url.split('.gif')[0] + '.gif'
    elif '.webp' in image_url:
        return image_url.split('.webp')[0] + '.webp'
    elif '.bmp' in image_url:
        return image_url.split('.bmp')[0] + '.bmp'
    
    return image_url

@product_management_bp.route('/test-vector-generation', methods=['POST'])
def test_vector_generation():
    """
    测试向量生成功能
    
    Request Body:
    {
        "tags": ["标签1", "标签2", "标签3"],
        "description": "商品描述"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据不能为空"
            }), 400
        
        tags = data.get('tags', [])
        description = data.get('description', '')
        
        # 测试向量生成
        query_vector = _generate_query_vector_from_tags(tags, description)
        
        if query_vector is not None:
            return jsonify({
                "success": True,
                "data": {
                    "vector_generated": True,
                    "vector_dimension": len(query_vector),
                    "vector_preview": query_vector[:10].tolist(),  # 只显示前10维
                    "tags": tags,
                    "description": description
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": "无法生成向量，词向量模型可能未加载"
            }), 500
            
    except Exception as e:
        logger.error(f"测试向量生成失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"测试向量生成失败: {str(e)}"
        }), 500

@product_management_bp.errorhandler(400)
def handle_bad_request(error):
    """处理400错误"""
    return jsonify({
        "success": False,
        "error": "请求参数错误",
        "details": str(error)
    }), 400

@product_management_bp.errorhandler(500)
def handle_internal_error(error):
    """处理500错误"""
    logger.error(f"商品管理API内部错误: {str(error)}")
    return jsonify({
        "success": False,
        "error": "服务器内部错误",
        "details": "请稍后重试"
    }), 500
