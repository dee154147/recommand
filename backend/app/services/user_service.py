from flask import current_app
from app import db
from app.models import User, UserInteraction, Product
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class UserService:
    """用户服务类"""
    
    def __init__(self):
        pass
    
    def get_user_by_id(self, user_id: int):
        """根据ID获取用户信息"""
        user = User.query.filter_by(id=user_id).first()
        return user.to_dict() if user else None
    
    def get_user_by_user_id(self, user_id: str):
        """根据用户ID获取用户信息"""
        user = User.query.filter_by(user_id=user_id).first()
        return user.to_dict() if user else None
    
    def create_user(self, user_data: dict):
        """创建新用户"""
        user = User(
            user_id=user_data.get('user_id'),
            username=user_data.get('username'),
            email=user_data.get('email'),
            preferences=json.dumps(user_data.get('preferences', {}))
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user.to_dict()
    
    def update_user(self, user_id: int, user_data: dict):
        """更新用户信息"""
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None
        
        for key, value in user_data.items():
            if hasattr(user, key):
                if key == 'preferences':
                    setattr(user, key, json.dumps(value))
                else:
                    setattr(user, key, value)
        
        db.session.commit()
        return user.to_dict()
    
    def get_user_interactions(self, user_id: int, page: int = 1, per_page: int = 20):
        """获取用户交互历史"""
        interactions_query = UserInteraction.query.filter_by(user_id=user_id).order_by(
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
            # 添加商品信息
            if interaction.product:
                interaction_dict['product'] = interaction.product.to_dict()
            interactions.append(interaction_dict)
        
        return {
            'interactions': interactions,
            'pagination': {
                'page': page,
                'pages': pagination.pages,
                'per_page': per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
    
    def record_interaction(self, user_id: int, product_id: int, interaction_type: str, 
                          interaction_score: float = 1.0, session_id: str = None):
        """记录用户交互"""
        interaction = UserInteraction(
            user_id=user_id,
            product_id=product_id,
            interaction_type=interaction_type,
            interaction_score=interaction_score,
            session_id=session_id
        )
        
        db.session.add(interaction)
        db.session.commit()
        
        return interaction.to_dict()
    
    def get_user_preferences(self, user_id: int):
        """获取用户偏好分析"""
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None
        
        # 获取用户交互统计
        interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        
        # 分析交互类型分布
        interaction_types = {}
        for interaction in interactions:
            interaction_type = interaction.interaction_type
            if interaction_type not in interaction_types:
                interaction_types[interaction_type] = 0
            interaction_types[interaction_type] += 1
        
        # 分析偏好分类
        category_preferences = {}
        for interaction in interactions:
            if interaction.product and interaction.product.category:
                category_name = interaction.product.category.name
                if category_name not in category_preferences:
                    category_preferences[category_name] = 0
                category_preferences[category_name] += interaction.interaction_score
        
        # 获取最近活跃度
        recent_interactions = UserInteraction.query.filter(
            UserInteraction.user_id == user_id,
            UserInteraction.created_at >= datetime.utcnow() - timedelta(days=30)
        ).count()
        
        preferences = {
            'interaction_types': interaction_types,
            'category_preferences': category_preferences,
            'recent_activity': recent_interactions,
            'total_interactions': len(interactions),
            'preferences': json.loads(user.preferences) if user.preferences else {}
        }
        
        return preferences
    
    def update_user_preferences(self, user_id: int, preferences: dict):
        """更新用户偏好"""
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None
        
        user.preferences = json.dumps(preferences)
        db.session.commit()
        
        return user.to_dict()
    
    def get_user_statistics(self, user_id: int):
        """获取用户统计信息"""
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return None
        
        # 基础统计
        total_interactions = UserInteraction.query.filter_by(user_id=user_id).count()
        unique_products = db.session.query(UserInteraction.product_id).filter_by(
            user_id=user_id
        ).distinct().count()
        
        # 最近7天活动
        recent_week = datetime.utcnow() - timedelta(days=7)
        recent_interactions = UserInteraction.query.filter(
            UserInteraction.user_id == user_id,
            UserInteraction.created_at >= recent_week
        ).count()
        
        # 最常交互的商品类型
        top_categories = db.session.query(
            Product.category_id,
            db.func.count(UserInteraction.id).label('count')
        ).join(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).group_by(Product.category_id).order_by(
            db.desc('count')
        ).limit(5).all()
        
        statistics = {
            'total_interactions': total_interactions,
            'unique_products_viewed': unique_products,
            'recent_week_activity': recent_interactions,
            'top_categories': [
                {'category_id': cat_id, 'interaction_count': count}
                for cat_id, count in top_categories
            ],
            'account_created': user.created_at.isoformat() if user.created_at else None,
            'last_updated': user.updated_at.isoformat() if user.updated_at else None
        }
        
        return statistics
    
    def delete_user(self, user_id: int):
        """删除用户"""
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return False
        
        # 删除用户相关的交互记录
        UserInteraction.query.filter_by(user_id=user_id).delete()
        
        # 删除用户
        db.session.delete(user)
        db.session.commit()
        
        return True
