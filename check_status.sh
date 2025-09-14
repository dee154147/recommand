#!/bin/bash

# 推荐系统后台运行状态检查脚本

echo "🔍 推荐系统后台运行状态检查"
echo "================================"

# 检查后端服务
echo "📦 后端服务状态:"
if lsof -i :5001 > /dev/null 2>&1; then
    echo "✅ 后端服务运行中 (端口 5001)"
    echo "   进程ID: $(lsof -ti:5001 | head -1)"
    echo "   访问地址: http://localhost:5001"
    echo "   健康检查: http://localhost:5001/health"
else
    echo "❌ 后端服务未运行"
fi

echo ""

# 检查前端服务
echo "🎨 前端服务状态:"
if lsof -i :3000 > /dev/null 2>&1; then
    echo "✅ 前端服务运行中 (端口 3000)"
    echo "   进程ID: $(lsof -ti:3000 | head -1)"
    echo "   访问地址: http://localhost:3000"
else
    echo "❌ 前端服务未运行"
fi

echo ""

# 检查日志文件
echo "📋 日志文件状态:"
if [ -f "backend/backend.log" ]; then
    echo "✅ 后端日志文件存在: backend/backend.log"
    echo "   最后更新: $(ls -la backend/backend.log | awk '{print $6, $7, $8}')"
else
    echo "❌ 后端日志文件不存在"
fi

if [ -f "frontend/frontend.log" ]; then
    echo "✅ 前端日志文件存在: frontend/frontend.log"
    echo "   最后更新: $(ls -la frontend/frontend.log | awk '{print $6, $7, $8}')"
else
    echo "❌ 前端日志文件不存在"
fi

echo ""

# 显示系统访问信息
echo "🌐 系统访问信息:"
echo "   前端界面: http://localhost:3000"
echo "   后端API: http://localhost:5001"
echo "   健康检查: http://localhost:5001/health"
echo ""

# 显示管理命令
echo "🛠️  管理命令:"
echo "   查看日志: tail -f backend/backend.log"
echo "   查看日志: tail -f frontend/frontend.log"
echo "   停止服务: ./stop.sh"
echo "   重启服务: ./start.sh"
echo ""

# 检查是否有错误日志
echo "⚠️  错误检查:"
if [ -f "backend/backend.log" ] && grep -i "error\|exception\|traceback" backend/backend.log > /dev/null 2>&1; then
    echo "❌ 后端日志中发现错误"
    echo "   请运行: tail -20 backend/backend.log"
else
    echo "✅ 后端日志正常"
fi

if [ -f "frontend/frontend.log" ] && grep -i "error\|failed\|exception" frontend/frontend.log > /dev/null 2>&1; then
    echo "❌ 前端日志中发现错误"
    echo "   请运行: tail -20 frontend/frontend.log"
else
    echo "✅ 前端日志正常"
fi

echo ""
echo "🎉 系统后台运行状态检查完成"
