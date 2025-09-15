"""
相似商品查询服务
基于商品向量计算相似度，提供相似商品推荐功能
"""

import json
import numpy as np
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import sessionmaker
import logging
import time
from functools import lru_cache

from app import db
from app.models import Product

logger = logging.getLogger(__name__)

class SimilarProductService:
    """相似商品查询服务类"""
    
    def __init__(self):
        self.vector_dimension = 200  # 腾讯词向量维度
        self.cache_size = 1000  # 缓存大小
        self._vector_cache = {}  # 向量缓存
        
    def _get_product_vector(self, product_id: int) -> Optional[np.ndarray]:
        """获取商品向量"""
        try:
            # 先检查缓存
            if product_id in self._vector_cache:
                return self._vector_cache[product_id]
            
            # 从数据库获取
            product = db.session.query(Product).filter(
                Product.id == product_id,
                Product.embedding.isnot(None)
            ).first()
            
            if not product:
                logger.warning(f"商品 {product_id} 不存在或没有向量")
                return None
            
            # 解析向量
            embedding_data = json.loads(product.embedding)
            if not isinstance(embedding_data, list) or len(embedding_data) != self.vector_dimension:
                logger.warning(f"商品 {product_id} 向量格式错误: {type(embedding_data)}, 长度: {len(embedding_data) if isinstance(embedding_data, list) else 'N/A'}")
                return None
            
            vector = np.array(embedding_data, dtype=np.float32)
            
            # 缓存向量
            if len(self._vector_cache) < self.cache_size:
                self._vector_cache[product_id] = vector
            
            return vector
            
        except Exception as e:
            logger.error(f"获取商品 {product_id} 向量失败: {e}")
            return None
    
    def _calculate_cosine_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """计算余弦相似度"""
        try:
            # 计算点积
            dot_product = np.dot(vector1, vector2)
            
            # 计算向量模长
            norm1 = np.linalg.norm(vector1)
            norm2 = np.linalg.norm(vector2)
            
            # 避免除零错误
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # 计算余弦相似度
            similarity = dot_product / (norm1 * norm2)
            
            # 确保相似度在[-1, 1]范围内
            return max(-1.0, min(1.0, similarity))
            
        except Exception as e:
            logger.error(f"计算余弦相似度失败: {e}")
            return 0.0
    
    def _clean_image_url(self, image_url: str) -> str:
        """清理图片URL中的特殊字符 - 仅用于修复相似商品列表图片显示问题"""
        if not image_url:
            return ""
        
        # 直接去掉文件扩展名之后的所有字符串
        # 使用简单的字符串分割方法
        if '.jpg' in image_url:
            return image_url.split('.jpg')[0] + '.jpg'
        elif '.jpeg' in image_url:
            return image_url.split('.jpeg')[0] + '.jpeg'
        elif '.png' in image_url:
            return image_url.split('.png')[0] + '.png'
        elif '.gif' in image_url:
            return image_url.split('.gif')[0] + '.gif'
        elif '.webp' in image_url:
            return image_url.split('.webp')[0] + '.webp'
        elif '.bmp' in image_url:
            return image_url.split('.bmp')[0] + '.bmp'
        
        # 如果没有找到标准扩展名，返回原URL
        return image_url
    
    def find_similar_products(self, 
                            product_id: int, 
                            limit: int = 10, 
                            threshold: float = 0.0,
                            exclude_self: bool = True) -> List[Dict]:
        """
        查找相似商品 - 使用pgvector进行全量向量搜索
        
        Args:
            product_id: 目标商品ID
            limit: 返回数量限制
            threshold: 相似度阈值
            exclude_self: 是否排除自身
            
        Returns:
            相似商品列表，包含商品信息和相似度
        """
        start_time = time.time()
        
        try:
            # 获取目标商品信息
            target_product = db.session.query(Product).filter(Product.id == product_id).first()
            if not target_product:
                logger.warning(f"商品 {product_id} 不存在")
                return []
            
            # 检查目标商品是否有向量数据
            if not target_product.embedding:
                logger.warning(f"商品 {product_id} 没有向量数据")
                return []
            
            logger.info(f"开始查找商品 {product_id} 的相似商品，限制: {limit}, 阈值: {threshold}")
            
            # 使用pgvector进行全量向量相似度搜索
            from sqlalchemy import text
            
            # 构建SQL查询
            sql_query = text("""
                SELECT 
                    id, 
                    name, 
                    description, 
                    price, 
                    category_id, 
                    image_url, 
                    tags,
                    product_vector <=> (SELECT product_vector FROM products WHERE id = :product_id) as distance,
                    1 - (product_vector <=> (SELECT product_vector FROM products WHERE id = :product_id)) as similarity
                FROM products 
                WHERE product_vector IS NOT NULL
            """)
            
            # 添加排除自身的条件
            if exclude_self:
                sql_query = text("""
                    SELECT 
                        id, 
                        name, 
                        description, 
                        price, 
                        category_id, 
                        image_url, 
                        tags,
                        product_vector <=> (SELECT product_vector FROM products WHERE id = :product_id) as distance,
                        1 - (product_vector <=> (SELECT product_vector FROM products WHERE id = :product_id)) as similarity
                    FROM products 
                    WHERE product_vector IS NOT NULL 
                    AND id != :product_id
                """)
            
            # 添加相似度阈值过滤和排序
            sql_query = text(str(sql_query) + """
                AND (1 - (product_vector <=> (SELECT product_vector FROM products WHERE id = :product_id))) >= :threshold
                ORDER BY product_vector <=> (SELECT product_vector FROM products WHERE id = :product_id)
                LIMIT :limit
            """)
            
            # 执行查询
            result = db.session.execute(sql_query, {
                'product_id': product_id,
                'threshold': threshold,
                'limit': limit
            })
            
            # 格式化结果
            similarities = []
            for row in result.fetchall():
                similarities.append({
                    'product_id': row.id,
                    'name': row.name,
                    'description': row.description,
                    'price': float(row.price) if row.price else None,
                    'category_id': row.category_id,
                    'image_url': self._clean_image_url(row.image_url),
                    'similarity': float(round(row.similarity, 4)),
                    'tags': json.loads(row.tags) if row.tags else []
                })
            
            # 记录查询日志
            query_time = (time.time() - start_time) * 1000  # 转换为毫秒
            logger.info(f"相似商品查询完成: 商品 {product_id}, 找到 {len(similarities)} 个结果, 耗时 {query_time:.2f}ms")
            
            return similarities
            
        except Exception as e:
            logger.error(f"查找相似商品失败: {e}")
            return []
    
    def batch_find_similar_products(self, 
                                  product_ids: List[int], 
                                  limit: int = 10, 
                                  threshold: float = 0.0) -> Dict[int, List[Dict]]:
        """
        批量查找相似商品
        
        Args:
            product_ids: 商品ID列表
            limit: 每个商品返回的数量限制
            threshold: 相似度阈值
            
        Returns:
            商品ID到相似商品列表的映射
        """
        results = {}
        
        for product_id in product_ids:
            try:
                similar_products = self.find_similar_products(
                    product_id=product_id,
                    limit=limit,
                    threshold=threshold,
                    exclude_self=True
                )
                results[product_id] = similar_products
                
            except Exception as e:
                logger.error(f"批量查询商品 {product_id} 相似商品失败: {e}")
                results[product_id] = []
        
        return results
    
    def calculate_similarity(self, product_id1: int, product_id2: int) -> Optional[float]:
        """
        计算两个商品之间的相似度
        
        Args:
            product_id1: 商品1 ID
            product_id2: 商品2 ID
            
        Returns:
            相似度分数，如果计算失败返回None
        """
        try:
            vector1 = self._get_product_vector(product_id1)
            vector2 = self._get_product_vector(product_id2)
            
            if vector1 is None or vector2 is None:
                return None
            
            similarity = self._calculate_cosine_similarity(vector1, vector2)
            return round(similarity, 4)
            
        except Exception as e:
            logger.error(f"计算商品 {product_id1} 和 {product_id2} 相似度失败: {e}")
            return None
    
    def get_similarity_stats(self) -> Dict:
        """获取相似度计算统计信息"""
        try:
            # 统计有向量的商品数量
            total_products = db.session.query(Product).count()
            products_with_vectors = db.session.query(Product).filter(
                Product.embedding.isnot(None)
            ).count()
            
            # 检查pgvector列的数据
            from sqlalchemy import text
            pgvector_count_result = db.session.execute(text("SELECT COUNT(*) FROM products WHERE product_vector IS NOT NULL")).fetchone()
            products_with_pgvector = pgvector_count_result[0] if pgvector_count_result else 0
            
            return {
                'total_products': total_products,
                'products_with_vectors': products_with_vectors,
                'products_with_pgvector': products_with_pgvector,
                'vector_coverage': round(products_with_vectors / total_products * 100, 2) if total_products > 0 else 0,
                'pgvector_coverage': round(products_with_pgvector / total_products * 100, 2) if total_products > 0 else 0,
                'vector_dimension': self.vector_dimension,
                'cache_size': len(self._vector_cache),
                'max_cache_size': self.cache_size,
                'implementation': 'pgvector_full_search'  # 标识当前实现方式
            }
            
        except Exception as e:
            logger.error(f"获取相似度统计信息失败: {e}")
            return {}
    
    def clear_cache(self):
        """清空向量缓存"""
        self._vector_cache.clear()
        logger.info("向量缓存已清空")
