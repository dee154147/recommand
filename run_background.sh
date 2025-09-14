#!/bin/bash

# 推荐系统后台运行管理脚本

echo "🚀 推荐系统后台运行管理"
echo "========================"

# 检查是否已经在运行
if lsof -i :5001 > /dev/null 2>&1 && lsof -i :3000 > /dev/null 2>&1; then
    echo "✅ 系统已在后台运行"
    echo ""
    echo "🌐 访问地址:"
    echo "   前端界面: http://localhost:3000"
    echo "   后端API: http://localhost:5001"
    echo ""
    echo "🛠️  管理命令:"
    echo "   查看状态: ./check_status.sh"
    echo "   查看日志: tail -f backend/backend.log"
    echo "   查看日志: tail -f frontend/frontend.log"
    echo "   停止服务: ./stop.sh"
    exit 0
fi

echo "📦 启动后端服务..."
cd backend
nohup python3 run.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   后端进程ID: $BACKEND_PID"

echo "🎨 启动前端服务..."
cd ../frontend
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   前端进程ID: $FRONTEND_PID"

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 8

# 检查服务状态
echo ""
echo "🔍 检查服务状态..."

if lsof -i :5001 > /dev/null 2>&1; then
    echo "✅ 后端服务启动成功 (端口 5001)"
else
    echo "❌ 后端服务启动失败"
fi

if lsof -i :3000 > /dev/null 2>&1; then
    echo "✅ 前端服务启动成功 (端口 3000)"
else
    echo "❌ 前端服务启动失败"
fi

echo ""
echo "🎉 系统后台启动完成！"
echo ""
echo "🌐 访问地址:"
echo "   前端界面: http://localhost:3000"
echo "   后端API: http://localhost:5001"
echo "   健康检查: http://localhost:5001/health"
echo ""
echo "🛠️  管理命令:"
echo "   查看状态: ./check_status.sh"
echo "   查看后端日志: tail -f backend/backend.log"
echo "   查看前端日志: tail -f frontend/frontend.log"
echo "   停止服务: ./stop.sh"
echo ""
echo "📋 进程信息:"
echo "   后端进程ID: $BACKEND_PID"
echo "   前端进程ID: $FRONTEND_PID"
echo ""
echo "💡 提示: 系统现在在后台运行，您可以关闭终端窗口"
