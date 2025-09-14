from flask import render_template, jsonify, request
from app.main import bp
from app.services.recommendation_service import RecommendationService

@bp.route('/')
@bp.route('/index')
def index():
    """主页"""
    return jsonify({
        'message': '推荐系统API服务运行正常',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'api_products': '/api/products',
            'api_categories': '/api/categories',
            'api_recommendations': '/api/recommendations',
            'api_search': '/api/search'
        }
    })

@bp.route('/health')
def health():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': 'Recommendation System API is running'
    })

@bp.route('/api/test')
def test_api():
    """API测试接口"""
    return jsonify({
        'message': 'API is working',
        'version': '1.0.0'
    })
