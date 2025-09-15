#!/usr/bin/env python3
"""
基于PostgreSQL + pgvector的推荐服务
去除随机采样，实现全量商品向量搜索
"""

import json
import logging
import numpy as np
from typing import List, Dict, Optional
from sqlalchemy import text
from app import db
from app.models import Product, Category, ProductTag
from app.utils.text_processing import TextProcessor
from app.utils.hybrid_text_processing import HybridVectorTextProcessor

logger = logging.getLogger(__name__)

class PgVectorRecommendationService:
    """基于pgvector的推荐服务"""
    
    def __init__(self):
        """初始化推荐服务"""
        self.text_processor = TextProcessor()
        self.word_vectors = self.load_word_vectors()
        self.hybrid_processor = None
        
        # 如果词向量加载成功，初始化混合分词器
        if self.word_vectors:
            self.hybrid_processor = HybridVectorTextProcessor(self.word_vectors)
            logger.info("混合分词器初始化完成")
        
        logger.info("PgVector推荐服务初始化完成")
    
    def load_word_vectors(self) -> Dict[str, np.ndarray]:
        """加载词向量模型"""
        try:
            # 使用现有的推荐服务加载词向量
            from app.services.recommendation_service import RecommendationService
            old_service = RecommendationService()
            
            # 确保词向量模型已加载
            if not old_service.word_vectors:
                logger.warning("RecommendationService词向量模型未加载，尝试加载...")
                if old_service.load_word_vectors():
                    self.word_vectors = old_service.word_vectors
                    logger.info("词向量模型加载完成")
                else:
                    logger.error("词向量模型加载失败")
                    return {}
            else:
                self.word_vectors = old_service.word_vectors
                logger.info("词向量模型加载完成")
            
            return self.word_vectors
        except Exception as e:
            logger.error(f"加载词向量模型失败: {e}")
            return {}
    
    def calculate_query_vector(self, query: str) -> Optional[str]:
        """计算查询向量"""
        try:
            # 确保查询字符串是UTF-8编码
            if isinstance(query, bytes):
                query = query.decode('utf-8')
            
            logger.info(f"计算查询向量: '{query}'")
            
            # 使用混合分词器处理查询
            if self.hybrid_processor:
                words = self.hybrid_processor.segment_text(query)
                logger.info(f"混合分词结果: {words}")
                meaningful_words = words  # 混合分词器已经过滤了有意义的词
            else:
                # 降级到原始分词器
                words = self.text_processor.segment_text(query)
                logger.info(f"原始分词结果: {words}")
                
                # 过滤有意义的词
                meaningful_words = []
                for word in words:
                    if self.text_processor._is_meaningful_word(word):
                        meaningful_words.append(word)
            
            logger.info(f"有意义的词: {meaningful_words}")
            
            if not meaningful_words:
                logger.warning("没有找到有意义的词")
                return None
            
            # 计算词向量的平均值
            vectors = []
            for word in meaningful_words:
                if word in self.word_vectors:
                    vectors.append(self.word_vectors[word])
                    logger.debug(f"词 '{word}' 向量获取成功")
                else:
                    logger.warning(f"词 '{word}' 不在词向量模型中")
            
            if not vectors:
                logger.warning("无法获取任何词向量")
                return None
            
            # 计算平均向量
            avg_vector = np.mean(vectors, axis=0)
            
            # 转换为PostgreSQL vector格式
            vector_str = '[' + ','.join(map(str, avg_vector)) + ']'
            logger.info(f"查询向量计算完成，长度: {len(avg_vector)}")
            return vector_str
            
        except Exception as e:
            logger.error(f"计算查询向量失败: {e}")
            return None
    
    def semantic_search(self, query: str, top_k: int = 20) -> List[Dict]:
        """使用pgvector进行全量语义搜索"""
        try:
            logger.info(f"开始语义搜索: query='{query}', top_k={top_k}")
            
            # 计算查询向量
            query_vector = self.calculate_query_vector(query)
            if not query_vector:
                logger.warning("无法计算查询向量")
                return []
            
            logger.info(f"查询向量计算完成，长度: {len(query_vector)}")
            
            # 使用pgvector进行相似度搜索
            # 这里使用余弦相似度 (<=> 操作符)
            sql = text("""
                SELECT 
                    id, 
                    name, 
                    description, 
                    price, 
                    category_id, 
                    image_url, 
                    tags,
                    product_vector <=> :query_vector as distance,
                    1 - (product_vector <=> :query_vector) as similarity
                FROM products 
                WHERE product_vector IS NOT NULL
                ORDER BY product_vector <=> :query_vector
                LIMIT :top_k
            """)
            
            logger.info(f"执行SQL查询，查询向量: {query_vector[:50]}...")
            result = db.session.execute(sql, {
                'query_vector': query_vector,
                'top_k': top_k
            })
            
            # 格式化结果
            results = []
            for row in result.fetchall():
                product_data = {
                    'id': row.id,
                    'name': row.name,
                    'description': row.description,
                    'price': row.price,
                    'category_id': row.category_id,
                    'image_url': row.image_url,
                    'tags': json.loads(row.tags) if row.tags else [],
                    'similarity': float(row.similarity),
                    'distance': float(row.distance)
                }
                results.append(product_data)
            
            logger.info(f"语义搜索完成，返回 {len(results)} 条结果")
            return results
            
        except Exception as e:
            logger.error(f"语义搜索失败: {e}")
            return []
    
    def get_similar_products(self, product_id: int, top_k: int = 10) -> List[Dict]:
        """获取相似商品"""
        try:
            logger.info(f"获取相似商品: product_id={product_id}, top_k={top_k}")
            
            # 获取目标商品的向量
            product = Product.query.filter_by(id=product_id).first()
            if not product or not product.embedding:
                logger.warning(f"商品 {product_id} 不存在或没有向量数据")
                return []
            
            # 将embedding转换为vector格式
            try:
                vector_data = json.loads(product.embedding)
                product_vector = '[' + ','.join(map(str, vector_data)) + ']'
            except:
                logger.error(f"商品 {product_id} 的向量数据格式错误")
                return []
            
            # 使用pgvector进行相似度搜索
            sql = text("""
                SELECT 
                    id, 
                    name, 
                    description, 
                    price, 
                    category_id, 
                    image_url, 
                    tags,
                    product_vector <=> :product_vector as distance,
                    1 - (product_vector <=> :product_vector) as similarity
                FROM products 
                WHERE product_vector IS NOT NULL 
                AND id != :product_id
                ORDER BY product_vector <=> :product_vector
                LIMIT :top_k
            """)
            
            result = db.session.execute(sql, {
                'product_vector': product_vector,
                'product_id': product_id,
                'top_k': top_k
            })
            
            # 格式化结果
            results = []
            for row in result.fetchall():
                product_data = {
                    'id': row.id,
                    'name': row.name,
                    'description': row.description,
                    'price': row.price,
                    'category_id': row.category_id,
                    'image_url': row.image_url,
                    'tags': json.loads(row.tags) if row.tags else [],
                    'similarity': float(row.similarity),
                    'distance': float(row.distance)
                }
                results.append(product_data)
            
            logger.info(f"获取相似商品完成，返回 {len(results)} 条结果")
            return results
            
        except Exception as e:
            logger.error(f"获取相似商品失败: {e}")
            return []
    
    def get_category_recommendations(self, category_id: int, top_k: int = 20) -> List[Dict]:
        """获取分类推荐商品"""
        try:
            logger.info(f"获取分类推荐: category_id={category_id}, top_k={top_k}")
            
            # 获取分类信息
            category = Category.query.filter_by(id=category_id).first()
            if not category:
                logger.warning(f"分类 {category_id} 不存在")
                return []
            
            # 计算分类关键词的向量
            category_vector = self.calculate_query_vector(category.name)
            if not category_vector:
                logger.warning(f"无法计算分类 {category_id} 的向量")
                return []
            
            # 使用pgvector进行相似度搜索
            sql = text("""
                SELECT 
                    id, 
                    name, 
                    description, 
                    price, 
                    category_id, 
                    image_url, 
                    tags,
                    product_vector <=> :category_vector as distance,
                    1 - (product_vector <=> :category_vector) as similarity
                FROM products 
                WHERE product_vector IS NOT NULL
                AND category_id = :category_id
                ORDER BY product_vector <=> :category_vector
                LIMIT :top_k
            """)
            
            result = db.session.execute(sql, {
                'category_vector': category_vector,
                'category_id': category_id,
                'top_k': top_k
            })
            
            # 格式化结果
            results = []
            for row in result.fetchall():
                product_data = {
                    'id': row.id,
                    'name': row.name,
                    'description': row.description,
                    'price': row.price,
                    'category_id': row.category_id,
                    'image_url': row.image_url,
                    'tags': json.loads(row.tags) if row.tags else [],
                    'similarity': float(row.similarity),
                    'distance': float(row.distance)
                }
                results.append(product_data)
            
            logger.info(f"获取分类推荐完成，返回 {len(results)} 条结果")
            return results
            
        except Exception as e:
            logger.error(f"获取分类推荐失败: {e}")
            return []
    
    def batch_semantic_search(self, queries: List[str], top_k: int = 10) -> Dict[str, List[Dict]]:
        """批量语义搜索"""
        try:
            logger.info(f"开始批量语义搜索: {len(queries)} 个查询")
            
            results = {}
            for query in queries:
                results[query] = self.semantic_search(query, top_k)
            
            logger.info("批量语义搜索完成")
            return results
            
        except Exception as e:
            logger.error(f"批量语义搜索失败: {e}")
            return {}
    
    def get_search_statistics(self) -> Dict:
        """获取搜索统计信息"""
        try:
            # 获取商品总数
            total_products = Product.query.count()
            
            # 获取有向量的商品数
            products_with_vectors = Product.query.filter(Product.embedding.isnot(None)).count()
            
            # 获取分类数
            total_categories = Category.query.count()
            
            # 获取标签数
            total_tags = ProductTag.query.count()
            
            return {
                'total_products': total_products,
                'products_with_vectors': products_with_vectors,
                'vector_coverage': products_with_vectors / total_products if total_products > 0 else 0,
                'total_categories': total_categories,
                'total_tags': total_tags
            }
            
        except Exception as e:
            logger.error(f"获取搜索统计信息失败: {e}")
            return {}
