#!/usr/bin/env python3
"""
个性化推荐API路由 - 重写版本
完全确定性的推荐算法，确保结果一致性
"""

from flask import Blueprint, jsonify, request
from app import db
from app.models import User, Product, UserInteraction
import json
import numpy as np
from sqlalchemy import text
import hashlib
import time
from typing import List, Dict, Tuple, Optional

personalized_recommendation_bp_v2 = Blueprint('personalized_recommendation_v2', __name__, url_prefix='/api/v2/personalized-recommendations')

class DeterministicRecommendationEngine:
    """
    确定性推荐引擎
    确保相同输入产生相同输出
    """
    
    def __init__(self):
        self.cache = {}
    
    def calculate_user_preference_vector(self, user_id: int) -> Optional[np.ndarray]:
        """
        计算用户偏好向量 - 确定性版本
        """
        try:
            # 获取用户交互历史
            interactions = db.session.query(UserInteraction).filter(
                UserInteraction.user_id == user_id,
                UserInteraction.interaction_score.isnot(None)
            ).order_by(UserInteraction.id).all()  # 使用ID排序确保稳定性
            
            if not interactions:
                return None
            
            # 获取所有相关商品的特征向量
            product_ids = [interaction.product_id for interaction in interactions]
            products = db.session.query(Product).filter(
                Product.id.in_(product_ids),
                Product.embedding.isnot(None)
            ).order_by(Product.id).all()  # 使用ID排序确保稳定性
            
            if not products:
                return None
            
            # 构建商品ID到向量的映射
            product_vectors = {}
            for product in products:
                try:
                    vector = np.array(json.loads(product.embedding))
                    product_vectors[product.id] = vector
                except Exception as e:
                    print(f'解析商品 {product.id} 向量失败: {e}')
                    continue
            
            if not product_vectors:
                return None
            
            # 计算加权平均向量
            weighted_sum = None
            total_weight = 0
            
            for interaction in interactions:
                if interaction.product_id in product_vectors:
                    weight = max(0, interaction.interaction_score or 1.0)
                    vector = product_vectors[interaction.product_id]
                    
                    if weighted_sum is None:
                        weighted_sum = weight * vector
                    else:
                        weighted_sum += weight * vector
                    total_weight += weight
            
            if weighted_sum is None or total_weight == 0:
                return None
            
            # 归一化
            user_vector = weighted_sum / total_weight
            return user_vector
            
        except Exception as e:
            print(f'计算用户偏好向量失败: {e}')
            return None
    
    def get_candidate_products(self, limit: int) -> List[Product]:
        """
        获取候选商品 - 确定性版本
        使用完全稳定的查询策略
        """
        try:
            # 使用完全确定性的查询
            # 1. 先按ID排序获取所有商品
            # 2. 使用Python层面的过滤和排序
            products = db.session.query(Product).filter(
                Product.embedding.isnot(None)
            ).order_by(Product.id).all()
            
            # 为了性能，限制候选商品数量
            max_candidates = min(len(products), limit * 20)  # 最多取limit*20个候选商品
            return products[:max_candidates]
            
        except Exception as e:
            print(f'获取候选商品失败: {e}')
            return []
    
    def calculate_similarities(self, user_vector: np.ndarray, products: List[Product]) -> List[Tuple[Dict, float]]:
        """
        计算相似度 - 确定性版本
        """
        recommendations = []
        
        for product in products:
            try:
                # 解析商品向量
                product_vector = np.array(json.loads(product.embedding))
                
                # 计算余弦相似度
                dot_product = np.dot(user_vector, product_vector)
                norm_user = np.linalg.norm(user_vector)
                norm_product = np.linalg.norm(product_vector)
                
                if norm_user == 0 or norm_product == 0:
                    similarity = 0.0
                else:
                    similarity = dot_product / (norm_user * norm_product)
                
                # 构建商品信息
                product_dict = {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': float(product.price) if product.price else None,
                    'category_id': product.category_id,
                    'image_url': product.image_url,
                    'tags': json.loads(product.tags) if product.tags else [],
                    'similarity_score': float(similarity),
                }
                
                recommendations.append((product_dict, similarity))
                
            except Exception as e:
                print(f'处理商品 {product.id} 时出错: {e}')
                continue
        
        return recommendations
    
    def sort_recommendations(self, recommendations: List[Tuple[Dict, float]], limit: int) -> List[Dict]:
        """
        排序推荐结果 - 确定性版本
        使用稳定的排序策略
        """
        # 使用稳定的排序：先按相似度降序，再按商品ID升序
        # 这确保了相同相似度的商品有稳定的排序
        recommendations.sort(key=lambda x: (-x[1], x[0]['id']))
        
        # 取前limit个
        final_recommendations = [rec[0] for rec in recommendations[:limit]]
        
        return final_recommendations
    
    def get_recommendations(self, user_id: int, limit: int = 24) -> Dict:
        """
        获取推荐结果 - 修改版本
        优先使用已存储的用户特征向量，不重新计算
        """
        print(f'🔍 开始获取推荐，用户ID: {user_id}, 限制: {limit}')
        try:
            # 1. 首先尝试从数据库获取已存储的用户特征向量
            user = User.query.filter_by(id=user_id).first()
            if not user:
                print(f'❌ 用户 {user_id} 不存在')
                return {
                    'success': False,
                    'error': '用户不存在',
                    'recommendations': []
                }
            
            print(f'✅ 用户 {user_id} 存在: {user.username}')
            
            # 2. 检查是否有已存储的特征向量
            if not user.feature_vector:
                print(f'⚠️  用户 {user_id} 没有特征向量')
                return {
                    'success': False,
                    'error': '用户尚未生成特征向量，请先点击"更新用户画像"',
                    'recommendations': []
                }
            
            print(f'✅ 用户 {user_id} 有特征向量，长度: {len(user.feature_vector)}')
            
            # 3. 使用已存储的特征向量，不重新计算
            try:
                user_vector = np.array(json.loads(user.feature_vector))
                print(f'✅ 成功解析用户特征向量，维度: {user_vector.shape}')
            except Exception as e:
                print(f'❌ 解析用户特征向量失败: {e}')
                return {
                    'success': False,
                    'error': '用户特征向量格式错误，请重新更新用户画像',
                    'recommendations': []
                }
            
            # 4. 获取候选商品
            candidate_products = self.get_candidate_products(limit)
            if not candidate_products:
                print(f'❌ 没有候选商品')
                return {
                    'success': False,
                    'error': '没有可推荐的商品',
                    'recommendations': []
                }
            
            print(f'✅ 获取到 {len(candidate_products)} 个候选商品')
            
            # 5. 计算相似度
            recommendations = self.calculate_similarities(user_vector, candidate_products)
            if not recommendations:
                print(f'❌ 相似度计算失败')
                return {
                    'success': False,
                    'error': '相似度计算失败',
                    'recommendations': []
                }
            
            print(f'✅ 计算出 {len(recommendations)} 个推荐结果')
            
            # 6. 排序并返回结果
            final_recommendations = self.sort_recommendations(recommendations, limit)
            
            result = {
                'success': True,
                'recommendations': final_recommendations,
                'total': len(final_recommendations),
                'user_id': user_id,
                'algorithm_version': 'v2_deterministic',
                'feature_vector_source': 'stored'  # 标识使用的是已存储的特征向量
            }
            
            print(f'🎯 返回结果，包含字段: {list(result.keys())}')
            print(f'🎯 feature_vector_source: {result["feature_vector_source"]}')
            
            return result
            
        except Exception as e:
            print(f'❌ 获取推荐失败: {e}')
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'推荐计算失败: {str(e)}',
                'recommendations': []
            }

