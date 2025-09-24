#!/bin/bash

# 智能推荐系统停止脚本
# 使用方法: ./stop_system.sh

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛑 智能推荐系统停止脚本${NC}"
echo -e "${BLUE}================================${NC}"

# 停止后端服务
echo -e "${YELLOW}🔧 停止后端服务...${NC}"
pkill -f "python.*run.py" 2>/dev/null
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    kill $BACKEND_PID 2>/dev/null
    rm -f logs/backend.pid
fi
echo -e "${GREEN}✅ 后端服务已停止${NC}"

# 停止前端服务
echo -e "${YELLOW}🎨 停止前端服务...${NC}"
pkill -f "npm.*dev" 2>/dev/null
if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    kill $FRONTEND_PID 2>/dev/null
    rm -f logs/frontend.pid
fi
echo -e "${GREEN}✅ 前端服务已停止${NC}"

# 清理端口
echo -e "${YELLOW}🧹 清理端口...${NC}"
lsof -ti:5004 | xargs kill -9 2>/dev/null
lsof -ti:3001 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🎉 所有服务已停止${NC}"
echo -e "${BLUE}================================${NC}"
