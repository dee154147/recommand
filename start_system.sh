#!/bin/bash

# 智能推荐系统一键启动脚本
# 使用方法: ./start_system.sh [--daemon]
# --daemon: 后台启动模式

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_DIR="/Users/liuzhichao/cursorProjects/recommand2"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}/frontend"

# 检查是否后台启动
DAEMON_MODE=false
if [[ "$1" == "--daemon" ]]; then
    DAEMON_MODE=true
fi

echo -e "${BLUE}🚀 智能推荐系统启动脚本${NC}"
echo -e "${BLUE}================================${NC}"

# 检查项目目录
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ 项目目录不存在: $PROJECT_DIR${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

# 检查依赖服务
echo -e "${YELLOW}🔍 检查系统依赖...${NC}"

# 检查PostgreSQL
if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
    echo -e "${RED}❌ PostgreSQL服务未运行，正在启动...${NC}"
    brew services start postgresql@14 2>/dev/null || {
        echo -e "${RED}❌ 无法启动PostgreSQL服务${NC}"
        echo -e "${YELLOW}请手动启动PostgreSQL: brew services start postgresql@14${NC}"
        exit 1
    }
    sleep 3
fi

# 检查Redis
if ! redis-cli ping >/dev/null 2>&1; then
    echo -e "${RED}❌ Redis服务未运行，正在启动...${NC}"
    brew services start redis 2>/dev/null || {
        echo -e "${RED}❌ 无法启动Redis服务${NC}"
        echo -e "${YELLOW}请手动启动Redis: brew services start redis${NC}"
        exit 1
    }
    sleep 2
fi

echo -e "${GREEN}✅ 依赖服务检查完成${NC}"

# 检查Python依赖
echo -e "${YELLOW}🐍 检查Python环境...${NC}"
if ! python3 -c "import flask, psycopg2, redis" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  正在安装Python依赖...${NC}"
    pip3 install -r backend/requirements.txt 2>/dev/null || {
        echo -e "${RED}❌ Python依赖安装失败${NC}"
        exit 1
    }
fi

# 检查Node.js依赖
echo -e "${YELLOW}📦 检查Node.js环境...${NC}"
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${YELLOW}⚠️  正在安装Node.js依赖...${NC}"
    cd "$FRONTEND_DIR"
    npm install 2>/dev/null || {
        echo -e "${RED}❌ Node.js依赖安装失败${NC}"
        exit 1
    }
    cd "$PROJECT_DIR"
fi

# 停止现有服务
echo -e "${YELLOW}🛑 停止现有服务...${NC}"
pkill -f "python.*run.py" 2>/dev/null
pkill -f "npm.*dev" 2>/dev/null
sleep 2

# 清理端口占用
echo -e "${YELLOW}🧹 清理端口占用...${NC}"
lsof -ti:5004 | xargs kill -9 2>/dev/null
lsof -ti:3001 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
sleep 2

# 启动后端服务
echo -e "${YELLOW}🔧 启动后端服务...${NC}"
cd "$BACKEND_DIR"
if [ "$DAEMON_MODE" = true ]; then
    nohup python3 run.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    echo -e "${GREEN}✅ 后端服务已启动 (PID: $BACKEND_PID)${NC}"
else
    python3 run.py &
    BACKEND_PID=$!
    echo -e "${GREEN}✅ 后端服务已启动 (PID: $BACKEND_PID)${NC}"
fi

# 等待后端启动
echo -e "${YELLOW}⏳ 等待后端服务启动...${NC}"
sleep 5

# 检查后端是否启动成功
for i in {1..10}; do
    if curl -s http://localhost:5004/health >/dev/null 2>&1; then
        echo -e "${GREEN}✅ 后端服务启动成功${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ 后端服务启动失败，请检查日志${NC}"
        if [ -f "logs/backend.log" ]; then
            echo -e "${YELLOW}📄 后端日志:${NC}"
            tail -10 logs/backend.log
        fi
        exit 1
    fi
    echo -e "${YELLOW}⏳ 等待后端服务... ($i/10)${NC}"
    sleep 2
done

# 启动前端服务
echo -e "${YELLOW}🎨 启动前端服务...${NC}"
cd "$FRONTEND_DIR"
if [ "$DAEMON_MODE" = true ]; then
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    echo -e "${GREEN}✅ 前端服务已启动 (PID: $FRONTEND_PID)${NC}"
else
    npm run dev &
    FRONTEND_PID=$!
    echo -e "${GREEN}✅ 前端服务已启动 (PID: $FRONTEND_PID)${NC}"
fi

# 等待前端启动
echo -e "${YELLOW}⏳ 等待前端服务启动...${NC}"
sleep 8

# 检查前端是否启动成功
for i in {1..10}; do
    if curl -s http://localhost:3001 >/dev/null 2>&1 || curl -s http://localhost:3000 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ 前端服务启动成功${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ 前端服务启动失败，请检查日志${NC}"
        if [ -f "logs/frontend.log" ]; then
            echo -e "${YELLOW}📄 前端日志:${NC}"
            tail -10 logs/frontend.log
        fi
        exit 1
    fi
    echo -e "${YELLOW}⏳ 等待前端服务... ($i/10)${NC}"
    sleep 2
done

# 创建日志目录
mkdir -p "$PROJECT_DIR/logs"

# 显示启动结果
echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🎉 系统启动成功！${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🌐 前端地址: http://localhost:3001${NC}"
echo -e "${GREEN}🔧 后端地址: http://localhost:5004${NC}"
echo -e "${GREEN}📊 健康检查: http://localhost:5004/health${NC}"
echo -e "${BLUE}================================${NC}"

if [ "$DAEMON_MODE" = true ]; then
    echo -e "${YELLOW}📝 后台模式启动完成${NC}"
    echo -e "${YELLOW}📋 进程ID已保存到 logs/ 目录${NC}"
    echo -e "${YELLOW}📄 日志文件: logs/backend.log, logs/frontend.log${NC}"
    echo -e "${YELLOW}🛑 停止服务: ./stop_system.sh${NC}"
else
    echo -e "${YELLOW}💡 按 Ctrl+C 停止所有服务${NC}"
    echo -e "${YELLOW}🛑 或运行: ./stop_system.sh${NC}"
fi

echo -e "${BLUE}================================${NC}"

# 如果不是后台模式，等待用户中断
if [ "$DAEMON_MODE" = false ]; then
    echo -e "${YELLOW}⏳ 服务运行中，按 Ctrl+C 停止...${NC}"
    trap 'echo -e "\n${YELLOW}🛑 正在停止服务...${NC}"; pkill -f "python.*run.py"; pkill -f "npm.*dev"; echo -e "${GREEN}✅ 服务已停止${NC}"; exit 0' INT
    wait
fi
