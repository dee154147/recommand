from flask import current_app
from app import db
from app.models import Product, Category
from sqlalchemy import or_, and_
import json
import os

class ProductService:
    """商品服务类"""
    
    def __init__(self):
        self.per_page = current_app.config.get('POSTS_PER_PAGE', 20)
    
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
        """搜索商品"""
        if per_page is None:
            per_page = self.per_page
            
        search_term = f"%{query}%"
        products_query = Product.query.filter(
            or_(
                Product.title.ilike(search_term),
                Product.description.ilike(search_term),
                Product.keywords.ilike(search_term)
            )
        )
        
        pagination = products_query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        products = [product.to_dict() for product in pagination.items]
        
        return {
            'products': products,
            'query': query,
            'pagination': {
                'page': page,
                'pages': pagination.pages,
                'per_page': per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
    
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
