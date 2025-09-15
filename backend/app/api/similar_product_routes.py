"""
相似商品查询API路由
提供相似商品查询、批量查询、相似度计算等接口
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging
from typing import List, Dict

from ..services.similar_product_service import SimilarProductService

logger = logging.getLogger(__name__)

# 创建蓝图
similar_product_bp = Blueprint('similar_product', __name__, url_prefix='/api/v1/similar-products')

# 初始化服务
similar_product_service = SimilarProductService()

@similar_product_bp.route('/<int:product_id>', methods=['GET'])
@cross_origin()
def get_similar_products(product_id: int):
    """
    获取相似商品列表
    
    Query Parameters:
        limit: 返回数量限制 (默认: 10, 最大: 50)
        threshold: 相似度阈值 (默认: 0.0, 范围: 0.0-1.0)
        exclude_self: 是否排除自身 (默认: true)
    """
    try:
        # 获取查询参数
        limit = request.args.get('limit', 10, type=int)
        threshold = request.args.get('threshold', 0.0, type=float)
        exclude_self = request.args.get('exclude_self', 'true').lower() == 'true'
        
        # 参数验证
        if limit <= 0 or limit > 50:
            return jsonify({
                'success': False,
                'error': 'limit参数必须在1-50之间'
            }), 400
        
        if threshold < 0.0 or threshold > 1.0:
            return jsonify({
                'success': False,
                'error': 'threshold参数必须在0.0-1.0之间'
            }), 400
        
        # 查询相似商品
        similar_products = similar_product_service.find_similar_products(
            product_id=product_id,
            limit=limit,
            threshold=threshold,
            exclude_self=exclude_self
        )
        
        return jsonify({
            'success': True,
            'data': {
                'product_id': product_id,
                'similar_products': similar_products,
                'count': len(similar_products),
                'limit': limit,
                'threshold': threshold
            },
            'message': f'找到 {len(similar_products)} 个相似商品'
        })
        
    except Exception as e:
        logger.error(f"获取相似商品失败: {e}")
        return jsonify({
            'success': False,
            'error': f'获取相似商品失败: {str(e)}'
        }), 500

@similar_product_bp.route('/batch', methods=['POST'])
@cross_origin()
def batch_get_similar_products():
    """
    批量获取相似商品
    
    Request Body:
        {
            "product_ids": [1, 2, 3],
            "limit": 10,
            "threshold": 0.0
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '请求体不能为空'
            }), 400
        
        product_ids = data.get('product_ids', [])
        limit = data.get('limit', 10)
        threshold = data.get('threshold', 0.0)
        
        # 参数验证
        if not isinstance(product_ids, list) or len(product_ids) == 0:
            return jsonify({
                'success': False,
                'error': 'product_ids必须是非空数组'
            }), 400
        
        if len(product_ids) > 20:
            return jsonify({
                'success': False,
                'error': '批量查询最多支持20个商品'
            }), 400
        
        if limit <= 0 or limit > 50:
            return jsonify({
                'success': False,
                'error': 'limit参数必须在1-50之间'
            }), 400
        
        if threshold < 0.0 or threshold > 1.0:
            return jsonify({
                'success': False,
                'error': 'threshold参数必须在0.0-1.0之间'
            }), 400
        
        # 批量查询相似商品
        results = similar_product_service.batch_find_similar_products(
            product_ids=product_ids,
            limit=limit,
            threshold=threshold
        )
        
        return jsonify({
            'success': True,
            'data': {
                'results': results,
                'total_queries': len(product_ids),
                'successful_queries': len([r for r in results.values() if r])
            },
            'message': f'批量查询完成，处理了 {len(product_ids)} 个商品'
        })
        
    except Exception as e:
        logger.error(f"批量获取相似商品失败: {e}")
        return jsonify({
            'success': False,
            'error': f'批量获取相似商品失败: {str(e)}'
        }), 500

@similar_product_bp.route('/similarity', methods=['POST'])
@cross_origin()
def calculate_similarity():
    """
    计算两个商品之间的相似度
    
    Request Body:
        {
            "product_id1": 1,
            "product_id2": 2
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '请求体不能为空'
            }), 400
        
        product_id1 = data.get('product_id1')
        product_id2 = data.get('product_id2')
        
        # 参数验证
        if product_id1 is None or product_id2 is None:
            return jsonify({
                'success': False,
                'error': 'product_id1和product_id2不能为空'
            }), 400
        
        if not isinstance(product_id1, int) or not isinstance(product_id2, int):
            return jsonify({
                'success': False,
                'error': 'product_id1和product_id2必须是整数'
            }), 400
        
        if product_id1 == product_id2:
            return jsonify({
                'success': False,
                'error': '不能计算商品与自身的相似度'
            }), 400
        
        # 计算相似度
        similarity = similar_product_service.calculate_similarity(product_id1, product_id2)
        
        if similarity is None:
            return jsonify({
                'success': False,
                'error': '无法计算相似度，请检查商品是否存在且有向量'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'product_id1': product_id1,
                'product_id2': product_id2,
                'similarity': similarity
            },
            'message': f'商品 {product_id1} 和 {product_id2} 的相似度为 {similarity}'
        })
        
    except Exception as e:
        logger.error(f"计算相似度失败: {e}")
        return jsonify({
            'success': False,
            'error': f'计算相似度失败: {str(e)}'
        }), 500

@similar_product_bp.route('/stats', methods=['GET'])
@cross_origin()
def get_similarity_stats():
    """获取相似度计算统计信息"""
    try:
        stats = similar_product_service.get_similarity_stats()
        
        return jsonify({
            'success': True,
            'data': stats,
            'message': '获取统计信息成功'
        })
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return jsonify({
            'success': False,
            'error': f'获取统计信息失败: {str(e)}'
        }), 500

@similar_product_bp.route('/cache/clear', methods=['POST'])
@cross_origin()
def clear_cache():
    """清空向量缓存"""
    try:
        similar_product_service.clear_cache()
        
        return jsonify({
            'success': True,
            'message': '缓存清空成功'
        })
        
    except Exception as e:
        logger.error(f"清空缓存失败: {e}")
        return jsonify({
            'success': False,
            'error': f'清空缓存失败: {str(e)}'
        }), 500
