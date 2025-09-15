"""
商品搜索API路由
提供模糊匹配和语义搜索功能
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import joinedload
from typing import List, Dict, Optional
import logging
import signal
import time

from ..models import db, Product, ProductTag, Category

logger = logging.getLogger(__name__)

search_bp = Blueprint('search', __name__, url_prefix='/api/v1/search')

@search_bp.route('/products', methods=['GET'])
def search_products():
    """
    商品搜索接口
    支持模糊匹配和语义搜索
    """
    try:
        # 获取查询参数
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'fuzzy')  # fuzzy 或 semantic
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        # category_id = request.args.get('category_id', type=int)  # 去掉分类筛选
        
        if not query:
            return jsonify({'success': False, 'error': "搜索关键词不能为空"}), 400
        
        # 分页参数验证
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # 根据搜索类型选择搜索方法
        start_time = time.time()
        
        if search_type == 'semantic':
            # 语义搜索增加超时时间
            results = semantic_search(query, page, per_page, timeout=30)
        else:
            results = fuzzy_search(query, page, per_page)
        
        # 记录查询时间
        query_time = time.time() - start_time
        logger.info(f"搜索查询耗时: {query_time:.2f}秒, 类型: {search_type}, 关键词: {query}")
        
        return jsonify({'success': True, 'data': results, 'message': "搜索完成"})
        
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        return jsonify({'success': False, 'error': f"搜索失败: {str(e)}"}), 500

def fuzzy_search(query: str, page: int, per_page: int) -> Dict:
    """
    模糊匹配搜索
    在商品名称、标签中搜索关键词
    """
    try:
        # 构建基础查询
        base_query = db.session.query(Product)
        
        # 去掉分类过滤逻辑
        
        # 构建搜索条件
        search_conditions = []
        
        # 在商品名称中搜索
        search_conditions.append(Product.name.like(f'%{query}%'))
        
        # 在商品标签中搜索
        tag_subquery = db.session.query(ProductTag.product_id).filter(
            ProductTag.tag.like(f'%{query}%')
        ).subquery()
        search_conditions.append(Product.id.in_(tag_subquery))
        
        # 组合搜索条件
        base_query = base_query.filter(or_(*search_conditions))
        
        # 按ID排序（模糊匹配的默认排序）
        base_query = base_query.order_by(Product.id)
        
        # 分页查询
        pagination = base_query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 构建返回结果
        products = []
        for product in pagination.items:
            # 获取商品标签
            product_tags = db.session.query(ProductTag).filter(
                ProductTag.product_id == product.id
            ).all()
            
            # 获取分类信息
            category = db.session.query(Category).filter(
                Category.id == product.category_id
            ).first()
            
            product_data = {
                'id': product.id,
                'name': product.name,
                'image_url': product.image_url,
                'category_id': product.category_id,
                'category_name': category.name if category else None,
                'tags': [tag.tag for tag in product_tags],
                'created_at': product.created_at.isoformat() if product.created_at else None
            }
            products.append(product_data)
        
        return {
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next
            },
            'search_info': {
                'query': query,
                'type': 'fuzzy'
            }
        }
        
    except Exception as e:
        logger.error(f"模糊搜索失败: {e}")
        raise

def semantic_search(query: str, page: int, per_page: int, timeout: int = 30) -> Dict:
    """
    语义搜索
    使用pgvector进行全量向量相似度匹配
    """
    try:
        # 使用pgvector推荐服务进行语义搜索
        from app.services.pgvector_recommendation_service import PgVectorRecommendationService
        recommendation_service = PgVectorRecommendationService()
        
        # 使用pgvector进行全量语义搜索
        semantic_results = recommendation_service.semantic_search(query, top_k=per_page * 3)
        
        if not semantic_results:
            # 如果没有语义搜索结果，降级到模糊搜索
            logger.info(f"语义搜索无结果，降级到模糊搜索: {query}")
            return fuzzy_search(query, page, per_page)
        
        # 分页处理
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_results = semantic_results[start_idx:end_idx]
        
        # 构建返回结果
        products = []
        for result in page_results:
            # 获取商品标签
            product_tags = db.session.query(ProductTag).filter(
                ProductTag.product_id == result['id']
            ).all()
            
            # 获取分类信息
            category = db.session.query(Category).filter(
                Category.id == result['category_id']
            ).first()
            
            product_data = {
                'id': result['id'],
                'name': result['name'],
                'image_url': result['image_url'],
                'price': float(result['price']) if result['price'] else 0.0,
                'category_name': category.name if category else '未分类',
                'category_id': result['category_id'],
                'tags': result['tags'],
                'similarity': result['similarity'],  # 添加相似度分数
                'distance': result['distance']  # 添加距离分数
            }
            products.append(product_data)
        
        # 计算分页信息
        total_results = len(semantic_results)
        total_pages = (total_results + per_page - 1) // per_page
        
        return {
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_results,
                'pages': total_pages,
                'has_prev': page > 1,
                'has_next': page < total_pages
            },
            'search_info': {
                'query': query,
                'type': 'semantic',
                'total_searched': total_results  # 添加搜索总数信息
            }
        }
        
    except Exception as e:
        logger.error(f"语义搜索失败: {e}")
        raise

def calculate_match_score(query_words: List[str], product_tags) -> float:
    """
    计算商品与查询词的匹配分数
    """
    if not query_words or not product_tags:
        return 0.0
    
    score = 0.0
    tag_texts = [tag.tag for tag in product_tags]
    
    for word in query_words:
        if len(word) <= 1:
            continue
        
        # 完全匹配
        if word in tag_texts:
            score += 1.0
        else:
            # 部分匹配
            for tag in tag_texts:
                if word in tag or tag in word:
                    score += 0.5
                    break
    
    return score

@search_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    获取所有商品分类
    """
    try:
        categories = Category.query.all()
        
        category_list = []
        for category in categories:
            category_list.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'product_count': db.session.query(Product).filter(
                    Product.category_id == category.id
                ).count()
            })
        
        return jsonify({'success': True, 'data': category_list, 'message': "获取分类成功"})
        
    except Exception as e:
        logger.error(f"获取分类失败: {e}")
        return jsonify({'success': False, 'error': f"获取分类失败: {str(e)}"}), 500

@search_bp.route('/suggestions', methods=['GET'])
def get_search_suggestions():
    """
    获取搜索建议
    基于热门标签和商品名称
    """
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 2:
            return jsonify({'success': True, 'data': [], 'message': "搜索建议为空"})
        
        suggestions = []
        
        # 从标签中获取建议
        tag_suggestions = db.session.query(ProductTag.tag).filter(
            ProductTag.tag.like(f'%{query}%')
        ).distinct().limit(10).all()
        
        for tag_tuple in tag_suggestions:
            suggestions.append({
                'text': tag_tuple[0],
                'type': 'tag'
            })
        
        # 从商品名称中获取建议
        product_suggestions = db.session.query(Product.name).filter(
            Product.name.like(f'%{query}%')
        ).distinct().limit(5).all()
        
        for name_tuple in product_suggestions:
            suggestions.append({
                'text': name_tuple[0],
                'type': 'product'
            })
        
        return jsonify({'success': True, 'data': suggestions, 'message': "获取搜索建议成功"})
        
    except Exception as e:
        logger.error(f"获取搜索建议失败: {e}")
        return jsonify({'success': False, 'error': f"获取搜索建议失败: {str(e)}"}), 500
