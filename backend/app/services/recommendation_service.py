from flask import current_app
from app import db
from app.models import Product, User, UserInteraction, RecommendationCache
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    """推荐服务类 - 基础架构框架"""
    
    def __init__(self):
        self.cache_expiry_hours = 24  # 缓存过期时间（小时）
        self.default_limit = 10  # 默认推荐数量
    
    def get_similar_products(self, product_id: int, limit: int = None) -> List[Dict]:
        """获取相似商品推荐 - 待实现"""
        if limit is None:
            limit = self.default_limit
        
        logger.info(f"Getting similar products for product_id: {product_id}, limit: {limit}")
        
        try:
            # 检查缓存
            cache_key = f"similar_products_{product_id}_{limit}"
            cached_result = self._get_cached_recommendations(cache_key)
            if cached_result:
                logger.info(f"Returning cached recommendations for product {product_id}")
                return cached_result
            
            # 获取目标商品
            target_product = Product.query.filter_by(id=product_id).first()
            if not target_product:
                logger.warning(f"Product {product_id} not found")
                return []
            
            # TODO: 实现基于内容的推荐算法
            # 这里返回模拟数据，实际实现时会被替换
            similar_products = self._get_mock_similar_products(target_product, limit)
            
            # 缓存结果
            self._cache_recommendations(cache_key, 'similar_products', str(product_id), similar_products)
            
            return similar_products
            
        except Exception as e:
            logger.error(f"Error getting similar products for {product_id}: {str(e)}")
            return []
    
    def get_user_recommendations(self, user_id: int, limit: int = None) -> List[Dict]:
        """获取用户个性化推荐 - 待实现"""
        if limit is None:
            limit = self.default_limit
        
        logger.info(f"Getting user recommendations for user_id: {user_id}, limit: {limit}")
        
        try:
            # 检查缓存
            cache_key = f"user_recommendations_{user_id}_{limit}"
            cached_result = self._get_cached_recommendations(cache_key)
            if cached_result:
                logger.info(f"Returning cached recommendations for user {user_id}")
                return cached_result
            
            # 获取用户信息
            user = User.query.filter_by(id=user_id).first()
            if not user:
                logger.warning(f"User {user_id} not found")
                return []
            
            # TODO: 实现基于用户偏好的推荐算法
            # 这里返回模拟数据，实际实现时会被替换
            recommendations = self._get_mock_user_recommendations(user, limit)
            
            # 缓存结果
            self._cache_recommendations(cache_key, 'user_recommendations', str(user_id), recommendations)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting user recommendations for {user_id}: {str(e)}")
            return []
    
    def _get_mock_similar_products(self, target_product: Product, limit: int) -> List[Dict]:
        """模拟相似商品推荐 - 用于测试和演示"""
        try:
            # 获取同分类的其他商品
            similar_products = Product.query.filter(
                Product.category_id == target_product.category_id,
                Product.id != target_product.id
            ).limit(limit).all()
            
            # 转换为字典格式
            recommendations = []
            for product in similar_products:
                product_dict = product.to_dict()
                product_dict['similarity_score'] = 0.85  # 模拟相似度分数
                product_dict['recommendation_reason'] = 'same_category'
                recommendations.append(product_dict)
            
            logger.info(f"Returning {len(recommendations)} mock similar products")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting mock similar products: {str(e)}")
            return []
    
    def _get_mock_user_recommendations(self, user: User, limit: int) -> List[Dict]:
        """模拟用户推荐 - 用于测试和演示"""
        try:
            # 获取用户交互历史
            user_interactions = UserInteraction.query.filter_by(user_id=user.id).all()
            
            if not user_interactions:
                # 如果没有交互历史，返回热门商品
                return self._get_mock_popular_products(limit)
            
            # 获取用户交互过的商品分类
            interacted_product_ids = [interaction.product_id for interaction in user_interactions]
            user_products = Product.query.filter(Product.id.in_(interacted_product_ids)).all()
            
            # 获取用户偏好的分类
            preferred_categories = set()
            for product in user_products:
                if product.category_id:
                    preferred_categories.add(product.category_id)
            
            # 获取同分类的其他商品
            recommendations = []
            for category_id in preferred_categories:
                category_products = Product.query.filter(
                    Product.category_id == category_id,
                    ~Product.id.in_(interacted_product_ids)
                ).limit(limit // len(preferred_categories) + 1).all()
                
                for product in category_products:
                    product_dict = product.to_dict()
                    product_dict['similarity_score'] = 0.75  # 模拟相似度分数
                    product_dict['recommendation_reason'] = 'user_preference'
                    recommendations.append(product_dict)
            
            # 限制返回数量
            recommendations = recommendations[:limit]
            
            logger.info(f"Returning {len(recommendations)} mock user recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting mock user recommendations: {str(e)}")
            return self._get_mock_popular_products(limit)
    
    def _get_mock_popular_products(self, limit: int) -> List[Dict]:
        """模拟热门商品推荐"""
        try:
            # 获取一些商品作为热门商品
            popular_products = Product.query.limit(limit).all()
            
            recommendations = []
            for product in popular_products:
                product_dict = product.to_dict()
                product_dict['similarity_score'] = 0.90  # 模拟相似度分数
                product_dict['recommendation_reason'] = 'popular'
                recommendations.append(product_dict)
            
            logger.info(f"Returning {len(recommendations)} mock popular products")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting mock popular products: {str(e)}")
            return []
    
    def _get_cached_recommendations(self, cache_key: str) -> Optional[List[Dict]]:
        """获取缓存的推荐结果"""
        try:
            cache_entry = RecommendationCache.query.filter_by(cache_key=cache_key).first()
            if cache_entry and cache_entry.expires_at > datetime.utcnow():
                return json.loads(cache_entry.recommendations)
            elif cache_entry:
                # 删除过期缓存
                db.session.delete(cache_entry)
                db.session.commit()
        except Exception as e:
            logger.error(f"Error getting cached recommendations: {str(e)}")
        return None
    
    def _cache_recommendations(self, cache_key: str, cache_type: str, target_id: str, recommendations: List[Dict]):
        """缓存推荐结果"""
        try:
            expires_at = datetime.utcnow() + timedelta(hours=self.cache_expiry_hours)
            
            cache_entry = RecommendationCache(
                cache_key=cache_key,
                cache_type=cache_type,
                target_id=target_id,
                recommendations=json.dumps(recommendations),
                expires_at=expires_at
            )
            
            # 删除旧的缓存
            old_cache = RecommendationCache.query.filter_by(cache_key=cache_key).first()
            if old_cache:
                db.session.delete(old_cache)
            
            db.session.add(cache_entry)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error caching recommendations: {str(e)}")
    
    def clear_cache(self, cache_type: str = None):
        """清除缓存"""
        try:
            if cache_type:
                RecommendationCache.query.filter_by(cache_type=cache_type).delete()
            else:
                RecommendationCache.query.delete()
            db.session.commit()
            logger.info(f"Cleared cache: {cache_type or 'all'}")
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
    
    def get_recommendation_stats(self) -> Dict[str, any]:
        """获取推荐系统统计信息"""
        try:
            total_products = Product.query.count()
            total_users = User.query.count()
            total_interactions = UserInteraction.query.count()
            cache_entries = RecommendationCache.query.count()
            
            return {
                'total_products': total_products,
                'total_users': total_users,
                'total_interactions': total_interactions,
                'cache_entries': cache_entries,
                'service_status': 'running',
                'algorithm_status': 'mock_mode'  # 标识当前为模拟模式
            }
        except Exception as e:
            logger.error(f"Error getting recommendation stats: {str(e)}")
            return {
                'error': str(e),
                'service_status': 'error'
            }