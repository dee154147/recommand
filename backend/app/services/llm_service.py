# -*- coding: utf-8 -*-
"""
LLM服务模块
用于调用DeepSeek API
"""

import requests
import json
import logging
import time
from typing import List, Dict, Any, Optional
from config.llm_config import llm_config

logger = logging.getLogger(__name__)

class LLMService:
    """LLM服务类"""
    
    def __init__(self):
        self.config = llm_config
        self.session = requests.Session()
        
    def _make_request(self, data: Dict[str, Any], max_retries: int = None) -> Dict[str, Any]:
        """发送API请求，带重试机制"""
        if max_retries is None:
            max_retries = self.config.request_config["max_retries"]
            
        for attempt in range(max_retries + 1):
            try:
                # DeepSeek API使用配置的完整URL
                url = self.config.base_url
                
                response = self.session.post(
                    url,
                    headers=self.config.get_request_headers(),
                    json=data,
                    timeout=self.config.request_config["timeout"]
                )
                
                response.raise_for_status()
                result = response.json()
                
                logger.info(f"DeepSeek API请求成功，尝试次数: {attempt + 1}")
                return result
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"DeepSeek API请求失败，尝试次数: {attempt + 1}, 错误: {str(e)}")
                
                if attempt < max_retries:
                    delay = self.config.request_config["retry_delay"] * (2 ** attempt)  # 指数退避
                    time.sleep(delay)
                else:
                    raise Exception(f"DeepSeek API请求失败，已重试{max_retries}次: {str(e)}")
                    
    def generate_tags(self, product_description: str) -> List[str]:
        """
        生成商品标签
        
        Args:
            product_description: 商品描述
            
        Returns:
            List[str]: 生成的标签列表
        """
        try:
            # 获取模型配置
            model_config = self.config.get_model_config(self.config.tag_generation_config["model"])
            
            # 构建请求数据
            data = {
                "model": model_config["model_name"],
                "messages": [
                    {
                        "role": "system",
                        "content": self.config.tag_generation_config["system_prompt"]
                    },
                    {
                        "role": "user",
                        "content": self.config.get_tag_generation_prompt(product_description)
                    }
                ],
                "stream": self.config.tag_generation_config.get("stream", False),
                "temperature": self.config.tag_generation_config.get("temperature", 0.3),
                "max_tokens": self.config.tag_generation_config.get("max_tokens", 200)
            }
            
            logger.info(f"开始生成商品标签，商品描述长度: {len(product_description)}")
            
            # 发送请求
            result = self._make_request(data)
            
            # 解析响应
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"].strip()
                logger.info(f"DeepSeek返回内容: {content}")
                
                # 解析标签
                tags = self._parse_tags(content)
                logger.info(f"解析得到标签: {tags}")
                
                return tags
            else:
                raise Exception("DeepSeek API响应格式错误")
                
        except Exception as e:
            logger.error(f"生成商品标签失败: {str(e)}")
            raise Exception(f"生成商品标签失败: {str(e)}")
    
    def _parse_tags(self, content: str) -> List[str]:
        """
        解析DeepSeek返回的标签内容
        
        Args:
            content: DeepSeek返回的原始内容
            
        Returns:
            List[str]: 解析后的标签列表
        """
        try:
            # 移除可能的额外文本
            content = content.strip()
            
            # 查找标签部分
            if "标签：" in content:
                content = content.split("标签：")[-1].strip()
            
            # 按逗号分割
            tags = [tag.strip() for tag in content.split(",") if tag.strip()]
            
            # 过滤和清理标签
            cleaned_tags = []
            for tag in tags:
                # 移除可能的引号
                tag = tag.strip('"\'（）()【】[]')
                # 移除过长的标签
                if len(tag) <= 10 and len(tag) >= 1:
                    cleaned_tags.append(tag)
            
            # 确保返回5个标签
            if len(cleaned_tags) > 5:
                cleaned_tags = cleaned_tags[:5]
            elif len(cleaned_tags) < 5:
                # 如果标签不足5个，用通用标签补充
                default_tags = ["优质商品", "推荐产品", "热销商品", "精选商品", "品质保证"]
                for default_tag in default_tags:
                    if len(cleaned_tags) < 5 and default_tag not in cleaned_tags:
                        cleaned_tags.append(default_tag)
            
            return cleaned_tags
            
        except Exception as e:
            logger.error(f"解析标签失败: {str(e)}")
            # 返回默认标签
            return ["优质商品", "推荐产品", "热销商品", "精选商品", "品质保证"]
    
    def test_connection(self) -> Dict[str, Any]:
        """
        测试DeepSeek API连接
        
        Returns:
            Dict[str, Any]: 测试结果
        """
        try:
            model_config = self.config.get_model_config()
            
            data = {
                "model": model_config["model_name"],
                "messages": [
                    {
                        "role": "user",
                        "content": "你好，请回复'连接成功'"
                    }
                ],
                "stream": False,
                "temperature": 0.1,
                "max_tokens": 50
            }
            
            result = self._make_request(data)
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "message": "DeepSeek API连接成功",
                    "response": content,
                    "model": model_config["model_name"]
                }
            else:
                return {
                    "success": False,
                    "message": "DeepSeek API响应格式错误"
                }
                
        except Exception as e:
            logger.error(f"DeepSeek API连接测试失败: {str(e)}")
            return {
                "success": False,
                "message": f"DeepSeek API连接失败: {str(e)}"
            }
    
    def health_check(self) -> Dict[str, Any]:
        """
        健康检查
        
        Returns:
            Dict[str, Any]: 健康状态
        """
        try:
            test_result = self.test_connection()
            if test_result["success"]:
                return {
                    "status": "healthy",
                    "service": "DeepSeek LLM",
                    "message": "服务正常"
                }
            else:
                return {
                    "status": "unhealthy",
                    "service": "DeepSeek LLM",
                    "message": test_result["message"]
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "service": "DeepSeek LLM",
                "message": f"健康检查失败: {str(e)}"
            }

# 创建全局服务实例
llm_service = LLMService()