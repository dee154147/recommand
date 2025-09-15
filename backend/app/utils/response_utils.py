"""
响应工具模块
提供统一的API响应格式
"""

from flask import jsonify
from datetime import datetime
from typing import Any, Dict, Optional


def success_response(data: Any = None, message: str = "操作成功", code: int = 200) -> Dict:
    """
    成功响应格式
    """
    response = {
        "success": True,
        "data": data,
        "message": message,
        "code": code,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response), code


def error_response(message: str = "操作失败", code: int = 500, data: Any = None) -> Dict:
    """
    错误响应格式
    """
    response = {
        "success": False,
        "data": data,
        "message": message,
        "code": code,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response), code


def validation_error_response(errors: Dict[str, str], message: str = "参数验证失败") -> Dict:
    """
    参数验证错误响应格式
    """
    response = {
        "success": False,
        "data": {"errors": errors},
        "message": message,
        "code": 400,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response), 400


def not_found_response(message: str = "资源不存在") -> Dict:
    """
    资源不存在响应格式
    """
    response = {
        "success": False,
        "data": None,
        "message": message,
        "code": 404,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response), 404


def unauthorized_response(message: str = "未授权访问") -> Dict:
    """
    未授权响应格式
    """
    response = {
        "success": False,
        "data": None,
        "message": message,
        "code": 401,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response), 401


def forbidden_response(message: str = "禁止访问") -> Dict:
    """
    禁止访问响应格式
    """
    response = {
        "success": False,
        "data": None,
        "message": message,
        "code": 403,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response), 403


def paginated_response(data: list, page: int, per_page: int, total: int, message: str = "获取数据成功") -> Dict:
    """
    分页响应格式
    """
    total_pages = (total + per_page - 1) // per_page
    
    pagination_info = {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }
    
    response = {
        "success": True,
        "data": {
            "items": data,
            "pagination": pagination_info
        },
        "message": message,
        "code": 200,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response), 200
