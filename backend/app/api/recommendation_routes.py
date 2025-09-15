"""
推荐算法API路由
提供向量计算、相似商品推荐等接口
"""

from flask import Blueprint, request, jsonify
from app.services.recommendation_service import RecommendationService
from app.utils.response_utils import success_response, error_response
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
recommendation_bp = Blueprint('recommendation', __name__, url_prefix='/api/v1/recommendation')

@recommendation_bp.route('/precompute-tag-vectors', methods=['POST'])
def precompute_tag_vectors():
    """预计算标签向量"""
    try:
        service = RecommendationService()
        result = service.precompute_tag_vectors()
        
        if 'error' in result:
            return error_response(result['error'], 500)
        
        return success_response({
            'message': '标签向量预计算完成',
            'success_count': result['success'],
            'failed_count': result['failed']
        })
        
    except Exception as e:
        logger.error(f"预计算标签向量失败: {str(e)}")
        return error_response(f"预计算标签向量失败: {str(e)}", 500)

@recommendation_bp.route('/precompute-product-vectors', methods=['POST'])
def precompute_product_vectors():
    """预计算商品特征向量"""
    try:
        service = RecommendationService()
        result = service.precompute_product_vectors()
        
        if 'error' in result:
            return error_response(result['error'], 500)
        
        return success_response({
            'message': '商品向量预计算完成',
            'success_count': result['success'],
            'failed_count': result['failed']
        })
        
    except Exception as e:
        logger.error(f"预计算商品向量失败: {str(e)}")
        return error_response(f"预计算商品向量失败: {str(e)}", 500)

@recommendation_bp.route('/similar-products/<int:product_id>', methods=['GET'])
def get_similar_products(product_id):
    """获取相似商品"""
    try:
        top_k = request.args.get('top_k', 10, type=int)
        if top_k > 50:
            top_k = 50
        
        service = RecommendationService()
        similar_products = service.find_similar_products(product_id, top_k)
        
        return success_response({
            'product_id': product_id,
            'similar_products': similar_products,
            'count': len(similar_products)
        })
        
    except Exception as e:
        logger.error(f"获取相似商品失败: {str(e)}")
        return error_response(f"获取相似商品失败: {str(e)}", 500)

@recommendation_bp.route('/semantic-search', methods=['GET'])
def semantic_search():
    """语义搜索"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return error_response("查询参数不能为空", 400)
        
        top_k = request.args.get('top_k', 20, type=int)
        if top_k > 100:
            top_k = 100
        
        service = RecommendationService()
        results = service.semantic_search(query, top_k)
        
        return success_response({
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"语义搜索失败: {str(e)}")
        return error_response(f"语义搜索失败: {str(e)}", 500)

@recommendation_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """获取推荐算法统计信息"""
    try:
        service = RecommendationService()
        stats = service.get_statistics()
        
        return success_response(stats)
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {str(e)}")
        return error_response(f"获取统计信息失败: {str(e)}", 500)

@recommendation_bp.route('/test-word-vector', methods=['GET'])
def test_word_vector():
    """测试词向量功能"""
    try:
        word = request.args.get('word', '手机').strip()
        if not word:
            return error_response("词参数不能为空", 400)
        
        service = RecommendationService()
        
        # 测试词向量加载
        if not service.load_word_vectors():
            return error_response("词向量模型加载失败", 500)
        
        # 获取词向量
        vector = service.get_word_vector(word)
        if vector is None:
            return error_response(f"词 '{word}' 不在词向量模型中", 404)
        
        # 计算标签向量
        tag_vector = service.calculate_tag_vector(word)
        
        return success_response({
            'word': word,
            'word_vector_dim': len(vector),
            'word_vector_sample': vector[:10].tolist(),  # 只返回前10个维度
            'tag_vector_dim': len(tag_vector) if tag_vector is not None else 0,
            'tag_vector_sample': tag_vector[:10].tolist() if tag_vector is not None else None
        })
        
    except Exception as e:
        logger.error(f"测试词向量失败: {str(e)}")
        return error_response(f"测试词向量失败: {str(e)}", 500)

@recommendation_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    try:
        service = RecommendationService()
        model_loaded = service.load_word_vectors()
        
        return success_response({
            'status': 'healthy',
            'model_loaded': model_loaded,
            'model_path': service.model_path
        })
        
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return error_response(f"健康检查失败: {str(e)}", 500)
