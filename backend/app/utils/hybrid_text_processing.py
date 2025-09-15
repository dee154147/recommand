"""
混合分词策略模块
结合jieba智能分词和词向量模型验证，提供更准确的分词结果
"""

import jieba
import jieba.posseg as pseg
from typing import List, Set, Optional
import logging

logger = logging.getLogger(__name__)


class HybridVectorTextProcessor:
    """混合向量文本处理器"""
    
    def __init__(self, word_vectors):
        """
        初始化混合分词器
        
        Args:
            word_vectors: 词向量模型对象
        """
        self.word_vectors = word_vectors
        self.vocab_set = set(word_vectors.index_to_key)
        
        # 预定义商品相关词汇
        self.product_vocab = self._load_product_vocab()
        
        logger.info(f"混合分词器初始化完成，词汇量: {len(self.vocab_set)}")
    
    def _load_product_vocab(self) -> Set[str]:
        """加载商品相关词汇"""
        product_keywords = {
            # 餐具类
            '碗具', '餐具', '厨具', '茶具', '咖啡具', '酒具',
            '碗', '盘', '杯', '勺', '筷', '刀', '叉', '碟',
            
            # 材质类
            '陶瓷', '玻璃', '不锈钢', '塑料', '木质', '竹制',
            '铁制', '铜制', '银制', '金制', '钛制',
            
            # 功能类
            '厨房', '餐厅', '客厅', '卧室', '浴室', '书房',
            '办公', '学习', '娱乐', '运动', '健身',
            
            # 品牌类
            '美的', '海尔', '格力', '小米', '华为', '苹果',
            '三星', '索尼', '松下', '飞利浦', '西门子',
            
            # 其他商品类
            '家电', '数码', '手机', '电脑', '平板', '耳机',
            '音响', '相机', '手表', '包包', '服装', '鞋子'
        }
        
        # 只保留在词向量模型中的词汇
        valid_vocab = {word for word in product_keywords if word in self.vocab_set}
        logger.info(f"加载商品词汇: {len(valid_vocab)} 个")
        
        return valid_vocab
    
    def segment_text(self, text: str) -> List[str]:
        """
        混合分词策略
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 分词结果列表
        """
        if not text:
            return []
        
        logger.info(f"开始混合分词: '{text}'")
        
        # 步骤1: 优先检查整体词
        if text in self.vocab_set:
            logger.info(f"整体词匹配: '{text}'")
            return [text]
        
        # 步骤2: jieba分词
        jieba_words = self._jieba_segment(text)
        logger.info(f"jieba分词结果: {jieba_words}")
        
        # 步骤3: 词向量模型验证
        valid_words = self._validate_words(jieba_words)
        
        # 步骤4: 如果验证结果不理想，尝试降级分词
        if len(valid_words) == 0:
            valid_words = self._fallback_segmentation(text)
        
        # 步骤5: 如果还是没结果，尝试单字匹配
        if len(valid_words) == 0:
            valid_words = self._single_char_fallback(text)
        
        logger.info(f"最终分词结果: {valid_words}")
        return valid_words
    
    def _jieba_segment(self, text: str) -> List[str]:
        """jieba分词"""
        try:
            # 使用词性标注分词
            words = pseg.cut(text)
            meaningful_words = []
            
            for word, flag in words:
                if self._is_meaningful_word(word, flag):
                    meaningful_words.append(word)
            
            return meaningful_words
            
        except Exception as e:
            logger.error(f"jieba分词失败: {e}")
            return []
    
    def _is_meaningful_word(self, word: str, flag: str = None) -> bool:
        """判断词汇是否有意义"""
        # 停用词检查
        stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '个', '们', '中', '来', '用', '年', '月', '日', '时', '分', '秒'
        }
        
        if word in stop_words:
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
                'q',      # 量词（如：碗、杯、个等）
                'eng'     # 英文
            }
            return flag in meaningful_pos
        
        # 对于没有词性标注的词，长度至少为2
        if len(word) < 2:
            return False
        
        return True
    
    def _validate_words(self, words: List[str]) -> List[str]:
        """验证词汇是否在词向量模型中"""
        valid_words = []
        
        for word in words:
            if word in self.vocab_set:
                valid_words.append(word)
                logger.debug(f"✓ '{word}' 在词向量模型中")
            else:
                logger.debug(f"✗ '{word}' 不在词向量模型中")
        
        return valid_words
    
    def _fallback_segmentation(self, text: str) -> List[str]:
        """降级分词：尝试子词组合"""
        words = []
        
        # 尝试所有可能的子词组合
        for i in range(len(text)):
            for j in range(i+1, len(text)+1):
                subword = text[i:j]
                if subword in self.vocab_set and len(subword) >= 2:
                    words.append(subword)
                    logger.debug(f"降级分词找到: '{subword}'")
                    break
        
        return words
    
    def _single_char_fallback(self, text: str) -> List[str]:
        """单字降级：保留在词向量模型中的单字"""
        words = []
        
        for char in text:
            if char in self.vocab_set:
                words.append(char)
                logger.debug(f"单字匹配: '{char}'")
        
        return words
    
    def get_vocab_stats(self) -> dict:
        """获取词汇统计信息"""
        return {
            'total_vocab_size': len(self.vocab_set),
            'product_vocab_size': len(self.product_vocab),
            'product_vocab': list(self.product_vocab)
        }
