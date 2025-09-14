#!/bin/bash

echo "🚀 简化启动推荐系统"
echo "==================="

# 清理所有相关进程
echo "🧹 清理旧进程..."
pkill -f "python3 run.py" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
sleep 2

# 启动后端
echo "📦 启动后端服务..."
cd backend
python3 run.py &
BACKEND_PID=$!
echo "   后端进程ID: $BACKEND_PID"

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "   前端进程ID: $FRONTEND_PID"

# 等待前端启动
sleep 5

echo ""
echo "✅ 服务启动完成"
echo ""
echo "🌐 访问地址:"
echo "   前端: http://127.0.0.1:3000"
echo "   后端: http://127.0.0.1:5001"
echo "   健康检查: http://127.0.0.1:5001/health"
echo ""
echo "📋 进程信息:"
echo "   后端: $BACKEND_PID"
echo "   前端: $FRONTEND_PID"
echo ""
echo "🛑 停止服务: Ctrl+C 或运行 ./stop.sh"
