#!/bin/bash

# 推荐系统停止脚本
echo "🛑 停止推荐系统服务..."

# 停止Flask后端服务
echo "📦 停止Flask后端服务..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || echo "后端服务未运行"

# 停止Vue前端服务
echo "🎨 停止Vue前端服务..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || echo "前端服务未运行"

# 停止所有相关Python进程
echo "🐍 停止Python进程..."
pkill -f "python3 run.py" 2>/dev/null || echo "Python进程未运行"

# 停止所有相关Node进程
echo "📦 停止Node进程..."
pkill -f "npm run dev" 2>/dev/null || echo "Node进程未运行"

echo "✅ 所有服务已停止"
