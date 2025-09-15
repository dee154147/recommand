#!/usr/bin/env python3
"""
商品标签提取演示
展示jieba分词和标签提取的详细过程
"""

import sys
import os
sys.path.append('backend')

import jieba
import jieba.posseg as pseg

def demo_tag_extraction():
    """演示标签提取过程"""
    
    print("=" * 80)
    print("商品标签提取详细演示")
    print("=" * 80)
    
    # 示例商品标题
    sample_titles = [
        "经典故事 女装 秋装 热卖 时尚 简约 纯色 棉质 褶皱短裙 半身裙 A 字 群 Q 790",
        "iPhone 15 Pro Max 256GB 深空黑色",
        "Nike Air Max 270 运动鞋 男款 白色",
        "MacBook Pro 14英寸 M3芯片 深空灰色",
        "Sony WH-1000XM5 降噪耳机 无线蓝牙"
    ]
    
    # 停用词表（简化版）
    stop_words = {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '个', '们', '中', '来', '用', '年', '月', '日', '时', '分', '秒',
        '元', '块', '钱', '包', '件', '个', '只', '双', '条', '套', '台', '部', '张', '本', '支', '瓶', '盒', '袋', '箱', '包', '斤', '克', '升', '米', '厘米', '毫米', '寸', '尺', '码', '号', '色', '款', '型', '版', '式', '样', '类', '种', '品', '牌', '名', '称', '价', '格',
        '特', '价', '优', '惠', '折', '扣', '免', '费', '包', '邮', '正', '品', '原', '装', '进', '口', '国', '产', '新', '款', '老', '款', '热', '卖', '爆', '款', '限', '量', '特', '供', '专', '供', '独', '家', '首', '发', '抢', '购', '秒', '杀', '团', '购', '拼', '团', '砍', '价'
    }
    
    # 有意义的词性
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
    
    for i, title in enumerate(sample_titles, 1):
        print(f"\n📝 示例 {i}: {title}")
        print("-" * 60)
        
        # 1. 简单分词
        print("1️⃣ 简单分词结果:")
        simple_words = list(jieba.cut(title))
        print(f"   {simple_words}")
        
        # 2. 词性标注分词
        print("\n2️⃣ 词性标注分词:")
        pos_words = list(pseg.cut(title))
        for word, flag in pos_words:
            print(f"   '{word}' -> {flag}")
        
        # 3. 标签提取过程
        print("\n3️⃣ 标签提取过程:")
        tags = []
        filtered_words = []
        
        for word, flag in pos_words:
            # 检查条件
            length_ok = len(word) > 1
            not_stopword = word not in stop_words
            meaningful_pos_flag = flag in meaningful_pos
            not_digit = not word.isdigit()
            
            print(f"   '{word}' ({flag}): 长度>1:{length_ok}, 非停用词:{not_stopword}, 有意义词性:{meaningful_pos_flag}, 非纯数字:{not_digit}")
            
            if length_ok and not_stopword and meaningful_pos_flag and not_digit:
                tags.append(word)
                filtered_words.append(f"{word}({flag})")
            else:
                print(f"      ❌ 被过滤")
        
        # 4. 最终结果
        print(f"\n4️⃣ 最终提取的标签:")
        print(f"   过滤后的词汇: {filtered_words}")
        print(f"   最终标签: {tags}")
        print(f"   标签数量: {len(tags)}")
        
        print("\n" + "="*60)

def demo_word_frequency():
    """演示词频统计"""
    print("\n" + "=" * 80)
    print("标签词频统计演示")
    print("=" * 80)
    
    # 模拟一些商品标题
    titles = [
        "经典故事 女装 秋装 热卖 时尚 简约 纯色 棉质 褶皱短裙",
        "韩版 女装 时尚 连衣裙 夏季 新款 包邮",
        "男装 休闲 衬衫 商务 正装 白色 棉质",
        "运动鞋 跑步 男款 白色 透气 舒适",
        "手机 苹果 iPhone 15 Pro Max 深空黑色"
    ]
    
    # 统计所有标签
    all_tags = []
    for title in titles:
        words = list(pseg.cut(title))
        for word, flag in words:
            if (len(word) > 1 and 
                word not in {'的', '了', '在', '是', '和', '就', '不', '人', '都', '一', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '个', '们', '中', '来', '用', '年', '月', '日', '时', '分', '秒', '元', '块', '钱', '包', '件', '只', '双', '条', '套', '台', '部', '张', '本', '支', '瓶', '盒', '袋', '箱', '包', '斤', '克', '升', '米', '厘米', '毫米', '寸', '尺', '码', '号', '色', '款', '型', '版', '式', '样', '类', '种', '品', '牌', '名', '称', '价', '格', '特', '价', '优', '惠', '折', '扣', '免', '费', '包', '邮', '正', '品', '原', '装', '进', '口', '国', '产', '新', '款', '老', '款', '热', '卖', '爆', '款', '限', '量', '特', '供', '专', '供', '独', '家', '首', '发', '抢', '购', '秒', '杀', '团', '购', '拼', '团', '砍', '价'} and
                flag in ['n', 'nr', 'ns', 'nt', 'nw', 'nz', 'v', 'vn', 'a', 'ad', 'an', 'eng'] and
                not word.isdigit()):
                all_tags.append(word)
    
    # 统计词频
    from collections import Counter
    tag_counts = Counter(all_tags)
    
    print("标签词频统计:")
    for tag, count in tag_counts.most_common(10):
        print(f"   {tag}: {count}次")

if __name__ == "__main__":
    demo_tag_extraction()
    demo_word_frequency()
