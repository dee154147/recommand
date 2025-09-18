#!/usr/bin/env python3
"""
个性化推荐API路由 - 修复版本
使用Python层面的向量计算，避免SQL语法问题
"""

from flask import Blueprint, jsonify, request
from app import db
from app.models import User, Product, UserInteraction
from app.services.recommendation_service import RecommendationService
import json
import numpy as np
from sqlalchemy import text

personalized_recommendation_bp = Blueprint('personalized_recommendation', __name__, url_prefix='/api/v1/personalized-recommendations')

@personalized_recommendation_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'data': {
            'status': 'healthy',
            'version': 'fixed'
        }
    })

@personalized_recommendation_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """
    获取用户的个性化推荐商品
    使用Python层面的向量相似度计算
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

        # 检查用户是否有特征向量
        if not user.feature_vector:
            return jsonify({
                'success': False,
                'error': '用户尚未生成特征向量，请先进行商品交互',
                'recommendations': []
            }), 400

        # 获取请求参数
        limit = request.args.get('limit', 12, type=int)
        limit = min(limit, 50)  # 限制最大数量

        # 解析用户特征向量
        user_vector = np.array(json.loads(user.feature_vector))
        
        # 使用Python层面的向量相似度计算
        # 使用稳定的排序策略：只使用主键ID排序，确保结果一致性
        # 避免使用可能重复的字段（如name）导致QuickSort非确定性结果
        products = Product.query.filter(
            Product.embedding.isnot(None)
        ).order_by(
            Product.id  # 只使用主键排序，确保稳定性
        ).limit(min(limit * 10, 1000)).all()
        
        print(f'查询到 {len(products)} 个商品进行相似度计算')
        
        recommendations = []
        for product in products:
            try:
                product_vector = np.array(json.loads(product.embedding))
                # 计算余弦相似度
                similarity = np.dot(user_vector, product_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(product_vector))
                
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
        
        # 按相似度排序并取前limit个
        recommendations.sort(key=lambda x: x[1], reverse=True)
        final_recommendations = [rec[0] for rec in recommendations[:limit]]
        
        # 添加调试日志
        print(f'用户 {user_id} 推荐结果:')
        for i, rec in enumerate(final_recommendations[:3]):
            print(f'  {i+1}. {rec["name"]} (相似度: {rec["similarity_score"]:.4f})')

        return jsonify({
            'success': True,
            'recommendations': final_recommendations,
            'total': len(final_recommendations),
            'user_id': user_id
        })

    except Exception as e:
        print(f'获取推荐失败: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'获取个性化推荐失败: {str(e)}',
            'recommendations': []
        }), 500

@personalized_recommendation_bp.route('/user/<int:user_id>/update-profile', methods=['POST'])
def update_user_profile(user_id):
    """
    更新用户画像（计算用户特征向量）
    """
    try:
        # 获取用户信息
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在'
            }), 404

        # 获取用户的交互记录
        user_interactions = UserInteraction.query.filter_by(user_id=user_id).all()
        
        if not user_interactions:
            return jsonify({
                'success': False,
                'error': '用户暂无交互记录，无法生成特征向量'
            }), 400

        # 计算用户特征向量
        user_feature_vector = calculate_user_preference_vector(user_interactions)
        
        # 更新用户特征向量
        user.feature_vector = json.dumps(user_feature_vector.tolist())
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '用户画像更新成功',
            'user_id': user_id,
            'interaction_count': len(user_interactions)
        })

    except Exception as e:
        print(f'更新用户画像失败: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'更新用户画像失败: {str(e)}'
        }), 500

def calculate_user_preference_vector(user_interactions):
    """
    根据用户交互记录计算用户特征向量
    使用加权平均的方式
    """
    try:
        # 获取所有交互过的商品
        product_ids = [interaction.product_id for interaction in user_interactions]
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        
        if not products:
            return None
        
        # 创建商品ID到向量的映射
        product_vectors = {}
        for product in products:
            if product.embedding:
                try:
                    product_vectors[product.id] = np.array(json.loads(product.embedding))
                except Exception as e:
                    print(f'解析商品 {product.id} 向量失败: {e}')
                    continue
        
        if not product_vectors:
            return None
        
        # 计算加权平均向量
        weighted_sum = None
        total_weight = 0
        
        for interaction in user_interactions:
            if interaction.product_id in product_vectors:
                weight = max(0, interaction.interaction_score or 1.0)  # 只考虑正分
                if weighted_sum is None:
                    weighted_sum = product_vectors[interaction.product_id] * weight
                else:
                    weighted_sum += product_vectors[interaction.product_id] * weight
                total_weight += weight
        
        if total_weight == 0:
            return None
        
        # 归一化
        user_vector = weighted_sum / total_weight
        return user_vector
        
    except Exception as e:
        print(f'计算用户特征向量失败: {e}')
        return None
