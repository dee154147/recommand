#!/bin/bash

echo "🔍 推荐系统状态检查"
echo "=================="

# 检查后端服务
echo "📦 后端服务状态:"
if curl -s "http://localhost:5002/health" > /dev/null; then
    echo "  ✅ 后端服务正常运行 (端口: 5002)"
    echo "  🌐 API地址: http://localhost:5002"
else
    echo "  ❌ 后端服务未运行"
fi

# 检查前端服务
echo ""
echo "🎨 前端服务状态:"
if curl -s "http://localhost:3000" > /dev/null; then
    echo "  ✅ 前端服务正常运行 (端口: 3000)"
    echo "  🌐 访问地址: http://localhost:3000"
else
    echo "  ❌ 前端服务未运行"
fi

# 检查混合分词策略
echo ""
echo "🧪 混合分词策略测试:"
response=$(curl -s "http://localhost:5002/api/v1/recommendation/semantic-search?q=%E7%A2%97%E5%85%B7&top_k=1")
if echo "$response" | grep -q '"count": [1-9]'; then
    echo "  ✅ 混合分词策略正常工作"
    echo "  📊 '碗具'搜索返回结果"
else
    echo "  ❌ 混合分词策略异常"
fi

# 显示进程信息
echo ""
echo "📋 进程信息:"
echo "  后端进程: $(lsof -ti:5002 2>/dev/null || echo '未找到')"
echo "  前端进程: $(lsof -ti:3000 2>/dev/null || echo '未找到')"

echo ""
echo "🎯 系统状态: 后台运行中"