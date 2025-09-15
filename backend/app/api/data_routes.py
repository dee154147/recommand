"""
数据处理API路由
提供商品数据导入、处理、统计等接口
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import os
import logging
from typing import Dict, Any

from ..services.data_processing_service import DataProcessingService

logger = logging.getLogger(__name__)

# 创建蓝图
data_bp = Blueprint('data', __name__, url_prefix='/api/v1/data')

# 初始化数据处理服务
data_service = DataProcessingService()


@data_bp.route('/import-products', methods=['POST'])
@cross_origin()
def import_products():
    """
    批量导入商品数据
    POST /api/v1/data/import-products
    """
    try:
        # 获取请求参数
        data = request.get_json() or {}
        file_path = data.get('file_path', 'data/product.txt')
        batch_size = data.get('batch_size', 100)
        
        # 验证参数
        if not file_path:
            return jsonify({'success': False, 'error': '文件路径不能为空'}), 400
        
        if batch_size <= 0 or batch_size > 1000:
            return jsonify({'success': False, 'error': '批次大小必须在1-1000之间'}), 400
        
        # 构建完整文件路径
        full_path = os.path.join(os.path.dirname(__file__), '../../..', file_path)
        
        # 检查文件是否存在
        if not os.path.exists(full_path):
            return jsonify({'success': False, 'error': f'文件不存在: {file_path}'}), 404
        
        # 开始导入数据
        logger.info(f"开始导入商品数据: {file_path}, 批次大小: {batch_size}")
        
        result = data_service.import_products_from_file(full_path, batch_size)
        
        if result['status'] == 'completed':
            return jsonify({'success': True, 'data': result, 'message': '商品数据导入完成'})
        else:
            return jsonify({'success': False, 'error': f'商品数据导入失败: {result.get("error", "未知错误")}'}), 500
            
    except Exception as e:
        logger.error(f"导入商品数据API错误: {e}")
        return jsonify({'success': False, 'error': f'导入商品数据失败: {str(e)}'}), 500


@data_bp.route('/import-progress', methods=['GET'])
@cross_origin()
def get_import_progress():
    """
    获取导入进度信息
    GET /api/v1/data/import-progress
    """
    try:
        progress = data_service.get_import_progress()
        return jsonify({'success': True, 'data': progress, 'message': '获取导入进度成功'})
        
    except Exception as e:
        logger.error(f"获取导入进度API错误: {e}")
        return jsonify({'success': False, 'error': f'获取导入进度失败: {str(e)}'}), 500


@data_bp.route('/statistics', methods=['GET'])
@cross_origin()
def get_statistics():
    """
    获取商品数据统计信息
    GET /api/v1/data/statistics
    """
    try:
        stats = data_service.get_product_statistics()
        return jsonify({'success': True, 'data': stats, 'message': '获取统计信息成功'})
        
    except Exception as e:
        logger.error(f"获取统计信息API错误: {e}")
        return jsonify({'success': False, 'error': f'获取统计信息失败: {str(e)}'}), 500


@data_bp.route('/clear', methods=['POST'])
@cross_origin()
def clear_data():
    """
    清空所有商品数据
    POST /api/v1/data/clear
    """
    try:
        # 获取确认参数
        data = request.get_json() or {}
        confirm = data.get('confirm', False)
        
        if not confirm:
            return jsonify({'success': False, 'error': '请确认是否要清空所有数据'}), 400
        
        # 清空数据
        success = data_service.clear_all_data()
        
        if success:
            return jsonify({'success': True, 'data': {'cleared': True}, 'message': '数据清空成功'})
        else:
            return jsonify({'success': False, 'error': '数据清空失败'}), 500
            
    except Exception as e:
        logger.error(f"清空数据API错误: {e}")
        return jsonify({'success': False, 'error': f'清空数据失败: {str(e)}'}), 500


@data_bp.route('/test-segmentation', methods=['POST'])
@cross_origin()
def test_segmentation():
    """
    测试分词功能
    POST /api/v1/data/test-segmentation
    """
    try:
        data = request.get_json() or {}
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': '请输入要分词的文本'}), 400
        
        # 测试分词
        tags = data_service.extract_tags_from_title(text)
        
        result = {
            'original_text': text,
            'tags': tags,
            'tag_count': len(tags)
        }
        
        return jsonify({'success': True, 'data': result, 'message': '分词测试完成'})
        
    except Exception as e:
        logger.error(f"分词测试API错误: {e}")
        return jsonify({'success': False, 'error': f'分词测试失败: {str(e)}'}), 500


@data_bp.route('/test-category', methods=['POST'])
@cross_origin()
def test_category_detection():
    """
    测试分类检测功能
    POST /api/v1/data/test-category
    """
    try:
        data = request.get_json() or {}
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': '请输入要检测分类的文本'}), 400
        
        # 提取标签
        tags = data_service.extract_tags_from_title(text)
        
        # 检测分类
        category_id = data_service.determine_category(text, tags)
        
        result = {
            'original_text': text,
            'tags': tags,
            'detected_category_id': category_id,
            'category_name': data_service.categories.get(category_id, {}).get('name', '未知分类') if category_id else '未检测到分类'
        }
        
        return jsonify({'success': True, 'data': result, 'message': '分类检测测试完成'})
        
    except Exception as e:
        logger.error(f"分类检测测试API错误: {e}")
        return jsonify({'success': False, 'error': f'分类检测测试失败: {str(e)}'}), 500


@data_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """
    健康检查接口
    GET /api/v1/data/health
    """
    try:
        # 检查服务状态
        progress = data_service.get_import_progress()
        
        health_status = {
            'status': 'healthy',
            'service': 'data_processing',
            'total_products': progress.get('total_products', 0),
            'total_tags': progress.get('total_tags', 0)
        }
        
        return jsonify({'success': True, 'data': health_status, 'message': '服务状态正常'})
        
    except Exception as e:
        logger.error(f"健康检查API错误: {e}")
        return jsonify({'success': False, 'error': f'服务状态异常: {str(e)}'}), 500
