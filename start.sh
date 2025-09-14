#!/bin/bash

# 推荐系统启动脚本
echo "🚀 启动推荐系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

# 检查npm环境
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装，请先安装npm"
    exit 1
fi

echo "✅ 环境检查通过"

# 启动后端服务
echo "📦 启动后端服务..."
cd backend

# 检查依赖是否安装
if [ ! -d "venv" ]; then
    echo "📥 安装Python依赖..."
    pip3 install -r requirements.txt
fi

# 启动Flask应用
echo "🌐 启动Flask应用 (端口: 5001)..."
python3 run.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端服务
echo "🎨 启动前端服务..."
cd ../frontend

# 检查前端依赖是否安装
if [ ! -d "node_modules" ]; then
    echo "📥 安装前端依赖..."
    npm install
fi

# 启动Vue应用
echo "🌐 启动Vue应用 (端口: 3000)..."
npm run dev &
FRONTEND_PID=$!

# 等待前端启动
sleep 5

echo ""
echo "🎉 推荐系统启动完成！"
echo ""
echo "📱 前端访问地址: http://localhost:3000"
echo "🔧 后端API地址: http://localhost:5001"
echo "🏥 健康检查: http://localhost:5001/health"
echo ""
echo "按 Ctrl+C 停止服务"

# 捕获中断信号
trap 'echo ""; echo "🛑 正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo "✅ 服务已停止"; exit 0' INT

# 保持脚本运行
wait
