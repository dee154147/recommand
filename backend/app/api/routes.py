from flask import jsonify, request
from app.api import bp
from app.services.recommendation_service import RecommendationService
from app.services.product_service import ProductService
from app.services.user_service import UserService

@bp.route('/products', methods=['GET'])
def get_products():
    """获取商品列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category', None)
        search = request.args.get('search', None)
        
        product_service = ProductService()
        products = product_service.get_products(
            page=page, 
            per_page=per_page, 
            category=category, 
            search=search
        )
        
        return jsonify({
            'status': 'success',
            'data': products,
            'message': 'Products retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """获取单个商品详情"""
    try:
        product_service = ProductService()
        product = product_service.get_product_by_id(product_id)
        
        if not product:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            }), 404
            
        return jsonify({
            'status': 'success',
            'data': product,
            'message': 'Product retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """获取推荐商品"""
    try:
        product_id = request.args.get('product_id', type=int)
        user_id = request.args.get('user_id', type=int)
        limit = request.args.get('limit', 10, type=int)
        
        if not product_id and not user_id:
            return jsonify({
                'status': 'error',
                'message': 'Either product_id or user_id is required'
            }), 400
        
        recommendation_service = RecommendationService()
        
        if product_id:
            recommendations = recommendation_service.get_similar_products(
                product_id=product_id, 
                limit=limit
            )
        else:
            recommendations = recommendation_service.get_user_recommendations(
                user_id=user_id, 
                limit=limit
            )
        
        return jsonify({
            'status': 'success',
            'data': recommendations,
            'message': 'Recommendations retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/categories', methods=['GET'])
def get_categories():
    """获取商品分类"""
    try:
        product_service = ProductService()
        categories = product_service.get_categories()
        
        return jsonify({
            'status': 'success',
            'data': categories,
            'message': 'Categories retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/search', methods=['GET'])
def search_products():
    """搜索商品"""
    try:
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Search query is required'
            }), 400
        
        product_service = ProductService()
        results = product_service.search_products(
            query=query,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'status': 'success',
            'data': results,
            'message': 'Search completed successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
