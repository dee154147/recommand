"""
用户管理API路由
提供用户注册、登录、信息管理等功能
"""

from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.models import User, UserInteraction
from app import db
from sqlalchemy import text
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

# 创建蓝图
user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')

@user_bp.route('/register', methods=['POST'])
def register_user():
    """用户注册"""
    try:
        data = request.get_json()
        
        # 验证必需参数
        required_fields = ['username', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False, 
                    'error': f'缺少必需参数: {field}'
                }), 400
        
        username = data['username']
        email = data['email']
        preferences = data.get('preferences', {})
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({
                'success': False, 
                'error': '用户名已存在'
            }), 409
        
        # 检查邮箱是否已存在
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({
                'success': False, 
                'error': '邮箱已存在'
            }), 409
        
        # 生成用户ID
        user_id = str(uuid.uuid4())
        
        # 创建用户数据
        user_data = {
            'user_id': user_id,
            'username': username,
            'email': email,
            'preferences': preferences
        }
        
        # 创建用户
        user_service = UserService()
        user = user_service.create_user(user_data)
        
        return jsonify({
            'success': True,
            'data': user,
            'message': '用户注册成功'
        }), 201
        
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'用户注册失败: {str(e)}'
        }), 500

@user_bp.route('/login', methods=['POST'])
def login_user():
    """用户登录"""
    try:
        data = request.get_json()
        
        # 验证必需参数
        required_fields = ['username']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False, 
                    'error': f'缺少必需参数: {field}'
                }), 400
        
        username = data['username']
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        # 返回用户信息
        user_data = user.to_dict()
        
        return jsonify({
            'success': True,
            'data': user_data,
            'message': '登录成功'
        })
        
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'用户登录失败: {str(e)}'
        }), 500

@user_bp.route('/<string:username>', methods=['GET'])
def get_user_by_username(username):
    """根据用户名获取用户信息"""
    try:
        # 检查是否是数字ID
        if username.isdigit():
            # 如果是数字，按ID查询
            user_service = UserService()
            user_data = user_service.get_user_by_id(int(username))
            if not user_data:
                return jsonify({
                    'success': False, 
                    'error': '用户不存在'
                }), 404
            return jsonify({
                'success': True,
                'data': user_data,
                'message': '获取用户信息成功'
            })
        else:
            # 如果是字符串，按用户名查询
            user = User.query.filter_by(username=username).first()
            if not user:
                return jsonify({
                    'success': False, 
                    'error': '用户不存在'
                }), 404
            
            return jsonify({
                'success': True,
                'data': user.to_dict(),
                'message': '获取用户信息成功'
            })
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取用户信息失败: {str(e)}'
        }), 500

