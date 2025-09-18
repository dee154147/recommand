"""
用户交互API路由
提供用户交互记录、查询、统计等功能
"""

from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.models import UserInteraction, Product, Category
from app import db
from sqlalchemy import text
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# 创建蓝图
user_interaction_bp = Blueprint('user_interaction', __name__, url_prefix='/api/v1/user-interactions')

@user_interaction_bp.route('/record', methods=['POST'])
def record_interaction():
    """记录用户交互"""
    try:
        data = request.get_json()
        
        # 验证必需参数
        required_fields = ['user_id', 'product_id', 'interaction_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False, 
                    'error': f'缺少必需参数: {field}'
                }), 400
        
        user_id = data['user_id']
        product_id = data['product_id']
        interaction_type = data['interaction_type']
        interaction_score = data.get('interaction_score', 1.0)
        session_id = data.get('session_id')
        
        # 验证交互类型
        valid_types = ['click', 'view', 'favorite', 'purchase', 'dislike']
        if interaction_type not in valid_types:
            return jsonify({
                'success': False, 
                'error': f'无效的交互类型: {interaction_type}'
            }), 400
        
        # 验证用户和商品是否存在
        from app.models import User, Product
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return jsonify({
                'success': False, 
                'error': '商品不存在'
            }), 404
        
        # 记录交互
        user_service = UserService()
        interaction = user_service.record_interaction(
            user_id=user_id,
            product_id=product_id,
            interaction_type=interaction_type,
            interaction_score=interaction_score,
            session_id=session_id
        )
        
        return jsonify({
            'success': True,
            'data': interaction,
            'message': '交互记录成功'
        })
        
    except Exception as e:
        logger.error(f"记录用户交互失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'记录交互失败: {str(e)}'
        }), 500

