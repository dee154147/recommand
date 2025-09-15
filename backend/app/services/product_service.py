from flask import current_app
from app import db
from app.models import Product, Category
from sqlalchemy import or_, and_, func, text
import json
import os
import time
from functools import lru_cache

class ProductService:
    """商品服务类"""
    
    def __init__(self):
        self.per_page = current_app.config.get('POSTS_PER_PAGE', 20)
        # 查询缓存
        self._query_cache = {}
        self._cache_ttl = 300  # 5分钟缓存
    
    def get_products(self, page=1, per_page=None, category=None, search=None):
        """获取商品列表"""
        if per_page is None:
            per_page = self.per_page
            
        query = Product.query
        
        # 按分类筛选
        if category:
            query = query.join(Category).filter(Category.name == category)
        
        # 搜索功能
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.title.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # 分页
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        products = [product.to_dict() for product in pagination.items]
        
        return {
            'products': products,
            'pagination': {
                'page': page,
                'pages': pagination.pages,
                'per_page': per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
    
    def get_product_by_id(self, product_id):
        """根据ID获取商品详情"""
        product = Product.query.filter_by(id=product_id).first()
        return product.to_dict() if product else None
    
    def get_product_by_product_id(self, product_id):
        """根据商品ID获取商品详情"""
        product = Product.query.filter_by(product_id=product_id).first()
        return product.to_dict() if product else None
    
    def search_products(self, query, page=1, per_page=None):
        """搜索商品 - 优化版本"""
        if per_page is None:
            per_page = self.per_page
        
        # 检查缓存
        cache_key = f"search_{query}_{page}_{per_page}"
        current_time = time.time()
        
        if cache_key in self._query_cache:
            cached_data, cache_time = self._query_cache[cache_key]
            if current_time - cache_time < self._cache_ttl:
                return cached_data
        
        # 优化查询：使用更精确的搜索条件
        search_term = f"%{query}%"
        
        # 使用原生SQL优化查询性能
        sql_query = text("""
            SELECT p.id, p.name, p.description, p.price, p.category_id, 
                   p.image_url, p.tags, p.embedding, p.created_at, p.updated_at,
                   c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.name LIKE :search_term 
               OR p.description LIKE :search_term
               OR p.tags LIKE :search_term
            ORDER BY p.id
            LIMIT :limit OFFSET :offset
        """)
        
        offset = (page - 1) * per_page
        
        # 执行查询
        result = db.session.execute(sql_query, {
            'search_term': search_term,
            'limit': per_page,
            'offset': offset
        })
        
        products = []
        for row in result:
            product_data = {
                'id': row.id,
                'name': row.name,
                'description': row.description,
                'price': float(row.price) if row.price else None,
                'category_id': row.category_id,
                'category_name': row.category_name,
                'image_url': row.image_url,
                'tags': json.loads(row.tags) if row.tags else [],
                'embedding': json.loads(row.embedding) if row.embedding else None,
                'created_at': row.created_at.isoformat() if row.created_at else None,
                'updated_at': row.updated_at.isoformat() if row.updated_at else None
            }
            products.append(product_data)
        
        # 获取总数（优化版本）
        count_query = text("""
            SELECT COUNT(*) as total
            FROM products p
            WHERE p.name LIKE :search_term 
               OR p.description LIKE :search_term
               OR p.tags LIKE :search_term
        """)
        
        total_result = db.session.execute(count_query, {'search_term': search_term})
        total = total_result.fetchone().total
        
        # 计算分页信息
        pages = (total + per_page - 1) // per_page
        
        result_data = {
            'products': products,
            'query': query,
            'pagination': {
                'page': page,
                'pages': pages,
                'per_page': per_page,
                'total': total,
                'has_next': page < pages,
                'has_prev': page > 1
            }
        }
        
        # 缓存结果
        self._query_cache[cache_key] = (result_data, current_time)
        
        return result_data
    
    def get_categories(self):
        """获取所有分类"""
        categories = Category.query.all()
        return [category.to_dict() for category in categories]
    
    def get_category_by_id(self, category_id):
        """根据ID获取分类"""
        category = Category.query.filter_by(id=category_id).first()
        return category.to_dict() if category else None
    
    def create_product(self, product_data):
        """创建新商品"""
        product = Product(
            product_id=product_data.get('product_id'),
            title=product_data.get('title'),
            image_url=product_data.get('image_url'),
            category_id=product_data.get('category_id'),
            price=product_data.get('price'),
            description=product_data.get('description'),
            keywords=json.dumps(product_data.get('keywords', []))
        )
        
        db.session.add(product)
        db.session.commit()
        
        return product.to_dict()
    
    def update_product(self, product_id, product_data):
        """更新商品信息"""
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return None
            
        # 更新字段
        for key, value in product_data.items():
            if hasattr(product, key):
                if key == 'keywords':
                    setattr(product, key, json.dumps(value))
                else:
                    setattr(product, key, value)
        
        db.session.commit()
        return product.to_dict()
    
    def delete_product(self, product_id):
        """删除商品"""
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return False
            
        db.session.delete(product)
        db.session.commit()
        return True
    
    def get_products_by_category(self, category_id, page=1, per_page=None):
        """根据分类获取商品"""
        if per_page is None:
            per_page = self.per_page
            
        products_query = Product.query.filter_by(category_id=category_id)
        
        pagination = products_query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        products = [product.to_dict() for product in pagination.items]
        
        return {
            'products': products,
            'category_id': category_id,
            'pagination': {
                'page': page,
                'pages': pagination.pages,
                'per_page': per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
