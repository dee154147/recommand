"""
基于内容的推荐算法服务
实现商品标签向量计算和商品特征向量生成
"""

import os
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from gensim.models import KeyedVectors
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
import logging
import hashlib
from functools import lru_cache
import time

from app import db
from app.models import Product, ProductTag, TagVector, Category
from app.utils.text_processing import TextProcessor

logger = logging.getLogger(__name__)

class RecommendationService:
    """推荐算法服务类"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecommendationService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # 从backend/app/services向上三级到项目根目录
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            self.model_path = os.path.join(project_root, 'model', 'Tencent_AILab_ChineseEmbedding.bin')
            self.word_vectors = None
            self.text_processor = TextProcessor()
            self.vector_dim = 200  # Tencent词向量维度
            
            # 查询结果缓存
            self.search_cache = {}
            self.cache_max_size = 100
            self.cache_ttl = 300  # 5分钟缓存时间
            
            # 在初始化时加载词向量模型
            logger.info("初始化推荐服务，正在加载词向量模型...")
            self.load_word_vectors()
            
            self._initialized = True
        
    def load_word_vectors(self) -> bool:
        """加载词向量模型"""
        try:
            if not os.path.exists(self.model_path):
                logger.error(f"词向量模型文件不存在: {self.model_path}")
                return False
                
            logger.info("正在加载Tencent词向量模型...")
            self.word_vectors = KeyedVectors.load(self.model_path, mmap='r')
            logger.info(f"词向量模型加载成功，词汇量: {len(self.word_vectors)}")
            return True
            
        except Exception as e:
            logger.error(f"加载词向量模型失败: {str(e)}")
            return False
    
    def _get_cache_key(self, query: str, top_k: int) -> str:
        """生成缓存键"""
        return hashlib.md5(f"{query}_{top_k}".encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[List[Dict]]:
        """从缓存获取结果"""
        if cache_key in self.search_cache:
            cached_data = self.search_cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_ttl:
                logger.debug(f"从缓存获取查询结果: {cache_key}")
                return cached_data['results']
            else:
                # 缓存过期，删除
                del self.search_cache[cache_key]
        return None
    
    def _save_to_cache(self, cache_key: str, results: List[Dict]):
        """保存结果到缓存"""
        # 清理过期缓存
        current_time = time.time()
        expired_keys = [k for k, v in self.search_cache.items() 
                       if current_time - v['timestamp'] > self.cache_ttl]
        for key in expired_keys:
            del self.search_cache[key]
        
        # 限制缓存大小
        if len(self.search_cache) >= self.cache_max_size:
            # 删除最旧的缓存
            oldest_key = min(self.search_cache.keys(), 
                           key=lambda k: self.search_cache[k]['timestamp'])
            del self.search_cache[oldest_key]
        
        self.search_cache[cache_key] = {
            'results': results,
            'timestamp': current_time
        }
        logger.debug(f"保存查询结果到缓存: {cache_key}")
    
    @lru_cache(maxsize=10000)
    def get_word_vector(self, word: str) -> Optional[np.ndarray]:
        """获取单个词的向量（带缓存）"""
        if not self.word_vectors:
            return None
            
        try:
            if word in self.word_vectors:
                return self.word_vectors[word]
            else:
                # 尝试小写
                word_lower = word.lower()
                if word_lower in self.word_vectors:
                    return self.word_vectors[word_lower]
                else:
                    logger.debug(f"词 '{word}' 不在词向量模型中")
                    return None
        except Exception as e:
            logger.error(f"获取词向量失败: {str(e)}")
            return None
    
    def calculate_tag_vector(self, tag: str) -> Optional[np.ndarray]:
        """计算标签的向量表示"""
        if not self.word_vectors:
            return None
            
        try:
            # 对标签进行分词
            words = self.text_processor.segment_text(tag)
            if not words:
                return None
            
            # 获取所有词的向量
            word_vectors = []
            for word in words:
                vector = self.get_word_vector(word)
                if vector is not None:
                    word_vectors.append(vector)
            
            if not word_vectors:
                logger.debug(f"标签 '{tag}' 无法获取有效词向量")
                return None
            
            # 计算标签向量的平均值
            tag_vector = np.mean(word_vectors, axis=0)
            return tag_vector
            
        except Exception as e:
            logger.error(f"计算标签向量失败: {str(e)}")
            return None
    
    def precompute_tag_vectors(self) -> Dict[str, int]:
        """预计算所有标签的向量"""
        logger.info("开始预计算标签向量...")
        
        if not self.load_word_vectors():
            return {"success": 0, "failed": 0, "error": "词向量模型加载失败"}
        
        # 获取所有唯一的标签
        unique_tags = db.session.query(ProductTag.tag).distinct().all()
        unique_tags = [tag[0] for tag in unique_tags]
        
        logger.info(f"发现 {len(unique_tags)} 个唯一标签")
        
        success_count = 0
        failed_count = 0
        
        for tag in unique_tags:
            try:
                # 检查是否已经计算过
                existing_vector = TagVector.query.filter_by(tag=tag).first()
                if existing_vector:
                    logger.debug(f"标签 '{tag}' 的向量已存在，跳过")
                    continue
                
                # 计算标签向量
                tag_vector = self.calculate_tag_vector(tag)
                if tag_vector is not None:
                    # 保存到数据库
                    tag_vector_obj = TagVector(
                        tag=tag,
                        vector=json.dumps(tag_vector.tolist())
                    )
                    db.session.add(tag_vector_obj)
                    success_count += 1
                    
                    if success_count % 100 == 0:
                        db.session.commit()
                        logger.info(f"已处理 {success_count} 个标签向量")
                        
                else:
                    failed_count += 1
                    logger.debug(f"标签 '{tag}' 向量计算失败")
                    
            except Exception as e:
                failed_count += 1
                logger.error(f"处理标签 '{tag}' 时出错: {str(e)}")
        
        # 提交剩余的更改
        try:
            db.session.commit()
            logger.info(f"标签向量预计算完成: 成功 {success_count}, 失败 {failed_count}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"提交标签向量时出错: {str(e)}")
            return {"success": 0, "failed": 0, "error": str(e)}
        
        return {"success": success_count, "failed": failed_count}
    
    def calculate_product_vector(self, product_id: int) -> Optional[np.ndarray]:
        """计算商品的特征向量（基于标签向量的加权平均）"""
        try:
            # 获取商品的所有标签及其权重
            product_tags = db.session.query(ProductTag).filter(
                ProductTag.product_id == product_id
            ).all()
            
            if not product_tags:
                logger.debug(f"商品 {product_id} 没有标签")
                return None
            
            # 获取标签向量
            tag_vectors = []
            weights = []
            
            for product_tag in product_tags:
                tag_vector_obj = TagVector.query.filter_by(tag=product_tag.tag).first()
                if tag_vector_obj:
                    vector = np.array(json.loads(tag_vector_obj.vector))
                    tag_vectors.append(vector)
                    weights.append(float(product_tag.weight) if product_tag.weight else 1.0)
            
            if not tag_vectors:
                logger.debug(f"商品 {product_id} 没有有效的标签向量")
                return None
            
            # 计算加权平均向量
            tag_vectors = np.array(tag_vectors)
            weights = np.array(weights)
            
            # 归一化权重
            weights = weights / np.sum(weights)
            
            # 计算加权平均
            product_vector = np.average(tag_vectors, axis=0, weights=weights)
            
            return product_vector
            
        except Exception as e:
            logger.error(f"计算商品 {product_id} 向量失败: {str(e)}")
            return None
    
    def precompute_product_vectors(self) -> Dict[str, int]:
        """预计算所有商品的特征向量"""
        logger.info("开始预计算商品特征向量...")
        
        # 获取所有商品
        products = Product.query.all()
        logger.info(f"发现 {len(products)} 个商品")
        
        success_count = 0
        failed_count = 0
        
        for product in products:
            try:
                # 检查是否已经计算过
                if product.embedding:
                    logger.debug(f"商品 {product.id} 的向量已存在，跳过")
                    continue
                
                # 计算商品向量
                product_vector = self.calculate_product_vector(product.id)
                if product_vector is not None:
                    # 保存到数据库
                    product.embedding = json.dumps(product_vector.tolist())
                    success_count += 1
                    
                    if success_count % 100 == 0:
                        db.session.commit()
                        logger.info(f"已处理 {success_count} 个商品向量")
                        
                else:
                    failed_count += 1
                    logger.debug(f"商品 {product.id} 向量计算失败")
                    
            except Exception as e:
                failed_count += 1
                logger.error(f"处理商品 {product.id} 时出错: {str(e)}")
        
        # 提交剩余的更改
        try:
            db.session.commit()
            logger.info(f"商品向量预计算完成: 成功 {success_count}, 失败 {failed_count}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"提交商品向量时出错: {str(e)}")
            return {"success": 0, "failed": 0, "error": str(e)}
        
        return {"success": success_count, "failed": failed_count}
    
    def calculate_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """计算两个向量的余弦相似度"""
        try:
            # 计算余弦相似度
            dot_product = np.dot(vector1, vector2)
            norm1 = np.linalg.norm(vector1)
            norm2 = np.linalg.norm(vector2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"计算相似度失败: {str(e)}")
            return 0.0
    
    def find_similar_products(self, product_id: int, top_k: int = 10) -> List[Dict]:
        """找到与指定商品相似的商品"""
        try:
            # 获取目标商品的向量
            target_product = Product.query.get(product_id)
            if not target_product or not target_product.embedding:
                logger.warning(f"商品 {product_id} 没有特征向量")
                return []
            
            target_vector = np.array(json.loads(target_product.embedding))
            
            # 获取所有有向量的商品
            products_with_vectors = Product.query.filter(
                Product.embedding.isnot(None),
                Product.id != product_id
            ).all()
            
            similarities = []
            for product in products_with_vectors:
                try:
                    product_vector = np.array(json.loads(product.embedding))
                    similarity = self.calculate_similarity(target_vector, product_vector)
                    
                    similarities.append({
                        'product_id': product.id,
                        'product_name': product.name,
                        'similarity': similarity
                    })
                except Exception as e:
                    logger.error(f"计算商品 {product.id} 相似度失败: {str(e)}")
                    continue
            
            # 按相似度排序
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"查找相似商品失败: {str(e)}")
            return []
    
    def semantic_search(self, query: str, top_k: int = 20, timeout: int = 30) -> List[Dict]:
        """基于语义的搜索 - 使用pgvector进行全量向量相似度匹配"""
        start_time = time.time()
        
        try:
            # 检查缓存
            cache_key = self._get_cache_key(query, top_k)
            cached_results = self._get_from_cache(cache_key)
            if cached_results is not None:
                return cached_results
            
            # 确保词向量模型已加载
            if not self.word_vectors:
                logger.warning("词向量模型未加载，使用降级策略")
                return self._fallback_tag_search(query, top_k)
            
            # 对查询进行分词
            query_words = self.text_processor.segment_text(query)
            logger.info(f"查询 '{query}' 分词结果: {query_words}")
            if not query_words:
                logger.warning(f"查询 '{query}' 分词结果为空")
                return []
            
            # 计算查询向量
            query_vectors = []
            for word in query_words:
                vector = self.get_word_vector(word)
                if vector is not None:
                    query_vectors.append(vector)
                    logger.debug(f"词 '{word}' 向量获取成功")
                else:
                    logger.warning(f"词 '{word}' 向量获取失败")
            
            if not query_vectors:
                logger.warning(f"查询 '{query}' 无法获取有效词向量")
                return []
            
            logger.info(f"查询 '{query}' 成功获取 {len(query_vectors)} 个词向量")
    
            # 计算查询向量的平均值
            query_vector = np.mean(query_vectors, axis=0)
            
            # 转换为PostgreSQL vector格式
            vector_str = '[' + ','.join(map(str, query_vector)) + ']'
            
            # 使用pgvector进行全量向量相似度搜索
            from sqlalchemy import text
            
            sql_query = text("""
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
            
            # 执行查询
            result = db.session.execute(sql_query, {
                'query_vector': vector_str,
                'top_k': top_k
            })
            
            # 格式化结果
            similarities = []
            for row in result.fetchall():
                similarities.append({
                    'product_id': row.id,
                    'product_name': row.name,
                    'similarity': float(row.similarity)
                })
            
            # 添加调试信息
            logger.info(f"语义搜索 '{query}' 使用pgvector全量搜索，找到 {len(similarities)} 个商品，最高相似度: {similarities[0]['similarity'] if similarities else 0}")
            
            # 保存到缓存
            self._save_to_cache(cache_key, similarities)
            
            return similarities
            
        except Exception as e:
            logger.error(f"语义搜索失败: {str(e)}")
            # 降级策略：使用标签匹配
            return self._fallback_tag_search(query, top_k)
    
    def _fallback_tag_search(self, query: str, top_k: int = 20) -> List[Dict]:
        """降级策略：基于标签的快速搜索"""
        try:
            logger.info(f"使用降级策略搜索: {query}")
            
            # 对查询进行分词
            query_words = self.text_processor.segment_text(query)
            if not query_words:
                return []
            
            # 通过标签匹配找到商品
            products = []
            for word in query_words:
                if len(word) > 1:  # 过滤单字符
                    # 直接查询商品，避免复杂的JOIN操作
                    matched_products = db.session.query(Product).join(ProductTag).filter(
                        ProductTag.tag.like(f'%{word}%')
                    ).order_by(Product.id).limit(50).all()  # 限制数量
                    
                    products.extend(matched_products)
            
            # 去重
            seen_ids = set()
            unique_products = []
            for product in products:
                if product.id not in seen_ids:
                    seen_ids.add(product.id)
                    unique_products.append(product)
            
            # 如果没有标签匹配，则选择一些商品作为候选
            if not unique_products:
                unique_products = Product.query.order_by(Product.id).limit(20).all()
            
            # 构建结果
            results = []
            for product in unique_products[:top_k]:
                results.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'similarity': 0.5  # 降级搜索给一个固定相似度
                })
            
            logger.info(f"降级搜索 '{query}' 找到 {len(results)} 个商品")
            return results
            
        except Exception as e:
            logger.error(f"降级搜索失败: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict:
        """获取推荐算法统计信息"""
        try:
            total_products = Product.query.count()
            products_with_vectors = Product.query.filter(Product.embedding.isnot(None)).count()
            total_tags = ProductTag.query.count()
            unique_tags = db.session.query(ProductTag.tag).distinct().count()
            tag_vectors_count = TagVector.query.count()
            
            return {
                'total_products': total_products,
                'products_with_vectors': products_with_vectors,
                'vector_coverage': products_with_vectors / total_products if total_products > 0 else 0,
                'total_tags': total_tags,
                'unique_tags': unique_tags,
                'tag_vectors_count': tag_vectors_count,
                'tag_vector_coverage': tag_vectors_count / unique_tags if unique_tags > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {str(e)}")
            return {}