# 创建推荐引擎实例
recommendation_engine = DeterministicRecommendationEngine()

@personalized_recommendation_bp_v2.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'data': {
            'status': 'healthy',
            'version': 'v2_deterministic',
            'algorithm': 'deterministic_recommendation_engine'
        }
    })

@personalized_recommendation_bp_v2.route('/user/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """
    获取用户的个性化推荐商品 - 重写版本
    使用完全确定性的算法
    """
    try:
        # 获取用户信息
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在',
                'recommendations': []
            }), 404

        # 获取请求参数
        limit = request.args.get('limit', 24, type=int)  # 默认增加到24个
        limit = min(limit, 50)  # 限制最大数量
        
        # 使用新的推荐引擎
        print(f'🚀 开始调用推荐引擎，用户ID: {user_id}, 限制: {limit}')
        result = recommendation_engine.get_recommendations(user_id, limit)
        
        # 添加调试信息
        print(f'🎯 推荐引擎返回结果: {result}')
        print(f'🎯 结果中的字段: {list(result.keys())}')
        print(f'🎯 feature_vector_source: {result.get("feature_vector_source", "NOT_FOUND")}')
        
        if result['success']:
            # 添加调试日志
            recommendations = result['recommendations']
            print(f'用户 {user_id} 推荐结果 (v2):')
            for i, rec in enumerate(recommendations[:3]):
                print(f'  {i+1}. {rec["name"]} (相似度: {rec["similarity_score"]:.4f})')
            print(f'特征向量来源: {result.get("feature_vector_source", "unknown")}')
        
        # 添加测试字段
        result['test_field'] = 'test_value'
        result['debug_info'] = f'API调用时间: {time.time()}'
        
        return jsonify(result)

    except Exception as e:
        print(f'获取推荐失败: {e}')
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}',
            'recommendations': []
        }), 500

@personalized_recommendation_bp_v2.route('/user/<int:user_id>/update-profile', methods=['POST'])
def update_user_profile(user_id):
    """
    更新用户画像 - 重写版本
    """
    try:
        # 获取用户信息
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在'
            }), 404

        # 计算新的用户偏好向量
        user_vector = recommendation_engine.calculate_user_preference_vector(user_id)
        if user_vector is None:
            return jsonify({
                'success': False,
                'error': '无法计算用户偏好向量，请确保有足够的交互数据'
            }), 400

        # 更新用户特征向量
        user.feature_vector = json.dumps(user_vector.tolist())
        db.session.commit()

        # 获取交互记录数量
        interaction_count = db.session.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).count()

        return jsonify({
            'success': True,
            'message': '用户画像更新成功',
            'interaction_count': interaction_count,
            'algorithm_version': 'v2_deterministic'
        })

    except Exception as e:
        print(f'更新用户画像失败: {e}')
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'更新失败: {str(e)}'
        }), 500

@personalized_recommendation_bp_v2.route('/test-consistency/<int:user_id>', methods=['GET'])
def test_consistency(user_id):
    """
    测试推荐结果的一致性
    """
    try:
        limit = request.args.get('limit', 5, type=int)
        iterations = request.args.get('iterations', 3, type=int)
        
        results = []
        for i in range(iterations):
            result = recommendation_engine.get_recommendations(user_id, limit)
            if result['success']:
                recommendations = result['recommendations']
                product_names = [rec['name'] for rec in recommendations]
                similarity_scores = [rec['similarity_score'] for rec in recommendations]
                results.append({
                    'iteration': i + 1,
                    'product_names': product_names,
                    'similarity_scores': similarity_scores
                })
        
        # 检查一致性
        if len(results) > 1:
            first_result = results[0]['product_names']
            is_consistent = all(
                result['product_names'] == first_result 
                for result in results[1:]
            )
        else:
            is_consistent = True
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'iterations': iterations,
            'is_consistent': is_consistent,
            'results': results,
            'algorithm_version': 'v2_deterministic'
        })
        
    except Exception as e:
        print(f'一致性测试失败: {e}')
        return jsonify({
            'success': False,
            'error': f'测试失败: {str(e)}'
        }), 500
