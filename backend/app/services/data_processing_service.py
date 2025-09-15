"""
商品数据处理服务
负责商品数据的导入、分词、标签生成和数据库存储
"""

import os
import json
import jieba
import jieba.posseg as pseg
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime

from ..models import db, Product, Category, ProductTag, TagVector
from ..utils.text_processing import TextProcessor

logger = logging.getLogger(__name__)


class DataProcessingService:
    """商品数据处理服务类"""
    
    def __init__(self):
        """初始化数据处理服务"""
        self.text_processor = TextProcessor()
        self.stop_words = self._load_stop_words()
        self.categories = self._load_categories()
        
    def _load_stop_words(self) -> set:
        """加载停用词表"""
        stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '个', '们', '中', '来', '用', '年', '月', '日', '时', '分', '秒', '元', '块', '钱', '包', '件', '个', '只', '双', '条', '套', '台', '部', '张', '本', '支', '瓶', '盒', '袋', '箱', '包', '斤', '克', '升', '米', '厘米', '毫米', '寸', '尺', '码', '号', '色', '款', '型', '版', '式', '样', '类', '种', '品', '牌', '名', '称', '价', '格', '特', '价', '优', '惠', '折', '扣', '免', '费', '包', '邮', '正', '品', '原', '装', '进', '口', '国', '产', '新', '款', '老', '款', '热', '卖', '爆', '款', '限', '量', '特', '供', '专', '供', '独', '家', '首', '发', '抢', '购', '秒', '杀', '团', '购', '拼', '团', '砍', '价', '分', '享', '收', '藏', '加', '购', '下', '单', '支', '付', '发', '货', '收', '货', '评', '价', '好', '评', '差', '评', '中', '评', '追', '评', '晒', '图', '退', '货', '换', '货', '售', '后', '服', '务', '客', '服', '联', '系', '咨', '询', '问', '答', '帮', '助', '说', '明', '介', '绍', '详', '情', '规', '格', '参', '数', '功', '能', '特', '点', '优', '势', '用', '法', '注', '意', '事', '项', '保', '修', '维', '修', '安', '装', '使', '用', '方', '法', '操', '作', '步', '骤', '注', '意', '事', '项', '禁', '忌', '适', '用', '人', '群', '场', '合', '环', '境', '条', '件', '温', '度', '湿', '度', '压', '力', '电', '压', '电', '流', '功', '率', '频', '率', '波', '长', '速', '度', '加', '速', '度', '重', '力', '密', '度', '硬', '度', '韧', '性', '弹', '性', '塑', '性', '粘', '性', '润', '滑', '性', '导', '热', '性', '导', '电', '性', '绝', '缘', '性', '透', '明', '度', '不', '透', '明', '度', '反', '光', '性', '吸', '光', '性', '防', '水', '性', '防', '火', '性', '防', '腐', '性', '耐', '磨', '性', '耐', '高', '温', '性', '耐', '低', '温', '性', '耐', '压', '性', '耐', '拉', '性', '耐', '弯', '性', '耐', '扭', '性', '耐', '冲', '击', '性', '耐', '疲', '劳', '性', '耐', '老', '化', '性', '耐', '紫', '外', '线', '性', '耐', '酸', '性', '耐', '碱', '性', '耐', '盐', '性', '耐', '油', '性', '耐', '溶', '剂', '性', '环', '保', '性', '可', '回', '收', '性', '可', '降', '解', '性', '无', '毒', '性', '无', '害', '性', '安', '全', '性', '可', '靠', '性', '稳', '定', '性', '一', '致', '性', '均', '匀', '性', '精', '度', '准', '确', '性', '灵', '敏', '度', '响', '应', '时', '间', '恢', '复', '时', '间', '寿', '命', '使', '用', '次', '数', '保', '质', '期', '有', '效', '期', '生', '产', '日', '期', '生', '产', '批', '号', '生', '产', '厂', '家', '生', '产', '地', '址', '联', '系', '电', '话', '传', '真', '邮', '箱', '网', '站', '微', '信', '微', '博', 'Q', 'Q', '阿', '里', '巴', '巴', '淘', '宝', '天', '猫', '京', '东', '苏', '宁', '国', '美', '当', '当', '亚', '马', '逊', '唯', '品', '会', '聚', '美', '优', '品', '美', '团', '大', '众', '点', '评', '携', '程', '去', '哪', '儿', '飞', '猪', '蚂', '蚁', '金', '服', '支', '付', '宝', '微', '信', '支', '付', '银', '联', '信', '用', '卡', '借', '记', '卡', '现', '金', '支', '付', '货', '到', '付', '款', '分', '期', '付', '款', '花', '呗', '白', '条', '京', '东', '白', '条', '苏', '宁', '白', '条', '国', '美', '白', '条', '当', '当', '白', '条', '亚', '马', '逊', '白', '条', '唯', '品', '会', '白', '条', '聚', '美', '优', '品', '白', '条', '美', '团', '白', '条', '大', '众', '点', '评', '白', '条', '携', '程', '白', '条', '去', '哪', '儿', '白', '条', '飞', '猪', '白', '条', '蚂', '蚁', '金', '服', '白', '条', '支', '付', '宝', '白', '条', '微', '信', '支', '付', '白', '条', '银', '联', '白', '条', '信', '用', '卡', '白', '条', '借', '记', '卡', '白', '条', '现', '金', '白', '条', '货', '到', '付', '款', '白', '条', '分', '期', '付', '款', '白', '条'
        }
        return stop_words
    
    def _load_categories(self) -> Dict[int, Dict]:
        """加载商品分类信息"""
        try:
            categories_file = os.path.join(os.path.dirname(__file__), '../../../data/productType.json')
            with open(categories_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {cat['id']: cat for cat in data['categories']}
        except Exception as e:
            logger.error(f"加载分类信息失败: {e}")
            return {}
    
    def parse_product_data(self, line: str) -> Optional[Dict]:
        """
        解析商品数据行
        格式: 商品ID商品标题图片链接分类ID品牌ID店铺ID (无分隔符)
        """
        try:
            line = line.strip()
            if len(line) < 50:  # 数据太短，跳过
                return None
            
            # 尝试提取商品ID（通常是开头的数字）
            import re
            id_match = re.match(r'^(\d+)', line)
            if not id_match:
                return None
            
            product_id = int(id_match.group(1))
            
            # 提取图片URL（http开头）
            url_match = re.search(r'(http://[^\s]+)', line)
            image_url = url_match.group(1) if url_match else ""
            
            # 提取分类ID（数字-数字格式）
            category_match = re.search(r'(\d+)-(\d+)', line)
            category_id = int(category_match.group(1)) if category_match else None
            
            # 提取品牌ID和店铺ID（字母数字组合）
            brand_match = re.search(r'([a-zA-Z]\d+)', line)
            brand_id = brand_match.group(1) if brand_match else ""
            
            shop_match = re.search(r'(s\d+)', line)
            shop_id = shop_match.group(1) if shop_match else ""
            
            # 提取商品标题（在ID和URL之间的部分）
            title_start = len(str(product_id))
            title_end = line.find(image_url) if image_url else len(line)
            title = line[title_start:title_end].strip()
            
            # 清理标题中的多余空格
            title = re.sub(r'\s+', ' ', title).strip()
            
            if not title:
                return None
            
            return {
                'id': product_id,
                'title': title,
                'image_url': image_url,
                'category_id': category_id,
                'brand_id': brand_id,
                'shop_id': shop_id
            }
        except Exception as e:
            logger.error(f"解析商品数据失败: {e}, 数据: {line}")
            return None
    
    def extract_tags_from_title(self, title: str) -> List[str]:
        """
        从商品标题中提取标签
        使用jieba分词，过滤停用词和短词
        """
        try:
            # 使用jieba进行分词和词性标注
            words = pseg.cut(title)
            
            tags = []
            for word, flag in words:
                # 过滤条件：
                # 1. 长度大于1
                # 2. 不在停用词表中
                # 3. 词性为名词、动词、形容词等有意义词性
                # 4. 不是纯数字
                if (len(word) > 1 and 
                    word not in self.stop_words and
                    flag in ['n', 'nr', 'ns', 'nt', 'nw', 'nz', 'v', 'vn', 'a', 'ad', 'an'] and
                    not word.isdigit()):
                    tags.append(word)
            
            # 去重并限制标签数量
            unique_tags = list(set(tags))
            return unique_tags[:10]  # 最多保留10个标签
            
        except Exception as e:
            logger.error(f"提取标签失败: {e}, 标题: {title}")
            return []
    
    def determine_category(self, title: str, tags: List[str]) -> Optional[int]:
        """
        根据商品标签与类别关键词的相似度确定商品分类
        使用Jaccard相似度和关键词匹配相结合的方法
        """
        try:
            if not tags:
                return None
            
            best_match = None
            best_score = 0
            
            for cat_id, category in self.categories.items():
                keywords = category.get('keywords', [])
                if not keywords:
                    continue
                
                # 方法1: 直接关键词匹配（权重较高）
                direct_match_score = 0
                matched_keywords = []
                for keyword in keywords:
                    for tag in tags:
                        if keyword == tag:  # 完全匹配
                            direct_match_score += 3  # 完全匹配权重为3
                            matched_keywords.append(keyword)
                            break
                        elif keyword in tag or tag in keyword:  # 包含匹配
                            direct_match_score += 2  # 包含匹配权重为2
                            matched_keywords.append(keyword)
                            break
                
                # 方法2: Jaccard相似度计算
                tag_set = set(tags)
                keyword_set = set(keywords)
                
                # 计算交集和并集
                intersection = tag_set & keyword_set
                union = tag_set | keyword_set
                
                jaccard_score = len(intersection) / len(union) if union else 0
                
                # 方法3: 部分匹配（包含关系）
                partial_match_score = 0
                for keyword in keywords:
                    for tag in tags:
                        # 检查是否包含关系
                        if len(keyword) >= 2 and len(tag) >= 2:
                            if keyword in tag or tag in keyword:
                                partial_match_score += 1
                                break
                
                # 特殊规则处理
                special_bonus = 0
                
                # 规则1: 运动鞋优先匹配运动户外类
                if cat_id == 3 and '运动鞋' in tags:  # 运动户外类
                    special_bonus += 2
                
                # 规则2: 童装优先匹配童装类
                if cat_id == 5 and any(tag in ['童装', '儿童', '宝宝', '婴儿', '女童', '男童'] for tag in tags):
                    special_bonus += 2
                
                # 规则3: 数码产品优先匹配
                if cat_id == 4 and any(tag in ['iPhone', 'iPad', 'MacBook', '电脑', '笔记本'] for tag in tags):
                    special_bonus += 2
                
                # 规则4: 鞋子类优先匹配
                if cat_id == 13 and any(tag in ['运动鞋', '皮鞋', '高跟鞋', '鞋子'] for tag in tags):
                    special_bonus += 2
                
                # 综合评分
                total_score = direct_match_score + jaccard_score * 3 + partial_match_score * 0.5 + special_bonus
                
                logger.debug(f"分类 {cat_id} ({category.get('name', '')}): "
                           f"直接匹配={direct_match_score}, Jaccard={jaccard_score:.3f}, "
                           f"部分匹配={partial_match_score}, 总分={total_score:.3f}")
                
                if total_score > best_score:
                    best_score = total_score
                    best_match = cat_id
            
            # 设置最低阈值，避免误分类
            if best_score < 0.5:
                logger.debug(f"最高分数 {best_score:.3f} 低于阈值 0.5，不进行分类")
                return None
            
            logger.debug(f"商品分类结果: {best_match}, 分数: {best_score:.3f}")
            return best_match
            
        except Exception as e:
            logger.error(f"分类确定失败: {e}, 标题: {title}, 标签: {tags}")
            return None
    
    def import_products_from_file(self, file_path: str, batch_size: int = 100) -> Dict:
        """
        从文件导入商品数据
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            total_count = 0
            success_count = 0
            error_count = 0
            batch_count = 0
            
            logger.info(f"开始导入商品数据: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                batch_products = []
                
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    
                    # 解析商品数据
                    product_data = self.parse_product_data(line)
                    if not product_data:
                        error_count += 1
                        continue
                    
                    # 提取标签
                    tags = self.extract_tags_from_title(product_data['title'])
                    
                    # 确定分类
                    if not product_data['category_id']:
                        product_data['category_id'] = self.determine_category(
                            product_data['title'], tags
                        )
                    
                    # 添加到批次
                    batch_products.append({
                        'product_data': product_data,
                        'tags': tags
                    })
                    
                    total_count += 1
                    
                    # 批量处理
                    if len(batch_products) >= batch_size:
                        batch_success = self._save_batch_to_database(batch_products)
                        success_count += batch_success
                        error_count += (len(batch_products) - batch_success)
                        batch_count += 1
                        
                        logger.info(f"已处理批次 {batch_count}, 成功: {batch_success}, 总数: {total_count}")
                        batch_products = []
                
                # 处理最后一批
                if batch_products:
                    batch_success = self._save_batch_to_database(batch_products)
                    success_count += batch_success
                    error_count += (len(batch_products) - batch_success)
                    batch_count += 1
            
            result = {
                'total_count': total_count,
                'success_count': success_count,
                'error_count': error_count,
                'batch_count': batch_count,
                'status': 'completed'
            }
            
            logger.info(f"商品数据导入完成: {result}")
            return result
            
        except Exception as e:
            logger.error(f"导入商品数据失败: {e}")
            return {
                'total_count': 0,
                'success_count': 0,
                'error_count': 0,
                'batch_count': 0,
                'status': 'failed',
                'error': str(e)
            }
    
    def _save_batch_to_database(self, batch_products: List[Dict]) -> int:
        """
        批量保存商品数据到数据库
        """
        success_count = 0
        
        try:
            for item in batch_products:
                product_data = item['product_data']
                tags = item['tags']
                
                # 创建商品记录
                product = Product(
                    id=product_data['id'],
                    name=product_data['title'],
                    description=f"商品ID: {product_data['id']}, 品牌: {product_data['brand_id']}, 店铺: {product_data['shop_id']}",
                    price=None,  # 价格信息在原始数据中不可用
                    category_id=product_data['category_id'],
                    image_url=product_data['image_url'],
                    tags=json.dumps(tags, ensure_ascii=False),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                # 保存商品
                db.session.add(product)
                
                # 保存商品标签
                for tag in tags:
                    product_tag = ProductTag(
                        product_id=product_data['id'],
                        tag=tag,
                        weight=1.0,  # 默认权重
                        created_at=datetime.utcnow()
                    )
                    db.session.add(product_tag)
                
                success_count += 1
            
            # 提交事务
            db.session.commit()
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"保存商品数据到数据库失败: {e}")
            success_count = 0
        except Exception as e:
            db.session.rollback()
            logger.error(f"保存商品数据时发生未知错误: {e}")
            success_count = 0
        
        return success_count
    
    def get_import_progress(self) -> Dict:
        """
        获取导入进度信息
        """
        try:
            # 统计数据库中的商品数量
            total_products = db.session.query(Product).count()
            total_tags = db.session.query(ProductTag).count()
            
            return {
                'total_products': total_products,
                'total_tags': total_tags,
                'status': 'ready'
            }
        except Exception as e:
            logger.error(f"获取导入进度失败: {e}")
            return {
                'total_products': 0,
                'total_tags': 0,
                'status': 'error',
                'error': str(e)
            }
    
    def clear_all_data(self) -> bool:
        """
        清空所有商品数据
        """
        try:
            # 删除所有商品标签
            db.session.query(ProductTag).delete()
            
            # 删除所有商品
            db.session.query(Product).delete()
            
            # 提交事务
            db.session.commit()
            
            logger.info("所有商品数据已清空")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"清空商品数据失败: {e}")
            return False
    
    def get_product_statistics(self) -> Dict:
        """
        获取商品数据统计信息
        """
        try:
            # 商品总数
            total_products = db.session.query(Product).count()
            
            # 标签总数
            total_tags = db.session.query(ProductTag).count()
            
            # 分类统计
            category_stats = db.session.query(
                Product.category_id,
                db.func.count(Product.id).label('count')
            ).group_by(Product.category_id).all()
            
            # 标签统计（前20个最常用标签）
            popular_tags = db.session.query(
                ProductTag.tag,
                db.func.count(ProductTag.id).label('count')
            ).group_by(ProductTag.tag).order_by(
                db.func.count(ProductTag.id).desc()
            ).limit(20).all()
            
            return {
                'total_products': total_products,
                'total_tags': total_tags,
                'category_stats': [
                    {'category_id': cat_id, 'count': count} 
                    for cat_id, count in category_stats
                ],
                'popular_tags': [
                    {'tag': tag, 'count': count} 
                    for tag, count in popular_tags
                ]
            }
            
        except Exception as e:
            logger.error(f"获取商品统计信息失败: {e}")
            return {
                'total_products': 0,
                'total_tags': 0,
                'category_stats': [],
                'popular_tags': []
            }
