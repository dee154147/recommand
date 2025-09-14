#!/bin/bash

echo "🔍 推荐系统访问问题诊断"
echo "========================"

echo "1. 检查服务进程状态:"
echo "-------------------"
ps aux | grep -E "(python3 run.py|npm run dev)" | grep -v grep

echo ""
echo "2. 检查端口监听状态:"
echo "-------------------"
lsof -i :5001 2>/dev/null || echo "❌ 端口 5001 未监听"
lsof -i :3000 2>/dev/null || echo "❌ 端口 3000 未监听"

echo ""
echo "3. 检查网络连接:"
echo "---------------"
echo "测试本地回环连接..."
ping -c 1 127.0.0.1 > /dev/null 2>&1 && echo "✅ 本地回环连接正常" || echo "❌ 本地回环连接失败"

echo ""
echo "4. 检查防火墙状态:"
echo "----------------"
if command -v pfctl > /dev/null 2>&1; then
    echo "macOS防火墙状态:"
    sudo pfctl -s info 2>/dev/null | head -3 || echo "无法检查防火墙状态"
fi

echo ""
echo "5. 检查系统代理设置:"
echo "------------------"
echo "HTTP代理: $http_proxy"
echo "HTTPS代理: $https_proxy"
echo "NO_PROXY: $no_proxy"

echo ""
echo "6. 尝试不同的访问方式:"
echo "-------------------"
echo "测试 127.0.0.1:5001..."
timeout 3 curl -s http://127.0.0.1:5001/health && echo "✅ 127.0.0.1 访问正常" || echo "❌ 127.0.0.1 访问失败"

echo "测试 localhost:5001..."
timeout 3 curl -s http://localhost:5001/health && echo "✅ localhost 访问正常" || echo "❌ localhost 访问失败"

echo ""
echo "7. 检查系统网络接口:"
echo "------------------"
ifconfig | grep -A 1 "inet 127.0.0.1" || echo "❌ 本地网络接口异常"

echo ""
echo "8. 建议的解决方案:"
echo "================="
echo "1. 重启网络服务: sudo dscacheutil -flushcache"
echo "2. 检查系统代理设置"
echo "3. 尝试使用 127.0.0.1 代替 localhost"
echo "4. 检查是否有其他软件占用端口"
echo "5. 重启系统网络服务"

echo ""
echo "9. 手动测试命令:"
echo "==============="
echo "curl -v http://127.0.0.1:5001/health"
echo "curl -v http://localhost:5001/health"
echo "telnet 127.0.0.1 5001"
