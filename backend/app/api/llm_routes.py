# -*- coding: utf-8 -*-
"""
LLM API路由
用于处理LLM相关的API请求
"""

from flask import Blueprint, request, jsonify
import logging
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

# 创建蓝图
llm_bp = Blueprint('llm', __name__, url_prefix='/api/v1/llm')

@llm_bp.route('/generate-tags', methods=['POST'])
def generate_tags():
    """
    生成商品标签
    
    Request Body:
    {
        "description": "商品描述文本",
        "options": {
            "max_tags": 5,
            "language": "zh"
        }
    }
    
    Response:
    {
        "success": true,
        "data": {
            "tags": ["标签1", "标签2", "标签3", "标签4", "标签5"],
            "confidence": 0.85
        }
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据不能为空"
            }), 400
        
        # 验证必需参数
        description = data.get('description', '').strip()
        if not description:
            return jsonify({
                "success": False,
                "error": "商品描述不能为空"
            }), 400
        
        # 验证描述长度
        if len(description) < 10:
            return jsonify({
                "success": False,
                "error": "商品描述至少需要10个字符"
            }), 400
        
        if len(description) > 2000:
            return jsonify({
                "success": False,
                "error": "商品描述不能超过2000个字符"
            }), 400
        
        logger.info(f"收到标签生成请求，描述长度: {len(description)}")
        
        # 调用LLM服务生成标签
        tags = llm_service.generate_tags(description)
        
        logger.info(f"标签生成成功，生成标签数量: {len(tags)}")
        
        # 返回结果
        return jsonify({
            "success": True,
            "data": {
                "tags": tags,
                "confidence": 0.85,  # 模拟置信度
                "description": description
            }
        })
        
    except Exception as e:
        logger.error(f"生成商品标签失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"生成标签失败: {str(e)}"
        }), 500

@llm_bp.route('/test-connection', methods=['GET'])
def test_connection():
    """
    测试LLM API连接
    
    Response:
    {
        "success": true,
        "message": "LLM API连接成功",
        "data": {
            "status": "connected",
            "model": "Doubao-1.5-pro-32k",
            "response": "连接成功"
        }
    }
    """
    try:
        logger.info("开始测试LLM API连接")
        
        # 测试连接
        result = llm_service.test_connection()
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "LLM API连接成功",
                "data": {
                    "status": "connected",
                    "model": result.get("model", "Unknown"),
                    "response": result.get("response", "")
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": result["message"]
            }), 500
            
    except Exception as e:
        logger.error(f"测试LLM API连接失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"连接测试失败: {str(e)}"
        }), 500

@llm_bp.route('/health', methods=['GET'])
def health_check():
    """
    LLM服务健康检查
    
    Response:
    {
        "success": true,
        "message": "LLM服务正常",
        "data": {
            "status": "healthy",
            "timestamp": "2025-01-22T17:40:00Z"
        }
    }
    """
    try:
        from datetime import datetime
        
        return jsonify({
            "success": True,
            "message": "LLM服务正常",
            "data": {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        })
        
    except Exception as e:
        logger.error(f"LLM服务健康检查失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"健康检查失败: {str(e)}"
        }), 500

@llm_bp.errorhandler(400)
def handle_bad_request(error):
    """处理400错误"""
    return jsonify({
        "success": False,
        "error": "请求参数错误",
        "details": str(error)
    }), 400

@llm_bp.errorhandler(500)
def handle_internal_error(error):
    """处理500错误"""
    logger.error(f"LLM API内部错误: {str(error)}")
    return jsonify({
        "success": False,
        "error": "服务器内部错误",
        "details": "请稍后重试"
    }), 500

@llm_bp.errorhandler(404)
def handle_not_found(error):
    """处理404错误"""
    return jsonify({
        "success": False,
        "error": "API接口不存在"
    }), 404
