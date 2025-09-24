#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统状态检查脚本
检查前后端服务是否正常运行
"""

import requests
import time
import subprocess
import sys

def check_backend_status():
    """检查后端服务状态"""
    try:
        # 检查基础API
        response = requests.get('http://localhost:5004/api/products', timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务 (端口5004): 正常运行")
            
            # 检查LLM API
            llm_response = requests.get('http://localhost:5004/api/v1/llm/health', timeout=5)
            if llm_response.status_code == 200:
                print("✅ LLM API: 正常运行")
                return True
            else:
                print("⚠️  LLM API: 异常")
                return False
        else:
            print("❌ 后端服务 (端口5004): 异常")
            return False
    except Exception as e:
        print(f"❌ 后端服务 (端口5004): 无法连接 - {str(e)}")
        return False

def check_frontend_status():
    """检查前端服务状态"""
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务 (端口3000): 正常运行")
            return True
    except:
        pass
    
    try:
        response = requests.get('http://localhost:3001', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务 (端口3001): 正常运行")
            return True
    except:
        pass
    
    print("❌ 前端服务: 无法连接 (尝试了端口3000和3001)")
    return False

def check_processes():
    """检查进程状态"""
    try:
        # 检查Python后端进程
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        python_processes = [line for line in result.stdout.split('\n') if 'python.*run.py' in line or 'run.py' in line]
        if python_processes:
            print("✅ 后端进程: 正在运行")
        else:
            print("⚠️  后端进程: 未找到")
        
        # 检查npm前端进程
        npm_processes = [line for line in result.stdout.split('\n') if 'npm.*dev' in line or 'vite' in line]
        if npm_processes:
            print("✅ 前端进程: 正在运行")
        else:
            print("⚠️  前端进程: 未找到")
            
    except Exception as e:
        print(f"⚠️  进程检查失败: {str(e)}")

def test_deepseek_api():
    """测试DeepSeek API"""
    try:
        response = requests.get('http://localhost:5004/api/v1/llm/test-connection', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ DeepSeek API: 连接成功")
                return True
            else:
                print(f"⚠️  DeepSeek API: 连接失败 - {data.get('message', '未知错误')}")
                return False
        else:
            print(f"❌ DeepSeek API: HTTP错误 {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ DeepSeek API: 测试失败 - {str(e)}")
        return False

def main():
    """主函数"""
    print("🔍 系统状态检查")
    print("=" * 50)
    
    # 检查进程
    check_processes()
    print()
    
    # 检查后端服务
    backend_ok = check_backend_status()
    print()
    
    # 检查前端服务
    frontend_ok = check_frontend_status()
    print()
    
    # 测试DeepSeek API
    deepseek_ok = test_deepseek_api()
    print()
    
    # 总结
    print("=" * 50)
    print("📊 系统状态总结:")
    
    if backend_ok and frontend_ok and deepseek_ok:
        print("🎉 系统完全正常运行！")
        print("\n🌐 访问地址:")
        print("   前端界面: http://localhost:3000 或 http://localhost:3001")
        print("   后端API: http://localhost:5004")
        print("\n🔧 主要功能:")
        print("   ✅ 商品管理模块")
        print("   ✅ DeepSeek LLM标签生成")
        print("   ✅ 相似商品检索")
        print("   ✅ 商业分析报告")
        return 0
    else:
        print("⚠️  系统部分功能异常，需要检查:")
        if not backend_ok:
            print("   - 后端服务异常")
        if not frontend_ok:
            print("   - 前端服务异常")
        if not deepseek_ok:
            print("   - DeepSeek API异常")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
