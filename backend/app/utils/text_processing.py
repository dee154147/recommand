"""
文本处理工具模块
提供中文文本处理、分词、清洗等功能
"""

import re
import jieba
import jieba.posseg as pseg
from typing import List, Dict, Set
import logging

logger = logging.getLogger(__name__)


class TextProcessor:
    """文本处理器类"""
    
    def __init__(self):
        """初始化文本处理器"""
        self.stop_words = self._load_stop_words()
        self._init_jieba()
    
    def _init_jieba(self):
        """初始化jieba分词器"""
        try:
            # 加载用户自定义词典（如果有的话）
            # jieba.load_userdict('path/to/userdict.txt')
            
            # 设置jieba的日志级别
            jieba.setLogLevel(logging.INFO)
            
            logger.info("jieba分词器初始化完成")
        except Exception as e:
            logger.error(f"初始化jieba分词器失败: {e}")
    
    def _load_stop_words(self) -> Set[str]:
        """加载停用词表"""
        stop_words = {
            # 常用停用词
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '个', '们', '中', '来', '用', '年', '月', '日', '时', '分', '秒',
            
            # 商品相关停用词
            '元', '块', '钱', '包', '件', '个', '只', '双', '条', '套', '台', '部', '张', '本', '支', '瓶', '盒', '袋', '箱', '包', '斤', '克', '升', '米', '厘米', '毫米', '寸', '尺', '码', '号', '色', '款', '型', '版', '式', '样', '类', '种', '品', '牌', '名', '称', '价', '格',
            
            # 营销词汇
            '特', '价', '优', '惠', '折', '扣', '免', '费', '包', '邮', '正', '品', '原', '装', '进', '口', '国', '产', '新', '款', '老', '款', '热', '卖', '爆', '款', '限', '量', '特', '供', '专', '供', '独', '家', '首', '发', '抢', '购', '秒', '杀', '团', '购', '拼', '团', '砍', '价',
            
            # 操作词汇
            '分', '享', '收', '藏', '加', '购', '下', '单', '支', '付', '发', '货', '收', '货', '评', '价', '好', '评', '差', '评', '中', '评', '追', '评', '晒', '图', '退', '货', '换', '货', '售', '后', '服', '务', '客', '服', '联', '系', '咨', '询', '问', '答', '帮', '助',
            
            # 描述词汇
            '说', '明', '介', '绍', '详', '情', '规', '格', '参', '数', '功', '能', '特', '点', '优', '势', '用', '法', '注', '意', '事', '项', '保', '修', '维', '修', '安', '装', '使', '用', '方', '法', '操', '作', '步', '骤', '禁', '忌', '适', '用', '人', '群', '场', '合', '环', '境', '条', '件',
            
            # 技术参数
            '温', '度', '湿', '度', '压', '力', '电', '压', '电', '流', '功', '率', '频', '率', '波', '长', '速', '度', '加', '速', '度', '重', '力', '密', '度', '硬', '度', '韧', '性', '弹', '性', '塑', '性', '粘', '性', '润', '滑', '性', '导', '热', '性', '导', '电', '性', '绝', '缘', '性', '透', '明', '度', '不', '透', '明', '度', '反', '光', '性', '吸', '光', '性',
            
            # 性能词汇
            '防', '水', '性', '防', '火', '性', '防', '腐', '性', '耐', '磨', '性', '耐', '高', '温', '性', '耐', '低', '温', '性', '耐', '压', '性', '耐', '拉', '性', '耐', '弯', '性', '耐', '扭', '性', '耐', '冲', '击', '性', '耐', '疲', '劳', '性', '耐', '老', '化', '性', '耐', '紫', '外', '线', '性', '耐', '酸', '性', '耐', '碱', '性', '耐', '盐', '性', '耐', '油', '性', '耐', '溶', '剂', '性',
            
            # 环保词汇
            '环', '保', '性', '可', '回', '收', '性', '可', '降', '解', '性', '无', '毒', '性', '无', '害', '性', '安', '全', '性', '可', '靠', '性', '稳', '定', '性', '一', '致', '性', '均', '匀', '性', '精', '度', '准', '确', '性', '灵', '敏', '度', '响', '应', '时', '间', '恢', '复', '时', '间', '寿', '命', '使', '用', '次', '数', '保', '质', '期', '有', '效', '期',
            
            # 生产信息
            '生', '产', '日', '期', '生', '产', '批', '号', '生', '产', '厂', '家', '生', '产', '地', '址', '联', '系', '电', '话', '传', '真', '邮', '箱', '网', '站', '微', '信', '微', '博', 'Q', 'Q',
            
            # 平台名称
            '阿', '里', '巴', '巴', '淘', '宝', '天', '猫', '京', '东', '苏', '宁', '国', '美', '当', '当', '亚', '马', '逊', '唯', '品', '会', '聚', '美', '优', '品', '美', '团', '大', '众', '点', '评', '携', '程', '去', '哪', '儿', '飞', '猪', '蚂', '蚁', '金', '服',
            
            # 支付方式
            '支', '付', '宝', '微', '信', '支', '付', '银', '联', '信', '用', '卡', '借', '记', '卡', '现', '金', '支', '付', '货', '到', '付', '款', '分', '期', '付', '款', '花', '呗', '白', '条'
        }
        return stop_words
    
    def clean_text(self, text: str) -> str:
        """
        清洗文本
        移除特殊字符、多余空格等
        """
        if not text:
            return ""
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除特殊字符，保留中文、英文、数字、空格
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text)
        
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)
        
        # 去除首尾空格
        text = text.strip()
        
        return text
    
    def segment_text(self, text: str, use_pos: bool = True) -> List[str]:
        """
        对文本进行分词
        """
        if not text:
            return []
        
        try:
            if use_pos:
                # 使用词性标注
                words = pseg.cut(text)
                # 过滤词性，只保留有意义的词
                meaningful_words = []
                for word, flag in words:
                    if self._is_meaningful_word(word, flag):
                        meaningful_words.append(word)
                return meaningful_words
            else:
                # 简单分词
                words = jieba.cut(text)
                return [word for word in words if self._is_meaningful_word(word)]
                
        except Exception as e:
            logger.error(f"分词失败: {e}, 文本: {text}")
            return []
    
    def _is_meaningful_word(self, word: str, flag: str = None) -> bool:
        """
        判断词汇是否有意义
        """
        # 长度检查
        if len(word) < 2:
            return False
        
        # 停用词检查
        if word in self.stop_words:
            return False
        
        # 纯数字检查
        if word.isdigit():
            return False
        
        # 纯英文检查（单个字母）
        if len(word) == 1 and word.isalpha():
            return False
        
        # 词性检查（如果提供了词性）
        if flag:
            meaningful_pos = {
                'n',      # 名词
                'nr',     # 人名
                'ns',     # 地名
                'nt',     # 机构团体
                'nw',     # 作品名
                'nz',     # 其他专名
                'v',      # 动词
                'vn',     # 名动词
                'a',      # 形容词
                'ad',     # 副形词
                'an',     # 名形词
                'eng'     # 英文
            }
            return flag in meaningful_pos
        
        return True
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """
        提取关键词
        """
        if not text:
            return []
        
        # 清洗文本
        clean_text = self.clean_text(text)
        
        # 分词
        words = self.segment_text(clean_text)
        
        # 统计词频
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 按频率排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # 返回前top_k个关键词
        return [word for word, freq in sorted_words[:top_k]]
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度（基于词汇重叠）
        """
        if not text1 or not text2:
            return 0.0
        
        # 提取关键词
        keywords1 = set(self.extract_keywords(text1))
        keywords2 = set(self.extract_keywords(text2))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        # 计算Jaccard相似度
        intersection = len(keywords1 & keywords2)
        union = len(keywords1 | keywords2)
        
        return intersection / union if union > 0 else 0.0
    
    def normalize_text(self, text: str) -> str:
        """
        文本标准化
        统一大小写、去除多余空格等
        """
        if not text:
            return ""
        
        # 转换为小写（英文部分）
        text = text.lower()
        
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)
        
        # 去除首尾空格
        text = text.strip()
        
        return text
    
    def get_text_statistics(self, text: str) -> Dict:
        """
        获取文本统计信息
        """
        if not text:
            return {
                'length': 0,
                'word_count': 0,
                'keyword_count': 0,
                'unique_words': 0
            }
        
        # 清洗文本
        clean_text = self.clean_text(text)
        
        # 分词
        words = self.segment_text(clean_text)
        
        # 统计信息
        stats = {
            'length': len(text),
            'clean_length': len(clean_text),
            'word_count': len(words),
            'unique_words': len(set(words)),
            'keyword_count': len(self.extract_keywords(text))
        }
        
        return stats
