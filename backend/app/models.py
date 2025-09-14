from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import ARRAY
import json

class Product(db.Model):
    """商品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    
    # 推荐系统相关字段
    keywords = db.Column(db.Text)  # 关键词，JSON格式存储
    vector_embedding = db.Column(db.Text)  # 向量嵌入，JSON格式存储
    similarity_scores = db.Column(db.Text)  # 相似度分数，JSON格式存储
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    interactions = db.relationship('UserInteraction', backref='product', lazy=True)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'title': self.title,
            'image_url': self.image_url,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'price': self.price,
            'description': self.description,
            'keywords': json.loads(self.keywords) if self.keywords else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.product_id}: {self.title[:50]}...>'

class Category(db.Model):
    """商品分类模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    keywords = db.Column(db.Text)  # 关键词列表，JSON格式存储
    description = db.Column(db.Text)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'keywords': json.loads(self.keywords) if self.keywords else [],
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    
    # 用户偏好相关
    preferences = db.Column(db.Text)  # 用户偏好，JSON格式存储
    behavior_vector = db.Column(db.Text)  # 行为向量，JSON格式存储
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    interactions = db.relationship('UserInteraction', backref='user', lazy=True)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'preferences': json.loads(self.preferences) if self.preferences else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.user_id}: {self.username}>'

class UserInteraction(db.Model):
    """用户交互模型"""
    __tablename__ = 'user_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False)  # view, click, like, purchase等
    interaction_score = db.Column(db.Float, default=1.0)  # 交互权重
    session_id = db.Column(db.String(100))  # 会话ID
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 索引
    __table_args__ = (
        db.Index('idx_user_product', 'user_id', 'product_id'),
        db.Index('idx_interaction_type', 'interaction_type'),
        db.Index('idx_created_at', 'created_at'),
    )
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'interaction_type': self.interaction_type,
            'interaction_score': self.interaction_score,
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<UserInteraction {self.user_id}-{self.product_id}: {self.interaction_type}>'

class RecommendationCache(db.Model):
    """推荐结果缓存模型"""
    __tablename__ = 'recommendation_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    cache_key = db.Column(db.String(200), unique=True, nullable=False, index=True)
    cache_type = db.Column(db.String(50), nullable=False)  # similar_products, user_recommendations等
    target_id = db.Column(db.String(50), nullable=False)  # 目标ID（商品ID或用户ID）
    recommendations = db.Column(db.Text, nullable=False)  # 推荐结果，JSON格式存储
    similarity_scores = db.Column(db.Text)  # 相似度分数，JSON格式存储
    
    # 缓存过期时间
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'cache_key': self.cache_key,
            'cache_type': self.cache_type,
            'target_id': self.target_id,
            'recommendations': json.loads(self.recommendations) if self.recommendations else [],
            'similarity_scores': json.loads(self.similarity_scores) if self.similarity_scores else {},
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<RecommendationCache {self.cache_type}: {self.target_id}>'