@user_bp.route('/id/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """根据用户ID获取用户信息"""
    try:
        user_service = UserService()
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': user,
            'message': '获取用户信息成功'
        })
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取用户信息失败: {str(e)}'
        }), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户信息"""
    try:
        data = request.get_json()
        
        # 验证用户是否存在
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        # 检查用户名是否重复
        if 'username' in data:
            existing_user = User.query.filter(
                User.username == data['username'],
                User.id != user_id
            ).first()
            if existing_user:
                return jsonify({
                    'success': False, 
                    'error': '用户名已存在'
                }), 409
        
        # 检查邮箱是否重复
        if 'email' in data:
            existing_email = User.query.filter(
                User.email == data['email'],
                User.id != user_id
            ).first()
            if existing_email:
                return jsonify({
                    'success': False, 
                    'error': '邮箱已存在'
                }), 409
        
        # 更新用户信息
        user_service = UserService()
        result = user_service.update_user(user_id, data)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': '更新用户信息成功'
        })
        
    except Exception as e:
        logger.error(f"更新用户信息失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'更新用户信息失败: {str(e)}'
        }), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    try:
        user_service = UserService()
        result = user_service.delete_user(user_id)
        
        if not result:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '删除用户成功'
        })
        
    except Exception as e:
        logger.error(f"删除用户失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'删除用户失败: {str(e)}'
        }), 500

@user_bp.route('/<int:user_id>/dashboard', methods=['GET'])
def get_user_dashboard(user_id):
    """获取用户仪表板数据"""
    try:
        user_service = UserService()
        
        # 获取用户基本信息
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        # 获取用户统计信息
        statistics = user_service.get_user_statistics(user_id)
        
        # 获取用户偏好分析
        preferences = user_service.get_user_preferences(user_id)
        
        # 获取最近的交互记录
        recent_interactions = user_service.get_user_interactions(
            user_id=user_id,
            page=1,
            per_page=10
        )
        
        dashboard_data = {
            'user': user,
            'statistics': statistics,
            'preferences': preferences,
            'recent_interactions': recent_interactions['interactions'][:5]  # 只返回最近5条
        }
        
        return jsonify({
            'success': True,
            'data': dashboard_data,
            'message': '获取用户仪表板数据成功'
        })
        
    except Exception as e:
        logger.error(f"获取用户仪表板数据失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取用户仪表板数据失败: {str(e)}'
        }), 500

@user_bp.route('/<int:user_id>/activity', methods=['GET'])
def get_user_activity(user_id):
    """获取用户活动记录"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        days = request.args.get('days', 30, type=int)
        
        # 验证分页参数
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # 验证用户是否存在
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({
                'success': False, 
                'error': '用户不存在'
            }), 404
        
        # 计算时间范围
        since_time = datetime.utcnow() - timedelta(days=days)
        
        # 查询用户活动记录
        activities_query = UserInteraction.query.filter(
            UserInteraction.user_id == user_id,
            UserInteraction.created_at >= since_time
        ).order_by(UserInteraction.created_at.desc())
        
        pagination = activities_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        activities = []
        for interaction in pagination.items:
            activity_dict = interaction.to_dict()
            # 添加商品信息
            if interaction.product:
                activity_dict['product'] = {
                    'id': interaction.product.id,
                    'name': interaction.product.name,
                    'category_id': interaction.product.category_id,
                    'category_name': interaction.product.category.name if interaction.product.category else None
                }
            activities.append(activity_dict)
        
        result = {
            'activities': activities,
            'pagination': {
                'page': page,
                'pages': pagination.pages,
                'per_page': per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'time_range': {
                'days': days,
                'since': since_time.isoformat()
            }
        }
        
        return jsonify({
            'success': True,
            'data': result,
            'message': '获取用户活动记录成功'
        })
        
    except Exception as e:
        logger.error(f"获取用户活动记录失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'获取用户活动记录失败: {str(e)}'
        }), 500

@user_bp.route('/search', methods=['GET'])
def search_users():
    """搜索用户"""
    try:
        query = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        if not query:
            return jsonify({
                'success': False, 
                'error': '搜索关键词不能为空'
            }), 400
        
        # 验证分页参数
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # 搜索用户
        users_query = User.query.filter(
            db.or_(
                User.username.like(f'%{query}%'),
                User.email.like(f'%{query}%')
            )
        ).order_by(User.created_at.desc())
        
        pagination = users_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        users = []
        for user in pagination.items:
            user_dict = user.to_dict()
            # 添加用户统计信息
            user_dict['total_interactions'] = UserInteraction.query.filter_by(
                user_id=user.id
            ).count()
            users.append(user_dict)
        
        result = {
            'users': users,
            'pagination': {
                'page': page,
                'pages': pagination.pages,
                'per_page': per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'search_info': {
                'query': query,
                'count': len(users)
            }
        }
        
        return jsonify({
            'success': True,
            'data': result,
            'message': '搜索用户成功'
        })
        
    except Exception as e:
        logger.error(f"搜索用户失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'搜索用户失败: {str(e)}'
        }), 500

@user_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    try:
        # 检查数据库连接
        db.session.execute(text('SELECT 1'))
        
        # 检查用户总数
        total_users = User.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'status': 'healthy',
                'database': 'connected',
                'total_users': total_users
            }
        })
        
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'健康检查失败: {str(e)}'
        }), 500