@user_interaction_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_interactions(user_id):
    """获取用户交互历史"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        interaction_type = request.args.get('type', None)
        
        # 验证分页参数
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        user_service = UserService()
        result = user_service.get_user_interactions(
            user_id=user_id,
            page=page,
            per_page=per_page
        )
        
        # 如果指定了交互类型，进行过滤
        if interaction_type:
            filtered_interactions = [
                interaction for interaction in result['interactions']
                if interaction['interaction_type'] == interaction_type
            ]
            result['interactions'] = filtered_interactions
            result['pagination']['total'] = len(filtered_interactions)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': '获取用户交互历史成功'
        })
        
    except Exception as e:
        logger.error(f"获取用户交互历史失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取交互历史失败: {str(e)}'
        }), 500

@user_interaction_bp.route('/user/<int:user_id>/statistics', methods=['GET'])
def get_user_interaction_statistics(user_id):
    """获取用户交互统计"""
    try:
        user_service = UserService()
        statistics = user_service.get_user_statistics(user_id)
        
        if not statistics:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': statistics,
            'message': '获取用户统计成功'
        })
        
    except Exception as e:
        logger.error(f"获取用户统计失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取统计失败: {str(e)}'
        }), 500

@user_interaction_bp.route('/user/<int:user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    """获取用户偏好分析"""
    try:
        user_service = UserService()
        preferences = user_service.get_user_preferences(user_id)
        
        if not preferences:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': preferences,
            'message': '获取用户偏好成功'
        })
        
    except Exception as e:
        logger.error(f"获取用户偏好失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取偏好失败: {str(e)}'
        }), 500

@user_interaction_bp.route('/user/<int:user_id>/preferences', methods=['PUT'])
def update_user_preferences(user_id):
    """更新用户偏好"""
    try:
        data = request.get_json()
        preferences = data.get('preferences', {})
        
        user_service = UserService()
        result = user_service.update_user_preferences(user_id, preferences)
        
        if not result:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': result,
            'message': '更新用户偏好成功'
        })
        
    except Exception as e:
        logger.error(f"更新用户偏好失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'更新偏好失败: {str(e)}'
        }), 500

@user_interaction_bp.route('/product/<int:product_id>/interactions', methods=['GET'])
def get_product_interactions(product_id):
    """获取商品交互统计"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 验证分页参数
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # 查询商品交互记录
        interactions_query = UserInteraction.query.filter_by(product_id=product_id).order_by(
            UserInteraction.created_at.desc()
        )
        
        pagination = interactions_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        interactions = []
        for interaction in pagination.items:
            interaction_dict = interaction.to_dict()
            # 添加用户信息
            if interaction.user:
                interaction_dict['user'] = {
                    'id': interaction.user.id,
                    'user_id': interaction.user.user_id,
                    'username': interaction.user.username
                }
            interactions.append(interaction_dict)
        
        # 计算商品交互统计
        total_interactions = UserInteraction.query.filter_by(product_id=product_id).count()
        unique_users = db.session.query(UserInteraction.user_id).filter_by(
            product_id=product_id
        ).distinct().count()
        
        # 按交互类型统计
        interaction_stats = db.session.query(
            UserInteraction.interaction_type,
            db.func.count(UserInteraction.id).label('count'),
            db.func.avg(UserInteraction.interaction_score).label('avg_score')
        ).filter_by(product_id=product_id).group_by(
            UserInteraction.interaction_type
        ).all()
        
        stats = {
            'total_interactions': total_interactions,
            'unique_users': unique_users,
            'interaction_types': [
                {
                    'type': stat.interaction_type,
                    'count': stat.count,
                    'avg_score': float(stat.avg_score) if stat.avg_score else 0
                }
                for stat in interaction_stats
            ]
        }
        
        result = {
            'interactions': interactions,
            'statistics': stats,
            'pagination': {
                'page': page,
                'pages': pagination.pages,
                'per_page': per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
        
        return jsonify({
            'success': True,
            'data': result,
            'message': '获取商品交互统计成功'
        })
        
    except Exception as e:
        logger.error(f"获取商品交互统计失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取商品交互统计失败: {str(e)}'
        }), 500

@user_interaction_bp.route('/recent', methods=['GET'])
def get_recent_interactions():
    """获取最近的交互记录"""
    try:
        limit = request.args.get('limit', 50, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        # 限制查询数量
        if limit > 200:
            limit = 200
        
        # 计算时间范围
        since_time = datetime.utcnow() - timedelta(hours=hours)
        
        # 查询最近的交互记录
        interactions = UserInteraction.query.filter(
            UserInteraction.created_at >= since_time
        ).order_by(
            UserInteraction.created_at.desc()
        ).limit(limit).all()
        
        result = []
        for interaction in interactions:
            interaction_dict = interaction.to_dict()
            # 添加用户信息
            if interaction.user:
                interaction_dict['user'] = {
                    'id': interaction.user.id,
                    'user_id': interaction.user.user_id,
                    'username': interaction.user.username
                }
            # 添加商品信息
            if interaction.product:
                interaction_dict['product'] = {
                    'id': interaction.product.id,
                    'name': interaction.product.name,
                    'category_id': interaction.product.category_id,
                    'category_name': interaction.product.category.name if interaction.product.category else None
                }
            result.append(interaction_dict)
        
        return jsonify({
            'success': True,
            'data': {
                'interactions': result,
                'count': len(result),
                'since': since_time.isoformat(),
                'hours': hours
            },
            'message': '获取最近交互记录成功'
        })
        
    except Exception as e:
        logger.error(f"获取最近交互记录失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取最近交互记录失败: {str(e)}'
        }), 500

@user_interaction_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    try:
        # 检查数据库连接
        db.session.execute(text('SELECT 1'))
        
        # 检查最近是否有交互记录
        recent_count = UserInteraction.query.filter(
            UserInteraction.created_at >= datetime.utcnow() - timedelta(hours=1)
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'status': 'healthy',
                'database': 'connected',
                'recent_interactions': recent_count
            }
        })
        
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'健康检查失败: {str(e)}'
        }), 500
