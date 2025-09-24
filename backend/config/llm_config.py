# -*- coding: utf-8 -*-
"""
LLM配置模块
用于配置DeepSeek API
"""

import os
from typing import Dict, Any

class LLMConfig:
    """LLM配置类"""
    
    def __init__(self):
        # DeepSeek API配置
        self.api_key = "sk-f9f9946cdbc745a5b6d04ede321f8a05"
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        
        # 模型配置
        self.models = {
            "deepseek_chat": {
                "model_name": "deepseek-chat",  # DeepSeek-V3.1-Terminus 非思考模式
                "description": "DeepSeek对话模型，适合一般任务"
            },
            "deepseek_reasoner": {
                "model_name": "deepseek-reasoner",  # DeepSeek-V3.1-Terminus 思考模式
                "description": "DeepSeek推理模型，适合复杂推理任务"
            }
        }
        
        # 默认使用的模型
        self.default_model = "deepseek_chat"
        
        # API请求配置
        self.request_config = {
            "timeout": 30,  # 请求超时时间（秒）
            "max_retries": 3,  # 最大重试次数
            "retry_delay": 1,  # 重试延迟（秒）
            "stream": False,  # 是否使用流式响应
            "temperature": 0.7,  # 温度参数，控制随机性
            "max_tokens": 1000,  # 最大token数
        }
        
        # 标签生成专用配置
        self.tag_generation_config = {
            "model": "deepseek_chat",  # 使用对话模型生成标签
            "system_prompt": """你是一个专业的商品标签生成助手。请根据用户提供的商品描述，生成5个准确、相关的关键词标签。

要求：
1. 生成5个中文关键词标签
2. 标签应该准确反映商品的核心特征、功能、用途、目标用户等
3. 标签长度控制在2-6个字
4. 标签应该具有商业价值，便于商品分类和推荐
5. 只返回标签内容，用逗号分隔，不要添加其他说明

示例：
输入：这是一款高端商务笔记本电脑，采用英特尔i7处理器，16GB内存，512GB SSD存储，14英寸4K显示屏，支持触控功能，适合商务人士办公使用
输出：商务办公,高效便捷,品质保证,专业设计,用户友好""",
            "temperature": 0.3,  # 降低随机性，确保标签准确性
            "max_tokens": 200,   # 标签生成不需要太多token
        }

    def get_model_config(self, model_name: str = None) -> Dict[str, Any]:
        """获取模型配置"""
        if model_name is None:
            model_name = self.default_model
        
        if model_name not in self.models:
            raise ValueError(f"模型 {model_name} 不存在")
        
        return self.models[model_name]

    def get_request_headers(self) -> Dict[str, str]:
        """获取API请求头"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_tag_generation_prompt(self, product_description: str) -> str:
        """获取标签生成的提示词"""
        return f"""请根据以下商品描述，生成5个准确、相关的关键词标签：

商品描述：{product_description}

要求：
1. 生成5个中文关键词标签
2. 标签应该准确反映商品的核心特征、功能、用途、目标用户等
3. 标签长度控制在2-6个字
4. 标签应该具有商业价值，便于商品分类和推荐
5. 只返回标签内容，用逗号分隔，不要添加其他说明

标签："""

# 创建全局配置实例
llm_config = LLMConfig()